---
name: agenticcache-eval
description: Evaluates the ability of embodied multi-agent systems to execute long-horizon, coordinated tasks efficiently using cache-driven asynchronous planning. It probes how well agents can reuse cached plan transitions to reduce LLM inference latency and token costs while maintaining high task success rates across diverse 3D simulation environments. Use when the user wants to benchmark on TDW-MAT, TDW-COOK, TDW-GAME, BEHAVIOR-1K, or asks about evaluating this task. Reports Success Rate.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2604.24039
  bibtex_key: kim2026agenticcache
  confidence: high
---

# agenticcache-eval

> AgenticCache: Cache-Driven Asynchronous Planning for Embodied AI Agents — Hojoon Kim, Yuheng Wu, Thierry Tambe (2026) (arXiv:2604.24039, 2026)

## What this evaluates

Evaluates the ability of embodied multi-agent systems to execute long-horizon, coordinated tasks efficiently using cache-driven asynchronous planning. It probes how well agents can reuse cached plan transitions to reduce LLM inference latency and token costs while maintaining high task success rates across diverse 3D simulation environments.

## Datasets

- **TDW-MAT** — total 48; splits: train (4), test (44)
- **TDW-COOK** — total 20; splits: train (2), test (18)
- **TDW-GAME** — total 10; splits: train (1), test (9)
- **BEHAVIOR-1K** — total 40; splits: train (4), test (36)

## Metrics

- `Success Rate` **(primary)** — range: percent
  - Percentage of episodes where the multi-agent team successfully completes the assigned task.
- `Latency` — range: hours
  - Total wall-clock execution time measured in hours.
- `Token Usage` — range: tokens
  - Cumulative input and output tokens consumed across all LLM/VLM calls per episode.
- `Cost` — range: USD
  - Total monetary expense in USD, calculated by multiplying token counts by per-token prices.

## Input / output format

**Input**: Multi-agent state observations (visual/textual), task instructions, and coordination prompts.

**Output**: Sequential action plans or next-step commands for each agent in the team.

## Scoring recipe

```python
def compute_metrics(predictions, gold, episodes):
    success = sum(1 for ep in episodes if check_completion(ep, predictions[ep]))
    sr = (success / len(episodes)) * 100
    total_tokens = sum(count_tokens(predictions[ep]) for ep in episodes)
    avg_tokens = total_tokens / len(episodes)
    avg_latency = sum(ep.wall_time for ep in episodes) / len(episodes)
    avg_cost = sum(ep.tokens * per_token_price for ep in episodes) / len(episodes)
    return {'Success Rate': sr, 'Latency': avg_latency, 'Token Usage': avg_tokens, 'Cost': avg_cost}
```

## Common pitfalls

- Confusing warm-start (cache prefilling) vs cold-start evaluation conditions, which drastically alter latency and success rates.
- Overlooking VLM vs LLM fallback latency differences, which heavily skew total execution time in TDW tasks.
- Assuming cost scales linearly with tokens without accounting for asynchronous cache hits that bypass LLM calls entirely.

## Evidence (verbatim from paper)

> As shown in Table 2, AgenticCache consistently achieves high task success rates. With GPT-5 and GPT-5-mini it reaches 84–100% across environments, and with GPT-5-nano it reaches 68–100%. Baselines struggle in multi-agent settings.

## Citation

```bibtex
@misc{kim2026agenticcache,
  title={AgenticCache: Cache-Driven Asynchronous Planning for Embodied AI Agents},
  author={Hojoon Kim, Yuheng Wu, Thierry Tambe (2026)},
  year={2026},
  note={arXiv:2604.24039}
}
```

- arXiv: 2604.24039
