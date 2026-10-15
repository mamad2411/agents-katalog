---
name: saturnswap-pools
description: |
  Use this skill when the user asks about SaturnSwap pools, trading pairs,
  order books, token prices, or wants to find a specific pool. Triggers on:
  "show me pools", "find the MNT pool", "what pools are on SaturnSwap",
  "order book for", "best bid/ask", "token price", "pool TVL", "pool volume".
version: 1.0.0
---

# SaturnSwap Pool Discovery & Order Book

Query pools, order books, and token metadata on SaturnSwap DEX (Cardano).

## Capabilities

- List pools sorted by volume or TVL
- Look up a specific pool by ID or token pair (policyId + assetName)
- View order book (bids and asks) for any pool
- Search token projects by ticker, policy ID, or market cap

## API Reference

All queries hit `https://api.saturnswap.io/v1/graphql/` — see `shared/saturnswap-api.md` for conventions.

## Scripts

### List Pools

```bash
node scripts/list-pools.js [--first N] [--order volume_24h|tvl] [--ticker MNT]
```

Returns pool ID, token pair tickers, 24h/7d/30d volume, and TVL.

### Get Pool Details

```bash
node scripts/get-pool.js --id <pool-uuid>
node scripts/get-pool.js --policy <policyId> --asset <assetName>
```

### Order Book

```bash
node scripts/order-book.js --pool <pool-uuid> [--side asks|bids|both] [--first N]
```

### Search Tokens

```bash
node scripts/search-tokens.js [--ticker MNT] [--first N] [--order market_cap|volume_24h]
```

## Key Concepts

- Every pool pairs ADA (`token_project_one`) with another token (`token_project_two`)
- Prices are in ADA per token
- `lowest_ask_price` = cheapest sell order; `highest_bid_price` = best buy offer
- All amounts in the API use **display units** (5 ADA, not 5000000 lovelace)
- Pools are identified by UUID; tokens by `policy_id` + `asset_name`

## Formatting Guidelines

When presenting pool data to users:
- Show token tickers (e.g. "ADA/MNT") not raw policy IDs
- Format volumes with commas and 2 decimal places
- Sort by volume or TVL descending by default
- Include spread (ask - bid) when showing order books
