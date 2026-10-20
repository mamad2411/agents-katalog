---
description: Print current vault stats — sources, concepts, entities, stubs, recent activity.
when_to_use: Use for a quick read on where the vault stands. Read-only; writes nothing. Reads from wiki/.meta/ sidecar cache — O(1) regardless of vault size. Triggered by phrases like "status", "vault stats", "what's in the wiki", "how many sources".
allowed-tools: Read, Bash, Glob, Grep
---

# Wiki Status

Print a one-screen summary of the current vault. Read-only — never writes.

## Source of truth

Read from `wiki/.meta/sources.json` and `wiki/.meta/backlinks.json`.
These are O(1) to read regardless of vault size. If either is
missing or older than the newest file under `wiki/sources/`,
`wiki/concepts/`, or `wiki/entities/`, run
`python3 scripts/build_meta.py` first.

## What to report

### Counts

| Layer | Count |
|---|---|
| Sources (`wiki/sources/`) | N |
| Concepts (full pages) | N |
| Concepts (stubs) | N |
| Entities (full pages) | N |
| Entities (stubs) | N |
| Syntheses | N |
| Outputs | N |

Derive "full pages" vs "stubs" from each page's `type:` frontmatter
(via a grep over the first ~15 lines of each file — or use
`wiki/.meta/backlinks.json` + per-type counts). Exclude `_index*.md`.

### Health signals

- **Raw sources awaiting ingest** — compare the
  `source_path` set in `wiki/.meta/sources.json` against
  `raw/**/*.{md,pdf,txt,docx,pptx,xlsx,xls,html,htm,epub,rtf}`.
  Any raw file not in the sidecar set is unprocessed.
  Report the count; if >0, list the paths.
- **Stubs approaching promotion** — read `wiki/.meta/backlinks.json`
  for nodes whose `type` is `concepts` or `entities` AND whose
  `source_count >= 2` OR `inbound_refs_primary >= 5`, AND whose frontmatter
  `type:` is `stub`. These are what `/wiki-promote` would promote. (The
  unscoped `inbound_refs` count is intentionally **not** used here —
  outputs and syntheses are Claude-authored and would inflate the signal.)
- **Recent activity** — last 5 entries from `wiki/log.md`.
- **Sidecar freshness** — newest file in `wiki/sources|concepts|entities`
  vs `wiki/.meta/backlinks.json.generated_at`. If sidecar is older,
  say so and suggest `/wiki-compile`.

### Size

- `wiki/index.md` — lines and approximate token count (chars ÷ 4).
  Since index.md is a generated thin top-level, it should stay
  under 1K tokens. Flag if it exceeds.
- Per-type `_index.md` size — flag any that exceeds 10K tokens
  (should have auto-sharded).
- Total `wiki/` content size (`du -sh`).

## Format

Tight single-screen output. Tables for counts. Bullets for
everything else. No prose paragraphs.

## Guardrails

- Do not write to any file.
- Do not invoke other commands. (Running `python3 scripts/build_meta.py`
  is OK — it's read-derived cache refresh, not a user-visible
  operation.)
- If the vault is empty (0 sources), say so with a one-liner
  pointing the user at `/wiki-init` or `/wiki-add`.
