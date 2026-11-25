---
name: 4seasons-eval
description: Evaluates visual SLAM and long-term localization for autonomous driving under challenging cross-season, multi-weather, and long-term environmental changes. Specifically probes visual odometry, global place recognition, and map-based visual localization capabilities. Use when the user wants to benchmark on 4Seasons, or asks about evaluating this task. Reports horizontal RMSE.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2301.01147
  bibtex_key: wenzel20234seasons
  confidence: high
---

# 4seasons-eval

> 4Seasons: Benchmarking Visual SLAM and Long-Term Localization for Autonomous Driving in Challenging Conditions — Wenzel et al. (2023) (arXiv:2301.01147, 2023)

## What this evaluates

Evaluates visual SLAM and long-term localization for autonomous driving under challenging cross-season, multi-weather, and long-term environmental changes. Specifically probes visual odometry, global place recognition, and map-based visual localization capabilities.

## Datasets

- **4Seasons** — total ?; splits: test (20)

## Metrics

- `horizontal RMSE` **(primary)** — range: meters
  - Root mean square error of the horizontal (x, y) translation components between predicted poses and GNSS/RTK reference poses after pose graph optimization.
- `percentage of accurate poses` — range: percent
  - Percentage of trajectory frames where the pose estimation error falls within an acceptable threshold, indicating sufficient accuracy for benchmarking long-term localization.
- `accumulated drift` — range: meters
  - Total positional and rotational error accumulated over the length of a sequence, used to evaluate visual odometry performance.

## Input / output format

**Input**: Synchronized 8-bit grayscale image frames and raw IMU measurements. For place recognition and localization, query images are matched against a reference map or previous frames.

**Output**: Predicted 6DoF camera poses (translation and rotation) for each timestamp, or ranked place recognition matches.

## Scoring recipe

```python
def compute_metrics(pred_poses, gt_poses, threshold=0.05):
    # Horizontal translation error
    errors = np.linalg.norm(pred_poses[:, :3] - gt_poses[:, :3], axis=1)
    rmse = np.sqrt(np.mean(errors**2))
    # Percentage of accurate poses
    accurate_count = np.sum(errors < threshold)
    accuracy_pct = (accurate_count / len(errors)) * 100
    # Accumulated drift (VO)
    drift = np.linalg.norm(pred_poses[-1, :3] - pred_poses[0, :3] - (gt_poses[-1, :3] - gt_poses[0, :3]))
    return {'horizontal_rmse': rmse, 'accurate_poses_pct': accuracy_pct, 'accumulated_drift': drift}
```

## Common pitfalls

- GNSS signals are unreliable in urban canyons and tunnels, so reference pose accuracy is only guaranteed where GNSS standard deviation is <5cm.
- Visual odometry evaluation relies on accumulated drift over time rather than per-frame ground truth, requiring only accurate start and end positions.
- Cross-season and weather variations cause drastic appearance changes, making feature matching and localization significantly harder than in single-season datasets.

## Evidence (verbatim from paper)

> We report the percentage of accurate reference poses for each trajectory. Moreover, we report the overall map accuracy in terms of horizontal RMSE between the GNSS poses and the refined poses after pose graph optimization.

## Citation

```bibtex
@misc{wenzel20234seasons,
  title={4Seasons: Benchmarking Visual SLAM and Long-Term Localization for Autonomous Driving in Challenging Conditions},
  author={Wenzel et al. (2023)},
  year={2023},
  note={arXiv:2301.01147}
}
```

- arXiv: 2301.01147
