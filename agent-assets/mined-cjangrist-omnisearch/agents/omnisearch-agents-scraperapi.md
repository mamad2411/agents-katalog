# AGENTS.md — src/providers/fetch/scraperapi/

## Purpose
ScraperAPI URL fetcher with markdown output. Sequential fallback tier.

## Vendor

- **Vendor**: ScraperAPI
- **Endpoint**: `GET https://api.scraperapi.com?api_key=...&url=...&output_format=markdown`
- **Auth**: query param `api_key=<SCRAPERAPI_API_KEY>`
- **Env var**: `SCRAPERAPI_API_KEY`
- **Returns**: `FetchResult` — content is the raw markdown response. Title via `extract_markdown_title`.

## Conventions / Invariants

- Implements `FetchProvider`.
- Uses `http_text` (not JSON).
- Hard-coded `output_format=markdown`.

## Related

- Registered as `scraperapi` in `../../unified/fetch.ts`.
- Sequential fallback in `../../../server/fetch_orchestrator.ts CONFIG.waterfall`.
