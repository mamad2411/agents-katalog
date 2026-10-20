---
name: 3dses-eval
description: Semantic segmentation of indoor Terrestrial Laser Scanning (TLS) point clouds. It probes a model's ability to classify 3D points into semantic categories (e.g., furniture, structural elements, clutter) using geometric coordinates and optionally Lidar intensity features. Use when the user wants to benchmark on 3DSES, or asks about evaluating this task. Reports mIoU.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2501.17534
  bibtex_key: merizette20253dses
  confidence: high
---

# 3dses-eval

> 3DSES: an indoor Lidar point cloud segmentation dataset with real and pseudo-labels from a 3D model — Mérizette et al. (2025) (arXiv:2501.17534, 2025)

## What this evaluates

Semantic segmentation of indoor Terrestrial Laser Scanning (TLS) point clouds. It probes a model's ability to classify 3D points into semantic categories (e.g., furniture, structural elements, clutter) using geometric coordinates and optionally Lidar intensity features.

## Datasets

- **3DSES** — total ?; splits: Gold (-1), Silver (-1), Bronze (-1)

## Metrics

- `mIoU` **(primary)** — range: [0, 1]
  - Mean Intersection over Union across all semantic classes. Calculated as the average of per-class IoU (intersection of predicted and ground truth points divided by their union).
- `OA` — range: [0, 1]
  - Overall Accuracy: the percentage of correctly classified points out of the total number of points.
- `AA` — range: [0, 1]
  - Average Accuracy: the mean of per-class accuracies (true positives divided by total ground truth points per class).

## Input / output format

**Input**: 3D point clouds represented as (x, y, z) coordinates, optionally augmented with Lidar intensity values. Points are subsampled to 1cm resolution for inference.

**Output**: A semantic class label for each point in the input point cloud.

## Scoring recipe

```python
def compute_metrics(preds, gold, classes):
    ious = []
    for c in classes:
        p = (preds == c)
        g = (gold == c)
        inter = np.sum(p & g)
        union = np.sum(p | g)
        ious.append(inter / union if union > 0 else 0.0)
    mIoU = np.mean(ious)
    OA = np.mean(preds == gold)
    class_accs = [np.sum((preds == c) & (gold == c)) / max(np.sum(gold == c), 1) for c in classes]
    AA = np.mean(class_accs)
    return mIoU, OA, AA
```

## Common pitfalls

- Models using voxelization (e.g., PointNeXt, Swin3D) do not fully exploit the high point density of 3DSES, leading to artificially low performance unless fine-resolution architectures are used.
- mIoU is heavily penalized by poor segmentation of small objects (<10^5 points), which can skew overall dataset difficulty assessments.
- Performance varies significantly depending on whether models are trained on real labels, pseudo-labels, or a mix, and whether Lidar intensity features are included.

## Evidence (verbatim from paper)

> Swin3D only slightly underperforms when trained on the pseudo-labels, with a 1.2% decrease in mIoU (47.8% vs. 49.0%) compared to the model trained on the real labels.

## Citation

```bibtex
@misc{merizette20253dses,
  title={3DSES: an indoor Lidar point cloud segmentation dataset with real and pseudo-labels from a 3D model},
  author={Mérizette et al. (2025)},
  year={2025},
  note={arXiv:2501.17534}
}
```

- arXiv: 2501.17534
