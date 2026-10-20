# AGENTS.md — src/providers/ai_response/exa_answer/

## Purpose
Exa Answer adapter. Synthesizes an answer over Exa's neural search index, returning grounded sources alongside the answer.

## Vendor

- **Vendor**: Exa
- **Endpoint**: `POST https://api.exa.ai/answer`
- **Auth**: `x-api-key: <EXA_API_KEY>`
- **Env var**: `EXA_API_KEY` (shared with `../../search/exa/`)
- **Returns**: SearchResult rows — first row is the answer (score 1.0), subsequent rows are sources scored by `0.9 - 0.1 * decay_index`.
- **Defaults**: `type=auto`, `livecrawl=fallback`.

## Conventions / Invariants

- Implements `SearchProvider`.
- Sends `includeDomains` / `excludeDomains` directly (Exa first-class params).
- `useAutoprompt` is forwarded if set in `BaseSearchParams.metadata`.

## Related

- Registered as `exa_answer` in `../../unified/ai_search.ts`.
- Sister module: `../../search/exa/`.
