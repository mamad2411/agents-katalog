---
name: aster-timesfm-pipeline
description: >
  Connects Aster DEX market data to TimesFM forecasting. Pulls klines via Aster MCP,
  feeds price/volume series to TimesFM for zero-shot crypto price forecasting with
  quantile intervals. Use for trading signal generation and risk assessment.
license: MIT
metadata:
  author: <your-name>
  version: "1.0.0"
  depends_on:
    - aster-trading
    - timesfm-forecasting
  mcp_servers:
    - aster
---

# Aster → TimesFM Forecasting Pipeline

## Overview

End-to-end crypto price forecasting: pull historical klines from Aster DEX via MCP,
transform to numpy arrays, run through TimesFM 2.5 for zero-shot point forecasts
with quantile prediction intervals.

## When to Use

- Forecasting crypto pair prices (BTC/USDT, ETH/USDT, SOL/USDT, etc.)
- Generating trading signals with confidence intervals
- Risk assessment via quantile spreads (10th-90th percentile)
- Comparing forecast vs actual for strategy validation

## Pipeline Steps

### Step 1: Pull Market Data via Aster MCP

```python
# Use mcp__aster__get_klines to pull historical data
# Example: 500 hourly candles for BTCUSDT
klines = mcp__aster__get_klines(symbol="BTCUSDT", interval="1h", limit=500)
```

Available intervals: `1m`, `5m`, `15m`, `1h`, `4h`, `1d`

### Step 2: Transform to TimesFM Input

```python
import numpy as np

# Extract close prices from klines response
# Klines format: [open_time, open, high, low, close, volume, ...]
close_prices = np.array([float(k[4]) for k in klines])
volumes = np.array([float(k[5]) for k in klines])

# Optional: use funding rates as covariate
# funding = mcp__aster__get_funding_rate(symbol="BTCUSDT")
```

### Step 3: Run TimesFM Forecast

```python
import timesfm

# Load model (cached after first call, ~800MB download)
tfm = timesfm.TimesFM_2p5_200M_torch()

# Forecast next N periods
horizon = 24  # 24 hours ahead for 1h candles
point_forecast, quantile_forecast = tfm.forecast(
    horizon=horizon,
    inputs=[close_prices],
)

# point_forecast shape: (1, horizon) — predicted prices
# quantile_forecast shape: (1, horizon, num_quantiles) — prediction intervals
```

### Step 4: Interpret Results

```python
# point_forecast[0] = array of predicted prices for next 24 hours
# quantile_forecast[0] = array of [10th, 20th, ..., 90th] percentile predictions

current_price = close_prices[-1]
predicted_price = point_forecast[0][-1]  # price at end of horizon
change_pct = (predicted_price - current_price) / current_price * 100

q10 = quantile_forecast[0][-1][0]  # 10th percentile (downside)
q90 = quantile_forecast[0][-1][-1]  # 90th percentile (upside)

print(f"Current: {current_price:.2f}")
print(f"Forecast ({horizon}h): {predicted_price:.2f} ({change_pct:+.2f}%)")
print(f"Range: {q10:.2f} to {q90:.2f}")
```

### Step 5: Multi-Pair Batch Forecasting

```python
pairs = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
all_series = []

for pair in pairs:
    klines = mcp__aster__get_klines(symbol=pair, interval="1h", limit=500)
    closes = np.array([float(k[4]) for k in klines])
    all_series.append(closes)

# Batch forecast all pairs at once (much faster than one-by-one)
point_forecasts, quantile_forecasts = tfm.forecast(
    horizon=24,
    inputs=all_series,
)
```

## Risk Rules

1. **Never trade solely on forecast** — TimesFM is general-purpose, not crypto-specific
2. **Validate accuracy first** — backtest on historical data before live trading
3. **Wide quantile spread = high uncertainty** — reduce position size when q90-q10 is large
4. **Short timeframes are noisier** — 1h/4h more reliable than 1m/5m for crypto
5. **Model freshness** — re-pull klines before each forecast, stale data = stale predictions

## Integration with Other Skills

- **anomaly-detector**: Alert when actual price breaks outside forecast quantile bounds
- **autoresearch**: Measure forecast accuracy over time, optimize horizon/interval parameters
- **council**: Present forecasts to multi-expert panel for trading decisions
- **MiroFish**: Combine quantitative TimesFM forecast with qualitative scenario simulation

## Environment

```bash
# TimesFM venv
source ~/Projects/timesfm/.venv/bin/activate

# Required: timesfm>=2.0.0, torch, numpy
# Model: google/timesfm-2.5-200m-pytorch (auto-downloads from HuggingFace)
```
