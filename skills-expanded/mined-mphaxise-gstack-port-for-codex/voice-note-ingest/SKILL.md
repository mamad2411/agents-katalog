---
name: voice-note-ingest
description: Ingest a voice note while preserving exact phrasing and routing ideas, people, and concepts into the brain.
---

# Voice Note Ingest

Use this skill when the user provides a voice note transcript or asks to ingest a voice note.

## Workflow

1. Use the supplied transcript verbatim. If no transcript was supplied, use a
   host-provided transcription tool when available and record that the text is
   machine-transcribed; do not require a particular GBrain command.
2. Preserve the exact supplied or machine-produced transcript as raw source.
3. Extract:
   - original phrasing
   - ideas
   - people or companies
   - tasks
   - concepts
   - emotional or strategic context
4. Use `brain-taxonomist` for new pages.
5. Use `capture` for the core note and specialized ingest skills for derived pages.
6. Return a receipt with created or recommended paths and the transcription source.

## Guardrails

- Do not paraphrase the user's exact words in the preserved source.
- Do not infer sensitive facts beyond the transcript.
- Do not overwrite existing brain pages without asking.
