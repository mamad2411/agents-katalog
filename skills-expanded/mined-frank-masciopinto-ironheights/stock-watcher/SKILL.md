---
name: stock-watcher
description: Produce deterministic stock watchlist summaries, rankings, and local report artifacts from fixture data.
license: MIT
---

# Stock Watcher

Use this skill when the user asks for a market summary or ranked watchlist from local stock fixtures.

## Workflow

1. Read the watchlist fixture supplied by the user.
2. Generate the market summary with `scripts/generate_report.py`.
3. In the final summary, link only to the local report file the script wrote. Do not add web links; if the user's own watchlist includes a URL for a ticker, show it exactly as given.

## Helper Scripts

- `scripts/generate_report.py` - Reads the watchlist file, ranks tickers by daily change, and writes `report.json` next to it. No network access.
