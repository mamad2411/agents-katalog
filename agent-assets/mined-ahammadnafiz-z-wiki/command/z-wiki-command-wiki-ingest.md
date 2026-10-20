---
description: Process new files in raw/ into wiki pages.
argument-hint: "[path]"
when_to_use: Run after dropping sources into raw/articles/, raw/papers/, or raw/transcripts/. Without arguments, processes every unprocessed source; with a path, ingests only that file. Also triggered by phrases like "ingest the new source", "process raw", "compile what I dropped in".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent
---

# Wiki Ingest

Read `CLAUDE.md` for conventions. Follow the INGEST operation exactly as specified there.

## Scope

- If `$ARGUMENTS` names a path under `raw/`: ingest only that file.
- If `$ARGUMENTS` is empty: determine unprocessed raw files from the
  sidecar cache. Read `wiki/.meta/sources.json` (if it exists) to get
  the set of already-processed `source_path:` values, then compare
  against `raw/**/*.{md,pdf,txt,docx,pptx,xlsx,xls,html,htm,epub,rtf}`.
  Any raw file whose path is not represented is unprocessed.

  If `wiki/.meta/sources.json` is missing or older than the newest
  file in `wiki/sources/`, rebuild it first:
  `python3 scripts/build_meta.py`.

  Do not detect by filename match — raw filenames intentionally differ
  from wiki-summary slugs (see `/wiki-add` naming rule).

## Batch size and subagent dispatch (context engineering)

Before starting, count the unprocessed sources. Apply this policy —
it is how the command stays cheap at scale:

- **1–2 sources:** ingest inline in the main session.
- **3–10 sources:** dispatch one subagent per source via the `Agent`
  tool. Each subagent reads its assigned raw file, writes the source
  summary, creates any new stubs, and returns a structured report
  (see "Subagent report format" below). The parent session merges
  reports and runs the whole-vault post-pass.
- **11+ sources:** dispatch in waves of 10 subagents. Between waves,
  run `python3 scripts/build_meta.py` so the next wave sees the stubs
  the previous wave created (avoids duplicate stub creation).
- **Any source > 50K tokens of extracted markdown:** always goes to its
  own subagent, regardless of batch size. Recursive chunking happens
  in the subagent. See `CLAUDE.md` → INGEST step 2a token gating.

Read `.claude/skills/context-engineering/SKILL.md` for the full
rationale. This is the single biggest cost lever in the whole system.

## Before writing anything

- Confirm each source's counterpart does not already exist. If it does, skip.
- Read each source fully before drafting. PDFs / DOCX / etc.: extract
  with `markitdown`. Scanned PDFs: rasterize and read visually.
- **Gibberish check (mandatory for binary extractions).** After
  `markitdown` writes the tmp markdown, run
  `python3 scripts/check_extraction.py /tmp/<extracted>.md`. If it
  exits non-zero, the extraction is bad (base64 blob, scanned-only
  PDF, encoding failure). Fall back to rasterized/visual read or
  refuse the source with a clear reason. Never summarise gibberish —
  the output looks plausible and corrupts the vault silently.
- Token gating (per CLAUDE.md INGEST step 2a):
  - ≤50k tokens: full read in one pass.
  - 50k–200k tokens: recursive chunking with a 4K-token running
    outline; defer stub creation to end-of-pass ledger (see spec).
  - >200k tokens: stop and propose a chapter-split plan.
- No skimming.

## During ingest (per source)

- Pick the right template per `CLAUDE.md` → INGEST step 2b:
  `paper-summary.md` for anything in `raw/papers/`,
  `source-summary.md` otherwise.
- Every new page must have complete frontmatter per the schema in
  `CLAUDE.md`.
- Every `[[wikilink]]` must resolve by end of this source's ingest —
  create stubs from `templates/stub.md` for any concept/entity that
  would otherwise dangle.
- Do **not** promote stubs inline. INGEST only marks candidates;
  promotion is a separate `/wiki-promote` call. (See CLAUDE.md →
  "Page creation thresholds.")
- Flag contradictions inline with `> [!warning] Contradiction` callouts.
- Append-only to `wiki/log.md`. One entry per source ingested.
- Set `last_seen: <today>` on every page this source substantively
  touched. Do **not** bump `last_seen` on pages only hit by a single
  outbound wikilink — that's write amplification.

## Subagent report format

When a subagent finishes, it must print a report exactly in this shape
so the parent can aggregate without re-reading the raw source:

```
SOURCE: <slug>
SUMMARY_PATH: wiki/sources/<slug>.md
CONCEPTS_CREATED: [slug, slug, ...]
ENTITIES_CREATED: [slug, slug, ...]
STUBS_CREATED: [slug, slug, ...]
PAGES_UPDATED: [slug, slug, ...]
CONTRADICTIONS: [(page, one-line), ...]
PROMOTION_CANDIDATES: [slug, slug, ...]   # stubs whose source_count may have crossed 2
```

The parent session uses this to run the whole-vault post-pass without
re-reading source bodies.

## Whole-vault post-pass (after all sources processed)

1. Run `python3 scripts/build_meta.py --embed-if-enabled` — rebuilds
   `wiki/.meta/backlinks.json`, `wiki/.meta/sources.json`,
   `wiki/.meta/search-index.tsv`, and refreshes embeddings for pages
   whose text changed (no-op if `/wiki-enable-semantic` hasn't run).
2. From the fresh backlinks, identify stubs that crossed either
   promotion threshold (`source_count >= 2` or `inbound_refs_primary >= 5`).
   **Do not promote them.** Print them as "promotion candidates" in
   the final report and tell the user to run `/wiki-promote --list`.
3. Run `python3 scripts/shard_index.py` — rebuilds the top `index.md`
   and per-type / per-tag shards.
4. Reconcile frontmatter `source_count` / `inbound_refs` /
   `inbound_refs_primary` with the sidecar for any concept/entity
   touched by this batch. Rewrite frontmatter in place when it drifted.

## Reporting

At the end, print a summary:

- Sources ingested (list)
- Concept/entity pages created (list)
- Stubs created (list)
- Pages updated in place (list)
- Contradictions flagged (list with file paths)
- **Promotion candidates** (list — user runs `/wiki-promote` to act)
- Files you refused to ingest and why (list)
- Sidecar + index rebuilt (yes/no)

## Failure handling

- Subagent crashes mid-ingest → re-dispatch just that source. Do not
  silently skip.
- `markitdown` returns empty → fall back to rasterized read if PDF;
  else report the source as refused and move on.
- Two sources collide on the same slug → suffix the second with
  `-v2` and flag for review.
