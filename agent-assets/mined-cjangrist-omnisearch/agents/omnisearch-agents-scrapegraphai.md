# AGENTS.md — src/providers/fetch/scrapegraphai/

## Purpose
ScrapeGraphAI markdownify URL fetcher. Returns clean markdown. Sequential fallback tier.

## Vendor

- **Vendor**: ScrapeGraphAI
- **Endpoint**: `POST https://api.scrapegraphai.com/v1/markdownify`
- **Auth**: `SGAI-APIKEY: <SCRAPEGRAPHAI_API_KEY>`
- **Env var**: `SCRAPEGRAPHAI_API_KEY`
- **Returns**: `FetchResult` with markdown content. Title via `extract_markdown_title`.

## Conventions / Invariants

- Implements `FetchProvider`.
- Response: `{ request_id, status, website_url, result, error }`.
- Throws `ProviderError(API_ERROR)` if `status !== 'completed'` or `result` is null.

## Related

- Registered as `scrapegraphai` in `../../unified/fetch.ts`.
- Sequential fallback in `../../../server/fetch_orchestrator.ts CONFIG.waterfall`.
