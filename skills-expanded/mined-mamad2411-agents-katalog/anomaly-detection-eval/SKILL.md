---
name: anomaly-detection-eval
description: Evaluates unsupervised and semi-supervised time series anomaly detection pipelines across multiple real-world and benchmark datasets. It measures how well different models identify known anomalous segments in telemetry, production traffic, and synthetic signals. Use when the user wants to benchmark on NAB, NASA, YAHOO, or asks about evaluating this task. Reports F1 score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2204.09108
  bibtex_key: alnegheimish2022sintel
  confidence: high
---

# anomaly-detection-eval

> Sintel: A Machine Learning Framework to Extract Insights from Signals — Alnegheimish et al. (2022) (arXiv:2204.09108, 2022)

## What this evaluates

Evaluates unsupervised and semi-supervised time series anomaly detection pipelines across multiple real-world and benchmark datasets. It measures how well different models identify known anomalous segments in telemetry, production traffic, and synthetic signals.

## Datasets

- **NAB** — total 45; splits: test (45); repo https://github.com/numenta/NAB
- **NASA** — total 80; splits: test (80); repo https://github.com/khundman/telemanom
- **YAHOO** — total 367; splits: test (367); repo https://webscope.sandbox.yahoo.com/catalog.php?datatype=s&did=70

## Metrics

- `F1 score` **(primary)** — range: [0, 1]
  - Calculated using an overlapping segment approach between predicted and ground-truth anomaly segments. Standard precision, recall, and F1 are reported per pipeline and dataset.

## Input / output format

**Input**: Univariate or multivariate time series signals (e.g., spacecraft telemetry, server traffic metrics).

**Output**: Binary anomaly labels or detected anomaly segments for each time step/segment.

## Scoring recipe

```python
def compute_f1(pred_segments, gold_segments):
    tp = sum(1 for p in pred_segments if any(overlap(p, g) for g in gold_segments))
    fp = len(pred_segments) - tp
    fn = len(gold_segments) - tp
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    return f1, precision, recall
```

## Common pitfalls

- No single pipeline dominates across all datasets; performance is highly dataset-dependent.
- High false positive rates can overwhelm human reviewers, making precision as critical as recall.
- Semi-supervised pipelines initially underperform unsupervised baselines until sufficient user annotations are accumulated.

## Evidence (verbatim from paper)

> Table [3]. Unsupervised anomaly detection results (F1 score, precision, and recall) per pipeline on each dataset.

## Citation

```bibtex
@misc{alnegheimish2022sintel,
  title={Sintel: A Machine Learning Framework to Extract Insights from Signals},
  author={Alnegheimish et al. (2022)},
  year={2022},
  note={arXiv:2204.09108}
}
```

- arXiv: 2204.09108
