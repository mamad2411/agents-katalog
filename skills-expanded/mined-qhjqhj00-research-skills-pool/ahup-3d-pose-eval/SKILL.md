---
name: ahup-3d-pose-eval
description: Evaluates monocular 3D human pose estimation models trained exclusively on synthetic 3D data and real 2D images, testing their ability to generalize to real-world 3D pose benchmarks without using any real 3D pose annotations during training. It probes domain adaptation capabilities, cross-dataset generalization, and the effectiveness of skeletal pose alignment strategies. Use when the user wants to benchmark on Human3.6M, MuPoTS, SURREAL, ScanAva+, MSCOCO, MPII Human Pose, or asks about evaluating this task. Reports PA MPJPE.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2105.10837
  bibtex_key: liu2021adaptedhumanpose
  confidence: high
---

# ahup-3d-pose-eval

> Adapted Human Pose: Monocular 3D Human Pose Estimation with Zero Real 3D Pose Data — Liu et al. (2021) (arXiv:2105.10837, 2021)

## What this evaluates

Evaluates monocular 3D human pose estimation models trained exclusively on synthetic 3D data and real 2D images, testing their ability to generalize to real-world 3D pose benchmarks without using any real 3D pose annotations during training. It probes domain adaptation capabilities, cross-dataset generalization, and the effectiveness of skeletal pose alignment strategies.

## Datasets

- **Human3.6M** — total ?; splits: test (-1)
- **MuPoTS** — total ?; splits: test (-1)
- **SURREAL** — total ?; splits: train (-1), val (-1), test (-1)
- **ScanAva+** — total 41; splits: train (36); repo https://github.com/ostadabbas/AdaptedHumanPose
- **MSCOCO** — total ?; splits: train (-1); HF `cocodataset/coco`
- **MPII Human Pose** — total ?; splits: train (-1)

## Metrics

- `PA MPJPE` **(primary)** — range: mm
  - Procrustes-aligned Mean Per Joint Position Error. Computes the average Euclidean distance between predicted and ground-truth 3D joints after applying optimal rigid transformation (rotation, translation, scaling) to align them.
- `3DPCK` — range: percent
  - 3D Percentage of Correct Keypoints. Measures the percentage of predicted joints falling within a 15 cm tolerance of the ground truth coordinates.
- `AUC` — range: percent
  - Area Under the Curve. Computes the integral of the 3DPCK curve across varying distance thresholds to summarize pose accuracy robustness.

## Input / output format

**Input**: Human-centered, cropped, and resized RGB images (256×256).

**Output**: 3D joint coordinates for 17 joints (pelvis-rooted), typically represented as a 64×64×64 heatmap or direct coordinate regression.

## Scoring recipe

```python
def compute_metrics(pred_3d, gt_3d):
    # Pelvis-rooted error
    pred_rooted = pred_3d - pred_3d[pelvis_idx]
    gt_rooted = gt_3d - gt_3d[pelvis_idx]
    # PA MPJPE
    aligned_pred = procrustes_alignment(pred_rooted, gt_rooted)
    pa_mpjpe = np.mean(np.linalg.norm(aligned_pred - gt_rooted, axis=2)) * 1000
    # 3DPCK (15cm tolerance)
    errors_cm = np.linalg.norm(pred_rooted - gt_rooted, axis=2) * 100
    pck = (np.sum(errors_cm <= 15.0) / errors_cm.size) * 100
    # AUC (trapezoidal integration over thresholds)
    auc = np.trapz(pck_curve, thresholds)
    return pa_mpjpe, pck, auc
```

## Common pitfalls

- Training strictly uses zero real 3D pose data; only synthetic 3D and real 2D images are available for supervision.
- Evaluations rely on pelvis-rooted error and Procrustes alignment to neutralize scale, rotation, and camera parameter differences across datasets.
- Datasets are artificially downsampled (SURREAL by 90x, H3.6M by 5x for training and 64x for testing) to balance iteration counts and batch sizes.
- Joint definitions differ across datasets; missing joints are interpolated using Human3.6M as a template, which can introduce alignment artifacts.

## Evidence (verbatim from paper)

> To provide a comprehensive view in our evaluation, we employ extensively-used metrics from real human pose benchmarks to report our performance, including mean per joint position error (MPJPE) for Human3.6M, 3D percentage of correct key-points (3DPCK), and the area under curve (AUC) for MuPoTS. For MPJPE, we also reported the Procrustes analysis (PA MPJPE) version, which is more reliable and fair, especially for cross-set evaluation due to varying camera parameters, joint definition, and body shape distributions.

## Citation

```bibtex
@misc{liu2021adaptedhumanpose,
  title={Adapted Human Pose: Monocular 3D Human Pose Estimation with Zero Real 3D Pose Data},
  author={Liu et al. (2021)},
  year={2021},
  note={arXiv:2105.10837}
}
```

- arXiv: 2105.10837
