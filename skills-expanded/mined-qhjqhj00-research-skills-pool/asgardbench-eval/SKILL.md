---
name: asgardbench-eval
description: This benchmark evaluates visually grounded interactive planning by testing an agent's ability to dynamically adapt action sequences based on real-time visual observations. It isolates plan adaptation from navigation and low-level manipulation, measuring how well models track environmental state and revise plans under minimal or absent corrective feedback. Use when the user wants to benchmark on AsgardBench, or asks about evaluating this task. Reports success_rate.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2603.15888
  bibtex_key: tupini2026asgardbench
  confidence: high
---

# asgardbench-eval

> AsgardBench - Evaluating Visually Grounded Interactive Planning Under Minimal Feedback — Tupini et al. (2026) (arXiv:2603.15888, 2026)

## What this evaluates

This benchmark evaluates visually grounded interactive planning by testing an agent's ability to dynamically adapt action sequences based on real-time visual observations. It isolates plan adaptation from navigation and low-level manipulation, measuring how well models track environmental state and revise plans under minimal or absent corrective feedback.

## Datasets

- **AsgardBench** — total 108; splits: test (108); repo https://github.com/microsoft/AsgardBench

## Metrics

- `success_rate` **(primary)** — range: [0, 1]
  - Binary success per task (1 if the task completes successfully within the allowed step limit, 0 otherwise), averaged across all 108 tasks. Success is determined by the environment's termination condition.

## Input / output format

**Input**: Per instance, the model receives a visual observation (image), a task instruction, and a prompt containing the history of previous actions. The prompt varies by experimental condition: Baseline (action history + Success/Failure tags), No Feedback (action history only), or Detailed Feedback (action history + explicit error explanations).

**Output**: A single action string formatted as a verb-object pair (e.g., 'FIND Plate', 'PICKUP Egg', 'CLEAN Mug').

## Scoring recipe

```python
def evaluate_task(model_output, env_state, max_steps):
    history = []
    for t in range(max_steps):
        action = model_output[t]
        obs, success_flag, done = env.step(action)
        history.append((action, success_flag))
        if done:
            return 1.0 if success_flag else 0.0
    return 0.0

# Aggregate across all 108 tasks
success_rate = sum(evaluate_task(task) for task in tasks) / len(tasks)
```

## Common pitfalls

- Models may exploit textual priors or detailed corrective feedback to bypass actual visual grounding, artificially inflating Text-Only performance.
- Visual misinterpretations (e.g., confusing reflections or shadows for task-relevant objects) are common and directly cause state-tracking failures.
- Agents frequently get stuck in repetitive action loops or consecutive failure states, triggering early termination before reaching the step limit.

## Evidence (verbatim from paper)

> Figure 2: Success rates for each model under image based and Text-Only conditions. Visual input substantially improves performance for all but the weakest models, confirming that AsgardBench requires perception-conditioned reasoning. Agents can’t rely on memorized action templates or detailed feedback.

## Citation

```bibtex
@misc{tupini2026asgardbench,
  title={AsgardBench - Evaluating Visually Grounded Interactive Planning Under Minimal Feedback},
  author={Tupini et al. (2026)},
  year={2026},
  note={arXiv:2603.15888}
}
```

- arXiv: 2603.15888
