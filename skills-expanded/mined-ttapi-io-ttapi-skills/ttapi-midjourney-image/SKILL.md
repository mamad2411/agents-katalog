---
name: ttapi-midjourney-image
description: Generate and continue Midjourney images through TTAPI with imagine, action, blend, describe, seed lookup and region inpainting; query and download existing image jobs. Use for Midjourney生图、MJ绘图、图片融合、图片反推提示词、放大变体、局部重绘、seed查询. Distinct from the separate Midjourney Edit product and Midjourney video.
---

# TTAPI Midjourney Image

Requires Node.js 20+; API calls need network access and `TTAPI_API_KEY`. No MCP server is required.

Use this product Skill for the classic Midjourney image workflow. Read [workflows](references/workflows.md) for the operation and parameter differences. Discover current official documentation at [TTAPI llms.txt](https://docs.ttapi.io/llms.txt); this bundled catalog is a versioned contract, not a live account entitlement list.

## Configure and inspect

Read `TTAPI_API_KEY` from the environment of the process that runs this Skill. The client sends it as `TT-API-KEY` to `https://api.ttapi.io`. Obtain a key from the [dashboard](https://dashboard.ttapi.io/); never ask for it in chat, echo it, or put it in request JSON or Git. Installation uses the official repository [ttapi-io/ttapi-skills](https://github.com/ttapi-io/ttapi-skills).

Run from this installed Skill directory, or use an absolute script path:

```sh
node scripts/ttapi.mjs models
node scripts/ttapi.mjs schema midjourney-imagine
node scripts/ttapi.mjs submit midjourney-imagine --input examples/midjourney-imagine.json --dry-run
```

`models`, `schema` and `--dry-run` are local and do not generate media or validate the account key. Build the input from the user's brief. The sample job IDs and one-pixel Base64 images only demonstrate request shape; replace them with the user's real completed job, reference images and matching mask before an actual submission.

## Execute within the user's request

- An explicit request to create, blend, upscale, vary, describe, obtain a seed or inpaint authorizes that requested operation. Current image pricing lists describe and seed as billable too; do not present them as free metadata lookups. Check [current image pricing](https://docs.ttapi.io/grids/en/start/pricing/image) before quoting a cost. Preserve existing authorization; do not repeatedly ask during the same task. Do not add paid variants, upscales or retries beyond the requested scope.
- For a new image, use `midjourney-imagine`. One imagine request normally returns a four-image grid; do not promise one generated image. Use `midjourney-action` only after fetching a completed source job and choosing an exact action in its returned `components`.
- Use `midjourney-blend` for 2–5 Base64 images, `midjourney-describe` for reverse prompts, `midjourney-seed` for a source image's seed, and `midjourney-inpaint` for a same-size black-and-white mask. Do not mix these inputs with the separate `/midjourney/image-edits/*` product.
- Save `data.jobId` from every submission immediately. `SUCCESS` with only a job ID acknowledges acceptance. Fetch via `get OP --task ID`; querying the existing task does not create a new generation. Retain the original operation for text/seed results so they are not mistaken for missing image assets.

```sh
node scripts/ttapi.mjs submit midjourney-imagine --input request.json --wait --output ./assets
node scripts/ttapi.mjs get midjourney-imagine --task SAVED_JOB_ID --wait --output ./assets
node scripts/ttapi.mjs get midjourney-describe --task SAVED_DESCRIBE_JOB_ID --wait
```

Image results may include `images`, `cdnImage`, a completed `components` list and seed metadata. Describe returns prompt suggestions; inspect the returned raw task data without inventing an undocumented text field. A seed result may expose `data.seed`. Return the requested result, model/product, operation, task ID, file paths and actual quota only when supplied.

Never automatically repeat a submission POST after a timeout, disconnection or ambiguous acknowledgement. Resume the recorded task; if no task ID was obtained, inspect saved receipts or the dashboard before proposing another paid operation. A polling timeout does not fail or cancel the remote task. Download finished assets promptly and, when requested, connect them to the current project's existing asset conventions.
