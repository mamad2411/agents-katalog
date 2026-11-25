---
name: whale-flow
description: "Live crypto whale trades and net buy/sell flow across 15 exchanges plus Ethereum, Base and Arbitrum DEXs. Use when the user asks what whales or smart money are doing on a specific named coin: large trades, buy or sell flow, or who is accumulating or dumping BTC, ETH, SOL or any coin. For screening which coins look unusual use whale-radar; for a full why-is-it-moving diagnosis use crypto-market-snapshot. Free, no API key."
license: MIT
compatibility: Requires network access (keyless CoinLobster public API), or the CoinLobster MCP server (https://coinlobster.com/mcp)
metadata:
  author: coinlobster
  version: "1.0"
---

# Whale Flow

Executed whale trades (not wallet transfers): side, size, price, venue, the moment they happen, merged across 15 centralized exchanges and on-chain DEX swaps on Ethereum, Base and Arbitrum.

## Data sources (in order)

1. **CoinLobster MCP connected?** Use its tools, fully qualified: `coinlobster:whale_trades` (recent trades; args: `coin`, `source` cex|dex|all, `min_usd`, `limit`) and `coinlobster:whale_flow` (hourly buy/sell USD buckets; args: `coin`, `hours`). `whale_tape` is a deprecated alias of `whale_trades` kept working for existing callers; prefer `whale_trades`, and fall back to `whale_tape` only if `tools/list` shows just that name.
2. **Named-wallet and DEX lanes (MCP).** `coinlobster:onchain_whales` (args: `chain`, `coin`, `min_usd`, `limit`) returns executed DEX swaps on Ethereum, Base and Arbitrum, each carrying the wallet and the DEX. `coinlobster:hl_whales` (args: `coin`, `limit`) returns Hyperliquid whale fills WITH the wallet address, and `coinlobster:hl_wallet` (args: `address`) opens that account's live book (positions, leverage, net bias). Hyperliquid is the one venue whose public feed names the account on both sides of a fill, so an HL row is followable in a way a CEX row is not. Say which lane a number came from.
3. **No MCP: curl the keyless API** (GET only, JSON):
   ```bash
   curl -s "https://coinlobster.com/api/public/crypto-whales?coin=BTC&limit=50"
   curl -s "https://coinlobster.com/api/public/onchain-whales?chain=ethereum&limit=50"
   curl -s "https://coinlobster.com/api/public/hyperliquid/whales?coin=ETH&limit=50"
   curl -s "https://coinlobster.com/api/public/whale-flow-history?coin=BTC&hours=168"
   ```
   Keyless, the measurement window on the three trade feeds is whatever the returned rows span; compute it from the min/max timestamps and state it. `whale-flow-history` is the REST twin of the `whale_flow` tool: hourly `{ t, buyUsd, sellUsd, netUsd, count, price }` rows, flow on the same grid as the hourly close, 7 days keyless (`maxFreeHours`), 30 (`proHours`) on a coinlobster.com website subscription. An API key does not widen this REST route; on an agent surface the 30-day window is the `whale_flow` MCP tool on a developer plan. `available: false` means no recorded whale hours for that coin yet; `coverage.hoursWithPrice` says how much of the window actually has a price behind it.
4. **Quick read without parsing:** fetch https://coinlobster.com/crypto-whales.md (markdown table of the latest trades).

More endpoints and field meanings: see [references/endpoints.md](references/endpoints.md).

## How to read the feed

- **Whale thresholds scale with liquidity**: $500K+ spot ($1M+ futures) on BTC, $1M+ spot ($2M+ futures) on ETH, $400K+ spot ($800K+ futures) on top majors, $100K+ spot ($200K+ futures) on everything else. A $400K whale trade on a small cap is a bigger event than $2M on BTC. On-chain, swaps are recorded from $100K on Ethereum and $25K on Base and Arbitrum, but the keyless views are floored higher: `/api/public/onchain-whales` and `whale_trades` with `source: dex` show $250K+ only, while the dedicated `onchain_whales` tool serves the full recorded floor.
- **Clusters beat single trades.** Multiple large same-direction trades within minutes suggest coordinated positioning. One trade is one trader's opinion.
- **Counter-trend whales are the strongest tell**: large buys during a selloff mean someone with size is stepping in against the crowd.
- **CEX vs DEX divergence matters**: DEX accumulation without CEX buying often precedes CEX flow; note which lane each trade came from. On MCP, `whale_trades` rows carry a `source` field (cex|dex). Over REST the lane is the endpoint you called: `/crypto-whales` is CEX only, `/onchain-whales` is DEX only.
- **Net flow direction**: sum buy USD vs sell USD over the window (whale_flow does this hourly). Report the split, not just the direction ("62% buys over 4h" beats "whales are buying").
- **Per-trade market conditions**: REST whale-trade rows carry a `marketConditions` object (funding and open interest across venues AT trade time). That is the joined context agents usually need a second provider for: a $4M buy traded while funding sat negative is a different fact than the same buy at extreme positive funding. Quote it when it changes the read.

## Rules

- Data is descriptive history. Report what whales DID, never predict what price will do. No advice.
- Only BTC/USD streams real-time on the free view. Every other coin is 15-min delayed, EXCEPT any trade $1M+, which streams live on any coin. Treat delayed rows as delayed and say so. Keyless DEX rows floor at $250K on `/api/public/onchain-whales` and on the merged `whale_trades` tape; say which view a number came from.
- Always state the window and coin you measured ("last 24h, BTC, CEX+DEX").
- Check the newest row's timestamp against the current time; if the freshest trade is hours old, report the feed as quiet since then rather than presenting stale trades as "right now".
- Few rows is not an error: the free feed floors mean only whale-sized trades stream keyless (BTC/USD from $500K spot, plus every $1M+ trade on any coin live), so 8 rows in 24h means 8 trades that size, not a broken feed. Name the floor when the row count is the story. If every row is one venue, say so.
