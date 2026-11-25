---
name: saturnswap-limit-orders
description: |
  Use this skill when the user wants to place or cancel limit orders on SaturnSwap.
  Triggers on: "place a limit order", "set a buy order at", "limit buy", "limit sell",
  "cancel my order", "cancel order", "set price to buy MNT at",
  "place a bid at", "create sell order". Use saturnswap-limit-orders-operator to execute.
version: 1.0.0
---

# SaturnSwap Limit Orders

Guide users through placing and cancelling limit orders on SaturnSwap.

## Capabilities

- Place limit buy orders (bid ADA for tokens at a target price)
- Place limit sell orders (offer tokens at a target ADA price)
- Cancel existing open orders
- Preview order placement against current order book

## Place Limit Order Flow

1. **Find the pool** — look up by ticker or policy ID
2. **Check current prices** — show best bid/ask and current price
3. **Calculate amounts** — user specifies price and quantity
4. **Build transaction** — call `createLimitOrder`
5. **Hand off to operator** — for signing and submission

## Cancel Order Flow

1. **List open orders** — use `getUserOrders` to find active orders
2. **Confirm which orders to cancel** — get explicit user approval
3. **Build cancel transaction** — call `cancelOrder` with UTxO IDs
4. **Hand off to operator** — for signing and submission

## Scripts

### Preview Limit Order

```bash
node scripts/preview-limit.js --pool <uuid> --side buy|sell --price <ada-per-token> --amount <display-units>
```

### Create Limit Order Transaction

```bash
node scripts/create-limit.js --address <bech32> --pool <uuid> --policy <policyId> --asset <assetName> --sell <amount> --buy <amount>
```

### Create Cancel Transaction

```bash
node scripts/create-cancel.js --address <bech32> --utxo-ids <id1,id2,...>
```

## Key Concepts

- **Limit buy**: You sell ADA to buy tokens at your target price or better
  - `policyId`/`assetName` = "" (selling ADA), `tokenAmountSell` = ADA amount, `tokenAmountBuy` = tokens you want
- **Limit sell**: You sell tokens to get ADA at your target price or better
  - `policyId`/`assetName` = token's policy/asset, `tokenAmountSell` = tokens, `tokenAmountBuy` = ADA you want
- Price = `tokenAmountBuy / tokenAmountSell` (or vice versa depending on direction)
- All amounts in **display units**

## Safety Rules

- Always show the effective price and compare to current market price
- Warn if limit price is >20% away from market (possible mistake)
- Require confirmation before creating the transaction
- For cancels, show order details before confirming
