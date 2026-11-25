---
name: agentvista-eval
description: Evaluates the ability of multimodal agents to perform long-horizon, multi-step tool use in complex, realistic visual environments. It probes cross-image reasoning, constraint tracking, and robust grounding when interacting with dynamic tools like web search and code execution. Use when the user wants to benchmark on AgentVista, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2602.23166
  bibtex_key: su2026agentvista
  confidence: high
---

# agentvista-eval

> AgentVista: Evaluating Multimodal Agents in Ultra-Challenging Realistic Visual Scenarios — Su et al. (2026) (arXiv:2602.23166, 2026)

## What this evaluates

Evaluates the ability of multimodal agents to perform long-horizon, multi-step tool use in complex, realistic visual environments. It probes cross-image reasoning, constraint tracking, and robust grounding when interacting with dynamic tools like web search and code execution.

## Datasets

- **AgentVista** — total ?; splits: test (-1); repo https://github.com/hkust-nlp/AgentVista

## Metrics

- `accuracy` **(primary)** — range: [0, 1]
  - Binary score indicating whether the model's final response exactly matches the annotated ground truth under the required deterministic format, as judged by GPT-4.1.

## Input / output format

**Input**: Natural language task instructions accompanied by single or multiple real-world images, with access to an interactive tool-use environment (web search, image search, navigation, code execution).

**Output**: A final answer/response in a concise, deterministic format specified by the task.

## Scoring recipe

```python
def compute_accuracy(predictions, gold):
    correct = 0
    for pred, g in zip(predictions, gold):
        # GPT-4.1 judge verifies format and content match
        if gpt41_judge(pred, g):
            correct += 1
    return correct / len(predictions)
```

## Common pitfalls

- The tool interaction budget is strictly capped at 30 turns per task; exceeding this terminates the episode without a valid answer.
- Evaluation relies on a fixed GPT-4.1 judge to verify format and content match, which may penalize semantically correct but syntactically divergent responses.
- Multi-image inputs do not necessarily decrease accuracy; they often improve performance by providing complementary visual evidence.

## Evidence (verbatim from paper)

> Since AgentVista provides concise target answers in deterministic formats, evaluation reduces to verifying the final answer. We use GPT-4.1 as a fixed judge model to assess whether a model’s final response matches the annotated ground truth under the required format. We report accuracy as the evaluation metric.

## Citation

```bibtex
@misc{su2026agentvista,
  title={AgentVista: Evaluating Multimodal Agents in Ultra-Challenging Realistic Visual Scenarios},
  author={Su et al. (2026)},
  year={2026},
  note={arXiv:2602.23166}
}
```

- arXiv: 2602.23166
