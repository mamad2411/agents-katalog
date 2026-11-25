---
name: couchbase-fts
description: "Design, build, and tune Couchbase Full Text Search (FTS) and vector search indexes. Use whenever the user asks about FTS indexes, Search service, text search, full-text search, fuzzy search, phrase search, wildcard search, regex search, geo search, geo-distance, geo-bounding-box, facets, scoring, boosting, analyzers, tokenizers, custom analyzers, language analyzers, type mappings, dynamic mappings, child mappings, FTS index design, FTS synonyms (8.x), vector search, kNN search, vector index, embedding search, hybrid search (FTS + vector), cb_fts_search, admin_fts_*, BLEVE, or 'how do I search text in Couchbase.' Distinct from couchbase-sqlpp-tuning (SQL++ index design) and couchbase-mcp (operating the tools). Use proactively when the user has a search use case — text relevance, semantic similarity, geo-proximity, or faceted navigation."
license: MIT
---

# Couchbase Full Text Search & Vector Search

A skill for *designing and operating* Couchbase FTS and vector search indexes. Distinct from:

- `couchbase-sqlpp-tuning` — SQL++ / GSI index design (not Search service)
- `couchbase-data-modeling` — document shape decisions that affect what FTS can index
- `couchbase-mcp` — calling the actual `cb_fts_search`, `admin_fts_*`, and `admin_vector_index_*` tools

If the conversation is "I need to search text / find similar documents / search by location," this is the right skill.

## When this skill applies

- "How do I do full-text search in Couchbase?"
- "How do I build an FTS index?"
- "Why isn't my FTS query matching what I expect?"
- "How do I add fuzzy / wildcard / phrase search?"
- "How do I search by geo-distance?"
- "How do I implement vector / semantic / kNN search?"
- "How do I combine text search with vector search (hybrid)?"
- "What analyzer should I use for [language]?"
- "How do I boost certain fields?"
- "What are FTS synonyms and when should I use them?"
- "How do I size FTS / vector index memory?"

## Pick the right reference

| Question | Read |
|---|---|
| "How do I design an FTS index — mappings, analyzers, type fields?" | `references/index-design.md` |
| "How do I write FTS queries — match, phrase, fuzzy, wildcard, conjunction, geo?" | `references/query-types.md` |
| "Analyzers, tokenizers, token filters — how do they work, which to pick?" | `references/analyzers.md` |
| "Vector search — kNN, hybrid search, index design for embeddings?" | `references/vector-search.md` |
| "FTS synonyms (8.x) — what they are, how to create, when to use?" | `references/synonyms.md` |
| "FTS is slow / results are wrong / index not updating — how to debug?" | `references/troubleshooting.md` |

## Three core principles

**Principle 1 — The index definition determines everything.**
FTS doesn't infer what to index from the document. If a field isn't mapped (or dynamic mapping is off), FTS ignores it. Get the index definition right before debugging queries. The most common FTS failure mode is "the field isn't indexed."

**Principle 2 — Analyzer choice is irreversible at query time.**
The analyzer applied at index time must be consistent with what you apply at query time. If you index with the `en` (English stemming) analyzer and query with `standard`, "running" and "run" won't match. Pick the analyzer once, document it, use it consistently.

**Principle 3 — FTS and GSI solve different problems.**
FTS is for relevance-ranked text search, fuzzy matching, linguistic analysis, geo search, and vector kNN. GSI is for exact-match, range, and structured queries with SQL++ syntax. They're complementary — use both. A common pattern: GSI for filtering (WHERE status = 'active'), FTS for text relevance (SEARCH(description, "fast delivery")).

## The five-question FTS design pass

Before building an index:

1. **What fields need to be searchable?** List them explicitly. Enabling dynamic mapping on large documents indexes everything, including fields you'll never search — wastes RAM and slows indexing.
2. **What languages?** Use language-specific analyzers (en, de, fr, etc.) for stemming and stop-word handling. Multi-language content needs multiple type mappings or a custom analyzer.
3. **Do you need relevance ranking?** If you just need "does this doc contain X" (filter), a simple match query is fine. If you need "most relevant first," you need to think about field weighting and boost values.
4. **Geo, facets, or highlighting?** These require specific field types (`geopoint` for geo, `text` with `include_term_vectors: true` for highlighting). Plan for them in the index definition, not after the fact.
5. **Vector search?** Vector indexes are separate from FTS indexes (8.x uses `admin_vector_index_*` tools; earlier versions use an FTS vector type). Decide whether you need pure vector, pure text, or hybrid before designing the index.

## Quick tool map

| Task | Tool |
|---|---|
| Run a search query | `cb_fts_search` |
| List FTS indexes | `admin_fts_list_indexes` |
| Create/update an FTS index | `admin_fts_upsert_index` |
| Delete an FTS index | `admin_fts_delete_index` |
| Get index stats (doc count, indexing rate) | `admin_fts_get_index_stats` |
| Pause/resume index ingestion | `admin_fts_pause_index_ingestion`, `admin_fts_resume_index_ingestion` |
| FTS synonym sets (8.x) | `cb_fts_synonym_upsert`, `cb_fts_synonym_list`, `cb_fts_synonym_delete` |
| Vector index create/drop/list (8.x) | `admin_vector_index_create`, `admin_vector_index_drop`, `admin_vector_index_list` |
| FTS service memory quota | `admin_stats_fts` (read), cluster settings (write) |

## Version notes

- **7.x:** FTS indexes, standard analyzers, geo search, facets, dynamic/static mappings. Vector search available as experimental in late 7.x releases.
- **8.0+:** `admin_vector_index_*` tools for dedicated vector indexes; FTS synonym sets via `cb_fts_synonym_*`; hybrid search combining FTS and vector scores. Note the algorithm differs by index type: the FTS/Search Vector Index (SVI) uses HNSW, while the dedicated Index-Service vector indexes — Composite (CVI) and Hyperscale (HVI) — use a different family (HVI is built on a Vamana/DiskANN-derived hybrid combined with IVF). See `couchbase-ai-applications` for index-type selection.
- **Capella:** FTS service is available on all tiers. Vector indexes require a minimum compute tier (check current Capella docs for limits).

## Related skills

- `couchbase-data-modeling` — document field types and structure that FTS will index
- `couchbase-sizing` — FTS and vector index memory budgeting
- `couchbase-mcp` — the actual tools for creating and querying FTS indexes
- `couchbase-sqlpp-tuning` — complementary GSI index design for the SQL++ side of hybrid queries
