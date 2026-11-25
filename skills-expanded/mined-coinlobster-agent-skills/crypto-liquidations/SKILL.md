---
name: crypto-liquidations
description: "Crypto liquidations from two separate worlds: perp liquidations from the centralized futures venues that publish a liquidation feed plus Hyperliquid, with the long vs short breakdown and an hourly series, and DeFi lending liquidations on Aave V3 and Morpho Blue across Ethereum, Arbitrum and Base where both wallets are named. Includes the market-wide view in one call and the Hyperliquid accounts that were closed out. Plus cascade and squeeze context from funding and open interest. Use when the user asks who is getting liquidated, whether longs or shorts are being wiped out, how much got liquidated today, about liquidation cascades, whether a short squeeze setup exists, or who got liquidated on-chain. Free, no API key."
license: MIT
compatibility: Requires network access (keyless CoinLobster MCP at https://coinlobster.com/mcp, callable via any MCP client or plain curl)
metadata:
  author: coinlobster
  version: "1.0"
---

# Crypto Liquidations

Two different events share this word. Keep them apart.

- **Perp liquidation**: a venue force-closes a leveraged position. Side, size, price, venue. From the venues that publish them.
- **DeFi lending liquidation**: a third party repays someone's debt and seizes their collateral on-chain (Aave V3 and Morpho Blue, Ethereum / Arbitrum / Base). Both wallets are named.

**Never add them together.** A combined total is a number with no meaning: one is leverage being flushed on an exchange, the other is collateral changing hands on a lending market. Report whichever the question is about, or both clearly labelled.

## Data sources (in order)

0. **"How much got liquidated?" with no pair named is a MARKET question.** Use `coinlobster:market_liquidations` (no args, keyless) or `GET https://coinlobster.com/api/public/liquidations`. One call covers the whole market instead of one pair: 24h dollars and counts split long vs short, an hourly series so a cascade is locatable, top coins, the biggest single event, and lending liquidations on their own lane. It is not every venue: only some publish a liquidation feed, so the perp totals are a floor. Do NOT assemble a market answer from per-pair calls.
1. **One pair named?** `coinlobster:liquidations` (args: `pair` e.g. BTC/USD, `limit`; keyless on any pair) and `coinlobster:market_snapshot` (args: `pair`; keyless on BTC/USD only, check `available`) for funding + OI context. For the on-chain side use `coinlobster:defi_liquidations` (args: `chain`, `limit`; keyless).
2. **No MCP client:** the hosted MCP answers plain JSON-RPC curl:
   ```bash
   curl -s -X POST https://coinlobster.com/mcp \
     -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
     -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"liquidations","arguments":{"pair":"BTC/USD","limit":50}}}'
   ```
   Swap `name` to `market_snapshot` for funding/OI (keyless that pair-gates to BTC/USD; check `available` in the response, and skip the context layer rather than guess when it is false).
3. **Market-wide over plain REST:**
   ```bash
   curl -s https://coinlobster.com/api/public/liquidations
   ```
   `perp_liquidations` carries `total_usd`, `long_usd`/`short_usd`, `long_count`/`short_count`, `long_share_pct`, `peak_hour`, `hourly[]`, `top_coins[]` and `venues[]`. `named_liquidations[]` lists Hyperliquid accounts that were force-closed, wallet included. `lending_liquidations` is the separate on-chain lane. `stale: true` means the snapshot is behind, so report that rather than the numbers.

4. **On-chain lending liquidations over plain REST:**
   ```bash
   curl -s "https://coinlobster.com/api/public/defi-liquidations?chain=ethereum&limit=50"
   ```
   Returns `count`, `total_usd` and `liquidations[]`, each row carrying `protocol`, `chain`, `symbol`, `amountUsd`, `txHash`, and both `liquidator` and `liquidatee`.

## How to read the DeFi lending side

- **Both wallets are named.** `liquidatee` is the account that got liquidated; `liquidator` is whoever repaid the debt and took the collateral. That pairing is the whole point of the on-chain lane and has no equivalent on a CEX.
- **`amountUsd` is the collateral seized**, not a position size. Do not describe it as leverage being flushed.
- **Coverage is Aave V3 and Morpho Blue on Ethereum, Arbitrum and Base**, above a size floor, and the payload states it in `protocols_covered`. Read that field rather than assuming. Other lending markets exist and are not in this number.
- **Quiet is normal.** Lending liquidations cluster in crashes; a calm week is genuinely a handful of events. An empty window is an answer, not a gap.
- **Never sum with perp liquidations**, and never present a "total liquidations" figure that mixes the two.

## How to read the market-wide view

- **`long_share_pct` is null when the window is empty.** That is deliberate: no liquidations is not "balanced 50/50". If it is null, say nothing was force-closed in the window rather than describing an even split.
- **Dollars and counts often disagree**, and both are true. 90 long events worth $820K against 30 short events worth $180K means longs were hit harder in both, but the reverse pattern (many small liquidations one way, a few huge ones the other) is common and worth stating explicitly.
- **`peak_hour` is where the cascade was.** A 24h total flattens a five-minute flush into a day. Quote the peak hour whenever the total is large.
- **`named_liquidations` is unique to Hyperliquid**, the one venue whose public tape names the wallets on both sides of a fill. Each row is an account that was force-closed and can be looked up.
- **The Hyperliquid share is a sample, not the venue.** It is read from the fills of tracked counterparties, so treat perp totals as a floor and say so when the number carries weight. The payload flags this in `coverage`.
- **`stale: true` means the collector is behind.** Report the staleness. Do not quote the numbers as current.

## How to read it

- **Side semantics**: a long is force-closed by SELLING, so sell-side events are long liquidations (push price down); buy-side events are short liquidations (push up). A one-sided burst amplifies the move that caused it.
- **Counts are not dollars**: `long_liquidations` / `short_liquidations` are event COUNTS. The dollar split is `long_usd` / `short_usd`, and the window total is `total_volume_usd`. Never quote a count as a dollar figure ("$1 of shorts" is the failure this prevents); per-row size lives in `size_quote`.
- **The REST twin names its fields differently.** Those names are the `liquidations` tool's. `GET /api/public/liquidation-history` returns its rows under `history[]`, sized in `quantity_quote`, and carries no `side` string at all: the side is `isBuy`, so `isBuy: false` (a forced SELL) is a long liquidation. Reading `size_quote` or `side` off a REST row silently gets you `undefined`, which is worse than an error because it looks like zero.
- **Always state the window**: `window_minutes` is the period the answer covers, so quote it with any total and with any zero ("no liquidations in the last 340 minutes", not "no liquidations"). `history_included: true` means the recorded series was merged in; `false` means live tape only, so an empty result is not evidence that nothing fired. Say which you had.
- **Cascade check**: many same-side liquidations in a short window + falling open interest = leverage flushing. Cascades exhaust; note whether the pace is accelerating or fading.
- **Squeeze setup (describe, never predict)**: strongly negative average funding (shorts paying) + whale BUYING on the live feed + shorts starting to liquidate is the classic squeeze configuration. Report the three ingredients and their values; stop short of forecasting.
- **Coverage honesty**: only some venues publish liquidation trades, so true totals are higher; say "liquidations we can see" when totals matter.

## Rules

- Descriptive only: report what was liquidated and the current configuration. No predictions, no advice.
- Always name the pair and window measured, and quote sizes in USD from the `*_usd` fields (never from the count fields).
