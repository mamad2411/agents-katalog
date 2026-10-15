---
name: mixio-generate
description: "Generate images and video through Mixio Studio jobs — script breakdown, keyframe sequences, image and video generation with character/location reference consistency."
version: 0.1.0
invoke: /mixio:generate
---

# Mixio Generate

Submit and track Studio generation jobs (image, video, script breakdown, keyframe sequences) through the proxied `studio_*` MCP tools. Jobs are billable and run async by default.

## Prerequisites

- MCP server configured in your agent: `@mixio-pro/mcp` (see INSTALL.md)
- **Resolved scope — required.** You must be working against a project, plus the deepest scope you know (episode / scene / shot) that the user has
  explicitly confirmed. If it is not established in this session, **fetch the list and show
  it, numbered, in the same message as the question** (`studio_list_projects` /
  `studio_list_episodes`) so the answer is one character. Asking "which episode?" without
  the list is a failure — it hands the lookup back to the user. Resolve this *before* any
  expensive read; never guess an id, infer one from a title, or create something to avoid
  asking. See `mixio-project`.

## Models & Use Cases

Model and use-case IDs change as Studio adds providers — always confirm with `studio_list_generation_models` / `studio_list_use_cases` before hardcoding an ID. As a starting point:

| Media | Model IDs |
|-------|-----------|
| Image | `gpt_image_2`, `gemini_image`, `nano_banana_2`, `seedream_5_pro`, `seedream_5_lite` |
| Video | `seedance_image_to_video_pro`, `seedance_text_to_video_pro`, `seedance_image_to_video_v2`, `veo_3_1`, `sora_2`, `kling_text_to_video_2_6_pro` |

Common `useCaseId` values: `image-hub` (general image gen with references), `production-generate-shot-keyframe-sequence` (production keyframes — see table below), `image-edit` (requires a source image), `refine-character-image`, `production-generate-video`, `keyframe-sequence` (Generate-page multi-frame workflow — does **not** land under a shot), `script-preproduction`.

## The use case decides where output lands — not `context`

This is the single easiest thing to get wrong, and it costs a paid job. Passing a correct `context: { projectId, episodeId, sceneId, shotId }` is **not sufficient** to make output appear under a shot. The use case has to be a production-scoped one.

| Use case | Scope | Output appears |
|---|---|---|
| **`production-generate-shot-keyframe-sequence`** | **one shot, planner-driven multi-frame sequence (`4/6/8/10/12` frames)** | **under that shot** |
| `production-generate-keyframes` | production, current scope | under the scene/shot in the production view |
| `production-generate-shot-keyframes` | one shot, single or counted keyframes | under that shot |
| `production-generate-scene-keyframes` | one scene, single or counted keyframes | under that scene |
| `production-generate-shot-keyframe-grid` | one shot, storyboard grid | under that shot |
| `production-generate-scene-keyframe-grid` | one scene, storyboard grid | under that scene |
| `production-generate-video` | production, current scope | under the scene/shot |
| `keyframe-sequence` | **not production-scoped** (`outputType: IMAGE`, `surfaces: ["generate"]`) | general / Image Hub list, *not* under the shot |
| `keyframe-grid` | not production-scoped (`outputType: IMAGE`, `surfaces: ["generate"]`) | general / Image Hub list |
| `image-hub`, `image-edit`, `refine-character-image` | general | Image Hub list |

All `production-*` use cases share `outputType: "STUDIO"` and `surfaces: ["studio"]`.

⚠️ **Discovery pitfall:** Because their `outputType` is `"STUDIO"`, production use cases are **invisible** when calling `studio_list_use_cases({ outputType: "IMAGE" })`. Call with no filter or `outputType: "all"` to see them. When operating inside a production pipeline, use the IDs directly — do not try to discover them via an `IMAGE` or `VIDEO` filter.

Observed in real use: a `keyframe-sequence` job submitted with a fully correct `context` including `shotId` still landed in the general Image Hub list and never appeared under the shot. The fix was resubmitting as `production-generate-shot-keyframe-sequence`. The Generate-page `keyframe-sequence` runs the same multi-pass Agno workflow but lacks production scope binding.

**Rule: if the user expects to see the result under a scene or shot in Studio, use a `production-*` use case.** Call `studio_list_use_cases()` to confirm the current set, and `studio_get_use_case_input_schema({ useCaseId })` for its exact contract, before submitting.

### You cannot verify context from the job read

`studio_get_job_status` returns `{ job: { id, status, jobType, createdAt, updatedAt, providerStatus, queuePosition }, tracking: {...} }`. It does **not** echo `projectId`, `episodeId`, `sceneId` or `shotId`, so there is no way to confirm from the response that your scope persisted. Get it right on submit; you will not get a second chance to check cheaply. On completion, confirm the link by querying relations or elements for the shot rather than by reading the job.

### No cancel tool

