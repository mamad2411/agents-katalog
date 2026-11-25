---
name: 3d-segmentation-eval
description: Evaluates a unified transformer-based model's ability to perform instance and semantic segmentation on 3D point clouds derived from raw RGB-D sensor data. It probes cross-modal feature fusion between 2D images and 3D coordinates, and tests robustness to real-world sensor noise and misalignments compared to mesh-sampled inputs. Use when the user wants to benchmark on ScanNet, ScanNet200, or asks about evaluating this task. Reports mAP, mIoU.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2401.02416
  bibtex_key: jain2024odin
  confidence: high
---

# 3d-segmentation-eval

> ODIN: A Single Model for 2D and 3D Segmentation — Ayush Jain et al. (arXiv:2401.02416, 2024)

## What this evaluates

Evaluates a unified transformer-based model's ability to perform instance and semantic segmentation on 3D point clouds derived from raw RGB-D sensor data. It probes cross-modal feature fusion between 2D images and 3D coordinates, and tests robustness to real-world sensor noise and misalignments compared to mesh-sampled inputs.

## Datasets

- **ScanNet** — total ?; splits: val (-1)
- **ScanNet200** — total ?; splits: val (-1)

## Metrics

- `mAP` **(primary)** — range: percent
  - Mean Average Precision across all classes. Computed by averaging the Area Under the Precision-Recall curve for each class, typically evaluated at IoU thresholds of 0.25, 0.50, and 0.75.
- `mIoU` **(primary)** — range: percent
  - Mean Intersection over Union across all semantic classes. Calculated as the average of the ratio of intersection to union between predicted and ground truth masks for each class.

## Input / output format

**Input**: Raw sensor RGB-D data (unprojected RGB-D images or sensor RGB-D point clouds). For embodied tasks, the last N egocentric views including RGB, depth, and camera poses.

**Output**: Per-instance segmentation masks/boxes with class labels for 3D point clouds, or per-point semantic class labels. For embodied tasks, task execution plans and action sequences.

## Scoring recipe

```python
def compute_mAP(predictions, ground_truth, iou_thresh):
    tp, fp = 0, 0
    for pred in predictions:
        best_iou = max(compute_iou(pred, gt) for gt in ground_truth)
        if best_iou >= iou_thresh:
            tp += 1
        else:
            fp += 1
    precision = tp / (tp + fp)
    recall = tp / len(ground_truth)
    return precision, recall

def compute_mIoU(pred_masks, gt_masks):
    intersections = [np.sum(p & g) for p, g in zip(pred_masks, gt_masks)]
    unions = [np.sum(p | g) for p, g in zip(pred_masks, gt_masks)]
    return np.mean(intersections / unions) * 100
```

## Common pitfalls

- Performance drops significantly when evaluating on raw sensor point clouds versus mesh-sampled point clouds due to camera pose noise and depth variations.
- Directly comparing zero-shot foundation models (e.g., OpenScene) with supervised methods is unfair as they lack in-domain training.
- Comparing models trained on different input modalities (sensor RGB-D vs. mesh-sampled point clouds) without accounting for preprocessing differences can skew results.

## Evidence (verbatim from paper)

> Evaluation metrics: We follow the standard evaluation metrics, namely mean Average Precision (mAP) for instance segmentation and mean Intersection over Union (mIoU) for semantic segmentation.

## Citation

```bibtex
@misc{jain2024odin,
  title={ODIN: A Single Model for 2D and 3D Segmentation},
  author={Ayush Jain et al.},
  year={2024},
  note={arXiv:2401.02416}
}
```

- arXiv: 2401.02416
