---
name: audio-visual-navigation-eval
description: Probes an embodied agent's ability to navigate unmapped 3D environments using fused audio-visual observations to locate both static and moving sound sources. It tests generalization to unseen environments and unheard audio distributions under clean and noisy conditions. Use when the user wants to benchmark on Replica, Matterport3D, or asks about evaluating this task. Reports Success rate (SR).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2111.14843
  bibtex_key: younes2021catchme
  confidence: high
---

# audio-visual-navigation-eval

> Catch Me If You Hear Me: Audio-Visual Navigation in Complex Unmapped Environments with Moving Sounds — Younes et al. (2021) (arXiv:2111.14843, 2021)

## What this evaluates

Probes an embodied agent's ability to navigate unmapped 3D environments using fused audio-visual observations to locate both static and moving sound sources. It tests generalization to unseen environments and unheard audio distributions under clean and noisy conditions.

## Datasets

- **Replica** — total ?; splits: train (9), val (4), test (5)
- **Matterport3D** — total ?; splits: train (59), val (10), test (12)

## Metrics

- `Success rate (SR)` **(primary)** — range: percent
  - The share of successful episodes out of all test episodes. An episode is successful if the agent executes the stop action at the goal location.
- `Success weighted by path length (SPL)` — range: [0, 1]
  - The ratio of the shortest path length to the goal over the executed path length, averaged over successful episodes.
- `Success weighted by number of actions (SNA)` — range: [0, 1]
  - The ratio of the number of actions required for the shortest path to the actual actions taken, averaged over successful episodes. It accounts for orientation changes unlike SPL.
- `Dynamic success weighted by path length (DSPL)` — range: [0, 1]
  - The primary metric for dynamic tasks. Calculated as the ratio of the path length to the earliest reachable intersection over the executed path length for successful episodes.
- `Dynamic success weighted by number of actions (DSNA)` — range: [0, 1]
  - An adjusted version of SNA that uses the distance to the earliest reachable intersection instead of the goal location.

## Input / output format

**Input**: Visual observations (RGB images) and spatial audio features from an embodied agent navigating an unmapped 3D environment, along with a target sound class.

**Output**: Discrete navigation actions (e.g., move forward, turn left/right, stop) to reach the sound source location.

## Scoring recipe

```python
def compute_metrics(paths, shortest_paths, actions, shortest_actions, success_mask):
    n_success = sum(success_mask)
    sr = n_success / len(success_mask)
    spl = sum(shortest_paths[i] / paths[i] for i in range(len(paths)) if success_mask[i]) / n_success
    sna = sum(shortest_actions[i] / actions[i] for i in range(len(actions)) if success_mask[i]) / n_success
    return sr, spl, sna
# For dynamic tasks, replace paths and shortest_paths with distances to the earliest reachable intersection.
```

## Common pitfalls

- Unheard vs. heard sound splits must be strictly maintained; evaluating on unheard sounds tests generalization to novel audio distributions, not just unseen environments.
- For dynamic tasks, agents must track moving sources; stopping at the initial sound position is insufficient and heavily penalized by DSPL/DSNA.
- Training on complex/noisy scenarios can sometimes degrade performance on clean 'heard' sound benchmarks due to dataset size limitations or removal of overfitting channels.

## Evidence (verbatim from paper)

> We evaluate the navigation performance based on: Success rate (SR): The share of successful episodes of all test episodes. An episode is considered successful if the agent executes the stop action at the goal location. Success weighted by path length (SPL) [44]: The ratio of the length of the shortest path to the goal to the length of the executed path for the successful episodes. ... We use the same train/val/test splits protocol used by [5], [9], where Replica splits into 9/4/5 scenes and Matterport3D (MP3D) splits into 59/10/12 scenes. The 102 different sounds are split into 73/11/18.

## Citation

```bibtex
@misc{younes2021catchme,
  title={Catch Me If You Hear Me: Audio-Visual Navigation in Complex Unmapped Environments with Moving Sounds},
  author={Younes et al. (2021)},
  year={2021},
  note={arXiv:2111.14843}
}
```

- arXiv: 2111.14843
