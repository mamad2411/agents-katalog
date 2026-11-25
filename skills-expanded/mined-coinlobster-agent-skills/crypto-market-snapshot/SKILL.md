---
name: crypto-market-snapshot
description: "Crypto market state and post-move diagnosis, combining price, 24h stats, funding, open interest and liquidations in one call, plus whale flow and news sentiment via companion tools. Use when the user asks the current price or 24h stats of a coin, what is happening in the crypto market right now, why a coin is moving, or for a full autopsy of why a pump or dump happened: whether the move was forced (liquidations) or organic (spot flow), who got wiped and how big vs normal, whether it was leverage-driven or spot-driven, or whether smart money bought the dip. Backward-looking by construction; reports the recorded sequence, never what happens next. Keyless for BTC/USD; other pairs need an active developer plan (from $29/mo) (whale trades and market overview stay keyless for every coin)."
license: MIT
compatibility: Requires network access (keyless CoinLobster public API), or the CoinLobster MCP server (https://coinlobster.com/mcp)
metadata:
  author: coinlobster
  version: "1.0"
---

# Crypto Market Snapshot

The "why is X moving" skill: assemble one coherent picture from price, derivatives, whale flow and news, then answer in that order of evidence.

## Data sources (in order)

1. **MCP connected?** `coinlobster:market_snapshot` (args: `pair`) then `coinlobster:crypto_news` (args: `coin`) for the narrative layer. Keyless, the snapshot serves **BTC/USD only**; other pairs return `{"available": false, "note": ...}`. Always check `available` first. With an active developer plan (from $29/mo), any covered pair works. A CoinLobster Pro website subscription ($9/mo) does not lift this.
2. **No MCP client:** the hosted MCP answers plain JSON-RPC curl:
   ```bash
   curl -s -X POST https://coinlobster.com/mcp \
     -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
     -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"market_snapshot","arguments":{"pair":"BTC/USD"}}}'
   ```
   Market-wide context (totals, regime, BTC, whale net flow):
   ```bash
   curl -s "https://coinlobster.com/api/public/overview?limit=10"
   ```
   Per-coin whale trades: `curl -s "https://coinlobster.com/api/public/crypto-whales?coin=SOL&limit=30"`
3. **Keyless, non-BTC coin:** skip the snapshot (it will answer `available: false`) and build the picture from what IS keyless for every coin: `/api/public/overview` (magnitude, regime, totals), `/api/public/crypto-whales?coin=X` (trades; keyless these are 15-min delayed on every coin except BTC/USD, and except any $1M+ trade, which is always live), the `liquidations` MCP tool, and `crypto_news`. Say which layer came from delayed data.

## The "why is X moving" workflow

Answer from data layers, strongest evidence first:

1. **Magnitude first**: price change vs its 24h range. Keyless, judge magnitude from `chg24hPct` alone; do not estimate a coin's typical daily range from memory. On MCP, `coinlobster:market_overview` with `coin` returns that one symbol's row directly (no paging). Over REST, `/api/public/overview` is volume-sorted with tokenized stocks dominating the top rows, so do not page for one coin: it takes a `q` search param that matches the base symbol or the name, e.g. `?q=SOL`. Rows arrive under `page.rows` with `page.total`; `limit` caps at 200 and pages with `offset`.
2. **Forced flow?** Check liquidations: a cascade explains fast moves better than any narrative. Only some venues publish liquidation trades; when quoting totals say "liquidations we can see".
3. **Whale flow**: were there large trades before or during the move, and which direction? (whale-flow skill / whale_trades). Whales leading the move and whales chasing it are different stories.
4. **Positioning**: funding rate and open interest. Rising OI + rising price = new longs; falling OI = closing, not conviction.
5. **Narrative last**: `crypto_news` sentiment and headlines. Only cite news when the timing actually matches the move. Quote sentiment as attributed history and strip forecast wording ("expected", "likely") from summaries; never carry it in your own voice.

Compose the answer as: what happened (numbers), what the flow shows (whales/liqs/OI), what the narrative says, clearly labeled as history.

## Forced or organic (the move autopsy)

When the question is specifically *why a pump or dump happened* (who got wiped, was it leverage-driven or spot-driven, did smart money buy the dip), run this decomposition instead of stopping at the 5 layers above. It sequences the three recorded series that only exist together here: real liquidation events, executed whale trades, and open interest, against price.

Tools: `coinlobster:liquidations` (side/size/venue), `coinlobster:whale_trades` (executed trades during the move), `coinlobster:market_snapshot` (OI + funding now), and `coinlobster:market_history` (daily OI/funding/liq series for percentile framing). If `market_history` returns no rows for the pair, run the autopsy on raw totals without percentile framing rather than reporting a failure. Keyless REST fallback:

```bash
curl -s "https://coinlobster.com/api/public/liquidation-history?pair=BTC/USD&limit=200"   # BTC/USD only keyless; other pairs 403. Rows under history[]: size is quantity_quote, side is isBuy (false = a long was force-sold)
curl -s "https://coinlobster.com/api/public/crypto-whales?coin=BTC&limit=50"
```

1. **Size the move first.** How big, over how long. A move inside the coin's normal daily range needs no autopsy; say so and stop.
2. **Liquidation timeline vs price.** CRITICAL sequencing: did liquidations cluster at the START of the move (forced flow drove it) or after it was underway (the move caused them)? Timestamps vs the price path answer this factually, never narrative.
3. **Scale the wipeout.** Day's liquidation total vs the pair's own recorded days when the baseline layer is up ("3rd largest long-liquidation day of its 127 recorded"); otherwise raw totals, naming the venues seen and this frame: "events from N venues that publish them; market-wide totals run far higher, so use this as a timing and sequencing series, not a size series". Drop rows with zero quantity from totals.
4. **OI: purge or build?** Falling OI during the move = positions closing (flush); rising OI = new positioning (conviction or fresh leverage).
5. **Funding flip.** Did the crowded side flip or reset? Funding before vs after, as percentiles when available.
6. **Executed whale trades during the move.** Did size sell INTO the drop (distribution), or buy the low (the counter-trend read)? Each row carries side, venue, timestamp and, on MCP `whale_trades` rows, per-trade `marketConditions` (funding/OI across venues at trade time).
7. **Compose the verdict as a factual decomposition**, e.g.: "$X of longs force-sold across 4 venues starting 14:02 UTC, liquidations led the price low by ~40s, OI purged $Y (to its 8th percentile of 127 recorded days), funding flipped negative, and whales spot-bought $Z in the hour after the low." Forced, organic, or mixed follows from the numbers; state which pattern the numbers show and stop there.

**Autopsy rules:** backward-looking only. It explains what the recorded data shows happened, never what happens next; "exhausted" / "bottomed" style conclusions are forecasts in disguise, do not use them. Sequencing claims come from timestamps you actually have. Wipeout totals always carry the "liquidations we can see" coverage note. Percentile claims always carry their recorded-days count. "Smart money" stays mechanically defined: the size-tier floors on the live feed ($500K+ spot / $1M+ futures on BTC, $1M+ / $2M+ on ETH, $400K+ on top majors, $100K+ elsewhere, $250K+ DEX swaps), nothing else.

## Positioning vs its own recorded history

Is today's funding / open interest actually unusual for THIS pair? Judge it against the pair's own recorded archive (daily percentile ladders, computed from data recorded live since 2026-03-18), not against a gut feel.

```bash
curl -s "https://coinlobster.com/api/public/baseline?pair=BTC/USD"
```

Response (`available: false`, an auth error, or any non-200 all mean the same thing keyless: say the layer is unavailable and skip it; `available: false` on a live deploy means under 30 recorded days for that pair):

- `.headline` (string|null): the single tightest line, e.g. "funding in its top 5% of 127 recorded days". Null means nothing is at an extreme. **Null is an answer**: report "positioning typical vs its own record", do not pad.
- `.funding.phrase`, `.funding.band` (record high | record low | top 5% | top 25% | typical | bottom 25% | bottom 5%), `.funding.asOf`, `.funding.days`, `.funding.outcome`
- `.oi.phrase`, `.oi.band`, `.oi.asOf`, `.oi.days`, `.oi.highDays`, `.oi.outcome` (`highDays` = N-day-high streak from the recorded series)

Useful one-liner: `jq -r '.headline, .funding.outcome, .oi.outcome'`

Market-wide sweep (which pairs sit at records or their own top/bottom 5% today, for funding, open interest or liquidations):

```bash
curl -s "https://coinlobster.com/api/public/extremes" | jq -r '.records[].phrase, .top5[].phrase'
```

Each entry in `.records[]` / `.top5[]`: `pair`, `metric` (funding | open_interest | liquidations), `band`, `day`, `days`, `phrase`, `outcome`. Quick read without parsing: fetch https://coinlobster.com/extremes.md (plain markdown, same scan).

### How to use it in the answer

1. Pull `/baseline` for the pair after the positioning step. If `.headline` is non-null, it upgrades your positioning read from "funding is 0.02%" to "funding in its top 5% of 127 recorded days".
2. State the baseline depth once per answer ("vs its 127 recorded days"); "top 5%" of 30 days and of 300 days are different claims, but one citation covers the answer.
3. Check `asOf` and treat it as load-bearing: "now" is a live venue-complete value; "recorded 2026-07-18" means you are ranking a day that is about a WEEK OLD (the archive settles behind live). Lead with the date in that case; a week-old percentile presented as current is the one mistake this layer must never make.
4. If `.outcome` exists, quote it in its own shape: "on the N recorded days funding was in its top 5%: price next day up X of N, median +Y%" (or "down or flat X of N"). That sentence is the recorded history of past occurrences. It is not a forecast; never reword it into one.

### Rules for this layer

- The judgment only speaks at extremes (records, top/bottom 5%, or a confirmed multi-day OI high). "Typical" produces silence, not a headline; do not manufacture significance from a null.
- Days evidence is always attached in the source phrases. Keep it attached in yours.
- Outcome sentences state what price did next on past recorded days, with n always shown. History, never a forecast, no advice.

## Rules

- Never lead with news; flow data usually explains more than headlines.
- State the pair, the window, and quote real numbers. Suppress any layer whose data came back empty rather than guessing.
- Descriptive only. No forecasts, no advice.
