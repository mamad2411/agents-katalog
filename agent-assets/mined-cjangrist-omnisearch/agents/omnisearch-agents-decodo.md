# AGENTS.md — src/providers/fetch/decodo/

## Purpose
Decodo (Smartproxy) Web Scraper API URL fetcher. Markdown output. Tier 2 parallel race (with `scrapfly`, `scrapedo`).

## Vendor

- **Vendor**: Decodo (formerly Smartproxy Web Scraper)
- **Endpoint**: `POST https://scraper-api.decodo.com/v2/scrape`
- **Auth**: `Authorization: Basic <DECODO_WEB_SCRAPING_API_KEY>` (the env value is already base64-encoded `username:password` — passed through verbatim)
- **Env var**: `DECODO_WEB_SCRAPING_API_KEY`
- **Returns**: `FetchResult` with markdown content. Title via `extract_markdown_title`.

## Conventions / Invariants

- Implements `FetchProvider`.
- Body sets `output_format: 'markdown'` and a render-spec for JS pages.
- Response: `{ results: [{ content, status_code, task_id }] }` — single-element array.

## Gotchas

- **Env value is pre-encoded.** The user is expected to base64-encode `username:password` themselves and store the result as `DECODO_WEB_SCRAPING_API_KEY`. The provider does NOT re-encode.
- **Longer per-provider timeout**: `config.fetch.decodo.timeout = 60000` (60s) vs. the 30s default for most fetch providers — Decodo's JS rendering can be slow.

## Related

- Registered as `decodo` in `../../unified/fetch.ts`.
- Tier 2 parallel race in `../../../server/fetch_orchestrator.ts CONFIG.waterfall`.
