# AGENTS.md — src/providers/fetch/jina/

## Purpose
Jina Reader URL fetcher. Token-efficient markdown extraction. Sequential fallback tier (tier 4).

## Vendor

- **Vendor**: Jina
- **Endpoint**: `POST https://r.jina.ai/` (the URL is sent in the request body)
- **Auth**: `Authorization: Bearer <JINA_API_KEY>`
- **Env var**: `JINA_API_KEY`
- **Returns**: `FetchResult` with markdown content. Title from `data.title`.

## Conventions / Invariants

- Implements `FetchProvider`.
- Jina's response: `{ code: 200, data: { title, url, content, usage: { tokens } } }`.
- Token usage is propagated to `FetchResult.metadata.tokens` for cost analysis.

## Related

- Registered as `jina` in `../../unified/fetch.ts`.
- First step of the sequential fallback in `../../../server/fetch_orchestrator.ts CONFIG.waterfall`.
