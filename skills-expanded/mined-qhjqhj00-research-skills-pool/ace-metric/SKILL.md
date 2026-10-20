---
name: ace-metric
description: Probes the physical plausibility and spatiotemporal flow preservation of data-driven weather forecasting models by directly measuring errors in horizontal (advection) and vertical (convection) atmospheric motions, rather than relying on pixel-wise accuracy metrics that reward blurriness. Use when the user has predictions and gold and needs to compute ACE.
metadata:
  skill_kind: metric
  source_arxiv: 2406.04678
  bibtex_key: kim2024ace
  confidence: high
---

# ace-metric

> ACE Metric: Advection and Convection Evaluation for Accurate Weather Forecasting — Kim et al. (2024) (arXiv:2406.04678, 2024)

## What this evaluates

Probes the physical plausibility and spatiotemporal flow preservation of data-driven weather forecasting models by directly measuring errors in horizontal (advection) and vertical (convection) atmospheric motions, rather than relying on pixel-wise accuracy metrics that reward blurriness.

## Datasets

- **WeatherBench2** — total ?; splits: test (-1)
- **MovingMNIST** — total 10000; splits: test (-1)

## Metrics

- `ACE` **(primary)** — range: other
  - Computes Advection Error (AE) and Convection Error (CE) by estimating spatiotemporal flow fields via multi-scale numerical optimization, then aggregates them (e.g., AE + CE/AE). Designed to penalize blurriness and reward physical flow preservation.
- `RMSE` — range: [0, inf)
  - Root Mean Squared Error between predicted and ground truth pixel values.
- `MAE` — range: [0, inf)
  - Mean Absolute Error between predicted and ground truth pixel values.
- `MSE` — range: [0, inf)
  - Mean Squared Error between predicted and ground truth pixel values.
- `PSNR` — range: [0, inf)
  - Peak Signal-to-Noise Ratio in decibels, derived from MSE.
- `SSIM` — range: [0, 1]
  - Structural Similarity Index measuring perceived image quality.
- `FVD` — range: [0, inf)
  - Frechet Video Distance measuring distributional similarity between real and generated video feature embeddings.

## Input / output format

**Input**: Paired spatiotemporal sequences (video frames or weather grid maps) representing ground truth and model predictions.

**Output**: Scalar error values for Advection Error (AE), Convection Error (CE), and the combined ACE score per sequence/forecast step.

## Scoring recipe

```python
def compute_ace(pred, gt, tau=0.25, lam=0.15, nscales=5, warps=5, eps=0.01, inner=30, outer=10, scale_step=0.8, median_k=5):
    flow = estimate_flow(pred, gt, tau, lam, nscales, warps, eps, inner, outer, scale_step, median_k)
    ae = compute_advection_error(flow)
    ce = compute_convection_error(flow)
    ace = ae + (ce / ae) if ae > 0 else float('inf')
    return ace, ae, ce
```

## Common pitfalls

- Relying solely on pixel-wise metrics like RMSE/MSE, which reward blurred outputs and fail to capture physical plausibility.
- Assuming lower ACE scores always indicate better forecasts without considering that the combined score uses a ratio (AE + CE/AE) rather than a simple sum.
- Ignoring that the metric requires flow estimation via numerical optimization, making it computationally heavier than standard pixel-wise losses.

## Evidence (verbatim from paper)

> The paper proposes the Advection and Convection Error (ACE) metric to evaluate data-driven weather forecasting models by directly assessing the physical accuracy of horizontal (advection) and vertical (convection) atmospheric motions—critical for predicting large-scale weather patterns and localized severe events. Unlike pixel-wise metrics (e.g., RMSE, MSE) that reward blurriness and fail to capture physical plausibility, ACE is designed to measure how well models preserve the spatiotemporal dynamics of real-world atmospheric flows, validated on WeatherBench2 and MovingMNIST datasets.

## Citation

```bibtex
@misc{kim2024ace,
  title={ACE Metric: Advection and Convection Evaluation for Accurate Weather Forecasting},
  author={Kim et al. (2024)},
  year={2024},
  note={arXiv:2406.04678}
}
```

- arXiv: 2406.04678
