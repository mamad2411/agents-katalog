---
name: aiotbench-eval
description: Evaluates AI inference performance across diverse image classification model architectures on mobile and embedded devices. It measures the trade-off between inference speed and computational efficiency to compare models, frameworks, and hardware. Use when the user wants to benchmark on ImageNet 2012, or asks about evaluating this task. Reports VIPS.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2005.05085
  bibtex_key: luo2020comparison
  confidence: high
---

# aiotbench-eval

> Comparison and Benchmarking of AI Models and Frameworks on Mobile Devices — Chunjie Luo et al. (2020) (arXiv:2005.05085, 2020)

## What this evaluates

Evaluates AI inference performance across diverse image classification model architectures on mobile and embedded devices. It measures the trade-off between inference speed and computational efficiency to compare models, frameworks, and hardware.

## Datasets

- **ImageNet 2012** — total 5000; splits: val (5000)

## Metrics

- `VIPS` **(primary)** — range: images/sec
  - Valid Images Per Second, measuring the number of correctly classified images processed per second during inference.
- `VOPS` — range: FLOPS
  - Valid FLOPs Per Second, quantifying computational efficiency by dividing the total valid inferences by the total FLOPs consumed per second.

## Input / output format

**Input**: Single RGB image for classification.

**Output**: Predicted class label.

## Scoring recipe

```python
def compute_metrics(predictions, gold_labels, elapsed_time, flops_per_img):
    valid_count = sum(1 for p, g in zip(predictions, gold_labels) if p == g)
    total_flops = valid_count * flops_per_img
    vips = valid_count / elapsed_time
    vops = total_flops / elapsed_time
    return {"VIPS": vips, "VOPS": vops}
```

## Common pitfalls

- Using the full 50,000 validation set instead of the sampled 5,000 subset, which takes too long on mobile devices.
- Reporting raw FPS or TOPS without filtering for valid (correctly classified) inferences, which misrepresents practical utility.
- Comparing frameworks without normalizing for device-specific hardware differences.

## Evidence (verbatim from paper)

> It proposes two unified, device-agnostic metrics—Valid Images Per Second (VIPS) and Valid FLOPs Per Second (VOPS)—to quantify the trade-off between inference speed and computational efficiency, enabling direct comparison of models, frameworks, and devices without requiring custom optimizations or full-stack tuning.

## Citation

```bibtex
@misc{luo2020comparison,
  title={Comparison and Benchmarking of AI Models and Frameworks on Mobile Devices},
  author={Chunjie Luo et al. (2020)},
  year={2020},
  note={arXiv:2005.05085}
}
```

- arXiv: 2005.05085
