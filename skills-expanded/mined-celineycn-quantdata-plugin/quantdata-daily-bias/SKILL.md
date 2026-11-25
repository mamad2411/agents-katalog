---
name: quantdata-daily-bias
description: Reads rolling Brooks price-action events for a stock, ETF, futures contract, FX pair or crypto pair from the Quant Data Brooks Events API — range breakouts with measured failure rates and a calibrated per-event estimate, breakout follow-through, range position, long-range breakouts and climactic spikes — together with a calibrated five-class day-type probability read for the US day session and a plain-arithmetic description of the shape the bars already printed, and quotes fact-checked price-action statistics. Use when the user asks what just happened structurally in a market, whether a breakout has held so far, how often past breakouts like this one failed, what kind of day the session in progress could resolve into, or whether a price-action claim such as the "80% rule" actually holds up in data.
---

# Quant Data — Brooks Events

An HTTP API that detects the classical Brooks price-action events in the window trading right
now and attaches to each one the outcome rate **measured** for that exact event definition in
that exact window — pre-registered, on sixteen years of S&P 500 futures data. Range breakouts
additionally carry a calibrated per-event failure estimate.

Two further blocks travel with every read and answer different questions. `day_type` is a
calibrated probability distribution over how the session in progress could resolve — a
prediction, with published accuracy, available in the US day session only. `shape` is
arithmetic over the bars that have already printed — a measurement, with no accuracy figure
because nothing is being predicted, available in every window. Keeping those two apart is a
hard rule of this skill; see "Two blocks that are not the same thing" below.

Base URL: `https://api.quantdata.uk`

## Authentication

Send the header `X-API-Key`, with a key starting `qd_`. Read it from the environment variable
**`QUANTDATA_API_KEY`**. Never write a key into this file, into code you generate, into a
commit, or into a message back to the user.

```bash
export QUANTDATA_API_KEY="qd_..."
```

If the variable is unset, one anonymous first-look response may still succeed per source per
UTC day. It is a complete response, and its legacy-named `free_tier` object has
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

While the person decides, the Max Pain pages at `https://quantdata.uk/max-pain/{ticker}` and
the GEX pages at `https://quantdata.uk/gex/{ticker}` are permanently free, and the fact-check
verdicts are on `https://quantdata.uk/methodology`.

## Endpoint

### `GET /v1/brooks/{symbol}` — events in the live window

Optional query parameter `window`:

- **omitted** — the read follows whichever window has the freshest bars. Prefer this: markets
  close, holidays happen, and the endpoint picks the window that is actually printing.
- `window=rth` — the US day session.
- `window=gap` — 16:00–21:30 Beijing, the stretch between the Asian close and the US open.
  This window has a live read here and almost nowhere else.
- `window=asia` — 09:00–16:00 Beijing.

`gap` and `asia` are **only accepted for 24-hour instruments**: futures (`ES=F`, `NQ=F`,
`GC=F` …), spot FX (`EURUSD`) and crypto (`BTC-USD`). Stocks and ETFs trade the US day session
only, so passing either for them returns `400`. These three are the **only** accepted values;
anything else returns `400`. The older `session` parameter was replaced by `window` on
2026-08-06; the day-type read is no longer selected by a parameter at all, it arrives as the
`day_type` block of every response — see "The day-type read" below.

```bash
curl -s -H "X-API-Key: $QUANTDATA_API_KEY" \
  https://api.quantdata.uk/v1/brooks/ES=F
```

Response (a gap-window read — the one window with no day-type model, so `day_type` comes
back unavailable with its reason and `shape` carries the arithmetic description):

