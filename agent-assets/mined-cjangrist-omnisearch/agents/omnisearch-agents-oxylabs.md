# AGENTS.md — src/providers/fetch/oxylabs/

## Purpose
Oxylabs Web Scraper API realtime URL fetcher. Sequential fallback tier.

## Vendor

- **Vendor**: Oxylabs
- **Endpoint**: `POST https://realtime.oxylabs.io/v1/queries`
- **Auth**: `Authorization: Basic <base64(username:password)>`
- **Env vars**: BOTH `OXYLABS_WEB_SCRAPER_USERNAME` AND `OXYLABS_WEB_SCRAPER_PASSWORD`
- **Returns**: `FetchResult` with markdown content. Title via `extract_markdown_title`.

## Conventions / Invariants

- Implements `FetchProvider`.
- Body: `{ source: 'universal', url, render: 'html', parse: false }` plus markdown formatting params.
- Response: `{ results: [{ content, status_code }] }` — single-element array; we take element 0.
- **Two env vars required.** Setting only username (or only password) leaves the provider inactive — the registration's `key()` checks `username`.

## Related

- Registered as `oxylabs` in `../../unified/fetch.ts`.
- Sequential fallback in `../../../server/fetch_orchestrator.ts CONFIG.waterfall`.
