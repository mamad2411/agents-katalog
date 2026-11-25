---
name: momentum
description: Scans for momentum and breakout candidates (RSI > 70) and evaluates them for trend-following.
license: Apache-2.0
metadata:
  version: v1
  publisher: arnoudhgz
---

# Momentum / Breakout advice

This workflow finds stocks with extreme relative strength (RSI > 70) to buy into momentum, contrasting with the mean-reversion base strategy.

## Step 1: Market posture
Check the overall market posture (WebSearch "stock market today..."). In bear markets, momentum strategies often fail.

## Step 2: Screen candidates
Run `python3 scripts/screen.py momentum --min-rsi 70 --exclude-held --exclude-advised`. Ensure all candidates adhere to STRATEGY.md.

## Step 3: Candidate pre-fetch
For the top 10 candidates, run:
- `python3 scripts/screen.py quote TICKER [TICKER...]`
- `python3 scripts/screen.py forecast TICKER [TICKER...]`
- `python3 scripts/screen.py news TICKER [TICKER...] --red-flags`

## Step 4: Research
Use parallel `stock-researcher` agents to evaluate the momentum strength. Focus on volume, 52-week highs, and breakout technicals instead of "oversold" metrics.

## Step 5: Table and Logging
Format exactly like the standard advice table.
Log the picks with `python3 scripts/advice_log.py add-pick TICKER --source momentum ...`
Run the auto-backup: `python3 scripts/autosync.py "momentum run"`
