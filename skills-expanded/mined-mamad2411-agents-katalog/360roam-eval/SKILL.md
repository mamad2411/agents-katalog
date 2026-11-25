---
name: 360roam-eval
description: Evaluates the capability of neural radiance field models to perform real-time, high-fidelity novel view synthesis on large-scale indoor scenes using 360° panoramic imagery. It probes the trade-off between rendering quality, computational efficiency, and geometric awareness in complex, unbounded indoor environments. Use when the user wants to benchmark on 360Roam Dataset, or asks about evaluating this task. Reports PSNR.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2208.02705
  bibtex_key: huang2022360roam
  confidence: high
---

# 360roam-eval

> 360Roam: Real-Time Indoor Roaming Using Geometry-Aware 360$^\circ$ Radiance Fields — Huajian Huang et al. (2022) (arXiv:2208.02705, 2022)

## What this evaluates

Evaluates the capability of neural radiance field models to perform real-time, high-fidelity novel view synthesis on large-scale indoor scenes using 360° panoramic imagery. It probes the trade-off between rendering quality, computational efficiency, and geometric awareness in complex, unbounded indoor environments.

## Datasets

- **360Roam Dataset** — total ?; splits: train (-1), test (-1)

## Metrics

- `PSNR` **(primary)** — range: dB
  - Peak Signal-to-Noise Ratio in decibels (dB), calculated as 10 * log10(MAX^2 / MSE) between the rendered and ground-truth images.
- `SSIM` — range: [0, 1]
  - Structural Similarity Index Measure, evaluating luminance, contrast, and structure similarity between images.
- `LPIPS` — range: [0, 1]
  - Learned Perceptual Image Patch Similarity, measuring perceptual difference using deep network features (lower is better).
- `Inference Speed` — range: seconds
  - Wall-clock time in seconds to render a single panoramic view at 1520×760 resolution.

## Input / output format

**Input**: 360° panoramic images (6080×3040 resolution) with known camera poses.

**Output**: Rendered novel-view panoramic images (1520×760 resolution).

## Scoring recipe

```python
def compute_metrics(pred, gt):
    psnr = peak_signal_noise_ratio(gt, pred)
    ssim = structural_similarity(gt, pred)
    lpips = learned_perceptual_image_patch_similarity(gt, pred)
    return psnr, ssim, lpips

def compute_speed(render_fn):
    start = time.time()
    render_fn((1520, 760))
    return time.time() - start
```

## Common pitfalls

- Evaluation images are resized to 1520×760, not the original 6080×3040 resolution.
- Inference speed is measured on a single RTX2080 Ti GPU without averaging over multiple runs or accounting for warm-up time.

## Evidence (verbatim from paper)

> Quantitative measurements in terms of appearance similarity include Peak Signal-to-noise Ratio (PSNR), Structural Similarity Index Measure (SSIM) and Learned Perceptual Image Patch Similarity (LPIPS) [45]. We also evaluated the inference speed of a panoramic view in 1520 × 760 on a single RTX2080 Ti GPU.

## Citation

```bibtex
@misc{huang2022360roam,
  title={360Roam: Real-Time Indoor Roaming Using Geometry-Aware 360$^\circ$ Radiance Fields},
  author={Huajian Huang et al. (2022)},
  year={2022},
  note={arXiv:2208.02705}
}
```

- arXiv: 2208.02705
