---
name: age-prediction-fairness-eval
description: Evaluates the accuracy and demographic fairness of deep learning models for age prediction from facial images. It probes the model's ability to generalize across diverse camera settings and ethnicities/genders while mitigating bias through distribution-aware curation and augmentation. Use when the user wants to benchmark on APPA-REAL, MORPH-2, UTKFace, Mega Asian, AFAD, CACD, or asks about evaluating this task. Reports MAE.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2009.05283
  bibtex_key: cao2020fair
  confidence: high
---

# age-prediction-fairness-eval

> Fair and accurate age prediction using distribution aware data curation and augmentation — Cao et al. (2020) (arXiv:2009.05283, 2020)

## What this evaluates

Evaluates the accuracy and demographic fairness of deep learning models for age prediction from facial images. It probes the model's ability to generalize across diverse camera settings and ethnicities/genders while mitigating bias through distribution-aware curation and augmentation.

## Datasets

- **APPA-REAL** — total ?; splits: test (-1)
- **MORPH-2** — total ?; splits: test (-1)
- **UTKFace** — total ?; splits: test (-1)
- **Mega Asian** — total ?; splits: test (-1)
- **AFAD** — total ?; splits: test (-1)
- **CACD** — total ?; splits: test (-1)

## Metrics

- `MAE` **(primary)** — range: other
  - Mean Absolute Error: the average of the absolute differences between predicted and ground-truth ages across all test samples.
- `Fairness score` — range: percent
  - Percentage of ages (out of 100 evaluated ages) where the mean distance between predicted ages across sensitive feature groups (ethnicity or gender) is below a threshold of t=3 years.

## Input / output format

**Input**: Pre-processed facial images (cropped and aligned) with ground-truth age and sensitive attributes (ethnicity, gender).

**Output**: Predicted age value (continuous or discrete interval) per image.

## Scoring recipe

```python
def compute_mae(preds, truths):
    return sum(abs(p - t) for p, t in zip(preds, truths)) / len(preds)

def compute_fairness_score(preds, truths, groups, threshold=3):
    fair_count = 0
    for age in range(100):
        age_preds = [p for p, t, g in zip(preds, truths, groups) if t == age]
        # Compute mean distance between group means (e.g., ethnicity A vs B)
        mean_dist = compute_mean_distance_between_groups(age_preds, groups, age)
        if mean_dist < threshold:
            fair_count += 1
    return (fair_count / 100) * 100
```

## Common pitfalls

- The Fairness score is not a standard demographic parity metric; it specifically measures the mean distance between predicted ages across sensitive groups per age, thresholded at 3 years.
- Evaluating on only a single benchmark dataset yields misleadingly high performance due to dataset-specific biases (e.g., camera settings, ethnicity distribution); cross-dataset evaluation is required.
- Industrial APIs output discrete ages or intervals, requiring median extraction or specific rounding before MAE calculation, unlike academic models that output continuous ages.

## Evidence (verbatim from paper)

> For performance, we opt for the commonly used mean absolute error (MAE), which calculates the mean of how many years the actual age has been mispredicted in absolute terms. For fairness, we build on commonly used mean distance which takes the mean distance between ages per sensitive features. For age prediction in particular, this distance has to be calculated for each age. Hence, we introduce a Fairness score for further evaluation, which takes the mean distance between sensitive features and checks if the distance is lower than a pre-defined threshold t=3, which stems from age discrimination based on the human rights act. Given 100 ages for evaluation, we calculate the fairness score by the per cent of ages, where the mean distance between sensitive features is below the defined threshold

## Citation

```bibtex
@misc{cao2020fair,
  title={Fair and accurate age prediction using distribution aware data curation and augmentation},
  author={Cao et al. (2020)},
  year={2020},
  note={arXiv:2009.05283}
}
```

- arXiv: 2009.05283
