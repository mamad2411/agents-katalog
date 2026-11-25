---
name: autofish-eval
description: Fine-grained instance segmentation and length estimation of visually similar fish species under realistic conveyor-belt conditions. The benchmark evaluates model robustness across separated, touching, and occluded fish configurations, using group-based splits to prevent data cross-contamination. Use when the user wants to benchmark on AutoFish, or asks about evaluating this task. Reports mAP.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2501.03767
  bibtex_key: bengtson2025autofish
  confidence: high
---

# autofish-eval

> AutoFish: Dataset and Benchmark for Fine-grained Analysis of Fish — Bengtson et al. (2025) (arXiv:2501.03767, 2025)

## What this evaluates

Fine-grained instance segmentation and length estimation of visually similar fish species under realistic conveyor-belt conditions. The benchmark evaluates model robustness across separated, touching, and occluded fish configurations, using group-based splits to prevent data cross-contamination.

## Datasets

- **AutoFish** — total 1500; splits: train (-1), val (-1), test (-1)

## Metrics

- `mAP` **(primary)** — range: [0, 1]
  - Mean Average Precision computed as AP@[IoU=.5:.95], averaging AP scores at IoU thresholds from 0.5 to 0.95 in steps of 0.05 between predictions and ground truth masks.
- `MAE` — range: cm
  - Mean Absolute Error in centimeters, calculated as the average of |predicted_length - true_length| across all specimens.
- `MAPE` — range: percent
  - Mean Absolute Percentage Error, calculated as the average of |(predicted_length - true_length) / true_length| * 100%.

## Input / output format

**Input**: RGB images of fish on a conveyor belt. For length estimation, inputs are either ground-truth instance masks or predicted instance masks from a segmentation model.

**Output**: For segmentation: class labels, bounding boxes, and instance segmentation masks. For length estimation: a single scalar value representing the estimated fish length in centimeters.

## Scoring recipe

```python
def compute_mAP(predictions, ground_truth):
    ious = compute_iou(predictions, ground_truth)
    aps = []
    for iou_thresh in np.arange(0.5, 0.96, 0.05):
        aps.append(compute_ap(ious, threshold=iou_thresh))
    return np.mean(aps)

def compute_mae_mape(pred_lengths, true_lengths):
    mae = np.mean(np.abs(pred_lengths - true_lengths))
    mape = np.mean(np.abs((pred_lengths - true_lengths) / true_lengths)) * 100
    return mae, mape
```

## Common pitfalls

- Splits are defined by experimental groups rather than random image shuffling to prevent cross-contamination of fish specimens across train/val/test.
- Length estimation using predicted masks requires a 0.9 confidence threshold; lower thresholds introduce noisy masks that significantly degrade MAE.
- Performance drops sharply when fish are touching or occluded, especially for skeletonization-based length methods compared to CNN regression.

## Evidence (verbatim from paper)

> The performance of our instance segmentation models are evaluated based on the mean average precision, which is calculated as $mAP\=AP@[IoU\=.5:.95]$ by thresholding the intersection over union (IoU) between the predictions and the ground truth annotations in steps of 0.05. The length estimation methods are evaluated based on the mean absolute error (MAE) in centimeters and the mean absolute percentage error (MAPE).

## Citation

```bibtex
@misc{bengtson2025autofish,
  title={AutoFish: Dataset and Benchmark for Fine-grained Analysis of Fish},
  author={Bengtson et al. (2025)},
  year={2025},
  note={arXiv:2501.03767}
}
```

- arXiv: 2501.03767
