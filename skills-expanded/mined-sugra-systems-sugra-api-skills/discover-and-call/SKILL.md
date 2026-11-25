---
name: discover-and-call
description: Find the right Sugra operation and call it over HTTPS or MCP. Use when the path or operation_id is unknown, before guessing parameters, or after a catalog miss. Confirm details on https://docs.sugra.ai. Do not invent routes.
license: MIT
---

# Discover and call

Do not invent paths or `operation_id`s. Confirm the operation on https://docs.sugra.ai (search or Ask AI, then the endpoint page). Two complete loops, same API.

## HTTP loop

1. If the path is already known, skip to step 4 after confirming it on docs.sugra.ai.
2. Search https://docs.sugra.ai. Machine companion: `GET https://sugra.ai/openapi.json`. Coarse map: `GET /services`, `GET /sources`.
3. Read parameters and, for POST, the request body. Required names come from docs or the spec.
4. Call `https://sugra.ai` with `x-api-key`. GET uses query params. POST uses JSON body plus any path or query params the spec lists.
5. Parse `{data, meta}`. Cite source and `data_time`. Read `X-RateLimit-Remaining`.

```
GET https://sugra.ai/api/v1/etf/sectors/relative-strength?window=1m
x-api-key: sugra_...
```

## MCP loop

Works on hosted (11 tools) and stdio (8 tools). Do not call hosted-only names on stdio.

1. `search_endpoints(query=..., toolset=None, source=None, limit=10)`. Unknown `toolset` / `source` returns `unknown_toolset` / `unknown_source` with the valid set, not an empty hit list.
2. Pick an `operation_id` from `results`. Confirm it on docs.sugra.ai.
3. `describe_endpoint(operation_id=...)` - params, `request_body_schema` on POST, `agent_hints` (`duration_class`, `max_concurrency`, `bulk_cost`).
4. `call_endpoint(operation_id=..., params={...}, body=...)`.

`fetch_data(query=...)` is a one-shot. If it misses, use the four-step loop. `list_toolsets` and `list_sources` (resources `sugra://catalog/domains`, `sugra://catalog/sources`) are the map, not the query.

Shaping on `call_endpoint` / `fetch_data`: `limit` bounds the records list, `fields` (dotted paths) projects each record, and `include_raw` attaches the complete original payload under `raw` when it fits the size cap. An object `data` without a records list, or an envelope-less object, counts as one record (`meta` / `_meta` stay), and lists nested inside records are never truncated. On the hosted server a projection that matches nothing removes nothing, and the records list can also be the one list inside an object `data`, when exactly one of `data`, `entries`, `events`, `history`, `items`, `observations`, `points`, `records`, `results`, `rows`, `series`, `timeseries` holds a list (for example `data.items`). A `fields` entry that names a key of that `data` itself projects `data` as one record instead, and `meta.shaped.records_path` names the list used. Stdio packages up to 0.12.0 do not look inside an object `data` for a records list, can return empty records when no field matches, and report no `records_path`. `meta.shaped` reports what applied.

Hosted only: `resolve_entity`, `get_snapshot`, `get_timeseries`. LEI/VAT and sanctions on every transport: `sugra_entity_lookup`, `sugra_entity_screen`.

Six MCP prompts (`market_snapshot`, `macro_briefing`, `sanctions_screening`, `sector_compare`, `earth_conditions`, `source_overview`) are recipes over the eight gateway tools. They are not the catalog.

## Misses

A miss is not "Sugra has no data". Search docs.sugra.ai. Widen the query. Drop a bad MCP `toolset`/`source` filter. If MCP search still misses, fetch live `/openapi.json` (the wheel catalog can lag), then HTTP-call if the spec has it.

Do not add per-endpoint MCP tools to skip this loop.

## Timeouts

30 seconds covers most GETs. Bulk or live-upstream POSTs can run longer. MCP `agent_hints.duration_class` is the budget hint. A timeout is not empty data.
