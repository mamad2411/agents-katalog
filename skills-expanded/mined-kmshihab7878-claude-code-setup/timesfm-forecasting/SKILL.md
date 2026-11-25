---
name: timesfm-forecasting
description: >
  Zero-shot time series forecasting with Google's TimesFM foundation model. Use this
  skill when forecasting ANY univariate time series — sales, sensor readings, stock prices,
  energy demand, patient vitals, weather, or scientific measurements — without training a
  custom model. Supports both basic forecasting and advanced covariate forecasting (XReg)
  with dynamic and static exogenous variables. Automatically checks system RAM/GPU before
  loading the model, validates dataset fit before processing, supports CSV/DataFrame/array
  inputs, and returns point forecasts with calibrated prediction intervals. Includes a
  preflight system checker script that MUST be run before first use to verify the machine
  can load the model and handle your specific dataset.
license: Apache-2.0
metadata:
  author: Clayton Young (@borealBytes)
  version: "1.0.0"
---
# TimesFM Forecasting

TimesFM is a zero-shot time-series foundation model for univariate forecasting. Use it for sales, demand, sensors, vitals, prices, weather, and other temporal numeric series when you need point forecasts plus calibrated quantile intervals without training a custom model.

## When to Use This Skill

Use when you need:

- zero-shot forecasting for one or many univariate series
- probabilistic forecasts with prediction intervals
- batch forecasting across many related series
- covariate forecasting with exogenous variables via TimesFM 2.5 + `timesfm[xreg]`
- anomaly screening by comparing actuals against forecast quantile bands

Do not use when the task needs coefficient interpretation, time-series classification/clustering, multivariate VAR/Granger causality, generic tabular ML, or unavailable optional XReg dependencies.

## Mandatory Safety Preflight

**Always run the system checker before first model load:**

```bash
python scripts/check_system.py
```

For dataset sizing, run the checker with `--num-series`, `--context-length`, `--horizon`, and `--batch-size`. Model weights are not stored here; they download on demand from Hugging Face.

Read `references/operational-guide.md` for the full RAM/GPU/disk decision tree, dataset memory formula, hardware table, install commands, examples, and validation checks.

## Minimum Operating Pattern

1. Run `scripts/check_system.py` and confirm RAM, disk, Python, and model dependency readiness.
2. Prepare numeric, ordered, one-dimensional arrays; handle missing values intentionally.
3. Use TimesFM 2.5 unless the task explicitly requires an older checkpoint.
4. Compile with `ForecastConfig` before calling `forecast()`.
5. Set `normalize_inputs=True`, `use_continuous_quantile_head=True`, and `fix_quantile_crossing=True` unless you have a reason not to.
6. Set `infer_is_positive=False` for temperatures, returns, PnL, or any negative-capable series.
7. Validate output shape, NaNs, quantile indices, and forecast reasonableness before reporting.

## Minimal Example

```python
import numpy as np
import torch
import timesfm

torch.set_float32_matmul_precision("high")
model = timesfm.TimesFM_2p5_200M_torch.from_pretrained(
    "google/timesfm-2.5-200m-pytorch"
)
model.compile(timesfm.ForecastConfig(
    max_context=1024,
    max_horizon=256,
    normalize_inputs=True,
    use_continuous_quantile_head=True,
    fix_quantile_crossing=True,
))

point, quantiles = model.forecast(
    horizon=24,
    inputs=[np.sin(np.linspace(0, 20, 200))],
)
```

## Output Rules

TimesFM returns `(point_forecast, quantile_forecast)`:

- `point_forecast`: `(batch, horizon)` median forecast.
- `quantile_forecast`: `(batch, horizon, 10)` with mean at index 0, q10 at index 1, median at index 5, and q90 at index 9.
- Values outside q10-q90 are unusual; use this carefully for anomaly screening.

## References

- `references/operational-guide.md` — full preflight, install, examples, workflows, tuning, scripts, quality checks, mistakes, and validation snippets.
- `references/system_requirements.md` — hardware tiers, GPU/CPU selection, and memory estimation.
- `references/api_reference.md` — full model classes, `ForecastConfig`, output shapes, and model checkpoints.
- `references/data_preparation.md` — input formats, NaN handling, CSV loading, and covariate setup.

## Quality Checklist

Before declaring success:

- output shapes match `(n_series, horizon)` and `(n_series, horizon, 10)`
- quantile indices are interpreted correctly
- context has at least 32 points
- forecasts contain no NaN values
- TimesFM 1.0/2.0 frequency flags are only used for those older versions
- headless plots set `matplotlib.use("Agg")` before pyplot import
- validation command output or saved artifacts are inspected
