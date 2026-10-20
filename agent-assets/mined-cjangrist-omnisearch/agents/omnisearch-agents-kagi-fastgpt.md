# AGENTS.md — src/providers/ai_response/kagi_fastgpt/

## Purpose
Kagi FastGPT answer adapter. Single-string answer plus structured `references[]`. Typically returns in ~900ms — the fastest provider in the answer fanout.

## Vendor

- **Vendor**: Kagi
- **Endpoint**: `POST https://kagi.com/api/v0/fastgpt`
- **Auth**: `Authorization: Bot <KAGI_API_KEY>` (note: `Bot`, not `Bearer`)
- **Env var**: `KAGI_API_KEY` (shared with `../../search/kagi/`)
- **Returns**: `{ data: { output, tokens, references[] } }` mapped to `SearchResult` rows. `output` is the answer; `references` is a list of `{ title, snippet, url }` cited sources.

## Conventions / Invariants

- Implements `SearchProvider`.
- Synchronous request — no streaming.
- Latency target ~900ms; uses 295s outer timeout for safety.

## Related

- Registered as `kagi_fastgpt` in `../../unified/ai_search.ts`.
- Sister module: `../../search/kagi/`.
