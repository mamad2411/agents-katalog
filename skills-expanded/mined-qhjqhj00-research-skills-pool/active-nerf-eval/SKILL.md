---
name: active-nerf-eval
description: Evaluates the accuracy of 3D geometry reconstruction from multi-view images using active pattern projection. It measures how closely the predicted point cloud matches the ground truth geometry and assesses robustness under varying view counts and camera-projector baselines. Use when the user wants to benchmark on NeRF derivative (synthetic), Real-world capture (RealSense D415), or asks about evaluating this task. Reports Chamfer Distance (mm).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2408.06592
  bibtex_key: tao2024activerf
  confidence: high
---

# active-nerf-eval

> ActiveNeRF: Learning Accurate 3D Geometry by Active Pattern Projection — Jianyu Tao et al. (2024) (arXiv:2408.06592, 2024)

## What this evaluates

Evaluates the accuracy of 3D geometry reconstruction from multi-view images using active pattern projection. It measures how closely the predicted point cloud matches the ground truth geometry and assesses robustness under varying view counts and camera-projector baselines.

## Datasets

- **NeRF derivative (synthetic)** — total 800; splits: test (800)
- **Real-world capture (RealSense D415)** — total 120; splits: test (120)

## Metrics

- `Chamfer Distance (mm)` **(primary)** — range: other
  - Symmetric Chamfer Distance: CD = 1/(2N) Σ_i min_j ||p_i - q_j|| + 1/(2M) Σ_j min_i ||q_j - p_i||, where p and q are predicted and ground truth points. Reported in millimeters.
- `P(CD < 0.01m) (%)` — range: percent
  - Percentage of points in the predicted point cloud where the Chamfer Distance to the ground truth is less than 0.01 meters (10 mm).
- `P(CD < 0.05m) (%)` — range: percent
  - Percentage of points in the predicted point cloud where the Chamfer Distance to the ground truth is less than 0.05 meters (50 mm).

## Input / output format

**Input**: Multi-view images (with and without active light projection), along with known camera and active light projector intrinsics and extrinsics. Images are downsampled to half resolution for input.

**Output**: Reconstructed 3D point cloud representing the scene geometry.

## Scoring recipe

```python
def evaluate(pred_pc, gt_pc, voxel_size=0.003):
    pred_pc = downsample_voxel(pred_pc, voxel_size)
    gt_pc = downsample_voxel(gt_pc, voxel_size)
    cd_m = chamfer_distance(pred_pc, gt_pc)
    cd_mm = cd_m * 1000
    p_01 = (cd_m < 0.01).mean() * 100
    p_05 = (cd_m < 0.05).mean() * 100
    return cd_mm, p_01, p_05
```

## Common pitfalls

- Point clouds must be downsampled to a voxel size of 0.003 before computing Chamfer Distance to ensure resolution consistency.
- The baseline between the camera and active light projector is critical; a zero baseline (collocated) causes the method to fail completely.
- Non-Lambertian surfaces (e.g., specular) can degrade active light pattern learning unless a BRDF module is included.
- Input images are downsampled to half resolution during training, which may affect high-frequency detail recovery.

## Evidence (verbatim from paper)

> We use chamfer distance between our reconstruction and ground truth to evaluate our model performance. For both reconstruction and ground truth, we downsample the point clouds to a voxel size of 0.003 to ensure resolution consistency. To measure the reconstruction quality in more depth, we compute the percentage of chamfer distance that is lower than 0.01m and 0.05m.

## Citation

```bibtex
@misc{tao2024activerf,
  title={ActiveNeRF: Learning Accurate 3D Geometry by Active Pattern Projection},
  author={Jianyu Tao et al. (2024)},
  year={2024},
  note={arXiv:2408.06592}
}
```

- arXiv: 2408.06592
