# AGENTS.md — src/providers/fetch/brightdata/

## Purpose
Bright Data Web Unlocker URL fetcher. Aggressive anti-bot bypass; native markdown output via `data_format=markdown`. Tier 3 solo (after the parallel proxy group).

## Vendor

- **Vendor**: Bright Data
- **Endpoint**: `POST https://api.brightdata.com/request`
- **Auth**: `Authorization: Bearer <BRIGHT_DATA_API_KEY>`
- **Env vars**:
  - `BRIGHT_DATA_API_KEY` (required)
  - `BRIGHT_DATA_ZONE` (optional, default `unblocker`)
- **Returns**: `FetchResult` — content is the raw markdown response body. Title via `extract_markdown_title`.

## Conventions / Invariants

- Implements `FetchProvider`.
- Uses `http_text` (not `http_json`) — the response body is markdown text, not JSON.
- Body: `{ zone, url, format: 'raw', data_format: 'markdown' }`.

## Gotchas

- **`BRIGHT_DATA_ZONE` is reset to `'unblocker'` on every `initialize_config`**, then re-applied if set. This prevents stale zone names from surviving after the env var is removed.

## Related

- Registered as `brightdata` in `../../unified/fetch.ts`.
- Tier 3 in `../../../server/fetch_orchestrator.ts CONFIG.waterfall`.
