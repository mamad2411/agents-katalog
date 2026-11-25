---
name: riskfolio-lib
description: "Portfolio risk and optimization: mean-variance, risk parity, CVaR, CDaR, worst-case, and robust optimization. Factor models, Black-Litterman, NCO. Supports plotting and interactive dashboards."
tags: [portfolio-optimization, risk-parity, cvar, factor-models, risk-management, quant-finance, zorai]
---
## Overview

Riskfolio-Lib provides portfolio optimization beyond mean-variance: risk parity, CVaR, CDaR, worst-case, robust optimization, NCO (Network Clustering), and hierarchical methods. Includes factor models, Black-Litterman, and built-in plotting for efficient frontiers.

## Installation

```bash
uv pip install riskfolio-lib
```

## Mean-Variance Optimization

```python
import riskfolio as rp
import yfinance as yf

prices = yf.download(["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"], start="2022-01-01")["Close"]
returns = prices.pct_change().dropna()

port = rp.Portfolio(returns=returns)
port.assets_stats(method_mu="hist", method_cov="hist")

# Max Sharpe
w = port.optimization(model="Classic", rm="MV", obj="Sharpe", hist=True)
print("Optimal weights:", w.to_dict())

# Risk parity
w_rp = port.optimization(model="Classic", rm="MV", obj="MinRisk", hist=True)
```

## References
- [Riskfolio-Lib docs](https://riskfolio-lib.readthedocs.io/)
- [Riskfolio-Lib GitHub](https://github.com/dcajasn/Riskfolio-Lib)