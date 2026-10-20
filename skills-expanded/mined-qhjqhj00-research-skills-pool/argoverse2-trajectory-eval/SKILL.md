---
name: argoverse2-trajectory-eval
description: Evaluates autonomous driving models on joint trajectory prediction and controllable generation tasks. It probes the model's ability to forecast multi-agent future paths accurately and generate realistic, goal-conditioned trajectories efficiently using diffusion-based sampling. Use when the user wants to benchmark on Argoverse 2, or asks about evaluating this task. Reports avgBrierMinFDE_K.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2408.00766
  bibtex_key: wang2024optimizing
  confidence: high
---

# argoverse2-trajectory-eval

> Optimizing Diffusion Models for Joint Trajectory Prediction and Controllable Generation — Wang et al. (2024) (arXiv:2408.00766, 2024)

## What this evaluates

Evaluates autonomous driving models on joint trajectory prediction and controllable generation tasks. It probes the model's ability to forecast multi-agent future paths accurately and generate realistic, goal-conditioned trajectories efficiently using diffusion-based sampling.

## Datasets

- **Argoverse 2** — total ?; splits: test (-1)

## Metrics

- `avgBrierMinFDE_K` **(primary)** — range: [0, 1]
  - Calculated similarly to avgMinFDE_K but scaled by the probability score of joint trajectory samples. Used as the primary metric for leaderboard ranking.
- `avgMinFDE_K` — range: meters
  - The average of the lowest final displacement error (FDE) across K joint trajectory samples.
- `avgMinADE_K` — range: meters
  - The average of the lowest average displacement error (ADE) across K joint trajectory samples.
- `actorMR_K` — range: [0, 1]
  - The rate of trajectory predictions considered missed (>2m FDE) in the lowest minFDE joint trajectory samples.
- `actorCR_K` — range: [0, 1]
  - The rate of collisions across the best (lowest avgMinFDE) joint trajectory samples.
- `JRDE` — range: meters
  - Joint Route Deviation Error measuring the displacement to realistic routes to evaluate trajectory realism.
- `JFDE` — range: meters
  - Joint Final Displacement Error evaluating the guidance effectiveness in controllable generation tasks.

## Input / output format

**Input**: Scene context features (target agent history, map, neighboring agents), noisy trajectory latent x_t, and diffusion time step t. For controllable generation, additional goal points/routes and velocity settings are provided as guidance conditions.

**Output**: Predicted noise epsilon_theta(x_t, t), which is decoded into 120-dimensional joint trajectories. For controllable generation, trajectories conditioned on goal points/routes.

## Scoring recipe

```python
def compute_metrics(preds, gt, k=128):
    # preds: (k, 120), gt: (1, 120)
    fde = np.linalg.norm(preds[-1] - gt[-1], axis=1)
    ade = np.mean(np.linalg.norm(preds - gt, axis=2), axis=1)
    min_fde = np.min(fde)
    min_ade = np.min(ade)
    mr = np.mean(fde > 2.0)
    cr = np.mean(check_collisions(preds))
    brier = min_fde * np.exp(-fde)
    return {'avgMinFDE': min_fde, 'avgMinADE': min_ade,
            'actorMR': mr, 'actorCR': cr, 'avgBrierMinFDE': brier}
```

## Common pitfalls

- Confusing the inference diffusion steps (T) with the training diffusion steps (T_train), which significantly impacts performance reporting and stability.
- Overlooking the sample clustering step (denoted by the * superscript in tables), which alters metric values compared to raw samples.
- Misinterpreting 'min' vs 'mean' metrics in controllable generation; 'min' evaluates the single best sample, while 'mean' assesses the ratio/average of all valid samples.

## Evidence (verbatim from paper)

> Given $K$ joint trajectories, the evaluation metrics are 1) $	extbf{avgMinFDE}_{K}$/$	extbf{avgMinADE}_{K}$: the average of lowest final/average displacement error (FDE/ADE) of joint trajectory samples; 2) $	extbf{actorMR}_{K}$: the rate of trajectory predictions that are considered to be “missed” (>2m FDE) in the lowest minFDE joint trajectory samples; 3) $	extbf{actorCR}_{K}$: the rate of collisions across “best” (lowest avgMinFDE) joint trajectory samples; 4) $	extbf{avgBrierMinFDE}_{K}$: calculated similarly to $	ext{avgMinFDE}_{K}$ but scaled by the probability score of joint trajectory samples.

## Citation

```bibtex
@misc{wang2024optimizing,
  title={Optimizing Diffusion Models for Joint Trajectory Prediction and Controllable Generation},
  author={Wang et al. (2024)},
  year={2024},
  note={arXiv:2408.00766}
}
```

- arXiv: 2408.00766
