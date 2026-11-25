---
name: kb-conventions
description: >-
  Shared conventions for the agent-knowledge repository: directory layout,
  confidence annotation markers, KB divergence markers, and analysis frontmatter
  schema. Read this skill whenever writing or reviewing any KB document.
  Referenced by research-paper and research-extraction.
metadata:
  version: "0.2.0"
---

# KB Conventions

Canonical rules for the `agent-knowledge` repository. Every document written
into the KB must follow these conventions so claims remain traceable and
cross-skill-consistent.

## Directory layout

```
<topic>/
  sources/
    <slug>/
      original.pdf        # Raw input (PDF, HTML snapshot, etc.)
      extracted.md        # Text output from pdf-parse — kept under git
      source.md           # llm-wiki page (paper.json schema) — source metadata + claims
  analysis/
    README.md             # Index of all analyses for this topic
    <slug>.md             # Per-source structured analysis
  drafts/                 # WIP integration notes, large synthesis tasks in progress
  synthesis/              # Authoritative KB documents for this topic
```

One subdirectory per source under `sources/` — keeps original, extracted text, and wiki metadata co-located and traceable.

## source.md template

Create `sources/<slug>/source.md` when acquiring a new source. Populate known fields immediately; update `claims` and `concepts` after analysis.

```yaml
---
title: "<Paper Title>"
type: paper
summary: "<one-line scope>"
tldr: "<one-sentence key takeaway — fill after reading>"
status: draft
last_updated: "<YYYY-MM-DD>"
tags:
  - <lowercase-hyphenated>
read_when:
  - <when is this source the right thing to reach for>
sources: []          # slugs of papers this source cites (surveys, etc.)
concepts: []         # slugs of synthesis/ pages this source informs — fill after analysis
confidence: 0.5      # raise toward 1.0 as claims are verified
claims: []           # fill after analysis — see claim schema below
---
```

Valid `type` values: `paper`, `article`, `documentation`, `clipping`, `transcript`, `note`, `data`, `book-chapter`, `thread`.

### Claim schema

Each entry in `claims` corresponds to a key finding. Confidence maps from annotation markers:

| Annotation | `confidence` |
|---|---|
| `[DIRECT]` | 0.9 – 1.0 |
| `[INFERRED]` | 0.6 – 0.8 |
| `[SPECULATIVE]` | 0.1 – 0.4 |

```yaml
claims:
  - text: "<factual statement>"
    confidence: 0.9
    source: "<slug>"
    section: "§2.3"
```

## Confidence annotation

Every non-trivial claim in a KB document carries one marker:

| Situation | Marker | Required extra |
|---|---|---|
| Verbatim or near-verbatim from source | `[DIRECT]` | Exact passage in a fenced blockquote: `> "exact text"` or ` ```quote ` block |
| Derived from 2+ passages | `[INFERRED]` | All section numbers + one-sentence reasoning |
| Plausible, not grounded in specific passage | `[SPECULATIVE]` | `> ⚠ SPECULATIVE:` block below the claim |
| Source is silent on this topic | — | `> ∅ NOT FOUND IN SOURCES:` + which sources checked |

Absence is data — always record when a source does not address a topic.

**∅ in table cells:** if a `∅` shorthand appears inside a table cell, also add a standalone blockquote immediately after the table:
```
> ∅ NOT FOUND IN SOURCES: <which sources checked, what topic>
```
The table cell alone is not sufficient — the standalone blockquote is required.

## KB divergence markers

Use these when a claim intersects with existing KB content:

| Marker | Meaning |
|---|---|
| `> ⚠ DIVERGES FROM KB:` | Contradicts or refines an existing KB claim |
| `> ✦ NEW:` | Information not present anywhere in the KB |
| `> ∅ NOT FOUND IN SOURCES:` | Source is silent on a topic the KB covers |

## Analysis frontmatter schema

Every file in `<topic>/analysis/` must begin with:

```yaml
---
title: "Analysis: <Document Title>"
type: note
summary: "<one-line summary>"
read_when:
  - <condition under which this analysis is the right thing to read>
status: active
last_updated: "<YYYY-MM-DD>"
source: "sources/<slug>/original.pdf"
---
```

**Critical:** `type: note` is required — the wiki indexer silently skips pages without it.

## Analysis index

`<topic>/analysis/README.md` is a flat index of all analyses for a topic.
Each entry: one line — title, source slug, one-sentence summary.
Create it if absent. Update it whenever a new analysis is added.

## Writing quality

Apply `anti-slop` skill before writing any `synthesis/`, `analysis/`, or
`drafts/` document. Structural rules, slop-pattern detection, and self-audit
checklist are defined there.

## Synthesis impact assessment

After writing or updating an analysis, check existing `<topic>/synthesis/` documents:

- Does this source introduce concepts not yet in the synthesis? Flag `✦ NEW`
- Does it contradict or refine existing claims? Flag `⚠ DIVERGES FROM KB`
- Is it silent on key synthesis topics? Flag `∅ NOT FOUND IN SOURCES`

If impact is significant:
- Small addition → update the synthesis document directly
- Large integration → create a draft in `<topic>/drafts/` documenting the work needed
