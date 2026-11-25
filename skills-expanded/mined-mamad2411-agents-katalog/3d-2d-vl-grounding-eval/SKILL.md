---
name: 3d-2d-vl-grounding-eval
description: Evaluates a unified vision-language model's ability to ground natural language instructions to 3D objects and 2D regions, as well as answer 3D visual questions. It probes spatial reasoning, cross-modal alignment, and robustness to different 3D input representations (mesh-sampled vs. sensor RGB-D point clouds). Use when the user wants to benchmark on SR3D, NR3D, ScanRefer, RefCOCO, RefCOCO+, RefCOCOg, ScanQA, SQA3D, or asks about evaluating this task. Reports top-1 accuracy (Acc@25/50/75).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2503.10745
  bibtex_key: jain2025unifying
  confidence: high
---

# 3d-2d-vl-grounding-eval

> Unifying 2D and 3D Vision-Language Understanding — Ayush Jain et al. (2025) (arXiv:2503.10745, 2025)

## What this evaluates

Evaluates a unified vision-language model's ability to ground natural language instructions to 3D objects and 2D regions, as well as answer 3D visual questions. It probes spatial reasoning, cross-modal alignment, and robustness to different 3D input representations (mesh-sampled vs. sensor RGB-D point clouds).

## Datasets

- **SR3D** — total ?; splits: val (-1)
- **NR3D** — total ?; splits: val (-1)
- **ScanRefer** — total ?; splits: val (-1)
- **RefCOCO** — total ?; splits: val (-1)
- **RefCOCO+** — total ?; splits: val (-1)
- **RefCOCOg** — total ?; splits: val (-1)
- **ScanQA** — total ?; splits: val (-1)
- **SQA3D** — total ?; splits: val (-1)

## Metrics

- `top-1 accuracy (Acc@25/50/75)` **(primary)** — range: percent
  - Top-1 accuracy computed at IoU thresholds of 0.25, 0.5, and 0.75. A prediction is correct if the IoU between the predicted bounding box (derived from mask extents) and the ground-truth box exceeds the threshold. For the GT setup, correctness is determined by selecting the correct pooled feature token.
- `exact-match accuracy (EM@1)` — range: percent
  - Measures whether the generated text answer exactly matches one of the provided ground-truth answer candidates (1 for SQA3D, 2 for ScanQA).

## Input / output format

**Input**: 3D point clouds (either mesh-sampled or sensor RGB-D unprojected) paired with natural language instructions/queries; or 2D images paired with language instructions.

**Output**: Predicted segmentation masks (converted to bounding boxes via extents) for grounding tasks; or generated text answers for VQA tasks.

## Scoring recipe

```python
def compute_accuracy(preds, golds, iou_threshold=0.25):
    correct = 0
    for pred, gold in zip(preds, golds):
        pred_box = get_bbox_from_mask(pred)
        iou = intersection_over_union(pred_box, gold)
        if iou >= iou_threshold:
            correct += 1
    return correct / len(golds)

def compute_em(preds, golds):
    matches = sum(1 for p, g in zip(preds, golds) if p in g)
    return matches / len(golds)
```

## Common pitfalls

- Confusing the GT setup (uses ground-truth object proposals) with the Det setup (requires object detection without GT boxes), which drastically changes the difficulty and reported accuracy.
- Mesh-sampled point clouds are standard in benchmarks but misalign with real sensor data, unfairly penalizing sensor-based methods; evaluations should explicitly note input type.
- Mask decoding relies on dot-products with visual tokens, while box decoding regresses coordinates; comparing them directly without accounting for this architectural difference is misleading.

## Evidence (verbatim from paper)

> We use the standard top-1 accuracy metric. For the Det setup, a predicted bounding box is considered correct if its intersection over union (IoU) with the ground truth box is higher than a predetermined threshold (we use the standard 0.25, 0.5 and 0.75). As UniVLG predicts masks (instead of axis-aligned bounding boxes), we obtain a bounding box by taking the extents of the mask.

## Citation

```bibtex
@misc{jain2025unifying,
  title={Unifying 2D and 3D Vision-Language Understanding},
  author={Ayush Jain et al. (2025)},
  year={2025},
  note={arXiv:2503.10745}
}
```

- arXiv: 2503.10745
