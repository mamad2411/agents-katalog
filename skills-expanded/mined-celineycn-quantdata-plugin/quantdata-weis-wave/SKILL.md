---
name: quantdata-weis-wave
description: Reads Weis Wave volume-price structure for a symbol from the Quant Data Weis Wave API — current wave direction and volume, recent completed waves, and detected events (climax-into-buying, no-supply, no-demand, sign-of-thrust) each carrying its pre-registered measured win rate. Use when the user asks about volume behaviour, effort versus result, Wyckoff or Weis wave analysis, whether a pullback is happening on light volume, whether a move has volume behind it, or wants volume confirmation of a price move.
---

# Quant Data — Weis Wave

An HTTP API that rebuilds the **Weis Wave** view of a market — price grouped into waves, each
wave carrying its cumulative volume — and reports which of five classical volume-price events
have fired, with the win rate each one actually measured over 16 years of data.

Base URL: `https://api.quantdata.uk`

## Authentication

Send the header `X-API-Key`. Keys start with `qd_`.

Read the key from the environment variable **`QUANTDATA_API_KEY`**. Never write a key into
this file, into generated code, into a commit, or into a message back to the user.

```bash
export QUANTDATA_API_KEY="qd_..."
```

If the variable is unset, one anonymous first-look response may still succeed per source per
UTC day. It is complete, and its legacy-named `free_tier` object has
`access_kind: "anonymous"`, `calls_remaining_today`, `resets_at`, and the next action.

For continued evaluation, ask the user which email address should receive a free key, then
`POST https://api.quantdata.uk/v1/access/free-key` with JSON:

```json
{"email":"you@example.com","marketing_opt_in":false,"source":"agent"}
```

An MCP-connected agent can call `quantdata_request_free_api_key` instead. No login, password,
card or GUI is required. The raw `qd_` key is delivered only to the inbox and never returned in
the REST or MCP result. Never invent an email address.

`marketing_opt_in` defaults to `false` and is separate from key delivery. Set it to `true` only
when the email owner explicitly asks for occasional product updates. A `true` request is only
pending. It is confirmed only if the recipient replies `SUBSCRIBE` to the key-delivery email;
no marketing updates are sent before confirmation. Do not report the request as a completed
subscription. A free key covers all four Quant Data endpoints, sharing **10 successful calls
per UTC day**.

When a free key reaches that allowance, relay `message_for_your_human`, pass its checkout URL
to the person, and stop. Paid access is $149/month for every endpoint, first 3 days free. An agent
cannot complete card authentication. Checkout with the same email upgrades the existing free
key in place.

While the person decides, the Max Pain pages at `https://quantdata.uk/max-pain/{ticker}`, the
GEX pages at `https://quantdata.uk/gex/{ticker}`, and
`https://quantdata.uk/methodology` remain free.

## The concept, in case you need to explain it

Weis Wave comes from the Wyckoff tradition. Instead of showing volume bar by bar, you group
price into **waves** — a run in one direction that continues until price reverses by more than
a threshold — and total the volume across each wave. Then you compare **effort** (volume) with
**result** (how far price moved).

A big rally on heavy volume that only travels a little is effort without result. A quiet
pullback that gives back almost nothing is a lack of selling rather than an absence of buying.
That comparison is the entire method.

Quant Data's wave construction uses a close-price zigzag with the reversal threshold set to
`0.3937 × ATR(60)`, a scale-free coefficient calibrated on S&P 500 E-mini futures. The same
threshold therefore behaves consistently across instruments of very different price levels.

## Endpoint

### `GET /v1/weis/{symbol}`

```bash
curl -s -H "X-API-Key: $QUANTDATA_API_KEY" \
  https://api.quantdata.uk/v1/weis/ES=F
```

Optional `session` query parameter:

- `rth` (default) cuts waves on the US regular session. It is operationally useful, but it is
  not a like-for-like window for the published reference win rates, which were measured on the
  full bar stream.
- `full` uses the whole bar stream, including pre- and post-market. Use it when directly
  comparing returned events with the published reference win rates. It requires genuine
  extended-hours volume; if the active source supplies mostly zero-volume extended bars, the
  API returns `422 NO_EXTENDED_VOLUME`. Obey `retryable`: retry once only when it is `true`,
  otherwise use `rth` or a symbol/source with real extended-hours volume.
