---
name: rwa-portfolio
description: >
  View portfolio holdings, P&L, allocation, and price history for tokenized stocks on Solana.
  Use when user asks about portfolio, holdings, positions, balance, allocation, P&L,
  24h change, price history, or chart data. Triggers: "show portfolio", "my holdings",
  "how much TSLA do I have", "price history SPY", "token performance".
---

# RWA Portfolio

View holdings, allocation, P&L, and price history for tokenized stocks on Solana.

## Prerequisites

Assume `rwa` is installed and in PATH. If "command not found", install:
```bash
curl -fsSL https://raw.githubusercontent.com/outputlayer/rwa_cli/main/install.sh | bash
```

Do NOT prepend `export PATH=...` to every command. The installer adds rwa to PATH automatically.

## Portfolio

```bash
# Own wallet (requires local wallet)
rwa --json gm portfolio

# Any public wallet address
rwa --json gm portfolio Dn9EqxugBePrno7gzCjbGeYxY3VJE9RB2WE2FH7t7qmH
```

### JSON Output

```json
{
  "wallet": "Dn9Eqx...",
  "sol": 19.33,
  "usdc": 19607.99,
  "positions": [
    {
      "token": "TSLAon",
      "balance": 0.26,
      "price": 385.0,
      "value_usd": 100.1,
      "alloc_pct": 15.2,
      "change_pct_24h": 1.2
    }
  ],
  "total_value_usd": 26612.0
}
```

Fields: `token`, `balance`, `price`, `value_usd`, `alloc_pct` (% of portfolio), `change_pct_24h`.

## Price History

```bash
rwa --json gm history TSLA              # Default: 1 month
rwa --json gm history TSLA -r 1D        # 1 day
rwa --json gm history TSLA -r 1W        # 1 week
rwa --json gm history TSLA -r 1M        # 1 month
rwa --json gm history TSLA -r 3M        # 3 months
rwa --json gm history TSLA -r 1Y        # 1 year
rwa --json gm history TSLA -r ALL       # All time
```

### JSON Output

```json
{
  "symbol": "TSLAON",
  "range": "1M",
  "candles": 527,
  "first": {"timestamp": 1708819200, "price": 407.04},
  "last": {"timestamp": 1711324800, "price": 385.75},
  "high": 419.42,
  "low": 356.83,
  "change_pct": -5.23
}
```

## Errors

- "Solana RPC unavailable" → retry in a few seconds, or set `RWA_RPC_URL`
- No positions shown → wallet may have no GM tokens, or check address is correct
