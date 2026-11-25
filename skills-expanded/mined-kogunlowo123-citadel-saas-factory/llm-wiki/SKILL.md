---
name: llm-wiki
description: Persistent compounding knowledge base — ingest sources into wiki, query against compiled knowledge, lint for health. The wiki is the persistent artifact where knowledge accumulates instead of being re-derived from scratch on every question. Use when ingesting documents, answering research questions, or maintaining the knowledge base.
allowed-tools: Read, Write, Grep, Glob, Bash
---

# LLM Wiki Skill

> **Karpathy's pattern.** The LLM maintains a compiled wiki as its persistent brain memory. Raw sources are immutable. The wiki compounds — every session adds to it instead of starting from scratch. The schema is co-evolved between human and LLM.
>
> Original: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

## The three layers

1. **`docs/vault/raw/`** — immutable source documents. Read, never modify.
2. **`docs/vault/wiki/`** — LLM-maintained compiled knowledge (`index.md`, `log.md`, `overview.md`, `entities/`, `concepts/`, `sources/`, `comparisons/`, `contradictions/`).
3. **`docs/vault/SCHEMA.md`** — governance, co-evolved with the human.

## When to invoke

- A new raw source landed in `docs/vault/raw/` → **ingest**.
- A research question needs an answer → **query** (consult the wiki first, not raw files).
- Periodic health check or before a release → **lint**.
- Valuable query answer should be preserved → file it back as a wiki page.

## The three core operations

### 1. Ingest

Fold a raw source into the compiled wiki. A single ingest touches 10–15 pages — that's the point, the wiki curator doesn't get bored.

**Steps:**

1. `Read` the raw file end-to-end.
2. Discuss the key takeaways with the user in 5–10 bullets (what's new, what's confirmed, what contradicts existing claims).
3. `Write` a summary page at `docs/vault/wiki/sources/<slug>.md` following the SCHEMA page format.
4. For each entity the source mentions:
   - `Glob` `docs/vault/wiki/entities/**` to see if a page already exists.
   - `Read` + `Write` to update it (or create it if missing). Add a backlink to the new source page.
5. For each concept the source mentions:
   - Same flow against `docs/vault/wiki/concepts/**`.
6. `Read` + `Write` `docs/vault/wiki/index.md` to register the new source + updated pages in the right categories.
7. `Read` + `Write` `docs/vault/wiki/log.md` to append `## [YYYY-MM-DD] ingest — <source title>` with a list of touched pages.
8. If the source contradicts existing claims, `Write` a page at `docs/vault/wiki/contradictions/<slug>.md` with a `[!contradiction]` callout. Never silently overwrite.
9. Confirm with the user: "Ingested <source>. Touched <N> pages. <M> contradictions flagged."

### 2. Query

Answer a research question against the wiki, and file valuable answers back into the wiki so explorations compound.

**Steps:**

1. `Read` `docs/vault/wiki/index.md` first. **This is non-negotiable** — the compiled knowledge is the first lookup, not raw grep.
2. `Grep` `docs/vault/wiki/` for the question's key terms to find relevant pages.
3. `Read` the matching pages.
4. If the wiki has enough information, synthesize the answer **with citations back to wiki pages**.
5. If the wiki is thin, `Read` relevant raw sources — and then **queue an ingest** for anything material you read.
6. **Offer to file the answer back.** If the question is non-trivial and likely to recur, propose creating:
   - a new `wiki/comparisons/<slug>.md` page (for A vs. B questions),
   - a new `wiki/concepts/<slug>.md` page (for definitional questions),
   - or an update to an existing entity/concept page.
7. Append `## [YYYY-MM-DD] query — <short>` to `log.md` with a pointer to any new page created.

### 3. Lint

Health-check the wiki. Run manually or on a schedule.

**Steps:**

1. `Glob` `docs/vault/wiki/**/*.md` to enumerate pages.
2. For each page, `Read` and check:
   - **Orphans** — any inbound wikilinks? (`Grep` the page's slug across the wiki.)
   - **Stale claims** — `status: stable` but newer sources exist that updated the same entities.
   - **Missing cross-references** — entity names mentioned in body text without a `[[wikilink]]`.
   - **Missing concept pages** — terms used ≥3 times with no `concepts/<term>.md` page.
   - **Data gaps** — `## Open questions` that could be filled by a web search or new raw source.
   - **Low-confidence stables** — `confidence < 0.7` and `status: stable`.
   - **Unresolved contradictions** — `contradictions/` pages with `status: open` > 7 days.
3. Suggest **new questions to investigate** and **new sources to look for**.
4. `Write` the lint report to `log.md` as `## [YYYY-MM-DD] lint — <N> findings` plus details.

## Operating principles

- **Wiki-first.** Before reading raw files or grepping the codebase for a question, read `wiki/index.md`. If the answer is already compiled, use it.
- **Append, don't overwrite.** Contradictions get flagged, not silently resolved.
- **The schema is the governance.** If you notice a pattern the schema doesn't cover, propose a schema edit via `log.md` — don't just invent a new convention.
- **Touch many pages per pass.** A good ingest updates 10–15 pages. If you only touched 2, you probably missed cross-references.
- **Cite wiki pages, not raw files.** Raw files are the primary source, but the wiki is the compiled knowledge. Citations should prefer `[[wiki/entities/foo]]` over `raw/articles/bar.md`.

## Vault Links

- [[../../../docs/vault/SCHEMA|Wiki Schema]]
- [[../../../docs/vault/wiki/index|Wiki Index]]
- [[../../../docs/vault/wiki/log|Activity Log]]
- [[../../agents/wiki-curator|wiki-curator agent]]
- [[../../commands/wiki-ingest|/project:wiki-ingest]]
- [[../../commands/wiki-query|/project:wiki-query]]
- [[../../commands/wiki-lint|/project:wiki-lint]]
- [[../../rules/llm-wiki|llm-wiki rule]]
