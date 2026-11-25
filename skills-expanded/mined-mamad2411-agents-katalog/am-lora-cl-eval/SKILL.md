---
name: am-lora-cl-eval
description: Evaluates a model's ability to continuously learn multiple text classification tasks without catastrophic forgetting, measuring how well it retains knowledge of previous tasks while adapting to new ones. Use when the user wants to benchmark on Standard CL benchmarks, Large number of tasks benchmark, or asks about evaluating this task. Reports average results.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2409.19611
  bibtex_key: liu2024am-lora
  confidence: high
---

# am-lora-cl-eval

> Learning Attentional Mixture of LoRAs for Language Model Continual Learning — Jialin Liu et al. (2024) (arXiv:2409.19611, 2024)

## What this evaluates

Evaluates a model's ability to continuously learn multiple text classification tasks without catastrophic forgetting, measuring how well it retains knowledge of previous tasks while adapting to new ones.

## Datasets

- **Standard CL benchmarks** — total ?; splits: train (1000), val (-1)
- **Large number of tasks benchmark** — total ?; splits: train (1000), val (-1)

## Metrics

- `average results` **(primary)** — range: percent
  - Percentage of correctly predicted class labels over the total number of validation instances, averaged across all tasks in the continual learning sequence.

## Input / output format

**Input**: Text input for classification tasks, formatted as prompts for T5-Large or LLaMA2-7B models.

**Output**: Predicted class label or generated text corresponding to the correct category.

## Scoring recipe

```python
def compute_average_results(predictions, golds):
    correct = sum(1 for p, g in zip(predictions, golds) if p == g)
    return (correct / len(golds)) * 100
```

## Common pitfalls

- The paper uses a fixed 1000-sample training split per task, which is much smaller than standard full splits, potentially inflating continual learning baselines.
- Task order significantly impacts results (Order1 vs Order2 vs Order3), so averaging across orders is necessary for fair comparison.
- Validation sets are fixed at 500 samples per category, but test set sizes are not reported, making direct comparison with full benchmarks difficult.

## Evidence (verbatim from paper)

> our method significantly outperforms all continual learning baseline methods in order1, order2 and average results, and is competitive with SOTA in order3.

## Citation

```bibtex
@misc{liu2024am-lora,
  title={Learning Attentional Mixture of LoRAs for Language Model Continual Learning},
  author={Jialin Liu et al. (2024)},
  year={2024},
  note={arXiv:2409.19611}
}
```

- arXiv: 2409.19611
