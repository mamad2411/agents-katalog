---
name: crypto-trade-context
description: "The data picture around a crypto position. Use when the user is about to enter or exit, is holding a position and wants what to watch, asks if their side is crowded, what holding costs, whether whales are on their side, or wants their own signal cross-checked against smart-money flow. Reports state and recorded history with sample sizes; never advice, never a forecast. Keyless on every streamed pair: trade_context, whale_context and funding_matrix on MCP, or /api/public/baseline, /api/public/whale-context, whale trades and liquidation history over plain curl. Percentile judgment vs a pair's own recorded days is keyless too, and so are whale USD magnitudes over /api/public/whale-context. Depth (whale USD on the MCP tools, crowding, full 24h stats) needs an active developer plan (from $29/mo), and so does squeeze_score outright; liq_zones is keyless on the free pair only."
license: MIT
compatibility: Requires network access (keyless CoinLobster public API), or the CoinLobster MCP server (https://coinlobster.com/mcp)
metadata:
  author: coinlobster
  version: "1.0"
---

# Crypto Trade Context

The user is making or holding a trade. Your job is the data picture, stated so they can decide: crowding as a percentile of the coin's own recorded days, carry cost in dollars, whale direction vs their side, where forced selling actually fired, and what to watch while holding. The decision is theirs; you never make it.

## Data sources (in order)

1. **MCP connected?** `coinlobster:trade_context` (args: `pair`, optional `position_usd`, optional `compact`) is the one-call blob: price, 24h stats, funding + OI with percentile judgment vs the pair's own recorded days, whale flow vs the coin's own baseline, visible liquidations, carry arithmetic, crowding (keyed). Keyless it answers on EVERY streamed pair; `depth` reports which shape you got (`lite` off the free pair, `free-pair`, or `keyed`) and `locked_layers` names exactly what a developer plan key (from $29/mo) adds: `stats_24h`, `whale_flow USD magnitudes` and `crowding`. **`vs_own_history` is never locked**: the percentile judgment is keyless on every pair, here and on `/api/public/baseline` and `market_screener`.
2. **No MCP:** assemble the same picture keyless:
   ```bash
   curl -s "https://coinlobster.com/api/public/baseline?pair=BTC/USD"        # percentile judgment + outcome history
   curl -s "https://coinlobster.com/api/public/whale-context?coin=BTC"       # whale flow vs own baseline (coin param required)
   curl -s "https://coinlobster.com/api/public/liquidation-history?pair=BTC/USD&limit=100"  # history[]: quantity_quote, isBuy (false = a long was force-sold)
   ```
   Companion MCP tools when present: `funding_matrix` (per-venue rates, keyless on any streamed pair), `squeeze_score` (developer plan only: keyless it answers `available: false`), `liq_zones` (projected levels, labeled as a projection; keyless it covers the free pair only and drops the cascade chains).

> On ANY non-200 (401/400/404 alike), fall back and keep a vs-own-history layer in the answer: `/api/public/whale-context?coin=X` carries the whale multiple, the buy-share baselines AND the USD behind them keyless (`ctx.usd24`, `ctx.net24`, `ctx.avgDayUsd`), which the `whale_context` MCP tool withholds without a key. When the tool locks magnitudes, this endpoint is where you get them. The last 24h of `/api/public/crypto-whales` rows embed per-trade funding/OI (`marketConditions`) for a crude funding-range check. Without an MCP client, every tool answers a raw POST:
> ```bash
> curl -s -X POST https://coinlobster.com/mcp -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"market_snapshot","arguments":{"pair":"BTC/USD"}}}'
> ```

## Workflow: pre-entry check

The user says which coin and (maybe) which side. Never ask them to reveal more than they offer; the picture is the same either way.

1. **Crowding**: funding and OI as percentiles of the pair's OWN recorded days (`vs_own_history` / `/baseline`). "Funding in its top 5% of 127 recorded days" is a crowding fact; "funding is 0.02%" is not. If the judgment layer says typical, say typical.
2. **Carry**: what holding costs at the current rate. `carry_cost.per_day_pct_at_current_rate` and `apr_pct_at_current_rate` (plus `per_day_usd_at_current_rate` when they gave a size; every key carries that suffix, so a bare `per_day_usd` reads back null). State who pays: positive funding means longs pay and a short collects (carry_cost.paid_by names the paying side); a side-blind cost line tells a short-seller the wrong sign. Fallback arithmetic when the tool is absent: `funding.average_rate` is an unweighted average across the venues streaming that pair, annualized AS IF every venue paid on an 8h clock (`funding.interval_h`), so per-day = rate x 3, APR = per-day x 365. They do not all pay on the same clock (Kraken Futures settles hourly where most venues settle every 8h), so `funding_matrix` returns the real `interval_h` per venue. Say "at an 8h interval" once, and read `funding_matrix` before comparing one venue's rate against another's.
3. **Whale direction vs their side**: `whale_flow.mult_vs_avg_24h` + `buy_share_24h` vs `buy_share_7d`. Report agreement or disagreement as fact: "whale volume 2.1x its 20-day average, 64% buys (7d average 51%); your short is against that flow."
4. **Forced-flow map**: recent liquidations by side and, when available, `liq_zones` projected levels. Projections are ALWAYS labeled as a model; recorded trades (`liquidation-history`) are what actually fired.
5. **The record**: if funding/OI sit at an extreme, quote the outcome sentence verbatim shape: "on the 14 recorded days funding was in its top 5%: price next day down or flat 9 of 14, median -0.8%". History with n shown, never reworded into a prediction.
6. **Compose**: one tight paragraph in the autopsy register (dense, numbers first), the baseline depth cited once, ending with the facts, not a verdict.

## Workflow: in-position monitoring

They hold a position and want to know what to watch.

1. Establish "since entry" when they say when they entered (no entry time given = skip since-entry framing, just report now): funding percentile then vs now, OI change, whale net direction since, liquidations near their range.
2. Build the watch-set from measurable conditions, each tied to data they can re-check: funding band change (top 5% entering/exiting), OI purge or build, whale flow flipping direction vs its baseline, liquidation bursts on their side. Where recorded history exists for a condition (outcome sentences, flag records), attach it with n.
3. Never say "exit if X". Say "these are the measurable conditions and their recorded history; here is how to re-check each one" (the exact curls).

## Workflow: percentile alert recipes (polling)

Standing watches defined against the coin's own history, not static thresholds:

- Whale flow unusual: poll `/api/public/whale-radar?window=1h` for the coin flagged `unusual: true` (that flag IS the vs-own-baseline trigger).
- Funding entering its own extreme: poll `/api/public/baseline?pair=X` until `.funding.band` is `top 5%`/`record high` (or bottom side).
- Flag fired on the coin: poll `flag_outcomes` with `coin` and a short `hours` window.

Poll at 60s+ intervals keyless (REST `/api/public/*` is 60 req/min per IP; the MCP has its own layered budget, so back off on `Retry-After` rather than assuming a rate). The free key is a one-off 1,000 credits (about 20 to 100 REST calls in total), so it will not carry a loop; sustained polling needs a developer plan (Builder = 300 req/min).

## Rules

- **No advice, ever.** No "should", no "looks good", no entry/exit calls, no position sizing. Descriptive adjectives backed by numbers are fine ("long side crowded: funding top 5% of 127d"); verdicts about what to DO are not.
- State the window and the baseline depth ONCE per answer ("baselines: 127 recorded days"), then let the numbers be numbers. One coverage note per answer, not per figure.
- Typical is an answer: "funding typical vs its 127 recorded days" ends the crowding layer; do not pad.
- Projections (liq_zones) are modeled levels; recorded liquidations are recorded events. Never blur them.
- Degraded layers are named and skipped, never guessed.
