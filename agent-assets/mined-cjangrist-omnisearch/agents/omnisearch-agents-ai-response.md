# AGENTS.md — src/providers/ai_response/

AI answer providers. Each one accepts a query and returns one or more `SearchResult` rows where the `snippet` field carries the synthesized answer prose and additional rows carry citations. The `answer` MCP tool fans out to all active ones in parallel and returns every provider's answer side-by-side for consensus comparison.

7 leaf folders, but the unified registry has up to 9 dispatch entries — `llm_search/` exports a 4-element registration array (chatgpt, claude, gemini, grok). `gemini_grounded/` is special: it is invoked directly from the answer orchestrator and never reaches the unified dispatcher.

## Subfolders

| Folder | Provider name(s) | Endpoint | Env var | Returns |
|--------|------------------|----------|---------|---------|
| [`perplexity/`](perplexity/AGENTS.md) | `perplexity` | `api.perplexity.ai/chat/completions` (sonar-pro) | `PERPLEXITY_API_KEY` | Sonar Pro answer + `citations[]`. No output token cap. |
| [`kagi_fastgpt/`](kagi_fastgpt/AGENTS.md) | `kagi_fastgpt` | `kagi.com/api/v0/fastgpt` | `KAGI_API_KEY` | Single output string + structured `references[]`. ~900ms typical. Bot auth header. |
| [`exa_answer/`](exa_answer/AGENTS.md) | `exa_answer` | `api.exa.ai/answer` | `EXA_API_KEY` | Synthesized answer + grounded sources. `livecrawl=fallback`, `type=auto`. |
| [`brave_answer/`](brave_answer/AGENTS.md) | `brave_answer` | `api.search.brave.com/res/v1/...` SSE | `BRAVE_ANSWER_API_KEY` | SSE-streamed answer with inline citation tags + structured citations (separate key from `BRAVE_API_KEY`). |
| [`tavily_answer/`](tavily_answer/AGENTS.md) | `tavily_answer` | `api.tavily.com/search` (`include_answer=advanced`) | `TAVILY_API_KEY` | Synthesized `answer` + 20 result rows for context. Shared key with search/fetch. |
| [`llm_search/`](llm_search/AGENTS.md) | `chatgpt`, `claude`, `gemini`, `grok` | `<LLM_SEARCH_BASE_URL>/chat/completions` | `LLM_SEARCH_BASE_URL` + `LLM_SEARCH_API_KEY` | Generic OpenAI-compatible bridge — registers 4 sub-providers sharing the same endpoint with different model strings. Optional `LLM_SEARCH_<NAME>_MODEL` overrides. |
| [`gemini_grounded/`](gemini_grounded/AGENTS.md) | `gemini-grounded` (orchestrator-only) | `generativelanguage.googleapis.com/v1beta/...generateContent` with `url_context` tool | `GEMINI_GROUNDED_API_KEY` | Native Gemini API; receives `web_search_fanout` results as grounding sources. Optional `GEMINI_GROUNDED_MODEL`. |

## Conventions / Invariants

- **All non-special providers implement `SearchProvider`** (the same interface as web search). The `snippet` field carries the answer prose; additional rows carry citations.
- **All non-special providers export `registration = { key: () => config.ai_response.<name>.api_key }`** consumed by `unified/ai_search.ts`.
- **`llm_search` exports `registration` as an array** (not an object). It is spread into `unified/ai_search.ts PROVIDERS` via `...llm_reg`.
- **`gemini_grounded` is the orchestrator-only special case**: no class implementing `SearchProvider`. It exports a `gemini_grounded_search(query, sources, signal)` function, plus a `GroundingSource` type. `answer_orchestrator.ts` calls it directly and treats the result as another fanout task.
- **Long timeouts**: AI answer providers run with 295s timeouts (matched to the global answer fanout deadline). Per-provider config is in `../../config/env.ts`.
- **Throw `ProviderError`** via `handle_provider_error`. Failure isolates to a single fanout entry.

## Gotchas / History

- **`brave_answer` does SSE parsing** — it's the only ai_response provider that does NOT use `http_json`. Inline citation tags `<<n>>` must be parsed out of the streamed text and matched against the citations array.
- **`gemini_grounded` blocks YouTube and Drive URLs** in the grounding sources (`BLOCKED_URL_PATTERNS`) because Gemini's URL context tool can't fetch them.
- **`gemini_grounded` has a 20-URL hard cap** (`MAX_URLS = 20`) imposed by the Gemini API.
- **Perplexity dual-purpose key**: `PERPLEXITY_API_KEY` powers BOTH the search provider in `../search/perplexity/` (sonar) AND this answer provider (sonar-pro). Same key, different models.
- **Exa dual-purpose key**: `EXA_API_KEY` powers both `../search/exa/` and `exa_answer` here.
- **Tavily triple-purpose key**: `TAVILY_API_KEY` powers `../search/tavily/`, `tavily_answer` here, and `../fetch/tavily/`.
- **LLM bridge default models** (in `../../config/env.ts`): chatgpt → `codex/gpt-5.4`, claude → `claude/haiku`, gemini → `gemini/search-fast`, grok → `grok`. Override per-provider via `LLM_SEARCH_<NAME>_MODEL`.
- **Empty-payload anomaly** under high concurrency on the `answer` tool — see `../../docs/mcp-empty-payload-anomaly.md`.

## Related

- `../unified/ai_search.ts` — dispatcher (registers 9 entries; does NOT register gemini_grounded)
- `../../server/answer_orchestrator.ts` — fanout + 295s deadline + AbortController + cache + gemini-grounded inline composition
- `../../server/tools.ts` — registers the `answer` MCP tool, which calls into `run_answer_fanout`
