---
name: adversarial-ood-robustness-eval
description: Evaluates the adversarial and out-of-distribution (OOD) robustness of LLMs across sentiment analysis, natural language inference, and domain-specific classification tasks. It measures how well models maintain performance under adversarial attacks and distribution shifts, and tests the effectiveness of prompt-based enhancement strategies (AHP and ICR). Use when the user wants to benchmark on PromptRobust (SST-2), AdvGlue++, FlipKart, DDXPlus, or asks about evaluating this task. Reports F1.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2412.10535
  bibtex_key: yang2024adversarial
  confidence: medium
---

# adversarial-ood-robustness-eval

> On Adversarial Robustness and Out-of-Distribution Robustness of Large Language Models — April Yang et al. (2024) (arXiv:2412.10535, 2024)

## What this evaluates

Evaluates the adversarial and out-of-distribution (OOD) robustness of LLMs across sentiment analysis, natural language inference, and domain-specific classification tasks. It measures how well models maintain performance under adversarial attacks and distribution shifts, and tests the effectiveness of prompt-based enhancement strategies (AHP and ICR).

## Datasets

- **PromptRobust (SST-2)** — total ?; splits: test (-1)
- **AdvGlue++** — total ?; splits: test (-1)
- **FlipKart** — total ?; splits: test (-1)
- **DDXPlus** — total ?; splits: test (-1)

## Metrics

- `Accuracy (Acc)` — range: [0, 1]
  - Proportion of correctly predicted labels out of total instances.
- `Precision (Prec)` — range: [0, 1]
  - Ratio of true positive predictions to all positive predictions.
- `Recall (Rec)` — range: [0, 1]
  - Ratio of true positive predictions to all actual positive instances.
- `F1` **(primary)** — range: [0, 1]
  - Harmonic mean of precision and recall: 2 * (Prec * Rec) / (Prec + Rec). Values are averaged across attacks, tasks, or datasets as specified per benchmark.

## Input / output format

**Input**: Text inputs containing adversarial perturbations, out-of-distribution samples, or in-context examples for rewriting, formatted as prompts.

**Output**: Model-generated predictions (class labels) or rewritten text outputs.

## Scoring recipe

```python
def compute_metrics(preds, golds):
    tp = sum(p == g == 1 for p, g in zip(preds, golds))
    fp = sum(p == 1 and g == 0 for p, g in zip(preds, golds))
    fn = sum(p == 0 and g == 1 for p, g in zip(preds, golds))
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
    acc = sum(p == g for p, g in zip(preds, golds)) / len(golds)
    return {'Acc': acc, 'Prec': prec, 'Rec': rec, 'F1': f1}
```

## Common pitfalls

- Prompt overloading from enforcing JSON formats can degrade task understanding and lower scores.
- ICR performance heavily depends on the curation and range of in-context examples provided.
- Model size does not linearly correlate with robustness gains; smaller models sometimes outperform larger ones on specific tasks.
- Averaging across diverse tasks (e.g., QNLI, MNLI) can mask task-specific failures and skew overall robustness metrics.

## Evidence (verbatim from paper)

> The results highlight distinct trends in the performance of AHP and ICR across models and benchmarks. For smaller models like LLaMA2:7b, ICR demonstrates superior robustness improvements over the baseline, with notable gains in recall and F1 scores on both PromptRobust and AdvGLUE++.

## Citation

```bibtex
@misc{yang2024adversarial,
  title={On Adversarial Robustness and Out-of-Distribution Robustness of Large Language Models},
  author={April Yang et al. (2024)},
  year={2024},
  note={arXiv:2412.10535}
}
```

- arXiv: 2412.10535
