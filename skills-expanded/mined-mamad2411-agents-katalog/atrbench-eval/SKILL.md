---
name: atrbench-eval
description: Evaluates SAR automatic target recognition (ATR) capabilities under realistic, wild conditions. It probes fine-grained vehicle classification and detection robustness across varying imaging geometries, scene complexities, and domain shifts (SOC vs EOC settings). Use when the user wants to benchmark on ATRBench, or asks about evaluating this task. Reports overall accuracy (%).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2501.13354
  bibtex_key: liu2025atrbench
  confidence: high
---

# atrbench-eval

> ATRNet-STAR: A Large Dataset and Benchmark Towards Remote Sensing Object Recognition in the Wild — Liu et al. (2025) (arXiv:2501.13354, 2025)

## What this evaluates

Evaluates SAR automatic target recognition (ATR) capabilities under realistic, wild conditions. It probes fine-grained vehicle classification and detection robustness across varying imaging geometries, scene complexities, and domain shifts (SOC vs EOC settings).

## Datasets

- **ATRBench** — total ?; splits: SOC-40 train (-1), SOC-40 test (-1), SOC-50 train (-1), SOC-50 test (-1), EOC-Scene train (-1), EOC-Scene test (-1), EOC-Depression train (-1), EOC-Depression test (-1), EOC-Azimuth train (-1), EOC-Azimuth test (-1), EOC-Band train (-1), EOC-Band test (-1), EOC-Polarization train (-1), EOC-Polarization test (-1); repo https://github.com/waterdisappear/ATRNet-STAR

## Metrics

- `overall accuracy (%)` **(primary)** — range: percent
  - The number of correctly classified samples divided by the total number of samples, multiplied by 100.
- `mAP50` — range: percent
  - Mean Average Precision at an Intersection over Union (IoU) threshold of 0.5. Computed as the average precision across all vehicle categories using horizontal bounding boxes.

## Input / output format

**Input**: SAR images provided as either magnitude images in the ground range coordinate system or complex images in the slant range coordinate system.

**Output**: Classification: predicted vehicle category label. Detection: horizontal bounding box coordinates (x, y, width, height) and predicted vehicle category.

## Scoring recipe

```python
# Classification scoring
preds = model.predict(images)
accuracy = (sum(1 for p, g in zip(preds, gold_labels) if p == g) / len(gold_labels)) * 100

# Detection scoring (mAP50)
# For each class, match predicted boxes to ground truth at IoU >= 0.5
# Compute precision-recall curve and interpolate to get AP_class
mAP50 = (sum(AP_class for class in classes) / num_classes) * 100
```

## Common pitfalls

- Confusing ground range magnitude images with slant range complex images, which have different annotation counts and require distinct preprocessing pipelines.
- Mixing up SOC (similar operating condition) and EOC (different operating condition) settings, which enforce strict train/test splits to evaluate specific domain shifts rather than standard generalization.
- Using oriented bounding boxes or contour masks for detection instead of horizontal bounding boxes, as the benchmark explicitly standardizes on horizontal boxes due to SAR target shape variations and noisy labels.

## Evidence (verbatim from paper)

> We use overall accuracy (%) as a metric, i.e., the number of correctly classified samples in proportion to the total number of samples. We use mAP50 as a metric, i.e., the average precision at IoU 0.5 because the horizontal bounding box does not exactly fit the contours of the different targets.

## Citation

```bibtex
@misc{liu2025atrbench,
  title={ATRNet-STAR: A Large Dataset and Benchmark Towards Remote Sensing Object Recognition in the Wild},
  author={Liu et al. (2025)},
  year={2025},
  note={arXiv:2501.13354}
}
```

- arXiv: 2501.13354
