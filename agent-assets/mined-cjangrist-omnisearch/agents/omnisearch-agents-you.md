# AGENTS.md — src/providers/fetch/you/

## Purpose
You.com Contents URL fetcher. Sequential fallback tier.

## Vendor

- **Vendor**: You.com
- **Endpoint**: `POST https://ydc-index.io/v1/contents`
- **Auth**: `X-API-Key: <YOU_API_KEY>`
- **Env var**: `YOU_API_KEY` (shared with `../../search/you/`)
- **Returns**: `FetchResult` with markdown content. Title from `data[0].title`.

## Conventions / Invariants

- Implements `FetchProvider`.
- Response is `[{ url, title, markdown }]` — array of size 1; we take element 0.
- Throws `ProviderError(API_ERROR)` if the array is empty or `markdown` is null.

## Related

- Registered as `you` in `../../unified/fetch.ts`.
- Sister module: `../../search/you/`.
