---
name: ig-research-transcribe
version: 1.0.0
description: |
  Transcribe state — runs Whisper on all downloaded audio files.
  Platform-agnostic: works with audio from Instagram, YouTube, Facebook, etc.
  Processes only files that don't already have a .txt transcript.

allowed-tools:
  - Bash
  - Read
---

# Social Research — Transcribe State

Transcribes all audio files in the project's `transcripts/` directory using OpenAI Whisper (tiny model for speed).

## Run

```bash
bash "$CLAUDE_SKILL_ROOT/scripts/transcribe.sh" <project-name> [sessionId]
```

## What it does

1. Finds all `.m4a`, `.mp3`, `.webm`, `.opus` files in `transcripts/`
2. Skips files that already have a matching `.txt`
3. Runs Whisper `tiny` model on each file
4. Saves transcripts as `.txt` files

## Performance

| Model | Speed   | Accuracy |
|-------|---------|----------|
| tiny  | Fastest | Good     |
| small | Medium  | Better   |
| medium| Slow    | Best     |

Edit `transcribe.sh` and change `--model tiny` to `--model small` or `--model medium` for better accuracy.

## Output

```
.ig-research/projects/<project-name>/transcripts/<postId>.txt
```
