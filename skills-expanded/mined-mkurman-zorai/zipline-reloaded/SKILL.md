---
name: zipline-reloaded
description: "Zipline Reloaded — event-driven backtesting engine. Minute and daily data, custom factors, pipeline API, risk and performance analytics. Forked from Quantopian's Zipline for continued development."
tags: [backtesting, quant-finance, event-driven, factor-models, pipeline, trading, zorai]
---
## Overview

Zipline Reloaded is an event-driven backtesting engine (forked from Quantopian). Supports minute and daily data, custom factors, pipeline API, and built-in risk/performance analytics.

## Installation

```bash
uv pip install zipline-reloaded
```

## Strategy

```python
from zipline.api import order_target, symbol
from zipline import run_algorithm

def initialize(context):
    context.asset = symbol("AAPL")

def handle_data(context, data):
    price = data.current(context.asset, "price")
    sma20 = data.history(context.asset, "price", 20, "1d").mean()
    sma50 = data.history(context.asset, "price", 50, "1d").mean()
    order_target(context.asset, 100 if sma20 > sma50 else 0)

results = run_algorithm(start=pd.Timestamp("2022-01-01"), end=pd.Timestamp("2023-01-01"),
                        initialize=initialize, handle_data=handle_data, capital_base=10000)
```

## References
- [Zipline docs](https://zipline.ml4trading.io/)
- [Zipline Reloaded GitHub](https://github.com/stefan-jansen/zipline-reloaded)