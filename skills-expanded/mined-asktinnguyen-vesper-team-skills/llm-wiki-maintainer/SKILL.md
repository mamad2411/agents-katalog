---
name: llm-wiki-maintainer
description: This skill should be used when turning a folder of sources, notes, transcripts, or markdown files into a self-maintaining compiled wiki that an LLM can continuously ingest, link, reconcile, and lint over time. It applies to Obsidian-style vaults, local knowledgebases, research archives, second-brain systems, and any workflow where raw material should stay immutable while the model owns the editorial bookkeeping.
license: Complete terms in LICENSE.txt
---

# LLM Wiki Maintainer

Turn a pile of notes into a compounding knowledge artifact.

## Purpose

Use this skill to set up, repair, or operate a markdown knowledge base where:

- raw sources remain immutable
- the model maintains linked wiki pages
- answers are compiled into durable pages instead of disappearing into chat
- the graph is kept healthy through index navigation and lint passes

This skill is for **compiled knowledge systems**, not generic RAG and not a loose folder of saved chats.

## When To Use

Use this skill when the user wants to:

- build a self-maintaining Obsidian-style vault
- create an LLM-maintained wiki from documents, transcripts, screenshots, or research notes
- define rules for how raw notes become durable knowledge pages
- repair a knowledge base that has become messy, orphaned, contradictory, or hard to navigate
- introduce ingest, query, and lint loops for a local markdown knowledge system

Do not use this skill for:

- simple one-off note saving
- pure retrieval pipelines with no editorial write-back
- memory systems whose main unit is atomic facts rather than linked wiki pages

## Core Model

Treat the system as three separated layers with explicit ownership:

1. `raw/` holds immutable source material and belongs to the human
2. `wiki/` holds compiled, linked pages and belongs to the model
3. `CLAUDE.md`, `AGENTS.md`, or equivalent schema docs hold update rules and belong to both

The human owns judgment and source curation.
The model owns summarizing, cross-linking, page updates, index maintenance, and linting.

Load [principles.md](./references/principles.md) before making structural changes.
Load [templates.md](./references/templates.md) when creating or standardizing files.

## Operating Rules

### 1. Preserve Source Immutability

Keep everything landed in `raw/` unchanged after capture.

- store transcripts, PDFs, screenshots, links, exports, and copied articles in `raw/`
- correct bad sources by adding a replacement source, not by silently rewriting the original
- keep interpretation in `wiki/`, never mixed into the source record

If the current system edits source files directly, propose a separation pass first.

### 2. Separate the Layers

Enforce a visible directory split:

```text
vault/
├── raw/
├── wiki/
├── index.md
└── AGENTS.md or CLAUDE.md
```

If the vault has no such split, create it before doing ambitious automation.

### 3. Let the Model Own the Wiki Bookkeeping

Avoid hand-maintaining the wiki unless the user explicitly wants manual control.

The model should:

- create or update topic pages
- summarize new source implications
- file material under the right page
- update neighboring pages when a new fact changes their meaning
- maintain links and index visibility

If the human is repeatedly doing cross-references by hand, the schema is too weak.

### 4. Compile, Do Not Re-Derive

Prefer compiled pages over raw-fragment retrieval.

- answer from the wiki first
- use raw sources to verify or refine when needed
- promote strong recurring answers back into durable pages

The goal is not “retrieve better.”
The goal is “improve the artifact so future retrieval is less necessary.”

### 5. Ingest One Source At A Time

Do not batch-dump a large archive and call it a wiki.

For each new source:

1. place it in `raw/`
2. identify affected pages in `wiki/`
3. update existing pages first when possible
4. create new pages only when the concept/entity deserves one
5. add links in both directions
6. update `index.md` if the source changes the navigable map

If many sources arrive at once, process them sequentially in small waves.

### 6. Link Everything

Every durable page should connect to others through visible wikilinks or standard markdown links.

- prefer linking concepts, entities, decisions, and related source summaries
- treat orphan pages as a health issue
- treat repeated unnamed concepts as candidates for a dedicated page

The value is in the edges, not only the nodes.

### 7. Navigate By Index

Maintain an honest `index.md` that reflects the territory.

Use the index as the first navigation surface for answering questions, reviewing the graph, and spotting gaps.

If the model must brute-force the entire vault for routine questions, the index is stale or dishonest.

### 8. Lint The Knowledge

Treat the wiki like code.

Run periodic health passes to find:

- contradictions between pages
- low-confidence claims with no source anchor
- orphan pages
- duplicate entities or spelling drift
- stale summaries that no longer match the graph
- pages that mention important concepts without linking them

Do not paper over contradictions. Surface them and point to the disagreeing sources.

### 9. Start Small

Prefer a small working system over a grand design.

- begin with a handful of sources
- get ingest, query, and lint working naturally
- add conventions only when they remove repeated pain

Avoid over-designing schema, frontmatter, or taxonomy before the first real ingest loops.

## Recommended Workflow

### A. Initialize Or Audit

1. inspect whether `raw/`, `wiki/`, `index.md`, and schema docs exist
2. create missing pieces using [templates.md](./references/templates.md)
3. identify mixed layers, edited source files, or misleading page structures
4. propose the smallest structural cleanup that restores trust

### B. Ingest

1. add exactly one source to `raw/`
2. trace its implications across existing pages
3. update the fewest pages necessary to absorb the new information cleanly
4. add links and source notes
5. update the index only if the map changed

### C. Query And Promote

1. answer from `index.md` and linked pages first
2. read raw sources only when verification or detail is missing
3. if the answer is strong and likely reusable, promote it into `wiki/`
4. link the promoted page back into the graph

### D. Lint

1. scan the index for clusters, hubs, and orphan pages
2. surface contradictions and spelling drift
3. find pages with implied but missing links
4. rewrite stale summaries when page neighborhoods changed
5. record open questions instead of forcing false certainty

## Output Expectations

When using this skill, produce one or more of:

- a proposed directory structure for the knowledge base
- schema rules for `AGENTS.md` / `CLAUDE.md`
- updated `index.md`
- ingested or reconciled wiki pages
- a lint report with contradictions, orphans, and stale pages
- a promotion plan for turning strong answers into durable pages

## Anti-Patterns

Avoid these failure modes:

- editing `raw/` to make it look cleaner
- stuffing everything into a search index without editorial structure
- creating many pages with no backlinks
- answering every question from scratch instead of improving the wiki
- overloading memory systems with long-form synthesis that belongs in the wiki
- designing a massive schema before the first ten sources work well

## Relationship To Other Systems

- Use this skill when the durable unit is a **linked page**.
- Use a fact-memory skill when the durable unit is an **atomic fact or preference**.
- Use both when the user needs sharp memory plus rich editorial synthesis.

## Success Criteria

The skill is working when:

- source trust is preserved
- the model does most of the bookkeeping
- useful answers increasingly come from compiled pages
- the graph becomes denser and easier to navigate over time
- lint passes find real signal instead of endless mess

The end state is a knowledge base that compounds instead of decays.
