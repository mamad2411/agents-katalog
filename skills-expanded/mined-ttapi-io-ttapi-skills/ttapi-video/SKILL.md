---
name: ttapi-video
description: Generate and download AI videos through TTAPI using Wan 3.0 or Grok, including text-to-video, first-frame image-to-video, Wan first/last frames, and querying existing tasks. Use for TTAPI video generation, Wan视频, Grok视频, 文生视频, 首帧图生视频, 首尾帧视频, or 视频任务查询.
---

# TTAPI Video

Use the bundled Node.js 20+ client to submit a video task, preserve its identifier, query it, and save the resulting video. It calls `https://api.ttapi.io` directly with the `TT-API-KEY` header derived from the `TTAPI_API_KEY` environment variable. Obtain the key from the [TTAPI dashboard](https://dashboard.ttapi.io); never place it in prompts, source files, request JSON, or command arguments.

## Choose the operation

- For Wan 3.0 text, a fixed first frame, or fixed first/last frames, read [references/wan.md](references/wan.md).
- For Grok text or first-frame generation, read [references/grok.md](references/grok.md).
- For an existing task, use its original operation and identifier. Querying does not submit a new generation.

Run commands from this skill's directory, or replace the script path with its absolute installed path:

```sh
node scripts/ttapi.mjs models
node scripts/ttapi.mjs schema wan-text-to-video
node scripts/ttapi.mjs submit wan-text-to-video --input request.json --dry-run
node scripts/ttapi.mjs submit wan-text-to-video --input request.json --wait --output ./videos
node scripts/ttapi.mjs get wan-text-to-video --task TASK_ID --wait --output ./videos
```

`schema` shows the supported request and an example. Build `request.json` from the user's prompt and the selected model; example media URLs are illustrations and must be replaced with the user's accessible assets. `--dry-run` validates locally without an API call. These video operations use JSON with remote media URLs; a local image path or `{"$file":"..."}` is not a video input URL.

## Execute and report

1. Select a documented operation and inspect its schema. Preserve the requested model. When no model was chosen, use a documented model appropriate to the input and state the selection.
2. Generation consumes the user's TTAPI balance. Establish authorization for the requested model, quantity and scope before submission; an explicit request to generate already authorizes that scope. Preserve that authorization across polling and completion, without repeatedly asking. Do not silently add paid variants, batch jobs, or replacement generations.
3. Save the returned task identifier immediately. Wan returns `output.task_id`; Grok returns `data.jobId`. Submission acknowledgement is not a completed video.
4. Poll through `get`, or use `--wait`. A timeout, interrupted connection or unknown submit outcome does not establish failure. Resume an identified task; if submission returned no identifier, inspect the dashboard before proposing a new paid submission. Do not automatically resubmit a generation POST.
5. Download completed videos with `--output`. Wan's documented result URL and task query validity are 24 hours, so save promptly. Report the model, task identifier, current status, and final video path or URL. Report actual quota only when the response supplies it; check [current video pricing](https://docs.ttapi.io/grids/en/start/pricing/video) before providing an estimate.

Do not combine the Grok compatibility request fields with the separate `/grok/v1/videos/*` API. Do not invent support for another model, media type or endpoint: the bundled catalog deliberately implements a verified subset of TTAPI's public documentation.
