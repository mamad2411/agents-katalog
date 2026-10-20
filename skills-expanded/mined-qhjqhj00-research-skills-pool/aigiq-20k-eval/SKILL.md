---
name: aigiq-20k-eval
description: This benchmark evaluates the perceptual quality and text-to-image alignment of AI-generated images. It benchmarks objective quality assessment models against large-scale human subjective ratings to measure how well automated metrics correlate with human perception. Use when the user wants to benchmark on AIGIQA-20K, or asks about evaluating this task. Reports SRoCC.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2404.03407
  bibtex_key: li2024aigiq20k
  confidence: high
---

# aigiq-20k-eval

> AIGIQA-20K: A Large Database for AI-Generated Image Quality Assessment — Li et al. (2024) (arXiv:2404.03407, 2024)

## What this evaluates

This benchmark evaluates the perceptual quality and text-to-image alignment of AI-generated images. It benchmarks objective quality assessment models against large-scale human subjective ratings to measure how well automated metrics correlate with human perception.

## Datasets

- **AIGIQA-20K** — total 20000; splits: full (20000)

## Metrics

- `SRoCC` **(primary)** — range: [-1, 1]
  - Computes the Spearman rank-order correlation coefficient between the predicted quality scores of an objective model and the human-derived Mean Opinion Scores (MOS). Ranges from -1 to 1, where 1 indicates perfect monotonic agreement.

## Input / output format

**Input**: AI-generated image paired with its corresponding text prompt.

**Output**: A continuous quality score (typically 0-5 or normalized) representing the predicted perceptual quality and text-to-image alignment.

## Scoring recipe

```python
def compute_srcc(pred_scores, human_mos):
    pred_rank = [x[0] for x in sorted(enumerate(pred_scores), key=lambda x: x[1])]
    gold_rank = [x[0] for x in sorted(enumerate(human_mos), key=lambda x: x[1])]
    n = len(pred_scores)
    d_sq = sum((p - g) ** 2 for p, g in zip(pred_rank, gold_rank))
    return 1 - (6 * d_sq) / (n * (n ** 2 - 1))
```

## Common pitfalls

- Human MOS computation involves a specific logarithmic normalization and Z-score conversion per the paper's formula, which differs from standard linear averaging.
- Outlier human raters are removed based on an SRoCC < 0.6 threshold against the global average before computing final MOS, which can significantly alter the ground truth if not replicated exactly.

## Evidence (verbatim from paper)

> we compute the Spearman Rank-order Correlation Coefficient (SRoCC) between them and the global average and remove the outliers with SRoCC lower than 0.6.

## Citation

```bibtex
@misc{li2024aigiq20k,
  title={AIGIQA-20K: A Large Database for AI-Generated Image Quality Assessment},
  author={Li et al. (2024)},
  year={2024},
  note={arXiv:2404.03407}
}
```

- arXiv: 2404.03407
