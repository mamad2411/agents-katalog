# AGENTS.md — src/providers/fetch/firecrawl/

## Purpose
Firecrawl scrape URL fetcher. Tier 1 solo — second waterfall step after Tavily.

## Vendor

- **Vendor**: Firecrawl
- **Endpoint**: `POST https://api.firecrawl.dev/v2/scrape`
- **Auth**: `Authorization: Bearer <FIRECRAWL_API_KEY>`
- **Env var**: `FIRECRAWL_API_KEY` (shared with `../../search/firecrawl/`)
- **Returns**: `FetchResult` with markdown content. Title from `data.metadata.title`.

## Conventions / Invariants

- Implements `FetchProvider`.
- Calls v2 with `onlyMainContent: true` to strip nav/footer/sidebar.
- Throws `ProviderError(API_ERROR)` if `data.markdown` is missing or `success === false`.

## Related

- Registered as `firecrawl` in `../../unified/fetch.ts`.
- Sister module: `../../search/firecrawl/`.
