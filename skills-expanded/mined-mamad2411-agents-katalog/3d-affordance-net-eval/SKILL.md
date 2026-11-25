---
name: 3d-affordance-net-eval
description: Evaluates 3D point cloud networks on visual object affordance understanding. It probes the model's ability to predict point-wise probabilistic scores for 18 affordance classes given full, partial, or rotated 3D shapes. Use when the user wants to benchmark on 3D AffordanceNet, or asks about evaluating this task. Reports mAP.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2103.16397
  bibtex_key: deng20213daffordancenet
  confidence: high
---

# 3d-affordance-net-eval

> 3D AffordanceNet: A Benchmark for Visual Object Affordance Understanding — Deng et al. (2021) (arXiv:2103.16397, 2021)

## What this evaluates

Evaluates 3D point cloud networks on visual object affordance understanding. It probes the model's ability to predict point-wise probabilistic scores for 18 affordance classes given full, partial, or rotated 3D shapes.

## Datasets

- **3D AffordanceNet** — total 23000; splits: train (-1), val (-1), test (-1)

## Metrics

- `mAP` **(primary)** — range: [0, 1]
  - Calculates Precision-Recall Curve and computes Average Precision (AP) for each affordance category, then macro-averaged over all shapes.
- `MSE` — range: [0, 1]
  - Mean squared error of predicted vs ground truth scores per affordance category, summed across categories.
- `AUC` — range: [0, 1]
  - Area under the Receiver Operating Characteristic curve for each affordance category, macro-averaged.
- `aIoU` — range: [0, 1]
  - Averaged Intersection Over Union across thresholds from 0 to 0.99 (step 0.01) after binarizing predictions and ground truth at 0.5 threshold.

## Input / output format

**Input**: 3D point cloud representing an object (full, partial, or rotated).

**Output**: Point-wise probabilistic score for each of the 18 affordance categories.

## Scoring recipe

```python
def compute_metrics(pred_scores, gt_scores, num_classes=18):
    gt_bin = (gt_scores >= 0.5).astype(float)
    ious = []
    for thresh in np.arange(0, 0.99, 0.01):
        pred_bin_t = (pred_scores >= thresh).astype(float)
        intersection = np.sum(pred_bin_t * gt_bin, axis=0)
        union = np.sum(pred_bin_t + gt_bin, axis=0)
        ious.append(np.mean(intersection / (union + 1e-8)))
    aIoU = np.mean(ious)
    mAP = compute_ap_per_class(pred_scores, gt_scores)
    AUC = compute_auc_per_class(pred_scores, gt_scores)
    MSE = np.mean((pred_scores - gt_scores)**2)
    return {'mAP': mAP, 'MSE': MSE, 'AUC': AUC, 'aIoU': aIoU}
```

## Common pitfalls

- Ground truth maps are binarized with a 0.5 threshold before evaluation for aIoU and other metrics.
- Metrics are macro-averaged over all shapes, except MSE which is summed across categories.
- Partial-view and rotation-invariant tasks use synthesized partial point clouds and rotated inputs respectively.

## Evidence (verbatim from paper)

> We evaluate four metrics for affordance estimation, including mean Average Precision (mAP) scores, mean squared error (MSE), Area Under ROC Curve (AUC) and average Intersection Over Union (aIoU). For AP, we calculate the Precision-Recall Curve and AP is calculated for each affordance. For AUC, we report the area under ROC Curve. For MSE, we calculate mean squared error of each affordance category and sum up the results from all affordance categories. For aIoU, we gradually tune up the threshold from 0 to 0.99 with 0.01 step to binarize the prediction, and the aIoU is the arithmetic average of all IoUs at each threshold. Except for the MSE, all the other metrics for each category are averaged over all shapes, a.k.a. macro-average. For each affordance category, the groundtruth map is binarized with 0.5 threshold before evaluation.

## Citation

```bibtex
@misc{deng20213daffordancenet,
  title={3D AffordanceNet: A Benchmark for Visual Object Affordance Understanding},
  author={Deng et al. (2021)},
  year={2021},
  note={arXiv:2103.16397}
}
```

- arXiv: 2103.16397
