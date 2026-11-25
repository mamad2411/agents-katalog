---
name: aigc-detection-accuracy-eval
description: Evaluates the cross-generator generalization capability of AI-generated image (AIGC) detectors. It probes whether models trained on a specific generator (SDv1.4) can accurately distinguish real from fake images produced by diverse, unseen generative models and in-the-wild sources. Use when the user wants to benchmark on GenImage, GenImage++, Chameleon, or asks about evaluating this task. Reports Accuracy (ACC).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2506.00874
  bibtex_key: zhou2025breakinglatent
  confidence: high
---

# aigc-detection-accuracy-eval

> Breaking Latent Prior Bias in Detectors for Generalizable AIGC Image Detection — Zhou et al. (2025) (arXiv:2506.00874, 2025)

## What this evaluates

Evaluates the cross-generator generalization capability of AI-generated image (AIGC) detectors. It probes whether models trained on a specific generator (SDv1.4) can accurately distinguish real from fake images produced by diverse, unseen generative models and in-the-wild sources.

## Datasets

- **GenImage** — total ?; splits: train (-1), test (-1)
- **GenImage++** — total ?; splits: test (-1)
- **Chameleon** — total ?; splits: test (-1)

## Metrics

- `Accuracy (ACC)` **(primary)** — range: percent
  - Percentage of correctly classified images (real vs. fake) out of the total test set. Calculated as (correct predictions / total predictions) × 100.

## Input / output format

**Input**: Single RGB image (real or AI-generated) passed through a detector model (e.g., ResNet50 or CLIP ViT-L/14 + Linear Head).

**Output**: Binary classification prediction (real or fake), evaluated as a percentage accuracy against ground-truth labels.

## Scoring recipe

```python
def calculate_accuracy(predictions, labels):
    correct = sum(1 for p, l in zip(predictions, labels) if p == l)
    return (correct / len(labels)) * 100
```

## Common pitfalls

- Models are trained exclusively on the SDv1.4 subset of GenImage, so in-domain accuracy on SDv1.4 may drop significantly after adversarial training, while cross-generator accuracy improves.
- The Chameleon dataset contains 'in-the-wild' images with diverse styles and compression, leading to substantially lower accuracy compared to controlled benchmark subsets.
- Comparisons must ensure baselines are trained under the same SDv1.4 protocol; some prior methods (e.g., AIDE) were trained on the full GenImage dataset, making direct comparison slightly unfair.

## Evidence (verbatim from paper)

> We assess detector performance using Accuracy (ACC).

## Citation

```bibtex
@misc{zhou2025breakinglatent,
  title={Breaking Latent Prior Bias in Detectors for Generalizable AIGC Image Detection},
  author={Zhou et al. (2025)},
  year={2025},
  note={arXiv:2506.00874}
}
```

- arXiv: 2506.00874
