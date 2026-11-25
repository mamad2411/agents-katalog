---
name: Video Extract
description: Extract content from any video - transcripts (speech-to-text) and AI understanding (visual analysis). Supports YouTube, Loom, and local files. Use when user mentions transcript, transcribe, video analysis, understand video, get text from video, video summary, extract from video, watch video, screen recording analysis, YouTube transcript, Loom transcript, or whisper transcription.
---

# Video Extract

Extract content from any video source. Two modes based on depth needed:

- **Transcript** - Get the words (speech-to-text). Fast, cheap, works everywhere.
- **Understand** - AI watches the video (visual + audio analysis via Gemini). Deeper, slower.

## Quick Start

```bash
# Transcript from YouTube
uv run .claude/skills/video-extract/scripts/transcript.py "https://youtube.com/watch?v=VIDEO_ID"

# Transcript from local file
uv run .claude/skills/video-extract/scripts/transcript.py recording.mp4 --backend groq

# AI understanding (local or YouTube)
uv run .claude/skills/video-extract/scripts/understand.py video.mp4 --mode summary
uv run .claude/skills/video-extract/scripts/understand.py "https://youtube.com/watch?v=VIDEO_ID"
```

---

## Transcript Mode

Get the spoken words from any video as text.

### How It Works

| Source | Method |
|--------|--------|
| YouTube URL | yt-dlp -> APIFY -> Supadata (waterfall fallback) |
| Loom URL | yt-dlp |
| Local file | Groq Whisper API -> local Whisper fallback |

### YouTube / Loom Transcripts

```bash
# Basic transcript
uv run .claude/skills/video-extract/scripts/transcript.py "https://youtube.com/watch?v=VIDEO_ID"

# With timestamps
uv run .claude/skills/video-extract/scripts/transcript.py "https://youtube.com/watch?v=VIDEO_ID" --timestamps

# As JSON
uv run .claude/skills/video-extract/scripts/transcript.py "https://youtube.com/watch?v=VIDEO_ID" --json

# Loom
uv run .claude/skills/video-extract/scripts/transcript.py "https://www.loom.com/share/abc123"

# Save to file
uv run .claude/skills/video-extract/scripts/transcript.py "https://youtube.com/watch?v=VIDEO_ID" -o transcript.txt
```

### Local File Transcripts

```bash
# Default (Groq, recommended)
uv run .claude/skills/video-extract/scripts/transcript.py recording.mp4 --backend groq

# With language for better accuracy
uv run .claude/skills/video-extract/scripts/transcript.py interview.mp4 --backend groq --language it

# SRT subtitles
uv run .claude/skills/video-extract/scripts/transcript.py video.mp4 --backend groq --format srt -o subtitles.srt

# Local Whisper fallback (no API key needed, slow)
uv run .claude/skills/video-extract/scripts/transcript.py video.mp4 --backend local --model medium
```

### Transcript Options

| Option | Values | Notes |
|--------|--------|-------|
| `--backend` | groq (default), local | Local files only |
| `--format` | txt, srt, vtt, json | Local files only |
| `--language` | en, it, es, fr, de, zh | Local files only, improves accuracy |
| `--model` | whisper-large-v3-turbo (Groq), base/medium/large (local) | Local files only |
| `--timestamps` | flag | URL transcripts only |
| `--json` | flag | URL transcripts only |
| `--output/-o` | file path | Save to file |
| `--verbose/-v` | flag | Show progress details |

### Groq vs Local Whisper

| Aspect | Groq (Default) | Local |
|--------|---------------|-------|
| Speed | ~100x faster | Slow (CPU-bound) |
| Quality | whisper-large-v3-turbo | Depends on model |
| Cost | Free tier: 8hrs/day | Free, unlimited |
| Setup | GROQ_API_KEY | pip install faster-whisper |
| Large files | Auto-chunks >25MB | No limit |

**Always use `--backend groq` unless Groq is unavailable.**

### Channel Batch Fetch

Fetch all transcripts from a YouTube channel:

```bash
uv run .claude/skills/video-extract/scripts/fetch_channel.py "https://www.youtube.com/@channelname"

# Limit to recent videos
uv run .claude/skills/video-extract/scripts/fetch_channel.py "https://www.youtube.com/@channelname" --limit 10

# With timestamps, skip existing
uv run .claude/skills/video-extract/scripts/fetch_channel.py "https://www.youtube.com/@channelname" --timestamps --skip-existing
```

| Option | Default | Description |
|--------|---------|-------------|
| --limit | None | Most recent N videos |
| --output | workspace/docs/{date} | Output directory |
| --timestamps | false | Include timestamps |
| --skip-existing | false | Skip already-fetched videos |
| --concurrency | 3 | Parallel fetches |

---

## Understand Mode

AI-powered video analysis using Google Gemini. The model "watches" the video and provides structured analysis.

### Prerequisites

Set `GEMINI_API_KEY` environment variable. Get one at: https://aistudio.google.com/apikey

### Usage

```bash
# Summary (default) - key moments, topics, takeaways
uv run .claude/skills/video-extract/scripts/understand.py video.mp4

# Process extraction - step-by-step from screen recordings
uv run .claude/skills/video-extract/scripts/understand.py recording.mp4 --mode process

# Visual analysis - describe what's shown
uv run .claude/skills/video-extract/scripts/understand.py video.mp4 --mode visual

# YouTube URL (no download needed)
uv run .claude/skills/video-extract/scripts/understand.py "https://youtube.com/watch?v=VIDEO_ID"

# Save to file
uv run .claude/skills/video-extract/scripts/understand.py video.mp4 -o analysis.md
```

### Analysis Modes

| Mode | Best For | Returns |
|------|----------|---------|
| `summary` (default) | General understanding | Overview, key moments with timestamps, topics, takeaways |
| `process` | Screen recordings | Step-by-step instructions, prerequisites, data fields, automation notes |
| `visual` | What's shown visually | Scene descriptions, people, objects, UI elements, text on screen |

### Understand Options

| Option | Values | Notes |
|--------|--------|-------|
| `--mode/-m` | summary, process, visual | Analysis type |
| `--output/-o` | file path | Save to file |
| `--model` | gemini-2.5-flash (default) | Gemini model |
| `--low-res` | flag | For long videos (up to 3hrs) |
| `--fps` | float | Custom frame rate (e.g., 0.5) |
| `--no-waterfall` | flag | Disable auto-retry on token limits |

### Limits

| Limit | Value |
|-------|-------|
| File size | 100MB inline, larger auto-uploaded |
| Duration | 1 hour (default), 3 hours (low resolution) |
| Formats | mp4, mov, avi, webm, mpeg, wmv, flv, 3gpp |

---

## Environment Variables

| Variable | Required For | Description |
|----------|-------------|-------------|
| GROQ_API_KEY | Local file transcription | Groq API (free: https://console.groq.com) |
| GEMINI_API_KEY | Understanding mode | Google AI Studio (https://aistudio.google.com/apikey) |
| APIFY_API_KEY | YouTube fallback | APIFY cloud scraper |
| SUPADATA_API_KEY | YouTube fallback | Supadata API |

## System Requirements

- **yt-dlp**: `brew install yt-dlp` (for YouTube/Loom transcripts)
- **FFmpeg**: `brew install ffmpeg` (for local file audio extraction)
