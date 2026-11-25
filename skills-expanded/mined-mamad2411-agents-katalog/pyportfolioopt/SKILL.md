---
name: pyportfolioopt
description: "Portfolio optimization library: mean-variance, Black-Litterman, CVaR optimization, risk parity, Hierarchical Risk Parity (HRP), and CLA. Factor models, shrinkage estimators, and ex-ante risk analysis."
tags: [portfolio-optimization, risk-management, asset-allocation, mean-variance, hrp, quant-finance, zorai]
---
## Overview

PyPortfolioOpt implements mean-variance optimization, Black-Litterman, CVaR optimization, risk parity, Hierarchical Risk Parity (HRP), and CLA. Handles asset allocation with factor models and ex-ante risk decomposition.

## Installation

```bash
uv pip install PyPortfolioOpt
```

## Max Sharpe Portfolio

```python
import yfinance as yf
from pypfopt import EfficientFrontier, risk_models, expected_returns

prices = yf.download(["AAPL", "MSFT", "GOOGL"], start="2022-01-01")["Close"]
mu = expected_returns.mean_historical_return(prices)
S = risk_models.sample_cov(prices)

ef = EfficientFrontier(mu, S)
weights = ef.max_sharpe()
print(ef.clean_weights())
perf = ef.portfolio_performance()
print(f"Return: {perf[0]:.2%}, Vol: {perf[1]:.2%}, Sharpe: {perf[2]:.2f}")
```

## HRP

```python
from pypfopt import HRPOpt
returns = prices.pct_change().dropna()
hrp = HRPOpt(returns)
weights = hrp.optimize()
```

## References
- [PyPortfolioOpt docs](https://pyportfolioopt.readthedocs.io/)
- [PyPortfolioOpt GitHub](https://github.com/robertmartin8/PyPortfolioOpt)