---
name: agentdb-mmr
description: Maximal Marginal Relevance rerank — get diverse top-k instead of redundant top-k. Use when standard search returns 5 near-duplicates, or when you want broader coverage of a topic.
---

# MMR Rerank

Diversity reranking on top of vector search. MMR balances relevance to the query with novelty among the picked results.

## When to use

- Top-k search returns 5 essentially-identical hits
- Need broader topic coverage (e.g., for synthesis prompts)
- RAG pipelines where redundancy wastes tokens

## API

```
agentdb_diversity_rank(
  query:        <embedding | string>
  candidates:   <id list>             // typically the top-50 from vector search
  k:            5                      // final size
  lambda:       0.5                    // 0=pure diversity, 1=pure relevance
)
```

## How it works

MMR picks greedily:

```
score(i) = λ · sim(query, i) - (1-λ) · max sim(i, picked_j)
```

High λ → behaves like vanilla top-k (relevance-only).
Low λ → emphasizes novelty among picks.

Default λ = 0.5 is a sensible balance for most uses.

## Pattern

1. Run vector search with k=50.
2. Pass results to `agentdb_diversity_rank` with k=5.
3. Use the diversified 5 in your prompt.

This is a 50→5 reduction with much higher topic coverage than top-5 directly.

## Don't

- Don't MMR on already-diverse search outputs. If your candidates span the topic well, MMR adds latency without lifting quality.
- Don't tune λ per-query manually. The bandit can pick it; expose `lambda: 'auto'` and let it learn.