```json
{
  "symbol": "ES=F",
  "window": "gap",
  "window_is_live": true,
  "session": "2026-08-06",
  "bars": 41,
  "quote": {"open": 6362.25, "high": 6371.5, "low": 6355.0,
            "last": 6368.75, "prev_close": 6360.5, "change_pct": 0.13},
  "source": "leandata",
  "volatility_base": {"avg_daily_range_5d": 62.75,
    "definition": "mean high-low range of the last 5 completed US regular sessions"},
  "events": [
    {
      "type": "range_breakout",
      "direction": "up",
      "at": "2026-08-06T18:05:00+08:00",
      "bars_since": 6,
      "breakout_level": 6366.0,
      "range": {"low": 6358.25, "high": 6366.0},
      "outcome_so_far": {"failed_within_10_bars": null, "resolved": false,
                         "bars_observed": 6},
      "conditional_estimate": {
        "p_fail_within_10_bars": 0.58,
        "meaning": "Of past breakouts whose own rolling context looked like this one, this share closed back through the breakout level within 10 bars."
      },
      "reference": {"failure_rate_pct": {
        "within_5_bars":  {"rate_pct": 50.4, "n": 3918},
        "within_10_bars": {"rate_pct": 62.8, "n": 3916},
        "within_20_bars": {"rate_pct": 72.4, "n": 3882}}}
    }
  ],
  "day_type": {
    "available": false,
    "why": "No day-type model has been trained or validated for the gap window. The day session has its own model (mode=day_session) and the Asian window has its own (mode=asia_session); the gap window is covered by the `shape` block and the event reads instead.",
    "window_note": "Two validated day-type reads exist, each from a model trained on its own window: the regular day session (mode=day_session, with its published accuracy) and the Asian window (mode=asia_session, trained natively on Asian windows under a pre-registered protocol with its own label taxonomy — the two accuracy sets are not comparable) ..."
  },
  "shape": {
    "bars_measured": 41,
    "net_move_pct_of_range": 61.2,
    "close_position_in_range": 0.83,
    "one_way_share": 0.58,
    "deepest_pullback_pct_of_range": 24.5,
    "high_made_at": 0.92,
    "low_made_at": 0.04,
    "direction_changes": 3,
    "range_tightness": 0.74,
    "how_to_read": "Arithmetic over the last 41 five-minute bars — what this stretch did, not what comes next. ...",
    "not_a_forecast": "Measured description of bars that have already printed. It carries no accuracy figure because nothing is being predicted, and it is not the day-type classification — that is a separate, model-based read with its own published accuracy."
  },
  "disclaimer": "Educational analytics, not investment advice."
}
```

In the US day session the same `day_type` block is the day-session read, which carries the
published 66%/80% accuracy; in the Asian window it is the natively trained
`mode: "asia_session"` read with its own pre-registered accuracy (see "The day-type read"
below):

```json
"day_type": {
  "available": true,
  "mode": "day_session",
  "bars_read": 54,
  "probs": {"TrendUp": 0.34, "Reversal": 0.22, "TrendingRange": 0.21,
            "Range": 0.2, "TrendDown": 0.03},
  "meaning": "Calibrated probability distribution over the five day types this session could resolve into. Report the distribution, not just the top class — the second script is often very much alive.",
  "accuracy": "Measured on held-out S&P 500 E-mini years the model never trained on: at 18 bars (90 minutes in) top-1 53.5% and top-2 68.6%; over a complete session 66% and 80%. The majority class covers 37% of days — quote that baseline alongside any accuracy figure. Calibration error is under 10% ..."
}
```

Field notes:

- `events` holds each classical event detected in this window today — **first occurrence per
  type per window**, because that is the definition the reference rates were measured under,
  so the live detection and the published numbers describe the same population. An empty array
  means nothing has fired yet; `no_events_note` then says so. **That is a finding, not an
  error** — report it as one.
- `window` is the window the events were built on; `session` is the window-local trading date
  the read covers, not today's wall-clock date.
- `window_is_live` — **check this before you use the word "today" or "now".** `true` means the
  window is open right now and you are reading it in progress. `false` means you are holding
  the **last completed** window; `window_note` then says which one, and whether the window is
  simply closed or has opened without bars arriving yet. Relay it and name the date.
- `bars` counts the 5-minute bars inside the window so far. `window_progress_note` appears
  when too few bars have printed for a range event to exist yet — an early window with no
  events is expected, not broken.
- `volatility_base` is the 5-day average daily range every event definition is scaled by.
  Fewer than 3 completed US sessions of history and the endpoint returns `404` rather than
  guessing it.
- `reference` on each event carries the outcome rate measured for that event type **in the
  window it fired in**, with `n`. The three windows were measured separately; never quote one
  window's rate for another's event.
- `conditional_estimate` appears on `range_breakout` events only — see below.
- `coverage_note` appears on every symbol other than `ES=F`, `NQ=F` and `QQQ`: the reference
  rates and the conditional model are context there, not validated claims. Relay it.
- `symbol_note` appears when the ticker resolved to something the user probably did not mean
  (for example `GOLD`). **Always relay it.**
