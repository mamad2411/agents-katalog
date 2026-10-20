---
name: artefact-eval
description: Evaluates the ability of segmentation models (CNNs, Transformers, diffusion models, and vision foundation models) to detect and classify diverse damage types on analogue media across different material and content categories. It probes cross-media generalization using a leave-one-out protocol and tests the effectiveness of zero-shot, supervised, and text-guided prompting strategies for pixel-level damage localization. Use when the user wants to benchmark on ARTeFACT, or asks about evaluating this task. Reports macro-averaged F1 Score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2412.04580
  bibtex_key: ivanova2024artefact
  confidence: high
---

# artefact-eval

> ARTeFACT: Benchmarking Segmentation Models on Diverse Analogue Media Damage — Ivanova et al. (2024) (arXiv:2412.04580, 2024)

## What this evaluates

Evaluates the ability of segmentation models (CNNs, Transformers, diffusion models, and vision foundation models) to detect and classify diverse damage types on analogue media across different material and content categories. It probes cross-media generalization using a leave-one-out protocol and tests the effectiveness of zero-shot, supervised, and text-guided prompting strategies for pixel-level damage localization.

## Datasets

- **ARTeFACT** — total ?; splits: train (-1), val (-1), test (-1)

## Metrics

- `macro-averaged F1 Score` **(primary)** — range: [0, 1]
  - Macro-averaged F1 score computed across all damage classes (binary or multiclass), calculated by averaging the per-class F1 scores (harmonic mean of precision and recall).
- `mIoU` — range: [0, 1]
  - Mean Intersection over Union averaged across all classes, measuring the overlap ratio between predicted and ground-truth segmentation masks per class before averaging.
- `Accuracy` — range: [0, 1]
  - Macro-averaged pixel-wise accuracy across all classes, reporting the proportion of correctly classified pixels per class before averaging.

## Input / output format

**Input**: RGB images of analogue media with varying resolutions and aspect ratios. For supervised models, images are split into 512x512 overlapping patches. For diffusion models, images are center-cropped and resized to 512x512. Zero-shot/text-guided settings additionally receive prompts (points, bounding boxes, or text descriptions).

**Output**: Pixel-wise segmentation masks (binary: Damaged/Clean or multiclass: 15 damage types) or per-class probability maps.

## Scoring recipe

```python
def compute_metrics(pred_masks, gt_masks, num_classes):
    # pred_masks, gt_masks: shape (H, W, num_classes) or (H, W) with class indices
    intersection = np.sum(pred_masks == gt_masks, axis=(0,1))
    pred_sum = np.sum(pred_masks, axis=(0,1))
    gt_sum = np.sum(gt_masks, axis=(0,1))
    union = pred_sum + gt_sum - intersection
    iou_per_class = intersection / (union + 1e-6)
    miou = np.mean(iou_per_class)
    precision = intersection / (pred_sum + 1e-6)
    recall = intersection / (gt_sum + 1e-6)
    f1_per_class = 2 * precision * recall / (precision + recall + 1e-6)
    macro_f1 = np.mean(f1_per_class)
    accuracy = np.mean(intersection / (gt_sum + 1e-6))
    return macro_f1, miou, accuracy
```

## Common pitfalls

- SAM's zero-shot evaluation requires an impractical number of prompts (e.g., ~112 bounding boxes per image) to achieve usable segmentation, making the zero-shot setting unrealistic for real-world restoration workflows.
- The dataset exhibits severe class imbalance towards 'Clean' regions, so standard accuracy is misleading; the paper explicitly uses macro-averaged metrics and macro-averaged Dice loss to mitigate this.
- Diffusion-based methods (DiffEdit/DiffSeg) rely on an oracle to assign Damaged/Clean labels to predicted segments during evaluation, which masks their inability to perform semantic classification without ground-truth supervision.

## Evidence (verbatim from paper)

> We measure macro-averaged F1 Score and Mean Intersection over Union (mIoU), fine-tuning models until the validation F1 score has not improved for 10 epochs.

## Citation

```bibtex
@misc{ivanova2024artefact,
  title={ARTeFACT: Benchmarking Segmentation Models on Diverse Analogue Media Damage},
  author={Ivanova et al. (2024)},
  year={2024},
  note={arXiv:2412.04580}
}
```

- arXiv: 2412.04580
