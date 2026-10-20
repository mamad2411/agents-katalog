---
name: 3d-obj-det-seg-eval
description: Evaluates a model's ability to detect and segment 3D objects in indoor scenes using point cloud inputs. It probes spatial reasoning and instance-level understanding by measuring how well the model generalizes from synthetic internet-scale data to real-world scanned environments. Use when the user wants to benchmark on ScanNet, SceneVerse++, or asks about evaluating this task. Reports AP.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2604.01907
  bibtex_key: chen2026lifting
  confidence: high
---

# 3d-obj-det-seg-eval

> Lifting Unlabeled Internet-level Data for 3D Scene Understanding — Chen et al. (2026) (arXiv:2604.01907, 2026)

## What this evaluates

Evaluates a model's ability to detect and segment 3D objects in indoor scenes using point cloud inputs. It probes spatial reasoning and instance-level understanding by measuring how well the model generalizes from synthetic internet-scale data to real-world scanned environments.

## Datasets

- **ScanNet** — total ?; splits: test (-1); repo https://github.com/ScanNet/ScanNet
- **SceneVerse++** — total ?; splits: train (-1)

## Metrics

- `AP25` — range: [0, 1]
  - Average Precision at Intersection over Union (IoU) threshold of 0.25.
- `AP50` — range: [0, 1]
  - Average Precision at IoU threshold of 0.50.
- `AP` **(primary)** — range: [0, 1]
  - Average Precision averaged across IoU thresholds from 0.25 to 0.75 in 0.05 increments.

## Input / output format

**Input**: 3D point clouds (often cropped to a 3-meter radius around a target object) with optional graph-based segmentation masks.

**Output**: Bounding boxes and instance segmentation masks for 15 semantic categories.

## Scoring recipe

```python
for each scene:
  preds = model.predict(point_cloud)
  for each pred_box:
    match with ground_truth_box
    if IoU(pred, gt) >= threshold:
      mark as true positive
  compute precision-recall curve
  interpolate AP at 101 recall levels
return mean AP across categories
```

## Common pitfalls

- Model performance is highly sensitive to the hyperparameters of the graph-based segmentation method (kThresh, segMinVerts) used to generate input segments.
- Distribution shift between synthetic training data (SceneVerse++) and real scanned data (ScanNet) causes significant performance degradation if not carefully managed.

## Evidence (verbatim from paper)

> The AP is reported as the average over the whole ScanNet.

## Citation

```bibtex
@misc{chen2026lifting,
  title={Lifting Unlabeled Internet-level Data for 3D Scene Understanding},
  author={Chen et al. (2026)},
  year={2026},
  note={arXiv:2604.01907}
}
```

- arXiv: 2604.01907
