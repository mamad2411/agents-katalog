---
name: capture
description: Save a thought, note, or short artifact into the local brain substrate with citations and a clear receipt.
---

# Capture

Use this skill when the user says to remember, save, capture, or drop something into the brain.

Upstream GBrain uses `gbrain capture` as the front door. This Codex port maps that idea to the repo's file-backed helpers first, then uses the upstream CLI when it exists.

## Workflow

1. Identify the content to capture:
   - inline user text
   - a local file
   - a short summary generated during the current task
2. Pick the right capture path:
   - use `scripts/brain_capture_signal.py` for short user phrasing or ideas
   - use `scripts/brain_ingest_source.py` for files and source material
   - use specialized skills for meetings, media, or article-style ingestion
3. Before creating a new brain page, use `brain-taxonomist` when the target folder or page type is not obvious.
4. Include source context:
   - who said it or where it came from
   - date
   - citation or local file path when available
5. Return a short receipt with the created or updated path.

## Guardrails

- Do not store secrets.
- Do not silently rewrite existing brain pages.
- Do not use shell inline arguments for sensitive content.
- If the user asks for a bulk import, route to `media-ingest`, `idea-ingest`, or `sync-gbrain` instead.
