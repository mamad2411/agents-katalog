---
name: aeria-edge-ai-eval
description: Evaluates an auction-based dynamic pricing and resource allocation mechanism for on-demand DNN inference at the edge. It probes the system's ability to jointly optimize model partitioning, pricing, and resource distribution under varying user requirements and real-world trace-driven conditions. Use when the user wants to benchmark on Multi30K, ImageNet-1K, CIFAR-100, CIFAR-10, Shanghai Telecom, or asks about evaluating this task. Reports revenue.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2503.04521
  bibtex_key: li2025aeria
  confidence: medium
---

# aeria-edge-ai-eval

> Dynamic Pricing for On-Demand DNN Inference in the Edge-AI Market — Li et al. (2025) (arXiv:2503.04521, 2025)

## What this evaluates

Evaluates an auction-based dynamic pricing and resource allocation mechanism for on-demand DNN inference at the edge. It probes the system's ability to jointly optimize model partitioning, pricing, and resource distribution under varying user requirements and real-world trace-driven conditions.

## Datasets

- **Multi30K** — total 30016; splits: test (-1)
- **ImageNet-1K** — total ?; splits: test (-1)
- **CIFAR-100** — total ?; splits: test (-1)
- **CIFAR-10** — total ?; splits: test (-1)
- **Shanghai Telecom** — total 800; splits: test (-1)

## Metrics

- `revenue` **(primary)** — range: other
  - Total earnings of the edge AI service provider from allocating inference resources to bidding users, optimized via the auction mechanism.
- `inference performance` — range: other
  - Composite metric evaluating inference latency and accuracy across multi-exit DNN branches under varying user requirements.

## Input / output format

**Input**: User bids R_i = {beta_i, t_i, sigma_i, w_i} (price, latency requirement, accuracy requirement, DNN model), device computation capacity, geographical coordinates, real-time wireless data rate, edge server capacity, and electricity price.

**Output**: Resource allocation decisions, dynamic pricing per time slot, and DNN model partitioning/exit selection for each user.

## Scoring recipe

```python
# Trace-driven simulation setup
users = load_shanghai_telecom_trace(n=800)
power_prices = load_ontario_power_trace(days=15)
bandwidth = load_ghent_4g_trace(slots=360)

revenues = []
for run in range(120):
    # Run mechanism and baselines (IAO, Edgent, AMR^2, Fixed Profit Rate)
    allocation = run_aeria(users, power_prices, bandwidth)
    rev = sum(user_bid_price for user in allocation if user.wins)
    revenues.append(rev)

avg_revenue = sum(revenues) / len(revenues)
# Compare avg_revenue against baseline averages
```

## Common pitfalls

- Relies on synthetic early-exit branches that equally apportion computation overhead, which may not reflect real ME-DNN training dynamics.
- Uses historical trace datasets (Shanghai Telecom, Ontario power, Ghent bandwidth) for simulation rather than live edge deployments, limiting real-world generalizability.
- Averages results over 120 runs but does not report statistical variance or confidence intervals in the provided section.

## Evidence (verbatim from paper)

> Differing from AERIA for revenue maximization, it takes a rigid earning target for the AI service providers with the fixed profit-rate objective of 1.0. All the trace-driven experimental results about the AERIA, IAO, Edgent, and Fixed Profit Rate = 1.0 are averaged over 120 runs.

## Citation

```bibtex
@misc{li2025aeria,
  title={Dynamic Pricing for On-Demand DNN Inference in the Edge-AI Market},
  author={Li et al. (2025)},
  year={2025},
  note={arXiv:2503.04521}
}
```

- arXiv: 2503.04521
