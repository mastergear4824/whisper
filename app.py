import os
import uuid
import whisper
import gc  # 가비지 컬렉션 모듈 추가
import time
import threading
import json
import torch
import numpy as np
import duckdb
import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory, session, g
from flask_babel import Babel, gettext as _, get_locale
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

# Flask 앱 초기화
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'mp3', 'wav', 'ogg', 'm4a', 'flac'}
# 용량 제한 해제 (로컬 애플리케이션용)
# app.config['MAX_CONTENT_LENGTH'] = 60 * 1024 * 1024  # 60MB 최대 파일 크기 (50MB 파일 + 여유 공간)
app.secret_key = 'whisper_secret_key'  # 세션을 위한 시크릿 키

# 지원하는 언어 목록 (Whisper 모델용)
SUPPORTED_LANGUAGES = {
    'auto': _('자동 감지'),
    'en': _('영어'),
    'ko': _('한국어'),
    'ja': _('일본어'),
    'zh': _('중국어'),
    'multilingual': _('다국어')
}

# 지원하는 UI 언어 목록
UI_LANGUAGES = {
    'ko': '한국어',
    'ja': '日本語',
    'en': 'English'
}

# Babel 설정
app.config['BABEL_DEFAULT_LOCALE'] = 'ko'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

def get_locale():
    # 사용자가 선택한 언어가 있으면 해당 언어 사용
    if 'language' in session:
        return session['language']
    # 없으면 요청 헤더의 Accept-Language를 기반으로 언어 선택
    return request.accept_languages.best_match(UI_LANGUAGES.keys())

babel = Babel(app, locale_selector=get_locale)

# 업로드 폴더가 없으면 생성
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 데이터베이스 폴더 설정
DB_FOLDER = 'data'
os.makedirs(DB_FOLDER, exist_ok=True)

# DuckDB 데이터베이스 초기화
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), DB_FOLDER, 'whisper_sessions.db')

def init_db():
    try:
        # 데이터베이스 디렉토리 확인 및 생성
        db_dir = os.path.dirname(DB_PATH)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
            app.logger.info(f"Created database directory: {db_dir}")
        
        conn = duckdb.connect(DB_PATH)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id VARCHAR PRIMARY KEY,
                filename VARCHAR,
                original_filename VARCHAR,
                language VARCHAR,
                result TEXT,
                created_at TIMESTAMP,
                audio_path VARCHAR
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS segments (
                id INTEGER PRIMARY KEY,
                session_id VARCHAR,
                start_time FLOAT,
                end_time FLOAT,
                text TEXT,
                FOREIGN KEY (session_id) REFERENCES sessions(id)
            )
        ''')
        conn.close()
        app.logger.info(f"Database initialized at {DB_PATH}")
        return True
    except Exception as e:
        app.logger.error(f"Error initializing database: {str(e)}")
        return False

# 데이터베이스 초기화 호출
try:
    db_initialized = init_db()
    if not db_initialized:
        app.logger.warning("Failed to initialize database. Session history will not be available.")
except Exception as e:
    app.logger.error(f"Failed to initialize database: {str(e)}")
    db_initialized = False

# Whisper 모델 로드 (처음 실행 시 모델을 다운로드할 수 있음)
model = None

# 진행 상황 추적을 위한 전역 변수
processing_tasks = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def load_model():
    global model
    if model is None:
        # 모델 크기는 'tiny', 'base', 'small', 'medium', 'large' 중 선택 가능
        # 더 큰 모델은 더 정확하지만 더 많은 리소스를 사용함
        # base에서 medium으로 업그레이드
        app.logger.info("Loading medium model...")
        model = whisper.load_model('medium')
        app.logger.info("Model loaded successfully")
    return model

# 세션 저장 함수
def save_session(task_id, filename, original_filename, language, result, segments, audio_path):
    if not db_initialized:
        app.logger.warning("Database not initialized. Session will not be saved.")
        return False
    
    try:
        conn = duckdb.connect(DB_PATH)
        
        # 세션 정보 저장
        conn.execute('''
            INSERT INTO sessions (id, filename, original_filename, language, result, created_at, audio_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (task_id, filename, original_filename, language, result, datetime.datetime.now(), audio_path))
        
        # 세그먼트 정보 저장
        for i, segment in enumerate(segments):
            conn.execute('''
                INSERT INTO segments (session_id, start_time, end_time, text)
                VALUES (?, ?, ?, ?)
            ''', (task_id, segment['start'], segment['end'], segment['text']))
        
        conn.close()
        app.logger.info(f"Session {task_id} saved to database")
        return True
    except Exception as e:
        app.logger.error(f"Error saving session to database: {str(e)}")
        return False

