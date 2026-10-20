---
name: freqtrade
description: "Open-source crypto trading bot. Strategy development in Python, backtesting, hyperparameter optimization, dry-run and live trading. Supports major exchanges via CCXT. Telegram integration for monitoring."
tags: [crypto, trading-bot, backtesting, automation, strategy, ccxt, zorai]
---
## Overview

Freqtrade is an open-source crypto trading bot written in Python. Supports strategy development, backtesting, hyperparameter optimization, and dry-run or live trading via 100+ exchange backends (CCXT).

## Installation

```bash
git clone https://github.com/freqtrade/freqtrade.git
cd freqtrade
uv pip install -e .
```

## Strategy

```python
from freqtrade.strategy import IStrategy

class MyStrategy(IStrategy):
    timeframe = "1h"
    minimal_roi = {"0": 0.01}
    stoploss = -0.05

    def populate_indicators(self, dataframe, metadata):
        dataframe["rsi"] = 100 - (100 / (1 + dataframe["close"] / dataframe["close"].shift(14)))
        return dataframe

    def populate_buy_trend(self, dataframe, metadata):
        dataframe.loc[(dataframe["rsi"] < 30) & (dataframe["volume"] > 0), "buy"] = 1
        return dataframe
```

## Run

```bash
freqtrade backtesting --strategy MyStrategy --timerange 20240101-20241231
freqtrade trade --strategy MyStrategy --dry-run
```

## References
- [Freqtrade docs](https://www.freqtrade.io/)
- [Freqtrade GitHub](https://github.com/freqtrade/freqtrade)