---
name: exec-deliverable
description: Non-code deliverable standards to embed into Codex prompts when a task produces content rather than code — data analysis, marketing copy, docs, research, plans. Replaces the coding-standards + self-testing blocks for non-engineering output, with the same "prove your own work" verification bar.
---

# Deliverable Standards for Non-Code Output (embed into Codex prompts)

The core flow assumes code, so Phase 4 embeds `exec-coding-standards` + `exec-self-testing` by
default. When a task's output is **content, not code** (a data analysis, a marketing brief, a
launch email, documentation, a research summary, a plan), those blocks don't fit. Embed THIS block
instead — plus any domain skills selected via `skill-selection`.

## Standards block

```
Deliverable standards (mandatory — this task produces content, not code):
- Accuracy first: every factual claim, number, or quote must be verifiable. Do not invent data,
  statistics, sources, quotes, or citations. If a figure is estimated or assumed, label it as such.
- Ground it: derive conclusions from the provided inputs/files/data; when you use an external fact,
  name the source. Distinguish "the data shows X" from "I recommend Y".
- Structure for the audience: lead with the answer/recommendation, then support it; use headings,
  short paragraphs, and lists so the reader can scan. Match the requested format and length exactly.
- Match voice & conventions: follow the project's existing tone, terminology, and templates (read a
  sample first) over a generic voice. Respect brand/style guides when provided.
- Scope discipline: deliver what the task asked for and nothing extra; flag gaps or missing inputs
  rather than filling them with speculation.
- No fabrication of authority: never imply endorsement, real people's words, or official records
  that don't exist.
```

## Data tooling block (embed additionally when the task processes a dataset)

Embed this block whenever the task reads or transforms data files beyond ~50 MB, in ANY lane —
a content task analyzing an export, or a code task that happens to crunch data. Tool choice
follows the data, not the repo's language: a TypeScript project does not mean Node scripts are
the right way to scan an 800 MB CSV.

```
Data tooling rules (mandatory — this task processes a large dataset):
- Measure before choosing: run `du -h` on the inputs (and `wc -l` when cheap) BEFORE picking
  tooling; these rules bind when inputs exceed ~50 MB — never guess sizes.
- Ingest once, query many: convert raw CSV/JSON exports into columnar form first (DuckDB database
  file or Parquet — e.g. `duckdb analysis.duckdb "CREATE TABLE events AS SELECT * FROM
  read_csv('<file>', union_by_name=true)"`), then run every question as a query against that.
  Never re-parse the raw file per question or per report.
- Never write row-by-row scan scripts (Node readline, Python line loops, etc.) over large raw
  files when columnar tooling can express the aggregation — regardless of the project's language.
- Sample-first iteration: develop and debug every query/script against a small sample (e.g. the
  first 10-50k rows) and run the full dataset exactly once, after the logic passes on the sample.
  Report the full-pass wall-clock time and row count in the deliverable.
- One pass, many outputs: when several reports derive from the same raw data, build shared
  intermediate tables (per-user, per-day aggregates) in the ingest step and point every report at
  those — never give each report its own full scan of the raw file.
- Keep heavy I/O local: if the input lives in a cloud-synced folder (OneDrive, Dropbox, Google
  Drive), copy it to a local temp dir before ingesting and write outputs locally; sync overhead
  can multiply runtimes.
- Memory discipline: never accumulate per-row objects for the whole dataset in RAM; aggregate
  incrementally or let the columnar engine do it.
```

## Verification block (the non-code equivalent of self-testing)

```
Verification before finishing (mandatory):
- Re-derive every number from the source data — recompute totals/percentages, don't eyeball them.
  For analysis tasks, show the calculation or the query so it can be checked.
- Fact-check each external claim against its named source; remove or flag anything you can't support.
- Check the piece against the task's acceptance criteria one by one before declaring done.
- Proofread: no broken references, no placeholder text, no contradictions between sections.
- State explicitly what you verified and what remains an assumption the reviewer should confirm.
```

## Claude's review duty for non-code tasks

Phase 5 conformance/quality still applies, re-read for content: does it meet each acceptance
criterion, are the numbers reproducible from the source, are claims sourced (not fabricated), does
it match the requested format and the project's voice? Spot-check at least one figure and one claim
yourself — Codex's "verified" is input, not evidence. `review-security` still triggers if the
deliverable embeds credentials, PII, or internal data that shouldn't leave the workspace.