- `asia` is experimental and accepted only for 24-hour instruments (`=F` and `=X`). Weis still
  requires real volume, so spot FX normally returns its no-volume result.

```json
{
  "waves_total": 214,
  "current_wave": {
    "dir": "up",
    "bars": 7,
    "move": 12.25,
    "volume": 48210.0,
    "vol_vs_median20": 0.41
  },
  "recent_waves": [
    {"dir": "down", "move": -18.5, "bars": 11, "volume": 141900.0,
     "end_time": "2026-07-24 11:35:00-04:00"},
    {"dir": "up", "move": 22.0, "bars": 9, "volume": 96400.0,
     "end_time": "2026-07-24 12:20:00-04:00"}
  ],
  "events": [
    {"type": "no_supply_long", "dir": "long",
     "time": "2026-07-24 13:05:00-04:00", "price": 6412.25,
     "reference": {"es_win": 0.514, "es_n": 23077, "es_p": "3e-5",
                   "verdict": "CONFIRMED(ES)",
                   "warning": "reverses on BTC (48.3%) — do not carry across assets"}}
  ],
  "disclaimer": "Wave/event analytics derived from Weis Wave methodology..."
}
```

Field notes:

- `current_wave` is the **unfinished** wave in progress. `dir` is `up`, `down` or `forming`.
  `vol_vs_median20` compares its volume so far against the median of the last 20 completed
  waves — below about 0.4 is quiet, above about 2 is heavy. It is the single most useful
  number in the response.
- `recent_waves` holds the last 8 completed waves, oldest first. Read `move` against `volume`
  to see effort versus result yourself.
- `events` holds up to the 10 most recent detections. Each carries a `reference` block with
  the measured statistics for that event type — **quote those, not folklore**.
- `session_window` says which window was used. Always relay `note_window` when present: under
  `rth` it warns that the returned events and full-stream reference rates are not like-for-like;
  under `full` it confirms that the windows match. Relay `note_session` for the experimental
  Asian window as well.
- `note` appears when the history window held too few waves for event detection (it needs at
  least 46). When you see it, say the event list is empty because of insufficient history,
  not because the market is quiet.
- `error` appears instead of the analysis when the window has fewer than 120 bars, or when the
  data source returned no volume at all. Weis analysis is impossible without volume — report
  that plainly rather than guessing.

## Resolving what the user said into a symbol

Same rules as the rest of Quant Data. **Resolve an instrument name to a ticker before
calling.**

| User says | Send |
|---|---|
| a US stock or ETF | the ticker — `SPY`, `QQQ`, `NVDA` |
| a Hong Kong stock | digits + `.HK` — Meituan = `3690.HK` |
| a China A-share | the 6-digit code — Kweichow Moutai = `600519` |
| a futures contract | `ES=F`, `NQ=F`, `GC=F`, `CL=F`, `YM=F` |
| Bitcoin / Ethereum | `BTC-USD` / `ETH-USD` |
| a currency pair | **not spot FX** — use the CME future: `6E=F` (EUR), `6B=F` (GBP), `6J=F` (JPY), `6A=F` (AUD) |
| "the S&P", SPX, US500 | `SPY` or `ES=F` |
| "the Nasdaq", NAS100 | `QQQ` or `NQ=F` |
| **gold**, XAU, spot gold | `GC=F` (COMEX futures) or `GLD` (ETF). `XAUUSD` answers with the `XAUT-USD` token reading plus a note (see below). |
| **tokenised gold**, XAUT, Tether Gold | `XAUT-USD` — a different instrument from spot gold (see below) |
| oil, WTI, crude | `CL=F` or `USO` |

**`GOLD` is a US-listed equity (Gold.com, Inc.) — not the metal.** Never pass a plain English
instrument name as a ticker.

One extra caution specific to this product: **volume quality decides whether the answer means
anything.** Consolidated tape volume for a liquid ETF or a futures contract is trustworthy.
Single-exchange volume for a thin name is not. If the instrument barely trades, say the wave
volumes are unreliable.