- `day_type` carries `mode` — the model trained for the current window. `day_session`
  (the rth window): `probs` (five classes, highest first, summing to 1), `meaning` and
  `accuracy` (the 66%/80% set), plus `provisional_note` when fewer than 18 bars have
  printed. `asia_session` (the Asian window of 24-hour instruments): a separate model
  trained natively on Asian windows, pre-registered and confirmed zero-shot on NQ; its
  `accuracy` field carries its own figures on its own label taxonomy. **Never mix the two
  accuracy sets** — quoting 66%/80% for an asia read (or the asia figures for a day-session
  read) is a fabrication. The gap window returns `available: false` — no model has been
  validated there; `available: false` also appears when history is too short.
- `shape` is present in every window as soon as ten bars exist, and never carries an accuracy
  figure. Its `how_to_read` explains each number in plain words and `not_a_forecast` states
  what it is not. Pass both through rather than paraphrasing them into a verdict.

## The five event types

| Event | What it is, and what comes attached |
|---|---|
| `range_breakout` | The day's first close outside a tight trading range. Carries the measured failure rates for its window — in the US session, 52.1% of past breakouts closed back through the level within 5 bars, 62.6% within 10 and 70.6% within 20 (about 3,900 events per horizon, one per day); the gap window measured 50.4 / 62.8 / 72.4 and the Asian window 46.7 / 58.7 / 69.4 — plus a calibrated per-event estimate. |
| `breakout_follow_through` | The bar after a breakout closes beyond the breakout bar's extreme. Carries the measured rate at which the projected measured-move target was touched before the window closed. |
| `range_position` | A close in the top or bottom third of an established range. Honest asymmetry, reported rather than averaged away: only the bottom-third ("first move up") half carries measured support, strongest in the Asian window at 55.6%; the top-third ("first move down") half did not confirm in the US session or the gap window. |
| `long_range_breakout` | A breakout from a range that has held for 20+ bars. The tradition says the direction is 50/50; the measured split is skewed upward in every window — 57.8% in the US session — a counter-example to the classical claim, reported as measured. |
| `climactic_spike` | Two or more consecutive strong bars closing near their extremes with little overlap. Carries the measured rate at which the spike's projected target was touched. |

## The conditional estimate

Every breakout looks different: how tight the range was, how strong the breakout bar was, how
often the range had been tested. `conditional_estimate.p_fail_within_10_bars` feeds features
of the event you are looking at into a small model and returns a **calibrated** probability
that this particular breakout closes back through its level within 10 bars.

The validation was pre-registered and zero-shot on NQ futures 2023+ — an instrument **and** a
period the model never trained on: AUC 0.646, with the lowest predicted tercile actually
failing 54.2% of the time against 79.1% for the highest, calibration error 5.1%, n=2,637. A
second zero-shot check on QQQ measured AUC 0.660 (n=2,017).

"Calibrated" means that across many events where the model said 60%, the outcome happened
about 60% of the time. It is a testable property of the probabilities, not a claim about how
good the model is — and it is what lets the number go into an expected-value calculation
instead of being a vibe.

Keep the two kinds of numbers apart when you report them. The `reference` block is a static,
window-level, pre-registered rate for all events of that type. The `conditional_estimate` is
per-event and model-based. Say which one you are quoting.

## The day-type read

`day_type` is the five-class day-type probability distribution for the session in progress:
`TrendUp`, `TrendDown`, `Range`, `TrendingRange`, `Reversal`. It is a sequence model reading
the session's 5-minute bars from the open, and it is calibrated — across many sessions where
it said 70%, roughly 70% resolved that way.

Two validated reads exist, each from a model trained on its own window. The `rth` window
serves `mode: "day_session"` — everything in the accuracy section below applies to it
**only**. The Asian window serves `mode: "asia_session"`: a model trained natively on Asian
windows under a pre-registered protocol (confirmed zero-shot on NQ), whose accuracy —
top-1 35.7/38.5/41.0% at 18/42/63 bars on held-out ES (n=908, baseline 30.2%), NQ
35.2/40.1/45.4% (n=915, baseline 29.9%) — uses its own frozen labelling rule and is **not
comparable** to the day-session figures; its known weakness (near-blind on TrendingRange,
unpowered on Reversal) is disclosed in the response. Quoting either mode's figures for the
other is a fabrication. The gap window has no validated model and returns
`available: false`; the `shape` block covers every window with plain arithmetic either way.

