---
name: 6dof-visual-localization-eval
description: Evaluates a model's ability to estimate 6-degree-of-freedom camera poses for query images against a reference 3D model, specifically testing robustness to drastic changes in lighting (day/night), weather, and seasonal vegetation. Use when the user wants to benchmark on Aachen Day-Night, RobotCar Seasons, CMU Seasons, or asks about evaluating this task. Reports translation error and rotation error.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1707.09092
  bibtex_key: sattler2017benchmarking
  confidence: high
---

# 6dof-visual-localization-eval

> Benchmarking 6DOF Outdoor Visual Localization in Changing Conditions — Sattler et al. (2017) (arXiv:1707.09092, 2017)

## What this evaluates

Evaluates a model's ability to estimate 6-degree-of-freedom camera poses for query images against a reference 3D model, specifically testing robustness to drastic changes in lighting (day/night), weather, and seasonal vegetation.

## Datasets

- **Aachen Day-Night** — total ?; splits: test (-1)
- **RobotCar Seasons** — total ?; splits: test (-1)
- **CMU Seasons** — total ?; splits: test (-1)

## Metrics

- `translation error and rotation error` **(primary)** — range: [0, ∞) m / [0, 180] deg
  - Translation error is the Euclidean distance between the estimated and ground truth camera centers. Rotation error is the angle between the estimated and ground truth rotation matrices.

## Input / output format

**Input**: Query image(s) and a reference 3D model (point cloud + reference camera poses/intrinsics).

**Output**: Estimated 6DOF camera pose (translation vector and rotation matrix) for each query image relative to the reference model.

## Scoring recipe

```python
def compute_pose_error(est_pose, gt_pose):
    trans_err = np.linalg.norm(est_pose[:3, 3] - gt_pose[:3, 3])
    rot_mat = est_pose[:3, :3] @ gt_pose[:3, :3].T
    trace = np.trace(rot_mat)
    rot_err = np.arccos(np.clip((trace - 1) / 2, -1, 1)) * 180 / np.pi
    return trans_err, rot_err
```

## Common pitfalls

- Ground truth poses for challenging conditions (night/seasons) are derived from hand-labeled 2D-3D matches or LIDAR/ICP alignment rather than direct SfM, which can introduce subtle inaccuracies.
- Reference models are constructed from a single environmental condition, requiring models to generalize across extreme appearance and geometric changes without condition-specific fine-tuning.
- Automotive datasets suffer from motion blur and auto-exposure artifacts that drastically reduce feature matchability compared to hand-held captures.

## Evidence (verbatim from paper)

> The final median RMS errors between aligned point clouds was under 0.10m in translation and 0.5∘ in rotation across all locations.

## Citation

```bibtex
@misc{sattler2017benchmarking,
  title={Benchmarking 6DOF Outdoor Visual Localization in Changing Conditions},
  author={Sattler et al. (2017)},
  year={2017},
  note={arXiv:1707.09092}
}
```

- arXiv: 1707.09092
