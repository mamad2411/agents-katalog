# AGENTS.md — src/providers/fetch/scrapedo/

## Purpose
Scrape.do proxy-based URL fetcher with markdown output. Tier 2 parallel race (with `scrapfly`, `decodo`).

## Vendor

- **Vendor**: Scrape.do
- **Endpoint**: `GET https://api.scrape.do?token=...&url=...&output=markdown`
- **Auth**: query param `token=<SCRAPE_DO_API_TOKEN>`
- **Env var**: `SCRAPE_DO_API_TOKEN` (note: `_API_TOKEN`, not `_API_KEY`)
- **Returns**: `FetchResult` — content is the raw markdown response body. Title via `extract_markdown_title`.

## Conventions / Invariants

- Implements `FetchProvider`.
- Uses `http_text` — the response is markdown text, not JSON.
- Sets `output=markdown` in the query string.
- Uses `AbortSignal.timeout(config.fetch.scrapedo.timeout)` directly (not `make_signal`) — no external signal composed in.

## Related

- Registered as `scrapedo` in `../../unified/fetch.ts`.
- Tier 2 parallel race in `../../../server/fetch_orchestrator.ts CONFIG.waterfall`.
