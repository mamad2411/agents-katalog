---
name: amodal-3d-reconstruction-eval
description: Evaluates a model's ability to infer occluded (amodal) 3D geometry and predict physically stable configurations in cluttered tabletop scenes. It further tests downstream robotic manipulation success (grasping, pushing, rearranging) under varying levels of visual occlusion. Use when the user wants to benchmark on ShapeNet, MuJoCo Cluttered Tabletop Benchmark, or asks about evaluating this task. Reports Chamfer distance.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2009.13146
  bibtex_key: agnew2020amodal
  confidence: high
---

# amodal-3d-reconstruction-eval

> Amodal 3D Reconstruction for Robotic Manipulation via Stability and Connectivity — Agnew et al. (2020) (arXiv:2009.13146, 2020)

## What this evaluates

Evaluates a model's ability to infer occluded (amodal) 3D geometry and predict physically stable configurations in cluttered tabletop scenes. It further tests downstream robotic manipulation success (grasping, pushing, rearranging) under varying levels of visual occlusion.

## Datasets

- **ShapeNet** — total 8171; splits: train (4803), test (3368)
- **MuJoCo Cluttered Tabletop Benchmark** — total 2574; splits: test (2574)

## Metrics

- `Chamfer distance` **(primary)** — range: other
  - Average Chamfer distance between predicted and ground truth mesh/point cloud representations. Lower values indicate better geometric alignment.
- `Task success rate` — range: [0, 1]
  - Percentage of successfully completed manipulation tasks (grasping, pushing, rearrangement) out of the total number of generated task instances.

## Input / output format

**Input**: RGB images (or RGBD observations) of cluttered tabletop scenes with randomized camera views, along with ground truth instance segmentations for evaluation isolation.

**Output**: Multi-channel voxel representation or 3D mesh of the scene, including inferred occluded (amodal) regions and object bases.

## Scoring recipe

```python
def compute_chamfer_distance(predictions, ground_truth):
    total_cd = 0.0
    for pred_mesh, gt_mesh in zip(predictions, ground_truth):
        total_cd += chamfer_distance(pred_mesh.points, gt_mesh.points)
    return total_cd / len(predictions)

def compute_task_success_rate(tasks, predictions):
    successes = 0
    for task, pred_mesh in zip(tasks, predictions):
        if execute_manipulation_in_mujoco(pred_mesh, task.goal):
            successes += 1
    return successes / len(tasks)
```

## Common pitfalls

- Applying stability and connectivity loss gradients to observed (non-occluded) voxels instead of restricting them to occluded voxels only, which violates the training protocol.
- Evaluating manipulation performance without using ground truth instance segmentations, which would confound segmentation errors with reconstruction errors.
- Measuring scene stability without a standardized physics simulation (MuJoCo) for a fixed duration (5 seconds) under gravity, leading to inconsistent stability metrics.

## Evidence (verbatim from paper)

> We quantitatively compare the visual reconstruction quality of ARM to our baselines on reconstruction of cluttered scenes generated with held-out test objects and ground truth segmentations in Figure 4 (left). ARM outperforms the baseline at all occlusion levels, improving Chamfer loss by 28% overall. ... To evaluate the efficacy of our method on robot manipulation tasks, we create a suite of robotics manipulation tasks across a range of challenging objects in cluttered scenes. We consider three important robot tasks: grasping, pushing, and rearrangement... Figure 6 (left) shows average task success rates on the manipulation tasks for each of the methods.

## Citation

```bibtex
@misc{agnew2020amodal,
  title={Amodal 3D Reconstruction for Robotic Manipulation via Stability and Connectivity},
  author={Agnew et al. (2020)},
  year={2020},
  note={arXiv:2009.13146}
}
```

- arXiv: 2009.13146
