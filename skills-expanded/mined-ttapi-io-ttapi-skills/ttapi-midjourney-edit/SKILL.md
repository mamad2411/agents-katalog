---
name: ttapi-midjourney-edit
description: Edit or retexture supplied images through TTAPI's separate Midjourney Edit product, then query and save its four image results. Use for Midjourney编辑、MJ图片编辑、透明区域补绘、retexture、图片重新纹理化. This product accepts an image, unlike classic Midjourney jobId-plus-mask inpainting.
---

# TTAPI Midjourney Edit

Requires Node.js 20+; API calls need network access and `TTAPI_API_KEY`. No MCP server is required.

Use the dedicated `/midjourney/image-edits/*` product to edit or retexture a supplied image. Read [the operation reference](references/editing.md) for image preparation and result differences. Discover updated official API pages through [TTAPI llms.txt](https://docs.ttapi.io/llms.txt); source installation is [ttapi-io/ttapi-skills](https://github.com/ttapi-io/ttapi-skills).

## Configure and prepare

The bundled client reads `TTAPI_API_KEY` from its process environment and sends it as `TT-API-KEY` to `https://api.ttapi.io`. Get the key from the [dashboard](https://dashboard.ttapi.io/). Keep it out of chat, request files, logs, source and Git; do not print it to verify setup.

Run from this installed Skill directory, or use an absolute script path:

```sh
node scripts/ttapi.mjs models
node scripts/ttapi.mjs schema midjourney-edit
node scripts/ttapi.mjs submit midjourney-edit --input examples/midjourney-edit.json --dry-run
```

These inspection commands run locally, do not consume quota and do not verify the API key. Replace the example image URL with the user's actual public image or Base64 image data. For `midjourney-edit`, prepare transparent regions in the input image where changes should occur; do not substitute classic Midjourney's black-and-white mask payload. No `jobId` is needed to start a new edit.

## Execute and finish

1. Select `midjourney-edit` (`type: "edit"`) or `midjourney-retexture` (`type: "retexture"`) according to the user's goal. Preserve their original image and editing scope. Prefer English edit instructions as recommended by the source. Use the documented speed `mode`, not an invented model name.
2. Editing/retexturing consumes TTAPI quota and normally yields four image candidates. A request to perform the chosen edit authorizes that operation; preserve existing authorization without repeated approval questions. Do not silently add paid alternate styles, batches or retries. Check [current image pricing](https://docs.ttapi.io/grids/en/start/pricing/image) before quoting costs.
3. Save `data.jobId` from the submission acknowledgement, then poll this product's **own** `/midjourney/image-edits/fetch`. The official fetch endpoint is free and does not initiate another edit.

```sh
node scripts/ttapi.mjs submit midjourney-edit --input request.json --wait --output ./assets
node scripts/ttapi.mjs get midjourney-edit --task SAVED_JOB_ID --wait --output ./assets
```

4. On success, download `data.cdnImages` and return the saved paths with the operation and task ID. The raw response also retains original `data.images`, progress and actual quota when available. When requested, select the appropriate result and update the current project's asset reference; do not replace unrelated project files.

Never automatically resend an edit POST after a network error, timeout or unclear acknowledgement. Resume an identified task; if no ID was obtained, check saved receipts or the dashboard before another paid request. A local polling timeout does not fail or cancel the remote edit. Download completed results promptly.
