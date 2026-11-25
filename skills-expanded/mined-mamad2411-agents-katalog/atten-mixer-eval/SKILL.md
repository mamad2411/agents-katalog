---
name: atten-mixer-eval
description: Evaluates a session-based recommendation model's ability to predict the next item in a user's browsing session. It probes the model's capacity to capture multi-level user intent and item semantics through attention mechanisms while handling session-specific inductive biases. Use when the user wants to benchmark on Diginetica, Gowalla, Last.fm, or asks about evaluating this task. Reports HR@K, MRR@K.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2206.12781
  bibtex_key: zhang2022attenmixer
  confidence: high
---

# atten-mixer-eval

> Efficiently Leveraging Multi-level User Intent for Session-based Recommendation via Atten-Mixer Network — Peiyan Zhang et al. (2022) (arXiv:2206.12781, 2022)

## What this evaluates

Evaluates a session-based recommendation model's ability to predict the next item in a user's browsing session. It probes the model's capacity to capture multi-level user intent and item semantics through attention mechanisms while handling session-specific inductive biases.

## Datasets

- **Diginetica** — total ?; splits: train (-1), val (-1), test (-1)
- **Gowalla** — total ?; splits: train (-1), val (-1), test (-1)
- **Last.fm** — total ?; splits: train (-1), val (-1), test (-1)

## Metrics

- `HR@K, MRR@K` **(primary)** — range: [0, 1]
  - Hit Rate@K (HR@K) is 1 if the ground truth item appears in the top-K predicted items, else 0. Mean Reciprocal Rank@K (MRR@K) is 1/rank if the ground truth is in the top-K, else 0. K takes values 5, 10, 20.

## Input / output format

**Input**: A sequence of item IDs representing a user's session history.

**Output**: A ranked list of candidate items (top-K) for the next interaction.

## Scoring recipe

```python
def hr_at_k(preds, gold, k):
    return 1 if gold in preds[:k] else 0

def mrr_at_k(preds, gold, k):
    for i, item in enumerate(preds[:k]):
        if item == gold:
            return 1.0 / (i + 1)
    return 0.0

# Average over test set
hr = sum(hr_at_k(p, g, k) for p, g in zip(preds, golds)) / len(golds)
mrr = sum(mrr_at_k(p, g, k) for p, g in zip(preds, golds)) / len(golds)
```

## Common pitfalls

- Data preprocessing includes filtering short sessions and infrequent items, plus dataset-specific data augmentation before splitting.
- Temporal splitting varies by dataset: last week for Diginetica, last 20% of sessions for Gowalla and Last.fm, with fixed time intervals (1 day or 8 hours) for the latter two.
- Position bias in recommendation means smaller K values (e.g., K=5) are more sensitive to ranking quality and user attention.
- Results are averaged over 5 runs with different random seeds, not single runs.

## Evidence (verbatim from paper)

> We use the same evaluation metrics HR@K (Hit Rate) and MRR@K (Mean Reciprocal Rank) following previous studies (Li et al., 2017; Qiu et al., 2019; Ren et al., 2019; Wu et al., 2019; Chen and Wong, 2020; Xu et al., 2019; Pan et al., 2020; Gupta et al., 2019).

## Citation

```bibtex
@misc{zhang2022attenmixer,
  title={Efficiently Leveraging Multi-level User Intent for Session-based Recommendation via Atten-Mixer Network},
  author={Peiyan Zhang et al. (2022)},
  year={2022},
  note={arXiv:2206.12781}
}
```

- arXiv: 2206.12781
