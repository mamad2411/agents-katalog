---
name: ad2-bench-eval
description: Evaluates multimodal large language models on autonomous driving tasks under adverse weather and complex scenes. It probes base and advanced visual perception, relational understanding, event reasoning, and the coherence of hierarchical chain-of-thought reasoning. Use when the user wants to benchmark on AD^2-Bench, or asks about evaluating this task. Reports Avg-S.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2506.09557
  bibtex_key: wei2025ad2bench
  confidence: high
---

# ad2-bench-eval

> AD^2-Bench: A Hierarchical CoT Benchmark for MLLM in Autonomous Driving under Adverse Conditions — Wei et al. (2025) (arXiv:2506.09557, 2025)

## What this evaluates

Evaluates multimodal large language models on autonomous driving tasks under adverse weather and complex scenes. It probes base and advanced visual perception, relational understanding, event reasoning, and the coherence of hierarchical chain-of-thought reasoning.

## Datasets

- **AD^2-Bench** — total 70000; splits: test (-1)

## Metrics

- `Avg-S` **(primary)** — range: percent
  - Average accuracy across Base Perception, Advanced Perception, Relation Understanding, and Event Reasoning sub-tasks. Calculated as the mean of the four sub-task accuracy scores.

## Input / output format

**Input**: RGB images of adverse weather/complex driving scenes paired with text prompts (multiple-choice questions or hierarchical CoT instructions).

**Output**: Single-letter answers for multiple-choice questions, or structured Chain-of-Thought steps enclosed in specific tags (e.g., '<startN>…<end>').

## Scoring recipe

```python
def compute_avg_s(predictions, golds):
    correct = sum(1 for p, g in zip(predictions, golds) if p.strip() == g.strip())
    return (correct / len(golds)) * 100
```

## Common pitfalls

- Models often output proportional coordinates instead of absolute bounding boxes due to image patching strategies.
- Excessively long CoT outputs are frequently truncated, requiring careful handling for fair evaluation.
- Failure to adhere to strict formatting instructions (e.g., missing structural tags or outputting extraneous text) leads to scoring penalties.

## Evidence (verbatim from paper)

> | Models | LLM | Base Perc. | Adv. Perc. | Relation Und. | Event Res. | Avg-S (*w/* CoT) |

## Citation

```bibtex
@misc{wei2025ad2bench,
  title={AD^2-Bench: A Hierarchical CoT Benchmark for MLLM in Autonomous Driving under Adverse Conditions},
  author={Wei et al. (2025)},
  year={2025},
  note={arXiv:2506.09557}
}
```

- arXiv: 2506.09557
