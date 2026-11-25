---
name: evolution-engine
description: Domain knowledge for the Evolution Engine — LLM-powered autonomous strategy discovery from raw OHLCV data. Covers the generate-backtest-select-evolve loop, vectorized backtesting, out-of-sample validation, and strategy graduation. Use when discovering trading patterns, running backtests, evolving strategies, or reviewing evolution logs. Triggers on "evolve", "discover patterns", "backtest", "evolution", "strategy generation", "candidate strategy".
---

# Evolution Engine

## Overview

The Evolution Engine autonomously discovers trading strategies from raw price data. It uses LLM-powered pattern generation combined with vectorized backtesting to evolve, test, and graduate viable trading rules — without manual rule writing.

This is not parameter optimization on a known strategy. It's open-ended strategy discovery: the LLM proposes novel entry/exit logic, the engine validates it against real data, and natural selection eliminates the losers.

## How It Works

### The Evolution Loop

```
OHLCV Data → LLM Generation → Vectorized Backtest → Selection → Mutation → Repeat
                                                          ↓
                                                    Out-of-Sample Validation
                                                          ↓
                                                    Graduated Strategies
```

### Step-by-Step

1. **Data Fetch**: Pull OHLCV candles from Binance public API (no key needed)
2. **Generate**: LLM analyzes price patterns and proposes N candidate strategies (entry/exit rules, position sizing, stop loss)
3. **Backtest**: Each candidate is backtested vectorized (numpy, no loop-per-candle) for speed
4. **Score**: Candidates scored by Sharpe ratio, win rate, max drawdown, total return
5. **Select**: Top K candidates survive. Bottom candidates are eliminated (graveyard).
6. **Mutate**: LLM takes survivors and generates variations (parameter tweaks, rule modifications)
7. **Repeat**: Steps 3-6 for N generations
8. **Validate**: Final survivors are tested on held-out out-of-sample data
9. **Graduate**: Strategies that pass OOS validation are marked as graduated

### Key Design Decisions

- **LLM generates rules, not parameters.** The engine doesn't optimize MACD(12,26,9) → MACD(14,28,10). It discovers entirely new rule combinations.
- **Vectorized backtesting.** No candle-by-candle loops. Numpy vectorized operations make backtests 100x faster than event-driven simulators.
- **OOS validation is mandatory.** In-sample performance means nothing. Only OOS-validated strategies graduate.
- **Graveyard is data.** Failed strategies are logged with failure reasons. This prevents re-discovering the same dead ends.

## MCP Tools

| Tool | Purpose |
|------|---------|
| `evolution_fetch_market_data` | Fetch OHLCV data from Binance for a symbol/timeframe/period |
| `evolution_discover_patterns` | LLM-powered pattern discovery — generates N candidate strategies |
| `evolution_run_backtest` | Backtest a single candidate — returns Sharpe, win rate, drawdown |
| `evolution_evolve_strategy` | Full evolution loop: generate → backtest → select → mutate × N generations |
| `evolution_get_log` | History of evolution runs: graduated strategies, graveyard, metrics |

## Backtest Metrics

Every backtest produces:

| Metric | Minimum for Graduation |
|--------|----------------------|
| Sharpe Ratio | > 1.0 (OOS) |
| Win Rate | > 40% |
| Max Drawdown | < 25% |
| Number of Trades | > 30 (statistical significance) |
| Profit Factor | > 1.2 |

These thresholds are guidelines. Context matters — a Sharpe of 0.9 with 500 trades may be more reliable than 2.5 with 15 trades.

## Best Practices

### Before Running Evolution
- **Choose the right timeframe.** 1h and 4h produce the most tradeable strategies. 1m is noise. 1d may not have enough data points.
- **Use enough data.** 90 days minimum for 1h data. 180 days for 4h. Less data = more overfitting risk.
- **Start small.** 3 generations × 10 candidates is a good starting point. Don't jump to 10 × 50.

### During Evolution
- **Don't interrupt.** Each generation builds on the previous. Stopping mid-run wastes compute.
- **Monitor the graveyard.** If 90% of candidates fail on the same metric (e.g., max drawdown), the symbol/timeframe may not be suitable.
- **Watch for convergence.** If surviving strategies across generations look increasingly similar, the engine has found a local optimum.

### After Evolution
- **Never deploy without OOS validation.** In-sample results are marketing, not science.
- **Paper trade first.** Even OOS-validated strategies should be paper traded for 2-4 weeks.
- **Check regime sensitivity.** A strategy discovered in a trending market may fail in ranging conditions. Test across multiple market regimes.
- **Log everything.** Use `evolution_get_log` to review what was tried, what failed, and why.

### When NOT to Use Evolution
- **Not for parameter optimization.** If you already have a strategy and just want to tune parameters, use a traditional optimizer.
- **Not for HFT.** The engine works on candle data, not tick data. Sub-minute strategies need different infrastructure.
- **Not as a replacement for domain knowledge.** Evolution discovers patterns, but you still need to understand why a pattern works before risking real money.

## Common Mistakes

| Mistake | Why It's Bad | Fix |
|---------|-------------|-----|
| Too few data points | Strategies overfit to noise | Use 90+ days for 1h, 180+ for 4h |
| Skipping OOS validation | In-sample Sharpe of 3.0 means nothing | Always validate on held-out data |
| Too many generations | Overfitting through excessive selection pressure | 3-5 generations is usually sufficient |
| Deploying immediately | No buffer for regime changes | Paper trade 2-4 weeks first |
| Ignoring the graveyard | Re-discovering dead strategies wastes compute | Review `evolution_get_log` before new runs |
| Using correlated symbols | BTCUSDT and ETHUSDT strategies overlap heavily | Test on uncorrelated markets |

## Requirements

- `ANTHROPIC_API_KEY` — Required for LLM-powered pattern discovery
- Binance public API — Used for OHLCV data (no API key needed)
- Python with numpy — For vectorized backtesting
