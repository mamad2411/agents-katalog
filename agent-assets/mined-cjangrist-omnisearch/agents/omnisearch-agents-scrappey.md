# AGENTS.md — src/providers/fetch/scrappey/

## Purpose
Scrappey headless browser URL fetcher. Returns `innerText` (plain text), not markdown. Sequential fallback tier.

## Vendor

- **Vendor**: Scrappey
- **Endpoint**: `POST https://publisher.scrappey.com/api/v1?key=<SCRAPPEY_API_KEY>`
- **Auth**: query param `key=<SCRAPPEY_API_KEY>` (URL-encoded)
- **Env var**: `SCRAPPEY_API_KEY`
- **Returns**: `FetchResult` with `solution.innerText` as content. Title via `extract_html_title` (Scrappey returns HTML in `solution.response`).

## Conventions / Invariants

- Implements `FetchProvider`.
- Response: `{ solution: { innerText, response, currentUrl, statusCode }, data }`.
- **Returns plain text**, not markdown — better for "give me everything visible on the page" but worse for structure-aware fetching.

## Related

- Registered as `scrappey` in `../../unified/fetch.ts`.
- Sequential fallback in `../../../server/fetch_orchestrator.ts CONFIG.waterfall`.
