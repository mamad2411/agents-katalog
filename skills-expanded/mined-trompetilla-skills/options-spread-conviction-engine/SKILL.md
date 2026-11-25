---
name: options-spread-conviction-engine
description: Multi-regime vertical spread analysis engine. Scores bull put, bear call, bull call, and bear put spreads using Ichimoku, RSI, MACD, and Bollinger Bands. Outputs 0-100 conviction scores with actionable recommendations.
version: 1.0.0
author: Leonardo Da Pinchy
metadata:
  openclaw:
    emoji: 📊
    requires:
      bins: ["python3"]
    install:
      - id: venv-setup
        kind: exec
        command: "cd {baseDir} && python3 scripts/setup-venv.sh"
        label: "Setup isolated Python environment with dependencies"
---

# Options Spread Conviction Engine

**Multi-regime vertical spread scoring using Ichimoku, RSI, MACD, and Bollinger Bands.**

## Overview

This engine analyzes any ticker and scores four vertical spread strategies:

| Strategy | Type | Philosophy | Ideal Setup |
|----------|------|------------|-------------|
| **bull_put** | Credit | Mean Reversion | Bullish trend + oversold dip |
| **bear_call** | Credit | Mean Reversion | Bearish trend + overbought rip |
| **bull_call** | Debit | Breakout | Strong bullish momentum |
| **bear_put** | Debit | Breakout | Strong bearish momentum |

## Scoring Methodology

Weights vary by strategy type (Credit = Mean Reversion, Debit = Breakout):

### Credit Spreads (bull_put, bear_call)
| Indicator | Weight | Purpose |
|-----------|--------|---------|
| Ichimoku Cloud | 30 pts | Trend structure & equilibrium |
| RSI | 25 pts | Entry timing (mean-reversion) |
| MACD | 20 pts | Momentum confirmation |
| Bollinger Bands | 25 pts | Volatility regime |

### Debit Spreads (bull_call, bear_put)
| Indicator | Weight | Purpose |
|-----------|--------|---------|
| Ichimoku Cloud | 25 pts | Trend confirmation |
| RSI | 15 pts | Directional momentum |
| MACD | 35 pts | Breakout acceleration |
| Bollinger Bands | 25 pts | Bandwidth expansion |

**Total: 100 points**

## Conviction Tiers

| Score | Tier | Action |
|-------|------|--------|
| 80-100 | EXECUTE | High conviction — Enter the spread |
| 60-79 | PREPARE | Favorable — Size the trade |
| 40-59 | WATCH | Interesting — Add to watchlist |
| 0-39 | WAIT | Poor conditions — Avoid / No setup |

## Usage

### Basic Analysis
```bash
conviction-engine AAPL
conviction-engine SPY --strategy bear_call
conviction-engine QQQ --strategy bull_call --period 2y
```

### Multiple Tickers
```bash
conviction-engine AAPL MSFT GOOGL --strategy bull_put
```

### JSON Output (for automation)
```bash
conviction-engine TSLA --strategy bear_call --json
```

### Full Options
```bash
conviction-engine <ticker> [ticker...]
  --strategy {bull_put,bear_call,bull_call,bear_put}
  --period {1y,2y,3y,5y}
  --json
  --verbose
```

## Example Output

```
================================================================================
SPY — Bull Call Spread (Debit/Breakout)
================================================================================
Price: $478.23 | Trend: BULLISH | Cloud: $462-$471

Indicator Scores:
  Ichimoku        22.5/25  Price above cloud, bullish TK cross
  RSI             12.0/15  RSI=58.3, room to run
  MACD            32.5/35  MACD above signal, rising histogram
  Bollinger       23.1/25  %B=0.72, bandwidth stable

CONVICTION SCORE: 90.1/100 — EXECUTE ✅

Recommendation: Favorable setup for bull call spread. Strong momentum
with cloud support. Consider 30-45 DTE strikes $480/$485.
```

## Academic Foundation

- **Ichimoku Cloud** — Trend structure (Hosoda, 1968)
- **RSI** — Momentum oscillator (Wilder, 1978)
- **MACD** — Trend momentum (Appel, 1979)
- **Bollinger Bands** — Volatility envelopes (Bollinger, 2001)

Combining orthogonal signals reduces false-positive rate compared to single-indicator strategies (Pring, 2002; Murphy, 1999).

## Requirements

- Python 3.10+ (Python 3.14+ supported via pure-python mode)
- Isolated virtual environment (auto-created on first run)
- Internet connection (fetches data from Yahoo Finance)

## Installation

```bash
clawhub install options-spread-conviction-engine
```

The skill automatically creates a virtual environment and installs:
- pandas >= 2.0
- pandas_ta >= 0.4.0 (pure Python mode on 3.14+)
- yfinance >= 1.0
- scipy, tqdm

**Note:** On Python 3.14+, the engine runs in pure Python mode without numba (numba doesn't support 3.14 yet). Performance is slightly reduced but all functionality works correctly.

## Files

- `scripts/conviction-engine` — Main wrapper script
- `scripts/spread_conviction_engine.py` — Core engine
- `scripts/setup-venv.sh` — Environment setup
- `assets/` — Documentation and examples

## License

MIT — Part of the Financial Toolkit for OpenClaw
