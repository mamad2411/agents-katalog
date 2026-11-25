---
name: accounting-fraud-detection-eval
description: Evaluates machine learning models' ability to detect accounting fraud using financial statement ratios across different industry sectors. It probes the models' predictive accuracy, sensitivity to fraud cases, and robustness to class imbalance and industry-specific data distributions. Use when the user wants to benchmark on SIC Industry Financial Fraud Dataset, or asks about evaluating this task. Reports Accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1805.02840
  bibtex_key: jofre2018fighting
  confidence: high
---

# accounting-fraud-detection-eval

> Fighting Accounting Fraud Through Forensic Data Analytics — Jofre et al. (2018) (arXiv:1805.02840, 2018)

## What this evaluates

Evaluates machine learning models' ability to detect accounting fraud using financial statement ratios across different industry sectors. It probes the models' predictive accuracy, sensitivity to fraud cases, and robustness to class imbalance and industry-specific data distributions.

## Datasets

- **SIC Industry Financial Fraud Dataset** — total ?; splits: test (-1)

## Metrics

- `Accuracy` **(primary)** — range: [0, 1]
  - Proportion of correctly classified instances (fraud and non-fraud) out of the total number of instances.
- `AUC` — range: [0, 1]
  - Area under the Receiver Operating Characteristic curve, measuring the model's ability to discriminate between fraud and non-fraud classes across all classification thresholds.
- `Sensitivity` — range: [0, 1]
  - True positive rate; proportion of actual fraud cases correctly identified by the model.
- `Specificity` — range: [0, 1]
  - True negative rate; proportion of actual non-fraud cases correctly identified by the model.
- `Precision` — range: [0, 1]
  - Proportion of predicted fraud cases that are actually fraudulent.
- `F-Measure` — range: [0, 1]
  - Harmonic mean of Precision and Sensitivity (F1-score).
- `G-Mean` — range: [0, 1]
  - Geometric mean of Sensitivity and Specificity, used to evaluate balance between class performance.

## Input / output format

**Input**: Financial statement ratios (e.g., RETA, CATA, IVSA, PYCOGS, IVTA, RVSA, TLTE) and firm industry classification (SIC code).

**Output**: Binary classification label indicating whether the firm is fraudulent or non-fraudulent.

## Scoring recipe

```python
def compute_metrics(y_true, y_pred):
    tp = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 1)
    tn = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 0)
    fp = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 1)
    fn = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 0)
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    f_measure = 2 * precision * sensitivity / (precision + sensitivity) if (precision + sensitivity) > 0 else 0
    g_mean = (sensitivity * specificity) ** 0.5
    return accuracy, specificity, sensitivity, precision, g_mean, f_measure
```

## Common pitfalls

- Small sample sizes in certain industries (e.g., Agriculture n=22) lead to unstable performance estimates and limit generalizability.
- High specificity often comes at the cost of low sensitivity, indicating class imbalance or threshold bias that favors predicting non-fraud cases.
- Results are reported per industry rather than globally, making cross-industry comparison difficult and highlighting strong domain-specific bias.

## Evidence (verbatim from paper)

> Table 9 reports the results of the proposed models by SIC industry. ... Accuracy | Specificity | Sensitivity | Precision | G-Mean | F-Measure | AUC

## Citation

```bibtex
@misc{jofre2018fighting,
  title={Fighting Accounting Fraud Through Forensic Data Analytics},
  author={Jofre et al. (2018)},
  year={2018},
  note={arXiv:1805.02840}
}
```

- arXiv: 1805.02840
