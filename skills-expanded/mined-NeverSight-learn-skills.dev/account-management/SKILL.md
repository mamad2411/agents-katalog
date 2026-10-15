---
name: account-management
description: Manage GRVT trading account — check balances, positions, margin, and trade history. Use when the user asks about their portfolio, PnL, or account status.
---

# GRVT Account Management

## When to Use

Use this skill when the user wants to:
- Check account balance or portfolio value
- View open positions and unrealized PnL
- Manage position margin (add margin, check limits)
- View trade/fill history
- Check funding payment history

## Prerequisites

```bash
pip install grvt-pysdk
```

All account endpoints require authentication. GRVT has two types of API keys:

```bash
# Trading API Key — for balances, positions, trade history
export GRVT_TRADING_API_KEY="<Trading API Key from GRVT exchange UI>"
export GRVT_TRADING_PRIVATE_KEY="<private key associated with Trading API Key>"

# Funding API Key — for funding account transfers
export GRVT_FUNDING_API_KEY="<Funding API Key from GRVT exchange UI>"
export GRVT_FUNDING_PRIVATE_KEY="<private key associated with Funding API Key>"

export GRVT_ENV="testnet"  # or "prod"
```

Both key types can be created at:
- Production: https://exchange.grvt.io/exchange/account/api-keys
- Testnet: https://exchange.testnet.grvt.io/exchange/account/api-keys

**This skill primarily uses `GRVT_TRADING_API_KEY`. Use `GRVT_FUNDING_API_KEY` only for funding account transfers.**

## SDK Setup

Login to auto-detect `trading_account_id` and `funding_account_address`:

```python
import os
import requests
from pathlib import Path
from pysdk.grvt_ccxt import GrvtCcxt
from pysdk.grvt_ccxt_env import GrvtEnv

# Load .env file if present
env_file = Path(".env")
if env_file.exists():
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())

env = os.getenv("GRVT_ENV", "testnet")
base = "edge.testnet.grvt.io" if env == "testnet" else "edge.grvt.io"

# Login with Trading API Key
login_resp = requests.post(
    f"https://{base}/auth/api_key/login",
    json={"api_key": os.getenv("GRVT_TRADING_API_KEY")},
).json()
trading_account_id = login_resp["sub_account_id"]
funding_account_address = login_resp["funding_account_address"]

api = GrvtCcxt(
    env=GrvtEnv.TESTNET if env == "testnet" else GrvtEnv.PRODUCTION,
    parameters={
        "api_key": os.getenv("GRVT_TRADING_API_KEY"),
        "trading_account_id": trading_account_id,
        "private_key": os.getenv("GRVT_TRADING_PRIVATE_KEY"),
    },
)

# For funding account operations, login with Funding API Key instead:
# login_resp = requests.post(
#     f"https://{base}/auth/api_key/login",
#     json={"api_key": os.getenv("GRVT_FUNDING_API_KEY")},
# ).json()
```

## Account Balance

```python
# Get account balance
balance = api.fetch_balance()
# Top-level keys: info, timestamp, datetime, total, free, used, USDT
print(f"USDT Total: {balance['total']['USDT']}")
print(f"USDT Free:  {balance['free']['USDT']}")
print(f"USDT Used:  {balance['used']['USDT']}")

# Detailed info per currency in balance["info"]
for entry in balance["info"]:
    print(f"{entry['currency']}: balance={entry['balance']}, unrealized_pnl={entry['unrealized_pnl']}")
```

## Account Summary

```python
# Sub-account summary — balances, margin usage, equity
summary = api.get_account_summary(type="sub-account")

# Aggregated summary across all sub-accounts
agg_summary = api.get_account_summary(type="aggregated")
```

## Positions

```python
# Fetch all open positions
positions = api.fetch_positions()

# Fetch positions for specific symbols
positions = api.fetch_positions(symbols=["BTC_USDT_Perp", "ETH_USDT_Perp"])

for pos in positions:
    side = "long" if float(pos["size"]) > 0 else "short"
    print(f"{pos['instrument']}: size={pos['size']} side={side}")
    print(f"  Entry: {pos['entry_price']}, Mark: {pos['mark_price']}")
    print(f"  Unrealized PnL: {pos['unrealized_pnl']}, ROI: {pos['roi']}%")
    print(f"  Leverage: {pos['leverage']}x, Margin: {pos['margin_type']}")
```

## Position Margin Management

```python
# Add margin to a position (reduce liquidation risk)
api.add_position_margin(
    symbol="BTC_USDT_Perp",
    amount=100,  # Additional USDT margin
)

# Check margin limits
limits = api.get_position_margin_limits(symbol="BTC_USDT_Perp")
```

## Trade / Fill History

```python
# Recent fills
fills = api.fetch_my_trades(symbol="BTC_USDT_Perp", limit=50)
for fill in fills:
    side = "buy" if fill.get("is_taker_buyer") else "sell"
    print(f"{side} {fill['size']} @ {fill['price']} — trade_id: {fill['trade_id']}")
```

## Funding Payment History

```python
# Check funding payments received/paid on perpetual positions
funding = api.fetch_funding_payment_history(symbol="BTC_USDT_Perp", limit=24)
for f in funding:
    print(f"Payment: {f['amount']} at {f['datetime']}")
```

## Account History

```python
# Full account history (deposits, withdrawals, transfers, settlements)
history = api.fetch_account_history()
```

## Common Patterns

### Portfolio Overview

```python
def portfolio_overview(api):
    balance = api.fetch_balance()
    positions = api.fetch_positions()

    print(f"Account Balance: {balance['total']['USDT']} USDT")
    print(f"Available: {balance['free']['USDT']} USDT")
    print(f"\nOpen Positions ({len(positions)}):")
    total_pnl = 0
    for pos in positions:
        pnl = float(pos.get("unrealized_pnl", 0))
        total_pnl += pnl
        side = "long" if float(pos["size"]) > 0 else "short"
        print(f"  {pos['instrument']}: {pos['size']} ({side})")
        print(f"    Entry: {pos['entry_price']} | PnL: {pnl}")
    print(f"\nTotal Unrealized PnL: {total_pnl}")
```

## Important Notes

- All account data requires authentication — ensure env vars are set
- Position PnL is calculated against current mark price
- Funding payments occur at regular intervals on perpetual positions (typically every 8 hours)
- Use `GrvtEnv.TESTNET` for testing before production
