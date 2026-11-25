---
name: abnormal-driving-detection-eval
description: Detects abnormal driving behaviors in naturalistic driving data using event-level safety indicators and motion features. It evaluates a semi-supervised machine learning model's ability to distinguish between normal and anomalous driving events based on vehicle dynamics and temporal proximity metrics. Use when the user wants to benchmark on Naturalistic Driving Dataset, or asks about evaluating this task. Reports F1-score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2312.04610
  bibtex_key: dong2023data
  confidence: high
---

# abnormal-driving-detection-eval

> Data-Driven Semi-Supervised Machine Learning with Safety Indicators for Abnormal Driving Behavior Detection — Dong et al. (2023) (arXiv:2312.04610, 2023)

## What this evaluates

Detects abnormal driving behaviors in naturalistic driving data using event-level safety indicators and motion features. It evaluates a semi-supervised machine learning model's ability to distinguish between normal and anomalous driving events based on vehicle dynamics and temporal proximity metrics.

## Datasets

- **Naturalistic Driving Dataset** — total 23605; splits: test (15118), train (-1), val (-1)

## Metrics

- `F1-score` **(primary)** — range: [0, 1]
  - Harmonic mean of precision and recall: 2 * (precision * recall) / (precision + recall).
- `Accuracy` — range: [0, 1]
  - Proportion of true results among total cases: (TP + TN) / (TP + TN + FP + FN).
- `Precision` — range: [0, 1]
  - Proportion of correctly predicted positives among all predicted positives: TP / (TP + FP).
- `Recall` — range: [0, 1]
  - Proportion of actual positives correctly classified: TP / (TP + FN).
- `TPR` — range: [0, 1]
  - True positive rate, identical to recall: TP / (TP + FN).
- `FPR` — range: [0, 1]
  - False positive rate: FP / (FP + TN).

## Input / output format

**Input**: Per-instance vehicle features: coordinates, velocity, heading angle, longitudinal/lateral acceleration, inter-vehicle distance, and 2D time-to-collision (2D-TTC).

**Output**: Binary classification label: 'abnormal driving' (positive) or 'normal driving' (negative).

## Scoring recipe

```python
TP = sum(y_true == 1 and y_pred == 1)
TN = sum(y_true == 0 and y_pred == 0)
FP = sum(y_true == 0 and y_pred == 1)
FN = sum(y_true == 1 and y_pred == 0)
accuracy = (TP + TN) / (TP + TN + FP + FN)
precision = TP / (TP + FP)
recall = TP / (TP + FN)
f1 = 2 * (precision * recall) / (precision + recall)
tpr = TP / (TP + FN)
fpr = FP / (FP + TN)
```

## Common pitfalls

- The dataset is explicitly balanced by sampling normal instances to match anomalies, which may not reflect real-world driving frequency distributions.
- The evaluation uses a semi-supervised setup with self-supervised pre-training on unlabeled data, so performance heavily depends on the unlabeled data distribution and pre-training strategy.
- Feature ablation compares three specific engineered settings (raw motion, motion+distance, motion+2D-TTC), so results are not directly comparable to models using different feature engineering pipelines.

## Evidence (verbatim from paper)

> Accuracy, precision, and recall were computed based on these four terms. Accuracy refers to the proportion of true results among the total number of cases examined: $$ \text {A c c u r a c y} = \frac {\mathrm {T P} + \mathrm {T N}}{\mathrm {T P} + \mathrm {T N} + \mathrm {F P} + \mathrm {F N}} \tag {13} $$ Precision is utilized to gauge the accurate prediction of positive patterns among the total predicted patterns in a positive class: $$ \mathrm {P r e c i s i o n} = \frac {\mathrm {T P}}{\mathrm {T P} + \mathrm {F P}} \tag {14} $$ Another widely utilized measure is recall, which accounts for the proportion of actual positives that are correctly classified: $$ \text {R e c a l l} = \frac {\mathrm {T P}}{\mathrm {T P} + \mathrm {F N}} \tag {15} $$ The F1-score is a measure combining and balancing precision and recall, and it is defined as the harmonic mean of precision and recall: $$ F 1 - \text {s c o r e} = 2 \times \frac {\text {p r e c i s i o n} \times \text {r e c a l l}}{\text {p r e c i s i o n} + \text {r e c a l l}} \tag {16} $$

## Citation

```bibtex
@misc{dong2023data,
  title={Data-Driven Semi-Supervised Machine Learning with Safety Indicators for Abnormal Driving Behavior Detection},
  author={Dong et al. (2023)},
  year={2023},
  note={arXiv:2312.04610}
}
```

- arXiv: 2312.04610
