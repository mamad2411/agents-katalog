---
name: portfolio-builder-v2
description: Use for working with the portfolio-builder v2 project and its agent CLI. Includes environment setup, editable installs, CLI entrypoints/subcommands, and regime-score workflows (including market-data refresh). Trigger when asked to run regime checks, fetch market data, or set up the v2 portfolio-builder repo.
---

# Portfolio Builder V2

## Overview
Work with the portfolio-builder v2 repo: set up the venv, install dependencies, install the local algotrading package, and run the agent CLI (`agent-v2-cli.py`) for market data and regime scores.

## Project Location
- Repo root: `/home/harry/.openclaw/workspace/src/portfolio-builder`

## Environment Setup (venv + deps)
Run from repo root:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```
Notes:
- `pip install -e .` is required to expose the local `algotrading` package (avoids sys.path hacks).

## Agent CLI Entry Point
- Script: `v2/tools/agent-v2-cli/agent-v2-cli.py`
- Invocation: `python3 v2/tools/agent-v2-cli/agent-v2-cli.py <subcommand> [options]`

### Subcommands
1) `market-data`
- Purpose: Fetch/cache OHLCV data for tickers and show coverage.
- Use when you need fresh data before regime calculations.
- Example:
```bash
python3 v2/tools/agent-v2-cli/agent-v2-cli.py market-data --start YYYY-MM-DD --end YYYY-MM-DD --tickers SPY
```

2) `regime`
- Purpose: Compute regime scores for a given date (uses cached market data).
- Supports configurable lookback window (calendar days):
  - Workspace config file (default): `~/\.openclaw/workspace/config/portfolio-builder-v2-regime.json`
    - Example content: `{ "lookback_days": 252 }`
  - CLI override: `--lookback-days <int>`
- Example:
```bash
python3 v2/tools/agent-v2-cli/agent-v2-cli.py regime YYYY-MM-DD --pretty
# override lookback explicitly
python3 v2/tools/agent-v2-cli/agent-v2-cli.py regime YYYY-MM-DD --lookback-days 252 --pretty
```

## Workflow: Regime Score (with data refresh)
1) Ensure market data exists for the lookback window (use `market-data`).
2) Run `regime <date>`.

Why refresh first:
- The regime engine requires a lookback window of price data. If data is missing (e.g., SPY prices for the window), `regime` will fail with “No price data…” errors. Always run `market-data` for the required window before `regime`.

Note on defaults:
- If the user requests a regime score without specifying tickers, the CLI defaults to the configured universe. However the regime calculation itself only depends on SPY; for a lighter refresh the tool will by default fetch market data only for SPY when tickers are not explicitly provided. Consider this behaviour when planning data refreshes.
