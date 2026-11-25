---
name: quantdata-max-pain
description: Looks up options positioning for US stocks and ETFs — max pain, open-interest call and put walls, put/call ratio, and estimated dealer gamma exposure (GEX) with the zero gamma flip level. Reads Quant Data's free public pages when no API key is set, and prefers the JSON endpoints /v1/maxpain and /v1/gamma when QUANTDATA_API_KEY is present. Use when the user asks where max pain is, about option pinning into expiration, where the call wall or put wall sits, which way dealer gamma leans, where the gamma flip level is, or how options open interest is positioned around a ticker before an expiration.
---

# Quant Data — Max Pain & Gamma Exposure

Options positioning for US-listed stocks and ETFs: max pain per expiration, the open-interest
call and put walls, put/call ratio, and estimated dealer gamma exposure (GEX) with the zero
gamma (flip) level.

There are three ways in. Check whether the environment variable **`QUANTDATA_API_KEY`** is set:

- **Key present** — use the JSON endpoints on `api.quantdata.uk`. A free email key gives all
  four endpoints 10 shared successful calls per UTC day; a paid key removes that evaluation
  limit. The options routes cover any US-listed
  stock or ETF with a liquid options chain — not just the tickers that have free pages — and
  return machine-readable figures instead of rendered HTML.
- **No key, ticker not on the free pages** — one anonymous first-look JSON response may succeed
  per source per UTC day. It is complete. For further calls, ask which email should receive a
  free key and use the request flow below.
- **No key, ticker is on the free pages** — read the public page instead and save the
  anonymous first look. It is the same number computed by the same code, and it costs nothing.

Never send an `X-API-Key` header to `quantdata.uk`. The static site does not read it, and
putting a key in a request to the wrong host is how keys leak into logs.

## Without a key — the free pages

```
https://quantdata.uk/max-pain/{ticker}   max pain, OI walls, put/call ratio, per expiration
https://quantdata.uk/gex/{ticker}        net GEX, zero gamma (flip) level, gamma walls
```

GEX lives on its **own page**, not on the max-pain page — fetch both if the user wants both
views. **The ticker goes in lowercase in the path.** An uppercase path 301-redirects to the
lowercase one, so it works either way, but link and cite the lowercase form.

### Coverage — always check, never assume

**https://quantdata.uk/max-pain** and **https://quantdata.uk/gex** are the authoritative
lists. This document deliberately does not name the covered tickers, because a hardcoded list
here goes stale silently the moment coverage changes — which has already happened once.

- The free pages cover a selected set of liquid US stocks and ETFs, and the set changes. The
  site is rebuilt nightly from the latest upstream settlement available; every ticker page
  states its own `as_of` date. Fetch the index when a ticker misses, when the user asks what is
  available, or before stating that something is not covered.
- A ticker can have a max-pain page but no GEX page: the GEX page is only built where the
  gamma estimate resolved for that night's snapshot.
- A ticker with no free page is not the end of the road: the paid endpoints below cover any
  optionable US stock or ETF. Say which surface you are reading from.

Every page carries an **`as_of` date** for the options snapshot and a separate **`spot_date`**
for the price. Read both and report them. Options open interest is end-of-day data; a page
fetched at 10am may describe a settlement from one or more prior trading days against a price
that has since moved. Never infer freshness from fetch time.

## With a key — the JSON endpoints

Base URL: `https://api.quantdata.uk`, header `X-API-Key`, keys start `qd_`. Read the key from
**`QUANTDATA_API_KEY`**. Never write a key into this file, into generated code, into a commit,
or into a message back to the user.

To request a free key, ask the user for the delivery email, then
`POST https://api.quantdata.uk/v1/access/free-key` with:

```json
{"email":"you@example.com","marketing_opt_in":false,"source":"agent"}
```

An MCP-connected agent may call `quantdata_request_free_api_key` instead. The raw key is sent
only to the inbox and never returned in the REST or MCP result. No login, password, card or GUI
is required. Never invent an email address.

`marketing_opt_in` defaults to `false` and is not required for key delivery. Set it to `true`
only after the email owner explicitly asks for occasional product updates. A `true` request is
only pending. It is confirmed only if the recipient replies `SUBSCRIBE` to the key-delivery
email; no marketing updates are sent before confirmation. Do not report the request as a
completed subscription. The free key covers all four endpoints, sharing 10 successful calls
per UTC day. Paid access is $149/month, first 3 days free, and covers the same four endpoints
without the evaluation limit.

### `GET /v1/maxpain/{symbol}` — max pain per expiration, from open interest alone