**Accuracy, and the baseline it must always travel with.** Measured on held-out S&P 500
E-mini years the model never trained on: over a complete session top-1 **66%** and top-2
**80%**; at the 18-bar mark (90 minutes in) top-1 **53.5%** and top-2 **68.6%**. The
majority class covers **37%** of days, and calibration error is under **10%**.

**Never quote 66% without the 37% baseline in the same sentence.** On its own it reads as
twice as good as a coin flip; against the baseline it is what it is — an honest, modest
improvement over always guessing the most common day type. The same rule applies to 53.5%.

Report the distribution, not only the top class. When the top two classes are 0.34 and 0.22
the second script is very much alive, and collapsing that into "today is a trend-up day" is a
misreading of what a probability distribution says. If `provisional_note` is present, fewer
than 18 bars have printed and nothing has been measured that early — relay it.

The accuracy figures were measured on ES. On any other symbol the read is descriptive and
carries no accuracy claim; say so in the same breath.

## The shape block

`shape` is arithmetic over the bars that already printed in this window — up to the last 81
5-minute bars. There is no model in it, so there is nothing to be right or wrong about, and
anyone with the same bars computes the same numbers.

| Field | What it measures |
|---|---|
| `bars_measured` | How many bars the description covers |
| `net_move_pct_of_range` | Net move from the first open to the last close, as a percentage of the stretch's own high-low range |
| `close_position_in_range` | Where the last close sits inside that range — 1.0 at the top, 0.0 at the bottom |
| `one_way_share` | Net move divided by total travel — near 1.0 is close to a straight line, near 0 means it retraced most of what it covered |
| `deepest_pullback_pct_of_range` | Largest counter-move against the net direction, as a share of the range |
| `high_made_at` / `low_made_at` | Where the extremes landed — 0 is the start of the stretch, 1 is the latest bar |
| `direction_changes` | Turns in the smoothed close |
| `range_tightness` | Range height against the bar-to-bar movement that produced it; under 1 is a coiled range rather than a directional run |

Report it as description: "over the last 41 bars price finished near the top of its own range,
about 58% of the travel was one-way, and the low was set in the first few bars." That sentence
is checkable. Anything that turns those numbers into what happens next is not.

## Two blocks that are not the same thing

|  | `day_type` | `shape` |
|---|---|---|
| Answers | what the session could resolve into | what the stretch just did |
| Nature | a prediction, and it can be wrong | a measurement, with nothing to be wrong about |
| Track record | published accuracy against a stated baseline | none, and none is needed |
| Availability | the US day session only | every window, including the gap |

**Do not name `shape` output a day type.** It is not a trend day, not a reversal day, not a
range day, not a Brooks classification — those words belong to the model-based read that has a
measured track record. **Do not attach 66%, 80%, 53.5% or any other accuracy figure to
`shape`.** Borrowing a validated model's credibility for a descriptive statistic is exactly
the kind of thing this product exists not to do. And do not describe `shape` as pointing at
what comes next; it describes bars that are already on the chart.

## Resolving what the user said into a symbol

**Resolve an instrument name to a ticker before you call.** Passing a plain English name is
the most common mistake and it produces a wrong answer more often than an error.

| User says | Send |
|---|---|
| a US stock or ETF | the ticker as-is — `NVDA`, `TSLA`, `SPY`, `QQQ` |
| a Hong Kong stock | digits + `.HK`, padded to four — Meituan = `3690.HK`, Tencent = `0700.HK` (not `700.HK`) |
| a China A-share | the 6-digit code — Kweichow Moutai = `600519`, Ping An = `000001` |
| a futures contract | Yahoo-style suffix — `ES=F`, `NQ=F`, `GC=F`, `CL=F`, `YM=F` |
| Bitcoin / Ethereum | `BTC-USD` / `ETH-USD` |
| a currency pair | the pair with no slash — `EURUSD`, `GBPUSD`, `USDJPY` (`EUR-USD` works too; `EUR/USD` does **not** — the slash splits the URL path and 404s) |
| "the S&P", SPX, US500 | `SPY` (ETF) or `ES=F` (futures) |
| "the Nasdaq", NAS100 | `QQQ` or `NQ=F` |
| "the Dow", US30 | `DIA` or `YM=F` |
| **gold**, XAU, spot gold | `GC=F` (COMEX futures) or `GLD` (ETF). `XAUUSD` answers with the `XAUT-USD` token reading plus a note (see below). |
| **tokenised gold**, XAUT, Tether Gold | `XAUT-USD` — a different instrument from spot gold (see below) |
| oil, WTI, crude | `CL=F` or `USO` |

