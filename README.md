# Whisper 음성 인식 웹 애플리케이션

# Whisper Speech Recognition Web Application

# Whisper 音声認識ウェブアプリケーション

## 소개 (Introduction / 紹介)

### 한국어

이 프로젝트는 OpenAI의 Whisper 모델을 활용한 음성 인식 웹 애플리케이션입니다. 사용자가 오디오 파일을 업로드하면 자동으로 텍스트로 변환하고, 결과를 세그먼트 단위로 표시합니다. 다국어 지원(영어, 한국어, 일본어)과 함께 사용자 인터페이스도 다양한 언어(한국어, 영어, 일본어)로 제공됩니다.

주요 기능:

- 다양한 오디오 파일 형식 지원 (mp3, wav, ogg, m4a, flac)
- 다국어 음성 인식
- 세그먼트 단위 텍스트 편집 및 저장
- 이전 변환 기록 저장 및 관리
- 다국어 사용자 인터페이스

### English

This project is a web application for speech recognition using OpenAI's Whisper model. When users upload audio files, the system automatically converts them to text and displays the results in segments. It supports multiple languages for transcription (English, Korean, Japanese) and provides a user interface in various languages (Korean, English, Japanese).

Key Features:

- Support for various audio file formats (mp3, wav, ogg, m4a, flac)
- multilingual speech recognition
- Segment-level text editing and saving
- Storage and management of previous conversion records
- Multilingual user interface

### 日本語

このプロジェクトは、OpenAI の Whisper モデルを活用した音声認識ウェブアプリケーションです。ユーザーがオーディオファイルをアップロードすると、自動的にテキストに変換し、結果をセグメント単位で表示します。多言語対応（英語、韓国語、日本語）とともに、ユーザーインターフェースも様々な言語（韓国語、英語、日本語）で提供されます。

主な機能：

- 様々なオーディオファイル形式のサポート（mp3、wav、ogg、m4a、flac）
- 多言語音声認識
- セグメント単位のテキスト編集と保存
- 過去の変換履歴の保存と管理
- 多言語ユーザーインターフェース

## 설치 방법 (Installation Guide / インストール方法)

### 한국어

#### 사전 요구사항

- Python 3.8 이상
- pip (Python 패키지 관리자) 또는 Conda
- Git
- FFmpeg (오디오 처리용)

#### 1. 저장소 복제

```bash
git clone https://github.com/yourusername/whisper.git
cd whisper
```

#### 2. 설치 방법 (두 가지 옵션)

##### 옵션 A: 가상 환경 설정 (venv 사용)

```bash
# 가상 환경 생성
python -m venv venv

# 가상 환경 활성화
# Windows의 경우:
venv\Scripts\activate
# macOS/Linux의 경우:
source venv/bin/activate

# 의존성 설치
pip install flask flask-babel torch numpy whisper duckdb werkzeug
```

##### 옵션 B: Conda 환경 설정 (environment.yml 사용)

```bash
# environment.yml 파일이 있는 경우
conda env create -f environment.yml

# 환경 활성화
conda activate whisper

# 또는 직접 환경 생성
conda create -n whisper python=3.10
conda activate whisper
conda install -c conda-forge flask flask-babel numpy
pip install torch whisper duckdb
```

#### 3. FFmpeg 설치

