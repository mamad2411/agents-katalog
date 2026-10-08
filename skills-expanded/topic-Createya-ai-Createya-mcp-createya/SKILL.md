---
name: createya
description: Createya MCP integration — run AI image and video generation models through a single MCP endpoint at api.createya.ai/mcp. Direct access without VPN, ruble billing, free credits on signup. Use when user asks to generate image or video via Createya, says "сгенерируй / сгенерь через Createya", "Создаю", references Createya API/MCP, or wants AI image/video generation through a single key with Russian-friendly billing.
---

# Createya MCP skill

Createya is an AI-platform that aggregates 20+ image and video generation model families under a single API key + single MCP endpoint. Direct access without VPN, billing in rubles. Free credits on signup.

> Currently supported via MCP/REST: **image** and **video**. Audio and text models are on the roadmap.

## When to trigger this skill

- User says "сгенерируй / создай / сгенерь картинку или видео через Createya"
- User wants AI image/video without VPN, with ruble billing
- User mentions `createya.ai`, `crya_sk_`, or `https://api.createya.ai/mcp`
- User asks for a specific model family that's on Createya's roster (see live catalog below — never guess slugs)

## How to use — golden rule

**Always call `createya:list_models` first.** Do not assume slugs from memory or from this file. The live catalog reflects what's actually available right now (new models added daily, some removed, prices change). This file's examples are illustrative only — agents that hardcode slugs from memory get 404 model_not_found.

### 1. Check connection

If `createya:list_models` tool is available — proceed. If not, point user to setup:

```bash
# One-line install (Claude Code, Cursor, Codex, opencode all supported)
curl -fsSL https://raw.githubusercontent.com/Createya-ai/createya-mcp/main/install.sh \
  | bash -s -- crya_sk_YOUR_KEY
```

