---
name: agentsynth-eval
description: Evaluates the ability of multimodal language models to execute long-horizon, multi-step computer-use tasks on a desktop environment. It probes visual grounding, precise GUI interaction, state tracking, and error recovery across varying task complexities and software domains. Use when the user wants to benchmark on AgentSynth, or asks about evaluating this task. Reports success rate.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2506.14205
  bibtex_key: xie2025agentsynth
  confidence: high
---

# agentsynth-eval

> AgentSynth: Scalable Task Generation for Generalist Computer-Use Agents — Xie et al. (2025) (arXiv:2506.14205, 2025)

## What this evaluates

Evaluates the ability of multimodal language models to execute long-horizon, multi-step computer-use tasks on a desktop environment. It probes visual grounding, precise GUI interaction, state tracking, and error recovery across varying task complexities and software domains.

## Datasets

- **AgentSynth** — total 6000; splits: test (300); repo https://github.com/sunblaze-ucb/AgentSynth

## Metrics

- `success rate` **(primary)** — range: [0, 1]
  - Fraction of tasks where the automatic verifier agent determines the full trajectory successfully completed the goal. Calculated as (number of successful tasks / total evaluated tasks).

## Input / output format

**Input**: At each interaction step: task description, current desktop screenshot, and previous thoughts/action history.

**Output**: Executable Python code using the pyautogui library to perform the next desktop action.

## Scoring recipe

```python
def compute_success_rate(predictions, gold_tasks):
    successful = 0
    for task in gold_tasks:
        trajectory = predictions[task.id]
        is_success = verifier_agent.analyze(
            task_description=task.prompt,
            trajectory=trajectory
        )
        if is_success:
            successful += 1
    return successful / len(gold_tasks)
```

## Common pitfalls

- Evaluating bare LLMs without agent scaffolding provides a lower-bound estimate, not a fair comparison to optimized agent frameworks.
- The automatic verifier relies on LLM judgment to assess task completion, which may introduce its own hallucination or grounding biases.
- Binary success/failure scoring masks partial progress and specific failure modes like misclicks or state loss.

## Evidence (verbatim from paper)

> Task completion is assessed using the automatic verifier agent introduced in section 3, which analyzes the full trajectory and determines whether the task was successfully completed. The top panel of Figure 4 shows the success rates of four state-of-the-art language models on the AgentSynth benchmark across task difficulty levels 1 through 6.

## Citation

```bibtex
@misc{xie2025agentsynth,
  title={AgentSynth: Scalable Task Generation for Generalist Computer-Use Agents},
  author={Xie et al. (2025)},
  year={2025},
  note={arXiv:2506.14205}
}
```

- arXiv: 2506.14205
