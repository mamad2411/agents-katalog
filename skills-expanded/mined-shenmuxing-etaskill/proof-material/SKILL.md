---
name: proof-material
description: Store and inspect source-indexed proof material extracted from papers, notes, PDFs, or LaTeX sources. Use when Codex needs stable material IDs, source locations, reusable abstractions, proof skeletons, tags, and public attribution before any proof ideas are cooked into proof-usage.
---

# Proof Material

## Overview

Use this skill as the intermediate proof library between `proof-finder` and `proof-cooker`. It preserves one source's proof topology per file so later agents can trace every reusable idea back to a public source, a paper location, and a stable material ID.

`proof-material` is not the final proof playbook. Do not organize it by final technique or strategy category; organize it by original source.

## Pipeline Position

`proof-material` sits after extraction and before synthesis:

```text
proof-finder -> proof-material -> proof-cooker
```

Its job is fidelity. Keep source-local structure, stable IDs, paper locations, dependencies, tags, and reusable abstractions intact so `proof-cooker` can later make taxonomy decisions without losing evidence.

## Library Layout

- Keep the global source index at [references/index.md](references/index.md).
- Create one material file per public source under `references/<source-slug>.md`.
- Use lowercase hyphenated source slugs, usually `<authors-year-short-title>.md`.
- Keep scratch extraction prompts, DeepSeek transcripts, local OCR output, and one-off run logs outside tracked files.

## Source File Contract

Each source material file should use this structure:

```markdown
# <Paper Title>

## Source Metadata

- Source kind: `PDF`
- Public title:
- Authors:
- Year:
- Source file name:
- Public citation:

## Local Index

| ID | Paper location | Type | Short name | Tags | Value |
| --- | --- | --- | --- | --- | --- |

## Items

### <ID>: <Short name>

- Type: `DETAIL`
- Paper location:
- Depends on:
- Local statement:
- Reusable abstraction:
- Proof skeleton:
- Why it is valuable:
- Backtest signal:
- Candidate tags:
- Cooker hints:
```

Use `DETAIL`, `STRATEGY`, `DEFINITION`, `DEPENDENCY`, or `BOTH` as extraction labels only. These are not final proof-usage categories.

## Update Workflow

1. Identify the source and slug.
   - Reuse an existing material file when the public source already appears in the index.
   - Create a new file only when the source is genuinely new.
2. Preserve source topology.
   - Record section, theorem, lemma, equation, page, algorithm line, proof paragraph, or appendix location when available.
   - Keep definitions and dependencies near the items that rely on them.
3. Assign stable IDs.
   - Use a short source prefix plus a two-digit counter, such as `CR24-D01` or `GGSXY25-S02`.
   - Never renumber an existing ID because an item is moved, merged, or cooked later.
4. Rewrite for reuse.
   - Separate `Local statement` from `Reusable abstraction`.
   - Keep `Proof skeleton` concise; do not paste long source passages.
   - Mark uncertainty honestly in `Cooker hints` rather than overstating a theorem.
5. Update [references/index.md](references/index.md).
   - Add or adjust item counts, main domains, and tags.
   - Keep the index lightweight enough for quick routing.

## Public Safety

- Do not include private machine paths, account names, unpublished project details, raw transcripts, or local operational logs.
- Use public citations, public titles, and source filenames only when they do not reveal private workspace details.
- Prefer generic examples such as `sample-project` or `private-workspace` when explaining local scratch areas.
- Attribute ideas to public sources, but keep source excerpts short and paraphrased.

## Handoff To Proof Cooker

When enough material exists for synthesis, pass one or more material files to `proof-cooker`. The cooker may cluster, merge, or split items, but it must preserve backward links to these stable material IDs.
