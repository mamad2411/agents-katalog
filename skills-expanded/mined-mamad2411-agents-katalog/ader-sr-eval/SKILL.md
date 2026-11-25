---
name: ader-sr-eval
description: Evaluates continual learning performance for session-based recommendation by measuring how well a model maintains prediction accuracy on historical items while adapting to new sessions over time. It probes stability-plasticity trade-offs by averaging recommendation quality across multiple sequential update cycles. Use when the user wants to benchmark on DIGINETICA, YOOCHOOSE, or asks about evaluating this task. Reports Recall@k.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2007.12000
  bibtex_key: mi2020ader
  confidence: high
---

# ader-sr-eval

> ADER: Adaptively Distilled Exemplar Replay Towards Continual Learning for Session-based Recommendation — Mi et al. (2020) (arXiv:2007.12000, 2020)

## What this evaluates

Evaluates continual learning performance for session-based recommendation by measuring how well a model maintains prediction accuracy on historical items while adapting to new sessions over time. It probes stability-plasticity trade-offs by averaging recommendation quality across multiple sequential update cycles.

## Datasets

- **DIGINETICA** — total 993483; splits: train (-1), val (-1), test (-1)
- **YOOCHOOSE** — total 3370578; splits: train (-1), val (-1), test (-1)

## Metrics

- `Recall@k` **(primary)** — range: percent
  - The ratio of sessions where the ground-truth next item appears in the top-k recommended items. Evaluated at k=10 and k=20.
- `MRR@k` — range: percent
  - The mean reciprocal rank of the ground-truth item within the top-k recommended list. Evaluated at k=10 and k=20.

## Input / output format

**Input**: Sequence of item IDs in a user session up to the current time step, used to predict the next item.

**Output**: Ranked list of top-k candidate item IDs (k=10 or 20).

## Scoring recipe

```python
def compute_metrics(preds, gold, k):
    recalls, mrrs = [], []
    for p, g in zip(preds, gold):
        topk = p[:k]
        recalls.append(1.0 if g in topk else 0.0)
        if g in topk:
            mrrs.append(1.0 / (topk.index(g) + 1))
        else:
            mrrs.append(0.0)
    return recalls, mrrs
# Average over all test sessions and 16 update cycles
```

## Common pitfalls

- Metrics are averaged across all 16 continual learning update cycles rather than reported per cycle.
- Sessions of length 1 and items appearing fewer than 5 times are removed prior to evaluation.
- Early stopping is based on Recall@20 on the validation set, not the test set.

## Evidence (verbatim from paper)

> Two commonly used evaluation metrics are used: (1). Recall@k: The ratio when the desired item is among the top-k recommended items. (2). MRR@k: Recall@k does not consider the order of the items recommended, while MRR@k measures the mean reciprocal ranks of the desired items in top-k recommended items. For easier comparison, we reported the mean value of these two metrics averaged over all 16 update cycles.

## Citation

```bibtex
@misc{mi2020ader,
  title={ADER: Adaptively Distilled Exemplar Replay Towards Continual Learning for Session-based Recommendation},
  author={Mi et al. (2020)},
  year={2020},
  note={arXiv:2007.12000}
}
```

- arXiv: 2007.12000
