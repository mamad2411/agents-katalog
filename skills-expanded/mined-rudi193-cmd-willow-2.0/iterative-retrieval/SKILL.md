---
name: iterative-retrieval
description: Progressively refine a search across Willow KB, store, and JELES before reading files
---

@markdownai v1.0

# Iterative Retrieval

Use when looking for context about a topic before reading files or writing code.

## Retrieval Ladder (run in order — stop when you have enough)

**Rung 1 — KB search** (broadest, fastest):
Call `kb_search(query="<topic>", fields=["id","title","summary"])`. Read titles and summaries. If 2+ relevant atoms found, go to Rung 1b.

**Rung 1b — KB get** (precise, low-token):
If you already have an atom id, call `kb_get(id="<ATOM_ID>")` (embeddings are omitted by default).

**Rung 2 — Store search** (collection-scoped):
Call `soil_search(collection="hanuman/atoms", query="<topic>")` or `soil_search` on `hanuman/file-index`. Use when KB search returns nothing.

**Rung 3 — Temporal query** (if currency matters):
Call `kb_at(query="<topic>", at_time="<ISO>")` to get KB state at a specific point in time.

**Rung 4 — JELES retrieval** (session history):
Call `mem_jeles_extract(app_id, query="<topic>")` to pull from indexed session JSONLs.

**Rung 5 — File read** (last resort):
Only read the specific file section if Rungs 1–4 returned nothing useful. Read the specific section, not the whole file.

## Rule

Never skip to Rung 5. The KB is the map. Files are the territory. Read the map first.
