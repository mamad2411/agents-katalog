---
name: agentbench-eval
description: Evaluates LLMs as autonomous agents across eight diverse, real-world environments requiring multi-turn interaction, long-term reasoning, decision-making, and strict instruction following. The benchmark measures success rates across code, game, and web-based tasks to identify performance gaps between commercial and open-source models. Use when the user wants to benchmark on AgentBench, or asks about evaluating this task. Reports overall_score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2308.03688
  bibtex_key: liu2023agentbench
  confidence: high
---

# agentbench-eval

> AgentBench: Evaluating LLMs as Agents — Xiao Liu et al. (arXiv:2308.03688, 2023)

## What this evaluates

Evaluates LLMs as autonomous agents across eight diverse, real-world environments requiring multi-turn interaction, long-term reasoning, decision-making, and strict instruction following. The benchmark measures success rates across code, game, and web-based tasks to identify performance gaps between commercial and open-source models.

## Datasets

- **AgentBench** — total 1360; splits: dev (269), test (1091); repo https://github.com/THUDM/AgentBench

## Metrics

- `overall_score` **(primary)** — range: percent
  - A weighted average across 8 tasks. Weights are calculated as the reciprocal of the average success rate of all evaluated models on each task to normalize for difficulty. The final score is the average of each model's task score multiplied by its task's weight.
- `task_success_rate` — range: percent
  - Percentage of individual tasks successfully completed within the allowed interaction turns or time limit.

## Input / output format

**Input**: Multi-turn dialogue history formatted as (u_0, a_0, ..., u_k) where u represents user instructions/environment feedback and a represents agent responses. History is truncated to ≤3500 tokens, with omitted messages noted. For non-chat models, formatted as alternating 'USER:' and 'AGENT:' prompts.

**Output**: Agent's next turn response containing a 'Thought' (Chain-of-Thought) and an 'Action' following the task-specific format. Generated via greedy decoding (temperature=0).

## Scoring recipe

```python
# For each task t in 8 tasks:
avg_score_t = mean(model_scores[t] for all_models)
weight_t = 1.0 / avg_score_t

# For a specific model:
overall_score = sum(model_score[t] * weight_t for t in tasks) / 8
```

## Common pitfalls

- Task Limit Exceeded (TLE) is the dominant failure mode, often due to repeated generation or running out of turns, rather than simple factual errors.
- The overall score uses a non-standard weighting scheme based on the reciprocal of average task scores, not a simple arithmetic mean.
- Strict format and action constraints vary heavily by environment; e.g., DB requires exact output formatting with no retries, while HH/WB require actions from a predefined discrete space.

## Evidence (verbatim from paper)

> Overall Score Calculation. We have observed that the score distribution for each task varies significantly as tasks differ in difficulty levels. As a consequence, a naively averaged score is heavily impacted by tasks that generally yield higher scores (e.g., Web Shopping in our observation), overshadowing those with lower scores and being unsuitable for AGENTBENCH's purpose. Therefore, we produce the overall score by first resizing each task's average score to 1 across all the models we evaluate and then averaging the scores across all tasks for each model (Cf. Table 2). To standardize and simplify score calculations for future studies, we utilize the reciprocal average score of all the tested LLMs in each task as a fixed weight for future overall score calculation. The total score is then computed as the average value obtained by multiplying the score of each task by its corresponding weight.

## Citation

```bibtex
@misc{liu2023agentbench,
  title={AgentBench: Evaluating LLMs as Agents},
  author={Xiao Liu et al.},
  year={2023},
  note={arXiv:2308.03688}
}
```

- arXiv: 2308.03688
