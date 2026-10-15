---
name: seaart-execute
description: "Optional SeaArt execution adapter for image and video generation. Use only after `image-create` or `video-create` and `image-prompt` or `video-prompt` have prepared a final Prompt, the user explicitly asks to generate with SeaArt, and a SeaArt MCP connection is available."
---

# seaart-execute

## Scope

- Treat this as an optional execution layer, never as an image or video creation entry point.
- Accept only a final Prompt, declared reference materials, output requirements, and an explicit SeaArt generation request.
- Do not replace an unavailable SeaArt setup with another provider. Return the prepared Prompt instead.

## Prerequisites

Before creating, editing, or generating media, confirm all of the following:

1. The user explicitly asked to generate with SeaArt.
2. The relevant upstream Prompt is complete: `image-create -> image-prompt` for images, or `video-create -> video-prompt` for video.
3. SeaArt CLI is installed and authenticated.
4. SeaArt MCP is configured in the current Codex host and its tools are available.

If either SeaArt CLI or SeaArt MCP is unavailable, do not submit a task. State:

> SeaArt execution is not configured. Install and authenticate the SeaArt CLI, configure the SeaArt MCP for this Codex host, then restart the host and retry. The prepared Prompt is ready to use.

Never ask the user to paste passwords, tokens, or cookies into chat. Do not print, store, or repeat credentials.

## Execution

1. Identify the requested mode: text-to-image, image edit, text-to-video, image-to-video, reference-to-video, or task status.
2. Resolve the model in this order: the user's explicit model, a compatible configured default, then the current SeaArt catalog.
3. Query the selected model's live parameters through SeaArt MCP before generation. Use only the returned model version and supported values.
4. Translate semantic reference labels from `video-prompt` into the MCP's accepted bindings. Do not submit unresolved references.
5. Submit only after the user has requested the paid or credit-consuming action.
6. Report the returned task ID, status, result URLs, and error description. Use `N/A` for fields the tool does not return.

## Boundaries

- Prefer SeaArt MCP for generation, model lookup, account lookup, and task status when it is available.
- Do not call undocumented SeaArt HTTP APIs directly.
- Do not invent model IDs, versions, parameter values, credits, task IDs, result URLs, or reference-image consumption.
- A request echo or metadata count proves request transmission only; do not claim the model consumed a reference without authoritative evidence.
- If a live parameter lookup fails or the requested mode is incompatible, report the exact failure and ask for a compatible model or a different next step.
