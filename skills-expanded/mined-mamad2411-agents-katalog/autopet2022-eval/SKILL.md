---
name: autopet2022-eval
description: Evaluates the capability of 3D medical image segmentation models to accurately delineate lesions in whole-body FDG-PET/CT scans. It probes the model's ability to handle high-resolution volumetric data and distinguish pathological regions from healthy tissue. Use when the user wants to benchmark on autoPET 2022, or asks about evaluating this task. Reports DSC.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2210.07490
  bibtex_key: ye2022exploring
  confidence: high
---

# autopet2022-eval

> Exploring Vanilla U-Net for Lesion Segmentation from Whole-body FDG-PET/CT Scans — Ye et al. (2022) (arXiv:2210.07490, 2022)

## What this evaluates

Evaluates the capability of 3D medical image segmentation models to accurately delineate lesions in whole-body FDG-PET/CT scans. It probes the model's ability to handle high-resolution volumetric data and distinguish pathological regions from healthy tissue.

## Datasets

- **autoPET 2022** — total ?; splits: preliminary test (-1), final test (-1), validation (103)

## Metrics

- `DSC` **(primary)** — range: [0, 1]
  - Dice Similarity Coefficient: 2 * |A ∩ B| / (|A| + |B|), where A and B are the predicted and ground truth lesion masks.
- `FPV` — range: other
  - False Positive Volume: number of voxels predicted as lesion but belonging to healthy tissue.
- `FNV` — range: other
  - False Negative Volume: number of voxels belonging to the ground truth lesion but missed by the prediction.

## Input / output format

**Input**: 3D volumetric FDG-PET/CT image patches (typically cropped to 192×192×192 during training) with original or resampled spacing.

**Output**: 3D binary segmentation mask indicating lesion voxels.

## Scoring recipe

```python
def compute_metrics(pred_mask, gt_mask):
    intersection = np.sum(pred_mask & gt_mask)
    union = np.sum(pred_mask) + np.sum(gt_mask)
    dsc = 2 * intersection / union if union > 0 else 0.0
    fpv = np.sum(pred_mask & ~gt_mask)
    fnv = np.sum(~pred_mask & gt_mask)
    return dsc, fpv, fnv
```

## Common pitfalls

- DSC is insensitive to spatial localization errors when lesion volumes are small; FPV and FNV must be reported alongside it.
- Inference step size and crop dimensions heavily influence FPV/FNV trade-offs without significantly altering DSC scores.
- The challenge uses a hidden final test set; preliminary leaderboard rankings do not guarantee final placement due to different evaluation splits.

## Evidence (verbatim from paper)

> The vanilla U-Net outperforms other architectures for DSC and FPV on the preliminary test set.

## Citation

```bibtex
@misc{ye2022exploring,
  title={Exploring Vanilla U-Net for Lesion Segmentation from Whole-body FDG-PET/CT Scans},
  author={Ye et al. (2022)},
  year={2022},
  note={arXiv:2210.07490}
}
```

- arXiv: 2210.07490
