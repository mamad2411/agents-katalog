---
name: comfyui-workflow-builder
description: Build, edit, debug, research, and prompt ComfyUI workflows. Use when Codex needs to create or modify ComfyUI UI workflow JSON or API prompt JSON, inspect graph routing, add nodes such as LoRA/control/audio/video loaders, research custom nodes or model requirements, write model-aware positive/negative prompts, diagnose workflow runtime errors, distinguish generation conditioning from final muxing, or verify ComfyUI node/model compatibility before creating runnable workflows. Pair with comfy-cloud-mcp when the user wants to run, search, upload, poll, cancel, or retrieve jobs through Comfy Cloud MCP.
---

# ComfyUI Workflow Builder

## Operating Procedure

1. Clarify the user's target behavior only when local files and the request are not enough.
2. Locate workflow files and identify whether each file is ComfyUI UI workflow JSON or API prompt JSON.
3. Run `scripts/inventory_comfy_workflow.py` on relevant workflows before editing.
4. Prefer modifying the closest known-working workflow over inventing a graph from scratch.
5. Trace model, CLIP, VAE, LoRA, conditioning, latent, image, video, audio, sampler, decoder, and save/mux paths.
6. Verify unknown node schemas before writing JSON. Prefer local `/object_info`, installed custom node source, existing examples, official docs, GitHub repos, Hugging Face model cards, and real workflow JSON.
7. Make a versioned copy unless the user explicitly asks to edit in place.
8. Patch exact nodes, links, widget values, titles, and groups. Preserve existing behavior unless the user asks for a behavior change.
9. Run `scripts/validate_comfy_workflow.py` after edits.
10. Summarize changed behavior, dependencies, install paths, test settings, and remaining risks.

## Comfy Cloud Handoff

- Use `$comfy-cloud-mcp` for Comfy Cloud account actions: model/node/template search, file upload, cloud job submission, polling, cancellation, and output retrieval.
- Use this skill for workflow JSON reasoning before cloud submission: graph structure, node schemas, UI-vs-API workflow conversion, routing, conditioning, and output-node validation.
- Before handing a workflow to Comfy Cloud MCP, verify it is API-format JSON unless the active cloud tool explicitly accepts UI workflows.

## Hard Rules

- Do not invent node class names, port names, widget order, model folders, or install requirements when they can be verified.
- Do not claim a source conditions generation unless the graph routes it into model patching, conditioning, latent generation, sampler guidance, or an encode/control path used before sampling.
- Distinguish generation conditioning from final audio/video muxing. Audio connected only to a final video node is output audio, not lipsync conditioning.
- Keep working defaults stable. Add new LoRA/control/audio branches disabled by default or at zero strength when the user wants an optional feature.
- Add clear node titles and labeled groups for user-facing controls.
- If a runnable graph cannot be verified, produce a safe scaffold, install checklist, or patch plan instead of fake workflow JSON.

## Reference Files

- Read `references/workflow-json.md` for UI workflow/API prompt structure, link edits, validation targets, and behavior-preserving patch patterns.
- Read `references/research-rules.md` when node schemas, model locations, dependencies, or install steps are unknown.
- Read `references/prompting.md` when writing positive/negative prompts or explaining prompt strategy.
- Read `references/video-workflows.md` for image/video/reference motion workflows, guide ordering, first/last frame guides, LoRA ordering, and over-copying issues.
- Read `references/audio-workflows.md` for vocal separation, lipsync conditioning, audio latent paths, and final mux audio.

## Script Usage

```bash
python scripts/inventory_comfy_workflow.py path/to/workflow.json
python scripts/validate_comfy_workflow.py path/to/workflow.json --summary
```

If a workflow fails validation, fix structural references before discussing creative or model-quality behavior.
