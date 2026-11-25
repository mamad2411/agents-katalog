---
name: stock-watchlist
description: Manage a stock/crypto watchlist with price target and stop-loss alerts via AIsa API. Add, remove, list, and check tickers with live price alerts. Use when the user wants to track stocks, set price alerts, manage a watchlist, or check triggered alerts.
compatibility: Designed for Agent Skills compatible clients such as OpenClaw, Claude Code, Hermes, and GitHub-backed skill catalogs. Requires system binaries python3, environment variables AISA_API_KEY and internet access to api.aisa.one.
metadata:
  author: AIsa
  version: 1.0.0
  homepage: https://aisa.one
  repository: https://github.com/baofeng-tech/agent-skills
  tags: stock,aisa
  platforms: agentskills.io,agentskill.sh,github
  primary_env: AISA_API_KEY
allowed-tools: Read
---

# Watchlist Management — AIsa Edition

Manage a watchlist with price target and stop-loss alerts using the AIsa API.

## Usage

```bash
# Add a ticker with price target and stop-loss
python3 scripts/watchlist.py add AAPL --target 220 --stop 160

# Add with signal-change alert
python3 scripts/watchlist.py add AAPL --alert-on signal

# List all watchlist items
python3 scripts/watchlist.py list

# Check live prices and trigger alerts
python3 scripts/watchlist.py check

# Check with notification
python3 scripts/watchlist.py check --notify

# Remove a ticker
python3 scripts/watchlist.py remove AAPL
```

### Actions

| Action | Description |
|--------|-------------|
| `add TICKER` | Add ticker with optional `--target`, `--stop`, `--alert-on signal` |
| `remove TICKER` | Remove ticker from watchlist |
| `list` | Show all watchlist items |
| `check` | Fetch live prices and check alerts |

## Data Storage

Watchlist data is stored in `./.claude-skill-data/watchlist.json` for persistence across sessions.

**NOT FINANCIAL ADVICE.** For informational purposes only.
