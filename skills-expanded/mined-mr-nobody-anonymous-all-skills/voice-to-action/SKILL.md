---
name: voice-to-action
description: Convert rough voice-note text into clarified tasks, owners, dates, and follow-ups.
category: productivity
aliases:
- dictation
- memo
- transcribe
- action
triggers:
- From my voice memo
- Transcribe this audio
- What did I just say
- Convert this to a task
keywords:
- voice
- audio
- transcribe
- dictation
- memo
- action
- task
- whisper
dependencies:
- optional:transcript
risk: low
version: 1.0.0
source: custom
enabled: true
capabilities:
- voice-to-action
- productivity
inputs:
- task
- context
outputs:
- result
- report
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- action
- audio
- dictation
- productivity
- transcribe
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

# Voice To Action

## Purpose
Take a voice memo (or live audio stream) and turn it into a **single concrete
action** plus a verbatim transcript and a confidence score. The skill assumes the
user spoke quickly, was distracted, and meant something specific.

## When to Use
- The user has just finished a voice memo and wants it processed
- The user is dictating a task, a calendar event, or a note
- A live transcription should be paired with intent classification

## When NOT to Use
- The audio contains many speakers (use a meeting-specific skill)
- The user wants high-fidelity word-for-word transcription only (use `audio-transcribe`)
- The user is in a setting where the device microphone is unavailable

## Capabilities
- Transcribe audio via `whisper` (local or API)
- Classify the *intent* of the memo:
  - `task` — needs to land in a todo list
  - `event` — has a time and a date
  - `note` — wants to be saved as-is
  - `message` — needs to be sent to a person
  - `idea` — capture only, no action
- Extract entities (people, dates, places) and link to the action
- Output a one-line action plus a short transcript with timestamps

## Inputs
- An audio file path **or** a live mic stream id
- Optional `intent_hint` (one of `task|event|note|message|idea`)
- Optional `target` (a todo app, calendar, or person)

## Workflow
1. **Acquire** the audio (file or live chunk).
2. **Transcribe** with `whisper` (or a cloud STT API), capturing word-level timestamps.
3. **Classify intent** with a small model prompt + the transcript.
4. **Extract entities** (dates â†’ ISO, people â†’ contacts, places â†’ maps).
5. **Build the action**:
   - For `task`: short verb phrase + due date.
   - For `event`: title + start time + duration.
   - For `note`: a clean markdown body, with `[...]` for uncertain words.
   - For `message`: the message text + recipient (ask if ambiguous).
   - For `idea`: title + one-line summary.
6. **Confirm** with the user before performing the action (`add to todo`, `create event`).
7. **Append** the verbatim transcript to a log if the user opted in.

## Tools
- `whisper` (local `whisper.cpp` / `whisper-cli`, or OpenAI Whisper API)
- `ffmpeg` for audio prep (16 kHz mono PCM)
- Optional: `calendar` / `todo` / `telegram-actions` for execution

## Examples
**User:** "Process this voice memo."
**Response:** Intent: `task`. "Email Sam about the launch date, by Friday."
Confirmed: adding to your todo with due date 2026-02-13.

**User:** "Capture this idea."
**Response:** Intent: `idea`. Saved to `notes/ideas/2026-02-09-001.md`. Transcript
appended.

## Safety
- Never send a `message` action without explicit user confirmation
- Strip the recording from the device once processed, unless the user opts in
- Honor a "private" flag (no log, no cloud STT)
- Surface a confidence score; ask when below 0.7

## Source
Auto-generated from openclawskills.net description.

## Notes
Maintained as part of canonical productivity category.
