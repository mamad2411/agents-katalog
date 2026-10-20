# AGENTS.md — src/providers/search/exa/

## Purpose
Exa neural / semantic search. Embedding-based ranking that often surfaces results keyword search misses.

## Vendor

- **Vendor**: Exa
- **Endpoint**: `POST https://api.exa.ai/search`
- **Auth**: `x-api-key: <EXA_API_KEY>`
- **Env var**: `EXA_API_KEY` (shared with `../../ai_response/exa_answer/`)
- **Returns**: `{ title, url, snippet, source_provider: "exa" }[]` — snippet pulled from `text` content (capped at 1500 chars).
- **Defaults**: `type=auto`, `livecrawl=fallback`, 20 results, `contents.text=true`.

## Conventions / Invariants

- Implements `SearchProvider`.
- Sends `includeDomains` / `excludeDomains` directly (Exa supports them as first-class params, no operator translation needed).
- `MAX_CONTENT_CHARS = 1500` — long content fields are truncated before being returned as `snippet`.

## Related

- Registered as `exa` in `../../unified/web_search.ts`.
- Sister module: `../../ai_response/exa_answer/`.