# 세션 목록 조회 함수
def get_sessions(limit=10):
    if not db_initialized:
        app.logger.warning("Database not initialized. Cannot retrieve sessions.")
        return []
    
    try:
        conn = duckdb.connect(DB_PATH)
        result = conn.execute('''
            SELECT id, original_filename, language, created_at, audio_path
            FROM sessions
            ORDER BY created_at DESC
            LIMIT ?
        ''', (limit,)).fetchall()
        
        sessions = []
        for row in result:
            sessions.append({
                'id': row[0],
                'filename': row[1],
                'language': row[2],
                'created_at': row[3].strftime('%Y-%m-%d %H:%M:%S') if row[3] else '',
                'audio_path': row[4]
            })
        
        conn.close()
        return sessions
    except Exception as e:
        app.logger.error(f"Error getting sessions from database: {str(e)}")
        return []

# 세션 상세 조회 함수
def get_session(session_id):
    if not db_initialized:
        app.logger.warning("Database not initialized. Cannot retrieve session.")
        return None
    
    try:
        conn = duckdb.connect(DB_PATH)
        
        # 세션 정보 조회
        session_result = conn.execute('''
            SELECT id, filename, original_filename, language, result, created_at, audio_path
            FROM sessions
            WHERE id = ?
        ''', (session_id,)).fetchone()
        
        if not session_result:
            conn.close()
            return None
        
        session = {
            'id': session_result[0],
            'filename': session_result[1],
            'original_filename': session_result[2],
            'language': session_result[3],
            'result': session_result[4],
            'created_at': session_result[5].strftime('%Y-%m-%d %H:%M:%S') if session_result[5] else '',
            'audio_path': session_result[6]
        }
        
        # 세그먼트 정보 조회
        segments_result = conn.execute('''
            SELECT start_time, end_time, text
            FROM segments
            WHERE session_id = ?
            ORDER BY start_time
        ''', (session_id,)).fetchall()
        
        segments = []
        for row in segments_result:
            segments.append({
                'start': row[0],
                'end': row[1],
                'text': row[2]
            })
        
        session['segments'] = segments
        
        conn.close()
        return session
    except Exception as e:
        app.logger.error(f"Error getting session from database: {str(e)}")
        return None

# 대용량 파일 처리를 위한 최적화된 transcribe 함수
def optimized_transcribe(model, audio_path, task_id, language='auto'):
    try:
        # 처리 시작 상태 업데이트
        update_task_status(task_id, _("시작됨"), 0)
        
        # 메모리 사용량을 줄이기 위한 설정
        options = {
            "fp16": False,  # 16비트 부동소수점 비활성화 (메모리 사용량 감소)
            "task": "transcribe",  # 음성-텍스트 변환 작업
            "beam_size": 1,  # 빔 크기 감소 (속도 향상)
        }
        
        # 언어 설정
        if language != 'auto' and language != 'multilingual':
            options["language"] = language
        
        # 음성 로드 중 상태 업데이트
        update_task_status(task_id, _("오디오 로드 중"), 10)
        time.sleep(0.5)  # 상태 업데이트가 보이도록 약간의 지연
        
        # 음성 분석 준비
        update_task_status(task_id, _("음성 분석 준비 중"), 20)
        time.sleep(0.5)
        
        # 음성을 텍스트로 변환 (진행 상황 업데이트를 위한 콜백 추가)
        update_task_status(task_id, _("음성 분석 중"), 30)
        
        # 실제 변환 작업 수행
        result = model.transcribe(audio_path, **options)
        
        # 변환 완료 후 상태 업데이트
        update_task_status(task_id, _("변환 완료"), 70)
        time.sleep(0.5)
        
        # 텍스트 후처리
        update_task_status(task_id, _("텍스트 후처리 중"), 90)
        processed_text = process_text_with_line_breaks(result["text"])
        result["text"] = processed_text
        
        # 세그먼트 정보 저장 (동기화에 사용)
        processing_tasks[task_id]["segments"] = extract_segments(result)
        
        # 처리 완료 상태 업데이트
        update_task_status(task_id, _("처리 완료"), 100)
        
        # 메모리 정리
        gc.collect()
        
        return result
    except Exception as e:
        # 오류 발생 시 상태 업데이트
        update_task_status(task_id, _("오류 발생: {}").format(str(e)), -1)
        raise e

