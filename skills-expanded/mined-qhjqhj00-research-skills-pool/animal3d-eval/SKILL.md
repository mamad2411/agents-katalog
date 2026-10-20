---
name: animal3d-eval
description: This benchmark evaluates the ability of deep learning models to estimate 3D pose and shape of diverse mammal species from single images. It probes cross-species generalization, synthetic-to-real transfer, and the adaptation of human-centric pose estimation architectures to non-human anatomies. Use when the user wants to benchmark on Animal3D, or asks about evaluating this task. Reports S-MPJPE.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2308.11737
  bibtex_key: xu2023animal3d
  confidence: high
---

# animal3d-eval

> Animal3D: A Comprehensive Dataset of 3D Animal Pose and Shape — Xu et al. (2023) (arXiv:2308.11737, 2023)

## What this evaluates

This benchmark evaluates the ability of deep learning models to estimate 3D pose and shape of diverse mammal species from single images. It probes cross-species generalization, synthetic-to-real transfer, and the adaptation of human-centric pose estimation architectures to non-human anatomies.

## Datasets

- **Animal3D** — total 3379; splits: train (3059), test (320)

## Metrics

- `S-MPJPE` **(primary)** — range: other
  - Scale-aligned Mean Per Joint Position Error. Computes the mean Euclidean distance between predicted and ground-truth 3D joint positions after aligning the predicted and ground-truth scales via a uniform scaling factor.
- `PA-MPJPE` — range: other
  - Procrustes-aligned Mean Per Joint Position Error. Computes the mean Euclidean distance after aligning both scale and rotation between predictions and ground truth using rigid Procrustes analysis.
- `PCK` — range: [0, 1]
  - Percentage of Correct Keypoints. Measures the fraction of predicted 2D joints that fall within a threshold distance of the ground-truth 2D joints, where the threshold is defined as half the head-to-tail length of the animal.

## Input / output format

**Input**: Cropped and resized (224x224) animal images with bounding boxes, optionally augmented with random rotation and flipping.

**Output**: 26 predicted 3D joint positions (vertices) and corresponding 2D projections, along with SMAL model shape and pose parameters.

## Scoring recipe

```python
def compute_metrics(pred_3d, gt_3d, pred_2d, gt_2d, head_tail_len):
    # S-MPJPE
    scale = np.linalg.norm(gt_3d) / np.linalg.norm(pred_3d)
    s_mpjpe = np.mean(np.linalg.norm(pred_3d * scale - gt_3d, axis=1))
    # PA-MPJPE
    aligned_pred, _ = procrustes_alignment(pred_3d, gt_3d)
    pa_mpjpe = np.mean(np.linalg.norm(aligned_pred - gt_3d, axis=1))
    # PCK
    threshold = head_tail_len / 2.0
    correct = np.linalg.norm(pred_2d - gt_2d, axis=1) < threshold
    pck = np.mean(correct)
    return s_mpjpe, pa_mpjpe, pck
```

## Common pitfalls

- Using unaligned MPJPE instead of S-MPJPE/PA-MPJPE, which penalizes scale differences rather than pose accuracy.
- Applying fixed pixel thresholds for PCK instead of the relative head-to-tail length, causing unfair comparisons across species.
- Assuming direct transfer of human pose estimators without accounting for the anatomical and parameter-space differences between SMPL and SMAL models.

## Evidence (verbatim from paper)

> Evaluation metrics. We report scale-aligned mean per joint position error (S-MPJPE) and Procrustes-aligned mean per joint position error (PA-MPJPE) in mm as the main evaluation metrics, where the latter is the former plus rotational alignment. We do not use the popular per joint position error (MPJPE) in 3D human pose estimation since the scale of animals can vary a lot. We also report the 2D Percentage of Correct Keypoints (PCK) with threshold defined by half of the head-to-tail length to measure how well the prediction aligns with the 2D image.

## Citation

```bibtex
@misc{xu2023animal3d,
  title={Animal3D: A Comprehensive Dataset of 3D Animal Pose and Shape},
  author={Xu et al. (2023)},
  year={2023},
  note={arXiv:2308.11737}
}
```

- arXiv: 2308.11737
