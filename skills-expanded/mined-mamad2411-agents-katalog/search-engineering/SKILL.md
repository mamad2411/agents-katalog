---
name: search-engineering
description: Design search features. Use when building search into an application.
metadata:
  tags: search, engineering
---

# Search Engineering

## Use this skill when
- Designing search indexes and relevance
- Implementing filtering, faceting, and ranking
- Choosing engines and syncing data

## Do not use this skill when
- Database LIKE queries where search is primary
- Building a search engine from scratch

## Instructions
1. Choose an engine (Elastic/OpenSearch, Typesense, Meilisearch, pg full-text) for the scale.
2. Define the document schema and analysis per field.
3. Tune relevance: scoring, boosts, synonyms, suggestions.
4. Add filters and facets with principled bucket counts.
5. Handle typos, stemming, and stop words intentionally.
6. Sync documents from source with backfill + incremental.
7. Monitor query latency, indexing lag, and relevance metrics.

## Output Format
- Engine | schema/analysis | relevance | facets | sync pipeline

## Common Mistakes
- index everything “so it’s fast” with wrong semantics
- No relevance tuning
- Sync that silently lags
