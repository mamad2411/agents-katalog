---
name: Transcribe
description: Convert audio files (M4A, WAV, MP3) to Markdown transcripts. USE WHEN transcribe, audio to text, meeting recording, voice memo.
---

# Transcribe - Audio to Markdown

Convert audio files to clean Markdown transcripts. Auto-selects best backend.

## Usage

```
/transcribe <audio-file>
/transcribe <audio-file> --azure   # Force Azure gpt-4o-mini-transcribe (best quality)
/transcribe <audio-file> --groq    # Force Groq whisper-large-v3-turbo (fastest)
/transcribe <audio-file> --local   # Force local whisper.cpp (free)
```

## Auto-Selection Priority

1. **Azure** — if `AZURE_OPENAI_KEY` + `AZURE_OPENAI_ENDPOINT` set (gpt-4o-mini-transcribe, lowest WER)
2. **Groq** — if `GROQ_API_KEY` set (216x realtime, cheapest API)
3. **Local** — whisper.cpp fallback (free, ~1x realtime)

## Supported Formats
- M4A, WAV, MP3, FLAC, OGG, WEBM

## Workflow

When invoked, run:
```bash
~/.claude/skills/Transcribe/Tools/Transcribe.sh "<audio-file>" [--groq|--azure|--local]
```

Output saved to same directory as source: `{name}-transcript.md`

## Infrastructure

| Component | Path / Config |
|-----------|---------------|
| Transcribe.sh | `~/.claude/skills/Transcribe/Tools/Transcribe.sh` |
| Azure API | `AZURE_OPENAI_KEY`, `AZURE_OPENAI_ENDPOINT`, deployment: `gpt-4o-mini-transcribe` (default) with `whisper` fallback |
| Groq API | `GROQ_API_KEY` env var, model: whisper-large-v3-turbo |
| whisper-cli | `~/tools/whisper.cpp/build/bin/whisper-cli` |
| large-v3 model | `~/tools/whisper.cpp/models/ggml-large-v3.bin` |

## Cost Comparison

| Method | Cost | Speed | Quality | Best For |
|--------|------|-------|---------|----------|
| Azure (gpt-4o-mini-transcribe) | ~$0.30/hr | Fast | **Best** (lowest WER) | Default — best quality |
| Groq (turbo) | $0.04/hr | 216x realtime | Good | Bulk/fast transcription |
| Azure (whisper) | ~$0.36/hr | Fast | Good | Fallback |
| Local (large-v3) | FREE | ~1x realtime | Good | Offline, full privacy |
| Local (small.en) | FREE | ~3x faster | OK | Quick English drafts |

## Override Deployment

Set `AZURE_TRANSCRIBE_DEPLOYMENT` env var to use a different Azure deployment (e.g., `whisper` for old behavior).
