---
name: ttapi-novel-ai
description: Generate and redraw anime or illustration images with NovelAI on TTAPI, including text-to-image, image-to-image, character prompts and visual references. Use for NovelAI, Novel AI, NAI, 动漫生图、二次元、角色参考、图片重绘 through TTAPI.
---

# TTAPI NovelAI

Use this product's bundled Node.js 20+ client. Run commands from this skill directory or resolve its absolute path first. Keep `scripts/`, `examples/` and `references/` together when installing this independent skill.

Example natural-language request: “Use NovelAI to create one anime landscape and save it in my project. / 用 NovelAI 生成一张动漫风景图并保存到项目。” Preserve the user's chosen product, model, creative intent and requested output count. Inspect their project before choosing where to save or integrate files.

## Select the documented operation

Read [product contracts](references/api.md) for exact input fields, task transport, limits and known documentation inconsistencies. The table below lists the implemented workflows; it is not a live account/model-discovery endpoint.

| Operation | Purpose |
| --- | --- |
| `novel-text-to-image` | Generate anime or illustration images using documented NovelAI models. |
| `novel-image-to-image` | Redraw a supplied URL/base64 image using NovelAI image-to-image controls. |

Use `node scripts/ttapi.mjs models` to list bundled operations, then `node scripts/ttapi.mjs schema OPERATION` before constructing JSON. Follow the [official TTAPI docs index](https://docs.ttapi.io/llms.txt) to locate current product docs if the request is outside this snapshot; llms.txt is a document index, not an executable SDK or MCP service. Do not invent an endpoint or substitute another product's parameter names.

## Configure and create

The local environment must provide `TTAPI_API_KEY`; it is sent as the `TT-API-KEY` header to the documented TTAPI gateway. Obtain a key from https://dashboard.ttapi.io. If missing, explain how to set it in the process that runs the scripts. Never ask for the real key in chat, echo it, embed it in a command argument, write it into request JSON, or put it into frontend/source files.

Install this product from the published collection when needed:

```sh
npx skills add ttapi-io/ttapi-skills --skill ttapi-novel-ai
```

Adapt the selected example to the user's real prompt, reference images and desired model. Example media URLs and local paths are documentation inputs, not supplied user assets. Optional controls are not instructions to increase cost or change content.

```sh
node scripts/ttapi.mjs schema novel-text-to-image
node scripts/ttapi.mjs submit novel-text-to-image --input examples/novel-text-to-image.json --dry-run
node scripts/ttapi.mjs submit novel-text-to-image --input request.json --wait --output ./outputs
```

Installing, models, schema and dry-run do not call a generation API. Generating/editing consumes prepaid TTAPI quota; check [current image pricing](https://docs.ttapi.io/grids/en/start/pricing/image) when a cost estimate is requested. A clear user request to generate/edit authorizes that requested operation; proceed without an extra confirmation. Asking for documentation, options, a preview or dry-run does not authorize a paid request. Do not add paid variants or replacements beyond the requested scope.

## Save results and resume safely

Submit a requested generation only once. Save the returned operation and taskId immediately; an acceptance status with only an ID is not a finished image. The client writes local task receipts before waiting. For async operations, query the same job and download the generated result:

```sh
node scripts/ttapi.mjs get novel-text-to-image --task SAVED_TASK_ID --wait --output ./outputs
```

Use the selected operation's documented poll method; do not mix task IDs across products. Stop on terminal success/failure or the wait limit. A timeout does not establish failure: preserve the ID and resume `get`. If a submission times out without an ID, it may have reached TTAPI; check the local receipt/dashboard and report uncertainty instead of automatically repeating a paid POST. A failed result does not authorize a paid replacement.

Return the selected model/route, status, task ID and saved file paths or generated URLs. Download useful media promptly because storage is temporary. Integrate only the generated asset into the user's project; credentials remain in the local script environment. If a current official contract conflicts with this client, explain the precise mismatch before attempting an unsupported operation.