There is no MCP cancel. Cancellation is HTTP-only (`POST /api/studio-jobs/{id}/cancel`), which means shell access and handling the API key outside the MCP boundary — and that endpoint has been observed returning HTTP 500. **Do not design a flow that depends on cancelling.** Confirm cost before submitting instead; a misrouted job cannot be reliably recalled.

## MCP Tools

| Tool | Purpose |
|------|---------|
| `studio_submit_studio_job` | Submit one image/video/script-breakdown/keyframe-sequence job |
| `studio_batch_submit_studio_jobs` | Submit up to 50 jobs in one call (same job shape, wrapped in a `jobs` array) |
| `studio_get_job_status` | Poll a job by `jobId` **and** `projectId` — returns status + output URL when complete |
| `studio_list_generation_models` | List model IDs, optionally filtered by `useCaseId` or `mediaType` |
| `studio_list_use_cases` | List use-case IDs, optionally filtered by `outputType` |
| `studio_list_references` | List a project's CHARACTER/LOCATION/PROP elements — use to get reference image URLs |
| `studio_get_use_case_input_schema` | **Returns the exact input contract (media slots + parameters) for a use case.** Call this before submitting an unfamiliar use case instead of guessing at `input.media` / `input.parameters` |
| `studio_generation_catalog_get` | Bounded catalog read (newer discovery adapter, smaller result set than `list_generation_models`) |
| `studio_get_studio_job_api_schema` | Returns the underlying HTTP contract for `/api/studio-jobs/*` — rarely needed since the tools above cover submit/status directly |

Call `studio_tools_describe` on any of these for the exact current input schema.

### Audio — reachable, but not discoverable

There is no dedicated audio MCP tool, and both discovery filters omit audio:
`studio_list_use_cases`'s `outputType` enum is `IMAGE | VIDEO | all`, and
`studio_list_generation_models`'s `mediaType` is `image | video | all`.

Audio generation nevertheless **works through the normal job path** — the engine
has an `AUDIO` output type and use cases including `text-to-speech`,
`voiceover`, `voice-change`, and `audio-driven-performance`, and
`studio_submit_studio_job` accepts any `useCaseId` string:

```
studio_list_use_cases()                       // no filter — audio use cases appear here
studio_get_use_case_input_schema({ useCaseId: "text-to-speech" })   // exact contract
studio_submit_studio_job({ jobType: "audio", useCaseId: "text-to-speech",
                           prompt, input: { parameters }, context: { projectId } })
```

Call `studio_list_use_cases()` **without** `outputType` to see them — passing
`"IMAGE"` or `"VIDEO"` filters them out, and there is no `"AUDIO"` value to pass.
Confirm the current ids from that call rather than trusting the list above.

### Key gotchas (from the tool's own docs)

- **Reference images and aspect ratio must go through `input.media` / `input.parameters`.** Omitting them silently generates without reference consistency at a default `1:1` aspect ratio.
- **`input.media` slots take real URLs, not Payload media IDs.** The server rejects UUID-looking values. `studio_list_references` only returns a summary (`hasAttachments` boolean, no URLs) — get the actual attachment URLs from `studio_get_element`/`studio_get_production_context` (`referenceVariants[].attachments[].media.url`), or upload fresh with `upload_file`/`get_public_url`. See `mixio-references` for the full Cast & World reference workflow.
- Media slots: `primary`, `references`, `character_ref`, `location_ref`, `style_ref`, `asset_ref`, `endFrame` — each accepts `{ url }` or an array of them.

### Link every job to everything it knows about

Six separate context mechanisms, and they do different jobs. Pass all of them you can.

| Field | Shape | Why |
|---|---|---|
| `context` | `{ projectId (required), episodeId?, sceneId?, shotId? }` | Where the job belongs. **Always pass the deepest scope you know** — a shot-level job should carry all four |
| `selectedElements` | `[{ id, type, identityKey?, mentionCode? }]` | Which characters/locations/props the prompt refers to. Helps the backend resolve references and hold consistency |
| `slotReferences` | `{ <slot>: { url, elementId?, mediaId?, referenceType?, displayLabel? } }` | Images **with provenance**. Unlike raw `input.media`, `elementId` records which element an image came from |
| `slotTags` | `{ <assetKey>: "@tag" }` | Binds a reference image to a mention tag. `assetKey` is `elementId \|\| mediaId \|\| url` |
| `mentionMap` | `{ "@tag": "Human Label" }` | Binds that tag to a subject name. **Both maps are required** for a tag to bind |
| `input.media` | `{ <slot>: { url } }` | Raw URLs with no provenance |

Prefer `slotReferences` over bare `input.media` when the image came from a Studio element — the `elementId` is what lets scene anchors dedupe against an explicit per-shot choice instead of attaching twice. `type` in `selectedElements` is one of `CHARACTER`, `LOCATION`, `PROP`, `SHOT`, `SCENE`.

