---
name: adult-eval
description: This benchmark evaluates income prediction models for fairness regarding demographic attributes like race and gender. It probes prediction stability under demographic perturbations (individual fairness) and measures equity in true positive rates across protected groups (group fairness). Use when the user wants to benchmark on Adult, or asks about evaluating this task. Reports Balanced Accuracy (BA).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2006.14168
  bibtex_key: yurochkin2020sensi
  confidence: high
---

# adult-eval

> SenSeI: Sensitive Set Invariance for Enforcing Individual Fairness — Yurochkin et al. (2020) (arXiv:2006.14168, 2020)

## What this evaluates

This benchmark evaluates income prediction models for fairness regarding demographic attributes like race and gender. It probes prediction stability under demographic perturbations (individual fairness) and measures equity in true positive rates across protected groups (group fairness).

## Datasets

- **Adult** — total ?; splits: train (-1), test (-1); HF `uciml/adult`

## Metrics

- `Balanced Accuracy (BA)` **(primary)** — range: [0, 1]
  - Average of sensitivity and specificity, used to handle class imbalance.
- `S-Con. (Spouse Consistency)` — range: [0, 1]
  - Prediction consistency when marital status is perturbed.
- `GR-Con. (Gender/Race Consistency)` — range: [0, 1]
  - Prediction consistency when gender and race are perturbed.
- `Gap_G^RMS` — range: [0, 1]
  - RMS gap between true positive rates across genders.
- `Gap_R^RMS` — range: [0, 1]
  - RMS gap between true positive rates across races.

## Input / output format

**Input**: Tabular demographic and socioeconomic features (education, gender, race, marital status, hours worked, etc.).

**Output**: Binary income prediction (> $50k vs ≤ $50k).

## Scoring recipe

```python
Perturb demographic features (marital status, gender, race) to generate counterfactuals.
s_con = mean(predictions == perturbed_marital_preds)
gr_con = mean(predictions == perturbed_gender_race_preds)
gap_g_rms = sqrt(mean((tpr_male - tpr_female)**2))
gap_r_rms = sqrt(mean((tpr_race1 - tpr_race2)**2))
```

## Common pitfalls

- CLP baseline is excluded because counterfactuals are undefined for tabular data.
- Fair metric uses Mahalanobis distance with certain demographic dimensions projected out, which may affect consistency scores.

## Evidence (verbatim from paper)

> To quantify group fairness they used RMS gaps and maximum gaps between true positive rates across genders (Gap_G^RMS and Gap_G^max) and races (Gap_R^RMS and Gap_R^max). Due to class imbalance, performance is quantified with balanced accuracy (B-Acc).

## Citation

```bibtex
@misc{yurochkin2020sensi,
  title={SenSeI: Sensitive Set Invariance for Enforcing Individual Fairness},
  author={Yurochkin et al. (2020)},
  year={2020},
  note={arXiv:2006.14168}
}
```

- arXiv: 2006.14168
