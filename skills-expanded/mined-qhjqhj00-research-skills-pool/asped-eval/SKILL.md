---
name: asped-eval
description: Binary audio classification to detect the presence of pedestrians in urban environments. It probes a model's ability to distinguish pedestrian activity from background noise under varying spatial radii and pedestrian count thresholds. Use when the user wants to benchmark on ASPED, or asks about evaluating this task. Reports macro-average recall.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2309.06531
  bibtex_key: seshadri2023asped
  confidence: high
---

# asped-eval

> ASPED: An Audio Dataset for Detecting Pedestrians — Seshadri et al. (2023) (arXiv:2309.06531, 2023)

## What this evaluates

Binary audio classification to detect the presence of pedestrians in urban environments. It probes a model's ability to distinguish pedestrian activity from background noise under varying spatial radii and pedestrian count thresholds.

## Datasets

- **ASPED** — total ?; splits: train (-1), val (-1), test (-1)

## Metrics

- `macro-average recall` **(primary)** — range: [0, 1]
  - Unweighted mean of recall scores computed independently for the positive (pedestrian present) and negative (no pedestrian) classes. Recall is calculated as TP / (TP + FN) per class.

## Input / output format

**Input**: 10-second audio segments processed in 1-second frames. Input features are either 128-dimensional VGGish embeddings, 96x64 log-mel spectrograms, or 100x128 AST spectrograms, forming a sequence of 10 time steps per segment.

**Output**: Binary classification probability (pedestrian present vs. not present) per 1-second frame, derived via a sigmoid activation on a linear classification layer.

## Scoring recipe

```python
def macro_average_recall(y_true, y_pred):
    tp = np.sum((y_true == 1) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    recall_pos = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    tn = np.sum((y_true == 0) & (y_pred == 0))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    recall_neg = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    return (recall_pos + recall_neg) / 2.0
```

## Common pitfalls

- The dataset has severe class imbalance (highly skewed towards no-activity), so standard accuracy is misleading; the paper explicitly uses weighted sampling and loss weighting to mitigate this.
- Test sets differ across radius experiments because labels change with radius, even though the underlying audio is identical; direct performance comparison across radii must account for this label shift.
- Binary labels are derived from pedestrian counts (0 vs >0), but thresholds can be adjusted (e.g., >1, >2), changing the positive class definition and affecting generalization.

## Evidence (verbatim from paper)

> We evaluate the baseline performance measured by class-level and macro-average recall with the following experiments: ... The dataset was randomly split into train/test/Validation subsets with 80/10/10 proportion, respectively. ... As our data contains pedestrian counts per frame, we create classification labels where values of 0 are counted as negative-activity, and any value above 0 is counted as positive-activity.

## Citation

```bibtex
@misc{seshadri2023asped,
  title={ASPED: An Audio Dataset for Detecting Pedestrians},
  author={Seshadri et al. (2023)},
  year={2023},
  note={arXiv:2309.06531}
}
```

- arXiv: 2309.06531
