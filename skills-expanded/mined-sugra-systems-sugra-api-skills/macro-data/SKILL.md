---
name: macro-data
description: Load this skill first, before search_endpoints or any other Sugra tool, whenever a question asks for an economic figure or how an economy is doing - inflation and price indexes, jobs and unemployment, GDP and recession signals, policy rates and bond yields, mortgage rates and housing, money and central banks, debt and deficits, trade balances, release dates and meetings, or comparisons across countries. It names the call for each. Not for company fundamentals, market quotes, news or weather.
license: MIT
---

# Macro data

`knowledge/` says what to read together and how to read it. `bindings/` says which call returns each quantity. `knowledge/concepts.yaml` is the registry of concept ids (name, unit, frequency, usual lag): open it only for a lag or unit the knowledge file does not give. Calling and quoting the envelope follow `discover-and-call` and `envelope-and-attribution`.

## Work order

1. Pick the area, then read its two files in one turn: `knowledge/<area>.md` and `bindings/<area>.yaml`, then `bindings/mechanics.md` once. Nothing else. The parameters of the three generic ops are in mechanics.md: do not `describe_endpoint` them, and do not search for a concept with a binding or a named gap.

| Area | Knowledge file |
|---|---|
| unemployment, jobs, pay, claims, Sahm rule | `labour.md` |
| inflation and price indexes | `prices.md` |
| GDP, the current quarter, recession signals, PMI | `growth.md` |
| policy rate, yields, the curve | `rates.md` |
| construction, house prices, affordability | `housing.md` |
| central bank liquidity, money, credit | `liquidity.md` |
| trade and tariffs | `trade.md` |
| budget, debt, auctions | `fiscal.md` |
| comparing countries | `international.md` |
| release dates, meetings, consensus, revisions | `reading.md`; its bindings are `calendar.yaml` and `expectations.yaml` (there is no reading.yaml) |

2. A concept with a binding needs no search: call its `op` with `call_endpoint` and the entry's params, never `search_endpoints` first and never `get_timeseries`. Add a window (mechanics.md section 3): the latest points, not the full history. Batch independent calls in one turn.
3. Fetch the anchor and only the companions the method needs. Quote the series the question names; a neighbour is labelled as one, never given as the figure asked.
4. Derive from levels as the knowledge file says (changes, averages over months, annualised rates) and label it computed, with its last period and its base. A date in a series is the first day of its period.
5. Read each result with the methods and traps of the knowledge file; the unit and label in the response win over the binding. A failed call: mechanics.md section 5, then stop retrying. A gap or a missing source is named, with the substitute (mechanics.md section 7); a gap is final: no `search_endpoints`, `macro_search` or news for it.
6. Present: conclusion first, then figures with reference period, SA or NSA, kind of change, real or nominal, status and usual lag; companions that confirm or contradict; limits. Source and closing line follow `envelope-and-attribution`; operation ids only there. No forecast, no rating. Name the outcome honestly: "not in the catalog", "call failed" or "source stale"; never fill a number from memory or another country. Every number comes from a response, from these files or is computed from them: leave out what you only remember (times, error bands, typical values).
