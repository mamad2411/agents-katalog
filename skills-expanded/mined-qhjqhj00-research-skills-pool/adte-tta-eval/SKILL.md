---
name: adte-tta-eval
description: Evaluates test-time adaptation (TTA) capabilities of vision-language models under distribution shift and class imbalance. It probes how well a model can adapt to out-of-distribution and cross-domain image classification tasks without training, using adaptive entropy-based uncertainty estimation to select confident augmented views. Use when the user wants to benchmark on ImageNet & Cross-Domain Benchmarks, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2602.11743
  bibtex_key: wu2026adte
  confidence: high
---

# adte-tta-eval

> Adaptive Debiasing Tsallis Entropy for Test-Time Adaptation — Wu et al. (2026) (arXiv:2602.11743, 2026)

## What this evaluates

Evaluates test-time adaptation (TTA) capabilities of vision-language models under distribution shift and class imbalance. It probes how well a model can adapt to out-of-distribution and cross-domain image classification tasks without training, using adaptive entropy-based uncertainty estimation to select confident augmented views.

## Datasets

- **ImageNet & Cross-Domain Benchmarks** — total ?; splits: test (-1)

## Metrics

- `accuracy` **(primary)** — range: percent
  - Percentage of correctly classified test images out of the total number of test images. Reported per dataset and averaged across OOD variants or cross-domain datasets.

## Input / output format

**Input**: RGB image patches paired with text prompts (either hand-crafted templates or GPT-generated CuPL descriptions), processed by a frozen CLIP vision encoder (ViT-B/16 or ViT-L/14) during inference.

**Output**: Class prediction probabilities (logits) and entropy/uncertainty scores for each augmented view, used to select the most confident predictions for test-time adaptation.

## Scoring recipe

```python
predictions = []
for image, label in test_set:
    views = augment(image, N=64)
    probs = model(views, text_prompts)
    selected_probs = filter_confident(probs, ratio=0.1)
    pred = argmax(selected_probs)
    predictions.append(pred)
accuracy = sum(p == l for p, l in zip(predictions, labels)) / len(labels)
```

## Common pitfalls

- Hyperparameters are strictly fixed (N=64 views, 0.1 filtering ratio, memory bank size=10, q interval [0.01, 0.9]) and must not be tuned per dataset.
- Results must be averaged over 3 random seeds, and both template-based and CuPL text prompts should be evaluated separately.
- The memory bank size of 1 does not mean the bank can be removed; it still aggregates pseudo-labels across all 200+ categories for bias estimation.

## Evidence (verbatim from paper)

> Table 1: Accuracy comparison (%) on ImageNet and its variants for CLIP ViT-B/16 and ViT-L/14.

## Citation

```bibtex
@misc{wu2026adte,
  title={Adaptive Debiasing Tsallis Entropy for Test-Time Adaptation},
  author={Wu et al. (2026)},
  year={2026},
  note={arXiv:2602.11743}
}
```

- arXiv: 2602.11743
