# Audio Master Suite

Small desktop tool that batch-converts audio files into CD WAVs, only handles conversion.

- 44.1 kHz
- 16-bit
- stereo PCM (`pcm_s16le`)

Output folder:

- `~/Desktop/Mastering_Queue`
- Files are named `Track_01.wav`, `Track_02.wav`, etc

## Requirements

- Python 3.10+
- `ffmpeg` on your PATH
- PyQt6

## Setup (macOS)

```bash
brew install ffmpeg
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python audio_master_suite.py
