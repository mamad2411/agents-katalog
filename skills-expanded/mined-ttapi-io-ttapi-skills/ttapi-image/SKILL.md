---
name: ttapi-image
description: Generate and edit images through TTAPI using GPT Image 2, GPT Image 2.5 variants, and Nano Banana models. Use for TTAPI image generation, reference-image edits, transparent product assets, 生图、图片编辑、图生图、商品图、海报、Nano Banana、香蕉模型, or resuming an existing TTAPI GPT image job.
---

# TTAPI Image

Use the bundled Node.js 20+ client. Paths below are relative to this installed skill directory. Keep the complete directory, including `scripts/` and `references/`.

Read `TTAPI_API_KEY` from the local environment; the client sends it in the `TT-API-KEY` header. Get an account/key from <https://dashboard.ttapi.io>. If missing, ask the user to configure the environment variable locally, without pasting the key into chat or a command argument.

## Choose the correct route

| Operation | Use | Response | Read when selected |
| --- | --- | --- | --- |
| `image2-generate` | Standard GPT Image 2, 2.5 Flare/Sunburst text-to-image | Synchronous base64 images | [GPT standard](references/gpt-image-standard.md) |
| `image2-edit` | Standard GPT Image 2 source-image/mask edits | Synchronous base64 images | [GPT standard](references/gpt-image-standard.md) |
| `image2-async` | User chooses TTAPI's unofficial GPT Image 2/2 Plus/2.5 route | Job ID, then fetch | [GPT asynchronous](references/gpt-image-async.md) |
| `nano-generate` | Any documented Nano Banana model; prompt-only or reference edits | Synchronous image URL | [Nano Banana](references/nano-banana.md) |

Keep an explicitly chosen model and route. `gpt-image-2.5` on the unofficial route and `gpt-image-2.5-flare` / `gpt-image-2.5-sunburst` on the standard route are different API values. Do not silently substitute them. If the user asks only for GPT Image 2 without a route preference, use `image2-generate`, or `image2-edit` when source images are supplied. `models` lists the bundled contract, not live account availability.

## Run a task

1. Use `node scripts/ttapi.mjs models` to discover operations and `node scripts/ttapi.mjs schema OP` for exact accepted inputs. Read only the selected route's reference. If current documentation changes the contract, report the mismatch instead of inventing fields.
2. Write the user's creative inputs to a JSON request file, preserving their intent and model choice. Start from `examples/OP.json`; do not treat its demonstration prompt or source photo as the user's input. Optional fields belong only when requested or useful. Default to one image. Reference URLs must be reachable by the API.
3. Optionally validate without making a request: `node scripts/ttapi.mjs submit OP --input request.json --dry-run`.
4. When the user has clearly requested generation/editing, submit once: `node scripts/ttapi.mjs submit OP --input request.json --wait --output ./outputs`. Generation consumes the user's TTAPI prepaid quota; dry runs and schema discovery do not. See [current image pricing](https://docs.ttapi.io/grids/en/start/pricing/image) if the user asks about cost. An explicit generation request already authorizes that requested generation; avoid an extra confirmation cycle.
5. For `image2-async`, retain the returned task ID and operation. Resume with `node scripts/ttapi.mjs get image2-async --task TASK_ID --wait --output ./outputs`. Querying the job does not submit another generation. A submission envelope with `status: SUCCESS` and `data.jobId` means accepted, not finished.

For a local source/mask with `image2-edit`, prepare JSON data URLs using the bundled helper:

```bash
node scripts/local-edit.mjs ./source.png ./request.json "Replace the background with a photography studio"
# Optional final argument: a local PNG mask.
node scripts/ttapi.mjs submit image2-edit --input ./request.json --output ./outputs
```

This helper only creates a local request file. It makes no API request. Nano Banana and the unofficial GPT route use public reference-image URLs; this skill does not invent a file-upload endpoint for them.

## Completion and recovery

- Standard GPT and Nano requests remain open until the result is ready. Their default gateway is `https://api.ttapi.org`, recommended by TTAPI for long synchronous image calls. They have no documented submit→poll contract here. Never call a different product's fetch endpoint to recover them.
- A synchronous timeout, disconnected submit, or unclear response may follow an accepted billable request. Do not automatically resubmit, change model, or promise idempotency: these endpoint docs do not specify an idempotency key. Return the uncertainty and let the user decide whether to create another generation. For asynchronous work, resume only using the returned job ID.
- Stop polling on documented success/failure or the client's wait limit. Preserve the task ID for later retrieval. A failed generation does not authorize an extra paid replacement.
- Return the selected model/route, status, file links or image URL, and task ID when relevant. Report server errors faithfully. Asset extraction uses generated-output fields only, not reference images.
- Download useful results promptly. TTAPI storage is temporary and varies by host; do not claim permanent URLs or a universal 72-hour lifetime. See [storage rules](https://docs.ttapi.io/grids/en/faq/storage).

This client accepts non-streaming responses only. It does not expose the upstream streaming/partial-image options.
