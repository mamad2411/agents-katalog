---
name: financial-modeling
description: Advanced financial modeling with DCF, Monte Carlo, portfolio optimization, risk metrics, and Aster DEX integration for backtesting
triggers:
  - financial model
  - DCF
  - monte carlo
  - portfolio optimization
  - VaR
  - sharpe ratio
  - backtesting
  - risk metrics
  - financial analysis
---

# Financial Modeling (Advanced)

Quantitative finance patterns for trading strategies, portfolio optimization, and risk analysis. Integrates with Aster DEX via MCP tools.

## Risk Metrics

```python
import numpy as np
import pandas as pd

def sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.0) -> float:
    excess = returns - risk_free_rate / 252
    return np.sqrt(252) * excess.mean() / excess.std()

def sortino_ratio(returns: pd.Series, risk_free_rate: float = 0.0) -> float:
    excess = returns - risk_free_rate / 252
    downside = excess[excess < 0].std()
    return np.sqrt(252) * excess.mean() / downside if downside > 0 else np.inf

def max_drawdown(returns: pd.Series) -> float:
    cumulative = (1 + returns).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    return drawdown.min()

def value_at_risk(returns: pd.Series, confidence: float = 0.95) -> float:
    return np.percentile(returns, (1 - confidence) * 100)

def conditional_var(returns: pd.Series, confidence: float = 0.95) -> float:
    var = value_at_risk(returns, confidence)
    return returns[returns <= var].mean()
```

## Monte Carlo Simulation

```python
def monte_carlo_portfolio(
    returns: pd.DataFrame,
    n_simulations: int = 10000,
    n_days: int = 252,
) -> dict:
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    results = np.zeros((n_simulations, 3))  # return, vol, sharpe

    for i in range(n_simulations):
        weights = np.random.dirichlet(np.ones(len(returns.columns)))
        port_return = np.sum(mean_returns * weights) * n_days
        port_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix * n_days, weights)))
        results[i] = [port_return, port_vol, port_return / port_vol]

    return {
        "max_sharpe_idx": results[:, 2].argmax(),
        "min_vol_idx": results[:, 1].argmin(),
        "results": results,
    }
```

## Aster DEX Integration

```python
# Fetch real-time data via Aster MCP
# Use mcp__aster__get_klines for historical data
# Use mcp__aster__get_ticker for current prices
# Use mcp__aster__get_positions for portfolio state

# Backtesting pattern
async def backtest_strategy(symbol: str, interval: str = "1h", lookback: int = 500):
    klines = await mcp__aster__get_klines(symbol=symbol, interval=interval, limit=lookback)
    df = pd.DataFrame(klines, columns=["time", "open", "high", "low", "close", "volume"])
    df["close"] = df["close"].astype(float)
    df["returns"] = df["close"].pct_change()

    # Apply strategy signals
    signals = generate_signals(df)

    # Calculate strategy returns
    strategy_returns = signals * df["returns"]

    return {
        "total_return": (1 + strategy_returns).prod() - 1,
        "sharpe": sharpe_ratio(strategy_returns),
        "max_drawdown": max_drawdown(strategy_returns),
        "win_rate": (strategy_returns > 0).mean(),
    }
```

## Portfolio Optimization (Mean-Variance)

```python
from scipy.optimize import minimize

def optimize_portfolio(returns: pd.DataFrame, target_return: float = None):
    n = len(returns.columns)
    mean_returns = returns.mean() * 252
    cov_matrix = returns.cov() * 252

    def portfolio_volatility(weights):
        return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

    constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}]
    if target_return:
        constraints.append({
            "type": "eq",
            "fun": lambda w: np.sum(mean_returns * w) - target_return
        })
    bounds = [(0, 1) for _ in range(n)]

    result = minimize(portfolio_volatility, np.ones(n) / n,
                      method="SLSQP", bounds=bounds, constraints=constraints)
    return dict(zip(returns.columns, result.x))
```
