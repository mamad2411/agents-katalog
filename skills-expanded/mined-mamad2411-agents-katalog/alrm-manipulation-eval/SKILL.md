---
name: alrm-manipulation-eval
description: Evaluates an agentic LLM's ability to plan and execute multistep robotic manipulation tasks in simulation. It tests closed-loop reasoning via ReAct-style loops, comparing code-as-policy and tool-as-policy execution modes across linguistically diverse tasks. Use when the user wants to benchmark on ALRM Simulation Benchmark, or asks about evaluating this task. Reports task_completion.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2601.19510
  bibtex_key: gaboardidosantos2026alrm
  confidence: low
---

# alrm-manipulation-eval

> ALRM: Agentic LLM for Robotic Manipulation — Gaboardi dos Santos et al. (2026) (arXiv:2601.19510, 2026)

## What this evaluates

Evaluates an agentic LLM's ability to plan and execute multistep robotic manipulation tasks in simulation. It tests closed-loop reasoning via ReAct-style loops, comparing code-as-policy and tool-as-policy execution modes across linguistically diverse tasks.

## Datasets

- **ALRM Simulation Benchmark** — total 56; splits: test (-1)

## Metrics

- `task_completion` **(primary)** — range: [0, 1]
  - Binary success metric indicating whether the LLM agent successfully fulfills the user's high-level manipulation request within the maximum step limit.

## Input / output format

**Input**: High-level natural language task descriptions or subtask templates (e.g., 'Pick the lemon and place it in the trash').

**Output**: Iterative sequences of thoughts, single-step actions (tool calls or Python code), and environmental observations until task completion or maximum steps.

## Scoring recipe

```python
```python
success = False
for step in range(max_steps):
    action = model.generate_action(observation)
    observation = env.execute(action)
    if env.check_task_completion(observation):
        success = True
        break
return success
```
```

## Common pitfalls

- Simulation-to-real gap: Evaluation is conducted in Gazebo/MoveIt simulation, not on physical hardware.
- Code-as-Policy brittleness: Single syntax or logic errors in generated Python code cause immediate subtask failure.
- Step limit dependency: Performance heavily depends on the arbitrary maximum step count threshold.

## Evidence (verbatim from paper)

> The framework is evaluated on a novel benchmark of 56 linguistically diverse, multistep manipulation tasks across simulation environments, demonstrating superior performance in high-level reasoning and adaptability, with Claude-4.1-Opus and Falcon-H1-7B emerging as top performers in closed-loop and code-based execution respectively.

## Citation

```bibtex
@misc{gaboardidosantos2026alrm,
  title={ALRM: Agentic LLM for Robotic Manipulation},
  author={Gaboardi dos Santos et al. (2026)},
  year={2026},
  note={arXiv:2601.19510}
}
```

- arXiv: 2601.19510
