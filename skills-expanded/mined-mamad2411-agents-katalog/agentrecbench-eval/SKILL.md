---
name: agentrecbench-eval
description: This benchmark evaluates LLM-based agentic recommender systems across three scenarios: classic, evolving-interest, and cold-start recommendation. It probes the agents' ability to dynamically plan, utilize textual interaction environments, and adapt to user preference shifts or data sparsity using structured user/item profiles and reviews. Use when the user wants to benchmark on Amazon, GoodReads, Yelp, or asks about evaluating this task. Reports Hit Rate@$N.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2505.19623
  bibtex_key: shang2025agentrecbench
  confidence: high
---

# agentrecbench-eval

> AgentRecBench: Benchmarking LLM Agent-based Personalized Recommender Systems — Shang et al. (2025) (arXiv:2505.19623, 2025)

## What this evaluates

This benchmark evaluates LLM-based agentic recommender systems across three scenarios: classic, evolving-interest, and cold-start recommendation. It probes the agents' ability to dynamically plan, utilize textual interaction environments, and adapt to user preference shifts or data sparsity using structured user/item profiles and reviews.

## Datasets

- **Amazon** — total ?; splits: test (-1)
- **GoodReads** — total ?; splits: test (-1)
- **Yelp** — total ?; splits: test (-1)

## Metrics

- `Hit Rate@$N` **(primary)** — range: [0, 1]
  - Measures the probability that the ground-truth positive item appears in the top-N ranked positions. Formally: HR@N = (1/|T|) * sum_{t in T} I(p_t in R_t^N), where T is the test set, p_t is the ground-truth item, and R_t^N is the top-N recommendations.

## Input / output format

**Input**: Structured user profile (ID, review count, social connections, avg rating), item profile (ID, name, type, metadata, avg rating, review count), review history, and a candidate set of 20 items (1 ground-truth positive + 19 unobserved negatives).

**Output**: A ranked list of items from the candidate set, typically returning the top-N recommendations.

## Scoring recipe

```python
def hit_rate_at_n(predictions, ground_truth, n):
    top_n = predictions[:n]
    return 1.0 if ground_truth in top_n else 0.0

# Aggregate over test set T:
# HR@N = mean(hit_rate_at_n(preds_t, gold_t, n) for t in T)
# Evaluated at N in {1, 3, 5}
```

## Common pitfalls

- Negative sampling is fixed to exactly 19 unobserved items per test instance, which may artificially inflate or deflate ranking difficulty compared to real-world candidate pools.
- Cold-start thresholds (m for users, n for items) are dataset-dependent and not explicitly standardized in the text, making cross-dataset comparison of cold-start performance difficult.
- The evaluation focuses solely on ranking accuracy (HR@N) and does not assess conversational coherence, tool-use latency, or multi-turn interaction quality.

## Evidence (verbatim from paper)

> We evaluate recommendation performance using ranking-based metrics with emphasis on Top-$N$ accuracy. Following standard evaluation protocols*[[5], [7]]*, each test instance consists of 20 candidate items: one ground-truth positive item sampled from the user’s interaction history and 19 negative items sampled from unobserved interactions. The primary metric is *Hit Rate@$N$* (HR@$N$), measuring the probability that the ground-truth item appears in the top-$N$ ranked positions ($N\in{1,3,5}$). Formally: $\text{HR@}N\=\frac{1}{|\mathcal{T}|}\sum_{t\in\mathcal{T}}\mathbb{I}(p_{t}\in\mathcal{R}_{t}^{N})$

## Citation

```bibtex
@misc{shang2025agentrecbench,
  title={AgentRecBench: Benchmarking LLM Agent-based Personalized Recommender Systems},
  author={Shang et al. (2025)},
  year={2025},
  note={arXiv:2505.19623}
}
```

- arXiv: 2505.19623
