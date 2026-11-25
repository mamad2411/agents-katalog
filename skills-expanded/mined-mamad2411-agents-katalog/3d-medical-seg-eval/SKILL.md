---
name: 3d-medical-seg-eval
description: Evaluates the segmentation performance of various 3D medical image architectures across multiple public datasets. It probes whether newer architectures genuinely outperform established U-Net baselines when trained under standardized, hardware-scaled conditions without external advantages like ensembling or pretraining. Use when the user wants to benchmark on BTCV, ACDC, LiTS, BraTS, KiTS, AMOS, or asks about evaluating this task. Reports DSC score [%].
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2404.09556
  bibtex_key: isensee2024nnunet
  confidence: high
---

# 3d-medical-seg-eval

> nnU-Net Revisited: A Call for Rigorous Validation in 3D Medical Image Segmentation — Isensee et al. (2024) (arXiv:2404.09556, 2024)

## What this evaluates

Evaluates the segmentation performance of various 3D medical image architectures across multiple public datasets. It probes whether newer architectures genuinely outperform established U-Net baselines when trained under standardized, hardware-scaled conditions without external advantages like ensembling or pretraining.

## Datasets

- **BTCV** — total 30; splits: test (-1)
- **ACDC** — total 200; splits: test (-1)
- **LiTS** — total 131; splits: test (-1)
- **BraTS** — total 1251; splits: test (-1)
- **KiTS** — total 489; splits: test (-1)
- **AMOS** — total 360; splits: test (-1)

## Metrics

- `DSC score [%]` **(primary)** — range: percent
  - Dice Similarity Coefficient: 2 * |A ∩ B| / (|A| + |B|), where A and B are the predicted and ground truth segmentation masks. Computed per case and averaged across the dataset.

## Input / output format

**Input**: 3D volumetric medical images (CT/MRI scans) with corresponding ground truth segmentation masks.

**Output**: Predicted 3D segmentation masks (binary or multi-class voxel labels) for each input volume.

## Scoring recipe

```python
def compute_dsc(pred, gt):
    intersection = np.sum(pred & gt)
    union = np.sum(pred) + np.sum(gt)
    return 2.0 * intersection / union if union > 0 else 0.0
scores = [compute_dsc(p, g) for p, g in zip(predictions, ground_truths)]
return np.mean(scores) * 100
```

## Common pitfalls

- Comparing models with vastly different compute budgets or sizes without scaling baselines appropriately.
- Overreliance on saturated datasets (e.g., BraTS) or noisy datasets (e.g., BTCV) that fail to differentiate methods.
- Using unreported advantages like ensembling, pretraining, or hardware scaling to claim architectural superiority.

## Evidence (verbatim from paper)

> Table 1. Benchmark results of prevalent 3D medical segmentation methods measured as DSC score [%].

## Citation

```bibtex
@misc{isensee2024nnunet,
  title={nnU-Net Revisited: A Call for Rigorous Validation in 3D Medical Image Segmentation},
  author={Isensee et al. (2024)},
  year={2024},
  note={arXiv:2404.09556}
}
```

- arXiv: 2404.09556