A job that passes only `projectId` and raw URLs will still render, but nothing downstream can tell what it was *for*.

- `input.parameters`: `aspect_ratio` (`auto`, `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `21:9`), `quality`, `duration` (video, seconds), `style`, `output_format`, `watermark` (Seedream models only), `keyframe_count`, `sequence_notes`, `orchestrate_frames`.
- `keyframe_count` is a **closed set, not a range**: `4 | 6 | 8 | 10 | 12` for `production-generate-shot-keyframe-sequence` (default `6`), and `1 | 2 | 3 | 4 | 6 | 8 | 9` for `production-generate-shot-keyframes`. Odd values in between are rejected. The 12 ceiling comes from a 16-slot output reservation shared with up to 4 background plates — `orchestrate_frames` does **not** raise it. For more than 12 frames, submit more than one job.
- `orchestrate_frames` is already `true` by default on the production sequence path. It makes the job return a *plan* and dispatch one child job per frame rather than rendering inline. Side effect worth knowing: the server's own evaluation pass is **skipped** whenever it is true, so run `mixio-eval` yourself before delivery.
- `sequence_notes` is the one lossless way to add direction to a sequence job. It is appended verbatim to the planner's prompt, whereas a caller-supplied `prompt` **replaces** Studio's auto-assembled shot-spec prompt (camera enums, dialogue, scene heading, scaling constraints) instead of adding to it. Leave `prompt` unset and use `sequence_notes` unless you intend to author the whole prompt.
- `studio_get_job_status` requires **both** `jobId` and `projectId` — it's not a bare job lookup.
- There's no MCP cancel tool. Cancellation is HTTP-only (`POST /api/studio-jobs/{id}/cancel`), outside this tool set.
- Job status values: `PENDING`, `RUNNING`, `IN_QUEUE`, `IN_PROGRESS`, `COMPLETED`, `FAILED`, `CANCELLED`.

### Mentions — how a reference image gets bound to a subject

Sending two character images does **not** tell the model which is which. That binding is done by `@tag` tokens in the prompt, rewritten at dispatch into whatever reference syntax the provider speaks (`@Image1`/`@Element1` for Kling, `image1` indexed, `@Image1`/`@Video1` for Seedance, `Image 1` for Hailuo). Substitution happens **in place**, so the tag binds wherever you put it in the sentence.

- **For `production-*` use cases the maps are derived for you** from the shot's related elements, and anything you pass overrides the derived value. You mostly get binding for free.
- **For every other use case there is no derivation.** Send `slotTags` + `mentionMap` yourself or multi-reference binding silently does not happen: the images are uploaded, no token exists to rewrite, and the model guesses which subject is which.
- **Write the tag as the element's name, slugified with dots** — `Tony` → `@tony`, a look variant → `@tony.casual`. `mentionCode`, `title`, `displayLabel` and `name` are all resolved as aliases, so a tag matching any of them binds.
- **Literal `slotTags` values only survive in generic form** — `@char1`, `@loc1`, `@asset2`, `@style1`, `@scene1`, `@shot1`, `@pose1`, `@Image1`. Anything else is reassigned. Use the human form in the *prompt* and let aliases resolve it; use the generic form only when you need to pin a specific slot.
- **An unresolved tag degrades to its plain label** rather than leaking `@garbage` into the prompt. Safe, but the binding is lost with no error — so verify the reference actually carries the name you tagged.
- Tags prefixed `@scene`, `@shot`, `@style` or `@pose` are treated as narrative bookkeeping, not bindable subjects, and are skipped when subject bindings are built.

Put per-character staging inline next to the mention rather than in a separate field — `@tony (MC, three-quarter-left, seated cross-legged, on BED)`. Structured staging fields get flattened or dropped on the way to the model; the mention token is the one thing guaranteed to survive with its position intact.

## Workflow

```
1. studio_list_use_cases() / studio_list_generation_models()   → confirm useCaseId / model
2. studio_list_references(projectId) → studio_get_element(referenceId)   → get character/location reference image URLs, if needed
3. studio_submit_studio_job({ jobType, model, useCaseId, prompt, input: { media, parameters }, context: { projectId } })
                                                                  → job id + tracking
4. studio_get_job_status({ jobId, projectId })                  → poll until COMPLETED, read output.output_url
5. (optional) upload_file(local_path)                            → persist a local render to workspace
```

## Prompt Tips

### Images
- Be specific about composition: "wide shot", "close-up", "overhead"
- Specify lighting: "golden hour", "neon-lit", "soft diffused"
- Include medium: "photograph", "digital painting", "3D render"

### Video
- Describe motion: "slow pan left", "tracking shot", "zoom in"
- Keep prompts shorter than image prompts (models handle less complexity)
- Specify duration and a start frame (`input.media.primary`) when possible

## References

See `references/model-comparison.md` for how to pick a model/use case from the live catalog.
