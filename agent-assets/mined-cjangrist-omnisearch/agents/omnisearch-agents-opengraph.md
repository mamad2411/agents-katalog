# AGENTS.md — src/providers/fetch/opengraph/

## Purpose
OpenGraph.io Extract URL fetcher. Returns structured tag-extracted text. Sequential fallback tier (last resort).

## Vendor

- **Vendor**: OpenGraph.io
- **Endpoint**: `GET https://opengraph.io/api/1.1/extract/{encoded_url}?app_id=<OPENGRAPH_IO_API_KEY>`
- **Auth**: query param `app_id=<key>`
- **Env var**: `OPENGRAPH_IO_API_KEY`
- **Returns**: `FetchResult` with `concatenatedText` as the primary content (joined tag innerText), plus the host's response code.

## Conventions / Invariants

- Implements `FetchProvider`.
- Response shape: `{ tags: [{ tag, innerText, position }], concatenatedText, requestInfo: { host, responseCode } }`.
- The provider returns **structured text** rather than markdown — best for OG metadata extraction, weaker for body content.

## Related

- Registered as `opengraph` in `../../unified/fetch.ts`.
- Last step of the sequential fallback in `../../../server/fetch_orchestrator.ts CONFIG.waterfall`.