Spot gold itself is no longer covered; a request for `XAUUSD` answers with the `XAUT-USD`
token reading plus a note saying so. `GC=F` carries real exchange volume and is the gold
instrument to use on this endpoint.

**`XAUT-USD` is not a spot-gold substitute.** It reads the Tether Gold token's order book on
a crypto exchange. The token is redeemable for allocated LBMA gold, but it has consistently
traded at a discount to spot, the size of that discount moves over time, and it keeps trading
on weekends when the gold market is closed. Send it only when the user asked for tokenised
gold, or relay what the API itself returned for a spot-gold request (it self-reports the
swap in a `symbol_note`). Responses for it carry an `instrument_note` stating all of this
and noting that the pre-registered ES win rates do not transfer to it; relay that note
verbatim, and never present its readings as spot-gold readings.

## The five events, and the honest scoreboard

Pre-registered tests on S&P 500 E-mini futures, 5-minute bars, 2010–2026, with symmetric
±3×ATR barriers and a Bonferroni correction. Baseline — the win rate of any wave flip at all —
is **49.3%**.

| Event | What the tradition says it means | Measured (ES) | n | Verdict |
|---|---|---|---|---|
| `cib_long` | heavy up-wave, then a light pullback → buyers defended | **51.8%** (p=1.6e-5) | 13,867 | **CONFIRMED** — matches the claim |
| `no_supply_long` | down-wave volume dries up without breaking the prior low → sellers exhausted | **51.4%** (p=3e-5) | 23,077 | **CONFIRMED** — matches the claim |
| `no_demand_short` | weak up-wave on light volume → rally has no buyers, bearish | **45.6%** | 22,262 | **REVERSED** — the bullish read is right, 54.4% |
| `sot_short` | shortening of the thrust: each push travels less → trend exhausting, bearish | **47.6%** | 9,427 | **REVERSED** — fading it does not work |
| `cib_short` | mirror of `cib_long` on the downside | **48.6%** | 12,642 | below baseline — bearish reads fail systematically |

**Read that table before you interpret any event.** Two of the five confirm the tradition. Two
measured the opposite of what the tradition teaches. On S&P 500 futures, every bearish
volume-price read tested below 50% — in a market with long-run upward drift, "the rally looks
weak" is not a reason to be short. That asymmetry is the strongest single finding here, and it
is the opposite of what the textbooks say.

So when a `no_demand_short` or `sot_short` fires, do **not** report it as bearish. Report that
the event fired, that the tradition reads it as bearish, and that on 22,262 measured instances
it resolved bearishly only 45.6% of the time.

## Day-type gating — the strongest result

A Weis event on its own is a weak trigger. In the research, the same event **filtered by the
day-type context** from the day-type model was measurably stronger:

| Asset | `cib_long` under TrendUp | Comparison | Gap |
|---|---|---|---|
| ES (trained asset) | **56.5%** | 50.8% in the opposite context | +5.6pt, p=0.002 |
| NQ (zero-shot) | **56.1%** | 45.3% under TrendDown | +10.8pt, p=2e-6 |
| QQQ (zero-shot) | **54.3%** | 44.3% under TrendDown | +10.0pt, p=7e-5 |

The comparison column is the same event measured in the **opposite day-type context** — it is
not an ungated baseline. Ungated, `cib_long` measured 51.8% on ES; the gate moves the same
event both ways from there.

Zero-shot means the day-type model had never seen NQ or QQQ during training. The gate is the
most durable component of the whole system. Adding a third filtering layer on top made results
*worse* — it only shrank the sample.

**Where the day-type read lives now.** It is the `day_type` block of the
`GET /v1/brooks/{symbol}` response (see the `quantdata-daily-bias` skill), alongside the
rolling price-action events — and only in the US day session, because a day type is a property
of a session that has an open and a close. In the gap and Asian windows the block returns
`available: false` with its reason.

So the context can be read live again in the day session. Report it as two descriptions side
by side — the day-type distribution with its 37% majority-class baseline, and the Weis event
with its measured rate and `n`. The gating numbers above are a **research** result measured
under the study's own protocol, published on `https://quantdata.uk/methodology`; they are not
the measured rate of anything a live pair of readings produces, so do not attach 56.5% or
56.1% to a live combination, and do not turn any pairing into a trigger, an entry or a
recommendation.

