---
name: compile
description: "Incrementally compile the vault's raw/ directory into a structured wiki of concept pages, summaries, and backlinks. Use when the user says 'compile my knowledge base', 'update my wiki', 'fold in new research', or finishes a batch of ingests. Part of the knowledge-base pack implementing Karpathy's raw→wiki workflow."
license: MIT
metadata:
  author: markfive-proto
  version: "0.1.0"
  pack: knowledge-base
---

# Compile Pack — "Turn my raw dumps into a real wiki"

`compile` is the **LLM-driven build step**. It reads new/changed `raw/` items, updates `compiled/` with concept pages, summaries, backlinks, and a top-level index. You rarely write `compiled/` by hand — that is this skill's job.

## Philosophy

- **Additive and incremental.** One raw note can touch many concept pages. Don't rewrite everything every run — touch only what's new.
- **Extract concepts, not sentences.** Each raw source contributes to 2-6 concept pages.
- **Backlinks are automatic.** Every concept page lists every raw source it draws from, using wikilinks.
- **Human-editable outputs.** The wiki is still just markdown. The user can hand-edit and the next compile respects those edits (see "Merge rules").

## Directory output

```
compiled/
  00-INDEX.md           # top-level MOC
  concepts/             # one file per concept
    <concept-slug>.md
  people/               # one file per notable person
  orgs/                 # one file per org/company
  glossary.md           # short-definition hub
  COMPILE-LOG.md        # append-only log of compile runs
```

## Commands

### /compile — Incremental compile

When the user invokes `/compile` (optionally `/compile --since 7d` or `/compile --full`):

1. **Find work.** Read `raw/INGEST-LOG.md` and list entries since last compile (or since `--since`). Full mode rereads everything.
2. **Read new raw notes** into memory with `obs note read` or direct file read.
3. **For each raw note:**
   - Extract 3-10 concepts: nouns/named entities/ideas that deserve their own page.
   - For each concept, decide: does `compiled/concepts/<slug>.md` already exist?
     - **Exists:** append a new section under `## Sources` with a 2-5 line synthesis of how THIS raw note contributes, plus a wikilink `[[<raw-file-basename>]]`.
     - **New:** create the concept page. Template below.
   - Extract notable people → `compiled/people/<name>.md` (same pattern).
   - Extract notable orgs → `compiled/orgs/<name>.md` (same pattern).
4. **Update glossary** for any 1-line-definable term introduced.
5. **Rebuild index** `00-INDEX.md` as a grouped Map of Content.
6. **Append to COMPILE-LOG.md:**
   ```
   - 2026-04-17 14:45  run=incremental  raw_added=3  concepts_touched=14  concepts_new=5
   ```
7. Report back: what changed, new concept pages, suggested next actions.

### Concept-page template

```markdown
---
title: <Concept Name>
type: concept
tags: [compiled, <domain-tag>]
first_seen: <ISO date of earliest source>
last_updated: <ISO date of this compile>
sources_count: <N>
---

# <Concept Name>

## TL;DR
<2-3 sentence synthesis across all sources. Overwrite on every compile that touches this page.>

## Key claims
- <Claim 1> — from [[<raw-source>]]
- <Claim 2> — from [[<raw-source-2>]]
- ...

## Related concepts
- [[<other-concept>]] — how they relate
- ...

## Sources
### [[<raw-source-filename>]]
<2-5 line synthesis of what this source contributes to the concept.>

### [[<raw-source-2>]]
<...>

## Open questions
- <questions that the current sources don't answer — seed for future ingests>
```

### /compile-concept <name> — Rebuild a single concept page

When the user invokes `/compile-concept <name>`:

1. Grep `raw/` for all notes that mention `<name>` (word boundary match).
2. Fully regenerate `compiled/concepts/<slug>.md` from scratch using those sources.
3. Warn the user if the user has hand-edited the file (detect `human-edited: true` in frontmatter) — ask whether to preserve or overwrite.

### /compile-index — Rebuild 00-INDEX.md

When the user invokes `/compile-index`:

1. List every file under `compiled/concepts/`, `compiled/people/`, `compiled/orgs/`.
2. Group by tag / domain (read frontmatter).
3. Sort each group by `last_updated` desc.
4. Write an MOC with sections:
   - "Recently updated" (top 10 last 14 days)
   - Per-domain groupings
   - Orphans (concepts with `sources_count == 1`)
5. Save as `compiled/00-INDEX.md`.

### /compile-diff — Preview what compile would do

When the user invokes `/compile-diff`:

1. Run the compile logic in dry-run mode.
2. Report: new concepts that would be created, existing concepts that would be updated, sources that would be attached, glossary deltas.
3. Do NOT write anything.
4. Let user approve, then run `/compile`.

## Merge rules (how to not destroy human edits)

- Any `compiled/` file with frontmatter `human-edited: true` is treated as a **lock**. Compile skips it, but reports "skipped due to lock" and shows what would have changed.
- Without the lock, compile freely updates TL;DR and Sources sections but **preserves** any markdown section whose heading starts with `## Notes` or `## My take` — those are reserved for the user.
- "Open questions" is additive: compile appends new questions, never deletes existing ones.

## Concept-extraction heuristics (what to extract)

Extract a concept if it is:
- A multi-word noun phrase used 2+ times in the source.
- A proper noun (person, org, product, method name).
- An acronym expanded once.
- A named framework, theory, or equation.
- A dataset, benchmark, or study.

Do NOT extract:
- Pronouns, common nouns, overly generic terms ("data", "system").
- One-off mentions.
- Concepts already in the glossary with a link.

## Token-budget discipline

For each concept page touch, summarize ONLY the relevant passage from the raw source — not the whole source. Target ≤400 tokens synthesis per source contribution. If a concept is drawing from 20+ sources, split the page into sub-pages by era/school/sub-topic.

## Related skills (same pack)

- `[[ingest]]` — upstream (source → raw)
- `[[qa]]` — downstream (query the compiled wiki)
- `[[lint]]` — health check
- `[[render]]` — output formats

## Attribution

Pack inspired by Andrej Karpathy's personal-KB workflow. The compile loop operationalizes his observation that LLMs are very good at incrementally maintaining a wiki from raw source material.
