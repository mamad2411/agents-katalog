---
name: abdomenct1k-eval
description: This benchmark evaluates the ability of 3D medical image segmentation models to accurately delineate abdominal organs (liver, kidney, spleen, pancreas) under clinically challenging conditions. It specifically probes generalization across unseen medical centers, CT contrast phases, and severe pathologies like tumors, while measuring both volumetric overlap and boundary precision. Use when the user wants to benchmark on AbdomenCT-1K, or asks about evaluating this task. Reports DSC.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2010.14808
  bibtex_key: ma2020abdomenct1k
  confidence: high
---

# abdomenct1k-eval

> AbdomenCT-1K: Is Abdominal Organ Segmentation A Solved Problem? — Ma et al. (2020) (arXiv:2010.14808, 2020)

## What this evaluates

This benchmark evaluates the ability of 3D medical image segmentation models to accurately delineate abdominal organs (liver, kidney, spleen, pancreas) under clinically challenging conditions. It specifically probes generalization across unseen medical centers, CT contrast phases, and severe pathologies like tumors, while measuring both volumetric overlap and boundary precision.

## Datasets

- **AbdomenCT-1K** — total 1000; splits: test (100), train (-1); repo https://github.com/JunMa11/AbdomenCT-1K

## Metrics

- `DSC` **(primary)** — range: percent
  - Dice Similarity Coefficient: 2|A∩B|/(|A|+|B|), computed per organ and averaged across cases. Reported as a percentage.
- `NSD` — range: percent
  - Normalized Surface Distance: average surface distance between prediction and ground truth, normalized by the maximum diameter of the ground truth mask. Reported as a percentage.

## Input / output format

**Input**: 3D abdominal CT scan volumes (Hounsfield units)

**Output**: 3D segmentation masks with class labels for liver, kidney, spleen, and pancreas

## Scoring recipe

```python
def compute_metrics(pred_mask, gt_mask, num_classes=4):
    dice_scores = []
    nsd_scores = []
    for cls in range(1, num_classes + 1):
        p = (pred_mask == cls)
        g = (gt_mask == cls)
        intersection = np.sum(p & g)
        union = np.sum(p | g)
        dice = 2 * intersection / union if union > 0 else 0.0
        dice_scores.append(dice)
        nsd = calculate_nsd(p, g)
        nsd_scores.append(nsd)
    return np.mean(dice_scores) * 100, np.mean(nsd_scores) * 100
```

## Common pitfalls

- Relying solely on DSC masks boundary inaccuracies, which are clinically critical for surgical planning.
- Evaluating on homogeneous data (same center/phase) inflates performance; the benchmark requires testing on unseen centers, phases, and lesion-affected cases.
- Failing to report per-organ results hides severe degradation in smaller organs like the pancreas.

## Evidence (verbatim from paper)

> For the DSC score, though the high DSC scores and low dispersed distributions from the violin plots of the liver segmentation indicate great performance, the results degrade for the other organs. For the NSD score, the obtained scores and the dispersed distributions observed from the violin plots indicate unsatisfying segmentation performance for all four organs.

## Citation

```bibtex
@misc{ma2020abdomenct1k,
  title={AbdomenCT-1K: Is Abdominal Organ Segmentation A Solved Problem?},
  author={Ma et al. (2020)},
  year={2020},
  note={arXiv:2010.14808}
}
```

- arXiv: 2010.14808
