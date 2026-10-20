---
name: adbench-eval
description: Evaluates tabular anomaly detection models on their ability to identify outliers in medium- and high-dimensional datasets by measuring ranking quality and precision-recall trade-offs under a standardized semi-supervised protocol. Use when the user wants to benchmark on ADBench, or asks about evaluating this task. Reports ROC-AUC.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2604.20255
  bibtex_key: lu2026uleadtabpfn
  confidence: high
---

# adbench-eval

> uLEAD-TabPFN: Uncertainty-aware Dependency-based Anomaly Detection with TabPFN — Lu et al. (2026) (arXiv:2604.20255, 2026)

## What this evaluates

Evaluates tabular anomaly detection models on their ability to identify outliers in medium- and high-dimensional datasets by measuring ranking quality and precision-recall trade-offs under a standardized semi-supervised protocol.

## Datasets

- **ADBench** — total 57; splits: train (-1), test (-1)

## Metrics

- `ROC-AUC` **(primary)** — range: [0, 1]
  - Area under the Receiver Operating Characteristic curve, measuring the trade-off between true positive rate and false positive rate across all classification thresholds.
- `PR-AUC` — range: [0, 1]
  - Area under the Precision-Recall curve, measuring the trade-off between precision and recall across thresholds, particularly sensitive to class imbalance in anomaly detection.

## Input / output format

**Input**: Normalized tabular feature vectors (using RCS mean and standard deviation) in a semi-supervised setting.

**Output**: Continuous anomaly scores per instance.

## Scoring recipe

```python
scores = model.predict(X_test)
roc_auc = roc_auc_score(y_test, scores)
pr_auc = average_precision_score(y_test, scores)
# Repeat for 5 different random seeds
final_roc_auc = np.mean(roc_aucs_over_seeds)
final_pr_auc = np.mean(pr_aucs_over_seeds)
```

## Common pitfalls

- The benchmark enforces a semi-supervised protocol where models must be trained only on normal data; using labeled anomalous data during training violates the evaluation standard.
- Features must be normalized using the RCS (Robust Centering and Scaling) mean and standard deviation before evaluation, as specified by the ADBench protocol.
- Results must be averaged over five independent runs with different random seeds to account for variance, rather than reporting a single deterministic run.

## Evidence (verbatim from paper)

> We evaluate uLEAD-TabPFN on ADBench*(Han et al., [2022](#bib.bib19 ""))*, a comprehensive benchmark for tabular anomaly detection, following its standardized semi-supervised evaluation protocol as adopted in prior work*(Han et al., [2022](#bib.bib19 "")); Livernoche et al., [2024](#bib.bib33 "")); Feuer et al., [2024](#bib.bib13 "")); Sattarov et al., [2025](#bib.bib46 ""))*. ADBench consists of 57 tabular anomaly detection datasets spanning a wide range of dimensionalities, sample sizes, and anomaly ratios, all of which are used in our experiments. All features are normalized using the RCS mean and standard deviation. We report ROC-AUC and PR-AUC, averaged over five runs with different random seeds.

## Citation

```bibtex
@misc{lu2026uleadtabpfn,
  title={uLEAD-TabPFN: Uncertainty-aware Dependency-based Anomaly Detection with TabPFN},
  author={Lu et al. (2026)},
  year={2026},
  note={arXiv:2604.20255}
}
```

- arXiv: 2604.20255
