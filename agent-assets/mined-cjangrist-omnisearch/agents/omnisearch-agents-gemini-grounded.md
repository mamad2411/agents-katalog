# AGENTS.md — src/providers/ai_response/gemini_grounded/

## Purpose
Native Gemini API answer with the `url_context` tool — receives a list of grounding sources (URLs + snippets) from `web_search_fanout` and uses them to ground the response. **Not a regular `SearchProvider`** — invoked directly from `../../server/answer_orchestrator.ts`.

## Files

- `index.ts` — `gemini_grounded_search(query, sources, signal)` function + `GroundingSource` type. No class, no `registration` export.

## Vendor

- **Vendor**: Google (Gemini)
- **Endpoint**: `POST https://generativelanguage.googleapis.com/v1beta/.../{model}:generateContent`
- **Auth**: query param `key=<GEMINI_GROUNDED_API_KEY>`
- **Env var**: `GEMINI_GROUNDED_API_KEY` (optional `GEMINI_GROUNDED_MODEL` for model override; default `gemini-3.1-flash-lite-preview`)
- **Returns**: SearchResult rows — primary row carries the Gemini answer; citation rows reference the grounding sources Gemini actually cited.

## Conventions / Invariants

- **Orchestrator-only.** Not registered in `../../unified/ai_search.ts`. The answer orchestrator imports `gemini_grounded_search` directly.
- **Composes a sub-fanout**: `answer_orchestrator.ts` runs an inline 10-second `web_search_fanout(query)` first, takes the top URLs + snippets, and passes them as `GroundingSource[]` to this function.
- **Hard cap**: `MAX_URLS = 20` — Gemini's `url_context` tool rejects more.
- **Blocks unsupported domains** via `BLOCKED_URL_PATTERNS` (`youtube.com`, `youtu.be`, `docs.google.com`, `drive.google.com`) before sending to the API.
- **Records its own trace** with `parent_trace_id` linking to the inner web_search trace.

## Gotchas

- Setting `GEMINI_GROUNDED_API_KEY` is the only step needed to activate. No registration line, no entry in any `PROVIDERS` array.
- If a web search dispatcher is NOT also configured, gemini-grounded is silently skipped (`answer_orchestrator.ts` checks both before adding the task).
- The `gemini-grounded` entry in `/health`'s `providers` count is **not** included — `/health` reports the unified-registry sizes only, and gemini_grounded is orchestrator-only.

## Related

- Imported by `../../server/answer_orchestrator.ts` (line 10): `import { gemini_grounded_search } from '../providers/ai_response/gemini_grounded/index.js';`
- Wiring: `../../config/env.ts` `config.ai_response.gemini_grounded`.
- Reads context from `../../server/web_search_fanout.ts` (the inline 10s fanout).
