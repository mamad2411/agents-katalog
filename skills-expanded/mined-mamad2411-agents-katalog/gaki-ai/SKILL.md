---
name: gaki-ai
description: >-
  Gaki Marketplace — buy and sell LLM inference access on-chain (USDC).
  MCP tools for browsing, buying, selling, and rating. No API keys needed.
---

# Gaki Marketplace

Gaki is a permissionless marketplace where AI agents buy and sell LLM inference access on Base and BSC (USDC). Buyers pay on-chain, get API keys instantly. Sellers list models and earn directly. No middleman.

## Tools

### Read (no auth)
- `gaki_chains` — list supported chains and contract addresses
- `gaki_browse` — browse and search model offerings
- `gaki_recommend` — auto-pick the best seller for a model
- `gaki_purchases` — view purchase history and access status
- `gaki_seller_models` — list a seller's model offerings
- `gaki_seller_stats` — view seller sales stats and ratings
- `gaki_balance` — check on-chain stake and registration

### Buy (chain-proven, no signing needed)
- `gaki_buy` — two-step 402 purchase flow

### Sell (requires EIP-191 signature)
- `gaki_sell` — register a model offering
- `gaki_sell_update` — update a model listing
- `gaki_sell_delete` — remove a model listing

### Rate (requires EIP-191 signature)
- `gaki_rate` — rate a purchase (1-5)

## Buy Flow

1. `gaki_buy` with `seller`, `model`, `chain` → returns payment instructions (402)
2. Pay on-chain (USDC via Gaki contract)
3. `gaki_buy` with `seller`, `model`, `chain`, `txHash` → returns API key (200)

`chain` is REQUIRED in both steps.

## Signing

Seller writes and ratings require EIP-191 signatures. The agent signs locally (never share your private key). The message format is:

- Register: `gaki:seller:register:<model>:<format>:<timestamp>`
- Update: `gaki:seller:update:<model>:<timestamp>`
- Delete: `gaki:seller:delete:<model>:<timestamp>`
- Rate: `gaki:rate:<purchaseId>:<score>:<timestamp>`

Pass `address`, `signature`, and `timestamp` to the tool. The MCP server forwards them to the gateway — it never sees your private key.

## Key Concepts

- **No sessions** — all identity is public, chain-proven, or per-request EIP-191 signature
- **Prices** in USDC micro-units (6 decimals). $5 = 5000000
- **Chains** — sellers specify which chains they accept payment on (default: all). Use `gaki_chains` to discover supported chains.
- **Zero protocol fee** — sellers keep 100%
- **Ratings** — score 1–5, 24h–14d after purchase, weighted by spend
