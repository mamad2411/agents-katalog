---
name: attrseg-ovss-eval
description: This evaluation probes a model's ability to perform open-vocabulary semantic segmentation using either direct class names or decomposed attribute descriptions. It specifically tests robustness to textual ambiguity, neologisms, and unnameable categories by measuring pixel-level alignment across standard and novel datasets. Use when the user wants to benchmark on PASCAL-5i, COCO-20i, PASCAL VOC, PASCAL Context, Fantastic Beasts, or asks about evaluating this task. Reports mIoU.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2309.00096
  bibtex_key: ma2023attrseg
  confidence: high
---

# attrseg-ovss-eval

> AttrSeg: Open-Vocabulary Semantic Segmentation via Attribute Decomposition-Aggregation — Chaofan Ma et al. (2023) (arXiv:2309.00096, 2023)

## What this evaluates

This evaluation probes a model's ability to perform open-vocabulary semantic segmentation using either direct class names or decomposed attribute descriptions. It specifically tests robustness to textual ambiguity, neologisms, and unnameable categories by measuring pixel-level alignment across standard and novel datasets.

## Datasets

- **PASCAL-5i** — total ?; splits: val (-1)
- **COCO-20i** — total ?; splits: val (-1)
- **PASCAL VOC** — total ?; splits: val (1500)
- **PASCAL Context** — total ?; splits: val (5000)
- **Fantastic Beasts** — total ?; splits: test (-1)

## Metrics

- `mIoU` **(primary)** — range: percent
  - Mean Intersection-over-Union: the average of the IoU (intersection over union) computed for each semantic class across the dataset. IoU for a class is the number of correctly predicted pixels for that class divided by the union of predicted and ground truth pixels for that class.

## Input / output format

**Input**: RGB image paired with a textual prompt consisting of either a single class name or a set of decomposed attribute descriptions.

**Output**: Per-pixel semantic segmentation mask assigning one of the K class labels (or background) to each pixel.

## Scoring recipe

```python
def compute_miou(pred_masks, gt_masks, num_classes):
    ious = []
    for c in range(num_classes):
        pred_c = (pred_masks == c)
        gt_c = (gt_masks == c)
        intersection = np.logical_and(pred_c, gt_c).sum()
        union = np.logical_or(pred_c, gt_c).sum()
        ious.append(intersection / union if union > 0 else 0.0)
    return np.mean(ious) * 100
```

## Common pitfalls

- Results vary significantly across the 4 folds of PASCAL-5i and COCO-20i; reporting only a single fold is insufficient and misrepresents performance.
- Baseline comparisons are highly sensitive to training data (e.g., PASCAL VOC-15 vs COCO-Stuff), making direct mIoU comparisons across tables misleading without noting training splits.
- Models trained on class names often fail on attribute-only inputs, so evaluation must explicitly state the textual input modality to avoid unfair comparisons.

## Evidence (verbatim from paper)

> We report mean intersection-over-union (mIoU), following the recent open-vocabulary semantic segmentation (OVSS) literatures. PASCAL-5i contains 20 categories that are divided into 4 folds of 5 classes each, i.e., ${5^{i}}_{i\=0}^{3}$. COCO-20i is more challenging with 80 categories that are also divided into 4 folds, i.e., ${20^{i}}_{i\=0}^{3}$, with each fold having 20 categories. Of the four folds in the two datasets, one is used for evaluation, while the other three are used for training. PASCAL VOC is a classical dataset. We evaluate on the 1.5k validation images with 20 categories (PAS-20). PASCAL-Context contains 5k validation images. We evaluate on the most frequent used 59 classes version (PC-59).

## Citation

```bibtex
@misc{ma2023attrseg,
  title={AttrSeg: Open-Vocabulary Semantic Segmentation via Attribute Decomposition-Aggregation},
  author={Chaofan Ma et al. (2023)},
  year={2023},
  note={arXiv:2309.00096}
}
```

- arXiv: 2309.00096