# 세그먼트 추출 함수
def extract_segments(whisper_result):
    segments = whisper_result.get("segments", [])
    result_segments = []
    
    for segment in segments:
        result_segments.append({
            "start": segment["start"],
            "end": segment["end"],
            "text": segment["text"].strip()
        })
    
    return result_segments

# 문장 사이에 행 바꿈을 추가하는 함수
def process_text_with_line_breaks(text):
    import re
    
    # 문장 종료 패턴 (마침표, 물음표, 느낌표 등으로 끝나는 경우)
    sentence_end_pattern = r'([.!?])\s+'
    
    # 문장 종료 후 행 바꿈 추가
    processed_text = re.sub(sentence_end_pattern, r'\1\n\n', text)
    
    # 중복된 행 바꿈 제거
    processed_text = re.sub(r'\n{3,}', '\n\n', processed_text)
    
    return processed_text

# 비동기 처리를 위한 함수
def process_audio_async(model, filepath, task_id, original_filename):
    try:
        # 언어 설정 확인
        language = processing_tasks[task_id].get("language", "auto")
        
        result = optimized_transcribe(model, filepath, task_id, language)
        processing_tasks[task_id]["result"] = result["text"]
        processing_tasks[task_id]["completed"] = True
        
        # 오디오 파일 경로 저장 (재생에 사용)
        audio_filename = os.path.basename(filepath)
        processing_tasks[task_id]["audio_path"] = audio_filename
        
        # 세션 저장
        segments = processing_tasks[task_id].get("segments", [])
        try:
            if db_initialized:
                save_session(
                    task_id, 
                    audio_filename, 
                    original_filename,
                    language, 
                    result["text"], 
                    segments, 
                    audio_filename
                )
            else:
                app.logger.warning(f"Database not initialized. Session {task_id} will not be saved.")
        except Exception as e:
            app.logger.error(f"Error saving session: {str(e)}")
    except Exception as e:
        processing_tasks[task_id]["error"] = str(e)
        processing_tasks[task_id]["completed"] = True
        # 오류 발생 시 파일 삭제
        if os.path.exists(filepath):
            os.remove(filepath)

# 작업 상태 업데이트 함수
def update_task_status(task_id, status, progress):
    if task_id in processing_tasks:
        processing_tasks[task_id]["status"] = status
        processing_tasks[task_id]["progress"] = progress
        app.logger.info(f"Task {task_id}: {status} - {progress}%")

# 파일 크기 제한 초과 오류 처리 (용량 제한 해제로 사용되지 않지만 혹시 모를 경우를 대비해 유지)
@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    return jsonify({
        'error': _('파일 크기가 너무 큽니다.'),
        'code': 'FILE_TOO_LARGE'
    }), 413

# 모든 예외 처리
@app.errorhandler(Exception)
def handle_exception(e):
    # 디버그 모드에서도 항상 JSON 응답 반환
    app.logger.error(f"Unhandled exception: {str(e)}")
    return jsonify({'error': _('서버 오류가 발생했습니다: {}').format(str(e))}), 500

# 언어 변경 라우트
@app.route('/set_language/<language>')
def set_language(language):
    if language in UI_LANGUAGES:
        session['language'] = language
    return redirect(request.referrer or url_for('index'))

@app.route('/')
def index():
    try:
        # 최근 세션 목록 조회
        sessions = get_sessions(limit=5) if db_initialized else []
        return render_template('index.html', languages=SUPPORTED_LANGUAGES, ui_languages=UI_LANGUAGES, sessions=sessions)
    except Exception as e:
        app.logger.error(f"Error in index route: {str(e)}")
        return render_template('index.html', languages=SUPPORTED_LANGUAGES, ui_languages=UI_LANGUAGES, sessions=[])

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': _('파일이 없습니다')}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': _('선택된 파일이 없습니다')}), 400
    
    # 언어 설정 확인
    language = request.form.get('language', 'auto')
    if language not in SUPPORTED_LANGUAGES:
        language = 'auto'
    
    if file and allowed_file(file.filename):
        # 안전한 파일명으로 변환하고 고유 ID 추가
        original_filename = file.filename
        filename = secure_filename(file.filename)
        task_id = str(uuid.uuid4())
        unique_filename = f"{task_id}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # 파일 저장
        file.save(filepath)
        
        try:
            # Whisper 모델 로드
            model = load_model()
            
            # 작업 상태 초기화
            processing_tasks[task_id] = {
                "filename": unique_filename,
                "original_filename": original_filename,
                "status": _("대기 중"),
                "progress": 0,
                "completed": False,
                "result": None,
                "error": None,
                "start_time": time.time(),
                "language": language
            }
            
            # 비동기 처리 시작
            thread = threading.Thread(target=process_audio_async, args=(model, filepath, task_id, original_filename))
            thread.daemon = True
            thread.start()
            
            return jsonify({
                'success': True,
                'message': _('파일 처리가 시작되었습니다'),
                'task_id': task_id
            })
        except Exception as e:
            # 오류 발생 시 파일 삭제
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': _('처리 중 오류가 발생했습니다: {}').format(str(e))}), 500
    
    return jsonify({'error': _('허용되지 않는 파일 형식입니다')}), 400

