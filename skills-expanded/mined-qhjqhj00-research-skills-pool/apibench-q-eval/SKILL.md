---
name: apibench-q-eval
description: Evaluates the retrieval accuracy and ranking quality of query-based API recommendation systems for Java APIs at both class and method levels. It also measures how query reformulation techniques impact recommendation performance. Use when the user wants to benchmark on APIBench-Q, or asks about evaluating this task. Reports Success Rate@k.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2112.12653
  bibtex_key: peng2021revisiting
  confidence: high
---

# apibench-q-eval

> Revisiting, Benchmarking and Exploring API Recommendation: How Far Are We? — Peng et al. (2021) (arXiv:2112.12653, 2021)

## What this evaluates

Evaluates the retrieval accuracy and ranking quality of query-based API recommendation systems for Java APIs at both class and method levels. It also measures how query reformulation techniques impact recommendation performance.

## Datasets

- **APIBench-Q** — total ?; splits: test (-1); repo https://github.com/JohnnyPeng18/APIBench

## Metrics

- `Success Rate@k` **(primary)** — range: [0, 1]
  - Proportion of queries where at least one correct API appears in the top-k returned results. Calculated as |{q : correct_api(q) in top_k(q)}| / |Q|.
- `MAP@k` — range: [0, 1]
  - Mean Average Precision at k. Averages precision scores at each position where a relevant API is retrieved, up to rank k.
- `MRR` — range: [0, 1]
  - Mean Reciprocal Rank. Average of 1/rank for the first correctly recommended API across all queries.
- `NDCG@k` — range: [0, 1]
  - Normalized Discounted Cumulative Gain at k. Measures ranking quality by discounting gains logarithmically with position, normalized by the ideal DCG.

## Input / output format

**Input**: Natural language query (original or reformulated) requesting a specific Java API.

**Output**: Ranked list of candidate API classes or methods returned by the recommendation system.

## Scoring recipe

```python
def compute_metrics(predictions, gold, k=10):
    pred_k = predictions[:k]
    hit = 1.0 if any(p in gold for p in pred_k) else 0.0
    precisions = [1.0 if p in gold else 0.0 for p in pred_k]
    ap = sum(p * (1.0 / (i + 1)) for i, p in enumerate(precisions)) / min(len(gold), k)
    rr = 0.0
    for i, p in enumerate(predictions):
        if p in gold:
            rr = 1.0 / (i + 1)
            break
    dcg = sum(1.0 / math.log2(i + 2) for i, p in enumerate(pred_k) if p in gold)
    idcg = sum(1.0 / math.log2(i + 2) for i in range(min(len(gold), k)))
    ndcg = dcg / idcg if idcg > 0 else 0.0
    return hit, ap, rr, ndcg
```

## Common pitfalls

- Class-level and method-level recommendations are evaluated separately; method-level accuracy drops significantly (~45% lower) compared to class-level.
- NDCG is defined uniformly for both class and method levels in this benchmark, so scores are identical across levels for the same model.
- Learning-based methods underperform retrieval-based methods here due to insufficient training data (only ~150k Stack Overflow posts available).

## Evidence (verbatim from paper)

> From Table VI, we find that there exist obvious gaps between the scores of Success Rate@k and the metrics for evaluating API ranking, such as MAP@k and NDCG@k. For example, RACK achieves Success Rate@10 score at 0.41, but its MAP@10 score is only 0.24.

## Citation

```bibtex
@misc{peng2021revisiting,
  title={Revisiting, Benchmarking and Exploring API Recommendation: How Far Are We?},
  author={Peng et al. (2021)},
  year={2021},
  note={arXiv:2112.12653}
}
```

- arXiv: 2112.12653
