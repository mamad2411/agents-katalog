---
name: ttapi-midjourney-video
description: Animate a starting image with TTAPI Midjourney Video, optionally specify an ending frame, extend completed video clips, and query or download results. Use for Midjourney视频、MJ视频、图片转视频、首尾帧动画、Midjourney视频续写. Requires an input image; this is distinct from Midjourney image generation.
---

# TTAPI Midjourney Video

Requires Node.js 20+; API calls need network access and `TTAPI_API_KEY`. No MCP server is required.

Use the separate `/midjourney/video/*` product for image-led animation and continuation. Read [the video contract](references/video.md) before preparing inputs, especially the batch size and motion fields. Current official references are discoverable through [TTAPI llms.txt](https://docs.ttapi.io/llms.txt). Installation source is [ttapi-io/ttapi-skills](https://github.com/ttapi-io/ttapi-skills).

## Configure and inspect

The bundled script reads `TTAPI_API_KEY` from its process environment and sends it as `TT-API-KEY` to `https://api.ttapi.io`. Obtain the key from the [dashboard](https://dashboard.ttapi.io/). Never ask the user to paste it into chat, print it, or store it in request JSON, code or Git.

Run commands from this installed Skill directory, or use an absolute script path:

```sh
node scripts/ttapi.mjs models
node scripts/ttapi.mjs schema midjourney-video-generate
node scripts/ttapi.mjs submit midjourney-video-generate --input examples/midjourney-video-generate.json --dry-run
```

These are local inspection commands, not API-key or model availability verification. Replace the sample first-frame URL and previous job IDs with the user's real assets. A remote publicly accessible image is required; local paths, Base64 and `{"$file":"..."}` are not documented video input formats. If the user has only text, obtain their intended source image rather than silently adding a separate paid image generation.

## Execute and retrieve

- A request to generate or extend a video authorizes that requested operation within the user's chosen scope. Generation/extension consumes quota; preserve existing authorization rather than repeatedly asking during polling. Check [current video pricing](https://docs.ttapi.io/grids/en/start/pricing/video) before quoting a cost. Do not add unrequested paid variants or retries.
- `midjourney-video-generate` needs `prompt` and `imageUrl`. Optional `endingUrl` fixes the final image. `model: "fast"` is a speed mode, `manual` is `low` or `high`, and `resolution` is `sd` or `hd`. There is no documented text-only, duration, audio or aspect-ratio JSON field in this product.
- Set `bs` explicitly for the requested number of outputs (1, 2 or 4). The server documents a default of four; the bundled generation example chooses one. Do not silently turn a one-clip request into a default four-video batch.
- Save `data.jobId` from the submission acknowledgement and poll **this product's** `/midjourney/video/fetch`. Fetch is documented as free and does not create another video. Completion requires the fetch status and actual output URLs, not just submission `SUCCESS`.

```sh
node scripts/ttapi.mjs submit midjourney-video-generate --input request.json --wait --output ./videos
node scripts/ttapi.mjs get midjourney-video-generate --task SAVED_JOB_ID --wait --output ./videos
```

- For extension, first fetch the completed source video job and verify the selected zero-based `index` exists. Submit `midjourney-video-extend` with that source `jobId`, `index`, and explicitly chosen `bs`. Preserve the newly returned task ID. An image job ID or a video URL is not the source-task input for this endpoint.
- Download the returned `data.videos[]` promptly. Return the saved paths, operation, task ID and actual quota if the response includes it; connect files to the current project only within the user's requested scope.

Never automatically repeat a video generation/extension POST after a timeout, lost connection or unclear acknowledgement. Resume the recorded task, or inspect saved receipts/the dashboard if no task ID was returned. A local wait limit does not fail or cancel the remote generation.
