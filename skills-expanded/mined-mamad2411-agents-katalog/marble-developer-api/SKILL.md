---
name: marble-developer-api
description: Build against the World Labs / Marble Public API v1 docs. Use when a coding agent needs to explain or implement World API integrations, WLT-Api-Key authentication, world generation, media asset upload flows, long-running Operation polling, world retrieval/list/delete, pano depth-to-RGB calls, or OpenAPI client generation.
---

# World Labs API

Use this skill when the user is working with the published World Labs /
Marble Public API v1.

Before answering API-contract questions or writing integration code, read
[references/api.md](references/api.md). For exact current endpoint and schema
details, also inspect [references/openapi.yaml](references/openapi.yaml).

## Working Style

- Authenticate with the `WLT-Api-Key` header, not bearer auth.
- Treat API keys as secrets. Never print, commit, or log a real key.
- Prefer explicit model names such as `marble-1.1` or `marble-1.1-plus`.
- Use media asset uploads for local image/video files before world generation.
- Poll `/marble/v1/operations/{operation_id}` until `done` is `true`; fetch the
  world by `world_id` when the caller needs the latest world object.
- Verify against `references/openapi.yaml` when generating clients or naming
  request fields.

## Common Tasks

- Write curl, Python, TypeScript, or SDK-style examples for world generation,
  operation polling, world retrieval, media asset upload, and pano depth-to-RGB.
- Generate or update client code from the OpenAPI spec.
- Explain request shapes for text, image, multi-image, video, media-asset, and
  URL-based world prompts.
- Debug authentication, validation, media upload, operation status, and asset URL
  issues.
