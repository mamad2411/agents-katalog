---
name: baboonland-eval
description: This benchmark evaluates computer vision models on three core tasks using drone footage of wild baboons: object detection, multi-object tracking, and fine-grained behavioral recognition. It probes a model's ability to handle extreme scale variation, heavy occlusion, and temporal context in natural, uncontrolled wildlife environments. Use when the user wants to benchmark on BaboonLand, or asks about evaluating this task. Reports Top-1 accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2405.17698
  bibtex_key: duporge2024baboonland
  confidence: high
---

# baboonland-eval

> BaboonLand Dataset: Tracking Primates in the Wild and Automating Behaviour Recognition from Drone Videos — Duporge et al. (2024) (arXiv:2405.17698, 2024)

## What this evaluates

This benchmark evaluates computer vision models on three core tasks using drone footage of wild baboons: object detection, multi-object tracking, and fine-grained behavioral recognition. It probes a model's ability to handle extreme scale variation, heavy occlusion, and temporal context in natural, uncontrolled wildlife environments.

## Datasets

- **BaboonLand** — total ?; splits: train (-1), val (-1), test (-1)

## Metrics

- `Top-1 accuracy` **(primary)** — range: percent
  - Percentage of correctly predicted behavioral categories out of total instances. Reported as both micro-average (per instance) and macro-average (per class) across 12 behavioral categories.
- `mAP@50` — range: percent
  - Mean Average Precision at Intersection over Union (IoU) threshold of 0.5. Averages the precision-recall curve for each class.
- `MOTA` — range: percent
  - Multiple Object Tracking Accuracy, measuring tracking correctness by penalizing false positives, false negatives, and identity switches relative to ground truth trajectories.

## Input / output format

**Input**: Drone video frames or short video clips (typically 16 frames sampled at rate 5) containing baboons in natural environments. Detection/tracking tasks utilize tiled multi-scale image pyramids (2x2, 3x3, 4x4) to handle small object sizes.

**Output**: Bounding boxes with class labels for detection/tracking, or discrete behavioral category labels (e.g., 'Sitting/Standing', 'Drinking', 'Foraging') for behavior recognition.

## Scoring recipe

```python
def compute_top1_accuracy(predictions, gold_labels, average='micro'):
    if average == 'micro':
        return sum(p == g for p, g in zip(predictions, gold_labels)) / len(gold_labels)
    else:  # macro
        classes = set(gold_labels)
        class_accs = [sum(p == g for p, g in zip(predictions, gold_labels) if g == c) / sum(1 for g in gold_labels if g == c) for c in classes]
        return sum(class_accs) / len(class_accs)
```

## Common pitfalls

- Rare behavioral categories are significantly harder to recognize than frequent ones, leading to skewed macro-averaged performance.
- Visual similarity between certain actions (e.g., Drinking, Foraging, Mounting) causes models to default to predicting 'Sitting/Standing'.
- Small object scale in raw drone footage requires a tiled multi-scale pyramid approach; evaluating on raw full-resolution frames without tiling yields poor detection.

## Evidence (verbatim from paper)

> To provide the baseline for behavior recognition, we trained I3D*[[60]], SlowFast*[[61]], and X3D*[[62]] models on our dataset. We report micro (per instance) average and macro (per class) average accuracy. The confusion matrix depicted in [Fig. 3] demonstrates the performance of the X3D model. We can see that the model performs quite well for common classes but rare behaviors are more challenging.

## Citation

```bibtex
@misc{duporge2024baboonland,
  title={BaboonLand Dataset: Tracking Primates in the Wild and Automating Behaviour Recognition from Drone Videos},
  author={Duporge et al. (2024)},
  year={2024},
  note={arXiv:2405.17698}
}
```

- arXiv: 2405.17698
