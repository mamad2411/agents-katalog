---
name: stock-portfolio
description: Manage investment portfolios with live P&L tracking via AIsa API. Create, add, update, remove positions, rename, and show portfolio summary with real-time profit/loss. Use when the user wants to track investments, manage a portfolio, check P&L, or add/remove holdings.
compatibility: Designed for Agent Skills compatible clients such as OpenClaw, Claude Code, Hermes, and GitHub-backed skill catalogs. Requires system binaries python3, environment variables AISA_API_KEY and internet access to api.aisa.one.
metadata:
  author: AIsa
  version: 1.0.0
  homepage: https://aisa.one
  repository: https://github.com/baofeng-tech/agent-skills
  tags: stock,aisa
  platforms: agentskills.io,agentskill.sh,github
  primary_env: AISA_API_KEY
allowed-tools: Read Bash Grep
---

# Portfolio Management — AIsa Edition

Manage investment portfolios with live P&L tracking using the AIsa API.

## Usage

```bash
# Create a new portfolio
python3 scripts/portfolio.py create "My Portfolio"

# Add a position
python3 scripts/portfolio.py add AAPL --quantity 10 --cost 150
python3 scripts/portfolio.py add BTC-USD --quantity 0.5 --cost 40000

# Show portfolio with live P&L
python3 scripts/portfolio.py show
python3 scripts/portfolio.py show --portfolio "My Portfolio"

# Update a position
python3 scripts/portfolio.py update AAPL --quantity 15 --cost 160

# Remove a position
python3 scripts/portfolio.py remove AAPL

# List all portfolios
python3 scripts/portfolio.py list

# Rename a portfolio
python3 scripts/portfolio.py rename "My Portfolio" "Tech Holdings"

# Delete a portfolio
python3 scripts/portfolio.py delete "Old Portfolio"
```

### Actions

| Action | Description |
|--------|-------------|
| `create NAME` | Create a new portfolio |
| `list` | List all portfolios |
| `show` | Show portfolio summary with live P&L |
| `add TICKER` | Add position with `--quantity` and `--cost` |
| `update TICKER` | Update position quantity/cost |
| `remove TICKER` | Remove position from portfolio |
| `rename OLD NEW` | Rename a portfolio |
| `delete NAME` | Delete a portfolio |

## Data Storage

Portfolio data is stored in `./.claude-skill-data/portfolios.json` for persistence across sessions.

**NOT FINANCIAL ADVICE.** For informational purposes only.
