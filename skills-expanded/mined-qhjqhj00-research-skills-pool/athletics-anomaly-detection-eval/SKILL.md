---
name: athletics-anomaly-detection-eval
description: Evaluates performance-based anomaly detection methods to identify athletes with confirmed anti-doping rule violations. It measures how well different algorithms surface sanctioned athletes while balancing precision and recall, accounting for environmental factors like wind and altitude. Use when the user wants to benchmark on 100 m Sprint, or asks about evaluating this task. Reports F1 score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2604.21953
  bibtex_key: madukoma2026performance
  confidence: high
---

# athletics-anomaly-detection-eval

> Performance Anomaly Detection in Athletics: A Benchmarking System with Visual Analytics — Madukoma et al. (2026) (arXiv:2604.21953, 2026)

## What this evaluates

Evaluates performance-based anomaly detection methods to identify athletes with confirmed anti-doping rule violations. It measures how well different algorithms surface sanctioned athletes while balancing precision and recall, accounting for environmental factors like wind and altitude.

## Datasets

- **100 m Sprint** — total 381447; splits: test (381447)

## Metrics

- `F1 score` **(primary)** — range: [0, 1]
  - Harmonic mean of precision and recall. Precision is the fraction of flagged athletes who are sanctioned; recall is the fraction of sanctioned athletes flagged.
- `Precision@200` — range: [0, 1]
  - Fraction of sanctioned athletes among the top 200 flagged athletes in the ranked list.

## Input / output format

**Input**: Longitudinal performance trajectories (race times) for each athlete, optionally augmented with environmental context (wind speed, altitude).

**Output**: Binary anomaly flag per athlete, or a ranked list of athletes prioritized for expert review.

## Scoring recipe

```python
def score(predictions, gold_sanctioned):
    flagged = set(predictions)
    tp = len(flagged & gold_sanctioned)
    fp = len(flagged - gold_sanctioned)
    fn = len(gold_sanctioned - flagged)
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
    return prec, rec, f1
```

## Common pitfalls

- Ground truth is incomplete: undetected dopers artificially lower measured recall, and unsanctioned flagged athletes are counted as false positives despite potentially doping.
- Evaluation operates at the athlete level rather than the performance instance level; a single anomalous performance is sufficient to count as a true positive.
- Extreme class imbalance (0.08% positive rate) yields very low absolute precision/recall values, making relative metrics like P@200 more operationally meaningful.

## Evidence (verbatim from paper)

> Methods are evaluated at the athlete level: a true positive is a sanctioned athlete flagged in at least one performance. This reflects operational screening requirements: a system should detect suspicious athletes even if not all their performances are anomalous. We report precision (fraction of flagged athletes who are sanctioned), recall (fraction of sanctioned athletes flagged), and F1 score.

## Citation

```bibtex
@misc{madukoma2026performance,
  title={Performance Anomaly Detection in Athletics: A Benchmarking System with Visual Analytics},
  author={Madukoma et al. (2026)},
  year={2026},
  note={arXiv:2604.21953}
}
```

- arXiv: 2604.21953
