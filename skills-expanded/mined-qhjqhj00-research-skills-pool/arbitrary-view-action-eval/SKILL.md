---
name: arbitrary-view-action-eval
description: Evaluates human action recognition models under varying camera viewpoints and different subjects. It probes the model's ability to generalize across unseen subjects, unseen camera angles, and continuous 360-degree view changes. Use when the user wants to benchmark on Varying-view RGB-D Action Dataset, or asks about evaluating this task. Reports average recognition accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1904.10681
  bibtex_key: ji2019large
  confidence: high
---

# arbitrary-view-action-eval

> A Large-scale Varying-view RGB-D Action Dataset for Arbitrary-view Human Action Recognition — Ji et al. (2019) (arXiv:1904.10681, 2019)

## What this evaluates

Evaluates human action recognition models under varying camera viewpoints and different subjects. It probes the model's ability to generalize across unseen subjects, unseen camera angles, and continuous 360-degree view changes.

## Datasets

- **Varying-view RGB-D Action Dataset** — total 25600; splits: train (-1), test (-1); repo https://github.com/HRI-UESTC/CFM-HRI-RGB-D-action-database

## Metrics

- `average recognition accuracy` **(primary)** — range: percent
  - The proportion of correctly classified action sequences out of the total number of test sequences. Reported per viewpoint or evaluation setting, then averaged across all test samples.

## Input / output format

**Input**: RGB video frames, depth sequences, or 3D skeleton joint coordinates. Sequences are uniformly sampled to 20 frames for RGB/depth and 40 frames for skeleton data.

**Output**: Predicted action class label.

## Scoring recipe

```python
def calculate_accuracy(predictions, gold_labels):
    correct = sum(1 for p, g in zip(predictions, gold_labels) if p == g)
    return correct / len(gold_labels)
```

## Common pitfalls

- Viewpoints 3 and 5 suffer from heavy occlusions, causing systematically lower accuracy that reflects data quality rather than model capability.
- The dataset supports three modalities (RGB, depth, skeleton) with vastly different performance baselines; comparing raw accuracy across modalities is misleading.
- Cross-view evaluations use fixed viewpoint groupings rather than random splits, making results highly sensitive to the specific camera angle configuration.

## Evidence (verbatim from paper)

> In experiments, the average recognition accuracy is recorded for the comparison of performance.

## Citation

```bibtex
@misc{ji2019large,
  title={A Large-scale Varying-view RGB-D Action Dataset for Arbitrary-view Human Action Recognition},
  author={Ji et al. (2019)},
  year={2019},
  note={arXiv:1904.10681}
}
```

- arXiv: 1904.10681
