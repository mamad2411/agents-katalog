# AGENTS.md — src/providers/ai_response/perplexity/

## Purpose
Perplexity Sonar Pro answer adapter. Returns a synthesized answer with citations.

## Vendor

- **Vendor**: Perplexity
- **Endpoint**: `POST https://api.perplexity.ai/chat/completions`
- **Auth**: `Authorization: Bearer <PERPLEXITY_API_KEY>`
- **Env var**: `PERPLEXITY_API_KEY` (shared with `../../search/perplexity/` which uses `sonar`, the cheaper model)
- **Returns**: `[{ source: 'perplexity', answer, citations: [{ title, url }], duration_ms }]` shaped via `SearchResult` (`snippet` carries the answer; rows for citations).
- **Model defaults**: `sonar-pro`, temperature 0.2. No `max_tokens` cap — the full answer is returned untruncated.

## Conventions / Invariants

- Implements `SearchProvider`.
- Maps the API's `citations[]` URL list into `SearchResult` rows alongside the primary answer row.
- Uses `make_signal(config.ai_response.perplexity.timeout, params.signal)` — 295s timeout matched to the global answer fanout deadline.

## Related

- Registered as `perplexity` in `../../unified/ai_search.ts`.
- Sister module: `../../search/perplexity/`.
