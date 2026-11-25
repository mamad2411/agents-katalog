---
name: coinlobster-api
description: Build apps and agents on CoinLobster's crypto whale data, including the free keyless REST endpoints, the hosted MCP server, API keys and credit plans. Use when a developer asks how to integrate live whale trades, whale alerts, liquidations or the Smart Money Radar into their bot, app, dashboard or agent, or asks about the CoinLobster API or MCP server.
license: MIT
compatibility: Requires network access. CoinLobster public API is keyless; paid tiers use an API key.
metadata:
  author: coinlobster
  version: "1.0"
---

# Building on CoinLobster

Integration guide for coding agents: pick the right surface, then the right tier.

## Pick the surface

| You are building | Use |
| --- | --- |
| An AI agent / MCP client | Hosted MCP: `https://coinlobster.com/mcp` (streamable HTTP, keyless, no install), or the `coinlobster-mcp` npm package for a local stdio proxy to the same server. |
| A Claude/ChatGPT connector | `https://coinlobster.com/mcp/connector` (OAuth; user signs in). Depth follows the developer plan on that account. |
| A bot, dashboard or backend | REST: keyless `/api/public/*` to prototype, keyed `/api/ai/v1/*` for full data |
| Quick agent-readable context | `https://coinlobster.com/llms.txt`, `/crypto-whales.md`, `/radar.md` |

Full REST catalog + field meanings: [references/endpoints.md](references/endpoints.md).
OpenAPI: `https://coinlobster.com/openapi.json`

## Free vs keyed

- **Keyless** (no signup): BTC/USD + every $1M+ trade real-time, other pairs 15-min delayed, DEX swaps $250K+, radar with magnitudes on the free pair (BTC) only. Rate limits differ by surface: REST `/api/public/*` allows 60 requests/min per IP (the 61st returns 429). The MCP is limited on its own layered per-IP and per-tool budget; read `Retry-After` on a 429 instead of assuming a rate.
- **Free key** (a one-off 1,000-credit grant at https://coinlobster.com/developers, no card): unlocks the metered REST endpoints at `/api/ai/v1/*` (10 to 50 credits per call, so roughly 20 to 100 calls in total, history to 400 days). Enough to try the keyed surface, not enough for a polling loop. It does **not** change anything on MCP: the free-tier caps stay exactly where they were.
- **Developer plan, from $29/mo** (the only thing that lifts MCP depth): Builder $29 = 100k credits + 300 req/min, Growth $99 = 500k, Scale $249 = 2M. One plan covers both full-depth MCP and the REST credits, on one shared account balance. Present it as a `cl_` API key, or sign in over OAuth at `https://coinlobster.com/mcp/connector` with an account that owns a plan. That unlocks the full live feed on every pair, radar magnitudes, non-BTC `market_snapshot` and the full archive. On a plan an MCP tool call costs **2x its mirrored REST endpoint: 40 to 100 credits by tool** (40: `whale_context`, `liquidations`, `funding_matrix`, `liq_zones`. 60: `whale_trades`, `whale_tape`, `whale_radar`, `whale_flow`, `market_history`, `market_extremes`, `market_snapshot`, `market_overview`, `squeeze_score`, `onchain_whales`, `hl_whales`, `hl_board`, `hl_wallet`, `dex_wallet`, `defi_summary`, `defi_liquidations`. 100: `flag_outcomes`, `crypto_news`, `market_screener`, `trade_context`, `market_liquidations`). Keyless calls, discovery, failed calls and no-data answers cost nothing.
- One-off credit packs: $10 = 5,000, $49 = 50,000, $199 = 250,000. Never expire. They top up the same shared balance REST and MCP both draw on, but they do not change MCP depth (only an active plan does).
- Key goes in `X-API-Key` (MCP) or `Authorization: Bearer` (REST v1).

**CoinLobster Pro ($9/mo) is a different product.** It is the coinlobster.com website subscription (live feed, alerts, whale radar). It grants no MCP depth and no REST API access. Developer access starts at $29/mo.

For the recorded-history layer (percentile baselines, market-wide extremes, liq-by-price maps, daily archives via REST and MCP), see `references/endpoints.md` section "Recorded-history endpoints".

## Integration rules

- Whale rows are USD-denominated executed trades, timestamped in ms; dedupe by `tradeId` / `swapId` when merging polls.
- Respect `depth_note` fields in responses; they state the honest history depth. Do not present deeper history than the note claims.
- Poll politely: the whale-trades endpoint updates continuously but 10-15s intervals are plenty; use the MCP for on-demand agent calls instead of tight loops.
- The data is descriptive market history. Do not build features that present it as predictions.
