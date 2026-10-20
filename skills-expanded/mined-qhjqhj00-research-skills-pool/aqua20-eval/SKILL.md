---
name: aqua20-eval
description: Evaluates deep learning models' ability to classify marine species from underwater images under challenging environmental conditions like turbidity, low illumination, and occlusion. It probes robustness to visual distortions, class imbalance, and fine-grained feature discrimination in complex aquatic scenes. Use when the user wants to benchmark on AQUA20, or asks about evaluating this task. Reports Accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2506.17455
  bibtex_key: fuad2025aqua20
  confidence: high
---

# aqua20-eval

> AQUA20: A Benchmark Dataset for Underwater Species Classification under Challenging Conditions — Fuad et al. (2025) (arXiv:2506.17455, 2025)

## What this evaluates

Evaluates deep learning models' ability to classify marine species from underwater images under challenging environmental conditions like turbidity, low illumination, and occlusion. It probes robustness to visual distortions, class imbalance, and fine-grained feature discrimination in complex aquatic scenes.

## Datasets

- **AQUA20** — total 8171; splits: test (-1)

## Metrics

- `Accuracy` **(primary)** — range: [0, 1]
  - Proportion of correct predictions (both TP and TN) among the total number of cases examined. Formula: (TP + TN) / (TP + TN + FP + FN).
- `F1-Score` — range: [0, 1]
  - Harmonic mean of precision and recall. Formula: 2 * (Precision * Recall) / (Precision + Recall).
- `Precision` — range: [0, 1]
  - Proportion of TP among all positive predictions. Formula: TP / (TP + FP).
- `Recall` — range: [0, 1]
  - Proportion of TP that were correctly identified. Formula: TP / (TP + FN).
- `ROC-AUC` — range: [0, 1]
  - Area under the receiver operating characteristic curve, plotting TPR against FPR at different thresholds. Formula: ∫ TPR(FPR) dFPR.

## Input / output format

**Input**: RGB images resized to 32×32 pixels, normalized using ImageNet statistics (μ=(0.485, 0.456, 0.406), σ=(0.229, 0.224, 0.225)).

**Output**: Single class label prediction (one of 20 marine species). The paper also reports Top-2 and Top-3 accuracy rankings.

## Scoring recipe

```python
def compute_metrics(predictions, labels, num_classes=20):
    tp = tn = fp = fn = 0
    for p, y in zip(predictions, labels):
        if p == y:
            if p == 0: tn += 1
            else: tp += 1
        else:
            if p == 0: fp += 1
            else: fn += 1
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    return {'accuracy': accuracy, 'precision': precision, 'recall': recall, 'f1': f1}
```

## Common pitfalls

- The dataset exhibits severe class imbalance (e.g., 11 samples for Crab vs. 538 for Fish), causing per-class F1 and recall to be highly volatile and not directly comparable to balanced benchmarks.
- Input resolution is fixed at 32×32 pixels, which is unusually low for modern vision models and may artificially suppress performance on fine-grained underwater textures compared to standard 224×224 evaluations.
- No data augmentation was applied during training, meaning reported metrics are strictly dependent on the exact image distribution and environmental conditions present in the fixed split.

## Evidence (verbatim from paper)

> We have selected accuracy as our primary evaluation metric. Additionally, we report other performance metrics to provide a comprehensive evaluation of each model, as shown in Table[3]. The metrics used in this paper are defined as follows: Accuracy is the proportion of correct predictions (both TP and TN) among the total number of cases examined.

## Citation

```bibtex
@misc{fuad2025aqua20,
  title={AQUA20: A Benchmark Dataset for Underwater Species Classification under Challenging Conditions},
  author={Fuad et al. (2025)},
  year={2025},
  note={arXiv:2506.17455}
}
```

- arXiv: 2506.17455
