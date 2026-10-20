---
name: amodal-optical-flow-eval
description: Evaluates a model's ability to predict multi-layered pixel-level motion fields that explicitly account for both visible and occluded regions of objects (amodal optical flow), along with associated masks and semantic labels. It also assesses the utility of these predictions for downstream panoptic tracking. Use when the user wants to benchmark on AmodalSynthDrive, or asks about evaluating this task. Reports AFQ.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2311.07761
  bibtex_key: luz2023amodalfow
  confidence: high
---

# amodal-optical-flow-eval

> Amodal Optical Flow — Luz et al. (2023) (arXiv:2311.07761, 2023)

## What this evaluates

Evaluates a model's ability to predict multi-layered pixel-level motion fields that explicitly account for both visible and occluded regions of objects (amodal optical flow), along with associated masks and semantic labels. It also assesses the utility of these predictions for downstream panoptic tracking.

## Datasets

- **AmodalSynthDrive** — total ?; splits: val (-1), test (-1)

## Metrics

- `AFQ` **(primary)** — range: percent
  - Amodal Flow Quality metric. Specific mathematical formulation is not provided in the text, but it serves as the headline score for evaluating multi-layer amodal optical flow predictions.
- `mWAUC` — range: percent
  - Mean Weighted Area Under Curve metric used to evaluate pure optical flow performance.
- `mIoU` — range: percent
  - Mean Intersection over Union metric used to evaluate mask and semantic prediction accuracy.
- `PAT` — range: percent
  - Panoptic Tracking metric that combines Panoptic Quality (PQ) and Tracking Quality (TQ) to assess object association performance across consecutive frames.

## Input / output format

**Input**: Paired consecutive synthetic driving video frames containing visible and occluded objects.

**Output**: Multi-layered pixel-level amodal optical flow vectors, corresponding amodal masks, and semantic labels for each object layer.

## Scoring recipe

```python
def evaluate(predictions, gold):
    # predictions and gold contain flow, masks, semantics, and tracking IDs
    afq = compute_afq(predictions['flow'], gold['flow'])
    mwauc = compute_mwauc(predictions['flow'], gold['flow'])
    miou = compute_miou(predictions['masks'], gold['masks'])
    pat = compute_pat(predictions['tracking_ids'], gold['tracking_ids'])
    return {'AFQ': afq, 'mWAUC': mwauc, 'mIoU': miou, 'PAT': pat}
# Evaluated on val and test splits of AmodalSynthDrive using 4 recurrent refinement steps.
```

## Common pitfalls

- Confusing modal (visible-only) optical flow with amodal flow, which requires reasoning about object continuity behind occlusions.
- Assuming standard flow benchmarks like Sintel directly transfer to amodal tasks without adapting to multi-layer predictions and occlusion handling.
- Overlooking that the PQ component of the PAT metric remains constant across modal/amodal variants because the underlying segmentation network is fixed.

## Evidence (verbatim from paper)

> AmodalFlowNet achieves an additional 20% (6.7 pp) improvement in AFQ over AmodalGMA on the test split.

## Citation

```bibtex
@misc{luz2023amodalfow,
  title={Amodal Optical Flow},
  author={Luz et al. (2023)},
  year={2023},
  note={arXiv:2311.07761}
}
```

- arXiv: 2311.07761
