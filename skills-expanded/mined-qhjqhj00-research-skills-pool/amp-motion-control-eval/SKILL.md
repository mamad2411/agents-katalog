---
name: amp-motion-control-eval
description: Evaluates a physics-based character's ability to learn stylized locomotion and complex task execution (e.g., navigating targets, avoiding obstacles) by imitating unstructured motion datasets. It probes the model's capacity to compose disparate skills, generalize across gaits, and maintain high-fidelity motion tracking without manual motion planning. Use when the user wants to benchmark on AMP Motion Datasets, or asks about evaluating this task. Reports normalized task return.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2104.02180
  bibtex_key: peng2021amp
  confidence: high
---

# amp-motion-control-eval

> AMP: Adversarial Motion Priors for Stylized Physics-Based Character Control — Peng et al. (2021) (arXiv:2104.02180, 2021)

## What this evaluates

Evaluates a physics-based character's ability to learn stylized locomotion and complex task execution (e.g., navigating targets, avoiding obstacles) by imitating unstructured motion datasets. It probes the model's capacity to compose disparate skills, generalize across gaits, and maintain high-fidelity motion tracking without manual motion planning.

## Datasets

- **AMP Motion Datasets** — total ?; splits: train (-1)

## Metrics

- `normalized task return` **(primary)** — range: [0, 1]
  - Average reward per episode normalized to a [0, 1] scale, where 0 is the minimum possible return and 1 is the maximum. Computed over 32 episodes per model.
- `average pose error` — range: meters
  - Mean L2 distance between the simulated character's joint positions and the reference motion's joint positions at each time step, computed using root-relative coordinates in meters.

## Input / output format

**Input**: State observations from the Bullet physics simulation (joint positions, velocities, target coordinates/heading) and reference motion clips used to train the adversarial motion prior.

**Output**: Target joint positions for PD controllers, sampled at 30 Hz.

## Scoring recipe

```python
def compute_normalized_task_return(episode_rewards):
    return np.mean(episode_rewards)

def compute_average_pose_error(reference_poses, predicted_poses):
    # reference_poses and predicted_poses are (T, N_joints, 3)
    # positions are root-relative
    errors = np.linalg.norm(predicted_poses - reference_poses, axis=-1)
    return np.mean(errors)
```

## Common pitfalls

- Task return is pre-normalized to [0, 1] by the environment; do not divide by episode length or raw reward bounds.
- Pose error must be computed using root-relative joint positions, not absolute world coordinates.
- Results are averaged over 3 random seeds and 32 episodes per seed; reporting a single run will misrepresent performance.

## Evidence (verbatim from paper)

> Performance is recorded as the average normalized task return, with 0 being the minimum possible return per episode and 1 being the maximum possible return. The return is averaged across 3 models initialized with different random seeds, with 32 episodes recorded per model. Performance is evaluated using the average pose error, where the pose error $e_t^{	ext{pose}}$ at each time step $t$ is computed between the pose of the simulated character and the reference motion using the relative positions of each joint with respect to the root (in units of meters),

## Citation

```bibtex
@misc{peng2021amp,
  title={AMP: Adversarial Motion Priors for Stylized Physics-Based Character Control},
  author={Peng et al. (2021)},
  year={2021},
  note={arXiv:2104.02180}
}
```

- arXiv: 2104.02180
