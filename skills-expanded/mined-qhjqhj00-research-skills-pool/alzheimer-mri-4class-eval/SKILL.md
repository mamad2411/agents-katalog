---
name: alzheimer-mri-4class-eval
description: Evaluates multi-class classification performance on Alzheimer's disease MRI scans to assess a model's ability to distinguish between different stages of dementia and healthy controls under resource-constrained hardware conditions. Use when the user wants to benchmark on Alzheimer MRI 4 Classes Dataset, or asks about evaluating this task. Reports Accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2508.11532
  bibtex_key: xia2025efficient
  confidence: high
---

# alzheimer-mri-4class-eval

> An Efficient Medical Image Classification Method Based on a Lightweight Improved ConvNeXt-Tiny Architecture — Xia et al. (2025) (arXiv:2508.11532, 2025)

## What this evaluates

Evaluates multi-class classification performance on Alzheimer's disease MRI scans to assess a model's ability to distinguish between different stages of dementia and healthy controls under resource-constrained hardware conditions.

## Datasets

- **Alzheimer MRI 4 Classes Dataset** — total ?; splits: train (-1), val (-1), test (-1)

## Metrics

- `Accuracy` **(primary)** — range: [0, 1]
  - Proportion of correctly classified instances out of the total number of instances.
- `F1-score` — range: [0, 1]
  - Harmonic mean of precision and recall: 2 * (precision * recall) / (precision + recall). Reported per class and macro-averaged.
- `AUC` — range: [0, 1]
  - Area under the Receiver Operating Characteristic curve, measuring the trade-off between true positive rate and false positive rate across classification thresholds.

## Input / output format

**Input**: MRI image scans of Alzheimer's disease patients.

**Output**: Predicted class label from four categories: Non Demented, Mild Demented, Moderate Demented, Very Mild Demented.

## Scoring recipe

```python
def compute_metrics(y_true, y_pred, y_proba):
    accuracy = np.mean(y_true == y_pred)
    f1 = f1_score(y_true, y_pred, average='macro')
    auc = roc_auc_score(y_true, y_proba, multi_class='ovr')
    return {'accuracy': accuracy, 'f1_score': f1, 'auc': auc}
```

## Common pitfalls

- Different baseline models were trained with different learning rates and epoch counts, making direct performance comparisons potentially confounded by training schedule differences.
- Class imbalance is noted, particularly for the Moderate Demented class, which may skew accuracy and affect generalization metrics.
- Evaluation was conducted on CPU-only hardware, which impacts inference speed but the reported metrics focus solely on accuracy/F1/AUC.

## Evidence (verbatim from paper)

> The improved CN-T model achieved the best overall classification performance, with F1-scores ranging from 0.83 to 1.00.

## Citation

```bibtex
@misc{xia2025efficient,
  title={An Efficient Medical Image Classification Method Based on a Lightweight Improved ConvNeXt-Tiny Architecture},
  author={Xia et al. (2025)},
  year={2025},
  note={arXiv:2508.11532}
}
```

- arXiv: 2508.11532
