---
name: artist-eval
description: This evaluation probes an LLM's ability to perform complex mathematical reasoning and multi-turn function calling by autonomously deciding when and how to invoke external tools. It measures the model's capacity for outcome-based agentic reasoning, including state tracking, error recovery, and precise final answer generation without step-level supervision. Use when the user wants to benchmark on MATH-500, AIME, AMC, Olympiad Bench, BFCL v3, τ-bench, or asks about evaluating this task. Reports Pass@1 accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2505.01441
  bibtex_key: singh2025artist
  confidence: high
---

# artist-eval

> Agentic Reasoning and Tool Integration for LLMs via Reinforcement Learning — Singh et al. (2025) (arXiv:2505.01441, 2025)

## What this evaluates

This evaluation probes an LLM's ability to perform complex mathematical reasoning and multi-turn function calling by autonomously deciding when and how to invoke external tools. It measures the model's capacity for outcome-based agentic reasoning, including state tracking, error recovery, and precise final answer generation without step-level supervision.

## Datasets

- **MATH-500** — total 500; splits: test (500)
- **AIME** — total ?; splits: test (-1)
- **AMC** — total ?; splits: test (-1)
- **Olympiad Bench** — total ?; splits: test (-1)
- **BFCL v3** — total ?; splits: test (-1)
- **τ-bench** — total 165; splits: test (165)

## Metrics

- `Pass@1 accuracy` **(primary)** — range: [0, 1]
  - The percentage of problems or tasks for which the model's final answer exactly matches the ground truth. For function calling, it additionally requires that the resulting environment state matches the benchmark's ground truth.

## Input / output format

**Input**: Natural language math word problems or user queries requiring multi-turn interaction and tool invocation.

**Output**: A sequence of text-based reasoning steps interleaved with tool queries and tool outputs, culminating in a final answer or final response.

## Scoring recipe

```python
def compute_pass_at_1(predictions, golds, is_function_calling=False):
    correct = 0
    for pred, gold in zip(predictions, golds):
        if is_function_calling:
            if pred['response'] == gold['response'] and pred['env_state'] == gold['env_state']:
                correct += 1
        else:
            if pred['final_answer'] == gold['final_answer']:
                correct += 1
    return correct / len(predictions)
```

## Common pitfalls

- Assuming approximate or semantic matching is sufficient for math problems; the protocol strictly requires exact match of the final answer.
- Evaluating only the syntactic correctness of tool calls without verifying the resulting environment state against the ground truth for function calling tasks.
- Ignoring multi-turn state tracking and error recovery requirements, which are critical for the function calling benchmark.

## Evidence (verbatim from paper)

> We report Pass@1 accuracy: the percentage of problems for which the model’s final answer exactly matches the ground truth. This metric reflects the model’s ability to arrive at a correct solution in a single attempt.

## Citation

```bibtex
@misc{singh2025artist,
  title={Agentic Reasoning and Tool Integration for LLMs via Reinforcement Learning},
  author={Singh et al. (2025)},
  year={2025},
  note={arXiv:2505.01441}
}
```

- arXiv: 2505.01441