- **Windows**: [FFmpeg 공식 사이트](https://ffmpeg.org/download.html)에서 다운로드하여 설치하고 PATH에 추가
- **macOS**: `brew install ffmpeg`
- **Linux (Ubuntu/Debian)**: `sudo apt-get install ffmpeg`

#### 4. 디렉토리 구조 설정

```bash
# 업로드 폴더 생성
mkdir -p static/uploads
```

#### 5. 애플리케이션 실행

```bash
python app.py
```

#### 6. 웹 브라우저에서 접속

웹 브라우저를 열고 `http://localhost:4824`으로 접속하세요.

### English

#### Prerequisites

- Python 3.8 or higher
- pip (Python package manager) or Conda
- Git
- FFmpeg (for audio processing)

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/whisper.git
cd whisper
```

#### 2. Installation Methods (Two Options)

##### Option A: Set Up Virtual Environment (using venv)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# For Windows:
venv\Scripts\activate
# For macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install flask flask-babel torch numpy whisper duckdb werkzeug
```

##### Option B: Set Up Conda Environment (using environment.yml)

```bash
# If environment.yml file is available
conda env create -f environment.yml

# Activate the environment
conda activate whisper

# Or create environment manually
conda create -n whisper python=3.10
conda activate whisper
conda install -c conda-forge flask flask-babel numpy
pip install torch whisper duckdb
```

#### 3. Install FFmpeg

- **Windows**: Download from [FFmpeg official site](https://ffmpeg.org/download.html) and add to PATH
- **macOS**: `brew install ffmpeg`
- **Linux (Ubuntu/Debian)**: `sudo apt-get install ffmpeg`

#### 4. Set Up Directory Structure

```bash
# Create uploads folder
mkdir -p static/uploads
```

#### 5. Run the Application

```bash
python app.py
```

#### 6. Access in Web Browser

Open your web browser and navigate to `http://localhost:4824`.

### 日本語

#### 前提条件

- Python 3.8 以上
- pip (Python パッケージマネージャー) または Conda
- Git
- FFmpeg (オーディオ処理用)

#### 1. リポジトリのクローン

```bash
git clone https://github.com/yourusername/whisper.git
cd whisper
```

#### 2. インストール方法（2 つのオプション）

##### オプション A: 仮想環境のセットアップ（venv を使用）

```bash
# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化
# Windowsの場合：
venv\Scripts\activate
# macOS/Linuxの場合：
source venv/bin/activate

# 依存関係のインストール
pip install flask flask-babel torch numpy whisper duckdb werkzeug
```

##### オプション B: Conda 環境のセットアップ（environment.yml を使用）

```bash
# environment.ymlファイルがある場合
conda env create -f environment.yml

# 環境の有効化
conda activate whisper

# または手動で環境を作成
conda create -n whisper python=3.10
conda activate whisper
conda install -c conda-forge flask flask-babel numpy
pip install torch whisper duckdb
```

#### 3. FFmpeg のインストール

- **Windows**: [FFmpeg 公式サイト](https://ffmpeg.org/download.html)からダウンロードしてインストールし、PATH に追加
- **macOS**: `brew install ffmpeg`
- **Linux (Ubuntu/Debian)**: `sudo apt-get install ffmpeg`

#### 4. ディレクトリ構造のセットアップ

```bash
# アップロードフォルダの作成
mkdir -p static/uploads
```

#### 5. アプリケーションの実行

```bash
python app.py
```

#### 6. ウェブブラウザでアクセス

ウェブブラウザを開き、`http://localhost:4824`にアクセスしてください。

## 사용 방법 (Usage Guide / 使用方法)

### 한국어

1. 웹 브라우저에서 애플리케이션에 접속합니다.
2. 인식할 언어를 선택합니다.
3. 오디오 파일을 업로드 영역에 드래그 앤 드롭하거나 파일 선택 버튼을 클릭하여 선택하여 음성 인식을 시작합니다.
4. 변환이 완료되면 결과가 세그먼트 단위로 표시됩니다.
5. 필요한 경우 텍스트를 편집하고 저장할 수 있습니다.
6. 이전 변환 기록은 메인 페이지에서 확인할 수 있습니다.

### English

1. Access the application through your web browser.
2. Select the language for recognition.
3. Start speech recognition by dragging and dropping an audio file to the upload area or clicking the file selection button.
4. Once the conversion is complete, results will be displayed in segments.
5. You can edit and save the text if needed.
6. Previous conversion records can be viewed on the main page.

### 日本語

1. ウェブブラウザでアプリケーションにアクセスします。
2. 認識する言語を選択します。
3. オーディオファイルをアップロードエリアにドラッグ＆ドロップするか、ファイル選択ボタンをクリックして選択し、音声認識を開始します。
4. 変換が完了すると、結果がセグメント単位で表示されます。
5. 必要に応じてテキストを編集して保存できます。
6. 過去の変換履歴はメインページで確認できます。

## 라이센스 (License / ライセンス)

이 프로젝트는 MIT 라이센스 하에 배포됩니다. 자세한 내용은 LICENSE 파일을 참조하세요.

This project is distributed under the MIT License. See the LICENSE file for more details.

このプロジェクトは MIT ライセンスの下で配布されています。詳細は LICENSE ファイルを参照してください。
