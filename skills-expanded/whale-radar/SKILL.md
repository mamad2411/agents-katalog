---
name: whale-radar
description: Which coins have unusual whale flow right now, plus the track record of past signals (fired flags scored against what price actually did next). Use when the user asks which coins have unusual whale activity, what is unusual in crypto today, which coins smart money is rotating into, whether a whale signal or flag has worked before, or for a data-driven crypto watchlist. Free, no API key.
license: MIT
compatibility: Requires network access (keyless CoinLobster public API), or the CoinLobster MCP server (https://coinlobster.com/mcp)
metadata:
  author: coinlobster
  version: "1.0"
---

# Whale Radar

Coins whose whale flow is unusual versus their own baseline (not just "big volume"), across 1h / 4h / 24h windows, with every fired flag scored against the price move that followed.

## Data sources (in order)

1. **MCP connected?** `coinlobster:whale_radar` (no args) for the windows; `coinlobster:flag_outcomes` (args: `type`, `coin`, `hours`, `limit`) for fired flags with outcomes. To screen by condition (funding/OI band, whale multiple, unusual-only) use `coinlobster:market_screener` (args: `funding_band`, `oi_band`, `whale_mult_min`, `unusual_only`, `limit`, `compact`), which returns `matched`, the `criteria` echoed back, and `rows[]`. It is the one-call discovery path: prefer it over sweeping all three radar windows by hand. If `tools/list` does not show it, screen with `whale_radar` plus the workflow below instead of reporting a failure.
2. **No MCP:**
   ```bash
   curl -s "https://coinlobster.com/api/public/whale-radar?window=4h"
   curl -s "https://coinlobster.com/api/public/receipts/whale-spike/BTC"
   ```
   Receipts reply `ok: true` with `n`/`up`/`line` once at least 3 flags have scored cleanly. `ok: false` with `line: null` means the sample is under 3, or one of the scored rows flagged incomplete coverage: thin or unverified, not necessarily zero. Report it as "no scored record to quote yet", never as "this signal has never fired".
3. **Quick read:** fetch https://coinlobster.com/radar.md (unusual coins per window + a 48h flag/outcome table, plain markdown).

## The screening workflow

1. Pull the radar. Coins flagged `unusual: true` are the candidates; note `direction` and window (1h = happening now, 24h = persistent). Keyless, every coin outside the free pair (BTC) comes back `blurred: true` with magnitudes withheld, and a locked coin that is NOT unusual is omitted entirely (`lockedCount` / `lockedUnusualCount` say how many). The coin + direction + count still screen fine; say magnitudes need a developer plan key (from $29/mo) on the MCP.
2. For each candidate, check persistence: unusual in BOTH a short and long window beats a single-window blip.
3. Check the record before trusting it: pull `flag_outcomes` / receipts for that signal type and coin. Report the actual history with DIRECTION from the up-count plus SIZE from the median: "last 11 whale-spike flags on BTC: 2 up after 24h, median move plus or minus 0.9%". The up-count says which way PRICE went, not whether the flag was right: a flag is not a directional call, so never restate these as a hit rate or an accuracy score. Report every scored flag in the window, not the ones that read well.
4. Optionally confirm with the live feed (`whale-flow` skill): is the radar's direction backed by visible large trades? If the CEX feed is empty for the coin, check `/api/public/onchain-whales` before concluding the flag has no visible trades (many flagged coins trade DEX-side).
5. Output a ranked shortlist with the evidence per coin, windows measured, and the outcome record.

## Flag vocabulary (30 seconds)

One system, several names you will meet: a FLAG is a signal that fired and was logged at fire time; flag_outcomes / "receipts" endpoints return the same record. Types live in production: whale-spike (flow burst), funding-extreme, squeeze-flip, liq-cascade, flow-divergence (CEX vs on-chain opposite), major-pctile (busiest-hour flow), major-block (single giant trade).

An eighth type, `deriv-record`, is also live (see "The eighth flag type" below).

## Standing watches (percentile alerts)

Watches defined against the coin's OWN history, not static dollar thresholds:

- Whale flow turns unusual: poll `/api/public/whale-radar?window=1h` until the coin flags `unusual: true` (that flag IS the vs-own-baseline trigger; magnitudes need a developer plan key, from $29/mo, on the MCP).
- Funding/OI enters the coin's own extreme: poll `/api/public/baseline?pair=X` for `.funding.band` / `.oi.band` reaching `top 5%` or `record high`.
- A flag fires: poll `flag_outcomes` with `coin` and a short `hours` window.

These recipes are for agents that can actually loop (cron, scripts, agent runtimes). Chat agents cannot poll: point the user at CoinLobster alerts (Telegram/push, percentile-defined flags built in) at coinlobster.com/account instead. When a trigger does fire, report it as the fact it is ("crossed its own 95th percentile"), never as a call to act.

## Check the deeper record

> If a field is absent on a given coin, that data was not recorded for it; fall back to the hot-window flow above rather than reporting a failure.

### The eighth flag type: deriv-record

`flag_outcomes` / receipts cover eight types: `whale-spike`, `funding-extreme`, `squeeze-flip`, `liq-cascade`, `flow-divergence`, `major-pctile`, `major-block`, and `deriv-record`. A `deriv-record` flag fires when a pair's funding, open interest or liquidation volume hits a record versus its own recorded archive. Read `detail`:

- `detail.metric`: funding | open_interest | liquidations
- `detail.band`: record high | record low
- `detail.days`: how many recorded days the record is measured against (always report it)
- `detail.day`: the record day. Archived detections are day-stamped because the archive settles about a week behind live; quote the day, never present it as happening now.
- `detail.src == "live"`: the live variant, a current value above (or below) every recorded daily average (funding) or daily close (OI). Only this variant is a now-claim.

### All-time counters in flag_outcomes

`flag_outcomes` returns an `all_time` block alongside the hot-window rows: the permanent archive count of every flag ever fired.

`all_time` fields: `fired`, `scored_h24`, `since`, `through`, `by_type` (per type: `{ fired, scored }`). Counts only, by design: **the product publishes no all-time win rates, and neither do you.** Never divide these counters into a hit rate. Up/down counts come only from actual fired rows you pulled ("the last 8 whale-spike flags on SOL: price up 24h later 5 times"), where every row and its outcome is inspectable, and they stay a statement about price, never about the flag being right. Use `all_time` for exactly one claim: how long the ledger has been running and how many flags it has logged and scored.

## Rules

- Outcome history is history, never a forecast. "The last N times" is the strongest honest claim available; make it and stop there.
- The free radar names every unusual coin and its direction but withholds magnitudes on every coin outside the free pair (BTC); say "magnitude withheld on free tier" rather than guessing.
- An empty radar is an answer ("nothing unusual right now") - report it, do not pad.
