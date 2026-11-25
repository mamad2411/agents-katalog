---
name: aigibench-eval
description: Evaluates the generalization, robustness to image degradation, and sensitivity to data augmentation and pre-processing of AI-generated image (AIGI) detectors across 25 diverse test datasets spanning GANs, diffusion models, and face-swap/manipulation methods. Use when the user wants to benchmark on AIGIBench, or asks about evaluating this task. Reports F.Acc..
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2505.12335
  bibtex_key: li2025aigibench
  confidence: high
---

# aigibench-eval

> Is Artificial Intelligence Generated Image Detection a Solved Problem? — Li et al. (2025) (arXiv:2505.12335, 2025)

## What this evaluates

Evaluates the generalization, robustness to image degradation, and sensitivity to data augmentation and pre-processing of AI-generated image (AIGI) detectors across 25 diverse test datasets spanning GANs, diffusion models, and face-swap/manipulation methods.

## Datasets

- **AIGIBench** — total ?; splits: test (-1); repo https://github.com/HorizonTEL/AIGIBench

## Metrics

- `F.Acc.` **(primary)** — range: percent
  - Fake Accuracy: proportion of AI-generated images correctly classified as fake. Calculated as TP_fake / (TP_fake + FN_fake).
- `R.Acc.` — range: percent
  - Real Accuracy: proportion of real images correctly classified as real. Calculated as TP_real / (TP_real + FN_real).
- `Acc.` — range: percent
  - Overall Accuracy: proportion of all images correctly classified. Calculated as (TP_real + TP_fake) / Total.
- `A.P.` — range: [0, 1]
  - Average Precision: area under the precision-recall curve computed over varying confidence thresholds.

## Input / output format

**Input**: RGB images (real or AI-generated) of varying resolutions, optionally subjected to degradation (JPEG compression, Gaussian noise, up-down sampling), data augmentation (rotation, jitter, masking), or pre-processing (resize, crop).

**Output**: Binary prediction (Real/Fake) or confidence scores used for thresholding and Average Precision calculation.

## Scoring recipe

```python
def compute_metrics(preds, gold, scores):
    r_acc = sum(p == g for p, g in zip(preds_real, gold_real)) / len(gold_real)
    f_acc = sum(p == g for p, g in zip(preds_fake, gold_fake)) / len(gold_fake)
    acc = sum(p == g for p, g in zip(preds, gold)) / len(gold)
    ap = average_precision_score(gold, scores)
    return {'R.Acc.': r_acc, 'F.Acc.': f_acc, 'Acc.': acc, 'A.P.': ap}
```

## Common pitfalls

- High R.Acc. (real accuracy) often masks near-zero F.Acc. (fake accuracy), creating a false impression of detector robustness under degradation.
- Performance varies drastically between training settings (Setting-I vs Setting-II); adding SD-v1.4 to training boosts R.Acc. but frequently reduces F.Acc.
- Test-time pre-processing like cropping improves R.Acc. but frequently degrades F.Acc., indicating a critical trade-off for practical deployment.

## Evidence (verbatim from paper)

> Specifically: i) JPEG Compression and Gaussian Noise cause a dramatic decline in F.Acc. for all detectors, often approaching 0%, while R.Acc. remains artificially high (close to 100%). This indicates a strong bias toward predicting "real" under these perturbations, resulting in a failure to detect fake images.

## Citation

```bibtex
@misc{li2025aigibench,
  title={Is Artificial Intelligence Generated Image Detection a Solved Problem?},
  author={Li et al. (2025)},
  year={2025},
  note={arXiv:2505.12335}
}
```

- arXiv: 2505.12335
