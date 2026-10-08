---
name: domain-time-series
description: "Use for time-series tasks: forecasting (demand, sales, energy, finance), time-series classification, and anomaly detection over time (sensors, logs, monitoring). Picks classical vs ML vs deep forecasters, enforces temporal splits (no future leakage), and uses proper time-series metrics/backtesting. Triggers on 'forecast', 'predict next/future', 'time series', 'demand/sales/energy prediction', 'anomaly detection over time', 'seasonality'."
---

# Time-Series - Method Selection

Temporal order is sacred: **the future must never leak into training.**

## Decision table
| Sub-task | Recommended (simple to advanced) | Notes |
|---|---|---|
| Univariate / few series forecasting | **ETS / ARIMA / Theta / Prophet** | Strong, interpretable baselines. Often beat deep on small data. |
| Many related series | **LightGBM on lag/calendar features** then **N-BEATS/NHITS, TFT** | GBT-on-lags is a very strong, cheap default. |
| Long-horizon / rich covariates | **TFT / PatchTST / DeepAR** | Deep only when data volume justifies it. |
| Foundation / zero-shot | **TimesFM / Chronos / Moirai** | Good for cold-start / many series with little history. |
| TS classification | **ROCKET/MiniROCKET, InceptionTime, HIVE-COTE** | ROCKET = fast strong baseline. |
| Anomaly detection | **STL/residual + threshold, Isolation Forest, autoencoder/LSTM** | Start simple; label scarcity is the norm. |

## Temporal rigor (non-negotiable)
- **Split by time**: train strictly before validation before test. Use **rolling/expanding-window backtesting**, not random K-fold (`data-rigor-and-leakage`).
- **No future leakage in features**: lags/rolling stats use only past data; align target horizon carefully; no target-derived or post-hoc features.
- **Fit scalers/encoders on the training window only**, refit as the window rolls.
- **Respect gaps/frequency**: handle missing timestamps, irregular sampling, and known future covariates (holidays) vs unknown.

## Evaluation
- Metrics: **MAE / RMSE / MAPE / sMAPE / MASE** (MASE compares to a naive baseline - always include a naive/seasonal-naive baseline).
- Report per-horizon error and prediction intervals (coverage), not just a point metric.
- Backtest across multiple origins; a single split is not enough.
- Improve: use `accuracy-improvement-loop` (better features/lags, hierarchical reconciliation, ensembling classical+ML, then deep).
