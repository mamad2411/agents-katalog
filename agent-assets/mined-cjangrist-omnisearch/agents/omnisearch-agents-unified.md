# AGENTS.md — src/providers/unified/

Three dispatchers — `web_search`, `ai_search`, `fetch` — that abstract the registry of leaf providers behind a single class per category. Auto-built from each leaf module's `registration` export.

## Files

- **`web_search.ts`** — `UnifiedWebSearchProvider`. `PROVIDERS` array imports every leaf in `../search/` (10 entries: `tavily`, `brave`, `kagi`, `exa`, `firecrawl`, `perplexity`, `serpapi`, `linkup`, `you`, `kimi`). Constructor filters by `key()?.trim()` and instantiates only the active ones. `search({ provider, ...params })` dispatches by name, throwing `INVALID_INPUT` on unknown.
- **`ai_search.ts`** — `UnifiedAISearchProvider`. `PROVIDERS` includes the 5 named providers (`perplexity`, `kagi_fastgpt`, `exa_answer`, `brave_answer`, `tavily_answer`) plus `...llm_reg` — the spread expands into 4 sub-providers (`chatgpt`, `claude`, `gemini`, `grok`) all sharing `LLM_SEARCH_BASE_URL` + `LLM_SEARCH_API_KEY`. Total: 9 dispatch entries when all keys set. **Does NOT include `gemini-grounded`** — that one is invoked directly from `answer_orchestrator.ts`.
- **`fetch.ts`** — `UnifiedFetchProvider`. `PROVIDERS` array has 28 entries — the largest of the three. Constructor filters by `key()?.trim()`. `fetch_url(url, provider)` requires a provider name explicitly (no fallback). Used by `fetch_orchestrator.ts` to call individual providers per waterfall step.

## How a leaf provider gets registered

Each unified file has a clearly-marked `// ─── ADD ONE LINE HERE TO REGISTER A NEW PROVIDER ─` block. To add `foo`:

```ts
import { FooSearchProvider, registration as foo_reg } from '../search/foo/index.js';

const PROVIDERS = [
  // ...
  { name: 'foo', ...foo_reg, factory: () => new FooSearchProvider() },
] as const;
```

That's it. `get_active_search_providers()` and `has_any_search_provider()` automatically include `foo` if its `key()` returns a non-empty trimmed string.

## Conventions / Invariants

- **`PROVIDERS` is `as const`** so `WebSearchProvider`, `AISearchProvider`, `FetchProviderName` are derived as union literal types. New providers automatically appear in the type.
- **Constructor builds the active map**: `new Map(PROVIDERS.filter(p => p.key()?.trim()).map(p => [p.name, p.factory()]))`. Adding a key at runtime would not retroactively activate the provider — `initialize_config` + `initialize_providers` is the way to refresh.
- **`get_active_*_providers()`** returns `Array<{ name, key }>` — used by `/health` and the answer/fetch orchestrators to enumerate the active set.
- **`has_any_*_provider()`** returns boolean — used by `register_tools` to decide whether to register the corresponding MCP tool at all.
- **Dispatch errors throw `ProviderError(INVALID_INPUT)`** with a list of valid names — the REST/MCP layer surfaces these as 400-equivalent.

## Gotchas / History

- **The `llm_reg` spread is the only spread in any unified file.** It's the mechanism that lets a single `LLM_SEARCH_BASE_URL` + `LLM_SEARCH_API_KEY` produce 4 distinct provider entries. Don't collapse this into a single `llm_search` entry — the answer fanout treats them as 4 independent providers for consensus comparison.
- **`gemini-grounded` is conspicuously absent** from `ai_search.ts PROVIDERS`. It composes `web_search_fanout` + Gemini, which doesn't match the shape of a regular `SearchProvider`. `answer_orchestrator.ts` imports `gemini_grounded_search` directly and adds it as an extra task when `GEMINI_GROUNDED_API_KEY` AND a web search dispatcher both exist.
- **`UnifiedFetchProvider.fetch_url` requires a provider parameter** — the orchestrator selects the provider based on waterfall step + breaker config; bare callers must pass one.
- **Active map is built at construction time.** If `initialize_config` runs again (e.g., after a memoized init failure resets), `initialize_providers` will rebuild a new `UnifiedFetchProvider` instance with the current active set.

## Related

- `../<category>/<name>/index.ts` — each leaf exports a class + a `registration` object/array
- `../index.ts` — `initialize_providers()` constructs these and hands them to `ToolRegistry`
- `../../server/web_search_fanout.ts`, `../../server/answer_orchestrator.ts`, `../../server/fetch_orchestrator.ts` — consume the unified dispatchers
