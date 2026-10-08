# Orientations

`docs/` is the raw source layer (papers, vendor docs, posts). Search this directory **only as a last resort** — the curated `wiki/knowledge/` is the canonical knowledge surface (see root `CLAUDE.md` § Knowledge Lookup and `.claude/rules/wiki-routing.md`).

- **Vendor-documentation mirrors** (`docs/claude/`, `docs/claude-code/`, `docs/cursor/`) are *living mirrors* — re-synced against upstream when drift is material (see [ADR-0010](adr/0010-vendor-doc-mirrors-are-living.md)). Refresh them through the `/grill-with-docs` docs-sync workflow, not by hand-editing content.
- **All other `docs/` artifacts are immutable** — never edit them to "fix" them; they are point-in-time sources, not guidance.
- When a `docs/` source is read often and the wiki lacks a corresponding page, run `/wiki-ingest <path>` to compile a wiki entry instead of repeatedly re-reading the raw file.