```bash
curl -s -H "X-API-Key: $QUANTDATA_API_KEY" https://api.quantdata.uk/v1/maxpain/NVDA
```

Returns every expiration inside 45 days — max pain is a per-expiration quantity and the
near-dated and far-dated figures routinely disagree, so the endpoint refuses to pick one for
you. Per expiration: `expiration`, `dte`, `max_pain`, `spot_vs_max_pain_pct`, `call_oi`,
`put_oi`, `put_call_ratio`, `highest_call_oi_strike`, `highest_put_oi_strike`. Top level:
`as_of`, `spot`, `spot_date`, `contracts`, and a `method` string you can quote. Add
`?distribution=true` for the full `oi_by_strike` detail.

- **`dte` is counted from `as_of`** — the date the open interest was measured — not from
  today. Always cite the expiration (and its dte) alongside the strike; a max pain quoted
  without its expiry is meaningless.
- Pure arithmetic: no pricing model, no volatility assumption, no fitted parameter. Anyone
  with the same chain gets the same number.

### `GET /v1/gamma/{symbol}` — estimated dealer gamma exposure

```bash
curl -s -H "X-API-Key: $QUANTDATA_API_KEY" https://api.quantdata.uk/v1/gamma/NVDA
```

Returns a `gamma` object: `net`, `gross`, `ratio`, `regime` (`positive` or `negative`),
`flip`, `flip_vs_spot_pct`, `flip_status`, `contracts_used`, `heaviest_strikes`,
`by_expiration`. Add `?by_strike=true` for the strike-level profile.

- This is a **Black-Scholes estimate**, not observed data: zero rate, zero dividend, implied
  volatility solved from each contract's end-of-day quote, and the assumption that dealers are
  long every call and short every put — a convention, not a measurement. The response's
  `method` field says so; keep that framing when you report it.
- **`flip: null` is not an error.** Check `flip_status`: `"no_sign_change_within_10pct"`
  means the chain is thick enough but net gamma keeps one sign across ±10% of spot, so the
  whole traded range reads as one regime. That is a state worth reporting, not a failure.

### Coverage and symbol rules

- **US-listed stocks and ETFs only**, with a liquid chain: at least 200 contracts across at
  least 3 expirations inside the 45-day window, otherwise `404` (never charged).
- **Cash-settled index options (SPX, SPXW, NDX, RUT, VIX) return `400`** — the chain exists
  but the price source carries no index levels, and every figure here needs the underlying
  price. Use the tracking ETF instead: SPY for SPX, QQQ for NDX, IWM for RUT.
- **Foreign exchange is not covered, and there is no workaround to suggest.** Spot FX is
  traded over the counter, so no open interest exists to compute max pain from at all. The
  currency ETFs (FXE, FXB, FXY, FXA, FXF, UUP) are listed and do have options, but their
  chains are far too thin to produce a stable figure — roughly 40–60 contracts on a single
  expiration inside the window, against the 200-contract, 3-expiration requirement — so they
  return `404`. Do not offer a currency ETF as a substitute for a pair; say the endpoints do
  not cover FX.
- Hong Kong, A-share, futures and crypto symbols return `400` — no option chain here. None of
  these rejections are charged.

### Staleness

Both options endpoints read open interest **as of the prior settlement**. They describe yesterday's
positioning and cannot update intraday, whatever the timestamp suggests — say so when you
quote them, and never present the figure as live. If the response carries `stale: true`, the
upstream was unreachable and you are reading the last snapshot held; relay the `stale_note`
and the `as_of` date prominently.

### The two numbers are not equally hard

This is why they are two endpoints instead of one. **Max pain is arithmetic** on open
interest — reproducible by anyone with the same chain. **Gamma is a model estimate** built on
an unobservable dealer-positioning convention. Quote max pain as a figure; quote gamma as an
estimate; never present the two with the same confidence.

## What the numbers mean — explain these, do not assume the user knows

**Open interest (OI)** is the number of option contracts at a given strike that are currently
open — bought and not yet closed or expired. It is a stock of existing positions, not today's
trading. It updates once a day, at settlement.

**Max pain** is the strike where the *total* payout to all option holders at expiration would
be smallest. Compute the value of every open call and put for each candidate settlement price,
add it up, and the minimum is max pain. That is all it is: an arithmetic property of the
current open-interest distribution.

The folklore attached to it — that price gets "pulled" toward max pain into expiration because
option writers hedge that way — is a **theory, and a contested one**. Say so. What the number
genuinely tells you is where the largest concentration of open interest sits and therefore
which strikes a lot of positioning cares about. Treat it as a map of where the crowd is, not
as a forecast of where price will go.

