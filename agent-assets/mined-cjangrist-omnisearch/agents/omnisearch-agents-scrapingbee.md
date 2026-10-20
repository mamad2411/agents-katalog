# AGENTS.md — src/providers/fetch/scrapingbee/

## Purpose
ScrapingBee URL fetcher. Native markdown output. Sequential fallback tier.

## Vendor

- **Vendor**: ScrapingBee
- **Endpoint**: `GET https://app.scrapingbee.com/api/v1?api_key=...&url=...&render_js=false&return_page_markdown=true`
- **Auth**: query param `api_key=<SCRAPINGBEE_API_KEY>`
- **Env var**: `SCRAPINGBEE_API_KEY`
- **Returns**: `FetchResult` — content is the raw markdown response. Title via `extract_markdown_title`.

## Conventions / Invariants

- Implements `FetchProvider`.
- Uses `http_text` for the markdown response body.
- Disables JS rendering by default (`render_js=false`) for speed; `return_page_markdown=true` is the markdown switch.

## Related

- Registered as `scrapingbee` in `../../unified/fetch.ts`.
- Sequential fallback in `../../../server/fetch_orchestrator.ts CONFIG.waterfall`.
