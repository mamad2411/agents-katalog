---
name: abc-eval
description: This benchmark evaluates large language models' ability to understand symbolic music and follow instructions using text-based ABC notation. It probes capabilities ranging from basic syntax parsing and error detection to segment-level reasoning and sequence-level musical analysis like genre or emotion recognition. Use when the user wants to benchmark on ABC-Eval, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2509.23350
  bibtex_key: zhao2025abceval
  confidence: high
---

# abc-eval

> ABC-Eval: Benchmarking Large Language Models on Symbolic Music Understanding and Instruction Following — Zhao et al. (2025) (arXiv:2509.23350, 2025)

## What this evaluates

This benchmark evaluates large language models' ability to understand symbolic music and follow instructions using text-based ABC notation. It probes capabilities ranging from basic syntax parsing and error detection to segment-level reasoning and sequence-level musical analysis like genre or emotion recognition.

## Datasets

- **ABC-Eval** — total 1086; splits: test (1086)

## Metrics

- `accuracy` **(primary)** — range: [0, 1]
  - The proportion of correctly predicted answers out of the total number of test instances. Calculated as the number of exact matches between the model's output and the ground truth divided by the total number of samples.

## Input / output format

**Input**: ABC score, task instruction, options or templates defining the output format, and simple natural language instructions.

**Output**: Model must produce a response matching the provided options or output template.

## Scoring recipe

```python
def compute_accuracy(predictions, gold_labels):
    correct = sum(1 for p, g in zip(predictions, gold_labels) if p.strip() == g.strip())
    return correct / len(gold_labels)
```

## Common pitfalls

- High sensitivity to prompt variations: Even simple tasks show large performance drops (e.g., 30% accuracy) when prompts change slightly, indicating poor robustness.
- Task difficulty gradient: Models perform well on basic syntax but fail on segment-level and sequence-level reasoning, so evaluating only surface-level tasks may overestimate capabilities.

## Evidence (verbatim from paper)

> Most foundation models exceeded 90% accuracy on basic syntax understanding tasks, indicating their potential in symbolic music tasks. However, certain failure patterns (e.g., 30% accuracy achieved by DeepSeek-chat model) reveal that performances on even the simplest tasks are highly sensitive to prompt variations, indicating a significant lack of robustness.

## Citation

```bibtex
@misc{zhao2025abceval,
  title={ABC-Eval: Benchmarking Large Language Models on Symbolic Music Understanding and Instruction Following},
  author={Zhao et al. (2025)},
  year={2025},
  note={arXiv:2509.23350}
}
```

- arXiv: 2509.23350