## Where this fails — say so out loud

- **Gold, Bitcoin and Ethereum share an anti-signature.** The edge does not transfer. Eight
  pre-registered tests on BTC returned **0 confirmations**, and `no_supply_long` came back
  significantly *reversed* (48.3%). On GC and ETH, the same reversal. Outside index-type
  assets, the measured rate for a quiet pullback runs the other way.
- **Bearish events fail on index products** — see the scoreboard above.
- The Asian-session version of the day-type gate was pre-registered and came back **NO_GO**.
- 121,000+ Bulkowski-style chart-pattern detections produced an outcome AUC of 0.54, barely
  above coin-flip. Classical pattern shapes are not carrying the signal here; conditioned
  volume events gated by day type are.

If a user asks for a Weis read on BTC, ETH or gold, **give it and immediately say the measured
edge is absent or reversed on that asset class**. The wave structure is still descriptive and
still worth looking at; the win rates simply do not apply.

## Worked example

```python
import os, json, urllib.request

def qd(path):
    key = os.environ["QUANTDATA_API_KEY"]          # never hard-code
    req = urllib.request.Request(
        f"https://api.quantdata.uk{path}", headers={"X-API-Key": key})
    return json.load(urllib.request.urlopen(req, timeout=25))

w = qd("/v1/weis/QQQ")
if "error" in w:
    raise SystemExit(w["error"])

cur = w["current_wave"]
print(f"current wave: {cur['dir']}, {cur['bars']} bars, "
      f"move {cur['move']}, volume {cur['vol_vs_median20']}x the 20-wave median")

for ev in w["events"]:
    ref = ev.get("reference", {})
    print(f"{ev['time']}  {ev['type']}  measured {ref.get('es_win')} on n={ref.get('es_n')}")
```

The day-type read the gating study used is the `day_type` block of
`GET /v1/brooks/{symbol}`, and it is present in the US day session only. A second call there
gives you the day-type distribution to report next to the wave read — as two descriptions,
never as a combined signal, and never carrying the study's win rates onto the live pair.

## How to present the result to a human

- **Lead with effort versus result**, not with the event name. "The last down-wave gave back
  18 points on 141k contracts; the wave in progress has recovered 12 points on 48k — about 0.4
  of the recent median" is a sentence a beginner can use. "no_supply_long fired" is jargon.
- **Quote the measured number next to every event**, from the `reference` block. Say `n` too.
  A 51.4% win rate on 23,077 samples is a very different claim from 51.4% on 40.
- **Relay `note_window`.** The published reference rates used the full bar stream. An `rth`
  response is still descriptive, but its events are not a like-for-like sample for those rates;
  use `session=full` for that comparison when real extended-hours volume is available.
- **State the baseline: 49.3%.** A 51.8% win rate is +2.5 points over the baseline. That is a
  small, real edge, and describing it as anything more is a misrepresentation.
- **Never call these tradeable on their own.** The gross expectation is roughly the same size
  as transaction costs. The honest role is a confirmation layer or a weighting factor on a
  decision the user already has a reason to make. David Weis himself framed the method as
  interpretive rather than mechanical.
- **When a bearish event fires, report the reversal.** This is the single most valuable thing
  the product knows, and it is the thing an agent parroting the textbook would get wrong.

## Firm rules

- **Never present output as a buy or sell recommendation.** No entries, stops or targets. An
  event firing is a description of volume behaviour that already happened.
- **Never give personalized investment advice.** If asked "should I buy", explain what the
  wave structure describes and decline the recommendation.
- **Always carry the disclaimer** from the `disclaimer` field. Educational analytics, not
  investment advice; trading involves risk of loss.
- **Never claim precision the numbers do not have.** 51.8% is 51.8%. Do not call it strong,
  reliable, or high-probability, and do not compound several weak numbers into a confident
  narrative.
- **Never carry ES statistics onto another asset silently.** Every `es_win` is
  S&P-500-futures-specific. Naming the asset the statistic came from is mandatory.
- **Do not invent statistics.** If it is not in the `reference` block or in this file, you do
  not have it.
- Quant Data is independent research, not affiliated with or endorsed by David Weis, the
  Wyckoff tradition's estates, or any exchange or broker.

