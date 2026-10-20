---
name: Atomizer Core Rules
alwaysApply: true
description: Core project rules for the prompt-driven Atomizer pipeline.
---

# Atomizer Core Rules

You are working in the Atomizer project.

## Non-negotiable architecture rules

- Do not create a second Atomizer pipeline.
- Do not create duplicate output/export/storage systems.
- Do not reintroduce legacy heuristic fallback behavior.
- Do not silently fall back to heuristic extraction.
- Do not create dummy assets when atom coverage is insufficient.
- Do not set `publish_status` to `published`.
- Do not add auto-publishing.
- Do not add TXT export.
- Do not add CSV export.
- Do not add new production gates except `docs/go_no_go.md`.

## Pipeline rules

The Atomizer pipeline is prompt-driven.

Expected high-level flow:

1. Source import
2. Source normalization
3. Chunking for long sources
4. Per-chunk understanding / extraction / typing / validation
5. Merge validated atoms
6. Exactly one global dedupe pass
7. Grounded retention
8. Channel fit
9. Format generation
10. Output quality
11. Storage / export / API access

## Chunking and dedupe

- Chunk IDs must be unique.
- Long sources must be chunked.
- Dedupe must run globally after chunk processing, not repeatedly per chunk.
- Dedupe must not merge different atom types merely because they are thematically related.
- Preserve distinct atom types such as problem, cause, solution, risk, framework, example, recommendation, objection, CTA and checklist item.
- Retention must preserve diverse grounded atoms, not only the highest-ranked linear subset.

## Grounding rules

- Every retained atom must have `source_excerpt`.
- Every retained atom must have `source_reference`.
- `used_atom_ids` must reference existing atoms.
- Do not invent facts, examples, sources, numbers or claims.
- If grounding is insufficient, mark the format as `insufficient_atoms` instead of generating filler.

## Format rules

All supported format paths must stay intact:

- `linkedin_post`
- `linkedin_carousel`
- `linkedin_comment`
- `newsletter`
- `email_sequence`
- `youtube_longform`
- `youtube_short`
- `reel`
- `tiktok_short`
- `community_post`
- `leadmagnet`
- `onepager`
- `facts_check`

## Safety / review

- Output Quality must run per generated asset.
- `facts_check` must never be auto-approved.
- Rejected assets must not be sent as ready handoff.
- Assets requiring human review must remain blocked from creator-ready handoff.
- Handoff may expose blocked status, but must not bypass it.

## Testing expectations

When changing Atomizer logic:

- Run the relevant focused tests first.
- Then run the full suite.
- Keep existing green status intact.
- Use `git diff --check` before committing.
