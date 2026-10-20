---
name: argoverse2-waymo-eval
description: Evaluates the plausibility, diversity, and kinematic consistency of generated multi-agent traffic scene continuations conditioned on 5-second histories. It probes a model's ability to generate realistic, diverse, and physically plausible future trajectories over a 6-second horizon, including out-of-distribution generalization across different autonomous driving datasets. Use when the user wants to benchmark on Argoverse 2 (A2), Waymo (WO), or asks about evaluating this task. Reports minADE.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2504.05422
  bibtex_key: yao2025epdiffuser
  confidence: high
---

# argoverse2-waymo-eval

> EP-Diffuser: An Efficient Diffusion Model for Traffic Scene Generation and Prediction via Polynomial Representations — Yue Yao et al. (2025) (arXiv:2504.05422, 2025)

## What this evaluates

Evaluates the plausibility, diversity, and kinematic consistency of generated multi-agent traffic scene continuations conditioned on 5-second histories. It probes a model's ability to generate realistic, diverse, and physically plausible future trajectories over a 6-second horizon, including out-of-distribution generalization across different autonomous driving datasets.

## Datasets

- **Argoverse 2 (A2)** — total ?; splits: train (199908), val_R20P (5000), val_C500 (500)
- **Waymo (WO)** — total ?; splits: val_R20P (8400), val_C500 (500)

## Metrics

- `minADE` **(primary)** — range: m
  - Minimum Average Displacement Error over K=32 sampled trajectories. Computed as the minimum mean L2 distance between predicted and ground truth positions across all time steps for each sample, then taking the minimum over the 32 samples.
- `coverage` — range: m
  - Average pairwise Euclidean distance between the final positions of the 32 sampled trajectories. Serves as an auxiliary diversity metric.
- `realism` — range: [0, 1]
  - Sub-metric from the Sim Agents evaluation suite measuring scene plausibility. Computed over 32 sampled scenes.
- `kinematic` — range: [0, 1]
  - Sub-metric from the Sim Agents evaluation suite measuring agent kinematic plausibility. Computed over 32 sampled scenes.
- `interactive` — range: [0, 1]
  - Sub-metric from the Sim Agents evaluation suite measuring agent interaction realism. Computed over 32 sampled scenes.
- `map` — range: [0, 1]
  - Sub-metric from the Sim Agents evaluation suite measuring map adherence. Computed over 32 sampled scenes.

## Input / output format

**Input**: 5-second history of agent trajectories and map elements (lane centers and crosswalks).

**Output**: 6-second future trajectories for all agents. Generative models output 32 sampled scenes; regression models output a fixed number of predictions (e.g., 6), evaluated via ensemble/top-k selection.

## Scoring recipe

```python
def compute_coverage(samples_32):
    final_pos = [s[-1] for s in samples_32]
    return mean(pairwise_euclidean_distance(p1, p2) for p1, p2 in combinations(final_pos, 2))

def compute_minADE(samples_32, gt):
    ades = [mean(l2_distance(pred_t, gt_t) for t in range(T)) for pred in samples_32]
    return min(ades)

# Sim Agents metrics (realism, kinematic, interactive, map) are computed over the 32 samples using the official Sim Agents evaluation protocol.
```

## Common pitfalls

- OoD testing on Waymo uses a 4.1-second prediction horizon instead of the standard 6 seconds due to shorter recording lengths.
- Coverage is an auxiliary diversity metric and should not be interpreted as a standalone performance measure; it must be evaluated alongside plausibility metrics.
- FMAE-MA approximates the 32-sample requirement by ensembling 6 independently trained models and selecting the top 32 predictions by predicted probability, which may bias diversity metrics.

## Evidence (verbatim from paper)

> Inspired by the inter-policy diversity metric in [[37]], we compute the average pairwise distance between the final positions of the 32 sampled trajectories to measure the trajectory diversity. This metric serves as an auxiliary indicator and is not used as a standalone measure of performance – since high coverage is only meaningful when accompanied by high plausibility.

## Citation

```bibtex
@misc{yao2025epdiffuser,
  title={EP-Diffuser: An Efficient Diffusion Model for Traffic Scene Generation and Prediction via Polynomial Representations},
  author={Yue Yao et al. (2025)},
  year={2025},
  note={arXiv:2504.05422}
}
```

- arXiv: 2504.05422
