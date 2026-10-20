# AGENTS.md — src/common/

Shared infrastructure used by every other module. Types, HTTP, logging, R2 tracing, ranking, snippet selection, query operators, and small utilities.

## Files

- **`types.ts`** — Core interfaces:
  - `SearchResult { title, url, snippet, score?, source_provider, metadata? }`
  - `BaseSearchParams { query, limit?, include_domains?, exclude_domains?, signal? }`
  - `SearchProvider { search(params), name, description }`
  - `FetchResult { url, title, content, source_provider, metadata? }`
  - `FetchProvider { fetch_url(url), name, description }`
  - `enum ErrorType { API_ERROR, RATE_LIMIT, INVALID_INPUT, PROVIDER_ERROR }`
  - `class ProviderError extends Error { type, message, provider, details? }`
- **`http.ts`** — Streaming HTTP client. Two entry points:
  - `http_json<T>(provider_name, url, options)` — parses JSON, throws `ProviderError(API_ERROR | RATE_LIMIT)` on non-2xx.
  - `http_text(provider_name, url, options)` — returns raw text body.
  - 5MB response size guard (`MAX_RESPONSE_BYTES`).
  - Sensitive query params (`api_key`, `key`, `token`, `app_id`, `x-api-key`, `apikey`) redacted in log output via `sanitize_url`.
  - Records full HTTP round-trip into the active `TraceContext` (request headers, request body, response headers, response body, response_size_bytes, duration_ms).
- **`utils.ts`** —
  - `make_signal(timeout_ms, external?)` — combines an external `AbortSignal` with a per-provider timeout via `AbortSignal.any`, with a manual polyfill for runtimes that don't support it.
  - `timing_safe_equal(a, b)` — `crypto.subtle.timingSafeEqual` wrapper for REST auth.
  - `sanitize_for_log(s)` — strips control chars, truncates to 200 chars.
  - `hash_key(prefix, value)` — async SHA-256 hex digest with prefix; keeps KV keys under 512 bytes.
  - `authenticate_rest_request(request, expected_key)` — Bearer-token auth; returns 401 Response on failure or null on success.
  - `validate_api_key(key, provider)` — throws `ProviderError(API_ERROR)` if missing/empty.
  - `handle_provider_error(error, provider, context)` — converts thrown errors into `ProviderError` with provider context preserved.
  - `retry_with_backoff(fn, options)` — `pRetry` wrapper. Only retries `ProviderError(PROVIDER_ERROR)` (transient); `RATE_LIMIT` and `INVALID_INPUT` never retry.
  - `handle_rate_limit(response)` — reads `Retry-After`, throws `ProviderError(RATE_LIMIT)`.
- **`logger.ts`** — Structured JSON logger with AsyncLocalStorage<request_id> scoping.
  - `loggers.<component>()` factories: `worker`, `config`, `rest`, `http`, `aiResponse`, `fetch`, `search`, `cache`, `auth`.
  - `run_with_request_id(request_id, fn)` — scopes the ID through ALS so every log line emits with `request_id` set, even from deeply nested calls.
  - Level threshold: `info` by default; `globalThis.__LOG_LEVEL` overridable.
- **`r2_trace.ts`** — R2-backed request/response tracing.
  - Two AsyncLocalStorage stores: `trace_store` (TraceContext per request) + `ctx_store` (WaitUntilCapable per request).
  - `run_with_execution_context(ctx, fn)` and `run_with_trace(ctx, fn)` are the public scopers.
  - `WaitUntilCapable = { waitUntil(promise) }` — accepts both Worker `ExecutionContext` and `DurableObjectState`. Both expose `.waitUntil(promise)` on workerd.
  - `TraceContext` records: request_environment, orchestrator decisions, per-provider start/complete/error events, HTTP calls, final result.
  - `flush_background(final_result)` writes a single pretty-formatted JSON file to `request_traces/tool=<tool>/date=YYYY-MM-DD/hour=HH/trace_id=<uuid>.json`. Attached via `ctx.waitUntil` so the write survives the response being sent.
  - `set_trace_r2_bucket(bucket)` is called once per request from `initialize_config(env)`. If the bucket binding is missing, `flush_background` is a silent no-op.
