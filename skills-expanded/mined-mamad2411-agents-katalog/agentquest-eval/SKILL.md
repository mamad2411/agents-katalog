---
name: agentquest-eval
description: This evaluation protocol measures LLM agent performance on multi-step reasoning tasks by tracking step-wise progress toward goal completion and the frequency of repetitive actions or states. It enables fine-grained debugging and architectural refinement beyond simple pass/fail success rates. Use when the user wants to benchmark on ALFWorld, Sudoku, or asks about evaluating this task. Reports progress rate.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2404.06411
  bibtex_key: gioacchini2024agentquest
  confidence: medium
---

# agentquest-eval

> AgentQuest: A Modular Benchmark Framework to Measure Progress and Improve LLM Agents — Gioacchini et al. (2024) (arXiv:2404.06411, 2024)

## What this evaluates

This evaluation protocol measures LLM agent performance on multi-step reasoning tasks by tracking step-wise progress toward goal completion and the frequency of repetitive actions or states. It enables fine-grained debugging and architectural refinement beyond simple pass/fail success rates.

## Datasets

- **ALFWorld** — total ?; splits: test (-1)
- **Sudoku** — total ?; splits: test (-1)

## Metrics

- `progress rate` **(primary)** — range: percent
  - Measures the step-wise advancement toward task completion, calculated as the ratio of achieved progress to maximum possible progress at each step t.
- `repetition rate` — range: percent
  - Tracks the frequency of repeated actions or states during execution, calculated as the ratio of repetitive steps to total steps at each step t.

## Input / output format

**Input**: Environment state and task instructions provided to the LLM agent at each step.

**Output**: Agent action or decision per step, executed within the environment until task completion or max steps reached.

## Scoring recipe

```python
def score_agent_trajectory(actions, states, goal, max_steps):
    progress = []
    repetition = []
    for t in range(max_steps):
        progress.append(calculate_progress(states[t], goal))
        repetition.append(count_repeats(actions[:t+1]) / (t + 1))
    return progress, repetition
```

## Common pitfalls

- Averaging metrics over multiple runs (e.g., 15 runs) is required to smooth out stochastic agent behavior.
- Progress and repetition rates are tracked per-step, not just as final scalar values, requiring time-series analysis.
- Extending max steps can artificially inflate progress rate without improving actual success rate.

## Evidence (verbatim from paper)

> Figure 4: Progress rate PR${}_{t}$ and the repetition rate RR${}_{t}$ on ALFWorld and Sudoku averaged over 15 runs. ALFWorld: It starts out with a low repetition rate and quick increase of the progress rate. Then a slow increase of the repetition rate enables to further increase the progress rate although less quickly. Sudoku: The progress rate quickly reaches 8%. The repetition rate then slowly increases without any positive change in the progress rate.

## Citation

```bibtex
@misc{gioacchini2024agentquest,
  title={AgentQuest: A Modular Benchmark Framework to Measure Progress and Improve LLM Agents},
  author={Gioacchini et al. (2024)},
  year={2024},
  note={arXiv:2404.06411}
}
```

- arXiv: 2404.06411