@app.route('/status/<task_id>', methods=['GET'])
def get_task_status(task_id):
    if task_id not in processing_tasks:
        # 데이터베이스에서 세션 조회
        try:
            if db_initialized:
                session = get_session(task_id)
                if session:
                    return jsonify({
                        'completed': True,
                        'success': True,
                        'transcription': session['result'],
                        'status': _('처리 완료'),
                        'progress': 100,
                        'segments': session['segments'],
                        'audio_path': session['audio_path']
                    })
        except Exception as e:
            app.logger.error(f"Error retrieving session {task_id}: {str(e)}")
        
        return jsonify({'error': _('존재하지 않는 작업입니다')}), 404
    
    task = processing_tasks[task_id]
    
    # 작업이 완료되었고 오류가 없는 경우
    if task["completed"] and task["error"] is None:
        response = {
            'completed': True,
            'success': True,
            'transcription': task["result"],
            'status': task["status"],
            'progress': task["progress"]
        }
        
        # 세그먼트 정보가 있으면 추가
        if "segments" in task:
            response["segments"] = task["segments"]
        
        # 오디오 파일 경로가 있으면 추가
        if "audio_path" in task:
            response["audio_path"] = task["audio_path"]
        
        return jsonify(response)
    
    # 작업이 완료되었지만 오류가 있는 경우
    elif task["completed"] and task["error"] is not None:
        return jsonify({
            'completed': True,
            'success': False,
            'error': task["error"],
            'status': task["status"],
            'progress': task["progress"]
        })
    
    # 작업이 진행 중인 경우
    else:
        return jsonify({
            'completed': False,
            'status': task["status"],
            'progress': task["progress"],
            'elapsed_time': int(time.time() - task["start_time"])
        })

# 세션 상세 조회 API
@app.route('/session/<session_id>', methods=['GET'])
def get_session_api(session_id):
    try:
        if not db_initialized:
            return jsonify({'error': _('데이터베이스가 초기화되지 않았습니다')}), 500
            
        session = get_session(session_id)
        if session:
            return jsonify({
                'success': True,
                'session': session
            })
        return jsonify({'error': _('존재하지 않는 세션입니다')}), 404
    except Exception as e:
        app.logger.error(f"Error in get_session_api: {str(e)}")
        return jsonify({'error': _('세션 조회 중 오류가 발생했습니다: {}').format(str(e))}), 500

# 세션 목록 조회 API
@app.route('/sessions', methods=['GET'])
def get_sessions_api():
    try:
        if not db_initialized:
            return jsonify({'error': _('데이터베이스가 초기화되지 않았습니다')}), 500
            
        limit = request.args.get('limit', 10, type=int)
        sessions = get_sessions(limit=limit)
        return jsonify({
            'success': True,
            'sessions': sessions
        })
    except Exception as e:
        app.logger.error(f"Error in get_sessions_api: {str(e)}")
        return jsonify({'error': _('세션 목록 조회 중 오류가 발생했습니다: {}').format(str(e))}), 500

# 오래된 작업 정리 (선택적)
def cleanup_old_tasks():
    current_time = time.time()
    to_remove = []
    
    for task_id, task in processing_tasks.items():
        # 1시간 이상 지난 작업 정리
        if current_time - task["start_time"] > 3600:
            to_remove.append(task_id)
    
    for task_id in to_remove:
        del processing_tasks[task_id]

# 업로드된 오디오 파일 제공
@app.route('/audio/<filename>')
def serve_audio(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, port=5001) 