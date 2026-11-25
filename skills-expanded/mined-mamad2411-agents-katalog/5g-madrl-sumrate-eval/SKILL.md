---
name: 5g-madrl-sumrate-eval
description: Evaluates the ability of a multi-agent deep reinforcement learning framework to optimize the 3D placement and trajectory of mobile access points in dynamic 5G networks, balancing sum-rate maximization against user mobility and interference. Use when the user wants to benchmark on Custom 5G Network Simulation, or asks about evaluating this task. Reports sum-rate.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2303.05233
  bibtex_key: catte2023dualattention
  confidence: high
---

# 5g-madrl-sumrate-eval

> Dual-Attention Deep Reinforcement Learning for Multi-MAP 3D Trajectory Optimization in Dynamic 5G Networks — Catté et al. (2023) (arXiv:2303.05233, 2023)

## What this evaluates

Evaluates the ability of a multi-agent deep reinforcement learning framework to optimize the 3D placement and trajectory of mobile access points in dynamic 5G networks, balancing sum-rate maximization against user mobility and interference.

## Datasets

- **Custom 5G Network Simulation** — total ?; splits: train (-1), test (-1)

## Metrics

- `sum-rate` **(primary)** — range: Mbps
  - Total achievable data rate across all connected users and access points at each time step, aggregated over the simulation horizon. Computed using Nakagami fast-fading channel models with specified path loss and bandwidth parameters.

## Input / output format

**Input**: State vectors for each MAP and UE (position, mobility, traffic demand), processed through dual-attention message encoders and MLPs to form agent observations.

**Output**: 3D position/trajectory updates for each of the M=3 MAPs per time step.

## Scoring recipe

```python
# Evaluate average instantaneous sum-rate over test horizon T
total_rate = 0.0
for t in range(T):
    for ue in UEs:
        sinr = compute_sinr(ue, maps, interference)
        rate = ue.bandwidth * log2(1 + sinr)
        total_rate += rate
return total_rate / T  # Average over time slots
# Results averaged over 50 random deployments
```

## Common pitfalls

- The centralized benchmark's performance heavily depends on the clustering update period τ_c; comparing it without fixing τ_c leads to unfair baselines.
- Testing uses random waypoint mobility at 0.8 m/s, not the static mobility used during training, which tests generalization to unseen dynamics.
- Results are averaged over 50 random deployments, not single runs, to account for stochastic UE placement and fading.

## Evidence (verbatim from paper)

> We perform the training of our proposed MADRL algorithm for 10000 Monte-Carlo runs. For each run, we deploy M=3 MAPs moving with a step size Δℓ=5 m; we also deploy K=25 UEs in M centroids of radius 25 m, randomly sampled in a 200 m by 200 m area. During the training phase, the UEs are static for Te=300 iterations while they follow a random way-point centroid mobility at 0.8m/s during the testing phase. ... Figure 4 shows the instantaneous sum-rate comparison between our solution and the benchmark for static and mobile UEs over time. Results are averaged over 50 random deployments.

## Citation

```bibtex
@misc{catte2023dualattention,
  title={Dual-Attention Deep Reinforcement Learning for Multi-MAP 3D Trajectory Optimization in Dynamic 5G Networks},
  author={Catté et al. (2023)},
  year={2023},
  note={arXiv:2303.05233}
}
```

- arXiv: 2303.05233
