---
name: kraken
description: "Interact with the Kraken cryptocurrency exchange. Use when: (1) checking crypto prices or market data, (2) viewing account balances or trade history, (3) placing or cancelling orders, (4) building DCA strategies or price alerts, (5) any mention of Kraken, crypto trading, or portfolio management. Requires the tentactl binary."
metadata:
  {
    "openclaw":
      {
        "emoji": "🐙",
        "requires": { "bins": ["tentactl"] },
        "install":
          [
            {
              "id": "cargo",
              "kind": "cargo",
              "package": "tentactl",
              "bins": ["tentactl"],
              "label": "Install tentactl (cargo)",
            },
          ],
      },
  }
---

# Kraken Exchange

CLI tool for the Kraken crypto exchange. Speaks MCP over stdio but use it directly via exec for simplicity.

## Setup

First run only — configure API keys from 1Password or manually:

```bash
# Option A: 1Password (recommended)
scripts/setup-keys.sh

# Option B: Manual .env file
echo "KRAKEN_API_KEY=your-key" > ~/.kraken-mcp.env
echo "KRAKEN_API_SECRET=your-secret" >> ~/.kraken-mcp.env
chmod 600 ~/.kraken-mcp.env
```

## Usage

All commands go through `scripts/kraken.sh` (loads .env, finds binary) or `python3 scripts/kraken.py` directly:

```bash
# Market data (no auth needed)
scripts/kraken.sh get_ticker '{"pair":"XBTUSD"}'
scripts/kraken.sh get_orderbook '{"pair":"ETHUSD","count":5}'
scripts/kraken.sh get_ohlc '{"pair":"SOLUSD","interval":60}'

# Account (needs API keys)
scripts/kraken.sh get_balance
scripts/kraken.sh get_trade_history
scripts/kraken.sh get_open_orders

# Trading (needs API keys) ⚠️ REAL MONEY
scripts/kraken.sh place_order '{"pair":"XBTUSD","direction":"buy","order_type":"market","volume":"0.001","validate":true}'
scripts/kraken.sh cancel_order '{"txid":"TXID-123"}'
```

If binary is already in PATH and env vars are set, use `python3 scripts/kraken.py` directly with the same arguments.

## Tools Reference

See `references/tools.md` for full parameter docs.

## Safety Rules

- **ALWAYS** use `validate: true` first when placing orders
- **ALWAYS** confirm with the user before placing real orders
- **NEVER** place orders without explicit user approval
- Market orders execute IMMEDIATELY — prefer limit orders when possible
- Display the validation result and ask for confirmation before removing `validate`

## Trading Pairs

Kraken uses its own pair format: `XBTUSD` (not BTCUSD), `XETHZUSD`, `SOLUSD`, etc. When unsure, try the pair — the API returns a clear error for invalid pairs.

## Automation Patterns

### DCA (Dollar Cost Average)
Set up via openclaw cron:
```
openclaw cron add --schedule "0 9 * * 1" --task "Buy $50 of BTC on Kraken using the kraken skill. Use validate first, then execute."
```

### Price Alerts
Check in heartbeat or cron, notify if threshold crossed. Store alert config in `memory/kraken-alerts.json`.
