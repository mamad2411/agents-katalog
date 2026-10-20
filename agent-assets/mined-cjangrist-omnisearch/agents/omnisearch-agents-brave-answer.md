# AGENTS.md — src/providers/ai_response/brave_answer/

## Purpose
Brave Answer adapter. Streams the answer via SSE and parses inline citation markers (`<<n>>`) against a structured citations array. The largest answer-provider implementation (~239 lines).

## Vendor

- **Vendor**: Brave
- **Endpoint**: `POST https://api.search.brave.com/res/v1/...` (SSE stream)
- **Auth**: `X-Subscription-Token: <BRAVE_ANSWER_API_KEY>` (NOTE: separate key from `BRAVE_API_KEY` which powers `../../search/brave/`)
- **Env var**: `BRAVE_ANSWER_API_KEY`
- **Returns**: SearchResult rows — primary row is the answer with inline `<<n>>` markers replaced by citation fragments; citation rows are appended.
- **Model**: `brave`. Entities + citations enabled; research mode disabled.

## Conventions / Invariants

- Implements `SearchProvider`.
- **The only ai_response provider that does NOT use `http_json`** — manual SSE parsing of the response stream.
- Citations are scored `CITATION_SCORE_BASE - CITATION_SCORE_DECAY * index` (start 0.9, decay 0.05).
- Inline `<<n>>` markers in the streamed answer are matched against `citations[n]` to embed source links.

## Gotchas

- **Two-key gotcha**: `BRAVE_API_KEY` and `BRAVE_ANSWER_API_KEY` are independent. Setting one does not enable the other.

## Related

- Registered as `brave_answer` in `../../unified/ai_search.ts`.
- Sister module: `../../search/brave/`.
