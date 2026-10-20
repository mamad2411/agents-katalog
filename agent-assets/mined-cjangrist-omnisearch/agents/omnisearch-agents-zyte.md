# AGENTS.md — src/providers/fetch/zyte/

## Purpose
Zyte automatic structured extraction. Tier 3 solo (after parallel proxy group, before Bright Data).

## Vendor

- **Vendor**: Zyte
- **Endpoint**: `POST https://api.zyte.com/v1/extract`
- **Auth**: `Authorization: Basic <base64(SCRAPE_API_KEY:)>` (Basic auth with key as username, empty password)
- **Env var**: `ZYTE_API_KEY`
- **Returns**: `FetchResult`. Title from `pageContent.headline ?? pageContent.title`. Content from `pageContent.itemMain` (Zyte's main-article extractor).

## Conventions / Invariants

- Implements `FetchProvider`.
- Response shape: `{ url, statusCode, pageContent: { headline, title, itemMain, canonicalUrl, metadata } }`.
- Returns canonicalUrl in `FetchResult.metadata` if Zyte normalized it.
- Throws if `pageContent.itemMain` is empty — short responses are not treated as failures here (the orchestrator's 200-char check kicks in instead).

## Related

- Registered as `zyte` in `../../unified/fetch.ts`.
- Tier 3 in `../../../server/fetch_orchestrator.ts CONFIG.waterfall`.
