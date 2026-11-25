---
name: meeting-ingestion
description: GBrain-inspired meeting ingestion for Codex. Use when transcript or meeting-note files should become durable meeting pages with attendee and company propagation.
---

# Meeting Ingestion

Use this skill when the user wants a transcript or meeting-note file turned into structured memory under `brain/meetings/`.

This port is adapted from `garrytan/gbrain` at commit `0b47afbf402a4e27a648bb9d131ce584461461ea`.

## Important Adaptation

Upstream GBrain treats attendee enrichment as part of a broader live memory substrate. In this repo, meeting ingestion is explicit and file-backed:

- `python3 scripts/brain_ingest_meeting.py <file> --title ... --date ...`

## Workflow

1. Start from a local transcript or structured notes file.
2. Capture title, date, attendees, discussed companies, and action items.
3. Create the meeting page with summary, actions, and preserved raw transcript.
4. Update attendee and company pages with timeline references and backlinks.
5. Follow with `enrich` if the meeting surfaced deeper entity changes.

## Current Upstream Coverage

Extract decisions, action items, discussion notes, attendees, organizations, and dated timeline events. Attendee enrichment and entity propagation are required when supported by the transcript; do not infer commitments or ownership the meeting did not establish.

## Guardrails

- Do not create attendee pages without meaningful context.
- Do not mark a meeting as ingested if the structured page was never created.
- Do not skip backlinks for attendees or companies you explicitly captured.
