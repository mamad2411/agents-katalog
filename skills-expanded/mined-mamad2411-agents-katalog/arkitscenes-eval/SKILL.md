---
name: arkitscenes-eval
description: Evaluates 3D indoor scene understanding by testing object detection (single-frame and whole-scene) and color-guided depth upsampling on real-world mobile RGB-D data captured with consumer LiDAR devices. Use when the user wants to benchmark on ARKitScenes, or asks about evaluating this task. Reports mAP (mean average precision).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2111.08897
  bibtex_key: baruch2021arkitscenes
  confidence: high
---

# arkitscenes-eval

> ARKitScenes: A Diverse Real-World Dataset For 3D Indoor Scene Understanding Using Mobile RGB-D Data — Baruch et al. (2021) (arXiv:2111.08897, 2021)

## What this evaluates

Evaluates 3D indoor scene understanding by testing object detection (single-frame and whole-scene) and color-guided depth upsampling on real-world mobile RGB-D data captured with consumer LiDAR devices.

## Datasets

- **ARKitScenes** — total ?; splits: train (323868), test (41139), val (5600)

## Metrics

- `mAP (mean average precision)` **(primary)** — range: [0, 1]
  - Mean of average precision scores computed across all 17 furniture categories for 3D oriented bounding boxes.
- `L1` — range: meters
  - Mean absolute difference between predicted and ground truth depth values per pixel.
- `RMSE` — range: meters
  - Square root of the mean squared difference between predicted and ground truth depth values per pixel.

## Input / output format

**Input**: RGB-D frames or point clouds with XYZ coordinates and features for detection; low-resolution depth maps paired with high-resolution color images for upsampling.

**Output**: 3D oriented bounding boxes (center, size, category) for detection; high-resolution depth map for upsampling.

## Scoring recipe

```python
def compute_mAP(preds, gts, iou_thresh=0.25):
    ap_scores = []
    for cat in categories:
        tp, fp = 0, 0
        for p, g in zip(preds[cat], gts[cat]):
            if match_iou(p, g) >= iou_thresh: tp += 1
            else: fp += 1
        ap_scores.append(tp / (tp + fp))
    return sum(ap_scores) / len(ap_scores)

def compute_l1_rmse(pred_d, gt_d, mask=None):
    diff = pred_d - gt_d
    if mask is not None: diff = diff[mask]
    l1 = np.mean(np.abs(diff))
    rmse = np.sqrt(np.mean(diff**2))
    return l1, rmse
```

## Common pitfalls

- 65% of frames become empty after filtering; only boxes with ≥5 corners in the camera frustum and ≥10 points are kept.
- Real-world depth maps contain occlusions and artifacts (specular/transparent objects), requiring masking or adapted losses (e.g., SSIM cannot be used directly as a full-reference metric).
- Long videos are artificially subsampled to a maximum of 300 frames per scan to prevent model bias toward longer sequences.

## Evidence (verbatim from paper)

> VoteNet[4] is able to achieve mAP (mean average precision) of 0.358, while extra primitive supervision [43] and attention model [30] can further improve the overall performance to 0.383 and 0.419 respectively.

## Citation

```bibtex
@misc{baruch2021arkitscenes,
  title={ARKitScenes: A Diverse Real-World Dataset For 3D Indoor Scene Understanding Using Mobile RGB-D Data},
  author={Baruch et al. (2021)},
  year={2021},
  note={arXiv:2111.08897}
}
```

- arXiv: 2111.08897
