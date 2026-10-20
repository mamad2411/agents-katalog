# AGENTS.md — repo root

You are at the top of `omnisearch` — a Cloudflare-Workers MCP server that aggregates web search, AI answers, and URL fetching across many providers. This file is your map. If you can answer "where do I look for X" from here without grepping, it has done its job.

## Top-level layout

| Path | What's there |
|------|--------------|
| `README.md` | User-facing docs. Update when adding providers, REST endpoints, or env vars. |
| `LICENSE` | MIT. |
| `package.json` | ESM (`"type": "module"`). Deps: `@modelcontextprotocol/sdk ^1.29`, `agents`, `p-retry`, `zod`. Dev: `wrangler`, `typescript ^6.0.3`, `@cloudflare/workers-types`. Scripts: `dev`, `deploy`, `typecheck`. |
| `wrangler.toml` | CF Worker entry (`src/worker.ts`), `nodejs_compat` flag (required for `node:async_hooks`), DO binding `OmnisearchMCP`, KV binding `CACHE`, R2 binding `TRACE_BUCKET`, SQLite-classes migration tag `v1`. |
| `tsconfig.json` | TypeScript 6 config. |
| `config.yaml` | Documentation copy of the fetch waterfall + breakers + failure heuristics. **The runtime mirror is `CONFIG` in `src/server/fetch_orchestrator.ts`**. The TS literal is the source of truth — `config.yaml` is never loaded at startup. The two have drifted; treat `config.yaml` as advisory only. |
| `.env.example` | Documents env vars. Secrets live in Doppler / `wrangler secret`. May lag the actual `src/types/env.ts` — if a binding works at runtime but isn't in `.env.example`, regenerate from `types/env.ts`. |
| `docs/` | Postmortems, ROI analyses, multi-reviewer hydra-heads synthesis docs. See `docs/AGENTS.md`. |
| `src/` | Implementation. See `src/AGENTS.md`. |
| `tools/` | Offline harnesses (Python). Currently: `grounding_smoke.py`, `grounding_compare.py`, `grounding_lib.py` — before/after comparison runs for the grounded-snippets feature against fixed query corpora. Not deployed; run locally for tuning. |
| `tmp/` | Hydra-review sandboxes, ad-hoc test artifacts. **Ignore — do not edit, do not include in releases.** |
| `.wrangler/` | Local wrangler state. Ignore. |
| `trash/` | Per CLAUDE.md rule: `rm` is forbidden, deletions move here. |

## Provider count cheatsheet

The active provider count from `/health` is `search.size + ai_response.size + fetch.size`, populated by `initialize_providers()`. With every key set, the upper bound is **48**:
- **11 search providers**: tavily, brave, kagi, exa, firecrawl, perplexity, serpapi, linkup, you, kimi, parallel (kimi requires both `KIMI_API_KEY` and `SCRAPFLY_API_KEY`; parallel uses `PARALLEL_API_KEY`).
- **9 AI providers in the unified registry**: 5 named (perplexity, kagi_fastgpt, exa_answer, brave_answer, tavily_answer) + 4 LLM-bridge sub-providers (chatgpt, claude, gemini, grok) registered via spread `...llm_reg`.
- **28 fetch providers** (the count is from `unified/fetch.ts PROVIDERS` length).

`gemini-grounded` is NOT in the unified AI registry — it is invoked directly from `answer_orchestrator.ts` via `gemini_grounded_search(query, sources, signal)` after a 10s inline `web_search_fanout`. The `/health` count does not include it.

## Where do I look for X?

**Adding a search provider** → `src/providers/search/<name>/index.ts` for the adapter + one line in `src/providers/unified/web_search.ts`'s `PROVIDERS`. Also wire env in `src/types/env.ts` + `src/config/env.ts`.

**Adding an AI answer provider** → same flow against `src/providers/ai_response/<name>/` + `src/providers/unified/ai_search.ts`. The Gemini-grounded provider is special — it's invoked directly from `answer_orchestrator.ts` rather than through the dispatcher.

