# AGENTS.md — src/providers/fetch/leadmagic/

## Purpose
LeadMagic Web2MD URL fetcher. Boilerplate-removed markdown. Sequential fallback tier.

## Vendor

- **Vendor**: LeadMagic
- **Endpoint**: `POST https://api.web2md.app/api/scrape`
- **Auth**: `X-API-Key: <LEADMAGIC_API_KEY>`
- **Env var**: `LEADMAGIC_API_KEY`
- **Returns**: `FetchResult` with markdown. Title from `data.title` or `extract_markdown_title` fallback.

## Conventions / Invariants

- Implements `FetchProvider`.
- Response: `{ markdown, title, url }`.
- Body: `{ url }`.

## Related

- Registered as `leadmagic` in `../../unified/fetch.ts`.
- Sequential fallback in `../../../server/fetch_orchestrator.ts CONFIG.waterfall`.
