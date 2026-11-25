---
name: anomalygen-eval
description: This benchmark evaluates log-based anomaly detection models by measuring their ability to classify log sequences as normal or anomalous. It specifically probes how well different model paradigms (classical ML, supervised/unsupervised deep learning, and LLM-based) generalize when trained on code-guided synthetic data augmentation across varying augmentation ratios. Use when the user wants to benchmark on HDFS, Zookeeper, or asks about evaluating this task. Reports F1-score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2604.11107
  bibtex_key: li2026anomalygen
  confidence: high
---

# anomalygen-eval

> AnomalyGen: Enhancing Log-Based Anomaly Detection with Code-Guided Data Augmentation — Xinyu Li et al. (arXiv:2604.11107, 2026)

## What this evaluates

This benchmark evaluates log-based anomaly detection models by measuring their ability to classify log sequences as normal or anomalous. It specifically probes how well different model paradigms (classical ML, supervised/unsupervised deep learning, and LLM-based) generalize when trained on code-guided synthetic data augmentation across varying augmentation ratios.

## Datasets

- **HDFS** — total 11175629; splits: train (46000), test (-1)
- **Zookeeper** — total 74380; splits: train (-1), test (-1)

## Metrics

- `Precision` — range: [0, 1]
  - Precision measures the accuracy of positive predictions, calculated as TP / (TP + FP), where TP is true positives and FP is false positives.
- `Recall` — range: [0, 1]
  - Recall measures the model's ability to identify all actual positive instances, calculated as TP / (TP + FN), where FN is false negatives.
- `F1-score` **(primary)** — range: [0, 1]
  - F1-score is the harmonic mean of Precision and Recall, calculated as 2 * (Precision * Recall) / (Precision + Recall). It balances both metrics to provide a single score for anomaly detection performance.

## Input / output format

**Input**: Log sequences encoded either sequentially by log event IDs or semantically by log message text.

**Output**: Binary anomaly label (normal vs. anomaly) for each input log sequence.

## Scoring recipe

```python
def compute_metrics(y_true, y_pred):
    tp = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 1)
    fp = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 1)
    fn = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 0)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    return {'precision': precision, 'recall': recall, 'f1': f1}
```

## Common pitfalls

- Augmentation ratio R is defined as synthetic sessions divided by real training sessions (R = N_syn/N_real), evaluated at fixed ratios (0.001, 0.01, 0.1, 1.0) while keeping the test set constant across all conditions.
- Sequence-aware encodings (next_log, sequentials) benefit significantly more from structural augmentation than semantic encodings, which aggregate content and discard ordering information.
- Classical ML models (DT, SLFN, KNN) often hit performance ceilings on these datasets, showing changes within measurement noise rather than meaningful gains.

## Evidence (verbatim from paper)

> To evaluate the accuracy and effectiveness of anomaly detection techniques, we employ Precision, Recall and F1-score as evaluation metrics. These metrics are calculated based on the number of True Positives (TP), False Positives (FP), and False Negatives (FN), where positive refers to an anomaly.

## Citation

```bibtex
@misc{li2026anomalygen,
  title={AnomalyGen: Enhancing Log-Based Anomaly Detection with Code-Guided Data Augmentation},
  author={Xinyu Li et al.},
  year={2026},
  note={arXiv:2604.11107}
}
```

- arXiv: 2604.11107
