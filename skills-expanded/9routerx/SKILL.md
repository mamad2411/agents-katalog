---
name: 9routerx
description: Entry point for 9RouterX — local/remote AI gateway with OpenAI-compatible REST for chat, image, TTS, embeddings, web search, web fetch. Use when the user mentions 9RouterX, 9ROUTERX_URL, or wants AI without writing provider boilerplate. This skill covers setup + indexes capability skills; fetch the relevant capability SKILL.md from the URLs below when needed.
---

# 9RouterX

Local/remote AI gateway exposing OpenAI-compatible REST. One key, many providers, auto-fallback.

## Setup

```bash
export 9ROUTERX_URL="http://localhost:20128"      # or VPS / tunnel URL
export 9ROUTERX_KEY="sk-..."                      # from Dashboard → Keys (only if requireApiKey=true)
```

All requests: `${9ROUTERX_URL}/v1/...` with header `Authorization: Bearer ${9ROUTERX_KEY}` (omit if auth disabled).

Verify: `curl $9ROUTERX_URL/api/health` → `{"ok":true}`

## Discover models

```bash
curl $9ROUTERX_URL/v1/models                  # chat/LLM (default)
curl $9ROUTERX_URL/v1/models/image            # image-gen
curl $9ROUTERX_URL/v1/models/tts              # text-to-speech
curl $9ROUTERX_URL/v1/models/embedding        # embeddings
curl $9ROUTERX_URL/v1/models/web              # web search + fetch (entries have `kind` field)
curl $9ROUTERX_URL/v1/models/stt              # speech-to-text
curl $9ROUTERX_URL/v1/models/image-to-text    # vision
```

Use `data[].id` as `model` field in requests. Combos appear with `owned_by:"combo"`.

Response shape:
```json
{ "object": "list", "data": [
  { "id": "openai/gpt-5", "object": "model", "owned_by": "openai", "created": 1735000000 },
  { "id": "tavily/search", "object": "model", "kind": "webSearch", "owned_by": "tavily", "created": 1735000000 }
]}
```

## Capability skills

When the user needs a specific capability, fetch that skill's `SKILL.md` from its raw URL:

| Capability | Raw URL |
|---|---|
| Chat / code-gen | https://raw.githubusercontent.com/yanstd888/9routerx/refs/heads/main/skills/9routerx-chat/SKILL.md |
| Image generation | https://raw.githubusercontent.com/yanstd888/9routerx/refs/heads/main/skills/9routerx-image/SKILL.md |
| Text-to-speech | https://raw.githubusercontent.com/yanstd888/9routerx/refs/heads/main/skills/9routerx-tts/SKILL.md |
| Speech-to-text | https://raw.githubusercontent.com/yanstd888/9routerx/refs/heads/main/skills/9routerx-stt/SKILL.md |
| Embeddings | https://raw.githubusercontent.com/yanstd888/9routerx/refs/heads/main/skills/9routerx-embeddings/SKILL.md |
| Web search | https://raw.githubusercontent.com/yanstd888/9routerx/refs/heads/main/skills/9routerx-web-search/SKILL.md |
| Web fetch (URL → markdown) | https://raw.githubusercontent.com/yanstd888/9routerx/refs/heads/main/skills/9routerx-web-fetch/SKILL.md |

## Errors

- 401 → set/refresh `9ROUTERX_KEY` (Dashboard → Keys)
- 400 `Invalid model format` → check `model` exists in `/v1/models/<kind>`
- 503 `All accounts unavailable` → wait `retry-after` or add another provider account
