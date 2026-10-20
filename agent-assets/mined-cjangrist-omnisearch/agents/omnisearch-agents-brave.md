# AGENTS.md — src/providers/search/brave/

## Purpose
Brave Web Search adapter. Privacy-focused; supports the full search-operator vocabulary (site:, -site:, filetype:/ext:, intitle:, inurl:, inbody:, lang:, loc:, before:, after:, +term, -term, "exact").

## Vendor

- **Vendor**: Brave
- **Endpoint**: `GET https://api.search.brave.com/res/v1/web/search?q=...`
- **Auth**: `X-Subscription-Token: <BRAVE_API_KEY>`
- **Env var**: `BRAVE_API_KEY` (DO NOT confuse with `BRAVE_ANSWER_API_KEY`, which powers `../../ai_response/brave_answer/`)
- **Returns**: `{ title, url, snippet, source_provider: "brave" }[]`
- **Default limit**: 20 results.

## Conventions / Invariants

- Implements `SearchProvider`.
- Builds the query through `parse_search_operators` + `apply_search_operators` + `build_query_with_operators` so all operators travel as part of the `q` string (Brave parses them server-side).
- Combines `include_domains` and `exclude_domains` from `BaseSearchParams` with the parsed operators.

## Gotchas

- **Two separate keys**: `BRAVE_API_KEY` for web search; `BRAVE_ANSWER_API_KEY` for the SSE answer endpoint. Setting one does NOT activate the other.

## Related

- Registered as `brave` in `../../unified/web_search.ts`.
- Sister module: `../../ai_response/brave_answer/`.
