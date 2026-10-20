---
name: prophet
description: "Meta Prophet — forecasting at scale. Additive model with yearly/weekly/daily seasonality, holiday effects, changepoints, and trend decomposition. Handles missing data and outliers automatically."
tags: [prophet, forecasting, time-series, seasonality, trend, meta, zorai]
---
## Overview

Meta Prophet forecasts time series data with additive seasonality (yearly, weekly, daily), holiday effects, changepoint detection, and trend decomposition. Handles missing data and outliers automatically. Designed for business forecasting with human-interpretable components.

## Installation

```bash
uv pip install prophet
```

## Forecast

```python
import pandas as pd
from prophet import Prophet
import numpy as np

df = pd.DataFrame({
    "ds": pd.date_range("2023-01-01", periods=365, freq="D"),
    "y": [100 + i*0.5 + 10*(i%7==0) + np.random.normal(0, 5) for i in range(365)],
})

model = Prophet(yearly_seasonality=True, weekly_seasonality=True)
model.fit(df)

future = model.make_future_dataframe(periods=90)
forecast = model.predict(future)

model.plot(forecast)
model.plot_components(forecast)
```

## Holidays

```python
model = Prophet()
model.add_country_holidays("US")
model.fit(df)
```

## References
- [Prophet docs](https://facebook.github.io/prophet/)
- [Prophet GitHub](https://github.com/facebook/prophet)