---
name: transcribe-tool
description: >-
  Audio transcription tool. Converts audio files to text using Whisper, with optional LLM post-processing as needed.
  Use when: Use when: transcribing meeting recordings, podcast transcripts, or when text extraction from audio files is required.
tags: [audio, transcription, whisper, external]
---


# Transcribe Tool

Audio transcription tool using Whisper (faster-whisper).

## Invocation

**Bash**: Run with `animaworks-tool transcribe transcribe <音声ファイル> [オプション]`

### audio — Audio Transcription
```bash
animaworks-tool transcribe transcribe audio_file.wav [-l ja] [-m large-v3-turbo]
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| audio_path | string | (required) | Path to the audio file |
| language | string | null | Language code (e.g., ja, en). Auto-detected if null |
| model | string | "large-v3-turbo" | Whisper model name |
| raw | boolean | false | If true, skips LLM post-processing |

## CLI Usage

```bash
animaworks-tool transcribe transcribe audio_file.wav [-l ja] [-m large-v3-turbo]
```

## Notes

- faster-whisper must be installed
- When using GPU, CUDA-compatible ctranslate2 is required
- The model is automatically downloaded on first run