**Adding a fetch provider** → `src/providers/fetch/<name>/` + `src/providers/unified/fetch.ts`. If it should run in the auto-waterfall, also slot it into `src/server/fetch_orchestrator.ts CONFIG.waterfall` (and update `config.yaml` to keep documentation in sync). If it's a domain-specialist (YouTube transcripts, social media, GitHub), wire it into `CONFIG.breakers` instead.

**Routing / REST endpoint behavior** → `src/worker.ts` (top-level handler + SSE keepalive), `src/server/rest_*.ts` (one file per endpoint).

**MCP tool registration** → `src/server/tools.ts`. Tools are registered against an `McpServer` provided by the DO. **Each tool closure must capture its own `get_ctx` getter** (R4F01) — see comment block at top of `tools.ts`. Schemas are Zod.

**Orchestrator behavior** —
- search fanout + RRF + cache + tail rescue + grounded-snippets stage → `src/server/web_search_fanout.ts`
- AI answer fanout + 295s deadline + abort + cache + gemini-grounded inline → `src/server/answer_orchestrator.ts`
- fetch waterfall + breakers + multi-winner parallel race + skip_providers + cache → `src/server/fetch_orchestrator.ts`
- grounded snippets (Groq) — top-N URLs fetched + summarized after RRF → `src/server/grounded_snippets.ts` + `src/server/grounded_prompts.ts`. Default ON when `GROQ_API_KEY` is set; opt-out per call with `grounded_snippets:false`.

**Caching** — every orchestrator has a `is_valid_cached_*` validator and binds the request key (`query` or `requested_url`) inside the cached payload as defense-in-depth. See `README.md` "Caching" section.

**Tracing** → `src/common/r2_trace.ts`. `TraceContext` is the data model; `run_with_trace(ctx, fn)` scopes it via AsyncLocalStorage; `flush_background(final_result)` writes to R2 via the request's `ctx.waitUntil`. The R2 bucket is hive-partitioned by tool/date/hour.

**Logging** → `src/common/logger.ts`. `loggers.<component>()` factory + `run_with_request_id(uuid, fn)` scope. Level threshold: `info` by default, `LOG_LEVEL` overridable via `globalThis.__LOG_LEVEL`.

**HTTP requests** → `src/common/http.ts` `http_json` / `http_text`. Always go through these (not bare `fetch`) so the 5MB size guard, status-code → `ProviderError` mapping, and R2 trace recording all happen automatically.

**Error model** → `src/common/types.ts` `ProviderError(type, message, provider, details?)`. Types: `API_ERROR`, `RATE_LIMIT`, `INVALID_INPUT`, `PROVIDER_ERROR`. Only `PROVIDER_ERROR` is retried by `retry_with_backoff` (transient). Rate limit and bad input never retry.

**Search query operators (site:, filetype:, etc.)** → `src/common/search_operators.ts`. Used by Brave, Kagi, Tavily.

**Snippet ranking + collapse** → `src/common/rrf_ranking.ts` (RRF + dedup + tail rescue + quality filter) + `src/common/snippet_selector.ts` (bigram Jaccard + greedy sentence merge).

**AsyncLocalStorage stub** → `src/types/node-async-hooks.d.ts`. Workerd provides AsyncLocalStorage at runtime when `nodejs_compat` is on; we don't ship full `@types/node`.

**Provider initialization** → `src/providers/index.ts` `initialize_providers()`. Atomic-swap pattern — never exposes an empty `active_providers`.

**Cache leak fix** (cross-prompt) — cached payloads now bind the original `query` / `requested_url` and reject mismatches as defense-in-depth. See validators in each orchestrator.

## Common debugging entry points

