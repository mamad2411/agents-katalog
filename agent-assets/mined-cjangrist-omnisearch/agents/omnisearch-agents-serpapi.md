# AGENTS.md — src/providers/fetch/serpapi/

## Purpose
SerpAPI YouTube transcript fetcher. **YouTube-only** — uses SerpAPI's `youtube_video_transcript` engine. NOT a generic page fetcher.

## Vendor

- **Vendor**: SerpAPI
- **Endpoint**: `GET https://serpapi.com/search.json?engine=youtube_video_transcript&v=<video_id>&api_key=...`
- **Auth**: query param `api_key=<SERPAPI_API_KEY>`
- **Env var**: `SERPAPI_API_KEY` (shared with `../../search/serpapi/` which uses the `google_light` engine)
- **Returns**: `FetchResult` — content is concatenated transcript with timestamps; title is the video title.

## Conventions / Invariants

- Implements `FetchProvider`.
- `extract_video_id(url)` parses YouTube URLs (youtube.com/watch?v=, youtu.be/, /embed/, /shorts/, /live/) into the canonical video ID.
- Throws `ProviderError(INVALID_INPUT)` for non-YouTube URLs — falls through to other providers.
- Response shape: `{ transcript: [{ start, end, snippet }], search_metadata: { status }, error? }`.

## Gotchas

- **NOT in the default waterfall.** The YouTube breaker uses `supadata`. SerpAPI's transcript engine is available via explicit `provider: serpapi` in the REST `/fetch` endpoint, or as a future fallback.
- Same key as SerpAPI search — different engine.

## Related

- Registered as `serpapi` in `../../unified/fetch.ts`.
- Sister module: `../../search/serpapi/` (different engine).
