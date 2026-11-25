---
name: oddsrelay
description: Read bookmaker odds from the OddsRelay API (raw prices per bookmaker for the UK & Ireland and 20 more regions, in-play included, UK and Irish matched boards that line up each bookmaker's back price with the exchange lay price and its liquidity, and historical odds). Use when the user asks for odds, prices, a bookmaker's margin, an each-way, extra-place, BOG, 2Up or dutching board, historical odds, an event's price history, a day's closing prices, which bookmakers carry a sport, or how many API tokens a call would cost. Needs an OddsRelay API key in ODDSRELAY_KEY.
---

# OddsRelay odds data

OddsRelay is an odds feed for bookmakers in the UK & Ireland and 20 more regions: every bookmaker's own prices (the
raw board) in every region, and, for the UK & Ireland, matched boards where each bookmaker back price sits beside the
best exchange lay price and the liquidity at that lay. The API
is documented at https://oddsrelay.io/docs and described by its OpenAPI file, https://api.oddsrelay.io/v2/openapi.json
(no key needed to read it). Read that file before using a parameter this skill does not name.

## Two ways in

1. **The MCP server** (preferred when the client supports MCP): `npx -y oddsrelay-mcp`, with `ODDSRELAY_KEY` set. Its
   tools (`sports`, `events`, `bookmakers`, `regions`, `coverage`, `odds`, `raw_odds`, `event_odds`, `history`,
   `usage`) price every call that spends tokens before it runs and refuse a call above a per-call cap. `odds` reads the
   matched boards (UK & Ireland only); `raw_odds`, `event_odds` and `history` read every region. See this repository's
   README. It does not wrap one event's price changes or the bulk history files: use HTTPS for those.
2. **HTTPS**: the key from `ODDSRELAY_KEY` as a bearer token in the `Authorization` header, base
   `https://api.oddsrelay.io`.
   Ask for `Accept-Encoding: gzip`. Never print the key, write it to a file or paste it into a message.

## Spend nothing by accident

- Discovery is free: `GET /v2/sports`, `GET /v2/events?sport=<key>`, `GET /v2/bookmakers`, `GET /v2/coverage`,
  `GET /v2/usage` (your plan, balance and key scope), `GET /v2/pricing` (the price table), `GET /v2/historical/files`
  (the list of bulk history files).
- Data routes spend tokens: `GET /v2/odds/raw`, `GET /v2/odds/event/{id}`, `GET /v2/odds/{type}` where `type` is one
  of the matched boards the coverage route lists (`standard`, `2up`, `dutching`, `each-way`, `extra-place`, `bog`).
- History routes spend tokens too: `GET /v2/historical/odds/raw` (the raw board as of a time you name; `date` and `sports`
  required, gzip only, paged by `cursor`), `GET /v2/historical/events/{id}/odds` (one event's price changes; `from`
  required), `GET /v2/historical/closing` (a day's closing lines; `date` as `YYYY-MM-DD` and `sports` required) and
  `GET /v2/historical/files/{tier}/{sport}/{file}` (one bulk file, gzip CSV bytes: save them as they come). Their prices
  are in `GET /v2/pricing` under `regions.<code>.historical`, for the region you ask.
- **Quote first.** Add `quote=true` to any data call: it returns `{cost, remaining, rate_card}` and spends nothing.
  Tell the user the cost and ask before any call that costs more than they have agreed to.
- Narrow every call: `sports` (a sport key or prefix such as `soccer` or `horse_racing`), `bookmakers`, `markets`
  (such as `h2h` or `totals`), `commenceTimeFrom` and `commenceTimeTo`. A narrow call costs a fraction of a whole board.
- The raw board is paged: follow `meta.next_cursor` (pass it back as `cursor`) until it is absent. A cursor expires
  soon after it is issued (the OpenAPI file gives how soon), so page straight through.

## Reading the data

- Prices are decimal odds. A raw event lists `bookmakers`, each with its `markets` and their `outcomes`
  (`name`, `price`), named the way that bookmaker names them.
- A matched board's outcomes carry the bookmakers' back prices beside the exchange lay price and the liquidity at that
  lay, on the same fixture, market and line.
- Each response's `meta` carries when the board was produced (`processed_at`) and, on matched boards, each
  bookmaker's last read (`last_seen`): say how old the data is from those, never guess.
- A bookmaker's margin on a market is the sum of 1/price over its outcomes, minus 1.

## Limits to tell the user

- Pre-match by default. In-play prices come with `inPlay=include` or `inPlay=only` on the raw board and on one
  event's prices, and with `inPlay=only` on the `standard` and `dutching` boards; the other matched boards are
  pre-match. No scores and no results.
- Historical odds (`/v2/historical/*`) take `region` as the live routes do. In the UK & Ireland they are recorded
  from 17 October 2026 and carry the exchanges beside the bookmakers (`bookmakersOnly=true` for the bookmakers alone).
  In each other region they are bookmakers only, from 16 November 2026 (an earlier date is 400 `date_out_of_range`).
  No starting prices. History is released a UTC day at a time, the night after the day, so today's prices come from
  the live routes.
- Bulk files: an account whose scope narrows history, or whose plan names a bookmaker list, is 403
  `files_need_whole_scope`. Only so many downloads run at once, per account and in all: one more is 429
  `too_many_downloads`, so retry after its `Retry-After` seconds. A download is charged in full before its first byte,
  so one cut off keeps its charge.
- Pull only: no websocket, webhook or stream on the self-serve plans.
- Regions: `GET /v2/regions` lists the codes your key reads; a self-serve key reads every region, each at its own
  token price. Pass one `region` a call (left out, the API uses `uk`, or answers 400 `region_required` naming the
  code to send). The raw board alone also takes a comma list of
  international codes (`region=us,global`), priced as their sum; `uk` is always asked alone. Outside the UK & Ireland
  the feed serves raw prices, one event's prices and history: a matched board there is 403 `product_not_in_region`,
  and there are no exchange prices.
- The paid self-serve plans are for personal use: one person using the data for themselves. Any business, even one
  using the data only in-house, and any product that shows the data to other people runs on Enterprise
  (https://oddsrelay.io/pricing). A business can try the data first on Free, the plan a new account starts on.
- OddsRelay is a data supplier. It gives no tips and takes no bets: describe what the prices are, never what to bet.

## Get a key

Sign up at https://app.oddsrelay.io/signup and copy the key from the dashboard. Plans and token prices:
https://oddsrelay.io/pricing.
