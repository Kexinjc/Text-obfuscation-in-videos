## Pre-requisites
- Python 3.8 or higher
- Tesseract OCR

## Installation

1. Create virtual environment
```bash
python3 -m venv .venv
```

2. Activate virtual environment
```bash
source .venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Add environment variables
```bash
# for MacOS
export TESSERACT_PATH='/opt/homebrew/bin/tesseract'
export FFMPEG_PATH='/opt/homebrew/bin/ffmpeg'
# for Windows
$env:TESSERACT_PATH = 'C:\Program Files\Tesseract-OCR\tesseract.exe'
$env:FFMPEG_PATH = 'C:\Program Files\ffmpeg\bin\ffmpeg.exe'
```

4. Run the application
```bash
python3 main.py
```
# Text-obfuscation-in-videos
# Text-obfuscation-in-videos
