---
name: earth-data
description: Load this skill first, before search_endpoints or any other Sugra tool, whenever a question asks about conditions at a place - weather observed, forecast or past, climate normals and projections, natural hazards and warnings, rivers, tides and water levels, power grids, crops and growing-season weather, disruption to ports, flights and roads - or how such an event feeds energy, commodity or output data. It names the call for each. Not for macro series, market prices or news alone.
license: MIT
---

# Earth data

`knowledge/` says what to read together and how to read it. `bindings/` says which call returns each quantity. `knowledge/concepts.yaml` is the registry of concept ids (name, unit, frequency, usual lag): open it only for a lag or unit the knowledge file does not give. Calling and quoting the envelope follow `discover-and-call` and `envelope-and-attribution`.

## Work order

0. A question about meaning, a difference between terms or what to do (no figure for a place and a time asked) is answered from `knowledge/` alone: no data call, not even one to illustrate.
1. Read `knowledge/earth-reading.md` for every question. Then pick the area and read its two files in one turn, `knowledge/<area>.md` and `bindings/<area>.yaml`, then `bindings/mechanics.md` once. A companion of another area (`commodities.*`, `prices.*`, `trade.*`) is bound in `bindings/<that area>.yaml`.

| Area | Files |
|---|---|
| weather now, forecast, history, degree days, growing regions | `weather` |
| normals, long series, projections, El Nino | `climate` |
| warnings, storms, quakes, fires, volcanoes, space weather, air | `hazards` |
| rivers, gauges, floods, tides, surge, waves | `water` |
| grid load, fuel mix, flows, power price, plants | `power` |
| refineries exposed to a hazard, offshore output | `industry` |
| crop condition, yields, production, export flows | `crops` |
| airports, delays, ports, roads, freight | `logistics` |

2. Resolve the place and the time first: the point, station, gauge, airport, box or grid region the entry asks for; its time zone; the window, with the day boundary named (local or UTC). A site or station number comes from the question, the user or an earlier answer, never invented.
3. The binding is the route. Open the concept's entry before any catalog search: a concept with a binding needs no `search_endpoints`; call its `op` with `call_endpoint` and the entry's params, filled from step 2. mechanics.md sections 1 and 4-7 apply here; its parameter lists in section 3 are for the macro ops. Keep windows and limits small. Batch independent calls in one turn.
4. Keep the kinds apart: observation, model forecast, reanalysis, normal, projection, official warning, automatic or computed estimate. A model value is never an observation; an automatic alert or computed index is never an official warning.
5. An anomaly needs a named baseline: same place, same calendar window, base period named (1991-2020, or "computed, N years"). No "hot", "dry", "record" or "extreme" without it.
6. State the unit of every figure as the response gives it (degC or degF, m3/s or ft3/s, MW, metres above which datum); the response wins over the binding. One datum and one unit before subtracting.
7. A failed call: mechanics.md section 5, then stop retrying. A gap is final: say "not in the catalog" and give the entry's substitute, named as a substitute; no `search_endpoints` or news for it. A place outside a feed's coverage is a coverage gap, said as such, never filled from a neighbouring point, another country or memory.
8. Present: conclusion first; each figure with its kind, place, time (UTC and local), unit and baseline; the chain from event to exposure to the series asked, each market with its own sign; provisional readings flagged; limits. No safety advice: quote the warning in force and its issuer. Source and closing line follow `envelope-and-attribution`; operation ids only there.
