---
name: auto-forecasting-benchmark-eval
description: Evaluates automated time series forecasting frameworks (AutoGluon-Timeseries and sktime) across diverse datasets, comparing their performance under different time budgets, frequencies, and domains, and assessing the impact of hyperparameter tuning. Use when the user wants to benchmark on Time Series Forecasting Benchmark, or asks about evaluating this task. Reports SMAPE.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2407.16445
  bibtex_key: sreedhara2024autoforecast
  confidence: high
---

# auto-forecasting-benchmark-eval

> Can time series forecasting be automated? A benchmark and analysis — Sreedhara et al. (2024) (arXiv:2407.16445, 2024)

## What this evaluates

Evaluates automated time series forecasting frameworks (AutoGluon-Timeseries and sktime) across diverse datasets, comparing their performance under different time budgets, frequencies, and domains, and assessing the impact of hyperparameter tuning.

## Datasets

- **Time Series Forecasting Benchmark** — total 36; splits: test (-1)

## Metrics

- `SMAPE` **(primary)** — range: [0, 100]
  - Symmetric Mean Absolute Percentage Error: 100/n * Σ|y_i - ŷ_i| / (|y_i| + |ŷ_i|). The paper rescales this to [0, 1] for visualization.
- `MASE` — range: [0, ∞)
  - Mean Absolute Scaled Error: MAE of forecasts divided by the MAE of a naive seasonal forecast on the training data.

## Input / output format

**Input**: Historical time series observations with known frequency and domain labels.

**Output**: Point forecasts for a specified prediction horizon.

## Scoring recipe

```python
def smape(y_true, y_pred):
    mask = (y_true + y_pred) != 0
    return 100.0 * np.mean(np.abs(y_true[mask] - y_pred[mask]) / (np.abs(y_true[mask]) + np.abs(y_pred[mask])))

def mase(y_true, y_pred, y_train):
    naive_errors = np.mean(np.abs(np.diff(y_train)))
    return np.mean(np.abs(y_true - y_pred)) / naive_errors
```

## Common pitfalls

- 3600-second time limit causes timeouts for complex models or large datasets.
- Models fail on datasets with period=1 (yearly) or non-positive/zero values.

## Evidence (verbatim from paper)

> For both SMAPE and MASE, the AutoGluon framework and Trend methods exhibit statistically significant differences compared to other methods. Examining the corresponding violin plots, we see that SMAPE and MASE values are concentrated near 0 for AutoGluon and around 1 for Trend methods, indicating better accuracy and lower errors for AutoGluon.

## Citation

```bibtex
@misc{sreedhara2024autoforecast,
  title={Can time series forecasting be automated? A benchmark and analysis},
  author={Sreedhara et al. (2024)},
  year={2024},
  note={arXiv:2407.16445}
}
```

- arXiv: 2407.16445
