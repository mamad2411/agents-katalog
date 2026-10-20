# AGENTS.md — src/providers/ai_response/tavily_answer/

## Purpose
Tavily Answer adapter. Uses Tavily's search endpoint with `include_answer=advanced` to combine search + answer synthesis in one call.

## Vendor

- **Vendor**: Tavily
- **Endpoint**: `POST https://api.tavily.com/search`
- **Auth**: `Authorization: Bearer <TAVILY_API_KEY>`
- **Env var**: `TAVILY_API_KEY` (shared with `../../search/tavily/` and `../../fetch/tavily/`)
- **Returns**: SearchResult rows — primary row is the synthesized `answer` (score 1.0); subsequent rows are the 20 result hits used as context.
- **Defaults**: `search_depth=advanced`, `include_answer=advanced`, `max_results=20`, `chunks_per_source=3`, `topic=general`.

## Conventions / Invariants

- Implements `SearchProvider`.
- Throws `ProviderError(API_ERROR)` if the response does not include an `answer` field — `include_answer=advanced` should always produce one.

## Related

- Registered as `tavily_answer` in `../../unified/ai_search.ts`.
- Sister modules: `../../search/tavily/`, `../../fetch/tavily/`.
