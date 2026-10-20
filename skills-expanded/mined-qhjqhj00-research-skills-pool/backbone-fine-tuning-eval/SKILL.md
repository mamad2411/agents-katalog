---
name: backbone-fine-tuning-eval
description: Evaluates the fine-tuning performance of lightweight, pre-trained CNN and attention-based backbones across diverse image classification domains, including natural images, remote sensing, medical histopathology, and plant imaging. It probes how well different architectures generalize under data-scarce conditions and whether ImageNet pre-training accuracy correlates with downstream task performance. Use when the user wants to benchmark on CIFAR-10, CIFAR-100, Tiny ImageNet, Stanford Dogs, Flowers102, CUB200, Stanford Cars, DTD, UC Merced Land Use, EuroSAT, PlantVillage, PlantCLEF, Galaxy10, BreakHis, RSNA, Food-101, or asks about evaluating this task. Reports Top-1 classification accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2406.05612
  bibtex_key: jeevan2024backbone
  confidence: high
---

# backbone-fine-tuning-eval

> Which Backbone to Use: A Resource-efficient Domain Specific Comparison for Computer Vision — Jeevan et al. (2024) (arXiv:2406.05612, 2024)

## What this evaluates

Evaluates the fine-tuning performance of lightweight, pre-trained CNN and attention-based backbones across diverse image classification domains, including natural images, remote sensing, medical histopathology, and plant imaging. It probes how well different architectures generalize under data-scarce conditions and whether ImageNet pre-training accuracy correlates with downstream task performance.

## Datasets

- **CIFAR-10** — total ?; splits: test (-1)
- **CIFAR-100** — total ?; splits: test (-1)
- **Tiny ImageNet** — total ?; splits: test (-1)
- **Stanford Dogs** — total ?; splits: test (-1)
- **Flowers102** — total ?; splits: test (-1)
- **CUB200** — total ?; splits: test (-1)
- **Stanford Cars** — total ?; splits: test (-1)
- **DTD** — total ?; splits: test (-1)
- **UC Merced Land Use** — total ?; splits: test (-1)
- **EuroSAT** — total ?; splits: test (-1)
- **PlantVillage** — total ?; splits: test (-1)
- **PlantCLEF** — total ?; splits: test (-1)
- **Galaxy10** — total ?; splits: test (-1)
- **BreakHis** — total ?; splits: test (-1)
- **RSNA** — total ?; splits: test (-1)
- **Food-101** — total ?; splits: test (-1)

## Metrics

- `Top-1 classification accuracy` **(primary)** — range: percent
  - The percentage of correctly predicted class labels out of the total number of test instances.

## Input / output format

**Input**: RGB images resized to the backbone's standard input resolution (typically 224x224 or 256x256 pixels).

**Output**: Predicted class label (integer or string) corresponding to the dataset's class index.

## Scoring recipe

```python
def compute_accuracy(predictions, gold_labels):
    correct = sum(1 for p, g in zip(predictions, gold_labels) if p == g)
    return (correct / len(gold_labels)) * 100
```

## Common pitfalls

- ImageNet top-1 accuracy does not reliably predict fine-tuning performance on domain-specific datasets.
- Performance in medical datasets (BreakHis) varies significantly across different microscope magnification levels (40x, 100x, 200x, 400x).
- Model generalization degrades non-uniformly when training data is reduced to 1% or 10%, with some architectures failing faster than others.

## Evidence (verbatim from paper)

> The results of our fine-tuning experiments on datasets of all domains are shown in Table[4], Table[5] and Table[6]. ... Table 4: Top-1 classification accuracy for fine-tuning pre-trained backbones on natural image datasets.

## Citation

```bibtex
@misc{jeevan2024backbone,
  title={Which Backbone to Use: A Resource-efficient Domain Specific Comparison for Computer Vision},
  author={Jeevan et al. (2024)},
  year={2024},
  note={arXiv:2406.05612}
}
```

- arXiv: 2406.05612
