---
name: audio-transcribe
description: Transcribe audio into timestamped text and optionally extract speakers and actions.
category: utilities
aliases:
- speech-to-text
- transcription
triggers:
- Transcribe this audio
- Convert speech to text
- Get a transcript
- Speech recognition
keywords:
- audio
- transcription
- speech
- voice
- text
- whisper
dependencies:
- optional:transcription-engine
risk: low
version: 1.0.0
source: custom
enabled: true
capabilities:
- audio-transcribe
- utilities
inputs:
- task
- context
outputs:
- result
- report
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- audio
- speech
- transcribe
- transcription
- utilities
- voice
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Audio Transcribe

## Purpose
Transcribe audio files into timestamped text with speaker identification and action
extraction. The skill processes various audio formats and produces clean, usable
transcripts for documentation or analysis.

## When to Use
- Converting meeting recordings to text
- Transcribing voice memos or notes
- Creating captions for audio/video content
- Processing interview recordings

## When NOT to Use
- For real-time transcription (use specialized real-time tools)
- When audio quality is too poor for accurate transcription
- For languages without available transcription models

## Capabilities
- Multi-format audio support (MP3, WAV, M4A, FLAC, etc.)
- Timestamped output
- Speaker diarization (identify different speakers)
- Punctuation and formatting
- Confidence scores
- Multiple language support
- Action item extraction

## Inputs
- `audio` (required) — audio file URL or path
- `language` (optional) — source language (auto-detect if omitted)
- `speakers` (optional) — number of speakers (for diarization)
- `timestamps` (optional, default: true) — include timestamps
- `format` (optional) — one of: text, srt, vtt, json

## Workflow
1. **Validate** — Check audio format and accessibility
2. **Process** — Run transcription engine
3. **Format** — Apply formatting and timestamps
4. **Extract** — Identify speakers and actions (if requested)
5. **Deliver** — Provide transcript in requested format

## Tools
- Transcription engine (Whisper, DeepSpeech, or API)
- Audio preprocessing tools

## Examples
**User:** "Transcribe this meeting recording"
**Response:**
```
Transcribing meeting-audio.mp3...
[â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆ] 100%

00:00 - Speaker 1: "Let's start with the agenda..."
00:15 - Speaker 2: "I'll share my screen first."
00:42 - Speaker 1: "Action: Alice to follow up with vendor."

Transcript saved: transcript-meeting-2026-02-09.txt
```

## Safety
- Never store audio or transcripts without consent
- Respect speaker privacy
- Flag low-confidence transcriptions for review
- Handle sensitive content carefully

## Source
Auto-generated from openclawskills.net description.

## Notes
Maintained as part of canonical utilities category.
