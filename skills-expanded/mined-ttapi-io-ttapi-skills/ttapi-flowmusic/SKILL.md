---
name: ttapi-flowmusic
description: Generate FlowMusic/Lyria music and lyrics through TTAPI, extend or cover tracks, separate stems and import or export supported audio. Use for FlowMusic、Lyria音乐、背景音乐 and FlowMusic audio jobs.
---

# TTAPI FlowMusic

Use the self-contained Node.js 20+ client in this directory. Read `TTAPI_API_KEY` from the agent's execution environment; requests send the `TT-API-KEY` header to the documented TTAPI gateway. If missing, ask the user to configure it locally, without pasting a secret into chat, source files, request JSON or command arguments.

Read the relevant reference and inspect `schema` for the selected operation. The [official docs index](https://docs.ttapi.io/llms.txt) locates current endpoint documentation. Keep the user's chosen product, model and requested quantity. The local `models` command lists this version's supported contract, not account availability.

## Operations

| Operation | Use | Result |
| --- | --- | --- |
| `flowmusic-generate` | Generate one music clip from a sound prompt, lyrics, or both; asynchronous. | Task ID; resume the same job |
| `flowmusic-lyrics` | Generate lyrics from a prompt; synchronous response includes data.title and data.lyrics. | Task ID; resume the same job |
| `flowmusic-cover` | Create a new version of a completed FlowMusic clip. | Task ID; resume the same job |
| `flowmusic-extend` | Extend a completed FlowMusic clip; extend_s is at most 164 seconds. | Task ID; resume the same job |
| `flowmusic-stems` | Separate stems from a completed FlowMusic clip. | Task ID; resume the same job |
| `flowmusic-upload` | Import an audio file from a publicly reachable audio_url; not multipart. | Task ID; resume the same job |
| `flowmusic-download` | Request an existing FlowMusic clip in mp3 or wav format; asynchronous. | Task ID; resume the same job |

## Run in the user's project

Resolve this installed directory before running the client; the following commands run from it.

```sh
node scripts/ttapi.mjs models
node scripts/ttapi.mjs schema flowmusic-generate
node scripts/ttapi.mjs submit flowmusic-generate --input request.json --dry-run
node scripts/ttapi.mjs submit flowmusic-generate --input request.json --wait --output /absolute/path/to/project/assets
```

Build `request.json` from the user's actual brief and the selected schema. Bundled examples demonstrate input shapes; replace their sample prompts, example.com media URLs and placeholder previous IDs. A local file is not a public URL; use local file helpers only where the selected reference explicitly supports them.

`models`, `schema` and `--dry-run` work locally without a Key or API call. An explicit creation/edit request authorizes that requested paid operation; submit it once without another confirmation cycle. Do not add paid variants, batches or replacement jobs without a request. For unspecified quantity, default to one generation and explain products that intrinsically return multiple outputs.

For asynchronous operations retain the operation and returned task ID, then resume with `node scripts/ttapi.mjs get OPERATION --task SAVED_ID --wait --output /absolute/project/assets`. Submission acknowledgement is not completion. A timeout or unknown POST outcome must not trigger another paid submission. For synchronous endpoints, do not invent an asynchronous fetch workflow. Report errors and remaining uncertainty faithfully.

Save completed outputs to the user's existing project asset directory when asked, integrate them into the requested component and check the resulting page/player. Return the actual model, status, saved file paths and task ID when available. Retention varies; download useful outputs promptly. Check current [pricing](https://docs.ttapi.io/grids/en/start/pricing/audio) before quoting costs.

## Product references

- [flowmusic](references/flowmusic.md)

Install just this product with `npx skills add ttapi-io/ttapi-skills --skill ttapi-flowmusic`. This directory is independent of the legacy combined Skills and needs no MCP server.
