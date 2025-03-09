# Whisper 음성-텍스트 변환기

OpenAI의 Whisper 모델을 사용하여 음성 파일을 텍스트로 변환하는 웹 애플리케이션입니다.

## 기능

- 다양한 오디오 파일 형식 지원 (MP3, WAV, OGG, M4A, FLAC)
- 드래그 앤 드롭 파일 업로드
- 변환된 텍스트 복사 기능
- 반응형 디자인
- 화자 구분 기능 (다중 화자 대화 구분)
- 오디오 재생과 텍스트 동기화 (하이라이트 및 자동 스크롤)

## 설치 가이드 (초보자용)

이 섹션에서는 MAC, Windows, Linux 각 운영체제별로 설치 방법을 자세히 설명합니다.

### 공통 요구사항

- Python 3.10 이상
- FFmpeg
- Conda (Miniconda 또는 Anaconda)

### MAC OS 설치 가이드

#### 1. Python 및 Conda 설치

1. **Miniconda 설치**:
   - [Miniconda 다운로드 페이지](https://docs.conda.io/en/latest/miniconda.html)에서 macOS용 설치 파일을 다운로드합니다.
   - 다운로드한 `.pkg` 파일을 실행하고 설치 지침을 따릅니다.
   - 설치가 완료되면 터미널을 열고 다음 명령어로 설치를 확인합니다:
     ```bash
     conda --version
     ```

#### 2. FFmpeg 설치

1. **Homebrew를 사용한 설치** (권장):

   - Homebrew가 설치되어 있지 않다면 다음 명령어로 설치합니다:
     ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```
   - FFmpeg 설치:
     ```bash
     brew install ffmpeg
     ```

2. **수동 설치**:
   - [FFmpeg 다운로드 페이지](https://ffmpeg.org/download.html)에서 macOS용 바이너리를 다운로드합니다.
   - 압축을 풀고 경로를 설정합니다.

#### 3. 프로젝트 다운로드

1. **Git을 사용한 다운로드** (권장):

   ```bash
   git clone https://github.com/yourusername/whisper-transcription.git
   cd whisper-transcription
   ```

2. **ZIP 파일로 다운로드**:
   - GitHub 페이지에서 'Code' 버튼을 클릭하고 'Download ZIP'을 선택합니다.
   - 다운로드한 ZIP 파일을 압축 해제합니다.
   - 터미널을 열고 압축 해제한 폴더로 이동합니다:
     ```bash
     cd 압축해제한_폴더_경로
     ```

#### 4. 가상 환경 설정 및 패키지 설치

1. **가상 환경 생성 및 활성화**:

   ```bash
   conda create -n whisper-env python=3.10
   conda activate whisper-env
   ```

2. **필요한 패키지 설치**:

   ```bash
   pip install openai-whisper flask python-dotenv librosa
   ```

3. **화자 구분 기능을 위한 추가 패키지 설치** (선택사항):
   ```bash
   pip install pyannote.audio
   ```

#### 5. 애플리케이션 실행

1. **애플리케이션 시작**:

   ```bash
   python app.py
   ```

2. **웹 브라우저에서 접속**:
   - 브라우저를 열고 `http://127.0.0.1:5000` 또는 `http://localhost:5000`으로 접속합니다.

### Windows 설치 가이드

#### 1. Python 및 Conda 설치

1. **Miniconda 설치**:
   - [Miniconda 다운로드 페이지](https://docs.conda.io/en/latest/miniconda.html)에서 Windows용 설치 파일을 다운로드합니다.
   - 다운로드한 `.exe` 파일을 실행하고 설치 지침을 따릅니다.
   - "Add Miniconda3 to my PATH environment variable" 옵션을 체크하는 것이 좋습니다.
   - 설치가 완료되면 Anaconda Prompt를 열고 다음 명령어로 설치를 확인합니다:
     ```bash
     conda --version
     ```

#### 2. FFmpeg 설치

1. **공식 사이트에서 다운로드**:

   - [FFmpeg 다운로드 페이지](https://ffmpeg.org/download.html)에서 Windows용 바이너리를 다운로드합니다.
   - 다운로드한 파일을 압축 해제하고 내부의 `bin` 폴더를 기억해둡니다.
   - 시스템 환경 변수 PATH에 FFmpeg `bin` 폴더 경로를 추가합니다:
     - 제어판 > 시스템 > 고급 시스템 설정 > 환경 변수
     - '시스템 변수' 섹션에서 'Path' 변수를 찾아 편집
     - '새로 만들기'를 클릭하고 FFmpeg `bin` 폴더의 전체 경로를 추가
     - 확인을 클릭하여 저장

2. **Chocolatey를 사용한 설치** (대안):
   - 관리자 권한으로 PowerShell을 실행합니다.
   - Chocolatey가 설치되어 있지 않다면 다음 명령어로 설치합니다:
     ```powershell
     Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
     ```
   - FFmpeg 설치:
     ```powershell
     choco install ffmpeg
     ```

#### 3. 프로젝트 다운로드

1. **Git을 사용한 다운로드**:

   - [Git for Windows](https://gitforwindows.org/)를 설치합니다.
   - Git Bash 또는 명령 프롬프트를 열고 다음 명령어를 실행합니다:
     ```bash
     git clone https://github.com/yourusername/whisper-transcription.git
     cd whisper-transcription
     ```

2. **ZIP 파일로 다운로드**:
   - GitHub 페이지에서 'Code' 버튼을 클릭하고 'Download ZIP'을 선택합니다.
   - 다운로드한 ZIP 파일을 원하는 위치에 압축 해제합니다.
   - 명령 프롬프트를 열고 압축 해제한 폴더로 이동합니다:
     ```bash
     cd 압축해제한_폴더_경로
     ```

#### 4. 가상 환경 설정 및 패키지 설치

1. **가상 환경 생성 및 활성화**:

   - Anaconda Prompt를 열고 다음 명령어를 실행합니다:
     ```bash
     conda create -n whisper-env python=3.10
     conda activate whisper-env
     ```

2. **필요한 패키지 설치**:

   ```bash
   pip install openai-whisper flask python-dotenv librosa
   ```

3. **화자 구분 기능을 위한 추가 패키지 설치** (선택사항):
   ```bash
   pip install pyannote.audio
   ```

#### 5. 애플리케이션 실행

1. **애플리케이션 시작**:

   - Anaconda Prompt에서 가상 환경이 활성화된 상태로 다음 명령어를 실행합니다:
     ```bash
     python app.py
     ```

2. **웹 브라우저에서 접속**:
   - 브라우저를 열고 `http://127.0.0.1:5000` 또는 `http://localhost:5000`으로 접속합니다.

### Linux 설치 가이드 (Ubuntu/Debian 기준)

#### 1. Python 및 Conda 설치

1. **Miniconda 설치**:

   ```bash
   # 설치 파일 다운로드
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

   # 실행 권한 부여
   chmod +x Miniconda3-latest-Linux-x86_64.sh

   # 설치 실행
   ./Miniconda3-latest-Linux-x86_64.sh
   ```

   - 설치 중 라이선스 동의 및 설치 경로 확인 메시지가 나타납니다.
   - 설치가 완료되면 터미널을 다시 열거나 다음 명령어로 환경을 업데이트합니다:
     ```bash
     source ~/.bashrc
     ```
   - 설치 확인:
     ```bash
     conda --version
     ```

#### 2. FFmpeg 설치

1. **패키지 관리자를 사용한 설치**:

   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```

2. **설치 확인**:
   ```bash
   ffmpeg -version
   ```

#### 3. 프로젝트 다운로드

1. **Git을 사용한 다운로드**:

   ```bash
   # Git이 설치되어 있지 않다면 설치
   sudo apt install git

   # 프로젝트 클론
   git clone https://github.com/yourusername/whisper-transcription.git
   cd whisper-transcription
   ```

2. **ZIP 파일로 다운로드**:

   ```bash
   # 필요한 도구 설치
   sudo apt install wget unzip

   # ZIP 파일 다운로드 (GitHub URL 예시)
   wget https://github.com/yourusername/whisper-transcription/archive/refs/heads/main.zip

   # 압축 해제
   unzip main.zip

   # 폴더로 이동
   cd whisper-transcription-main
   ```

#### 4. 가상 환경 설정 및 패키지 설치

1. **가상 환경 생성 및 활성화**:

   ```bash
   conda create -n whisper-env python=3.10
   conda activate whisper-env
   ```

2. **필요한 패키지 설치**:

   ```bash
   pip install openai-whisper flask python-dotenv librosa
   ```

3. **화자 구분 기능을 위한 추가 패키지 설치** (선택사항):
   ```bash
   pip install pyannote.audio
   ```

#### 5. 애플리케이션 실행

1. **애플리케이션 시작**:

   ```bash
   python app.py
   ```

2. **웹 브라우저에서 접속**:
   - 브라우저를 열고 `http://127.0.0.1:5000` 또는 `http://localhost:5000`으로 접속합니다.

## 사용 방법

1. 웹 브라우저에서 `http://localhost:5000` 접속

2. 음성 파일을 업로드하거나 드래그 앤 드롭

   - 지원 형식: MP3, WAV, OGG, M4A, FLAC
   - 최대 파일 크기: 60MB

3. 필요에 따라 "화자 구분 활성화" 옵션 선택

   - 다중 화자가 있는 대화를 구분하려면 이 옵션을 선택하세요

4. 변환 진행 상황 확인

   - 진행 바와 상태 메시지로 처리 상황을 확인할 수 있습니다

5. 변환 결과 확인

   - 텍스트 결과가 화자별로 구분되어 표시됩니다
   - 오디오 플레이어로 원본 오디오를 재생할 수 있습니다
   - 오디오 재생 시 현재 위치에 해당하는 텍스트가 하이라이트됩니다

6. 필요시 텍스트 복사 버튼을 사용하여 결과 복사

## 문제 해결

### 일반적인 문제

1. **"FFmpeg not found" 오류**

   - FFmpeg가 올바르게 설치되었는지 확인하세요
   - 시스템 PATH에 FFmpeg가 추가되었는지 확인하세요

2. **"No module named 'whisper'" 오류**

   - 가상 환경이 활성화되었는지 확인하세요
   - `pip install openai-whisper` 명령으로 패키지를 다시 설치해보세요

3. **파일 업로드 오류**

   - 파일 형식이 지원되는지 확인하세요 (MP3, WAV, OGG, M4A, FLAC)
   - 파일 크기가 60MB 이하인지 확인하세요

4. **처리 속도가 느린 경우**
   - 대용량 파일은 처리 시간이 길어질 수 있습니다
   - 컴퓨터 사양에 따라 처리 속도가 달라질 수 있습니다
   - 더 작은 오디오 파일로 분할하여 처리해보세요

### 운영체제별 문제

#### MAC OS

1. **FFmpeg 설치 문제**

   ```bash
   # Homebrew 업데이트 후 다시 시도
   brew update
   brew install ffmpeg
   ```

2. **권한 문제**
   ```bash
   # 프로젝트 폴더에 쓰기 권한 부여
   chmod -R 755 whisper-transcription
   ```

#### Windows

1. **FFmpeg 경로 문제**

   - 시스템을 재부팅하여 환경 변수 변경사항을 적용하세요
   - 명령 프롬프트에서 `ffmpeg -version`을 실행하여 설치를 확인하세요

2. **CUDA 관련 오류** (GPU 사용 시)
   - 최신 NVIDIA 드라이버를 설치하세요
   - CUDA 버전이 PyTorch와 호환되는지 확인하세요

#### Linux

1. **라이브러리 의존성 문제**

   ```bash
   # 필요한 시스템 라이브러리 설치
   sudo apt update
   sudo apt install libsndfile1 libasound2-dev portaudio19-dev
   ```

2. **권한 문제**
   ```bash
   # 프로젝트 폴더에 쓰기 권한 부여
   chmod -R 755 whisper-transcription
   ```

## 참고 자료

- [OpenAI Whisper](https://github.com/openai/whisper)
- [Flask](https://flask.palletsprojects.com/)
- [FFmpeg](https://ffmpeg.org/)
- [Conda](https://docs.conda.io/)