Get the key at [createya.ai/settings/api-keys](https://createya.ai/settings/api-keys) (free credits on signup).

### 2. List families and pick one

```
createya:list_models()
```

Returns a `data: [...]` array of **families**, each with:

```json
{
  "id": "nano-banana-pro",          // ← pass this to run_model
  "object": "model_family",
  "name": "Nano Banana",            // brand
  "version": "Pro",                 // variant
  "output_type": "image",           // image | video | audio | text
  "status": "public" | "test",
  "credits_range": { "min": 18, "max": 152 },
  "endpoints": [
    {
      "id": "nano-banana-pro-t2i",
      "mode": "text-to-image",
      "credits_per_request": 18,    // typical (at defaults)
      "credits_min": 36,
      "credits_max": 152,
      "pricing": {
        "axes": [...],
        "human_description": "resolution: 1K=18кр, 2K=18кр, 4K=36кр; × num_images (1–4)"
      },
      "parameters_schema": [...],
      "media_inputs": [...]
    }
  ]
}
```

**Read `credits_range` to estimate cost** before running. `credits_per_request` is the cost at schema defaults, `credits_min` / `credits_max` are the actual range across all axis combinations.

**Read `parameters_schema[*].constraints`** for typed cross-axis rules (e.g. "при 4K только 16:9/9:16/4:3/3:4 — не 1:1"). Don't violate them — server will reject or downgrade.

### 3. Run a model with family slug

```
createya:run_model({
  model: "nano-banana-pro",   // family slug — server picks endpoint by input
  input: {
    prompt: "кот на луне в стиле Studio Ghibli",
    aspect_ratio: "16:9"
  }
})
```

**Family routing** — when you pass family slug, server scores endpoints by input shape:

| Input contains | Picks |
|---|---|
| `start_image_url` + `end_image_url` | `first-last-frame` |
| `video_url` / `input_video` | `video-to-*` |
| `image_url` / `input_images[]` | `image-to-*` or `-edit` |
| Just `prompt` | `text-to-*` |

If you want a **specific** endpoint, pass its full slug (e.g. `nano-banana-pro-i2i`) — it bypasses scoring.

### 4. Check balance with `get_balance`

```
createya:get_balance() → { object: "balance", credits_balance: 21134 }
```

Warn the user before expensive runs (`credits_max` close to balance). Link to [createya.ai](https://createya.ai) for top-up.

### 5. Always show the result URL

After `run_model` completes (sync) or `get_run_status` returns `completed`:
- Output at `output.urls[0]` (or `output.url` for single-output models)
- URL is a public CDN link — embed as markdown image/video preview if possible

## Categories — what families to pick by use case

Don't hardcode slugs from this list — always consult `list_models` for current names. Use these categories to filter:

| User goal | Look for `output_type` + filter by name |
|---|---|
| Универсальная картинка | `image` — наиболее «универсальные» (нет узкоспециализированных модификаторов): обычно `nano-banana-*`, `gpt-image-*`, `flux-*` |
| Фотореализм / лица | `image` — Flux-семейство, Kling Image, Higgsfield Soul |
| Cinematic / артистично | `image` — Midjourney, Higgsfield Soul, Recraft |
| Свежие модели xAI / Google | `image`/`video` — Grok-Imagine, Imagen, Veo |
| Видео OpenAI | `video` — Sora |
| Видео Google | `video` — Veo (несколько версий — выбирай по `version` и `credits_range`) |
| Видео Kling | `video` — Kling-Video (несколько версий) |
| Видео ByteDance | `video` — Seedance (несколько версий) |
| Bytedance image | `image` — Seedream |

Always verify exact family slug via `list_models` — the catalog evolves.

## Pricing transparency

Createya's API returns `credits_per_request` (typical), `credits_min`, `credits_max` per endpoint, plus `pricing.axes` with per-option breakdown. Use these:

- **Quick check**: `credits_per_request` tells you the cost at defaults
- **Budget worry**: `credits_max` is the worst case (high quality + max size + max num_images)
- **Cheap option**: `credits_min` is the cheapest combo — tell user "set quality=low and size=square_hd for ~X credits"
- **Detailed picker**: `pricing.human_description` reads like "resolution: 1K=4кр, 2K=7кр, 4K=11кр; × num_images" — surface this when user asks "сколько стоит?"

## Common issues

| Error code | Meaning | Action |
|---|---|---|
| 401 Unauthorized | Invalid key or expired | Re-create at `/settings/api-keys`, key must start with `crya_sk_` |
| 402 Insufficient credits | Out of credits | Direct user to [createya.ai](https://createya.ai) for top-up |
| 404 Model not found | Slug typo or model unpublished | **Re-call `list_models`** — agent must not assume slugs from memory |
| 422 Invalid input | Schema mismatch | Re-check `parameters_schema` and `parameters_schema[*].constraints` |
| 429 Rate limit | Concurrency cap | Wait or upgrade plan |
| Async stuck | Job timed out | `get_run_status` shows error; retry the run |

## Important conventions agent should know

- **Family slug** (e.g. `nano-banana-pro`) ≠ **endpoint slug** (e.g. `nano-banana-pro-i2i`). Family slug works in `run_model` and gets auto-routed. Endpoint slug works too — explicit.
- **Media URLs only** — base64 inline media not accepted in MCP. If user has a local file, use `createya:request_upload_url` for presigned PUT, or REST `POST /v1/uploads` (multipart). Then pass the returned CDN URL as `image_url` / `video_url`.
- **Hidden params** — params with `isHidden: true` are filtered out of MCP response. Don't try to pass them.
- **Constraints** — read `parameters_schema[*].constraints` (cross-axis rules). E.g. "For 4K, aspect_ratio must be in [16:9, 9:16, 4:3, 3:4]" — violating these triggers fallback or rejection.
- **Don't mention upstream providers** — Createya intentionally hides which API provider routes each model. Users care about the model name (Nano Banana, GPT Image 2), not the proxy. The API response itself contains no provider mentions; agent should follow suit.

## Docs

- Site: [createya.ai](https://createya.ai)
- Knowledge base: [createya.ai/knowledge](https://createya.ai/knowledge)
- API docs: [createya.ai/api](https://createya.ai/api)
- This repo: [github.com/Createya-ai/createya-mcp](https://github.com/Createya-ai/createya-mcp)
- Support: [support@createya.ai](mailto:support@createya.ai)
