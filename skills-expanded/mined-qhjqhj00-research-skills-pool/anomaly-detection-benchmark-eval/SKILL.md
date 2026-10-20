---
name: anomaly-detection-benchmark-eval
description: This benchmark evaluates the detection accuracy and computational efficiency of classical machine learning, tree-based, and deep learning anomaly detection algorithms across diverse multivariate and univariate datasets. It probes how well different models handle class imbalance, varying anomaly prevalence, and differing requirements for labeled anomaly data during training. The evaluation also measures training time and resource consumption to assess real-world deployment feasibility. Use when the user wants to benchmark on Anomaly Detection Benchmark Collection (73 multivariate + 31 univariate), or asks about evaluating this task. Reports F1 score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2402.07281
  bibtex_key: mehta2024benchmarking
  confidence: high
---

# anomaly-detection-benchmark-eval

> Benchmarking Anomaly Detection Algorithms: Deep Learning and Beyond — Mehta et al. (2024) (arXiv:2402.07281, 2024)

## What this evaluates

This benchmark evaluates the detection accuracy and computational efficiency of classical machine learning, tree-based, and deep learning anomaly detection algorithms across diverse multivariate and univariate datasets. It probes how well different models handle class imbalance, varying anomaly prevalence, and differing requirements for labeled anomaly data during training. The evaluation also measures training time and resource consumption to assess real-world deployment feasibility.

## Datasets

- **Anomaly Detection Benchmark Collection (73 multivariate + 31 univariate)** — total ?; splits: train (-1), test (-1); repo https://anonymous.4open.science/r/Anomaly-Benchmarking-776D/README.md

## Metrics

- `precision` — range: [0, 1]
  - Ratio of correctly predicted anomalies to all predicted anomalies (TP / (TP + FP)).
- `recall` — range: [0, 1]
  - Ratio of correctly predicted anomalies to all actual anomalies (TP / (TP + FN)).
- `F1 score` **(primary)** — range: [0, 1]
  - Harmonic mean of precision and recall: 2 * (precision * recall) / (precision + recall).
- `AUC-ROC` — range: [0, 1]
  - Area under the Receiver Operating Characteristic curve, measuring the trade-off between true positive rate and false positive rate across all classification thresholds.

## Input / output format

**Input**: Multivariate or univariate numerical feature vectors (time-series or tabular), accompanied by binary ground-truth labels indicating normal or anomalous status.

**Output**: Binary anomaly predictions (0 for normal, 1 for anomaly) derived from algorithm-specific anomaly scores or reconstruction errors using predefined or adaptive thresholds.

## Scoring recipe

```python
def compute_metrics(y_true, y_pred):
    tp = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 1)
    fp = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 1)
    fn = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 0)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    auc_roc = roc_auc_score(y_true, y_pred)
    return precision, recall, f1, auc_roc
```

## Common pitfalls

- Training data composition is inconsistent across algorithms: some require only normal data, while others (e.g., DAGMM, DevNet) explicitly require at least 2 anomalies or a minimum anomaly prevalence (e.g., 2%) in the training set.
- Thresholding strategies are highly algorithm- and dataset-dependent (e.g., fixed percentiles of MSE, standard deviations, or adaptive knee/elbow methods), making direct comparison of raw scores invalid without standardized thresholding.
- Computational limits caused early termination for deep learning models on large datasets (>3 hours training), resulting in missing (NA) results that may bias performance comparisons.

## Evidence (verbatim from paper)

> The performance metrics used for algorithm evaluation are precision, recall, F1 score and AUC-ROC. For transparency, all the codes and datasets are available in a completely anonymized repository. Python version 3.10.12 was used. Compute-intensive algorithms, namely, DevNet, DeepSAD, FTT and PReNet were run on Nvidia Tesla P100 GPU. All the other algorithms were run on CPU.

## Citation

```bibtex
@misc{mehta2024benchmarking,
  title={Benchmarking Anomaly Detection Algorithms: Deep Learning and Beyond},
  author={Mehta et al. (2024)},
  year={2024},
  note={arXiv:2402.07281}
}
```

- arXiv: 2402.07281
