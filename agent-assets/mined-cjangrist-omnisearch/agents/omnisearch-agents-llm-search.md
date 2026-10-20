# AGENTS.md — src/providers/ai_response/llm_search/

## Purpose
Generic OpenAI-compatible chat-completions bridge. **Registers 4 sub-providers** sharing the same endpoint with different model strings: `chatgpt`, `claude`, `gemini`, `grok`. Lets a single base-URL + API-key pair fan out to multiple LLM vendors via an OpenAI-API-compatible gateway.

## Files

- `index.ts` — `create_llm_provider(name, description, result_url, get_config)` factory + four exported provider factories (`ChatGPTProvider`, `ClaudeProvider`, `GeminiProvider`, `GrokProvider`) + the `registration` array.

## Vendor

- **Vendor**: configurable via env (any OpenAI-compatible chat completions endpoint)
- **Endpoint**: `POST <LLM_SEARCH_BASE_URL>/chat/completions`
- **Auth**: `Authorization: Bearer <LLM_SEARCH_API_KEY>`
- **Env vars**:
  - `LLM_SEARCH_BASE_URL` and `LLM_SEARCH_API_KEY` are shared by all four sub-providers.
  - Optional model overrides: `LLM_SEARCH_CHATGPT_MODEL`, `LLM_SEARCH_CLAUDE_MODEL`, `LLM_SEARCH_GEMINI_MODEL`, `LLM_SEARCH_GROK_MODEL`.
- **Default model strings** (in `../../config/env.ts`):
  - `chatgpt` -> `codex/gpt-5.4`
  - `claude` -> `claude/haiku`
  - `gemini` -> `gemini/search-fast`
  - `grok` -> `grok`
- **Returns**: a single SearchResult per call — title `{name} ({model})`, snippet is the assistant's `content`, score 1.0.

## Conventions / Invariants

- The exported `registration` is an **array** (4 entries) — `unified/ai_search.ts` uses `...llm_reg` to spread it into `PROVIDERS`.
- Each sub-provider's `key()` checks both `base_url` AND `api_key` are set — without both, the bridge is silently inactive.
- Body is `{ model, messages: [{ role: 'user', content: query }] }` — the query is sent verbatim as the user message; no system prompt or function calling.
- `result_url` is a vendor home page (`https://chatgpt.com`, etc.) used as the placeholder URL for the citation row.

## Gotchas

- **All four share one key + URL.** If you set `LLM_SEARCH_BASE_URL` and `LLM_SEARCH_API_KEY`, all four sub-providers activate together. There is no way to enable just one — pick the right gateway for your needs.
- **Not the Kimi scraping providers**: the `grok` entry here is xAI's Grok answer model reached through the shared LLM bridge (`LLM_SEARCH_API_KEY`). It is unrelated to the separate Kimi search/fetch scraping providers in `../../search/kimi/` and `../../fetch/kimi/`, which use `KIMI_API_KEY`.

## Related

- Registered (4 entries via spread) in `../../unified/ai_search.ts`.
- `../../config/env.ts` — defines the four config blocks (`config.ai_response.{chatgpt,claude,gemini,grok}`).
