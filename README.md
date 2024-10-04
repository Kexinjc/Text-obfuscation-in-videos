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
## Introduction
The rapid growth of audiovisual content on platforms like social media and streaming services has heightened privacy and data security concerns. Personal data, such as names and addresses, embedded in images and videos, can be unintentionally exposed, posing challenges, particularly in academic settings where regulations like GDPR apply. This is especially relevant in contexts such as tutorials and instructional videos created by educators, which may contain sensitive information, requiring careful handling to prevent privacy breaches.

To address these concerns, methods for obfuscating sensitive information have evolved. Machine learning, while effective, often requires large datasets and training, whereas rule-based systems offer a more interpretable solution.

In this paper, we present a system combining Microsoft Presidio for text anonymization with Tesseract OCR for text extraction. By blending rule-based and machine learning approaches, our system efficiently detects PII in Spanish multimedia, applying obfuscation to protect privacy while preserving the integrity of visual content. The system is adaptable, allowing for customized detection based on user-defined criteria.

## Flags

**-i **(input): This is a mandatory command that specifies the image or video file to be obfuscated.

**-o **(output): An optional command that defines the name of the output file. This file will be the result of the processing, containing the image or video with sensitive information anonymized.

**-r **(recognizers): Allows the selection of specific recognizers to be used for detecting sensitive information, such as ID numbers, phone numbers, etc. If no recognizer is specified, the system will use all available recognizers by default.

**-e **(exclude): This parameter allows users to indicate the recognizers they want to exclude from the process. This is useful for personalizing the analysis and focusing on certain types of sensitive information while ignoring others.

**-f** (filter): Used to obfuscate specific words that the user wants to protect. This option provides additional control over what information should be masked in the processed content.

**-u** (unfilter): Allows the de-obfuscation of words that were marked for obfuscation but which the user prefers not to hide in the final content.

**-v **(verbose): Activates verbose mode, providing detailed information about the internal detection and anonymization process. This option is particularly useful for debugging and monitoring, allowing users to gain a deeper understanding of the system’s operation.

**-t **(threshold): sets the threshold for reusing previous bounding boxes based on the percentage of change between frames.

# Text-obfuscation-in-videos
# Text-obfuscation-in-videos
