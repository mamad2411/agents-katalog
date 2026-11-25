---
name: envelope-and-attribution
description: Parse Sugra API payloads over HTTPS or MCP, keep source attribution, and tell observation time from request time. Use when reading a response, citing a figure, or shaping a large payload.
license: MIT
---

# Envelope and attribution

The API is LLM-friendly: one JSON envelope on every direction. Envelope detail also lives on https://docs.sugra.ai.

Most responses:

```json
{
  "data": {},
  "meta": {
    "endpoint": "/api/v1/...",
    "data_time": "2026-06-12T19:30:00Z",
    "response_time": "2026-06-12T19:30:01Z",
    "provider": "Sugra API"
  }
}
```

Some payloads are envelope-less (a flat object with `meta` or `_meta` on the same record). Provenance keys still apply.

HTTP: this JSON body plus `X-RateLimit-*` headers.

MCP: `call_endpoint` / `fetch_data` return the same payload (a top-level array is wrapped as `{data: ...}`). `limit` and `fields` shape the records list in `data`, and lists nested inside records are never truncated; `include_raw` attaches the complete original payload under `raw` when it fits the size cap. An object `data` without a records list, or an envelope-less object, counts as one record for `fields`, and `meta` / `_meta` stay. On the hosted server a projection that matches nothing removes nothing, and the records list can also be the one list inside an object `data`, when exactly one of `data`, `entries`, `events`, `history`, `items`, `observations`, `points`, `records`, `results`, `rows`, `series`, `timeseries` holds a list. Keys beside that list, such as `total` and `count`, stay unless a `fields` entry names a key of `data` itself, which projects `data` as one record instead. Stdio packages up to 0.12.0 do not look inside an object `data` for a records list and can return empty records when no field matches. `meta.shaped` reports `fields_applied`, `fields_unmatched`, `limit_applied` and, on the hosted server, `records_path`.

## Time

`meta.data_time` is the observation or publication clock of the data, not the HTTP response time. A row-level `as_of` is the period the figure is about. Quote both when they differ. Do not describe a delayed series as a live tick.

## Attribution

Every figure needs a source and an as-of. Read them from `meta` / `_meta`. Live list: https://sugra.ai/sources (MCP resource `sugra://attribution`).

- Sovereign, intergovernmental, and academic sources are named openly (for example FRED, IMF, ECB, NOAA, World Bank, SEC EDGAR).
- Commercial upstreams appear under Sugra-branded wrappers (Sugra Finance, Sugra News, Sugra Crypto, Sugra Forex, Sugra Weather). Do not substitute a commercial vendor name.

This is data presentation, not investment, legal, or compliance advice. Screening tools return a signal, not a determination.