**Call wall / put wall** (`highest_call_oi_strike` / `highest_put_oi_strike`) are simply the
strikes carrying the largest call and put open interest — the two most-watched levels on the
chain. No hold rate has been measured for them; report where they are and what they are, and
leave the interpretation to the person.

**Put/call ratio** is put OI divided by call OI for an expiration. Above 1 means more open put
contracts than calls. It is commonly read as a positioning or sentiment gauge; it is also
routinely distorted by hedging and by income strategies, so it is weak evidence on its own.

**GEX (gamma exposure)** estimates the aggregate gamma that dealers hold, converted into a
notional dollar figure per 1% move. The sign is what matters:

- **Positive net GEX** — dealers are estimated to be long gamma and hedge *against* moves,
  selling into rallies and buying dips. Associated with lower realized volatility.
- **Negative net GEX** — dealers are estimated to be short gamma and hedge *with* moves.
  Associated with amplified moves.

That is a description of a mechanism, not a forecast.

**Gamma flip (zero gamma)** is the price level where net GEX crosses zero — the boundary
between those two regimes. It is a modelled estimate that depends on assumptions about who is
on which side of each contract, and the assumptions are not observable. Present it as an
estimate.

## How to present it to a human

1. **Give the date first.** "As of the {as_of} options snapshot, with spot at {spot} on
   {spot_date}" — the whole reading is worthless without it.
2. **Name the expiration.** Max pain is per-expiration and moves between them. "Max pain for
   NVDA" is not a question with one answer; "max pain for the {date} expiration" is.
3. **Give the distance, not just the level.** "Max pain is 748, about 1% above spot" tells the
   user something. A bare number does not.
4. **Give the walls with the max pain.** The call wall above and the put wall below frame the
   range that the open interest is concentrated in. That structure is more informative than
   the single max-pain strike.
5. **State the theory as a theory.** Every time. "Max pain is X. The pinning idea — that price
   drifts toward this level into expiration — is a widely-repeated hypothesis, not an
   established effect, and it weakens the further you are from expiration."
6. **Keep the two confidences apart.** Max pain and the walls are read off the chain; net GEX
   and the flip are estimated from a model. One sentence each is enough to keep them straight.
7. **Do not build a trade around any of it.** Positioning maps describe where contracts sit.
   They do not tell you direction, and reporting them as if they did is inventing a signal.

A good answer looks roughly like this — **this is a shape to copy, not data to quote.**
Always read the live page or endpoint; never repeat these figures:

> For NVDA's 2026-07-27 expiration (3 days from the snapshot date), max pain sits at $210 —
> about 1.5% above the $206.84 close from 2026-07-24, using the 2026-07-23 options snapshot.
> The biggest call open interest is at $240 and the biggest put open interest at $200. Net
> dealer gamma is estimated positive, with the zero gamma level about 2% below spot — an
> estimate that assumes dealers are long every call and short every put. All of this describes
> where contracts were sitting as of that snapshot; none of it forecasts direction, no hit
> rate has been measured for any of these levels, and the idea that price gets pulled toward
> max pain is a popular hypothesis rather than a measured effect.

## Firm rules

- **Never present this as a buy or sell recommendation.** No entries, no targets, no "expect a
  move to max pain". These are positioning maps.
- **Never give personalized investment advice.** Options carry risk of total loss of premium
  and, for short positions, of much more. If the user asks what to trade, decline and explain
  what the numbers describe.
- **No hold rate has been measured for max pain, the flip level, or any strike these surfaces
  return.** Never call them support, resistance, entry points or targets. Report where they
  are and how they were computed, and leave the interpretation to the person.
- **Never claim precision the numbers do not have.** Max pain is exact arithmetic on a
  snapshot that is already stale by the time you read it. GEX and the flip are model estimates
  built on assumptions about dealer positioning that nobody can observe directly — quote them
  as estimates, never with the same confidence as the arithmetic.
- **Never present the reading as live.** Open interest settles overnight. Name the `as_of`
  date every time.
- **Never state pinning as fact.** It is a hypothesis. Label it as one.
- **Always carry the disclaimer.** Pass through the `disclaimer` field. Educational analytics,
  not investment advice; trading involves risk of loss.
- **Do not invent coverage, and do not substitute.** If a ticker is not covered, say so rather
  than fetching numbers from a different source and presenting them as Quant Data output.

## Errors

### Free pages (no key)

