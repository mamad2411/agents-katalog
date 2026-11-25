---
name: ade20k-scene-parse-eval
description: Evaluates a model's ability to perform dense pixel-wise semantic segmentation across 150 common scene categories, including both discrete objects and amorphous 'stuff' classes. It probes fine-grained scene understanding and the model's capacity to handle class imbalance and varying object scales. Use when the user wants to benchmark on SceneParse150, or asks about evaluating this task. Reports Mean IoU.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1608.05442
  bibtex_key: zhou2016ade20k
  confidence: high
---

# ade20k-scene-parse-eval

> Semantic Understanding of Scenes through the ADE20K Dataset — Zhou et al. (2016) (arXiv:1608.05442, 2016)

## What this evaluates

Evaluates a model's ability to perform dense pixel-wise semantic segmentation across 150 common scene categories, including both discrete objects and amorphous 'stuff' classes. It probes fine-grained scene understanding and the model's capacity to handle class imbalance and varying object scales.

## Datasets

- **SceneParse150** — total ?; splits: validation (-1); repo http://sceneparsing.csail.mit.edu

## Metrics

- `Mean IoU` **(primary)** — range: [0, 1]
  - Intersection-over-union between predicted and ground-truth pixels, averaged over all 150 classes.
- `Pixel accuracy` — range: percent
  - Proportion of correctly classified pixels across the entire image.
- `Mean accuracy` — range: percent
  - Proportion of correctly classified pixels averaged over all classes.
- `Weighted IoU` — range: [0, 1]
  - IoU weighted by the total pixel ratio of each class.

## Input / output format

**Input**: RGB images (rescaled so minimum height/width is 512 pixels for SceneParse150)

**Output**: Per-pixel class label predictions (150 classes) or instance segmentation masks

## Scoring recipe

```python
def compute_mean_iou(preds, gold, num_classes=150):
    ious = []
    for c in range(num_classes):
        pred_c = (preds == c)
        gold_c = (gold == c)
        intersection = np.sum(pred_c & gold_c)
        union = np.sum(pred_c | gold_c)
        ious.append(intersection / union if union > 0 else 1.0)
    return np.mean(ious)
```

## Common pitfalls

- Pixel accuracy is heavily biased toward large background classes (e.g., walls, floors), making Mean IoU the preferred metric for class-wise performance.
- Batch normalization size and synchronization critically impact scores; unsynchronized BN or small batch sizes (e.g., 2) can drop Mean IoU by ~5%.
- Results in Table 3 use multi-scale testing, while Table 4 explicitly states results are obtained without it, affecting direct comparability.

## Evidence (verbatim from paper)

> Results are reported in four metrics commonly used for semantic segmentation: Pixel accuracy indicates the proportion of correctly classified pixels; Mean accuracy indicates the proportion of correctly classified pixels averaged over all the classes. Mean IoU indicates the intersection-over-union between the predicted and ground-truth pixels, averaged over all the classes. Weighted IoU indicates the IoU weighted by the total pixel ratio of each class.

## Citation

```bibtex
@misc{zhou2016ade20k,
  title={Semantic Understanding of Scenes through the ADE20K Dataset},
  author={Zhou et al. (2016)},
  year={2016},
  note={arXiv:1608.05442}
}
```

- arXiv: 1608.05442
