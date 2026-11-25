---
name: llm-wiki
description: Build and maintain a continuously compiled Markdown-based knowledge base (LLM Wiki). Triggered when the user asks to ingest raw material into a wiki, query existing knowledge, lint the knowledge base for gaps or stale content, or update the schema governing how the wiki is organized.
---

# LLM Wiki

Treat the LLM Wiki as a "continuously compiled knowledge base," not a "temporary RAG retrieval on every question." The human's job is to supply source material, ask questions, and decide focus areas; the agent's job is to maintain the wiki as a persistent artifact.

## Core Model

Always think in three layers:

- `raw/`: Raw material layer. Read-only, source of truth.
- `wiki/`: LLM-maintained layer. Freely create, update, merge, rename, and cross-link pages.
- `AGENTS.md` / `CLAUDE.md`: Schema layer. Defines directory structure, templates, naming conventions, and operating procedures.

Prioritize maintaining "existing synthesized conclusions." Do not reassemble answers from raw material every time.

## Pre-Flight Check

After entering a task, verify these objects exist and prefer local conventions:

- Schema files: `AGENTS.md`, `CLAUDE.md`, or equivalents
- Raw material directory: `raw/`
- Wiki root directory: `wiki/`
- Index file: `wiki/index.md` or equivalent directory index
- Log file: `wiki/log.md` or a top-level `log.md`

If the repository uses different names, adapt to the local structure. Do not force default directory names.

## Operating Modes

Choose one of four modes based on the task:

- `ingest`: Ingest new material, update wiki, index, and log, and sync related pages.
- `query`: Read the index first, then read relevant wiki pages, and answer based on existing synthesized results.
- `lint`: Check for contradictions, stale content, orphaned pages, missing pages, weak links, and knowledge gaps.
- `schema-update`: Update the knowledge-base schema so the workflow is clearer and more executable.

## General Rules

- Read the schema before modifying the wiki.
- Treat `raw/` as a read-only trusted source. Do not clean or rewrite unless the user explicitly asks.
- `wiki/` is persistent working memory. Incremental maintenance is fine; do not obsess over "one source, one page."
- Prefer updating existing pages over generating new isolated summaries.
- Preserve local naming habits, directory organization, page templates, and language style.
- When the repository uses Obsidian, prefer `[[Page Name]]` wikilinks.
- `index.md` is for content navigation. Organize by category and keep one-sentence summaries.
- `log.md` is append-only. Never overwrite history.

## Ingest Workflow

Unless the schema specifies otherwise, execute in this order:

1. Read the new material and locate existing related wiki pages.
2. Extract key claims, concepts, entities, frameworks, conflicts, examples, and reusable insights.
3. Create or update a source summary page in `wiki/`.
4. Write back to affected concept pages, entity pages, topic pages, comparison pages, or resource pages.
5. Fill in cross-links, especially "Related Concepts / Related Entities / Related Topics / Sources."
6. Update `index.md`, registering new pages or updating one-sentence summaries.
7. Append a `log.md` entry. Use a consistent title format, e.g. `## [2026-04-16] ingest | Title`.

If a single source affects many pages, prioritize "few but critical" cross-page updates. Do not mechanically copy the same note everywhere.

## Query Workflow

When answering questions, prefer the wiki. Do not default back to re-reading all raw material:

1. Read `index.md` first to identify the most relevant pages.
2. Open only the necessary pages and synthesize existing conclusions.
3. If the answer depends on specific original claims, trace back to raw pages.
4. Cite sources when answering. Prefer wiki page citations; supplement with raw sources when needed.
5. If the Q&A produces reusable knowledge, persist it as a new page, e.g. under `wiki/topics/`, `wiki/comparisons/`, or `wiki/resources/`, then sync `index.md` and `log.md`.

Rule of thumb: high-value comparisons, frameworks, and analytical conclusions should not live only in chat history.

## Lint Workflow

Focus on these issues:

- Contradictory conclusions across pages.
- Stale summaries invalidated by newer material.
- Orphaned pages with no valid inbound or outbound links.
- High-frequency concepts or entities without dedicated pages.
- Weak or missing "Related Concepts / Related Entities / Related Topics" links.
- Missing source pointers, making conclusions untraceable.
- Topic pages that have grown too large and should be split.
- Obvious knowledge gaps worth filling with additional sources or web search.

When issues are found, fix them directly when appropriate; otherwise, record them as explicit follow-up pages or log entries.

## Page Families

Prefer existing repository templates. If the schema does not specify, organize by these families:

- `wiki/concepts/`: Definitions, detailed explanations, related concepts, sources.
- `wiki/entities/`: Introduction, key characteristics, use cases, related entities, sources.
- `wiki/topics/`: Synthesized conclusions across multiple sources.
- `wiki/comparisons/`: Comparison tables, trade-off analysis, decision frameworks.
- `wiki/resources/`: Tools, articles, datasets, further reading.

Frontmatter should only keep fields that genuinely aid navigation or Dataview, such as `title`, `created`, `source_count`, `tags`, `type`.

## Schema-Update Workflow

When the user asks to "update AGENTS.md" or "improve the LLM Wiki schema":

1. Observe existing directories and real usage first. Do not blindly copy generic templates.
2. Write the schema as executable operating rules for another agent, not conceptual marketing copy.
3. Explicitly define the three-layer structure, directory naming, page templates, ingest/query/lint workflow, and index/log conventions.
4. Prioritize "what must be done" and "in what order." Minimize generic background introductions.

## When to Read Reference Material

Read [references/llm-wiki-pattern.md](references/llm-wiki-pattern.md) in these situations:

- Need to supplement the design rationale behind LLM Wiki.
- Need to explain to the user how this pattern differs from RAG.
- Need to supplement applicable scenarios, extended operations, or practical advice.
