---
name: ai-face-fairness-bench-eval
description: Evaluates the fairness and utility of AI-generated face detectors across demographic attributes (skin tone, gender, age) and intersectional groups. It measures how well detectors distinguish real vs. AI-generated faces while ensuring equitable performance across demographic subgroups. Use when the user wants to benchmark on AI-Face, or asks about evaluating this task. Reports $F_{MEO}$.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2406.00783
  bibtex_key: lin2024aiface
  confidence: high
---

# ai-face-fairness-bench-eval

> AI-Face: A Million-Scale Demographically Annotated AI-Generated Face Dataset and Fairness Benchmark — Lin et al. (2024) (arXiv:2406.00783, 2024)

## What this evaluates

Evaluates the fairness and utility of AI-generated face detectors across demographic attributes (skin tone, gender, age) and intersectional groups. It measures how well detectors distinguish real vs. AI-generated faces while ensuring equitable performance across demographic subgroups.

## Datasets

- **AI-Face** — total 1000000; splits: train (-1), test (-1); repo https://github.com/Purdue-M2/AI-Face-FairnessBench

## Metrics

- `$F_{MEO}$` **(primary)** — range: percent
  - Max Equalized Odds: measures the maximum difference in equalized odds across demographic groups. Lower values indicate better group fairness.
- `$F_{DP}$` — range: percent
  - Demographic Parity: measures the difference in positive prediction rates across demographic groups. Lower values indicate better fairness.
- `$F_{EO}$` — range: percent
  - Equal Odds: measures the difference in true positive and false positive rates across demographic groups.
- `$F_{OAE}$` — range: percent
  - Overall Accuracy Equality: measures the difference in overall accuracy across demographic groups.
- `$F_{IND}$` — range: percent
  - Individual Fairness: measures whether similar individuals receive similar predicted outcomes.
- `AUC` — range: [0, 1]
  - Area Under the ROC Curve: measures the model's ability to discriminate between real and AI-generated faces across all classification thresholds.
- `ACC` — range: percent
  - Accuracy: proportion of correctly classified images (real vs. AI-generated).
- `AP` — range: [0, 1]
  - Average Precision: summary metric of the precision-recall curve.
- `EER` — range: percent
  - Equal Error Rate: the point where false positive rate equals false negative rate.
- `FPR` — range: percent
  - False Positive Rate: proportion of real faces incorrectly classified as AI-generated.

## Input / output format

**Input**: Single face image (real or AI-generated) with associated demographic labels (skin tone, gender, age).

**Output**: Binary prediction (real vs. AI-generated) or probability score per image.

## Scoring recipe

```python
def compute_metrics(predictions, labels, demographics):
    # Group by demographic attribute (e.g., gender, skin tone, age)
    groups = group_by_attribute(demographics, ['gender', 'skin_tone', 'age'])
    
    # Calculate utility metrics on full test set
    acc = accuracy_score(labels, predictions)
    auc = roc_auc_score(labels, predictions)
    
    # Calculate fairness metrics per group
    f_meo = 0
    f_dp = 0
    for group in groups:
        group_preds = predictions[group]
        group_labels = labels[group]
        tpr = true_positive_rate(group_labels, group_preds)
        fpr = false_positive_rate(group_labels, group_preds)
        f_dp += abs(mean(group_preds) - mean(predictions))
        f_meo = max(f_meo, abs(tpr - mean_tpr), abs(fpr - mean_fpr))
    
    return {'ACC': acc, 'AUC': auc, 'F_MEO': f_meo, 'F_DP': f_dp}
```

## Common pitfalls

- Evaluating only single demographic attributes (e.g., gender alone) while ignoring intersectional groups (e.g., Female-Dark skin tone).
- Relying solely on overall accuracy or AUC, which can mask severe demographic disparities in detection performance.
- Failing to normalize the 10 skin tone categories into Light/Medium/Dark groups before computing fairness metrics, as specified in the benchmark protocol.

## Evidence (verbatim from paper)

> To provide a comprehensive benchmarking, we consider 5 fairness metrics commonly used in fairness community[[90], [91], [92], [93], [94]] and 5 widely used utility metrics. For fairness metrics, we consider Demographic Parity ($F_{DP}$)[[90], [91]], Max Equalized Odds ($F_{MEO}$)[[93]], Equal Odds ($F_{EO}$)[[92]], and Overall Accuracy Equality ($F_{OAE}$)[[93]] for evaluating group (e.g., gender) and intersectional (e.g., individuals of a specific gender and simultaneously a specific skin tone) fairness.

## Citation

```bibtex
@misc{lin2024aiface,
  title={AI-Face: A Million-Scale Demographically Annotated AI-Generated Face Dataset and Fairness Benchmark},
  author={Lin et al. (2024)},
  year={2024},
  note={arXiv:2406.00783}
}
```

- arXiv: 2406.00783
