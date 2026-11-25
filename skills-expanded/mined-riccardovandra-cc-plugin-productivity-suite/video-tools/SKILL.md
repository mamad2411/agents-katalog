---
name: Video Tools
description: FFmpeg utilities for video file manipulation. Convert formats (MP4, WebM) and extract audio tracks. Use when user mentions video conversion, format change, extract audio, mp4, webm, ffmpeg, or file format.
---

# Video Tools

FFmpeg utilities for converting video formats and extracting audio.

## Prerequisites

**FFmpeg** must be installed:
```bash
brew install ffmpeg    # macOS
apt-get install ffmpeg # Ubuntu/Debian
```

## Commands

### Extract Audio

```bash
uv run .claude/skills/video-tools/scripts/video_tools.py extract-audio video.mp4 audio.wav
uv run .claude/skills/video-tools/scripts/video_tools.py extract-audio video.mp4 audio.mp3 --format mp3
```

Options: `--format` (wav, mp3, aac, flac)

### Convert to MP4

```bash
uv run .claude/skills/video-tools/scripts/video_tools.py to-mp4 input.avi output.mp4
uv run .claude/skills/video-tools/scripts/video_tools.py to-mp4 input.mov output.mp4 --preset fast --crf 20
```

Options: `--codec` (libx264), `--preset` (ultrafast..veryslow), `--crf` (0-51, default 23)

### Convert to WebM

```bash
uv run .claude/skills/video-tools/scripts/video_tools.py to-webm input.mp4 output.webm
```

Options: `--codec` (libvpx, libvpx-vp9), `--crf` (0-63, default 30), `--bitrate` (default 1M)
