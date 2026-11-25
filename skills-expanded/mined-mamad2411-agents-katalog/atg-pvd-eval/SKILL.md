---
name: atg-pvd-eval
description: Evaluates a drone-based suspect-and-investigate system for detecting and classifying illegally parked cars, moving cars, and legally parked cars from aerial imagery. Use when the user wants to benchmark on ATG-PVD, or asks about evaluating this task. Reports mAP.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2008.09305
  bibtex_key: wang2020atgpvd
  confidence: high
---

# atg-pvd-eval

> ATG-PVD: Ticketing Parking Violations on A Drone — Wang et al. (2020) (arXiv:2008.09305, 2020)

## What this evaluates

Evaluates a drone-based suspect-and-investigate system for detecting and classifying illegally parked cars, moving cars, and legally parked cars from aerial imagery.

## Datasets

- **ATG-PVD** — total 9322; splits: train (4924), test (4398); repo https://sites.google.com/view/atg-pvd

## Metrics

- `mAP` **(primary)** — range: [0, 1]
  - Mean Average Precision computed over ten IoU thresholds ranging from 0.50 to 0.95, averaged across three classes (IPC candidate, MC, LPC).
- `F1-Score` — range: [0, 1]
  - Harmonic mean of precision and recall for the end-to-end parking violation detection system.

## Input / output format

**Input**: RGB images captured by a drone camera, downsampled to 540x960 pixels, along with corresponding optical flow features.

**Output**: 2D bounding boxes with class predictions (IPC candidate, moving car, legally parked car) and a binary violation detection decision.

## Scoring recipe

```python
def compute_mAP(predictions, ground_truth, iou_thresholds=np.linspace(0.50, 0.95, 10)):
    ap_scores = []
    for iou in iou_thresholds:
        tp, fp = 0, 0
        for pred, gt in zip(predictions, ground_truth):
            if max_iou(pred, gt) >= iou: tp += 1
            else: fp += 1
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / len(ground_truth)
        ap_scores.append(interpolate_ap(precision, recall))
    return np.mean(ap_scores)

def compute_f1(precision, recall):
    return 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
```

## Common pitfalls

- IPCs are labeled as IPC candidates in both training and testing phases due to the re-identification requirement.
- All experiments are run on downsampled images (540x960) rather than the native 2160x3840 resolution.
- The optical flow module (SwiftFlow) is evaluated on KITTI benchmarks, not the ATG-PVD dataset, because ATG-PVD lacks flow ground truth.

## Evidence (verbatim from paper)

> In our experiments, we divide our ATG-PVD dataset into a training set and a testing set, which respectively contains 4924 and 4398 images. In our experiments, we compute the mean average precision (mAP) over ten IoU thresholds between 0.50 and 0.95 to quantitatively evaluate the performance of our proposed Flow-RCNN. We also comprehensively evaluate the performance of the entire system for parking violation detection using our ATG-PVD dataset, and a precision of 91.7%, a recall of 94.9% and an F1-Score of 93.3% are achieved.

## Citation

```bibtex
@misc{wang2020atgpvd,
  title={ATG-PVD: Ticketing Parking Violations on A Drone},
  author={Wang et al. (2020)},
  year={2020},
  note={arXiv:2008.09305}
}
```

- arXiv: 2008.09305
