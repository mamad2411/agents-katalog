---
name: ttapi-flux-image
description: Generate, edit, restyle and combine images using TTAPI FLUX 1, FLUX 2, FLUX Kontext, FLUX 3 Image and FLUX 3 Image Klein. Use for FLUX image requests including Flux生图、Flux改图、多图融合、Kontext、Klein; does not handle FLUX video.
---

# TTAPI FLUX Image

Use this product's bundled Node.js 20+ client. Run commands from this skill directory or resolve its absolute path first. Keep `scripts/`, `examples/` and `references/` together when installing this independent skill.

Example natural-language request: “Use FLUX 3 Image to make one square mountain illustration and save it to my assets folder. / 用 FLUX 3 Image 生成一张方形山景插画并保存。” Preserve the user's chosen product, model, creative intent and requested output count. Inspect their project before choosing where to save or integrate files.

## Select the documented operation

Read [product contracts](references/api.md) for exact input fields, task transport, limits and known documentation inconsistencies. The table below lists the implemented workflows; it is not a live account/model-discovery endpoint.

| Operation | Purpose |
| --- | --- |
| `flux-generate` | Generate images through TTAPI’s Flux compatibility request. |
| `flux-edit` | Edit with one or more local reference files using the documented multipart route. |
| `flux-kontext-max` | Generate or reference-edit using Flux Kontext Max. |
| `flux-kontext-pro` | Generate or reference-edit using Flux Kontext Pro. |
| `flux-ultra` | Generate using Flux 1.1 Pro Ultra. |
| `flux-pro-1-1` | Generate using Flux 1.1 Pro. |
| `flux-pro` | Generate using Flux 1 Pro. |
| `flux-dev` | Generate using Flux 1 Dev. |
| `flux-2-pro` | Generate or reference-edit using Flux 2 Pro. |
| `flux-2-flex` | Generate or reference-edit using Flux 2 Flex. |
| `flux-2-max` | Generate or reference-edit using Flux 2 Max. |
| `flux-2-klein-4b` | Generate or reference-edit using Flux 2 Klein 4B. |
| `flux-2-klein-9b` | Generate or reference-edit using Flux 2 Klein 9B. |
| `flux-3-image` | Generate, edit, restyle or combine up to ten references using FLUX 3 Image. |
| `flux-3-image-klein` | Generate or edit using FLUX 3 Image Klein with optional exact dimensions and seed. |

Use `node scripts/ttapi.mjs models` to list bundled operations, then `node scripts/ttapi.mjs schema OPERATION` before constructing JSON. Follow the [official TTAPI docs index](https://docs.ttapi.io/llms.txt) to locate current product docs if the request is outside this snapshot; llms.txt is a document index, not an executable SDK or MCP service. Do not invent an endpoint or substitute another product's parameter names.

## Configure and create

The local environment must provide `TTAPI_API_KEY`; it is sent as the `TT-API-KEY` header to the documented TTAPI gateway. Obtain a key from https://dashboard.ttapi.io. If missing, explain how to set it in the process that runs the scripts. Never ask for the real key in chat, echo it, embed it in a command argument, write it into request JSON, or put it into frontend/source files.

Install this product from the published collection when needed:

```sh
npx skills add ttapi-io/ttapi-skills --skill ttapi-flux-image
```

Adapt the selected example to the user's real prompt, reference images and desired model. Example media URLs and local paths are documentation inputs, not supplied user assets. Optional controls are not instructions to increase cost or change content.

```sh
node scripts/ttapi.mjs schema flux-3-image
node scripts/ttapi.mjs submit flux-3-image --input examples/flux-3-image.json --dry-run
node scripts/ttapi.mjs submit flux-3-image --input request.json --wait --output ./outputs
```

Installing, models, schema and dry-run do not call a generation API. Generating/editing consumes prepaid TTAPI quota; check [current image pricing](https://docs.ttapi.io/grids/en/start/pricing/image) when a cost estimate is requested. A clear user request to generate/edit authorizes that requested operation; proceed without an extra confirmation. Asking for documentation, options, a preview or dry-run does not authorize a paid request. Do not add paid variants or replacements beyond the requested scope.

## Save results and resume safely

Submit a requested generation only once. Save the returned operation and taskId immediately; an acceptance status with only an ID is not a finished image. The client writes local task receipts before waiting. For async operations, query the same job and download the generated result:

```sh
node scripts/ttapi.mjs get flux-3-image --task SAVED_TASK_ID --wait --output ./outputs
```

Use the selected operation's documented poll method; do not mix task IDs across products. Stop on terminal success/failure or the wait limit. A timeout does not establish failure: preserve the ID and resume `get`. If a submission times out without an ID, it may have reached TTAPI; check the local receipt/dashboard and report uncertainty instead of automatically repeating a paid POST. A failed result does not authorize a paid replacement.

Return the selected model/route, status, task ID and saved file paths or generated URLs. Download useful media promptly because storage is temporary. Integrate only the generated asset into the user's project; credentials remain in the local script environment. If a current official contract conflicts with this client, explain the precise mismatch before attempting an unsupported operation.
