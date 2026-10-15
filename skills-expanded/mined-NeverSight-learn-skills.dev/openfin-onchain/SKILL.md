---
name: openfin-onchain
description: Multi-chain on-chain token data — metadata, wallet portfolios, balances, and USD prices — across 100+ EVM and Solana networks via the OpenFinance /agent/onchain/* routes (Uniblock-backed). Use whenever an agent needs to look up what a token is, what an arbitrary address holds, or what something costs in USD before quoting / trading / displaying. Triggers&#58; "what is token 0x...", "lookup token name and decimals", "show me wallet 0x... portfolio", "what does this address hold", "USDC balance on Polygon / Base / Arbitrum / Optimism", "price of ETH / WBTC / SOL right now", "USD price of <contract>", "batch token metadata", "batch USD prices", "is this contract a token", "wallet NFTs", "wallet holdings on chainId X". Covers GET /agent/onchain/token/metadata, GET /agent/onchain/token/portfolio (native + fungibles + NFTs), GET /agent/onchain/token/balances (lighter — no NFTs, paginated), GET /agent/onchain/token/price (single or comma-separated batch). Read-only; no signing. Each call requires `x-api-key&#58; open_…`. Prerequisite&#58; openfin-setup. Pair with openfin-relay when the user wants to act on what they hold.
---

# Onchain Token Data

Read-only multi-chain token data through OpenFinance, backed by Uniblock.
Use this when an agent needs to know **what a token is**, **what an
address holds**, or **what something is worth in USD** before quoting,
trading, or displaying anything.

No signing, no wallet writes, no on-chain side effects — just enriched
reads across 100+ chains (every major EVM, Solana, Bitcoin, Tron, etc.).

## Prerequisite

1. User completed `openfin-setup` (API key in place — `open_…`).
2. All endpoints take `x-api-key: open_…`.

## Endpoints

### Token metadata

**`GET /agent/onchain/token/metadata`** — Resolve one or many token
contracts into human-readable info: `name`, `symbol`, `logo` URL,
`decimals`, `address`, `chainId`. Use before showing a token to a user,
or to look up `decimals` before formatting an on-chain raw balance.

| Param | Required | Notes |
|---|---|---|
| `chainId` | ✓ | `"1"` Ethereum, `"137"` Polygon, `"42161"` Arbitrum, `"8453"` Base, `"solana"`, etc. |
| `tokenAddress` | ✓ | Single contract, comma-separated for batch, or `"native"` |
| `includeRaw` | optional | Returns provider-raw payload (disables backup providers) |
| `provider` | optional | Force `Alchemy` / `GoldRush` / `Moralis` / `Tatum` / `Helius` / `SolScan` / `Shyft` / `Uniblock` |

### Address portfolio (native + fungibles + NFTs)

**`GET /agent/onchain/token/portfolio`** — Full holdings snapshot for
one wallet on one chain. Returns native balance, every fungible token,
and the NFT collection. Heavier than `/balances` because it enumerates
NFTs.

| Param | Required | Notes |
|---|---|---|
| `chainId` | ✓ | |
| `walletAddress` | ✓ | |
| `includePrice` | optional | Attach USD values to fungibles |
| `includeMetadata` | optional | Attach `name` / `symbol` / `logo` / `decimals` |
| `includeRaw`, `provider` | optional | |

Use when the agent needs the **complete** view ("show me everything in
this wallet"). For trade-prep checks, prefer `/balances` — it's faster.

### Address token balances (no NFTs, paginated)

**`GET /agent/onchain/token/balances`** — Native + fungible token
balances. Returns `balance` (raw) and `formattedBalance`
(human-readable, decimals applied). Paginated via `cursor`.

| Param | Required | Notes |
|---|---|---|
| `chainId` | ✓ | |
| `walletAddress` | ✓ | |
| `includePrice` | optional | Attach USD values |
| `includeMetadata` | optional | Attach token metadata |
| `cursor` | optional | From a previous response for the next page |
| `includeRaw`, `provider` | optional | |

Use this before placing trades, computing USD totals, or letting the
agent reason about what to swap.

### Token USD price

**`GET /agent/onchain/token/price`** — Current USD spot price for one or
many tokens. Returns `usdPrice`, plus `name`, `symbol`, `decimals`,
`logo`, source `exchangeName` / `exchangeAddress`, `updatedAt`.

| Param | Required | Notes |
|---|---|---|
| `chainId` | ✓ | Comma-separated for cross-chain batch |
| `contractAddress` | ✓ | Single, comma-separated for batch, or `native` |
| `exchange` | optional | Pin to `uniswap-v2` / `uniswap-v3` / `sushiswap-v2` / `pancakeswap-v1` / `pancakeswap-v2` / `quickswap` |
| `provider` | optional | `Alchemy` / `GoldRush` / `Moralis` |
| `includeRaw` | optional | |

Use before quoting a swap, computing portfolio USD totals, or
suggesting trades.

## Common chain IDs

| Chain | ID |
|---|---|
| Ethereum | `1` |
| Polygon | `137` |
| Base | `8453` |
| Arbitrum | `42161` |
| Optimism | `10` |
| BSC | `56` |
| Linea | `59144` |
| Solana | `solana` |
| Bitcoin | `bitcoin` |

(Uniblock supports 100+; pass the chain ID/key it expects. For Relay
bridging, see `openfin-relay` — its chain IDs differ for non-EVM.)

## Picking the right endpoint

| Need | Use |
|---|---|
| "What is this contract?" | `/token/metadata` |
| "What's the USD price?" | `/token/price` |
| "What does this wallet hold?" (fungibles only) | `/token/balances` |
| "Show me everything" (incl. NFTs) | `/token/portfolio` |

Don't call `/portfolio` when `/balances` is enough — NFT enumeration is
slow and you usually don't need it.

## Example flow — value a wallet's USDC across chains

1. For each chain ID the user cares about (e.g. `1`, `137`, `8453`,
   `42161`):
   - `GET /agent/onchain/token/balances?chainId=<id>&walletAddress=<addr>&includePrice=true&includeMetadata=true`
2. Sum `formattedBalance * usdPrice` across the response's `balances`
   array.

For a single token across many chains, `/token/price` accepts
comma-separated `chainId` and `contractAddress` for one round trip.

## Don't

- Don't poll `/portfolio` per-chain when the user just wants balances
  — `/balances` is much lighter.
- Don't pass user-provided "1.5 ETH" as `amount`; this skill is
  read-only. For sends/swaps, see `openfin-relay`.
- Don't assume `decimals = 18`. Always read it from `/metadata` (some
  tokens are 6, 8, 9, etc. — USDC is 6, WBTC is 8, USDT on Ethereum
  is 6, on BSC is 18).
- Don't use this for live trading prices on illiquid pairs — pin
  `exchange` if you need a specific DEX, and prefer the asset's native
  market endpoint (`openfin-polymarket` for prediction markets,
  `openfin-hyperliquid` for perp/spot mids).

## MCP note

Tool names mirror the routes (`onchain_` prefix):

- `onchain_get_token_metadata`
- `onchain_get_address_portfolio`
- `onchain_get_address_token_balances`
- `onchain_get_token_usd_price`