**The gold trap.** `GOLD` is a valid ticker — it is a US-listed equity, Gold.com, Inc. It is
not the metal. If the user means the metal, send `GC=F` for futures or `GLD` for the ETF.
**Spot gold itself is not covered** — serving it needs a licensed spot-metal feed we do not
have. A request for `XAUUSD` answers with the `XAUT-USD` token reading plus a `symbol_note`
saying exactly that; relay the note, and if the user wants the metal itself, use `GC=F`. If you do send `GOLD`, the API returns a `symbol_note` warning about
exactly this; relay it verbatim.

**`XAUT-USD` is not a spot-gold substitute.** It reads the Tether Gold token's order book on
a crypto exchange. The token is redeemable for allocated LBMA gold, but it has consistently
traded at a discount to spot, the size of that discount moves over time, and it keeps trading
on weekends when the gold market is closed. Send it only when the user asked for tokenised
gold, or relay what the API itself returned for a spot-gold request (it self-reports the
swap in a `symbol_note`). Responses for it carry an `instrument_note` stating all of this
and noting that the pre-registered ES win rates do not transfer to it; relay that note
verbatim, and never present its readings as spot-gold readings.

`XAUT-USD` is a 24-hour instrument, so `window=gap` and `window=asia` work on it the same way
they do on futures — including weekends, when the gold market itself is closed.

Six-digit codes are normalized server-side to `.SS` (Shanghai) or `.SZ` (Shenzhen), so
`600519` comes back as `600519.SS`. `HK:3690` and `03690.HK` both normalize to `3690.HK`.
Hong Kong codes shorter than four digits are padded, so `700.HK` and `HK:700` both come back
as `0700.HK` — the four-digit form is what the price source recognizes.

When you are unsure, try the ETF. A `404` response contains a hint naming the likely correct
ticker, and a failed lookup is not billed.

## Worked example

Python, no dependencies beyond the standard library:

```python
import os, json, urllib.request

def qd(path):
    key = os.environ["QUANTDATA_API_KEY"]          # never hard-code
    req = urllib.request.Request(
        f"https://api.quantdata.uk{path}", headers={"X-API-Key": key})
    return json.load(urllib.request.urlopen(req, timeout=20))

r = qd("/v1/brooks/ES=F")
live = "live" if r["window_is_live"] else "last completed"
print(f"{r['symbol']} {r['window']} window {r['session']} ({live}, {r['bars']} bars)")
for ev in r["events"]:
    print(f"  {ev['type']} at {ev['at']}")
    ce = ev.get("conditional_estimate")
    if ce:
        print(f"    calibrated p(fail within 10 bars): {ce['p_fail_within_10_bars']:.0%}")
if not r["events"]:
    print(" ", r.get("no_events_note", "no events in this window yet"))

dt = r.get("day_type", {})
if dt.get("available"):
    top = list(dt["probs"].items())[:2]
    # always report the 37% majority-class baseline next to any accuracy figure
    print("  day type:", ", ".join(f"{k} {v:.0%}" for k, v in top))
else:
    print("  day type: not available —", dt.get("why"))

sh = r.get("shape")
if sh:                                  # description of bars already printed, not a forecast
    print(f"  shape: closed at {sh['close_position_in_range']:.0%} of its own range, "
          f"{sh['one_way_share']:.0%} of the travel one-way")
```

## How to present the result to a human

This is the part that matters. The numbers are small and honest; your job is to keep them
that way.

**Date and place the read.** Name the window and the session date it covers. If
`window_is_live` is `false`, you are describing the last completed window — relay
`window_note` and do not say "today" or "right now".

**Quote the rate for the window the event fired in, with its `n`.** A gap-window breakout gets
the gap-window rates. "Historically 62.8% of gap-window breakouts closed back through the
level within 10 bars" is a sentence a person can check; "breakouts usually fail" is not.

**Keep reference and estimate apart.** The reference rate describes all past events of this
type in this window; the conditional estimate describes this one event. Both are historical
frequencies dressed as probabilities — neither is a forecast of price, and neither knows what
happens next.

