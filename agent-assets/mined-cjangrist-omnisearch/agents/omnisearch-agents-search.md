# AGENTS.md — src/providers/search/

11 web-search providers. Each one takes a query and returns a ranked `SearchResult[]`. The unified dispatcher (`../unified/web_search.ts`) fans out to all active ones in parallel; results are deduplicated by URL and ranked with Reciprocal Rank Fusion in `../../server/web_search_fanout.ts`.

## Subfolders

| Provider | Endpoint | Env var | Notes |
|----------|----------|---------|-------|
| [`tavily/`](tavily/AGENTS.md) | `https://api.tavily.com/search` | `TAVILY_API_KEY` | Academic/research bias; topic + depth params; key shared with `tavily_answer` and `tavily` fetch. |
| [`brave/`](brave/AGENTS.md) | `https://api.search.brave.com/res/v1/web/search` | `BRAVE_API_KEY` | Privacy-respecting; supports site:/filetype:/intitle: operators via shared parser. SEPARATE key from `BRAVE_ANSWER_API_KEY`. |
| [`kagi/`](kagi/AGENTS.md) | `https://kagi.com/api/v0/search` | `KAGI_API_KEY` | High-signal curated index; key shared with `kagi_fastgpt`. Bot-style auth header. |
| [`exa/`](exa/AGENTS.md) | `https://api.exa.ai/search` | `EXA_API_KEY` | Neural / semantic search; livecrawl=fallback; supports inline snippet contents. Key shared with `exa_answer`. |
| [`firecrawl/`](firecrawl/AGENTS.md) | `https://api.firecrawl.dev/v2/search` | `FIRECRAWL_API_KEY` | Web search results with descriptions; key shared with `firecrawl` fetch. |
| [`perplexity/`](perplexity/AGENTS.md) | `https://api.perplexity.ai/chat/completions` (sonar) | `PERPLEXITY_API_KEY` | Returns `search_results` from the model response, falling back to citation URLs; key shared with `perplexity` answer. |
| [`serpapi/`](serpapi/AGENTS.md) | `https://serpapi.com/search.json` (engine `google_light`) | `SERPAPI_API_KEY` | Google organic results; same key powers SerpAPI's YouTube transcript fetch. |
| [`linkup/`](linkup/AGENTS.md) | `https://api.linkup.so/v1/search` | `LINKUP_API_KEY` | Standard depth, text outputs; key shared with `linkup` fetch. |
| [`you/`](you/AGENTS.md) | `https://ydc-index.io/v1/search` | `YOU_API_KEY` | LLM-oriented snippets; key shared with `you` fetch. |
| [`kimi/`](kimi/AGENTS.md) | `https://api.kimi.com/coding/v1/search` (proxied) | `KIMI_API_KEY` + `SCRAPFLY_API_KEY` | Moonshot AI's coding-API search. Routed via Scrapfly residential proxy because api.kimi.com blocks Cloudflare-Workers ASN. **Currently disabled in production** per `docs/kimi-search-roi-analysis.md`. |
| [`parallel/`](parallel/AGENTS.md) | `https://api.parallel.ai/v1/search` (mode:"advanced") | `PARALLEL_API_KEY` | Owns its own crawler/index — 46% URL uniqueness vs omnisearch top-15 in pre-integration eval. `x-api-key` auth; `max_results` under `advanced_settings`. |

## Conventions / Invariants

- **All providers implement `SearchProvider` from `../../common/types.ts`** — a single `search(params: BaseSearchParams)` method.
- **All providers export a `registration = { key: () => config.search.<name>.api_key }`** object. The unified dispatcher imports it and uses `key()?.trim()` to gate activation.
- **Validate the API key first**: `validate_api_key(config.search.<name>.api_key, this.name)` throws if missing.
- **Use `make_signal(timeout, params.signal)`**: combines per-provider timeout with the orchestrator's external abort signal.
- **Return `SearchResult { title, url, snippet, source_provider, score?, metadata? }`** — `score` is provider-native and may be undefined; RRF in the orchestrator does its own ranking.
- **Throw `ProviderError`** via `handle_provider_error(error, this.name, "fetch search results")`. Never let raw errors escape.
- **Search operators**: providers that can express them (Brave, Kagi, Tavily) use `apply_search_operators` + `build_query_with_operators` from `../../common/search_operators.ts`. Providers that can't (Exa, Perplexity, You.com) translate the parsed operators into native filter params instead.

## Gotchas / History

- **Kimi search is multi-file** — `index.ts`, `headers.ts` (browser-identity headers Kimi CLI sends), `scrapfly_proxy.ts` (proxy POST helper). Don't collapse.
- **Kimi requires BOTH keys** — `KIMI_API_KEY` for Kimi auth, `SCRAPFLY_API_KEY` for the residential-proxy egress. Setting just one means it's silently inactive.
- **Tavily's `topic`/`depth` params are read from `BaseSearchParams.metadata`** if present — provider-specific extension.
- **Brave's web/answer split**: `BRAVE_API_KEY` is for `/web/search`. The Answer endpoint at `/res/v1/answer-search` uses a separate token (`BRAVE_ANSWER_API_KEY`). Setting `BRAVE_API_KEY` does NOT enable Brave answer.
- **SerpAPI uses `google_light` engine**, not `google` — lighter response, faster, cheaper. Same key separately powers a YouTube transcript fetch in `../fetch/serpapi/`.
- **Perplexity's two layers**: the search provider here uses `sonar`. The answer provider in `../ai_response/perplexity/` uses `sonar-pro`. Same key, different model.

## Related

- `../unified/web_search.ts` — dispatcher
- `../../server/web_search_fanout.ts` — parallel fanout + RRF + cache
- `../../common/search_operators.ts` — query syntax parser
- `../../common/types.ts` — `SearchProvider`, `SearchResult`, `BaseSearchParams`, `ProviderError`
