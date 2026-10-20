# AGENTS.md — src/providers/fetch/scrapeless/

## Purpose
Scrapeless Web Unlocker with JS rendering. Markdown response. Sequential fallback tier.

## Vendor

- **Vendor**: Scrapeless
- **Endpoint**: `POST https://api.scrapeless.com/api/v2/unlocker/request`
- **Auth**: `x-api-token: <SCRAPELESS_API_KEY>`
- **Env var**: `SCRAPELESS_API_KEY`
- **Returns**: `FetchResult` with markdown content. Title via `extract_markdown_title`.

## Conventions / Invariants

- Implements `FetchProvider`.
- Response: `{ code: 0, data: <markdown> }` — `code=0` is success.
- Body sets `js_render: true` and `response_type: 'markdown'`.

## Related

- Registered as `scrapeless` in `../../unified/fetch.ts`.
- Sequential fallback in `../../../server/fetch_orchestrator.ts CONFIG.waterfall`.