**An empty events array is a finding.** Most of these definitions fire at most once per window
per type. "Nothing has fired yet" is information about the day so far — report it as such.

**Quote the day-type distribution with its baseline.** Give the top two classes with their
probabilities, then the accuracy figure and the 37% majority-class baseline together — "66%
top-1 on held-out years, against 37% for always guessing the most common day type". A single
accuracy number with no baseline overstates the read. Outside the US day session, say the read
does not exist there and why, rather than implying it is missing.

**Describe `shape`, do not upgrade it.** It is arithmetic over bars that already printed. Call
it what it is — where price closed inside its own range, how much of the travel was one-way,
where the extremes landed. Never label it a trend day or a reversal day, never give it an
accuracy figure, and never present it as an indication of what comes next.

**Report the contradictions as measured.** The long-range breakout direction split is not
50/50, and the sell-zone half of the range-position claim did not confirm. The response says
so; do not soften it back toward the textbook.

**Flag coverage, every time.** The reference rates were measured on ES; the conditional model
was validated on ES, NQ and QQQ. On any other symbol — single stocks, gold, crypto, Hong Kong
or A-share names — the response carries a `coverage_note` and the numbers are context about
ES, not claims about that market. Say that plainly rather than burying it.

**When quoting folklore, answer from the verdicts below rather than from memory, and quote
both numbers.**

## The famous claims, fact-checked

Measured against S&P 500 E-mini 5-minute data, 2010–2026:

| Claim | Taught as | Measured | Sample |
|---|---|---|---|
| 90 minutes in, one side's daily extreme is already set | 90% | 81.2% | 3,946 days |
| On a bull day, the low forms in the first third | 90% | 83.3% | 3,946 days |
| After an opening-range breakout, the opposite extreme holds | 90% | 83.5% | 3,578 days |
| Trading-range breakouts fail (the "80% rule") | 80% | 52.1% / 62.6% / 70.6% within 5 / 10 / 20 bars | ~3,900 events |
| A breakout from a long-lived range goes either way 50/50 | 50/50 | 57.8% upward — claim reversed | 2,745 events |

The pattern: directionally mostly right, inflated by roughly 7–10 percentage points — and two
claims failed outright. The "80% rule" never reaches 80% under any definition tested; measured,
it tops out around 70% at the 20-bar horizon. The full set of verdicts, with sample sizes, is
published as a static table on `https://quantdata.uk/methodology`. That is an ordinary web
page — free to read, no key — so point a person there if they want to check the working
themselves.

## `POST /v1/brooks/backtest` — check the calibration yourself

The same detectors, run over 5-minute bars the caller supplies: it detects events day by day
and returns the model's probability next to the actual outcome, with a binned calibration
table. Use it when a user wants to verify the calibration on their own instrument instead of
taking the published NQ and QQQ numbers on trust. Full parameters are in the API reference at
`https://quantdata.uk/docs`.

## What happened to the day-type read

Until 2026-08-06 this path served the five-class day-type probability read on its own. On
2026-08-06 the endpoint was replaced by the rolling event read and the day-type read went
offline briefly; on **2026-08-07 it was restored**, and it now arrives as the `day_type` block
inside every response rather than as the whole response.

The reason for the change was coverage, not a failed result: a day type is a property of a
whole session, and for roughly eleven hours a day no session is running, so a day-type-only
endpoint had nothing live to say. Events are anchored to local structure instead of a session
open, so a read exists around the clock on 24-hour instruments. Restoring `day_type` as a block
keeps the session read where it applies — **the US day session only** — while the gap and Asian
windows get events and the `shape` description.

If an older note claims the day-type read no longer exists anywhere in the API, that is out of
date. It is the same model and the same published numbers as before: 66% top-1 and 80% top-2
over a complete session on held-out years, 53.5% and 68.6% at the 90-minute mark, against a
37% majority-class baseline, calibration error under 10%. The day-type gating study that the
`quantdata-weis-wave` skill describes is unchanged and remains published on
`https://quantdata.uk/methodology`.

## Firm rules

- **Never present output as a buy or sell recommendation.** No "go long", no "this is a buy",
  no entry, stop or target. The API returns detected events with measured historical
  frequencies attached. It does not know the user's position, account, horizon or risk
  tolerance, and it is not a forecast of price.