- **`rrf_ranking.ts`** — Reciprocal Rank Fusion + URL dedup + tail rescue + quality filter.
  - `rank_and_merge(provider_results, options)` — main entry. RRF: `score = sum 1/(60 + rank)` per provider that returned the URL.
  - URL dedup uses normalized URL (lowercase host, strip fragment, strip trailing slash).
  - Tail rescue: results from underrepresented domains in the tail are rescued if their per-provider intra-rank is < 2.
  - Quality filter: minimum snippet length and minimum content density. Skipped when the caller passes `skip_quality_filter`.
  - Exports `type SnippetSource = 'aggregated' | 'grounded' | 'fallback'` and an optional `snippet_source` field on `RankedWebResult`. The Groq grounding stage in `server/grounded_snippets.ts` overwrites `snippets[0]` with a query-grounded snippet and tags `snippet_source: 'grounded'`; on failure it tags `'fallback'` and leaves the original aggregated snippet untouched. Untouched ranked results carry no `snippet_source` (treated as `'aggregated'` downstream). Also exports `truncate_web_results(results, top_n)` used by the grounding stage to pick the top-N URLs to ground.
- **`snippet_selector.ts`** — Snippet collapse logic.
  - `collapse_snippets(snippets, query)` — when 2+ providers return the same URL, scores each candidate on bigram density times query-term relevance times log-length.
  - If the runner-up has Jaccard < 0.3 vs. the winner, runs greedy sentence-level set cover within a 500-char budget to produce a merged snippet. Otherwise returns the best single snippet.
  - Near-identical sentences (Jaccard > 0.7) are deduplicated.
- **`search_operators.ts`** — Parses query syntax (`site:`, `-site:`, `filetype:`, `intitle:`, `inurl:`, `inbody:`, `lang:`, `loc:`, `before:`, `after:`, `+term`, `-term`, `"exact"`) into structured params.
  - Used by Brave, Kagi, Tavily; provider-specific renderers in `apply_search_operators` and `build_query_with_operators`.
- **`html.ts`** — `extract_html_title(html)` and `extract_markdown_title(markdown)`. Used by fetch providers that return raw HTML/markdown without a title field.

## Conventions / Invariants

- **No bare `fetch`.** Always go through `http_json` / `http_text` so 5MB guard, status mapping, and trace recording happen automatically.
- **All per-request state goes through ALS stores**, never module-level mutables.
- **`hash_key` is async** — always `await`.
- **`ProviderError` is the only error orchestrators catch**. Other thrown errors propagate to the top-level handler and become 500s.
- **The R2 trace bucket stores unredacted payloads**. Redaction happens only in log output, by design — this is private incident-debugging telemetry.
- **No emojis.** Match the existing source-file tone.

## Gotchas / History

- **`AbortSignal.any` polyfill**: Cloudflare Workers had `AbortSignal.any` for a while, but the polyfill in `make_signal` exists as a safety net for older workerd builds and possible future runtime changes. Don't remove it.
- **Sensitive params constant**: extending `SENSITIVE_PARAMS` in `http.ts` is the right place to redact a new auth field. Don't add it elsewhere.
- **Trace recording uses two ALS stores** (trace_store + ctx_store). Both must be set for tracing to work end-to-end. `worker.ts` sets ctx_store; orchestrators wrap their work in `run_with_trace` to set trace_store.

## Related

- `../AGENTS.md` — src/ overview
- `../server/AGENTS.md` — orchestrator usage of these utilities
- `../config/AGENTS.md` — `set_trace_r2_bucket` is wired here
- `../../README.md` "Concurrency model" + "Tracing — R2" sections for the why
