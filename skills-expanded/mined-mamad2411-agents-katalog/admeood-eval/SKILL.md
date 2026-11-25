---
name: admeood-eval
description: Evaluates the out-of-distribution generalization of drug property prediction models under two specific domain shifts: noise-level-based confidence categorization (Noise Shift) and inconsistent labels across sources (Concept Conflict Drift). It probes whether models can maintain predictive performance when trained on in-distribution data and tested on molecular domains with shifted label distributions or conflicting assay results. Use when the user wants to benchmark on ADMEOOD, or asks about evaluating this task. Reports AUROC.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2310.07253
  bibtex_key: wei2023admeood
  confidence: high
---

# admeood-eval

> ADMEOOD: Out-of-Distribution Benchmark for Drug Property Prediction — Wei et al. (2023) (arXiv:2310.07253, 2023)

## What this evaluates

Evaluates the out-of-distribution generalization of drug property prediction models under two specific domain shifts: noise-level-based confidence categorization (Noise Shift) and inconsistent labels across sources (Concept Conflict Drift). It probes whether models can maintain predictive performance when trained on in-distribution data and tested on molecular domains with shifted label distributions or conflicting assay results.

## Datasets

- **ADMEOOD** — total ?; splits: IID (-1), OOD (-1)

## Metrics

- `AUROC` **(primary)** — range: percent
  - Area Under the Receiver Operating Characteristic curve. It measures the classifier's ability to distinguish between classes across all classification thresholds. Higher values indicate better performance.

## Input / output format

**Input**: Molecular structures (processed as graphs via a GIN backbone) and target ADME property labels.

**Output**: Predicted probability or continuous score for the target property.

## Scoring recipe

```python
def compute_auroc(y_true, y_pred_scores):
    from sklearn.metrics import roc_curve, auc
    fpr, tpr, _ = roc_curve(y_true, y_pred_scores)
    return auc(fpr, tpr) * 100
```

## Common pitfalls

- Using conventional random train/test splits instead of the specified domain shifts (Assay/Scaffold) and OOD splits, which masks the benchmark's core challenge.
- Reporting single-run results instead of averaging across different environments and random seeds as specified for robustness evaluation.
- Confusing the two distinct OOD shifts (Noise Shift vs. Concept Conflict Drift) and their respective domain-specific failure modes.

## Evidence (verbatim from paper)

> The evaluation metric used in the results is AUROC, which indicates the classifier's ability to distinguish between classes. The higher the AUC score, the better the model's performance in classification.

## Citation

```bibtex
@misc{wei2023admeood,
  title={ADMEOOD: Out-of-Distribution Benchmark for Drug Property Prediction},
  author={Wei et al. (2023)},
  year={2023},
  note={arXiv:2310.07253}
}
```

- arXiv: 2310.07253