## Errors

Every API error body is `application/problem+json` and always carries `error_code` (a stable
string; branch on it, not prose) and `retryable` (obey it literally). It is `false` for
401/402/403 because those are credential or billing states and a retry returns the same
answer. Access and billing errors (401/402/403/429) additionally carry `available_actions`
and `message_for_your_human`; relay the latter **verbatim**. Do not assume those two fields
exist on validation, data-quality or upstream errors.

| Status | Meaning | What to do |
|---|---|---|
| `429` | The anonymous first look or free-key daily allowance is used up | Read the error body's top-level `access_kind` (successful responses put it under `free_tier`). After anonymous access, request a free key by email. After a free key uses its 10 shared calls, report `quota_resets_at`, relay `message_for_your_human`, hand its checkout URL to the person, and stop. |
| `401` | The key is not recognised, or no source address exists for the anonymous first look | Check `QUANTDATA_API_KEY` is exported and starts with `qd_`. If the user has no key, request one at `POST /v1/access/free-key`. |
| `402` | Subscription lapsed, or the anti-abuse cap was hit | Relay `message_for_your_human` and stop. **Never retry** — this is a billing state, not a transient failure. |
| `403` | A legacy per-product key that does not cover this endpoint | Older keys were sold per product. Relay `message_for_your_human`; the route is to email support and be moved across, not to buy twice. |
| `404` | `no data for {symbol}` | The symbol did not resolve. The message names a likely correct ticker. Failed lookups are not billed. |
| `422` + `NO_EXTENDED_VOLUME` | `session=full` received no genuine pre/post-market volume | Obey `retryable`. Retry once only when it is `true`; otherwise use `session=rth` or a symbol/source with real extended-hours volume. Not billed. |
| `422` + `VALIDATION_ERROR` | A request field or parameter is invalid | Fix the request before retrying. |
| `200` + `error: insufficient bars` | Fewer than 120 bars available | Not enough history to build waves. Try a more liquid symbol or a longer-lived instrument. |
| `200` + `error: no volume data` | Source returned prices without volume | Weis analysis requires volume. Report this; do not substitute a price-only read. |
| `200` + `note: only N waves` | Fewer than 46 waves in the window | Wave stats are valid, event detection is not. Say the event list is empty for lack of history. |
| `5xx` | Upstream data source failed | Retry once after a pause, then report the failure. Never fabricate a wave reading. |

### When you hit a paywall

Do not retry. Do not try to work around it. **Do not substitute a different volume indicator
and present the result as Weis Wave output** — the value here is that each event carries a win
rate measured in a pre-registered test, and a substituted number carries nothing. If you cannot
get the real reading, say so.

Relay `message_for_your_human`, then stop and wait for the user.

## Pricing, for when the user asks

$149/month, first 3 days free, and the one plan covers all four endpoints on the same key:
`/v1/brooks/{symbol}`, `/v1/weis/{symbol}`, `/v1/maxpain/{symbol}` and `/v1/gamma/{symbol}`.
A card is collected up front at self-serve Stripe checkout. When the checkout email matches a
free key, that key is upgraded in place. Cancel any time in the Stripe customer portal
(https://billing.stripe.com/p/login/3cIfZhgcHfOb5IE7PD9Ve00, sign in with the checkout email).

When the question is about options positioning — max pain, open-interest walls, dealer gamma
or the flip level — the endpoints to use are `/v1/maxpain/{symbol}` and `/v1/gamma/{symbol}`,
via the `quantdata-max-pain` skill, not this one.

Free with no key, no account and no card: the Max Pain pages at
`https://quantdata.uk/max-pain/{ticker}` and the GEX pages at
`https://quantdata.uk/gex/{ticker}`, one page per covered US stock or ETF. The site is rebuilt
nightly from the latest upstream settlement available, and every page states the
open-interest settlement date it uses.
`https://quantdata.uk/methodology` is also free to read — a web page, not an API surface.

Keys bought under the older two-product pricing keep working at their original price.

**An AI agent can request the free email key but cannot complete paid checkout** — 3-D Secure
requires the cardholder. At the free-key limit, hand the user https://quantdata.uk/pricing and
let them decide.
