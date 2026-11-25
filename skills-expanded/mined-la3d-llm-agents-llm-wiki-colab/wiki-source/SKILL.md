---
name: wiki-source
description: Ingest a new source document (paper, article, design doc, README, external reference) into the wiki. Creates a source-summary page and links it into the existing wiki neighborhood.
---

A new external source has entered the project. Read it, extract what is durable, and integrate it into the wiki so the source's content becomes part of the project's compounding memory.

## What is "a source"

- A research paper, article, or technical report
- A design document or position paper (often under `docs/`)
- An external README, blog post, or specification
- A reference URL or PDF that the user wants to keep

This is the `llm-wiki.md`-style Ingest. It is **not** for filing our own experiment results. For experiment results, use `/wiki-experiment` instead.

## What to capture

Treat the wiki as durable, queryable memory, not a summary. The ingest succeeds only if a future agent, reading only these pages, can recover this source's specific claims — the exact quantities (with their units), the named systems and methods, and the conditions — and see how they connect to other pages. Preserve those particulars as first-class, retrievable structure (their own pages or clearly-marked sections, cross-linked), not merely as passing mentions folded under general concepts. A page that keeps the general ideas but loses the specifics has failed, however tidy it looks.

- Title, author(s), publication or source
- The one-sentence claim or contribution
- The specific arguments, methods, or findings that bear on this project
- Where the source agrees with, extends, or contradicts existing wiki claims
- Quotes worth keeping verbatim (cite location)

## Procedure

Follow the Ingest procedure in `.llm-wiki/SCHEMA_<repo>.md`. Pointers:

1. Read the source. If long, ask the user which sections matter most for this project.
2. Discuss the key takeaways with the user briefly before writing pages. Confirm the framing and the cross-link targets.
3. Create a source-summary page named after the source (e.g., `Karpathy-Memex-Gist.md`, `Vannevar-Bush-Memex-1945.md`). Frontmatter: `type: source-summary`, `up:` to the closest existing parent page (often the home page or a concept page that the source extends), and `source:` set to a URL or filesystem path. Add `supports:` / `criticizes:` / `extends:` typed edges to other wiki pages where the relationship is clear.
4. Page body: one-sentence opening line stating what the source is and what it contributes. Then sections for: contribution, methods or arguments relevant here, where it intersects with this project, quotes worth keeping, link to the source. Concise reference style.
5. Update related entity and concept pages so the new source reinforces or revises what they say. If the source contradicts a wiki claim, update or flag the affected page, do not leave the contradiction.
6. Fix cross-references in both directions on every affected page (`[[Page]]` in frontmatter, `[Display](Page)` in body).
7. Update `index_<repo>.md` under the "Source summaries" category.
8. Append a `## [YYYY-MM-DD] ingest | Source title` entry to `log_<repo>.md`. The first bullet is the attribution line `- by: <name> via claude-code`, where `<name>` is the output of `git config user.name` in the wiki repo (read it, do not invent it). Then 2 to 5 bullets describing the ingest. See "Log Entry Attribution" in `SCHEMA_<repo>.md`.
9. **Run the Verification Gate** at `${CLAUDE_PLUGIN_ROOT}/core/agents/verification-gate.md` over every page created or edited. Do not commit until all criteria pass. The gate catches projection-as-fact, missing corpus tags, missing back-references, and missing log/index entries.
10. Commit in the wiki's own git repo in two steps: first stage and commit the page and index changes by name with a descriptive message, then stage and commit the `log_<repo>.md` entry on its own. One commit per log entry keeps `git blame` on the log a faithful per-entry record (see "Log Entry Attribution" in SCHEMA). Do not push unless the user requests.

A typical source ingest touches 5 to 15 pages.

## When to skip

- The source is too short or off-topic to justify a page. (A one-line entry in another existing page may be enough.)
- The source duplicates content already covered by an existing wiki page. (Update that page instead of creating a new one.)
- The user has not actually asked for the source to enter the project's memory.

## After running

Tell the user which pages were created or updated, and which existing pages now link to the new source.
