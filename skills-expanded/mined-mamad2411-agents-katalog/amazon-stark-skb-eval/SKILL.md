---
name: amazon-stark-skb-eval
description: Evaluates the ability of neural retriever-reranker pipelines to accurately retrieve relevant product entities from semi-structured e-commerce knowledge graphs using natural language queries. It probes semantic matching, cross-encoder reranking effectiveness, and the impact of graph-based augmentation on retrieval precision and recall. Use when the user wants to benchmark on Amazon STaRK SKB, or asks about evaluating this task. Reports Hit@1.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2602.22219
  bibtex_key: rumble2025amazonstark
  confidence: high
---

# amazon-stark-skb-eval

> Comparative Analysis of Neural Retriever-Reranker Pipelines for Retrieval-Augmented Generation over Knowledge Graphs in E-commerce Applications — Rumble et al. (2025) (arXiv:2602.22219, 2025)

## What this evaluates

Evaluates the ability of neural retriever-reranker pipelines to accurately retrieve relevant product entities from semi-structured e-commerce knowledge graphs using natural language queries. It probes semantic matching, cross-encoder reranking effectiveness, and the impact of graph-based augmentation on retrieval precision and recall.

## Datasets

- **Amazon STaRK SKB** — total 9100; splits: validation (910), test (9100)

## Metrics

- `Hit@1` **(primary)** — range: [0, 1]
  - Binary indicator: 1 if the first retrieved item is relevant, 0 otherwise.
- `Hit@5` — range: [0, 1]
  - Binary indicator: 1 if any relevant item appears in the top 5 retrieved results, 0 otherwise.
- `Recall@20` — range: [0, 1]
  - Fraction of all relevant items successfully retrieved within the top 20 results.
- `MRR` — range: [0, 1]
  - Mean Reciprocal Rank: 1 divided by the rank position of the first relevant item retrieved.

## Input / output format

**Input**: Natural language product queries.

**Output**: Ranked list of retrieved knowledge graph nodes/entities.

## Scoring recipe

```python
def score(retrieved, relevant):
    hit1 = 1.0 if retrieved[0] in relevant else 0.0
    hit5 = 1.0 if any(r in relevant for r in retrieved[:5]) else 0.0
    recall20 = len(set(retrieved[:20]) & set(relevant)) / max(len(relevant), 1)
    rr = 0.0
    for i, r in enumerate(retrieved):
        if r in relevant:
            rr = 1.0 / (i + 1)
            break
    return {'Hit@1': hit1, 'Hit@5': hit5, 'Recall@20': recall20, 'MRR': rr}
```

## Common pitfalls

- Confusing the 910-query validation set with the full 9,100-query evaluation set when reporting results.
- Overlooking the massive computational cost difference between cross-encoder rerankers (e.g., 100s/query vs 0.5s/query) when comparing accuracy metrics.
- Assuming dense retrieval (FAISS) inherently outperforms sparse lexical methods (BM25) without accounting for graph augmentation strategies.

## Evidence (verbatim from paper)

> This analysis evaluated the performance of three information retrieval pipelines (BM25, FAISS-FLAT, and FAISS-HNSW) across 910 queries using four key metrics: HIT@1, HIT@5, RE-CALL@20, and MRR.

## Citation

```bibtex
@misc{rumble2025amazonstark,
  title={Comparative Analysis of Neural Retriever-Reranker Pipelines for Retrieval-Augmented Generation over Knowledge Graphs in E-commerce Applications},
  author={Rumble et al. (2025)},
  year={2025},
  note={arXiv:2602.22219}
}
```

- arXiv: 2602.22219
