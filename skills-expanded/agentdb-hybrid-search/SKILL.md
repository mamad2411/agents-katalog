---
name: agentdb-hybrid-search
description: Hybrid search — BM25 keyword + dense vector fused with Reciprocal Rank Fusion. Use when queries have specific identifiers, code symbols, or proper nouns that pure semantic search might miss.
---

# Hybrid Search

Combine sparse (BM25, exact terms) and dense (vector, semantic) search via Reciprocal Rank Fusion. Catches both "exact-string" queries and "intent" queries in one call.

## When to use

- Queries with code symbols (`getUserById`, `JWT_SECRET`)
- Queries with proper nouns (file names, package names, project IDs)
- Mixed-intent queries — "the auth module's token refresh logic"
- When you've seen pure vector search miss obvious string matches

## API

```
agentdb_hybrid_search(
  query:    <string>
  k:        5
  weights?: { bm25: 0.5, vector: 0.5 }   // default; bandit can pick
  filters?: { ... }                        // metadata filters
)
```

## How RRF works

Each result gets a rank in BM25 list (r_bm25) and a rank in vector list (r_vec). Final score:

```
score(i) = w_bm25 / (60 + r_bm25(i)) + w_vec / (60 + r_vec(i))
```

The constant 60 (k in the RRF paper) prevents top-1 hits from dominating; the additive structure rewards being well-ranked in *both* lists.

## When NOT to use hybrid

- Pure-natural-language queries with no identifiers → vector alone is fine and faster
- Pure-keyword queries (regex, exact match) → use BM25 directly
- Cross-language queries (query in English, docs in Japanese) → BM25 won't help; stick with vector

## Don't

- Don't tune `weights` manually per query. Let the bandit (`weights: 'auto'`) learn the right balance.
- Don't run hybrid on small corpora (< 1000 docs). BM25's IDF signal is noisy at that scale; vector alone is usually better.
