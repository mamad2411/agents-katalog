# AGENTS.md — src/types/

TypeScript type definitions specific to the Worker runtime. Two files only.

## Files

- **`env.ts`** — `interface Env` with all Cloudflare Worker bindings. Used by:
  - `worker.ts` `ExportedHandler<Env>` and `class OmnisearchMCP extends McpAgent<Env>`.
  - `config/env.ts` `initialize_config(env: Env)`.
  Members:
  - **Search keys**: `TAVILY_API_KEY`, `BRAVE_API_KEY`, `KAGI_API_KEY`, `EXA_API_KEY`, `SERPAPI_API_KEY`, `LINKUP_API_KEY`.
  - **AI answer keys**: `PERPLEXITY_API_KEY`, `BRAVE_ANSWER_API_KEY`, `GEMINI_GROUNDED_API_KEY`, `GEMINI_GROUNDED_MODEL`, `LLM_SEARCH_BASE_URL`, `LLM_SEARCH_API_KEY`, `LLM_SEARCH_CHATGPT_MODEL`, `LLM_SEARCH_CLAUDE_MODEL`, `LLM_SEARCH_GEMINI_MODEL`, `LLM_SEARCH_GROK_MODEL`.
  - **Snippet-grounding key**: `GROQ_API_KEY` — when set, `web_search` / `POST /search` regenerate top-N snippets via Groq from actual page content (see `src/server/grounded_snippets.ts`). Default ON when present; opt-out via per-call `grounded_snippets:false`.
  - **Shared keys**: `FIRECRAWL_API_KEY`, `YOU_API_KEY`.
  - **Fetch-only keys**: `JINA_API_KEY`, `BRIGHT_DATA_API_KEY` (+ `BRIGHT_DATA_ZONE`), `DIFFBOT_TOKEN`, `SOCIAVAULT_API_KEY`, `SPIDER_CLOUD_API_TOKEN`, `SCRAPFLY_API_KEY`, `SCRAPEGRAPHAI_API_KEY`, `SCRAPE_DO_API_TOKEN`, `SCRAPELESS_API_KEY`, `OPENGRAPH_IO_API_KEY`, `SCRAPINGBEE_API_KEY`, `SCRAPERAPI_API_KEY`, `ZYTE_API_KEY`, `SCRAPINGANT_API_KEY`, `OXYLABS_WEB_SCRAPER_USERNAME`, `OXYLABS_WEB_SCRAPER_PASSWORD`, `OLOSTEP_API_KEY`, `DECODO_WEB_SCRAPING_API_KEY`, `SCRAPPEY_API_KEY`, `LEADMAGIC_API_KEY`, `CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_EMAIL`, `CLOUDFLARE_API_KEY`, `SUPADATA_API_KEY`, `GITHUB_API_KEY`, `KIMI_API_KEY`.
  - **REST auth**: `OPENWEBUI_API_KEY`, `OMNISEARCH_API_KEY`.
  - **CF resources**: `CACHE: KVNamespace`, `TRACE_BUCKET: R2Bucket`, `OmnisearchMCP: DurableObjectNamespace`.
- **`node-async-hooks.d.ts`** — Minimal type stub for `node:async_hooks AsyncLocalStorage`. Workerd provides AsyncLocalStorage at runtime when `nodejs_compat` is enabled in `wrangler.toml`. We don't ship full `@types/node` — the stub declares only `AsyncLocalStorage<T>` with `getStore()` and `run(store, fn)`, which is what we use.

## Conventions / Invariants

- **Adding a new env binding**: add it here AND in `../config/env.ts initialize_config(env)` AND in `.env.example` (documentation). Three changes per new env var; the registry pattern handles the rest.
- **Comment about KV TTL**: line near the `CACHE` binding declaration comments `(24h TTL)` — this is stale; actual TTL is 36h (`KV_*_TTL_SECONDS = 129_600` in all three orchestrators). Worth fixing in a follow-up but not load-bearing.

## Gotchas / History

- **`KIMI_API_KEY` only enables Kimi if `SCRAPFLY_API_KEY` is also set** — the Kimi search adapter routes through Scrapfly residential proxy because `api.kimi.com` blocks Cloudflare-Workers ASN egress. The dependency is enforced at the registration / config layer, not in the env type.
- **`OXYLABS` is two env vars** (username + password) and `CLOUDFLARE_BROWSER` is three (account_id + email + api_key). Both providers' validators check all required fields.
- **Optional fields**: every key field is typed `string | undefined`. `validate_api_key()` (from `common/utils.ts`) throws `ProviderError(API_ERROR)` if missing — providers don't need to do their own null-check.

## Related

- `../config/env.ts` — wires these into `config`
- `../worker.ts` — uses `Env` as the type parameter for the Worker handler and the DO class
- `../common/r2_trace.ts` — `WaitUntilCapable` is the structural type used to scope CF `ExecutionContext` and DO `DurableObjectState` together
