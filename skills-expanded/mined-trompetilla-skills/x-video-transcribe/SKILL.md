---
name: x-video-transcribe
description: Transcribe and summarize X/Twitter videos using bird CLI + Gemini audio transcription.
---

# X Video Transcribe

Transcribe X/Twitter video posts to text. Downloads the video, extracts audio, and uses Gemini for accurate transcription.

## When to use

- User shares an X/Twitter URL containing a video
- User asks to "transcribe this tweet" or "what does this video say"
- User wants a summary of an X video

## Usage

```bash
# Basic transcript
~/agent-workspace/skills/x-video-transcribe/scripts/transcribe.sh "https://x.com/user/status/123"

# With summary
~/agent-workspace/skills/x-video-transcribe/scripts/transcribe.sh "https://x.com/user/status/123" --summary

# Save to file
~/agent-workspace/skills/x-video-transcribe/scripts/transcribe.sh "https://x.com/user/status/123" --summary --output /tmp/transcript.md
```

## Pipeline

1. **bird CLI** — Fetches tweet JSON, extracts video URL
2. **curl** — Downloads the video MP4
3. **ffmpeg** — Extracts audio as MP3 (much smaller than video)
4. **Gemini API** — Uploads audio, transcribes with gemini-2.0-flash

## Requirements

- `bird` CLI with auth (cookies in `~/agent-workspace/secrets/bird.env`)
- `ffmpeg`
- `GEMINI_API_KEY` environment variable

## Environment

| Variable | Default | Description |
|----------|---------|-------------|
| `GEMINI_API_KEY` | (required) | Google Gemini API key |
| `BIRD_ENV` | `~/agent-workspace/secrets/bird.env` | Path to bird credentials |
| `GEMINI_MODEL` | `gemini-2.0-flash` | Gemini model for transcription |
