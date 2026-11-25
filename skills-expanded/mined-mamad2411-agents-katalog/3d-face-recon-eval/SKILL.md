---
name: 3d-face-recon-eval
description: Evaluates the accuracy and realism of 3D face reconstruction and generation from single 2D images. Probes shape reconstruction fidelity against ground truth meshes, texture identity preservation across novel poses, and the diversity of synthesized 3D faces. Use when the user wants to benchmark on NoW Benchmark, REALY 3D Benchmark, or asks about evaluating this task. Reports Per-vertex error (mm).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2304.12483
  bibtex_key: rai2023towards
  confidence: high
---

# 3d-face-recon-eval

> Towards Realistic Generative 3D Face Models — Rai et al. (2023) (arXiv:2304.12483, 2023)

## What this evaluates

Evaluates the accuracy and realism of 3D face reconstruction and generation from single 2D images. Probes shape reconstruction fidelity against ground truth meshes, texture identity preservation across novel poses, and the diversity of synthesized 3D faces.

## Datasets

- **NoW Benchmark** — total 2054; splits: validation (-1), test (-1)
- **REALY 3D Benchmark** — total ?; splits: frontal (-1), side (-1)

## Metrics

- `Per-vertex error (mm)` **(primary)** — range: other
  - Rigidly align the predicted mesh to the ground truth using 3D face landmarks. Compute the Euclidean distance per vertex, then report the mean, median, and standard deviation across all vertices.
- `Landmark reconstruction error (mm)` — range: other
  - Compute the Euclidean distance between predicted and ground truth coordinates at specific facial regions (@nose, @mouth, @forehead, @cheek) and globally (@all).
- `Global diversity` — range: other
  - Generate n meshes and compute the mean vertex distance over all possible pairs of meshes.
- `Identity similarity` — range: [0, 1]
  - Measure the identity similarity score between the input 2D image and the corresponding 3D face rendered at multiple poses (same pose, 0°, ±15°, ±30°, ±45°).

## Input / output format

**Input**: Single 2D face image (typically cropped to 224×224 for shape estimation, or 1024×1024 for texture generation).

**Output**: 3D face mesh (FLAME-based shape with per-vertex displacements) and corresponding albedo/texture map, optionally rendered as 2D images at specified poses.

## Scoring recipe

```python
def compute_metrics(pred_mesh, gt_mesh, gt_landmarks):
    # Rigid alignment using 3D landmarks
    aligned_pred = rigid_align(pred_mesh, gt_mesh, landmarks=gt_landmarks)
    # Per-vertex error
    vertex_errors = np.linalg.norm(aligned_pred.vertices - gt_mesh.vertices, axis=1)
    per_vertex = {'mean': np.mean(vertex_errors), 'median': np.median(vertex_errors), 'std': np.std(vertex_errors)}
    # Landmark error
    landmark_errors = {}
    for region in ['nose', 'mouth', 'forehead', 'cheek', 'all']:
        landmark_errors[region] = compute_landmark_distance(aligned_pred, gt_mesh, region)
    return per_vertex, landmark_errors
```

## Common pitfalls

- NoW benchmark requires rigid alignment of the predicted mesh to the ground truth using 3D face landmarks before computing per-vertex error; skipping alignment invalidates the metric.
- REALY benchmark reports errors at specific facial regions (@nose, @mouth, etc.) separately; the '@all' metric is an aggregate that must be computed consistently across methods.
- Diversity metric requires generating exactly n=1000 meshes and computing the mean pairwise vertex distance across all combinations, not just a single sample or average distance to a mean mesh.

## Evidence (verbatim from paper)

> NoW benchmark [[46]] is a standard benchmark to evaluate the accuracy of 3D meshes estimated from 2D images. It consists of 2054 images for 100 test subjects across different expressions, poses, and occlusions, split across two sets for validation (20 subjects) and test (80 subjects). NoW provides 3D ground truth meshes for each test subject, and the predicted mesh is rigidly aligned with the ground truth mesh using 3D face landmarks. The per-vertex error is then used for all the subjects to compute the mean, median, and standard deviation of the errors.

## Citation

```bibtex
@misc{rai2023towards,
  title={Towards Realistic Generative 3D Face Models},
  author={Rai et al. (2023)},
  year={2023},
  note={arXiv:2304.12483}
}
```

- arXiv: 2304.12483
