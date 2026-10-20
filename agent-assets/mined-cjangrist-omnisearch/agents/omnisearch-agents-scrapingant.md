# AGENTS.md — src/providers/fetch/scrapingant/

## Purpose
ScrapingAnt LLM-ready markdown URL fetcher. Sequential fallback tier.

## Vendor

- **Vendor**: ScrapingAnt
- **Endpoint**: `GET https://api.scrapingant.com/v2/markdown?url=...&x-api-key=...`
- **Auth**: query param `x-api-key=<SCRAPINGANT_API_KEY>`
- **Env var**: `SCRAPINGANT_API_KEY`
- **Returns**: `FetchResult` with markdown content. Title via `extract_markdown_title`.

## Conventions / Invariants

- Implements `FetchProvider`.
- Response: `{ url, markdown }`.
- ScrapingAnt's `/v2/markdown` endpoint is purpose-built for LLM consumption — already cleaned and structured.

## Related

- Registered as `scrapingant` in `../../unified/fetch.ts`.
- Sequential fallback in `../../../server/fetch_orchestrator.ts CONFIG.waterfall`.
