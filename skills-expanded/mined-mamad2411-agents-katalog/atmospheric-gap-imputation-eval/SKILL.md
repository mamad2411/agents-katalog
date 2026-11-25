---
name: atmospheric-gap-imputation-eval
description: Evaluates the ability of machine learning models to reconstruct missing multivariate atmospheric data across time and altitude. It probes spatiotemporal continuity, physical gradient preservation, and performance under varying gap lengths (short, medium, long). Use when the user wants to benchmark on SD-WACCM-X synthetic atmospheric data, or asks about evaluating this task. Reports Pearson correlation R.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2509.01141
  bibtex_key: hu2025imputing
  confidence: high
---

# atmospheric-gap-imputation-eval

> Imputing Missing Long-Term Spatiotemporal Multivariate Atmospheric Data with CNN-Transformer Machine Learning — Hu et al. (2025) (arXiv:2509.01141, 2025)

## What this evaluates

Evaluates the ability of machine learning models to reconstruct missing multivariate atmospheric data across time and altitude. It probes spatiotemporal continuity, physical gradient preservation, and performance under varying gap lengths (short, medium, long).

## Datasets

- **SD-WACCM-X synthetic atmospheric data** — total ?; splits: test (-1)

## Metrics

- `MAE` — range: other
  - Mean Absolute Error: average of absolute differences between predicted and true values across the masked spatiotemporal grid.
- `Pearson correlation R` **(primary)** — range: [0, 1]
  - Pearson correlation coefficient measuring the linear relationship between reconstructed and ground truth fields across the masked region.
- `relative total variation error ($\Delta\mathrm{TV}_{r}$)` — range: percent
  - Percentage difference in total variation between prediction and truth: |TV(pred) - TV(true)| / TV(true) * 100. Measures preservation of vertical gradients.

## Input / output format

**Input**: Spatiotemporal atmospheric variable profiles (e.g., meridional wind) at 6-hour cadence across altitudes (75–115 km), with specific regions masked to simulate missing data gaps.

**Output**: Reconstructed values for the masked spatiotemporal grid cells, matching the input dimensions and units (m s⁻¹).

## Scoring recipe

```python
def compute_metrics(pred, true):
    mae = np.mean(np.abs(pred - true))
    r = np.corrcoef(pred.flatten(), true.flatten())[0, 1]
    tv_pred = np.sum(np.abs(np.diff(pred, axis=0)))
    tv_true = np.sum(np.abs(np.diff(true, axis=0)))
    delta_tv_r = abs(tv_pred - tv_true) / tv_true * 100
    return mae, r, delta_tv_r
```

## Common pitfalls

- Traditional baselines (linear interpolation, PCA, Kalman) tend to over-smooth or distort fine-scale vertical gradients, especially in long gaps.
- Performance degrades non-linearly with gap length; short-gap results should not be extrapolated to medium/long gaps.
- Evaluation focuses on specific coordinate case studies in the main text; full multi-variable averages are deferred to an appendix.

## Evidence (verbatim from paper)

> In the short-gap example at 46.65°N,121.25°W (6-hour cadence; 75-115 km), the two ML variants recover near-truth meridional wind profiles, with MAE ≈ 1.5ms⁻¹, R ≈ 0.99, and small relative total variation error of 0.92% for CT-MVP, 4.15% for a simple transformer. In contrast, the traditional methods yield large error in the missing interval and smear vertical gradients.

## Citation

```bibtex
@misc{hu2025imputing,
  title={Imputing Missing Long-Term Spatiotemporal Multivariate Atmospheric Data with CNN-Transformer Machine Learning},
  author={Hu et al. (2025)},
  year={2025},
  note={arXiv:2509.01141}
}
```

- arXiv: 2509.01141
