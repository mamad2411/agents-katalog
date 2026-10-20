---
name: atlas-benchmark-eval
description: This benchmark evaluates human motion prediction algorithms by testing their ability to forecast future trajectories given past observations and environmental context. It systematically probes robustness to perception noise, generalization across different social and cultural environments, and performance under varying observation and prediction horizons. Use when the user wants to benchmark on ETH, ATC, THÖR, or asks about evaluating this task. Reports ADE.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2207.09830
  bibtex_key: rudenko2022atlas
  confidence: high
---

# atlas-benchmark-eval

> The Atlas Benchmark: an Automated Evaluation Framework for Human Motion Prediction — Rudenko et al. (2022) (arXiv:2207.09830, 2022)

## What this evaluates

This benchmark evaluates human motion prediction algorithms by testing their ability to forecast future trajectories given past observations and environmental context. It systematically probes robustness to perception noise, generalization across different social and cultural environments, and performance under varying observation and prediction horizons.

## Datasets

- **ETH** — total ?; splits: test (-1)
- **ATC** — total ?; splits: test (-1)
- **THÖR** — total ?; splits: test (-1)

## Metrics

- `ADE` **(primary)** — range: other
  - Average Displacement Error: computes the error between points of predicted trajectories and the ground truth at the same timestep.
- `FDE` — range: other
  - Final Displacement Error: computes the error at the last prediction step.
- `NLP` — range: other
  - Negative Log-Probability: computes the average probability of the ground truth position under the predicted distribution for the corresponding frame.
- `Top-k ADE and FDE` — range: other
  - Computes the displacements between the ground truth position and the closest of the K samples from the predicted distribution.

## Input / output format

**Input**: Observed past trajectories of all people in the testing scenario (timestamps, person IDs, positions), along with environment data such as obstacles, semantic grid maps, and goals.

**Output**: Predicted future trajectories encoded as either: (1) a set of K discrete sampled positions per timestep (particle-based), (2) 2D grid-map probabilities per person per timestep, or (3) a mixture of Gaussians (sequence of μ, Σ and weights π).

## Scoring recipe

```python
def compute_ade_fde(pred, gt):
    errors = np.linalg.norm(pred - gt, axis=1)
    return np.mean(errors), errors[-1]

def compute_topk_ade_fde(particles, gt, k=1):
    dists = np.linalg.norm(particles - gt[:, None, :], axis=2)
    min_dists = np.min(dists, axis=1)
    return np.mean(min_dists), min_dists[-1]

def compute_nlp(dist, gt):
    log_probs = dist.log_prob(gt)
    return -np.mean(log_probs)
```

## Common pitfalls

- Prediction accuracy heavily depends on the chosen observation length and prediction horizon, so results are not directly comparable without matching these parameters.
- Models must handle various uncertainty representations (particles, Gaussians, grid-maps), and using the wrong metric for a given output format leads to invalid scores.
- Generalization to unseen environments is frequently overlooked in related work, yet the benchmark explicitly requires cross-dataset evaluation to assess true robustness.

## Evidence (verbatim from paper)

> The Atlas benchmark supports geometric and probabilistic metrics, as defined in [[4]]. Geometric metrics include the Average Displacement Error (ADE), which describes the error between points of predicted trajectories and the ground truth at the same timestep, and the Final Displacement Error (FDE), which computes the error at the last prediction step. Probabilistic metrics include the Negative Log-Probability (NLP), which computes the average probability of the ground truth position under the predicted distribution for the corresponding frame, and Top-k ADE and FDE, which compute the displacements between the ground truth position and the closest of the K samples from the predicted distribution.

## Citation

```bibtex
@misc{rudenko2022atlas,
  title={The Atlas Benchmark: an Automated Evaluation Framework for Human Motion Prediction},
  author={Rudenko et al. (2022)},
  year={2022},
  note={arXiv:2207.09830}
}
```

- arXiv: 2207.09830
