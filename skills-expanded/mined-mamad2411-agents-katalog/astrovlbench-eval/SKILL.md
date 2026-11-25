---
name: astrovlbench-eval
description: This benchmark evaluates the ability of vision-language models to perform multi-modal astronomical reasoning across five distinct observational modalities, including optical imaging, radio interferometry, photometry, light curves, and spectroscopy. It probes whether models can correctly classify celestial objects and interpret physical features, while also testing the impact of prompt guidance and input representation (visual vs. numerical) on classification accuracy and reasoning quality. Use when the user wants to benchmark on AstroVLBench, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2604.24589
  bibtex_key: ren2026astrovlbench
  confidence: high
---

# astrovlbench-eval

> A systematic evaluation of vision-language models for observational astronomical reasoning tasks — Ren et al. (2026) (arXiv:2604.24589, 2026)

## What this evaluates

This benchmark evaluates the ability of vision-language models to perform multi-modal astronomical reasoning across five distinct observational modalities, including optical imaging, radio interferometry, photometry, light curves, and spectroscopy. It probes whether models can correctly classify celestial objects and interpret physical features, while also testing the impact of prompt guidance and input representation (visual vs. numerical) on classification accuracy and reasoning quality.

## Datasets

- **AstroVLBench** — total 4100; splits: task1_agngalaxy (557), task2_radio (833), task3_sed (168), task4_lightcurve (142), task5_spectral_q1 (700), task5_spectral_q2 (500), task5_spectral_q3 (400)

## Metrics

- `accuracy` **(primary)** — range: [0, 1]
  - The proportion of correctly classified instances out of the total number of instances in a task. Reported with 95% bootstrap confidence intervals calculated over 10,000 iterations.

## Input / output format

**Input**: Astronomical observational data (optical/radio images, SED plots, light curves, or spectral plots) or structured numerical tables, accompanied by a text prompt (unguided, phenomenological, or physical) specifying the classification task.

**Output**: A discrete class label corresponding to the ground truth categories for the specific task (e.g., AGN/Galaxy, FRI/FRII, Type-1/Type-2/Galaxy, five light-curve classes, or BPT diagnostic categories), optionally accompanied by a textual justification.

## Scoring recipe

```python
def compute_accuracy(predictions, gold_labels):
    correct = sum(1 for p, g in zip(predictions, gold_labels) if p == g)
    return correct / len(gold_labels)

# Bootstrap CI calculation (10,000 iterations)
import numpy as np
def bootstrap_ci(predictions, gold_labels, n_iters=10000):
    accs = [compute_accuracy(np.random.choice(predictions, len(predictions)), gold_labels) for _ in range(n_iters)]
    return np.percentile(accs, [2.5, 97.5])
```

## Common pitfalls

- Models frequently exhibit mode collapse, defaulting to predicting the majority class (e.g., classifying all sources as galaxies or star-forming spectra) rather than learning fine-grained distinctions.
- Accuracy scores can be misleading when class distributions are imbalanced; high overall accuracy may mask near-zero recall for minority classes like broad-line AGN or specific transient types.
- Visual plots may obscure precise numerical values, leading models to rely on coarse morphological cues rather than quantitative features, which significantly impacts performance on tasks requiring ratio-based diagnostics.

## Evidence (verbatim from paper)

> Gemini 3 Pro achieves the highest accuracy at 74.5% (95% CI [0.709, 0.781]), followed by GPT-5.2 at 65.2% (95% CI [0.612, 0.691]) and Grok-4 at 63.6% (95% CI [0.596, 0.675]).

## Citation

```bibtex
@misc{ren2026astrovlbench,
  title={A systematic evaluation of vision-language models for observational astronomical reasoning tasks},
  author={Ren et al. (2026)},
  year={2026},
  note={arXiv:2604.24589}
}
```

- arXiv: 2604.24589