| What happened | What to do |
|---|---|
| `404` on `/max-pain/{ticker}` or `/gex/{ticker}` | Not on the free pages. Fetch https://quantdata.uk/max-pain or https://quantdata.uk/gex for the current list. If the user has a key, `/v1/maxpain` and `/v1/gamma` cover any optionable US stock or ETF. Do not substitute an unrelated ticker to have an answer. |
| Ticker has a max-pain page but no GEX page | The gamma estimate did not resolve for that snapshot. Report the max-pain side and say the GEX view is unavailable for this ticker in the latest available snapshot. |
| Ticker has no listed options | Max pain does not exist for it. Say so plainly. |
| `as_of` is several days old | Report the date prominently. The site rebuilds nightly, but the upstream settlement can lag the rebuild, especially around holidays. |
| `5xx` or a fetch failure | Retry once, then report the failure. Never fabricate strikes, walls or gamma numbers. |

### API endpoints (key set)

Every API error body is `application/problem+json` and always carries `error_code` (branch on
this, not on prose) and `retryable` (obey it literally). It is `false` for 401/402/403.
Access and billing errors (401/402/403/429) additionally carry `available_actions` and
`message_for_your_human`; relay the latter **verbatim**. Do not assume those two fields exist
on validation, data-quality or upstream errors.

| Status | Meaning | What to do |
|---|---|---|
| `400` | Index option root (SPX, NDX, RUT, VIX…) | Use the tracking ETF: SPY, QQQ, IWM. Not charged. |
| `400` | HK / A-share / futures / FX / crypto symbol | These endpoints cover US-listed stock and ETF options only. For FX there is no substitute to offer. Not charged. |
| `429` | The anonymous first look or free-key daily allowance is used up | Read the error body's top-level `access_kind` (successful responses put it under `free_tier`). After anonymous access, request a free key by email. After a free key uses its 10 shared calls, report `quota_resets_at`, relay `message_for_your_human`, hand its checkout URL to the person, and stop. |
| `401` | The key is not recognised, or no source address exists for the anonymous first look | Check `QUANTDATA_API_KEY` is exported and starts with `qd_`. If the user has no key, request one at `POST /v1/access/free-key`. The free pages above still work. |
| `402` | Subscription lapsed, or the anti-abuse cap was hit | Relay `message_for_your_human` and stop. **Never retry** — this is a billing state, not a transient failure. |
| `403` | A legacy per-product key | Older keys were sold per product and these endpoints need the current plan's entitlements. Relay `message_for_your_human`; the route is to email support and be moved across, not to buy twice. |
| `404` | Chain too thin (under 200 contracts or 3 expirations inside 45 days), or no expirations in the window | Say the chain is too thin for a stable figure. Not charged. |
| `404` on `/v1/gamma` | Fewer than 100 contracts had a usable quote | No gamma estimate is possible for this snapshot. `/v1/maxpain` may still work — it needs no quotes. Not charged. |
| `503` on `/v1/gamma` | Option quotes unavailable upstream | Gamma cannot be estimated right now; `/v1/maxpain` still works. Not charged. |
| `503` | Options source down, no cached snapshot | Report the failure. Never fabricate a reading. |

At a paywall: do not retry, do not work around it, and do not substitute a different data
source and present the result as Quant Data output. Relay `message_for_your_human`, then stop
and wait for the user.

## Pricing, for when the user asks

$149/month, every Quant Data endpoint — `/v1/brooks`, `/v1/weis`, `/v1/maxpain`, `/v1/gamma` —
first 3 days free. Checkout is self-serve at **https://quantdata.uk/pricing**, a card is
collected up front. When the checkout email matches a free key, that key is upgraded in place.
Cancel any time in the Stripe customer portal
(https://billing.stripe.com/p/login/3cIfZhgcHfOb5IE7PD9Ve00, sign in with the checkout
email). Keys bought under the older two-product pricing keep
working at their original price.

**An AI agent can request the free email key but cannot complete paid checkout** — card
authentication (3-D Secure) requires the cardholder. At the free-key limit, hand the user the
link and stop. Never enter card details on anyone's behalf.

Free with no key, no account and no card: the max-pain and GEX pages above, and
`https://quantdata.uk/methodology`, which publishes how every measured number in the paid
products was tested — a web page to read, not an endpoint to call.

## Related Quant Data skills

- `quantdata-daily-bias` — `GET /v1/brooks/{symbol}`, rolling Brooks price-action events
  with measured outcome rates, plus the `day_type` block (a calibrated five-class day-type
  probability read, US day session only) and the `shape` block (arithmetic over the bars
  already printed, every window).
- `quantdata-weis-wave` — `GET /v1/weis/{symbol}`, volume-price wave structure and measured
  event statistics.

Same base URL, same key, same header.