- **Cache pollution / cross-prompt leaks** → check `is_valid_cached_answer` (`answer_orchestrator.ts`), `is_valid_cached_fanout` (`web_search_fanout.ts`), `is_valid_cached_fetch` (`fetch_orchestrator.ts`).
- **Empty MCP envelope** → `docs/mcp-empty-payload-anomaly.md` (open intermittent issue at high concurrency). Workaround documented there: call serially.
- **Provider count drift** → look at `active_providers` in `src/server/tools.ts` (populated by `initialize_providers`). `/health` endpoint reports the live total.
- **Why is provider X not being called?** Check `key()` returns a non-empty trimmed string in the appropriate `unified/*.ts` `PROVIDERS` array.
- **Trace not showing up in R2** → confirm `TRACE_BUCKET` binding exists in `wrangler.toml` and `set_trace_r2_bucket(env.TRACE_BUCKET)` ran (in `initialize_config`). If `_r2_bucket` is undefined, `flush_background` is a no-op.
- **Skip_providers feature** → `src/server/fetch_orchestrator.ts` `parse_skip_providers` + `validate_skip_providers`. 9-reviewer multi-CLI synthesis lives at `docs/skip_providers_review_synthesis.md`.

## Conventions / Invariants (root-level)

- **No emojis in source code or docs.** Commit messages may use a single leading emoji (see `git log`); files do not.
- **ESM-only** (`"type": "module"`). Imports use `.js` suffix even for `.ts` source — TypeScript convention for ESM.
- **AsyncLocalStorage everywhere**: never module-scope per-request state. Anything that varies per request (request_id, ExecutionContext, TraceContext) lives in an ALS store.
- **`hash_key` is async** — always `await` it.
- **Module-level config singleton** (`src/config/env.ts`) populated by `initialize_config(env)` — must be called before any provider access.
- **Tokens cheap, correctness paramount**: prefer reading the full file over inferring from path names. The codebase has 11-file providers (github), proxy-routed providers (kimi), async-poll providers (supadata) — none of which would be correctly described by their folder name alone.

## Gotchas / History

- **Skip_providers is on `fetch` only.** It does NOT exist on the `answer` or `web_search` tools. Several upstream prompts confused this — the code is the source of truth (`src/server/tools.ts`). (Internally, `grounded_snippets.ts` does pass `skip_providers={attempt-1 winner}` into `run_fetch_race` for its retry path, but that's not exposed as a tool input.)
- **Kimi search is registered but currently disabled** (no key configured). Per `docs/kimi-search-roi-analysis.md`: median query gets zero unique URLs from Kimi, 41% of attempts time-abort, and Scrapfly residential proxy adds ~$0.00875/call. Do NOT delete the provider — keep it dormant for re-enable if the upstream improves. Kimi *fetch* (separate path) is still active.
- **Gemini-grounded is special**: not a regular `SearchProvider` registered through `unified/ai_search.ts`. It's invoked from inside `run_answer_fanout` via `gemini_grounded_search(query, sources, signal)` after pulling sources from a quick (10s timeout) inline web_search_fanout. Its trace links to the inner web_search trace via `parent_trace_id`.
- **Brave has TWO separate keys**: `BRAVE_API_KEY` for web search, `BRAVE_ANSWER_API_KEY` for the SSE answer endpoint. Setting one does not enable the other.
- **The DO is stateful.** Each MCP client session gets its own DO instance. R4F01 (per-closure ctx capture) exists because the `tools.ts` module-level registry is shared across DOs in the same isolate; capturing `() => this.ctx` per registration call keeps each tool callback bound to the DO that registered it.
- **The R2 trace bucket is private and stores unredacted payloads.** Sensitive query params are redacted in *log output* but not in R2 traces — by design, for incident debugging. Do not change without checking with the user.
- **`/researcher` accepts auth as `?api_key=...` query param** for GPT-Researcher compatibility — REST handler converts it to a Bearer header internally before calling the shared `authenticate_rest_request`.
- **`config.yaml` is documentation only** — the runtime fetch waterfall is the `CONFIG` literal in `fetch_orchestrator.ts`. The two have drifted. If you edit one, update the other; better still, treat the TS as canonical and regenerate the YAML.

## Related

- `src/AGENTS.md` — implementation overview
- `docs/AGENTS.md` — what's in `docs/`, when to add new docs
