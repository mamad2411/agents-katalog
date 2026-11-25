# MEGA Transcriber Skill (Local Whisper)

> **QUICK REFERENCE**
> - **Output folder**: `output/transcripts/`
> - **Transcribe script**: `.venv\Scripts\python.exe scripts/mega/transcribe.py`
> - **Supported formats**: mp4, mp3, wav, m4a, webm, mkv, flac, ogg, aac
> - **Prerequisites**: FFmpeg on PATH + `pip install openai-whisper torch`
> - **File naming**: `YYYY-MM-DD_filename_transcript.txt` and `_transcript.json`
> - **Python**: ALWAYS use `.venv\Scripts\python.exe` (never bare `python`)

## Purpose
Transcribe audio and video files locally using OpenAI Whisper.
Outputs plain text and timestamped JSON transcripts.

## Trigger Phrases
- "transcribe this video", "transcribe audio", "convert speech to text"
- "transcribe my recording", "get transcript from video"
- `/content transcribe`

## Supported Formats
mp4, mp3, wav, m4a, webm, mkv, flac, ogg, aac

## Prerequisites
- FFmpeg installed and on PATH
- Python packages: `openai-whisper`, `torch` (install via `pip install openai-whisper torch`)

## 3-Mode Workflow

### PLAN Mode
1. Check whisper is available:
   ```python
   python -c "import whisper; print('OK')"
   ```
2. If not installed → tell user: `pip install openai-whisper torch`
3. Check FFmpeg: `ffmpeg -version`
4. Identify input file(s) — single file or batch from a folder

### CLARIFY Mode
- Ask: Which file or folder to transcribe?
- Ask: Which Whisper model? Options:
  - `tiny` — Fastest, least accurate (~1GB VRAM)
  - `base` — Good balance (default) (~1GB VRAM)
  - `small` — Better accuracy (~2GB VRAM)
  - `medium` — High accuracy (~5GB VRAM)
  - `large` — Best accuracy (~10GB VRAM)
- Ask: Language? (default: auto-detect)
- Ask: Output format? (default: both .txt and .json)

### IMPLEMENT Mode
Run the transcription script:
```bash
python scripts/mega/transcribe.py --input "path/to/file.mp4" --model base --output references/transcripts/auto-transcribed/
```

For batch:
```bash
python scripts/mega/transcribe.py --input "path/to/folder/" --model base --output references/transcripts/auto-transcribed/ --batch
```

## Output
- `.txt` — Plain text transcript
- `.json` — Timestamped segments with start/end times
- Default location: `references/transcripts/auto-transcribed/`
- Alternative: `output/transcripts/`

## Notes
- First run downloads the model (~140MB for base, ~2.9GB for large)
- GPU (CUDA) used automatically if available, falls back to CPU
- CPU transcription is slower but works on any machine
