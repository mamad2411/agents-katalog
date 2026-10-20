# AGENTS.md — src/providers/search/parallel/

Parallel.ai search provider — POST `https://api.parallel.ai/v1/search` with `mode:"advanced"` and `advanced_settings.max_results=20` (matching the rest of the fanout). Auth via `x-api-key` header. Joined the fanout after a 10-query head-to-head eval (`tmp/parallel_ai_eval_2026-05-04/VERDICT.md`) showed 46% URL uniqueness vs omnisearch top-15 — genuine net-new recall, especially on multi-hop synthesis and obscure-entity queries.

## Files

| File | Role |
|------|------|
| `index.ts` | `ParallelSearchProvider` — single class implementing `SearchProvider`. Maps `results[].excerpts[]` (markdown excerpts) into a single `snippet` joined by `\n\n`. |

## Conventions / Invariants

- **Auth header is `x-api-key`** (not `Authorization: Bearer`). Documented at `https://docs.parallel.ai/search/search-quickstart`.
- **`max_results` lives under `advanced_settings`**, not top-level — non-obvious gotcha discovered during eval.
- **No `score` field in response** — rely on RRF positional rank like the other providers.
- **Empty `excerpts[]` is valid** — the grounded-snippets stage will rewrite the snippet from the actual page content. We pass through whatever parallel.ai returns.
- **Domain filtering** maps `BaseSearchParams.{include,exclude}_domains` → `advanced_settings.source_policy.{include,exclude}_domains`.

## Gotchas / History

- **Adversarial-query failure mode**: parallel.ai surfaced two SEO-spam domains in top-5 on Q10 of the eval (`claude5.ai`, `claude5.com` confidently fabricating a Claude 5 release). RRF + grounding mitigates this — keep parallel as a peer, not a privileged primary.
- **Ambiguity blind-spot**: 100% uniqueness on Q09 (`mercury`) was a *bug*, not a feature — it skipped Wikipedia/NASA/EPA. The other 10 providers cover this case.
- **Cost**: $0.005/call at `mode:"advanced"` with `max_results:10–20` (in-band with Tavily/Exa). 600 req/min rate ceiling — irrelevant for personal MCP use.

## Related

- `../unified/web_search.ts` — dispatcher (parallel registered alongside the other 10)
- `../../../server/web_search_fanout.ts` — RRF + dedup + grounded snippets
- `../../../../tmp/parallel_ai_eval_2026-05-04/VERDICT.md` — full pre-integration evaluation
