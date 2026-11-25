---
name: autoctr-ctr-eval
description: Evaluates automated neural architecture search for click-through rate prediction on heterogeneous tabular data. It measures how well discovered architectures predict user clicks compared to human-crafted models, and tests their transferability across different datasets. Use when the user wants to benchmark on Criteo, Avazu, KDD Cup, or asks about evaluating this task. Reports logloss.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2007.06434
  bibtex_key: song2020towardsautomated
  confidence: high
---

# autoctr-ctr-eval

> Towards Automated Neural Interaction Discovery for Click-Through Rate Prediction — Qingquan Song et al. (arXiv:2007.06434, 2020)

## What this evaluates

Evaluates automated neural architecture search for click-through rate prediction on heterogeneous tabular data. It measures how well discovered architectures predict user clicks compared to human-crafted models, and tests their transferability across different datasets.

## Datasets

- **Criteo** — total ?; splits: train (-1), val (-1), test (-1)
- **Avazu** — total ?; splits: train (-1), val (-1), test (-1)
- **KDD Cup** — total ?; splits: train (-1), val (-1), test (-1)

## Metrics

- `logloss` **(primary)** — range: other
  - Negative log-likelihood of the predicted click probability for the binary outcome. Lower values indicate better calibration and accuracy.
- `AUC` — range: [0, 1]
  - Area under the Receiver Operating Characteristic curve, measuring the model's ability to rank positive (click) instances higher than negative ones.

## Input / output format

**Input**: Heterogeneous tabular features (sparse categorical and dense numerical) representing user-item interactions, processed according to standard CTR preprocessing pipelines.

**Output**: Predicted click probability or ranking score per instance.

## Scoring recipe

```python
import numpy as np
from sklearn.metrics import log_loss, roc_auc_score

def compute_metrics(y_true, y_pred):
    ll = log_loss(y_true, y_pred)
    auc = roc_auc_score(y_true, y_pred)
    return {'logloss': ll, 'AUC': auc}
```

## Common pitfalls

- Low-fidelity search evaluation uses a fixed 2M-row subsample (80/10/10 split) rather than the full dataset, which can mislead architecture selection.
- Warm-start embedding initialization boosts low-fidelity validation scores but causes overfitting, yielding no improvement on the full test set.
- Search efficiency is measured in GPU days, but the actual training time for the searcher is explicitly ignored as negligible.

## Evidence (verbatim from paper)

> We use logloss and AUC score as the core evaluation metrics. Four questions are mainly explored: Q1. How is AutoCTR comparing with other baseline searchers on both the search efficiency and effectiveness? Q2. How is the performance of the best architecture explored by the AutoCTR comparing with the state-of-the-art (SOTA) human-crafted architectures?

## Citation

```bibtex
@misc{song2020towardsautomated,
  title={Towards Automated Neural Interaction Discovery for Click-Through Rate Prediction},
  author={Qingquan Song et al.},
  year={2020},
  note={arXiv:2007.06434}
}
```

- arXiv: 2007.06434
