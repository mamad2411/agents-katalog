---
name: 3d-pose-estimation-manifold-eval
description: Evaluates a model's ability to estimate 3D joint poses of articulated objects (mice, fish, human hands) from depth images. The benchmark probes continuous structured prediction on Lie group manifolds, requiring the model to output kinematic chain or tree configurations that align with ground-truth skeletal models. Use when the user wants to benchmark on Mouse, Fish, Human hand, or asks about evaluating this task. Reports average joint error.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1612.00596
  bibtex_key: zhang2016learning
  confidence: high
---

# 3d-pose-estimation-manifold-eval

> Learning to Search on Manifolds for 3D Pose Estimation of Articulated Objects — Yu Zhang et al. (2016) (arXiv:1612.00596, 2016)

## What this evaluates

Evaluates a model's ability to estimate 3D joint poses of articulated objects (mice, fish, human hands) from depth images. The benchmark probes continuous structured prediction on Lie group manifolds, requiring the model to output kinematic chain or tree configurations that align with ground-truth skeletal models.

## Datasets

- **Mouse** — total 108221; splits: train (104096), test (4125)
- **Fish** — total 96924; splits: train (95104), test (1820)
- **Human hand** — total 81009; splits: train (72757), test (8252)

## Metrics

- `average joint error` **(primary)** — range: other
  - Mean Euclidean distance between predicted and ground-truth 3D joint coordinates across all annotated joints in the kinematic chain or tree.

## Input / output format

**Input**: Square depth image patches (e.g., 40x40 to 224x224) containing the cropped object, normalized as a 3D point cloud with empirical centroid at origin.

**Output**: 3D coordinates for each joint in the object's kinematic chain/tree, represented as sequential rigid transformations (tangent vectors on a Lie group manifold).

## Scoring recipe

```python
def average_joint_error(pred_joints, gt_joints):
    total_error = 0.0
    for p, g in zip(pred_joints, gt_joints):
        total_error += np.linalg.norm(p - g)
    return total_error / len(pred_joints)
```

## Common pitfalls

- Input patch sizes and CNN architectures vary significantly across benchmarks and method variants (parallel vs sequential).
- The human hand benchmark evaluates only 14 out of 36 annotated joints, following prior work conventions.
- Error is reported in millimeters (mm), not normalized units, making cross-dataset comparison of absolute values difficult.

## Evidence (verbatim from paper)

> For performance evaluation, the commonly used metric of average joint error is adopted, which computes the averaged Euclidean distance over all 3D joints. The training set has 104,096 depth images and test set has 4,125 depth images of different lab mice. Training set contains 95,104 images, and test set contains 1,820 images of different zebrafish in water tanks... It consists of 72,757 training and 8,252 test images. 36 3D joints are annotated, while following[10], 14 of them are in use.

## Citation

```bibtex
@misc{zhang2016learning,
  title={Learning to Search on Manifolds for 3D Pose Estimation of Articulated Objects},
  author={Yu Zhang et al. (2016)},
  year={2016},
  note={arXiv:1612.00596}
}
```

- arXiv: 1612.00596
