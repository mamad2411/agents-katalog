---
name: apk2vec-eval
description: Evaluates the quality and transferability of semi-supervised multi-view graph embeddings for Android applications across classification, clustering, and link prediction tasks. Probes whether multi-view and semi-supervised learning improve embedding accuracy and scalability compared to unimodal baselines. Use when the user wants to benchmark on Batch malware detection, Online malware detection, Malware familial clustering, Clone detection, App recommendation, or asks about evaluating this task. Reports F-measure.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1809.05693
  bibtex_key: narayanan2018apk2vec
  confidence: high
---

# apk2vec-eval

> apk2vec: Semi-supervised multi-view representation learning for profiling Android applications — Narayanan et al. (2018) (arXiv:1809.05693, 2018)

## What this evaluates

Evaluates the quality and transferability of semi-supervised multi-view graph embeddings for Android applications across classification, clustering, and link prediction tasks. Probes whether multi-view and semi-supervised learning improve embedding accuracy and scalability compared to unimodal baselines.

## Datasets

- **Batch malware detection** — total 39944; splits: train (-1), test (-1)
- **Online malware detection** — total 10560; splits: train (1000), test (9560)
- **Malware familial clustering** — total 5560; splits: test (5560)
- **Clone detection** — total 280; splits: test (280)
- **App recommendation** — total 2318; splits: test (2318)

## Metrics

- `F-measure` **(primary)** — range: percent
  - Harmonic mean of precision and recall: 2 * (precision * recall) / (precision + recall). Reported as a percentage. Evaluated via 5-fold cross-validation for batch learning and online Passive Aggressive classifier updates for streaming data.
- `Adjusted Rand Index (ARI)` — range: other
  - Similarity measure between two clusterings adjusted for chance: (index - expected_index) / (max_index - expected_index). Computed after k-means clustering of embeddings against ground-truth family or clone labels.
- `AUC` — range: [0, 1]
  - Area under the Receiver Operating Characteristic curve, measuring the probability that a randomly chosen positive edge is ranked higher than a negative edge. Evaluated after randomly removing 10%, 20%, and 30% of edges from the recommendation graph.

## Input / output format

**Input**: Graph representations of Android apps constructed from API sequences (ADG), permissions (PDG), and system calls (SDG). Nodes represent app components/elements, edges represent control/data flow or relationships.

**Output**: 64-dimensional embedding vectors per app. Task-specific outputs: binary class labels (malware/benign), cluster IDs (1–179 or 1–100), or binary link prediction scores.

## Scoring recipe

```python
# Classification (Batch/Online)
tp = sum(pred == 1 and gold == 1)
fp = sum(pred == 1 and gold == 0)
fn = sum(pred == 0 and gold == 1)
precision = tp / (tp + fp) if (tp + fp) > 0 else 0
recall = tp / (tp + fn) if (tp + fn) > 0 else 0
f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

# Clustering
ari = adjusted_rand_score(gold_labels, kmeans_predict(embeddings, k=ground_truth_clusters))

# Link Prediction
auc = roc_auc_score(gold_edges, link_scores)
```

## Common pitfalls

- Baselines like GE-FSG fail on large graphs due to Out of Memory (OOM) errors, leading to missing results that skew comparative analysis.
- Semi-supervised embedding training uses only 25% of available class labels, which significantly boosts apk2vec's performance relative to fully unsupervised baselines if not explicitly noted.
- Online evaluation simulates real-world streaming by temporally sorting apps by release date, violating standard i.i.d. test split assumptions.

## Evidence (verbatim from paper)

> For both batch and online settings, to evaluate the efficacy, standard metrics such as precision, recall and f-measure are used. Adjusted Rand Index (ARI) is used as a metric to determine the clustering accuracy in both these tasks. Area under the ROC curve (AUC) is used as a metric to quantify the efficacy of link prediction.

## Citation

```bibtex
@misc{narayanan2018apk2vec,
  title={apk2vec: Semi-supervised multi-view representation learning for profiling Android applications},
  author={Narayanan et al. (2018)},
  year={2018},
  note={arXiv:1809.05693}
}
```

- arXiv: 1809.05693
