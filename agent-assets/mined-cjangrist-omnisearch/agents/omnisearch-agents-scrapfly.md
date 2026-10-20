# AGENTS.md — src/providers/fetch/scrapfly/

## Purpose
Scrapfly URL fetcher with anti-bot bypass. Markdown output. Tier 2 parallel race (with `scrapedo`, `decodo`).

## Vendor

- **Vendor**: Scrapfly.io
- **Endpoint**: `GET https://api.scrapfly.io/scrape`
- **Auth**: query param `key=<SCRAPFLY_API_KEY>`
- **Env var**: `SCRAPFLY_API_KEY` (also doubles as the residential proxy for Kimi search/fetch)
- **Returns**: `FetchResult` with markdown. Title via `extract_markdown_title`.

## Conventions / Invariants

- Implements `FetchProvider`.
- Response: `{ result: { content, status_code, url, format } }`.
- Sets `format=markdown` and antibot/proxy params in query string.

## Gotchas

- **Same key powers Kimi**: `SCRAPFLY_API_KEY` is required by both this fetch provider AND the Kimi search/fetch providers (which use Scrapfly's proxy egress to bypass `api.kimi.com`'s ASN block).

## Related

- Registered as `scrapfly` in `../../unified/fetch.ts`.
- Tier 2 parallel race in `../../../server/fetch_orchestrator.ts CONFIG.waterfall`.
- Used as a proxy by `../kimi/index.ts` and `../../search/kimi/scrapfly_proxy.ts`.
