---
name: 3d-vln-eval
description: Evaluates a model's ability to navigate 3D environments based on natural language instructions. It measures path efficiency, success in reaching targets, and robustness to scale calibration and data distribution shifts. Use when the user wants to benchmark on R2R, NaVILA, SceneVerse++ VLN, or asks about evaluating this task. Reports SR.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2604.01907
  bibtex_key: chen2026lifting
  confidence: high
---

# 3d-vln-eval

> Lifting Unlabeled Internet-level Data for 3D Scene Understanding — Chen et al. (2026) (arXiv:2604.01907, 2026)

## What this evaluates

Evaluates a model's ability to navigate 3D environments based on natural language instructions. It measures path efficiency, success in reaching targets, and robustness to scale calibration and data distribution shifts.

## Datasets

- **R2R** — total ?; splits: train (-1); repo https://github.com/peteanderson80/boston-pathway
- **NaVILA** — total 20000; splits: train (20000)
- **SceneVerse++ VLN** — total ?; splits: train (-1)

## Metrics

- `SR` **(primary)** — range: [0, 1]
  - Success Rate: fraction of episodes where the agent reaches within a threshold distance of the target.
- `SPL` — range: [0, 1]
  - Success weighted by Path Length: SR multiplied by the ratio of optimal path length to actual path length.
- `Dist` — range: [0, inf)
  - Distance-to-Goal: average Euclidean distance between the agent's final position and the target upon episode termination.

## Input / output format

**Input**: Camera trajectories, depth maps, and natural language navigation instructions.

**Output**: Sequence of navigation actions (e.g., forward, turn left/right) or trajectory waypoints.

## Scoring recipe

```python
sr = 0
spl_sum = 0
for episode in episodes:
    traj = model.navigate(instruction)
    if distance(traj.end, target) <= threshold:
        sr += 1
        optimal_len = compute_optimal_path(instruction)
        spl_sum += (optimal_len / len(traj))
sr = sr / len(episodes)
spl = spl_sum / len(episodes)
return sr, spl
```

## Common pitfalls

- Depth scale calibration is critical; arbitrary SfM scales must be converted to real-world meters using furniture-based monocular depth estimates.
- Label rebalancing during mixed-training can oversample rare actions, potentially biasing navigation behavior.

## Evidence (verbatim from paper)

> We evaluate two settings, zero-shot and mixed-training with R2R, and report results in [Tab. S.5]. ... SR↑ | OS↑ | SPL↑ | Dist↓ | PL

## Citation

```bibtex
@misc{chen2026lifting,
  title={Lifting Unlabeled Internet-level Data for 3D Scene Understanding},
  author={Chen et al. (2026)},
  year={2026},
  note={arXiv:2604.01907}
}
```

- arXiv: 2604.01907
