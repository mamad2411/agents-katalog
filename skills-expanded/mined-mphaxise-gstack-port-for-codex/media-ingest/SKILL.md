---
name: media-ingest
description: GBrain-inspired media ingest for Codex. Use when local PDFs, transcripts, screenshots, or repo notes should become structured brain pages with preserved raw artifacts.
---

# Media Ingest

Use this skill when the user provides a text-bearing media artifact that Codex can already inspect:

- PDF text already extracted locally
- transcript files
- screenshot OCR output
- repo notes or architecture captures

This port is adapted from `garrytan/gbrain` at commit `0b47afbf402a4e27a648bb9d131ce584461461ea`.

## Important Adaptation

Upstream GBrain handles richer pipelines for audio, video, and OCR services. In this repo, media ingest works when the text is already available or can be read directly by Codex.

Useful helpers:

- `python3 scripts/brain_ingest_source.py <file> ...`
- `python3 scripts/brain_ingest_meeting.py <file> ...` for transcript-style meetings

## Workflow

1. Confirm the media content is readable in the current environment.
2. Preserve the raw artifact with the ingest helper.
3. File the resulting page by primary subject, not by media format.
4. Add explicit people or company backlinks when the mentions matter.
5. If the result is still only a raw capture, follow with `enrich`.

## Current Upstream Coverage

Identify the media format, preserve the raw source, create a structured page with summary and time/page-addressable highlights, propagate mentioned people and organizations, then validate links and citations before sync.

## Guardrails

- Do not pretend binary media was parsed if only the filename is available.
- Do not dump transcripts without at least a summary layer.
- Do not file everything under `sources` when the primary subject is clearer.
