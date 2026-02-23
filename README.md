# Audio Master Suite

Small desktop tool that batch-converts audio files into CD-friendly WAVs:

- 44.1 kHz
- 16-bit
- stereo PCM (`pcm_s16le`)

It writes to:

- `~/Desktop/Mastering_Queue`
- `Track_01.wav`, `Track_02.wav`, etc

This repo only handles conversion. Burning a disc depends on your OS and drive.

## Languages

- Python

## Tech

- PyQt6
- ffmpeg

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
