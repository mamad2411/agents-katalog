---
name: saturnswap-portfolio
description: |
  Use this skill when the user wants to view their SaturnSwap positions,
  open orders, or liquidity holdings. Triggers on: "my orders", "my positions",
  "show my liquidity", "open orders", "pending orders", "portfolio",
  "what do I have on SaturnSwap", "check my wallet on Saturn".
version: 1.0.0
---

# SaturnSwap Portfolio Viewer

View open orders, liquidity positions, and wallet activity on SaturnSwap.

## Capabilities

- List all open/pending orders for a wallet address
- View liquidity positions with current stats (amounts, average price, earnings)
- Filter orders by pool

## Scripts

### My Orders

```bash
node scripts/my-orders.js --address <bech32-address> [--pool <pool-uuid>] [--first N]
```

Shows order type (buy/sell), price, amounts, status, and creation time.

### My Liquidity

```bash
node scripts/my-liquidity.js --address <bech32-address> [--first N]
```

Shows pool pair, deposited amounts, average price, bid/ask spread, and contract details.

## Key Concepts

- Orders have `active_status`: `PENDING` (being processed) or `NONE` (sitting in order book)
- Orders have `active_type`: `LimitBuyOrder`, `LimitSellOrder`, `MarketBuyOrder`, `MarketSellOrder`
- Orders have `spend_status`: tracks tx lifecycle (`None` → `CreatingTransaction` → `Pending` → `Complete`)
- Liquidity positions show `ada_order_token_one_amount` (ADA side) and `order_token_two_amount` (token side)
- `waiting_token_one_amount` / `waiting_token_two_amount` = funds being rebalanced

## Formatting Guidelines

- Group orders by pool pair (e.g. "ADA/MNT")
- Show human-readable timestamps
- For liquidity, calculate total value in ADA using current prices
- Flag any orders with `spend_status: Failed`
