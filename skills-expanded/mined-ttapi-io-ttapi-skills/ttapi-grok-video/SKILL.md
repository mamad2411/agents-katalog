---
name: ttapi-grok-video
description: Generate videos through TTAPI Grok video endpoints and retrieve existing video jobs. Use for Grok video, Grok视频、文生视频、图生视频; use ttapi-grok-image for still images.
---

# TTAPI Grok Video

Use the self-contained Node.js 20+ client in this directory. Read `TTAPI_API_KEY` from the agent's execution environment; requests send the `TT-API-KEY` header to the documented TTAPI gateway. If missing, ask the user to configure it locally, without pasting a secret into chat, source files, request JSON or command arguments.

Read the relevant reference and inspect `schema` for the selected operation. The [official docs index](https://docs.ttapi.io/llms.txt) locates current endpoint documentation. Keep the user's chosen product, model and requested quantity. The local `models` command lists this version's supported contract, not account availability.

## Operations

| Operation | Use | Result |
| --- | --- | --- |
| `grok-text-to-video` | Generate a video from text with the TTAPI Grok compatibility endpoint. | Task ID; resume the same job |
| `grok-first-frame-to-video` | Animate a first-frame image with Grok fast or Grok 1.5 through the TTAPI compatibility endpoint. | Task ID; resume the same job |

## Run in the user's project

Resolve this installed directory before running the client; the following commands run from it.

```sh
node scripts/ttapi.mjs models
node scripts/ttapi.mjs schema grok-text-to-video
node scripts/ttapi.mjs submit grok-text-to-video --input request.json --dry-run
node scripts/ttapi.mjs submit grok-text-to-video --input request.json --wait --output /absolute/path/to/project/assets
```

Build `request.json` from the user's actual brief and the selected schema. Bundled examples demonstrate input shapes; replace their sample prompts, example.com media URLs and placeholder previous IDs. A local file is not a public URL; use local file helpers only where the selected reference explicitly supports them.

`models`, `schema` and `--dry-run` work locally without a Key or API call. An explicit creation/edit request authorizes that requested paid operation; submit it once without another confirmation cycle. Do not add paid variants, batches or replacement jobs without a request. For unspecified quantity, default to one generation and explain products that intrinsically return multiple outputs.

For asynchronous operations retain the operation and returned task ID, then resume with `node scripts/ttapi.mjs get OPERATION --task SAVED_ID --wait --output /absolute/project/assets`. Submission acknowledgement is not completion. A timeout or unknown POST outcome must not trigger another paid submission. For synchronous endpoints, do not invent an asynchronous fetch workflow. Report errors and remaining uncertainty faithfully.

Save completed outputs to the user's existing project asset directory when asked, integrate them into the requested component and check the resulting page/player. Return the actual model, status, saved file paths and task ID when available. Retention varies; download useful outputs promptly. Check current [pricing](https://docs.ttapi.io/grids/en/start/pricing/video) before quoting costs.

## Product references

- [grok](references/grok.md)

Install just this product with `npx skills add ttapi-io/ttapi-skills --skill ttapi-grok-video`. This directory is independent of the legacy combined Skills and needs no MCP server.
