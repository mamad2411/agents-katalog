---
name: 3d-mir-eval
description: Probes the ability of medical imaging models to retrieve relevant 3D CT volumes based on lesion characteristics. It evaluates retrieval accuracy for binary lesion presence (flag) and morphological size categories (group) across four anatomical regions. Use when the user wants to benchmark on 3D-MIR, or asks about evaluating this task. Reports Average Precision (AP).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2311.13752
  bibtex_key: benabacha20233dmir
  confidence: high
---

# 3d-mir-eval

> 3D-MIR: A Benchmark and Empirical Study on 3D Medical Image Retrieval in Radiology — Ben Abacha et al. (2023) (arXiv:2311.13752, 2023)

## What this evaluates

Probes the ability of medical imaging models to retrieve relevant 3D CT volumes based on lesion characteristics. It evaluates retrieval accuracy for binary lesion presence (flag) and morphological size categories (group) across four anatomical regions.

## Datasets

- **3D-MIR** — total 851; splits: train (729), test (122); repo https://github.com/abachaa/3D-MIR

## Metrics

- `Average Precision (AP)` **(primary)** — range: percent
  - AP = \sum_{n} (R_n - R_{n-1}) P_n, where R_n and P_n are Recall and Precision at the nth threshold.
- `Precision@k (P@k)` — range: percent
  - Fraction of relevant retrieved volumes among the top-k results.

## Input / output format

**Input**: A query 3D CT volume (or 2D slices) with associated lesion flag and lesion group labels.

**Output**: A ranked list of top-k retrieved 3D CT volumes from the index.

## Scoring recipe

```python
def compute_ap(retrieved_labels, gold_label, k):
    ap = 0.0
    prev_recall = 0.0
    for n in range(1, k + 1):
        hits = sum(1 for l in retrieved_labels[:n] if l == gold_label)
        precision_n = hits / n
        recall_n = hits / total_gold_instances
        ap += (recall_n - prev_recall) * precision_n
        prev_recall = recall_n
    return ap
```

## Common pitfalls

- Ground truth labels were generated using a classification model, introducing signal noise that may artificially favor volume-based methods over slice-based ones.
- The ensemble method combining captions and slices underperforms due to low similarity between caption embeddings and image embeddings, contrary to typical multi-modal fusion expectations.
- Cross-dataset augmentation in the training index mixes healthy and lesioned volumes, which affects retrieval baseline heterogeneity and requires careful index construction.

## Evidence (verbatim from paper)

> We evaluate each search method by comparing the lesion flag and lesion group of the query volume and the top-k retrieved volumes. We then compute Precision@k (P@k) and Average Precision (AP), defined as: $$ A P = \sum _ {n} \left(R _ {n} - R _ {n - 1}\right) P _ {n} $$ with $R_{n}$ and $P_{n}$ are the Precision and Recall at the nth threshold.

## Citation

```bibtex
@misc{benabacha20233dmir,
  title={3D-MIR: A Benchmark and Empirical Study on 3D Medical Image Retrieval in Radiology},
  author={Ben Abacha et al. (2023)},
  year={2023},
  note={arXiv:2311.13752}
}
```

- arXiv: 2311.13752