- **Never give personalized investment advice.** If the user asks "should I buy", explain what
  the event and its measured rates describe and decline the recommendation.
- **Always carry the disclaimer.** Pass through the `disclaimer` field. Educational analytics,
  not investment advice; trading involves risk of loss.
- **Never claim precision the numbers do not have.** Do not round 62.6% into "most breakouts
  fail", do not call any of this a signal, and never quote a rate without its window and `n`.
  If a number is descriptive rather than validated for that asset, say so in the same sentence.
- **Never quote a day-type accuracy figure without the 37% majority-class baseline**, and
  report the probability distribution rather than only its top class.
- **Never present `shape` as a day type, a trend day or a reversal day, and never give it an
  accuracy figure.** It is arithmetic over bars that already printed; the day-type numbers
  belong to the model-based read alone, and borrowing them for a descriptive statistic
  misrepresents both.
- **Do not invent statistics.** Every number in this file is measured. If the user asks
  something not covered here or on `https://quantdata.uk/methodology`, say you do not know.
- **Quant Data is independent research**, not affiliated with or endorsed by Al Brooks,
  Brooks Trading Course, or any exchange or broker. Do not reproduce course material — the API
  returns measured statistics and Quant Data's own event definitions only.

## Errors

Every API error body is `application/problem+json` and always carries:

- `error_code` — a stable string (`NO_API_KEY`, `INVALID_API_KEY`, `PRODUCT_NOT_ENTITLED`,
  `SUBSCRIPTION_EXPIRED`, `USAGE_CAP_REACHED`). Branch on this, not on prose.
- `retryable` — obey it literally. It is **`false` for 401/402/403** because those are billing
  or credential states and a second attempt returns the same answer.

Access and billing errors (401/402/403/429) additionally carry `available_actions` and
`message_for_your_human`. Relay the latter **verbatim**. Do not assume those two fields exist
on validation, data-quality or upstream errors.

| Status | Meaning | What to do |
|---|---|---|
| `400` | An unrecognised `window` value, or `window=gap`/`window=asia` sent for a stock or ETF | Drop the parameter, or use a 24-hour instrument — futures (`=F`), spot FX, crypto. Only `rth`, `gap` and `asia` exist; the old `session` parameter was replaced by `window` on 2026-08-06. Not billed. |
| `429` | The anonymous first look or free-key daily allowance is used up | Read the error body's top-level `access_kind` (successful responses put it under `free_tier`). After anonymous access, request a free key by email. After a free key uses its 10 shared calls, report `quota_resets_at`, relay `message_for_your_human`, hand its checkout URL to the person, and stop. |
| `401` | The key is not recognised, or no source address exists for the anonymous first look | Check `QUANTDATA_API_KEY` is exported and starts with `qd_`. If the user has no key, request one at `POST /v1/access/free-key`. |
| `402` | Subscription lapsed, or the anti-abuse cap was hit | Relay `message_for_your_human` and stop. **Never retry** — this is a billing state, not a transient failure. |
| `403` | A legacy per-product key that does not cover this endpoint | Older keys were sold per product. Relay `message_for_your_human`; the route is to email support and be moved across, not to buy twice. |
| `404` | `no data for {symbol}` | The symbol did not resolve. The message names a likely correct ticker — use it. Failed lookups are not billed. |
| `404` | `insufficient sessions` | Upstream history holds fewer than 3 completed US regular sessions, so the volatility base cannot be established — typically a thin instrument or a long market holiday. Try a more liquid symbol. Not billed. |
| `5xx` | Upstream data source failed | Retry once after a short pause, then report the failure. Do not fabricate a reading. |

### When you hit a paywall

Do not retry. Do not try to work around it. **Do not substitute a different data source and
present the result as Quant Data output** — the entire value of this service is that its
numbers trace to a specific measurement, and a substituted number does not. If you cannot get
the real reading, say so.

Relay the `message_for_your_human` string, then stop and wait for the user. Readings update on
a 5-minute bar, so polling faster than that returns the same read anyway.

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
The fact-check verdicts are also published as a static table on
`https://quantdata.uk/methodology` — an ordinary web page a person can read, not an API.

Keys bought under the older two-product pricing keep working at their original price.

**An AI agent can request the free email key but cannot complete paid checkout** — 3-D Secure
requires the cardholder. At the free-key limit, hand the user https://quantdata.uk/pricing and
let them decide.
