---
name: adcraft-eval
description: Evaluates reinforcement learning agents' ability to optimize bidding strategies and budget allocation in a non-stationary, stochastic Search Engine Marketing (SEM) simulation. It probes how well policies handle sparse feedback, shifting reward landscapes, and long-term profitability constraints over a simulated campaign. Use when the user wants to benchmark on AdCraft Environment, or asks about evaluating this task. Reports NCP.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2306.11971
  bibtex_key: gomrokchi2023adcraft
  confidence: high
---

# adcraft-eval

> AdCraft: An Advanced Reinforcement Learning Benchmark Environment for Search Engine Marketing Optimization — Gomrokchi et al. (2023) (arXiv:2306.11971, 2023)

## What this evaluates

Evaluates reinforcement learning agents' ability to optimize bidding strategies and budget allocation in a non-stationary, stochastic Search Engine Marketing (SEM) simulation. It probes how well policies handle sparse feedback, shifting reward landscapes, and long-term profitability constraints over a simulated campaign.

## Datasets

- **AdCraft Environment** — total ?; splits: (unstated); repo https://github.com/Mikata-Project/adcraft

## Metrics

- `NCP` **(primary)** — range: other
  - Ratio of the agent's cumulative net profit to the expected profit of optimal bidding over a 60-time-step campaign window. NCP = agent_profit / optimal_profit.
- `AKNCP` — range: other
  - Average of the NCP scores computed independently for each keyword in the campaign. AKNCP = mean(NCP_per_keyword).

## Input / output format

**Input**: Current environment state including keyword-level bids, auction outcomes, remaining budget, and estimated ad values/conversion rates.

**Output**: Continuous bid values for each keyword in the campaign.

## Scoring recipe

```python
def compute_metrics(trajectory, optimal_profit_per_kw):
    agent_profit = sum(trajectory.rewards)
    ncp = agent_profit / optimal_profit_per_kw
    kw_ncps = [kw_reward / kw_optimal for kw_reward, kw_optimal in zip(trajectory.kw_rewards, optimal_profit_per_kw)]
    akncp = sum(kw_ncps) / len(kw_ncps)
    return ncp, akncp
```

## Common pitfalls

- Assuming the Vickrey-style baseline is optimal; the paper notes its assumptions (bids don't change ad value, value is known) are violated in practice.
- Treating NCP > 1 as an error; the authors explicitly state that 'lucky' bidding can push normalized scores above 1.
- Comparing raw cumulative profit across campaigns without normalization, as profitability varies wildly between different ad setups.

## Evidence (verbatim from paper)

> In practice many different performance indicators are used in SEM bidding, such as total clicks, return on ad spend, net profit, and more. We focus our investigations on cumulative net profit of bidding over a $60$ time step window representing a two month advertisement campaign. However, different ad campaigns might vary wildly in terms of profitability causing difficulty comparing campaign performance using only profit. To that end, the key metrics we focus on normalize profits by taking the ratio of an agents profit with the expected profit of optimal bidding. This normalized cumulative profit (NCP) can be determined either wholistically looking at the total profit of a campaign, or on a per-keyword basis, where we average per keywords the NCP achieved on each. Average per-Keyword NCP (AKNCP) will be the second metric we examine in our experiments.

## Citation

```bibtex
@misc{gomrokchi2023adcraft,
  title={AdCraft: An Advanced Reinforcement Learning Benchmark Environment for Search Engine Marketing Optimization},
  author={Gomrokchi et al. (2023)},
  year={2023},
  note={arXiv:2306.11971}
}
```

- arXiv: 2306.11971
