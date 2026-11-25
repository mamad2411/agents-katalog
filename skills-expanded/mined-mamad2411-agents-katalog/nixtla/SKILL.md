---
name: nixtla
description: "Nixtla ecosystem — statsforecast (statistical), neuralforecast (deep learning), hierarchicalforecast, and MLForecast. Production time series forecasting with AutoARIMA, ETS, Theta, Transformers, and ensemble blending."
tags: [nixtla, time-series, forecasting, arima, deep-learning, hierarchical, zorai]
---
## Overview

Nixtla provides time series forecasting with multiple backends — StatsForecast (statistical), NeuralForecast (deep learning), and HierarchicalForecast (hierarchical reconciliation). Covers ARIMA, ETS, Prophet, Theta, N-BEATS, DeepAR, Temporal Fusion Transformer, and more.

## Installation

```bash
uv pip install nixtla
```

## Statistical Forecasting (StatsForecast)

```python
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA, ETS, Theta

models = [AutoARIMA(season_length=12), ETS(season_length=12), Theta(season_length=12)]
sf = StatsForecast(models=models, freq="M")

# df needs ds (date), y (value), unique_id columns
forecasts = sf.forecast(df, h=12)
print(forecasts)
```

## Deep Learning (NeuralForecast)

```python
from neuralforecast import NeuralForecast
from neuralforecast.models import NBEATS, NHITS

nf = NeuralForecast(models=[NBEATS(input_size=24, h=12), NHITS(input_size=24, h=12)])
nf.fit(df)
forecasts = nf.predict()
```

## Hierarchical Reconciliation

```python
from hierarchicalforecast import HierarchicalForecast
from hierarchicalforecast.methods import BottomUp, TopDown

hf = HierarchicalForecast(models=forecasts, reconcilers=[BottomUp(), TopDown()])
hf.reconcile(S_hierarchy)
```

## References
- [Nixtla docs](https://nixtla.github.io/nixtla/)
- [Nixtla GitHub](https://github.com/Nixtla/nixtla)