---
name: agentboard-eval
description: Evaluates an agent's ability to complete multi-round interactive tasks and achieve target goals across diverse task types. It simulates real-world environments where the model must navigate sequential decision-making to reach a defined endpoint. Use when the user wants to benchmark on AgentBoard, or asks about evaluating this task. Reports target achievement rate.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2508.03991
  bibtex_key: bao2025galaxy
  confidence: high
---

# agentboard-eval

> Galaxy: A Cognition-Centered Framework for Proactive, Privacy-Preserving, and Self-Evolving LLM Agents — Bao et al. (2025) (arXiv:2508.03991, 2025)

## What this evaluates

Evaluates an agent's ability to complete multi-round interactive tasks and achieve target goals across diverse task types. It simulates real-world environments where the model must navigate sequential decision-making to reach a defined endpoint.

## Datasets

- **AgentBoard** — total ?; splits: test (-1)

## Metrics

- `target achievement rate` **(primary)** — range: percent
  - Percentage of tasks where the agent successfully completes the entire behavior chain to achieve the target goal.

## Input / output format

**Input**: Multi-round interactive task prompts simulating real-world scenarios.

**Output**: Agent actions and decisions across multiple turns until task completion or termination.

## Scoring recipe

```python
achieved = 0
total = len(tasks)
for task in tasks:
  if task.target_achieved:
    achieved += 1
return (achieved / total) * 100
```

## Common pitfalls

- Evaluating only single-turn success instead of the full behavior chain.
- Not accounting for the multi-round interactive nature of the tasks.

## Evidence (verbatim from paper)

> AgentBoard uses six types of tasks to simulate a multi-round interactive environment, and it uses the target achievement rate across the entire behavior chain as the model evaluation metric.

## Citation

```bibtex
@misc{bao2025galaxy,
  title={Galaxy: A Cognition-Centered Framework for Proactive, Privacy-Preserving, and Self-Evolving LLM Agents},
  author={Bao et al. (2025)},
  year={2025},
  note={arXiv:2508.03991}
}
```

- arXiv: 2508.03991
