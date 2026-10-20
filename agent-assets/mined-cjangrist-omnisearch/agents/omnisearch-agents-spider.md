# AGENTS.md — src/providers/fetch/spider/

## Purpose
Spider.cloud URL fetcher. Smart-request mode returns markdown. Sequential fallback tier.

## Vendor

- **Vendor**: Spider.cloud
- **Endpoint**: `POST https://api.spider.cloud/scrape`
- **Auth**: `Authorization: Bearer <SPIDER_CLOUD_API_TOKEN>`
- **Env var**: `SPIDER_CLOUD_API_TOKEN` (note: `_API_TOKEN`, not `_API_KEY`)
- **Returns**: `FetchResult` with markdown. Title via `extract_markdown_title`.

## Conventions / Invariants

- Implements `FetchProvider`.
- Response is an **array of page objects** (`SpiderPage[]`); we take element 0.
- Throws on non-200 `status` field inside the page object.

## Related

- Registered as `spider` in `../../unified/fetch.ts`.
- Sequential fallback in `../../../server/fetch_orchestrator.ts CONFIG.waterfall`.
