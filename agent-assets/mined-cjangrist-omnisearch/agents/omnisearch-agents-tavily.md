# AGENTS.md — src/providers/fetch/tavily/

## Purpose
Tavily Extract URL fetcher. First step in the waterfall (tier 1, solo).

## Vendor

- **Vendor**: Tavily
- **Endpoint**: `POST https://api.tavily.com/extract`
- **Auth**: `Authorization: Bearer <TAVILY_API_KEY>`
- **Env var**: `TAVILY_API_KEY` (shared with `../../search/tavily/` and `../../ai_response/tavily_answer/`)
- **Returns**: `FetchResult` with markdown content. Title is extracted via `extract_markdown_title` if the response includes a header.

## Conventions / Invariants

- Implements `FetchProvider`.
- Tavily's response shape: `{ results: [{ url, raw_content }], failed_results: [{ url, error }] }` — we look at `results[0]`.
- Throws `ProviderError(API_ERROR)` if `results[0]` is missing or empty.

## Related

- Registered as `tavily` in `../../unified/fetch.ts`.
- First step in `../../../server/fetch_orchestrator.ts CONFIG.waterfall`.
