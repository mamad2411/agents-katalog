---
name: aerr-continuous-eval
description: Evaluates a model's ability to recognize spontaneous apparent emotional reactions from video by predicting continuous arousal and valence dimensions per frame. Use when the user wants to benchmark on SEWA, RECOLA, or asks about evaluating this task. Reports ccc.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2210.11341
  bibtex_key: jegorova2022ssvaerr
  confidence: high
---

# aerr-continuous-eval

> SS-VAERR: Self-Supervised Apparent Emotional Reaction Recognition from Video — Jegorova et al. (2022) (arXiv:2210.11341, 2022)

## What this evaluates

Evaluates a model's ability to recognize spontaneous apparent emotional reactions from video by predicting continuous arousal and valence dimensions per frame.

## Datasets

- **SEWA** — total ?; splits: train (435), val (53), test (53)
- **RECOLA** — total ?; splits: train (197), val (152), test (-1)

## Metrics

- `ccc` **(primary)** — range: [-1, 1]
  - Concordance Correlation Coefficient measures agreement between predicted and ground-truth continuous values. Formula: ccc = (2 * rho * sigma_x * sigma_y) / (sigma_x^2 + sigma_y^2 + (mu_x - mu_y)^2), where rho is Pearson correlation, mu is mean, and sigma is standard deviation.

## Input / output format

**Input**: Grayscale video frames cropped to 96x96 around the face, sampled as fixed-length segments (200 frames for SEWA, 500 frames for RECOLA).

**Output**: Continuous scalar predictions for arousal and valence per frame/segment.

## Scoring recipe

```python
import numpy as np
def compute_ccc(pred, gold):
    mean_p, mean_g = np.mean(pred), np.mean(gold)
    var_p, var_g = np.var(pred, ddof=1), np.var(gold, ddof=1)
    cov = np.cov(pred, gold)[0, 1]
    rho = cov / np.sqrt(var_p * var_g)
    ccc = (2 * rho * np.sqrt(var_p * var_g)) / (var_p + var_g + (mean_p - mean_g)**2)
    return ccc
```

## Common pitfalls

- RECOLA's test set is not publicly available; evaluations must report results on the validation set instead.
- Metrics are computed per frame, but models are trained on fixed-length segments (200/500 frames), requiring careful alignment during inference.
- Face cropping to 96x96 and grayscale conversion are mandatory for fair comparison; raw RGB videos will yield invalid results.

## Evidence (verbatim from paper)

> Breakdown into training, validation, and test set is conducted in the same manner as in [[2]] for SEWA (train./val./test sets containing 435/53/53 instances), and as in [[19]] for RECOLA (train./val. containing 197/152 instances, with results reported on the validation set, as the test set for RECOLA is not publicly available). TABLE III: Comparison of the various losses for the downstream tasks with LiRA pre-training. Only non-zero loss-weights are presented. ‘Arous.’ and ‘Val.’ superscripts specify the loss applied specifically to either arousal or valence predictions. REGRESSION $w_{ccc}=1$ 0.678 0.737 0.652 0.722 0.630 0.607 0.560 0.603

## Citation

```bibtex
@misc{jegorova2022ssvaerr,
  title={SS-VAERR: Self-Supervised Apparent Emotional Reaction Recognition from Video},
  author={Jegorova et al. (2022)},
  year={2022},
  note={arXiv:2210.11341}
}
```

- arXiv: 2210.11341
