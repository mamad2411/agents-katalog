---
name: adni-fl-eval
description: Evaluates the performance of federated learning algorithms for binary classification of Alzheimer's disease versus normal controls using structural MRI-derived features. It probes how well FL methods handle non-IID data distributions and domain shifts across different scanner parameters (1.5T vs 3.0T) while preserving data privacy. Use when the user wants to benchmark on ADNI, or asks about evaluating this task. Reports ACC.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2306.05980
  bibtex_key: guan2023federated
  confidence: high
---

# adni-fl-eval

> Federated Learning for Medical Image Analysis: A Survey — Hao Guan et al. (arXiv:2306.05980, 2023)

## What this evaluates

Evaluates the performance of federated learning algorithms for binary classification of Alzheimer's disease versus normal controls using structural MRI-derived features. It probes how well FL methods handle non-IID data distributions and domain shifts across different scanner parameters (1.5T vs 3.0T) while preserving data privacy.

## Datasets

- **ADNI** — total 788; splits: train (-1), test (-1)

## Metrics

- `ACC` **(primary)** — range: [0, 1]
  - Classification accuracy: the proportion of correctly classified subjects out of the total number of subjects.
- `SEN` — range: [0, 1]
  - Sensitivity (recall): the proportion of actual AD patients correctly identified as AD.
- `SPE` — range: [0, 1]
  - Specificity: the proportion of actual NC subjects correctly identified as NC.
- `AUC` — range: [0, 1]
  - Area under the Receiver Operating Characteristic curve, measuring the model's ability to discriminate between classes across all classification thresholds.

## Input / output format

**Input**: 1D feature vector of length 90 representing the mean gray matter volumes of brain regions defined in the AAL atlas for each subject's MRI.

**Output**: Binary class label: 'AD' (Alzheimer's Disease) or 'NC' (Normal Control).

## Scoring recipe

```python
def compute_metrics(y_true, y_pred, y_scores):
    tp = sum((y_true == 1) & (y_pred == 1))
    tn = sum((y_true == 0) & (y_pred == 0))
    fp = sum((y_true == 0) & (y_pred == 1))
    fn = sum((y_true == 1) & (y_pred == 0))
    acc = (tp + tn) / (tp + tn + fp + fn)
    sen = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    spe = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    auc = roc_auc_score(y_true, y_scores)
    return {'ACC': acc, 'SEN': sen, 'SPE': spe, 'AUC': auc}
```

## Common pitfalls

- Domain shift between 1.5T (ADNI-1) and 3.0T (ADNI-2) scanners significantly impacts cross-client generalization, often causing the 'Cross' baseline to underperform.
- Random train/test splits are repeated 5 times to mitigate partition bias; reporting single-run results without standard deviations is inconsistent with the protocol.
- All methods use Logistic Regression as the base learner; results are not directly comparable to deep learning FL baselines without retraining.

## Evidence (verbatim from paper)

> We use four metrics to evaluate the classification performance, including classification accuracy (ACC), sensitivity (SEN), specificity (SPE), and area under the ROC curve (AUC).

## Citation

```bibtex
@misc{guan2023federated,
  title={Federated Learning for Medical Image Analysis: A Survey},
  author={Hao Guan et al.},
  year={2023},
  note={arXiv:2306.05980}
}
```

- arXiv: 2306.05980
