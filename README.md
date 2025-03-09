[Mastergear's Toy Project]

# Whisper 음성-텍스트 변환기 | 音声テキスト変換ツール | Speech-to-Text Converter

<div align="center">
  <h3>🌏 언어 선택 | 言語選択 | Language Selection</h3>
  <a href="#한국어">한국어</a> |
  <a href="#日本語">日本語</a> |
  <a href="#english">English</a>
</div>

---

<a id="한국어"></a>

## 🇰🇷 한국어

OpenAI의 Whisper 모델을 사용하여 음성 파일을 텍스트로 변환하는 웹 애플리케이션입니다.

### 주요 기능

- 다양한 오디오 파일 형식 지원 (MP3, WAV, OGG, M4A, FLAC)
- 드래그 앤 드롭 파일 업로드
- 변환된 텍스트 복사 기능
- 반응형 디자인
- 화자 구분 기능 (다중 화자 대화 구분)
- 오디오 재생과 텍스트 동기화 (하이라이트 및 자동 스크롤)
- 다국어 UI 지원 (한국어, 일본어, 영어)

---

<a id="日本語"></a>

## 🇯🇵 日本語

OpenAI の Whisper モデルを使用して、音声ファイルをテキストに変換するウェブアプリケーションです。

### 主な機能

- 様々な音声ファイル形式に対応 (MP3, WAV, OGG, M4A, FLAC)
- ドラッグ＆ドロップでのファイルアップロード
- 変換されたテキストのコピー機能
- レスポンシブデザイン
- 話者分離機能 (複数話者の会話を区別)
- 音声再生とテキスト同期 (ハイライトと自動スクロール)
- 多言語 UI サポート (韓国語、日本語、英語)

---

<a id="english"></a>

# Whisper Speech-to-Text Converter

A web application that converts audio files to text using OpenAI's Whisper model.

## Features

- Support for various audio file formats (MP3, WAV, OGG, M4A, FLAC)
- Drag and drop file upload
- Copy converted text functionality
- Responsive design
- Speaker differentiation (distinguishing between multiple speakers in conversations)
- Audio playback with text synchronization (highlighting and auto-scrolling)

## Installation Guide (For Beginners)

This section provides detailed installation instructions for MAC, Windows, and Linux operating systems.

### Common Requirements

- Python 3.10 or higher
- FFmpeg
- Conda (Miniconda or Anaconda)

### MAC OS Installation Guide

#### 1. Installing Python and Conda

1. **Install Miniconda**:
   - Download the macOS installer from the [Miniconda download page](https://docs.conda.io/en/latest/miniconda.html).
   - Run the downloaded `.pkg` file and follow the installation instructions.
   - After installation, open a terminal and verify the installation with:
     ```bash
     conda --version
     ```

#### 2. Installing FFmpeg

1. **Installation using Homebrew** (recommended):

   - If you don't have Homebrew installed, install it with:
     ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```
   - Install FFmpeg:
     ```bash
     brew install ffmpeg
     ```

2. **Manual installation**:
   - Download the macOS binary from the [FFmpeg download page](https://ffmpeg.org/download.html).
   - Extract and set up the path.

#### 3. Downloading the Project

1. **Download using Git** (recommended):

   ```bash
   git clone https://github.com/yourusername/whisper-transcription.git
   cd whisper-transcription
   ```

2. **Download as ZIP file**:
   - On the GitHub page, click the 'Code' button and select 'Download ZIP'.
   - Extract the downloaded ZIP file.
   - Open a terminal and navigate to the extracted folder:
     ```bash
     cd path_to_extracted_folder
     ```

#### 4. Setting Up Virtual Environment and Installing Packages

1. **Create and activate a virtual environment**:

   ```bash
   conda create -n whisper-env python=3.10
   conda activate whisper-env
   ```

2. **Install required packages**:

   ```bash
   pip install openai-whisper flask python-dotenv librosa
   ```

3. **Install additional packages for speaker differentiation** (optional):
   ```bash
   pip install pyannote.audio
   ```

#### 5. Running the Application

1. **Start the application**:

   ```bash
   python app.py
   ```

2. **Access in web browser**:
   - Open your browser and go to `http://127.0.0.1:4824` or `http://localhost:4824`.

### Windows Installation Guide

#### 1. Installing Python and Conda

1. **Install Miniconda**:
   - Download the Windows installer from the [Miniconda download page](https://docs.conda.io/en/latest/miniconda.html).
   - Run the downloaded `.exe` file and follow the installation instructions.
   - It's recommended to check the "Add Miniconda3 to my PATH environment variable" option.
   - After installation, open Anaconda Prompt and verify the installation with:
     ```bash
     conda --version
     ```

#### 2. Installing FFmpeg

1. **Download from the official site**:

   - Download the Windows binary from the [FFmpeg download page](https://ffmpeg.org/download.html).
   - Extract the downloaded file and note the location of the `bin` folder inside.
   - Add the FFmpeg `bin` folder path to your system's PATH environment variable:
     - Control Panel > System > Advanced System Settings > Environment Variables
     - In the 'System variables' section, find the 'Path' variable and edit it
     - Click 'New' and add the full path to the FFmpeg `bin` folder
     - Click OK to save

2. **Installation using Chocolatey** (alternative):
   - Run PowerShell as administrator.
   - If you don't have Chocolatey installed, install it with:
     ```powershell
     Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
     ```
   - Install FFmpeg:
     ```powershell
     choco install ffmpeg
     ```

#### 3. Downloading the Project

1. **Download using Git**:

   - Install [Git for Windows](https://gitforwindows.org/).
   - Open Git Bash or Command Prompt and run:
     ```bash
     git clone https://github.com/yourusername/whisper-transcription.git
     cd whisper-transcription
     ```

2. **Download as ZIP file**:
   - On the GitHub page, click the 'Code' button and select 'Download ZIP'.
   - Extract the downloaded ZIP file to your desired location.
   - Open Command Prompt and navigate to the extracted folder:
     ```bash
     cd path_to_extracted_folder
     ```

#### 4. Setting Up Virtual Environment and Installing Packages

1. **Create and activate a virtual environment**:

   - Open Anaconda Prompt and run:
     ```bash
     conda create -n whisper-env python=3.10
     conda activate whisper-env
     ```

2. **Install required packages**:

   ```bash
   pip install openai-whisper flask python-dotenv librosa
   ```

3. **Install additional packages for speaker differentiation** (optional):
   ```bash
   pip install pyannote.audio
   ```

#### 5. Running the Application

1. **Start the application**:

   - In Anaconda Prompt with the virtual environment activated, run:
     ```bash
     python app.py
     ```

2. **Access in web browser**:
   - Open your browser and go to `http://127.0.0.1:4824` or `http://localhost:4824`.

### Linux Installation Guide (Ubuntu/Debian based)

#### 1. Installing Python and Conda

1. **Install Miniconda**:

   ```bash
   # Download the installer
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

   # Give execute permission
   chmod +x Miniconda3-latest-Linux-x86_64.sh

   # Run the installer
   ./Miniconda3-latest-Linux-x86_64.sh
   ```

   - During installation, you'll be prompted to accept the license and confirm the installation path.
   - After installation, either restart your terminal or update your environment with:
     ```bash
     source ~/.bashrc
     ```
   - Verify the installation:
     ```bash
     conda --version
     ```

#### 2. Installing FFmpeg

1. **Installation using package manager**:

   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```

2. **Verify installation**:
   ```bash
   ffmpeg -version
   ```

#### 3. Downloading the Project

1. **Download using Git**:

   ```bash
   # Install Git if not already installed
   sudo apt install git

   # Clone the project
   git clone https://github.com/yourusername/whisper-transcription.git
   cd whisper-transcription
   ```

2. **Download as ZIP file**:

   ```bash
   # Install necessary tools
   sudo apt install wget unzip

   # Download the ZIP file (example GitHub URL)
   wget https://github.com/yourusername/whisper-transcription/archive/refs/heads/main.zip

   # Extract
   unzip main.zip

   # Navigate to the folder
   cd whisper-transcription-main
   ```

#### 4. Setting Up Virtual Environment and Installing Packages

1. **Create and activate a virtual environment**:

   ```bash
   conda create -n whisper-env python=3.10
   conda activate whisper-env
   ```

2. **Install required packages**:

   ```bash
   pip install openai-whisper flask python-dotenv librosa
   ```

3. **Install additional packages for speaker differentiation** (optional):
   ```bash
   pip install pyannote.audio
   ```

#### 5. Running the Application

1. **Start the application**:

   ```bash
   python app.py
   ```

2. **Access in web browser**:
   - Open your browser and go to `http://127.0.0.1:4824` or `http://localhost:4824`.

## How to Use

1. Access `http://localhost:4824` in your web browser

2. Upload or drag and drop an audio file

   - Supported formats: MP3, WAV, OGG, M4A, FLAC
   - Maximum file size: 60MB

3. Select the "Enable Speaker Differentiation" option if needed

   - Choose this option to distinguish between multiple speakers in a conversation

4. Check the conversion progress

   - You can monitor the processing status with the progress bar and status messages

5. Review the conversion results

   - Text results will be displayed with speaker differentiation
   - You can play the original audio using the audio player
   - During audio playback, the corresponding text will be highlighted

6. Use the copy text button to copy the results if needed

## Troubleshooting

### Common Issues

1. **"FFmpeg not found" error**

   - Verify that FFmpeg is correctly installed
   - Check that FFmpeg is added to your system PATH

2. **"No module named 'whisper'" error**

   - Ensure that your virtual environment is activated
   - Try reinstalling the package with `pip install openai-whisper`

3. **File upload errors**

   - Check that your file format is supported (MP3, WAV, OGG, M4A, FLAC)
   - Ensure that your file size is under 60MB

4. **Slow processing speed**
   - Large files may take longer to process
   - Processing speed can vary depending on your computer specifications
   - Try splitting into smaller audio files for processing

### Operating System Specific Issues

#### MAC OS

1. **FFmpeg installation issues**

   ```bash
   # Update Homebrew and try again
   brew update
   brew install ffmpeg
   ```

2. **Permission issues**
   ```bash
   # Grant write permissions to the project folder
   chmod -R 755 whisper-transcription
   ```

#### Windows

1. **FFmpeg path issues**

   - Restart your system to apply environment variable changes
   - Run `ffmpeg -version` in Command Prompt to verify the installation

2. **CUDA related errors** (when using GPU)
   - Install the latest NVIDIA drivers
   - Check that your CUDA version is compatible with PyTorch

#### Linux

1. **Library dependency issues**

   ```bash
   # Install necessary system libraries
   sudo apt update
   sudo apt install libsndfile1 libasound2-dev portaudio19-dev
   ```

2. **Permission issues**
   ```bash
   # Grant write permissions to the project folder
   chmod -R 755 whisper-transcription
   ```

## References

- [OpenAI Whisper](https://github.com/openai/whisper)
- [Flask](https://flask.palletsprojects.com/)
- [FFmpeg](https://ffmpeg.org/)
- [Conda](https://docs.conda.io/)
