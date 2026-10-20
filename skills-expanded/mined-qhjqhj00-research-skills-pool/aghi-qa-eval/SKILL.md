---
name: aghi-qa-eval
description: Evaluates the perceptual quality and text-image correspondence of AI-generated human images, while also benchmarking the ability of models to identify visible and semantically distorted human body parts. Use when the user wants to benchmark on AGHI-QA, or asks about evaluating this task. Reports SRCC.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2504.21308
  bibtex_key: li2025aghiqa
  confidence: high
---

# aghi-qa-eval

> AGHI-QA: A Subjective-Aligned Dataset and Metric for AI-Generated Human Images — Li et al. (2025) (arXiv:2504.21308, 2025)

## What this evaluates

Evaluates the perceptual quality and text-image correspondence of AI-generated human images, while also benchmarking the ability of models to identify visible and semantically distorted human body parts.

## Datasets

- **AGHI-QA** — total 4000; splits: train (-1), test (-1)

## Metrics

- `SRCC` **(primary)** — range: [-1, 1]
  - Spearman rank correlation coefficient measuring the monotonic relationship between predicted quality scores and human-annotated ground truth scores.
- `PLCC` — range: [-1, 1]
  - Pearson linear correlation coefficient measuring the linear relationship between predicted and ground truth scores.
- `KRCC` — range: [-1, 1]
  - Kendall rank-order correlation coefficient measuring the ordinal association between predicted and ground truth scores.

## Input / output format

**Input**: AI-generated human image (optionally cropped to human-centered region) and corresponding text prompt.

**Output**: Continuous quality scores for perceptual quality and text-image correspondence, or classification labels for visible/distorted human body parts.

## Scoring recipe

```python
def compute_correlations(pred, gold):
    # Rank both arrays
    pred_rank = np.argsort(np.argsort(pred))
    gold_rank = np.argsort(np.argsort(gold))
    n = len(pred)
    d_sq = np.sum((pred_rank - gold_rank) ** 2)
    srcc = 1 - (6 * d_sq) / (n * (n**2 - 1))
    # PLCC: linear regression then correlation
    slope, intercept = np.polyfit(pred, gold, 1)
    gold_pred = slope * pred + intercept
    plcc = np.corrcoef(gold, gold_pred)[0, 1]
    # KRCC
    krcc, _ = kendalltau(gold, pred)
    return srcc, plcc, krcc
```

## Common pitfalls

- Traditional no-reference IQA metrics (e.g., NIQE, BRISQUE) fail to capture semantic distortions in AI-generated human images.
- Zero-shot inference on vision-language models often underperforms compared to fine-tuned or adapted methods on this specific domain.
- Evaluating fine-grained distortions on complex parts like hands and faces is significantly harder than on limbs or torso, leading to skewed average scores.

## Evidence (verbatim from paper)

> Spearman rank correlation coefficient (SRCC), Pearson linear correlation coefficient (PLCC) and Kendall rank-order correlation coefficient (KRCC) are utilized for evaluating the scoring ability of each model. During evaluation, we split the data set into training set and testing set with a ratio of 0.8 and 0.2. We randomly split the data set five times and report the average results.

## Citation

```bibtex
@misc{li2025aghiqa,
  title={AGHI-QA: A Subjective-Aligned Dataset and Metric for AI-Generated Human Images},
  author={Li et al. (2025)},
  year={2025},
  note={arXiv:2504.21308}
}
```

- arXiv: 2504.21308
