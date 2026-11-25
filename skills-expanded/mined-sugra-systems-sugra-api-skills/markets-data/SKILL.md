---
name: markets-data
description: Load this skill first, before search_endpoints or any other Sugra tool, whenever a question asks how a market instrument is priced or trading - stock, fund and index prices, earnings against expectations, yields and spreads, volatility and options, positioning and flows, exchange rates, commodities and futures curves, crypto, prediction-market odds, or comparisons across instruments. It names the call for each. Not for macro releases (macro-data), news (news-data) or weather (earth-data).
license: MIT
---

# Markets data

`knowledge/` says what to read together and how to read a price. `bindings/` says which call returns each quantity. `knowledge/concepts.yaml` is the registry of concept ids (name, unit, frequency, usual lag): open it only for a lag or unit the knowledge file does not give. Calling and quoting the envelope follow `discover-and-call` and `envelope-and-attribution`.

## Work order

1. Read `knowledge/markets.md` first, for every question. Then read the area's two files in one turn, `knowledge/<area>.md` and `bindings/<area>.yaml`, and `bindings/mechanics.md` once. Nothing else.

| Area | Covers |
|---|---|
| `markets` | price moves, returns, volume, beta, indices, holidays |
| `equities` | earnings, estimates, fundamentals, valuation, sectors |
| `positioning` | insiders, holders, shorts, fund flows, futures positions |
| `volatility` | options, implied and market volatility |
| `bonds` | yields, term premium, real curve, credit spreads |
| `fx` | exchange rates, fixings, effective rates |
| `commodities` | energy, metals, farm goods, futures curves |
| `crypto` | coins, the crypto market, on-chain flows |
| `predictions` | event probabilities |

2. Binding before search. A concept with an entry is called by its `op` through `call_endpoint` with the entry's params; never `search_endpoints` or `get_timeseries` first. A companion of another area (`rates.`, `prices.`, `news.` ...) has its entry in `bindings/<prefix>.yaml`. A placeholder `from <op>` or `from resolve_entity` (CIK, CUSIP, ISIN, market name, contract ticker) is filled by that call first. Search only for a concept with no entry; a gap is final: say so, give its substitute.
3. Small windows that cover the method, never the full history (mechanics.md section 3). The anchor and only the companions the method needs; independent calls in one turn.
4. Rules no answer may miss:
   - As of: a price carries its time, session date and delay; outside the session it is the last close, said so; older is stale.
   - Returns from the adjusted close; levels, highs and lows unadjusted.
   - Trading days (21 a month, 252 a year) for listed instruments; calendar days in UTC for coins. Name the first and last date.
   - Currency: name the quote currency; a pair is quote per unit of base; convert only with a named rate and date.
   - A position (short interest, holdings, futures positions) is a stock on a date; a flow (short volume, fund flows, trades) covers a period. A disclosure has an as-of and a publication date.
   - Yields, spreads and implied volatility change in bp, pp or points; prices in percent.
   - A computed figure is labelled computed, with its operands and dates; an estimate (model, flow, implied move, term premium) names its method.
5. The unit, currency and label in the response win over the binding. A failed call: mechanics.md section 5, then stop retrying.
6. Present: conclusion first; figures with instrument, currency, as-of time and window; companions that confirm or contradict; limits. Source and closing line follow `envelope-and-attribution`; operation ids only there. No forecast, target, or buy, sell or hold. A cause only for an event inside the window before the move. Say "not in the catalog", "call failed" or "source stale"; never fill a price from memory.
