---
name: stt
description: Transcribe audio or video files to text locally on macOS using parakeet-mlx (NVIDIA Parakeet via Apple MLX). Use when the user asks to transcribe an audio/video file, get a transcript, generate subtitles/captions (srt/vtt), or convert speech in a file to text. Triggers on "transcribe this", "make a transcript", "get subtitles for", or pointing at an .mp3/.wav/.m4a/.mp4/.mov file with intent to extract speech. Apple Silicon only.
---

# Transcribe Audio

Local, offline transcription via `parakeet-mlx`. Requires Apple Silicon and `ffmpeg`. Resolve both commands with `command -v` before use and report a missing prerequisite instead of assuming an installation path.

## Run

```bash
parakeet-mlx <file>                          # → <file>.srt (default)
parakeet-mlx <file> --output-format txt      # plain text
parakeet-mlx <file> --output-format all      # txt + srt + vtt + json
parakeet-mlx *.mp3 --output-dir ~/transcripts # batch
```

Default output format is `srt`. Pass `--output-format txt` when the user wants plain prose, not subtitles. Output lands in the current dir unless `--output-dir` is set.

## Notes

- First run ever downloads the model (~600MB) from Hugging Face, then it's cached. Expect a one-time pause.
- Default model `mlx-community/parakeet-tdt-0.6b-v3` is multilingual (~25 languages). Override with `--model` if needed.
- Accepts audio and video (mp3/wav/m4a/mp4/mov/...); `ffmpeg` handles extraction.
- For languages outside Parakeet's set, fall back to `whisper-cli` (`brew install whisper-cpp`), which covers ~99 languages.
