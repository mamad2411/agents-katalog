---
name: strike-perpetuals
description: |
  Use this skill when the user wants to trade perpetuals or leveraged positions
  on Cardano via Strike Finance. Triggers on: "open a long", "short ADA",
  "leverage trade", "perpetuals", "Strike Finance", "open position",
  "close position", "stop loss", "take profit", "leveraged", "perps".
  Strike v2 API uses Ed25519 signature auth — requires API wallet setup.
  Use strike-perpetuals-operator to execute trades.
version: 2.0.0
---

# Strike Finance v2 Perpetuals

Trade leveraged long/short positions via Strike's v2 order-book API.

## Prerequisites

Strike v2 requires an **API Wallet** (Ed25519 key pair):
1. Generate key pair at https://app.strikefinance.org/api-keys
2. Set `STRIKE_API_PUBLIC_KEY` and `STRIKE_API_PRIVATE_KEY` env vars
3. Fund your Strike account via their deposit flow

## Capabilities

- View exchange info (all trading pairs and rules)
- View order book depth for any pair
- Get open/closed positions
- Place market, limit, stop, and strategy (TP/SL) orders
- Set leverage (1-125x) and margin mode (cross/isolated)
- Cancel orders

## Trading Pairs

Pairs follow `{ASSET}-USD` format: `ADA-USD`, `BTC-USD`, `ETH-USD`, `SOL-USD`, etc.
Use `exchange-info.js` to see all available pairs and their rules.

## Scripts

### Exchange Info (no auth)

```bash
node scripts/exchange-info.js
```

### Order Book (no auth)

```bash
node scripts/order-book.js --symbol ADA-USD [--limit 20]
```

### My Positions (auth required)

```bash
node scripts/my-positions.js [--symbol ADA-USD]
```

### Place Order (auth required)

```bash
node scripts/place-order.js --symbol ADA-USD --side buy --type market --size 100
node scripts/place-order.js --symbol ADA-USD --side buy --type limit --size 100 --price 0.45
```

### Strategy Order with TP/SL

```bash
node scripts/strategy-order.js --symbol ADA-USD --side buy --type market --size 100 --tp-price 0.50 --sl-price 0.40
```

### Set Leverage

```bash
node scripts/set-leverage.js --symbol ADA-USD --leverage 10
```

## Key Concepts

- **Order types**: market, limit, stop, stop_limit, take_profit, take_profit_limit
- **Time-in-force**: GTC (good-til-cancel), IOC (immediate-or-cancel), FOK (fill-or-kill)
- **Leverage**: 1-125x, set per symbol (affects new positions only)
- **Margin modes**: cross (shared margin) or isolated (per-position margin)
- **Auth**: Ed25519 signed headers — no CBOR/on-chain tx needed
- **Sizes**: In contract units (check exchangeInfo for precision)

## Safety Rules

- Always show current position before placing opposing orders
- Warn on leverage >10x
- Show liquidation price estimate
- Require confirmation before order placement
- Check exchangeInfo for min/max order sizes and tick sizes
