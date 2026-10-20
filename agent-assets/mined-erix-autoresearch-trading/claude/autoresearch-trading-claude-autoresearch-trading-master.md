# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Autoresearch-style options income strategy optimizer for SPY. Karpathy-style loop: start from a baseline, modify one parameter at a time, keep improvements, revert failures, log everything.

## Setup & Commands

```bash
# Install dependencies
uv sync

# Run all experiments (25 strategies, ~5 min)
uv run options_backtest_optionsdx.py

# Run a single experiment
uv run options_backtest_optionsdx.py 23

# Show leaderboard from saved results
uv run options_backtest_optionsdx.py leaderboard
```

## Architecture

**Main file:** `options_backtest_optionsdx.py` — experiment definitions, backtest engine, results logging.

**Data:** `data/spy/` — OptionsDX EOD options chains (2010-2023) with pre-calculated Greeks. Monthly TXT files, one row per strike/expiration/trading day.

**VIX data:** Downloaded via yfinance at runtime, used for position sizing.

**Results:** `data/optionsdx_experiments.csv` — per-year and overall metrics for each experiment.

## Strategy Parameters

Each experiment defines:
- `legs`: list of (side, target_delta) — e.g. `[("put", -0.30)]` or `[("put", -0.16), ("call", 0.16)]`
- `entry_dte`: target days to expiration (45 or 60)
- `mgmt_profit_pct`: profit target to close (0.25, 0.50, 0.75)
- `mgmt_dte_close`: close at this DTE regardless (21)
- `entry_interval`: days between new entries (5, 7, 14)
- `stop_loss_pct`: optional stop loss multiplier (None, 2.0, 3.0)
- `vix_sizing`: VIX-based position sizing mode (None, scale_up, scale_down, skip_high, only_high)

## Key Findings

- **VIX scale UP** (more contracts in high VIX) beats scale DOWN across regimes
- **20d put + VIX scale up** is the best risk-adjusted strategy (Sharpe 4.42 over 14 years)
- **Only enter when VIX > 20** has highest Sharpe (7.45) but fewest trades
- Short puts outperform strangles across all time periods
- 2020 (COVID) and 2022 (bear) are the hardest years for all strategies

## Archive

- `archive/equity_strategy/` — SPY equity signal optimization (strategy.py, prepare.py)
- `archive/options_marketdata/` — 1-year options experiments using marketdata.app API

## Environment

- `MARKETDATA_API_TOKEN` in `.env` — only needed for archived marketdata.app scripts
