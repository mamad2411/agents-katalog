---
name: saturnswap-market-swap
description: |
  Use this skill when the user wants to perform a market swap on SaturnSwap.
  Triggers on: "swap ADA for", "buy MNT", "sell tokens for ADA",
  "market buy", "market sell", "swap on SaturnSwap", "trade on Saturn".
  This skill guides the user through the swap — use saturnswap-market-swap-operator
  to execute the actual transaction.
version: 1.0.0
---

# SaturnSwap Market Swap

Guide users through market buy/sell swaps on SaturnSwap DEX.

## Flow

1. **Find the pool** — look up by ticker or policy ID
2. **Check the order book** — show current best ask/bid and spread
3. **Preview the swap** — calculate expected output at current price
4. **Build the transaction** — call `createMarketSwap` with pool ID and amount
5. **Hand off to operator** — the operator skill handles signing and submission

## Scripts

### Preview Swap

```bash
node scripts/preview-swap.js --pool <pool-uuid> --amount <display-units> [--side buy|sell]
```

Fetches current price and estimates output. Does NOT create a transaction.

### Create Swap Transaction

```bash
node scripts/create-swap.js --address <bech32> --pool <pool-uuid> --amount <display-units> [--slippage 3]
```

Calls the API to build an unsigned transaction. Returns `transactionId` and `hexTransaction`.

## Safety Rules

- **Always show the user**: pool pair, amount in, estimated amount out, slippage, and any fees
- **Require explicit confirmation** before calling create-swap
- **Display units only** — 5 ADA means `tokenAmountSell: 5`, never 5000000
- Slippage defaults to 3% — warn if user sets >10%
- Check `error` field even on HTTP 200 responses

## Key Concepts

- Market swaps execute immediately against the order book
- `tokenAmountSell` is the input amount (what you're giving up)
- Selling ADA → buying tokens (market buy of the token)
- Selling tokens → getting ADA back (market sell of the token)
- After creation, the hex must be signed locally and submitted via the operator skill
