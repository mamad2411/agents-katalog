---
name: androidworld-eval
description: This benchmark evaluates the ability of autonomous multimodal agents to navigate and interact with real-world Android applications to complete programmatic user instructions. It probes UI understanding, precise touch interaction, state tracking, and error recovery in a dynamic mobile environment. Use when the user wants to benchmark on AndroidWorld, or asks about evaluating this task. Reports Success Rate (SR).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2405.14573
  bibtex_key: rawles2024androidworld
  confidence: high
---

# androidworld-eval

> AndroidWorld: A Dynamic Benchmarking Environment for Autonomous Agents — Rawles et al. (2024) (arXiv:2405.14573, 2024)

## What this evaluates

This benchmark evaluates the ability of autonomous multimodal agents to navigate and interact with real-world Android applications to complete programmatic user instructions. It probes UI understanding, precise touch interaction, state tracking, and error recovery in a dynamic mobile environment.

## Datasets

- **AndroidWorld** — total 116; splits: test (116); repo https://github.com/google-research/android_world

## Metrics

- `Success Rate (SR)` **(primary)** — range: percent
  - The percentage of tasks successfully completed by the agent within the predefined maximum step limit. Calculated as (number of successful tasks / total tasks) * 100.

## Input / output format

**Input**: User instruction, current device screenshot, Set-of-Mark (SoM) annotated screenshot with labeled UI element bounding boxes, and/or accessibility tree (a11y) leaf nodes. Agents also receive available action types and operating guidelines.

**Output**: JSON object specifying the selected action and reasoning. For reflective variants, a concise step summary including intended action, success/failure status, failure reasons, and recommendations.

## Scoring recipe

```python
def compute_sr(tasks, max_steps):
    successes = 0
    for task in tasks:
        # Environment validates goal via Android OS state management
        if task.goal_state_reached() and task.steps_executed <= max_steps:
            successes += 1
    return (successes / len(tasks)) * 100
```

## Common pitfalls

- Tasks may terminate due to hitting the maximum step limit rather than actual logical failure, which can artificially lower success rates.
- Performance heavily depends on input modality; SoM annotations improve web-like benchmarks but can degrade performance on native Android apps due to accessibility tree completeness differences.
- Memory-intensive tasks (e.g., cross-app transcriptions, calculations) are disproportionately difficult for agents, skewing overall scores if not analyzed separately.

## Evidence (verbatim from paper)

> We evaluate M3A, M3A-Simple, and SeeAct on AndroidWorld and MobileMiniWoB++. We set the seed to 30 and the temperature to 0 to aid reproducibility. Each task has a maximum allowed number of steps (detailed in Appendix[F]), typically set to twice the number of steps needed by human annotators to complete the task. Table[3] presents the success rates (SR) for the agents and human performance on both task suites.

## Citation

```bibtex
@misc{rawles2024androidworld,
  title={AndroidWorld: A Dynamic Benchmarking Environment for Autonomous Agents},
  author={Rawles et al. (2024)},
  year={2024},
  note={arXiv:2405.14573}
}
```

- arXiv: 2405.14573
