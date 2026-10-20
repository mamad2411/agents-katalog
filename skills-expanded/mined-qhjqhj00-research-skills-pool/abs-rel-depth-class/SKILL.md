---
name: abs-rel-depth-class
description: Probes the ability of depth estimation models to accurately predict distances for specific semantic classes, particularly focusing on thin structures like wires and cables. It measures class-specific absolute relative error to highlight performance on challenging, low-pixel-count obstacles relevant to drone navigation. Use when the user has predictions and gold and needs to compute AbsRel_class.
metadata:
  skill_kind: metric
  source_arxiv: 2312.12494
  bibtex_key: kolbeinsson2023ddos
  confidence: high
---

# abs-rel-depth-class

> DDOS: The Drone Depth and Obstacle Segmentation Dataset — Kolbeinsson et al. (2023) (arXiv:2312.12494, 2023)

## What this evaluates

Probes the ability of depth estimation models to accurately predict distances for specific semantic classes, particularly focusing on thin structures like wires and cables. It measures class-specific absolute relative error to highlight performance on challenging, low-pixel-count obstacles relevant to drone navigation.

## Datasets

- **DDOS** — total ?; splits: test (-1)

## Metrics

- `AbsRel_class` **(primary)** — range: [0, 1] or percent
  - Average absolute relative difference between ground truth depth ($d_i$) and estimated depth ($\hat{d}_i$) for all pixels belonging to a specific semantic class: $\frac{1}{N_{\text{class}}} \sum_{i=1}^{N_{\text{class}}} \left| \frac{d_i - \hat{d}_i}{d_i} \right|$.

## Input / output format

**Input**: Per-pixel ground truth depth ($d_i$) and estimated depth ($\hat{d}_i$) for a specific semantic class, along with a class segmentation mask to isolate the target pixels.

**Output**: A single scalar value representing the average absolute relative depth error for the specified class.

## Scoring recipe

```python
def compute_abs_rel_class(gt_depth, pred_depth, class_mask):
    gt = gt_depth[class_mask]
    pred = pred_depth[class_mask]
    abs_rel_errors = np.abs((gt - pred) / gt)
    return np.mean(abs_rel_errors)
```

## Common pitfalls

- Global depth metrics average over all pixels, masking poor performance on thin structures like wires due to their low pixel count.
- The metric requires accurate semantic segmentation masks to isolate the target class before computing depth error.
- Values can exceed 1.0 for large errors, though typically reported as decimals or percentages.

## Evidence (verbatim from paper)

> We propose a novel set of depth metrics specifically tailored for drone applications, namely the absolute relative depth estimation error for each distinct class. To illustrate, we introduce the absolute relative depth error metric for the Ultra Thin class within the DDOS dataset. This metric quantifies the accuracy of depth estimation specifically for objects classified as Ultra Thin in the DDOS dataset.

$$
\operatorname {A b s R e l} _ {\text {c l a s s}} = \frac {1}{N _ {\text {c l a s s}}} \sum_ {i = 1} ^ {N _ {\text {c l a s s}}} \left| \frac {d _ {i} - \hat {d} _ {i}}{d _ {i}} \right| \tag {2}
$$

Here, $\mathrm{AbsRel}_{\mathrm{ultra thin}}$ represents the absolute relative depth estimation error for the Ultra Thin class. $N_{\mathrm{ultra thin}}$ denotes the total number of samples (pixels) in the Ultra Thin class, while $d_i$ and $\hat{d}_i$ represent the ground truth depth and estimated depth for the $i$-th pixel sample, respectively.

## Citation

```bibtex
@misc{kolbeinsson2023ddos,
  title={DDOS: The Drone Depth and Obstacle Segmentation Dataset},
  author={Kolbeinsson et al. (2023)},
  year={2023},
  note={arXiv:2312.12494}
}
```

- arXiv: 2312.12494
