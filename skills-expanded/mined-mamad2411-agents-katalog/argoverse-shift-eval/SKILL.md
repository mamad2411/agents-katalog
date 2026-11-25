---
name: argoverse-shift-eval
description: Evaluates the out-of-distribution generalization capability of trajectory prediction models on unseen HD map geometries. It measures how well models maintain prediction accuracy when transferred from seen to unseen domains without retraining. Use when the user wants to benchmark on argoverse-shift, or asks about evaluating this task. Reports minADE.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2305.17965
  bibtex_key: ye2023frenet
  confidence: high
---

# argoverse-shift-eval

> Improving the Generalizability of Trajectory Prediction Models with Frenet-Based Domain Normalization — Ye et al. (2023) (arXiv:2305.17965, 2023)

## What this evaluates

Evaluates the out-of-distribution generalization capability of trajectory prediction models on unseen HD map geometries. It measures how well models maintain prediction accuracy when transferred from seen to unseen domains without retraining.

## Datasets

- **argoverse-shift** — total ?; splits: train (-1), val (-1), test (-1)

## Metrics

- `minADE` **(primary)** — range: meters
  - Minimum over 6 predicted trajectories of the average L2 displacement error between predicted and ground-truth positions over the 3-second future horizon.
- `minFDE` — range: meters
  - Minimum over 6 predicted trajectories of the L2 displacement error at the final 3-second time step.
- `MR` — range: percent
  - Miss Rate: fraction of predictions where the final displacement error exceeds a predefined threshold (typically 2 meters in trajectory prediction benchmarks).

## Input / output format

**Input**: Initial 2 seconds of agent observations (positions/trajectories) and HD map geometry.

**Output**: 6 predicted future trajectories (positions) for each agent over the next 3 seconds.

## Scoring recipe

```python
def compute_metrics(preds, gt):
    # preds: (B, 6, T, 2), gt: (B, T, 2), T=3
    errors = np.linalg.norm(preds - gt[:, None, :], axis=-1)  # (B, 6, T)
    ade = errors.mean(axis=-1)  # (B, 6)
    fde = errors[:, :, -1]  # (B, 6)
    min_ade = ade.min(axis=-1)
    min_fde = fde.min(axis=-1)
    mr = (fde.min(axis=-1) > 2.0).mean()  # threshold typically 2m
    return min_ade, min_fde, mr
```

## Common pitfalls

- Confusing the 'seen' (validation) and 'unseen' (test) domain splits, which are automatically generated for domain shift evaluation.
- Failing to select the best of the 6 predicted trajectories before computing minADE and minFDE, which would inflate error values.
- Assuming standard Argoverse motion forecasting splits apply directly without the specific domain-shift partitioning used in argoverse-shift.

## Evidence (verbatim from paper)

> Metrics: We employ three standard metrics for trajectory prediction, including the Minimum Average Displacement Error (minADE), Minimum Final Displacement Error (minFDE) and Miss Rate (MR). Models predict six trajectories, and we report the best result with minimum errors.

## Citation

```bibtex
@misc{ye2023frenet,
  title={Improving the Generalizability of Trajectory Prediction Models with Frenet-Based Domain Normalization},
  author={Ye et al. (2023)},
  year={2023},
  note={arXiv:2305.17965}
}
```

- arXiv: 2305.17965
