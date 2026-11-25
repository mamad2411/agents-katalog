---
name: MDBI_MTBI
description: Evaluates the robustness and safety of autonomous driving systems by quantifying how far and how long the vehicle operates between human interventions (disengagements). It enables unbiased comparison across different AV platforms and road environments by normalizing disengagement frequency with spatial and temporal data. Use when the user has predictions and gold and needs to compute MDBI, MTBI.
metadata:
  skill_kind: metric
  source_arxiv: 2006.02518
  bibtex_key: paz2020autonomous
  confidence: high
---

# MDBI_MTBI

> Autonomous Vehicle Benchmarking using Unbiased Metrics — Paz et al. (2020) (arXiv:2006.02518, 2020)

## What this evaluates

Evaluates the robustness and safety of autonomous driving systems by quantifying how far and how long the vehicle operates between human interventions (disengagements). It enables unbiased comparison across different AV platforms and road environments by normalizing disengagement frequency with spatial and temporal data.

## Datasets

- **UC San Diego AV Deployment Data** — total ?; splits: (unstated)

## Metrics

- `MDBI` **(primary)** — range: other
  - Mean Distance Between Interventions. Calculated as Total Distance divided by Number of Interventions. Can be split into autonomous (MDBI_A) and manual (MDBI_M) segments.
- `MTBI` **(primary)** — range: other
  - Mean Time Between Interventions. Calculated as Total Uptime divided by Number of Interventions. Can be split into autonomous (MTBI_A) and manual (MTBI_M) segments.

## Input / output format

**Input**: Time-series vehicle telemetry: enable/disable (disengagement) signals with Unix timestamps, vehicle pose (x, y, z), and speed at each timestamp.

**Output**: Scalar metric values (MDBI, MTBI) and normalized intervention occupancy grids (2D arrays with values in [0, 1]) mapped to road coordinates.

## Scoring recipe

```python
def compute_mdbi_mtbi(trajectory):
    auto_dist, auto_time, manual_dist, manual_time = 0.0, 0.0, 0.0, 0.0
    interventions = 0
    for i in range(len(trajectory) - 1):
        curr, nxt = trajectory[i], trajectory[i+1]
        dt = nxt['t'] - curr['t']
        dist = np.linalg.norm([nxt['x']-curr['x'], nxt['y']-curr['y'], nxt['z']-curr['z']])
        if curr['signal'] and not nxt['signal']:
            interventions += 1
            auto_dist += dist
            auto_time += dt
        elif not curr['signal'] and nxt['signal']:
            manual_dist += dist
            manual_time += dt
    mdbi_a = auto_dist / interventions if interventions > 0 else float('inf')
    mtbi_a = auto_time / interventions if interventions > 0 else float('inf')
    mdbi_m = manual_dist / interventions if interventions > 0 else 0.0
    mtbi_m = manual_time / interventions if interventions > 0 else 0.0
    return mdbi_a, mtbi_a, mdbi_m, mtbi_m
```

## Common pitfalls

- Using raw intervention counts alone without normalizing by distance or time, which prevents objective comparison across systems.
- Failing to separate autonomous and manual driving segments, which obscures the system's actual robustness versus safety driver dependence.
- Ignoring road type variations (e.g., dynamic vs. freeway) when aggregating metrics, as environment complexity heavily influences disengagement rates.

## Evidence (verbatim from paper)

> For direct system robustness characterization, the metrics of choice are given by Mean Distance Between Interventions (MDBI) and Mean Time Between Interventions (MTBI). These metrics provide a normalized means of benchmarking system robustness over time by including temporal and spatial information. ... MDBI = Total Distance / Number of Interventions, MTBI = Total Uptime / Number of Interventions.

## Citation

```bibtex
@misc{paz2020autonomous,
  title={Autonomous Vehicle Benchmarking using Unbiased Metrics},
  author={Paz et al. (2020)},
  year={2020},
  note={arXiv:2006.02518}
}
```

- arXiv: 2006.02518
