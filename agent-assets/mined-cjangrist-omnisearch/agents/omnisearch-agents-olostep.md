# AGENTS.md — src/providers/fetch/olostep/

## Purpose
Olostep URL fetcher. Includes JS rendering and residential proxy by default. Tier 2 parallel race (with `diffbot`).

## Vendor

- **Vendor**: Olostep
- **Endpoint**: `POST https://api.olostep.com/v1/scrapes`
- **Auth**: `Authorization: Bearer <OLOSTEP_API_KEY>`
- **Env var**: `OLOSTEP_API_KEY`
- **Returns**: `FetchResult` with markdown content. Title via `extract_markdown_title`.

## Conventions / Invariants

- Implements `FetchProvider`.
- Response: `{ result: { markdown_content, html_content, markdown_hosted_url } }`.
- Uses `markdown_content`; falls back to fetching `markdown_hosted_url` if that's how Olostep returns it.

## Related

- Registered as `olostep` in `../../unified/fetch.ts`.
- Tier 2 parallel race in `../../../server/fetch_orchestrator.ts CONFIG.waterfall`.
