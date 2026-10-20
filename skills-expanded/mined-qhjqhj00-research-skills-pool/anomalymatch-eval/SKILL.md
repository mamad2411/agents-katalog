---
name: anomalymatch-eval
description: This evaluation probes a semi-supervised anomaly detection model's ability to identify rare or visually distinct objects in highly imbalanced image datasets. It measures how effectively the model ranks anomalies at the top of its predictions using limited initial labels and iterative active learning cycles. Use when the user wants to benchmark on miniImageNet, GalaxyMNIST, Galaxy Zoo 2 (Kaggle Challenge subset), or asks about evaluating this task. Reports AUROC.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2505.03509
  bibtex_key: gomez2025anomalymatch
  confidence: high
---

# anomalymatch-eval

> AnomalyMatch: Discovering Rare Objects of Interest with Semi-supervised and Active Learning — Gómez et al. (2025) (arXiv:2505.03509, 2025)

## What this evaluates

This evaluation probes a semi-supervised anomaly detection model's ability to identify rare or visually distinct objects in highly imbalanced image datasets. It measures how effectively the model ranks anomalies at the top of its predictions using limited initial labels and iterative active learning cycles.

## Datasets

- **miniImageNet** — total ?; splits: test (-1)
- **GalaxyMNIST** — total ?; splits: test (-1)
- **Galaxy Zoo 2 (Kaggle Challenge subset)** — total 60000; splits: test (60000); repo https://www.kaggle.com/c/galaxy-zoo-the-galaxy-challenge

## Metrics

- `AUROC` **(primary)** — range: [0, 1]
  - Area under the Receiver Operating Characteristic curve, measuring the trade-off between true positive rate and false positive rate across all classification thresholds.
- `AUPRC` — range: [0, 1]
  - Area under the Precision-Recall curve, summarizing the trade-off between precision and recall across thresholds, particularly sensitive to severe class imbalance.
- `Anomaly Detection Efficiency` — range: percent
  - The percentage of true anomalies recovered within the top X% of images ranked by descending anomaly score.

## Input / output format

**Input**: RGB images resized to 224×224 pixels.

**Output**: A continuous anomaly score for each image, used to rank images from most to least anomalous.

## Scoring recipe

```python
def compute_metrics(scores, labels):
    # scores: anomaly scores (higher = more anomalous)
    # labels: binary ground truth (1 = anomaly, 0 = normal)
    fpr, tpr, _ = roc_curve(labels, scores)
    auroc = auc(fpr, tpr)
    precision, recall, _ = precision_recall_curve(labels, scores)
    auprc = auc(recall, precision)
    top_k_indices = np.argsort(scores)[::-1][:int(len(scores) * 0.01)]
    efficiency_1pct = np.mean(labels[top_k_indices])
    return {'AUROC': auroc, 'AUPRC': auprc, 'Efficiency@1%': efficiency_1pct}
```

## Common pitfalls

- Initial labelled set sizes and anomaly ratios differ across datasets (e.g., 5 anomalies for miniImageNet vs. 10 for GalaxyMNIST vs. variable for Galaxy Zoo 2), so results are not directly comparable without accounting for the active learning starting point.
- The definition of an anomaly in the Galaxy Zoo 2 subset is soft and highly sensitive to the volunteer voter fraction cutoff (e.g., 0.70, 0.80, 0.90, 0.95), causing significant performance volatility.
- Efficiency metrics are reported at specific top-percentile thresholds (0.1% and 1%), not as continuous curves, so exact values depend on the chosen cutoff.

## Evidence (verbatim from paper)

> Throughout the experiments, we employed three key performance metrics: AUROC, AUPRC, and Anomaly Detection Efficiency. AUROC and AUPRC provide complementary views of classification performance, especially important under severe class imbalance. The Anomaly Detection Efficiency quantifies the fraction of anomalies correctly identified within a specified percentage of top-scoring samples, directly reflecting practical usefulness in scenarios involving human-in-the-loop validation and limited labelling resources.

## Citation

```bibtex
@misc{gomez2025anomalymatch,
  title={AnomalyMatch: Discovering Rare Objects of Interest with Semi-supervised and Active Learning},
  author={Gómez et al. (2025)},
  year={2025},
  note={arXiv:2505.03509}
}
```

- arXiv: 2505.03509
