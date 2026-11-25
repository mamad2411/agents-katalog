---
name: agentprmeval
description: Evaluates LLM agents' ability to navigate simulated environments and execute multi-step plans to complete natural language instructions. It probes step-wise decision-making, goal proximity tracking, and sequential task execution across web shopping, grid-world navigation, and text-based crafting scenarios. Use when the user wants to benchmark on WebShop, BabyAI, TextCraft, or asks about evaluating this task. Reports success rate.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2511.08325
  bibtex_key: xi2025agentprm
  confidence: high
---

# agentprmeval

> AgentPRM: Process Reward Models for LLM Agents via Step-Wise Promise and Progress — Xi et al. (2025) (arXiv:2511.08325, 2025)

## What this evaluates

Evaluates LLM agents' ability to navigate simulated environments and execute multi-step plans to complete natural language instructions. It probes step-wise decision-making, goal proximity tracking, and sequential task execution across web shopping, grid-world navigation, and text-based crafting scenarios.

## Datasets

- **WebShop** — total ?; splits: test (100); repo https://github.com/princeton-nlp/WebShop
- **BabyAI** — total ?; splits: test (90); repo https://github.com/mila-iqia/babyai
- **TextCraft** — total ?; splits: test (97); repo https://github.com/archiki/ADaPT

## Metrics

- `success rate` **(primary)** — range: [0, 1]
  - Proportion of test queries where the agent successfully completes the instructed task within the maximum interaction rounds.
- `reward` — range: other
  - Environment-specific scalar reward signal for BabyAI, reflecting task completion and step efficiency.

## Input / output format

**Input**: Natural language instruction/query describing the task goal. The model receives this in a ReAct format context where it must generate a reasoning process followed by an action.

**Output**: Sequential ReAct traces (Thought + Action) up to a maximum number of interaction rounds (6 for WebShop, 20 for BabyAI and TextCraft), ending with a final action or completion signal.

## Scoring recipe

```python
def compute_metric(predictions, gold, task_name):
    if task_name in ['WebShop', 'TextCraft']:
        return sum(1 for p in predictions if p['completed']) / len(predictions)
    elif task_name == 'BabyAI':
        return sum(p['env_reward'] for p in predictions) / len(predictions)
    return 0.0
```

## Common pitfalls

- Evaluating with greedy decoding (temperature 0.0) instead of Best-of-N or beam search, which significantly underestimates reward model utility and test-time scaling performance.
- Ignoring the strict maximum interaction round limits (6 for WebShop, 20 for BabyAI/TextCraft), leading to premature termination or unfair task failure penalties.
- Using training trajectories for evaluation instead of the specified test splits (100/90/97 queries), which inflates success metrics due to data leakage.

## Evidence (verbatim from paper)

> We report the success rate for WebShop and TextCraft, and the reward for BabyAI. Following AgentGym, we include 100, 90, 97 queries for evaluation on WebShop, BabyAI, TextCraft, respectively.

## Citation

```bibtex
@misc{xi2025agentprm,
  title={AgentPRM: Process Reward Models for LLM Agents via Step-Wise Promise and Progress},
  author={Xi et al. (2025)},
  year={2025},
  note={arXiv:2511.08325}
}
```

- arXiv: 2511.08325
