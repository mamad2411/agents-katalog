---
name: audio-pipeline
description: |
  Audio pipeline: transcription (Whisper), TTS (ElevenLabs), audio extraction (ffmpeg),
  and YouTube transcript via MCP.

  [WHAT] Audio skill for transcribe, TTS, voice-over, podcast workflow.
  Whisper for transcription (default OpenAI Whisper, configurable per-language),
  ElevenLabs for TTS, ffmpeg for extraction, YouTube-transcript MCP for video.

  [WHEN] Use when: transcribe, audio, TTS, voice-over, podcast, YouTube transcript,
  generate speech, read aloud, dictation audio, mp3, wav, m4a.

  [LANGUAGE] Configurable. TTS voice configurable per project.
allowed-tools: Bash, Read, Write, mcp__youtube-transcript__get_transcript, mcp__elevenlabs__Text_To_Speech
---

# Audio Pipeline

**Role:** unified audio workflow for transcribe, TTS, extract.

## Components

### 1. Transcription

**Default: OpenAI Whisper** (works for most languages).

Optional: language-specific models if better quality is needed (configure per project).

```bash
# Default OpenAI Whisper
~/.claude/scripts/transcribe input.mp3 --output transcript.md

# With language hint
~/.claude/scripts/transcribe input.mp3 --language en --output transcript.md

# Long file → chunked
~/.claude/scripts/transcribe long.m4a --chunk 600 --output transcript.md
```

Output: markdown with timestamps every ~60 seconds, speaker turns if detectable.

### 2. TTS (text-to-speech)

**Default: ElevenLabs** (configure voice ID in `~/.claude/.env`).

```bash
# ElevenLabs default voice
~/.claude/scripts/tts "Text to speak" --output speech.mp3

# Specific voice ID
~/.claude/scripts/tts "Text" --voice $VOICE_ID --output speech.mp3

# From file
~/.claude/scripts/tts --input script.txt --output speech.mp3
```

### 3. Audio extraction

**ffmpeg** for extracting audio from video, converting formats, splitting.

```bash
# Extract audio from video
ffmpeg -i video.mp4 -vn -acodec mp3 audio.mp3

# Convert m4a → mp3
ffmpeg -i input.m4a -acodec mp3 output.mp3

# Split into chunks
ffmpeg -i long.mp3 -f segment -segment_time 600 -c copy chunk_%03d.mp3

# Speed up 1.25x without pitch change
ffmpeg -i input.mp3 -filter:a "atempo=1.25" output.mp3
```

### 4. YouTube transcripts

Via MCP (no browser, no scraping):

```
mcp__youtube-transcript__get_transcript URL
```

Returns transcript with timestamps. Use directly or pipe to extract-wisdom skill.

## Common workflows

### Workflow 1: podcast → notes
1. Get audio: dictation file or extract from video
2. Transcribe
3. Run `extract-wisdom` skill on transcript
4. Save to vault via `archive-to-vault`

### Workflow 2: written text → audio
1. User has script (chronicle, talking points, etc.)
2. Run TTS
3. Output mp3 ready for review/listen

### Workflow 3: meeting recording → meeting notes
1. Extract audio from video meeting
2. Transcribe with speaker diarisation if available
3. Run `meeting-processor` agent on transcript

## Output paths

Configure per project. Common defaults:
- Transcripts: `~/Documents/transcripts/{YYYY-MM-DD}_{title}.md`
- Audio output: `~/Documents/audio/{YYYY-MM-DD}_{title}.mp3`

## Anti-patterns

- Transcribing without language hint when known (worse accuracy)
- TTS-ing very long texts in one call (chunks are more reliable)
- Missing audio metadata (always include duration, source, date)

---

🎯 COMPLETED: [SKILL:audio-pipeline] [audio operation completed]
🗣️ CUSTOM COMPLETED: [SKILL:audio-pipeline] [Audio done]
