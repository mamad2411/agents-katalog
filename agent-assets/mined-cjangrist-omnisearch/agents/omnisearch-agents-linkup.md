# AGENTS.md — src/providers/fetch/linkup/

## Purpose
Linkup Content Fetch URL fetcher. Clean markdown extraction. Tier 2 parallel race (with `cloudflare_browser`).

## Vendor

- **Vendor**: Linkup
- **Endpoint**: `POST https://api.linkup.so/v1/fetch`
- **Auth**: `Authorization: Bearer <LINKUP_API_KEY>`
- **Env var**: `LINKUP_API_KEY` (shared with `../../search/linkup/`)
- **Returns**: `FetchResult` with markdown. Title via `extract_markdown_title`.

## Conventions / Invariants

- Implements `FetchProvider`.
- Response: `{ markdown }`.

## Related

- Registered as `linkup` in `../../unified/fetch.ts`.
- Sister module: `../../search/linkup/`.
- Tier 2 parallel race in `../../../server/fetch_orchestrator.ts CONFIG.waterfall`.
