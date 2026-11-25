---
name: aerial-d-res-eval
description: This benchmark evaluates a model's ability to perform referring expression segmentation on aerial imagery, testing its capacity to localize objects or regions based on natural language instructions. It specifically probes robustness to domain-specific challenges such as densely packed targets, varying object scales, and simulated historical image degradation (monochrome, sepia, and grainy conditions). Use when the user wants to benchmark on Aerial-D, RRSIS-D, NWPU-Refer, RefSegRS, Urban1960SatSeg, or asks about evaluating this task. Reports mIoU.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2512.07338
  bibtex_key: marnoto2025aerialrefseg
  confidence: high
---

# aerial-d-res-eval

> Generalized Referring Expression Segmentation on Aerial Photos — Marnoto et al. (2025) (arXiv:2512.07338, 2025)

## What this evaluates

This benchmark evaluates a model's ability to perform referring expression segmentation on aerial imagery, testing its capacity to localize objects or regions based on natural language instructions. It specifically probes robustness to domain-specific challenges such as densely packed targets, varying object scales, and simulated historical image degradation (monochrome, sepia, and grainy conditions).

## Datasets

- **Aerial-D** — total 37288; splits: train (1117794), test (404729)
- **RRSIS-D** — total 17402; splits: test (-1)
- **NWPU-Refer** — total 15003; splits: test (-1)
- **RefSegRS** — total 4420; splits: test (-1)
- **Urban1960SatSeg** — total ?; splits: test (-1)

## Metrics

- `mIoU` **(primary)** — range: [0, 1]
  - Mean Intersection over Union computed across all test expressions. For each expression, IoU is calculated between the predicted mask and ground-truth mask; the final score is the arithmetic mean of these IoUs.

## Input / output format

**Input**: RGB aerial image paired with a natural language referring expression describing a target object or region.

**Output**: A segmentation mask (binary or instance-level) matching the input image dimensions, indicating the pixels belonging to the described target.

## Scoring recipe

```python
ious = []
for pred, gold in zip(predictions, ground_truth):
    inter = np.logical_and(pred, gold).sum()
    union = np.logical_or(pred, gold).sum()
    ious.append(inter / union if union > 0 else 1.0)
return np.mean(ious)
```

## Common pitfalls

- Overwhelming the model with Aerial-D's massive expression count if not balanced with other datasets during training, which can dominate gradients.
- Evaluating historic/filtered test sets without applying the exact same filter (grayscale, grain, sepia) to all images in the benchmark.
- Mixing up instance-level and semantic-level target evaluations, as the test split is explicitly divided into these two categories.

## Evidence (verbatim from paper)

> Model testing follows the original dataset splits, and Aerial-D relies on the full test split (405K expressions), which is further broken down into instance targets and semantic regions, as shown in Table III. To probe robustness we also evaluate fully filtered test sets for Aerial-D, RRSIS-D, NWPU-Refer, and RefSegRS, by converting every image with one of the three historic filters. Historic scores appear in italics alongside the original scores.

## Citation

```bibtex
@misc{marnoto2025aerialrefseg,
  title={Generalized Referring Expression Segmentation on Aerial Photos},
  author={Marnoto et al. (2025)},
  year={2025},
  note={arXiv:2512.07338}
}
```

- arXiv: 2512.07338
