---
name: 3d-semantic-segmentation-eval
description: This benchmark evaluates a model's ability to perform 3D semantic segmentation on indoor scenes. It probes the model's capacity to assign per-point semantic labels to 3D point clouds and assesses performance across head, common, and long-tail object categories. Use when the user wants to benchmark on ScanNet/ScanNet200, or asks about evaluating this task. Reports mIoU.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2410.13924
  bibtex_key: ji2024arkitlabelmaker
  confidence: high
---

# 3d-semantic-segmentation-eval

> ARKit LabelMaker: A New Scale for Indoor 3D Scene Understanding — Ji et al. (2024) (arXiv:2410.13924, 2024)

## What this evaluates

This benchmark evaluates a model's ability to perform 3D semantic segmentation on indoor scenes. It probes the model's capacity to assign per-point semantic labels to 3D point clouds and assesses performance across head, common, and long-tail object categories.

## Datasets

- **ScanNet/ScanNet200** — total 1613; splits: train (1201), val (312), test (100)

## Metrics

- `mIoU` **(primary)** — range: percent
  - Mean Intersection-over-Union computed as the average of per-class IoU scores across all evaluated categories. Per-class IoU is the ratio of the intersection to the union of predicted and ground truth points for each class.
- `mAcc` — range: percent
  - Mean per-class accuracy, calculated by averaging the accuracy of each class individually (intersection over ground truth count per class).
- `tAcc` — range: percent
  - Total per-point accuracy, calculated as the ratio of correctly classified points to the total number of points in the scene.

## Input / output format

**Input**: 3D point clouds down-sampled to a 2 cm voxel size with preserved normal information.

**Output**: Per-point semantic class labels (predictions over 20 or 200 classes depending on the benchmark).

## Scoring recipe

```python
def compute_metrics(preds, gold, num_classes):
    ious, accs = [], []
    for c in range(num_classes):
        p_c = (preds == c)
        g_c = (gold == c)
        inter = np.sum(p_c & g_c)
        union = np.sum(p_c | g_c)
        ious.append(inter / union if union > 0 else 0.0)
        accs.append(inter / np.sum(g_c) if np.sum(g_c) > 0 else 0.0)
    mIoU = np.mean(ious) * 100
    mAcc = np.mean(accs) * 100
    tAcc = np.sum(preds == gold) / len(gold) * 100
    return mIoU, mAcc, tAcc
```

## Common pitfalls

- Confusing the 20-class ScanNet evaluation with the 200-class ScanNet200 evaluation, as they share the same scene splits but use different label spaces.
- Ignoring the head/common/tail class breakdown, which is critical for assessing the long-tail performance improvements highlighted in the paper.
- Using the original 186-class ARKit LabelMaker label space directly for evaluation instead of mapping to the ScanNet/ScanNet200 classes as specified in the protocol.

## Evidence (verbatim from paper)

> We follow the standard metrics of the ScanNet 3D semantic segmentation task and compute the mean and per-class intersection-over-union (IoU), the mean per-class accuracy (mAcc) and the total per-point accuracy (tAcc).

## Citation

```bibtex
@misc{ji2024arkitlabelmaker,
  title={ARKit LabelMaker: A New Scale for Indoor 3D Scene Understanding},
  author={Ji et al. (2024)},
  year={2024},
  note={arXiv:2410.13924}
}
```

- arXiv: 2410.13924
