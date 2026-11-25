---
name: comfy-cloud-mcp
description: Use Comfy Cloud MCP from Codex to generate or edit images, video, audio, or 3D assets; search Comfy Cloud models, nodes, and templates; upload input media; run ComfyUI workflows in the user's Comfy Cloud account; poll jobs; cancel jobs; and retrieve generated outputs. Trigger when the user mentions Comfy Cloud, Comfy Cloud MCP, cloud.comfy.org, hosted ComfyUI generation, Comfy model/template/node search, or wants Codex to create media through their Comfy Cloud account.
---

# Comfy Cloud MCP

## Core Rules

- Confirm the Comfy Cloud MCP tools are present before promising generation. If no Comfy Cloud MCP tools are visible, tell the user to restart Codex or verify `mcp_servers.comfy-cloud`.
- Treat generation as account-affecting work. It can spend Comfy Cloud credits or queue cloud jobs, so clarify costly or ambiguous requests before submitting.
- Use live discovery tools for model, node, and template choices. Do not hard-code current catalog facts from docs, GitHub commands, or memory.
- Prefer existing Comfy Cloud templates over building workflows from scratch.
- Validate that each submitted workflow has a user-intent input path and at least one retrievable output/save node.
- Keep the local `comfyui-workflow-builder` skill for detailed workflow JSON editing, node graph reasoning, and local ComfyUI workflow validation.

## Workflow

1. Inspect the active Comfy Cloud MCP tool names and schemas in the current session.
2. Search before generating:
   - Use template search for task-level requests.
   - Use model search for model selection.
   - Use node search when the user names a provider, model family, node, or capability.
3. Upload user-provided media before referencing it in a cloud workflow.
4. Route partner/API-node requests directly when the server exposes a suitable partner generation tool.
5. For workflow jobs, submit only API-format workflow JSON or a supported template-derived workflow.
6. Poll job status at a modest cadence, report brief progress, and cancel if the user asks.
7. Retrieve outputs with the server output tool and present saved file paths or URLs clearly.

## Command Equivalents

Codex does not install Claude Code slash commands. If the user pastes or mentions a `/comfy-cloud:*` command, treat it as an intent alias:

- `/comfy-cloud:generate-image`: generate, edit, or modify an image.
- `/comfy-cloud:generate-video`: generate, edit, or extend a video.
- `/comfy-cloud:generate-audio`: generate audio.
- `/comfy-cloud:generate-3d`: generate a 3D model.
- `/comfy-cloud:remove-background`: remove the background from an image.
- `/comfy-cloud:upscale-image`: upscale an image.
- `/comfy-cloud:search-models`: search available models.
- `/comfy-cloud:search-nodes`: search available nodes.
- `/comfy-cloud:search-templates`: search workflow templates.
- `/comfy-cloud:help`: summarize visible Comfy Cloud MCP capabilities.
- `/comfy-cloud:combine-people`: composite people only after confirming input images and consent.
- `/comfy-cloud:rickroll`: proceed only as an explicit playful generation request; do not surprise users.

## References

- Read `references/cloud-tool-patterns.md` before building or submitting Comfy Cloud generation workflows, adapting Claude command guidance, or troubleshooting Comfy Cloud MCP tool behavior.
