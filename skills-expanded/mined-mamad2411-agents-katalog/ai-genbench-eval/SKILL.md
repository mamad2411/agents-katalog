---
name: ai-genbench-eval
description: Evaluates the ability of AI-generated image detectors to generalize to novel, temporally subsequent generative models under realistic post-processing conditions. It measures how well detectors maintain performance when incrementally trained on historically ordered synthetic data and tested on unseen future generators. Use when the user wants to benchmark on AI-GenBench, or asks about evaluating this task. Reports AUROC, Accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2504.20865
  bibtex_key: pellegrini2025aigenbench
  confidence: high
---

# ai-genbench-eval

> AI-GenBench: A New Ongoing Benchmark for AI-Generated Image Detection — Pellegrini et al. (2025) (arXiv:2504.20865, 2025)

## What this evaluates

Evaluates the ability of AI-generated image detectors to generalize to novel, temporally subsequent generative models under realistic post-processing conditions. It measures how well detectors maintain performance when incrementally trained on historically ordered synthetic data and tested on unseen future generators.

## Datasets

- **AI-GenBench** — total 360000; splits: train (288000), test (72000); repo https://github.com/MI-BioLab/AI-GenBench

## Metrics

- `AUROC` **(primary)** — range: [0, 1]
  - Area Under the Receiver Operating Characteristic curve, computed per chronological sliding window step and averaged across all steps in the Next Period scenario. Measures the probability that a randomly chosen synthetic image is ranked higher than a randomly chosen real image.
- `Accuracy` **(primary)** — range: [0, 1]
  - Fraction of correctly classified images (real vs. synthetic), computed per chronological sliding window step and averaged across all steps in the Next Period scenario.

## Input / output format

**Input**: Single RGB image file (JPEG/PNG) with a binary ground-truth label indicating whether it is real or AI-generated.

**Output**: Binary classification prediction (real/synthetic) or a continuous confidence score for each image.

## Scoring recipe

```python
def compute_metrics(predictions, labels, window_indices):
    # predictions, labels: arrays of shape (N,)
    # window_indices: maps each image to its sliding window step k (0..8)
    step_accs = []
    step_aurocs = []
    for k in range(9):
        mask = window_indices == k + 1  # Next Period: w_{k+1}
        if mask.sum() == 0: continue
        y_true = labels[mask]
        y_pred = predictions[mask]
        step_accs.append(accuracy_score(y_true, y_pred))
        step_aurocs.append(roc_auc_score(y_true, y_pred))
    return mean(step_accs), mean(step_aurocs)
```

## Common pitfalls

- Using non-deterministic or custom augmentation during evaluation, which violates the fixed DetermAugment protocol (multiplier=1).
- Training on generators from future sliding windows, breaking the chronological generalization constraint.
- Using additional datasets or pre-training on synthetic/real detection tasks, which is explicitly forbidden.
- Reporting metrics on Past or Whole Period instead of the primary Next Period scenario.

## Evidence (verbatim from paper)

> As compact ranking indicators for the leaderboard, we propose using the average Area Under Receiver Operating Characteristic (AUROC) curve and the average accuracy (across all steps) in the Next Period scenario. These indicators are chosen because they provide valuable insights into the detector’s ability to generalize to unseen generators that are being released.

## Citation

```bibtex
@misc{pellegrini2025aigenbench,
  title={AI-GenBench: A New Ongoing Benchmark for AI-Generated Image Detection},
  author={Pellegrini et al. (2025)},
  year={2025},
  note={arXiv:2504.20865}
}
```

- arXiv: 2504.20865
