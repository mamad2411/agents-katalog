---
name: wiki-qa
description: >
  Answer a teammate's free-form lookup question about this project's planning/wiki
  content (e.g. "what billing model did we settle on yesterday?", "how does X stand?",
  "how are Y and Z related?", "what's the payment scope?") by querying the graphify
  graph to narrow to the relevant concepts and reading only those source files
  (token-efficient and scales as the wiki grows), answering with cited evidence and
  surfacing graph-connected concepts — pure read-only Q&A; explicit work like
  conflict detection, refining, sprint, or backlog belongs to those skills.
version: 0.1.0
author: Loremaster
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [qa, wiki, graphify, query, search, retrieval, scrum, PM]
    related_skills: [refine-wiki, impact-analysis]
---

# Wiki Q&A — graphify graph-based retrieval

Answer the team's wiki/planning questions **without guessing, grounded in the actual
documents**. The key is to **not read everything**: use the graphify graph first to
narrow down "where to read" — token-efficient, and scales as the wiki grows.

## Principles (invariant)
- **No answer without evidence.** Quote only what actually exists in raw/wiki. No
  guessing, no invention — if it isn't there, answer "not there yet / undecided".
- **Cite sources.** State which files the answer came from
  (e.g. `(sources: wiki/concepts/billing-model.md, raw/PRD.md)`).
- This channel = this project's lore vault only. Never pull in concepts from other
  projects.
- `related`/`[[ ]]` are graphify-derived views — never edit them directly (read only).

## Retrieval procedure
Working directory is the project lore vault root (where `graphify-out/`, `wiki/`,
`raw/` are visible).

1. **Narrow the concepts — query graphify first:**
   - Free-form query: `graphify query "<keyword>" --graph graphify-out/graph.json`
     → returns the start node plus a BFS-connected subgraph of **related nodes,
     edges, and source file paths**. Query with the question's **key concept term
     as it is worded in the wiki** (e.g. "billing model", "payment scope").
   - Detail on one concept: `graphify explain "<concept>"` → that node's neighbors
     and relations (depends_on/references etc.).
   - Relation/ripple between two concepts: `graphify path "<A>" "<B>"` → shortest path.
   - **If nothing matches** (label mismatch, synonym, typo): look up the related
     concept name in `wiki/index.md` (the concept catalog, one-line summaries) and
     re-query with that name, or fall back to `search_files` (grep). **Never force
     a guessed answer.**
2. **Read the evidence (only what was narrowed):** `read_file` only the
   `wiki/concepts/<concept>.md` files that query/explain pointed to. If decision
   history or original wording is needed, also the relevant parts of `raw/PRD.md`
   and `raw/decisions/*.md`. **Do not read whole files the graph did not point to.**
3. **Answer:** answer concisely from what you read and attach the **sources**. Add
   one line of **graph-connected concepts** (e.g. `Related: payment scope, free-plan
   policy`) — surfacing connections even when unasked is graphify's value.

## Fallbacks / limits
- **If graph.json is missing** (not yet built): answer via `wiki/index.md` + direct
  `read_file`, and if the wiki looks like it needs refinement, point to refine-wiki.
- `graphify query` matches on **node names**, so it is weak on synonyms and spelling
  → on a miss, fall back to index.md/`search_files`; if still nothing, honestly
  answer "no evidence in the wiki".
- If the question is a **change request rather than a lookup** (planning edit,
  decision, backlog): do not answer it — hand off to the relevant skill
  (resolve-conflicts/backlog-update etc.) and its approval gate. Q&A is
  **read-only**.
