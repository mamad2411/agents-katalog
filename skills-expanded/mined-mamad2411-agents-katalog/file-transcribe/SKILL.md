---
name: file-transcribe
description: Transcribe audio/video files to text using Whisper via OpenKBS AI proxy. Supports MP4, MP3, WAV, OGG, MKV and other ffmpeg-compatible formats. Splits large files into chunks automatically.
allowed-tools: Bash(node *transcribe.mjs*)
---

# File Transcription Skill

Transcribe audio or video files to text using OpenAI Whisper, routed through the OpenKBS AI proxy. No API key needed — uses the project's credits. Language is auto-detected from the audio.

## When to use

Use this skill when the user asks to:
- Transcribe an audio file (MP3, WAV, OGG, FLAC, M4A, etc.)
- Transcribe a video file (MP4, MKV, MOV, AVI, WebM, etc.)
- Convert speech to text from any media file
- Get a text version of a recording, meeting, lecture, podcast, etc.

## Command

```bash
node .claude/skills/file-transcribe/transcribe.mjs <input-file> [output.txt]
```

- `<input-file>` — path to audio or video file (required)
- `[output.txt]` — output text file path (optional, defaults to `transcript.txt`)

## Examples

```bash
# Transcribe an uploaded MP3 (language auto-detected)
node .claude/skills/file-transcribe/transcribe.mjs .uploads/meeting.mp3

# Transcribe a video with custom output path
node .claude/skills/file-transcribe/transcribe.mjs .uploads/lecture.mp4 lecture_transcript.txt

# Force a specific language hint
WHISPER_LANG=en node .claude/skills/file-transcribe/transcribe.mjs .uploads/podcast.mp3
```

## Environment variables (optional)

| Variable | Default | Description |
|----------|---------|-------------|
| `WHISPER_LANG` | *(auto-detect)* | Language hint for Whisper (e.g. `en`, `bg`, `de`) |
| `CHUNK_SECONDS` | `600` | Chunk duration in seconds (for large files) |
| `BATCH` | `4` | Parallel transcription requests |

## How it works

1. Detects if input is video or audio
2. For video: extracts audio track as MP3
3. Checks file size — files under 25MB go directly to Whisper; larger files are split into chunks
4. Uploads to the preview server and calls the OpenKBS Whisper proxy
5. Stitches chunk results in order and writes the final transcript
6. Cleans up all temporary files

## Requirements

- `ffmpeg` must be installed
- One of:
  - **OpenKBS Studio** — works automatically (SERVER_URL + KB_ID are set by the container)
  - **OPENAI_KEY** — set this env var for direct OpenAI Whisper access outside of Studio

## Workflow

1. Verify the input file exists (check `.uploads/` or the path the user specified)
2. Run the transcription command to produce the raw transcript
3. Read the raw transcript and perform a refinement pass:

### Step 3: Refinement

After getting the raw transcript, you MUST read it and produce a polished version by fixing two things:

**A. Error correction** — Whisper mishears words, drops phrases, or garbles domain-specific terms. Analyze the full context of the conversation to infer what was actually said. For example, if the topic is clearly about databases and Whisper wrote "post-Greece queue well", that's "PostgreSQL". Fix these errors in-place while preserving the original meaning.

**B. Speaker identification** — Whisper does not label speakers. You must identify distinct speakers and label them. Use contextual clues: question→answer patterns, "I"/"you" shifts, topic ownership, speaking style differences. Label as `Speaker 1:`, `Speaker 2:`, etc. If names are mentioned in the conversation, use actual names instead.

Write the polished transcript to a separate file (e.g. `transcript_final.txt`) and keep the raw version for reference. Present the final version to the user.

### Step 4: Choose path

Once the refined transcript is ready, present the user with two options using AskUserQuestion:

- **Q&A then Requirement Specification (Recommended)** — Ask clarifying questions first to resolve ambiguities, Whisper errors, and missing details, then generate the specification
- **Direct Requirement Specification** — Generate the specification immediately from the transcript as-is

### Step 5a: Q&A path (if chosen)

Enter plan mode FIRST, then conduct the Q&A inside plan mode. Analyze the transcript for ambiguities, contradictions, missing details, or things that look like transcription errors. Ask questions ONE AT A TIME — ask one question, wait for the user's answer, then use that answer as context for the next question. Do not batch multiple questions. Each subsequent question should be informed by all previous answers. Continue until all ambiguities are resolved. Then produce the Requirement Specification.

### Step 5b: Direct path (if chosen)

Enter plan mode and produce the Requirement Specification directly from the refined transcript.

### Requirement Specification format

The document should cover: objectives, functional requirements, non-functional requirements, constraints, and acceptance criteria. Save as `requirements.md` (or a name the user prefers).
