---
name: build-vox-explainer-video
description: Build source-bound VOX-style Chinese explainer external-generation material packs, dynamic blueprints, or complete videos with research, fact script, narration beats, editorial collage keyframes, start/end image pairs, provider-neutral video prompts, authored semantic states, layered motion plans, deterministic overlays, optional conditioned video/TTS, provenance, cost controls, and hash-backed QC. Use when Codex is asked to plan, storyboard, generate image materials and prompts for external video platforms, animate, create, or improve a VOX/Vox-style science, history, technology, mechanism, map, data, documentary, collage, or motion-rich explainer without changing the separate codex-video-workflow Skill.
---

# Build VOX Explainer Video

## Purpose

Build a reproducible editorial evidence system, not a generic AI montage. Keep facts, exact copy, maps, charts, citations, timing, rights, and acceptance deterministic. Use generated pixels as bounded visual material; never use them as factual proof.

Maintain this Skill independently from `codex-video-workflow`. Write only under the selected run directory and never patch a sibling Skill to complete a VOX run.

## Load the contracts

- Always read [isolation-and-boundaries.md](references/isolation-and-boundaries.md) and [production-orchestration.md](references/production-orchestration.md).
- Read [editorial-and-visual-contract.md](references/editorial-and-visual-contract.md) before claims, scenes, or prompts.
- Read [reference-to-prompt-loop.md](references/reference-to-prompt-loop.md) before selecting a visual family.
- Read [dynamic-motion-blueprint.md](references/dynamic-motion-blueprint.md) before planning shots, states, motion tracks, transitions, prompts, or an animatic.
- Read [external-generation-material-pack.md](references/external-generation-material-pack.md) when the user wants prompts and image materials for another video platform.
- Read [topic-to-visual-evidence.md](references/topic-to-visual-evidence.md) before accepting any keyframe or shot prompt as theme-specific.
- Read [layered-asset-motion.md](references/layered-asset-motion.md) before producing independently movable elements.
- Read [vox-continuity-and-chatcut-contract.md](references/vox-continuity-and-chatcut-contract.md) when the brief includes narration-bound image prompts, external video generation, or ChatCut assembly.
- Read [provider-prompt-contract.md](references/provider-prompt-contract.md) before adapting a prompt for Google Flow, Veo, or another image-to-video provider.
- Use [vox-still-image-prompt.template.md](assets/templates/vox-still-image-prompt.template.md) and [vox-shot-card.template.md](assets/templates/vox-shot-card.template.md) when authoring prompts or shot cards; do not improvise a style-only prompt that omits narration and visible proof.
- Use [vox-provider-video-prompt.template.md](assets/templates/vox-provider-video-prompt.template.md) for the provider-ready video prompt; preserve the section order and deterministic post ownership.
- Read [seedance-agent-plan.md](references/seedance-agent-plan.md) only for remote motion.
- Read [quality-gates.md](references/quality-gates.md) before advancing any state or claiming completion.

## Required input

Accept a brief matching `assets/schemas/vox-brief.schema.json`, or create it from a researched script. Require:

- title, one central question, duration of at least 6 seconds, aspect, and scenes;
- narration, objective, claim IDs, and one primary render route per scene;
- at least one saved source and rights basis per claim;
- at least one scene binding per claim and at least one claim per scene;
- a deterministic fallback for every `generative` or `hybrid` scene;
- a topic-specific visual description for every scene; the prompt must name the spoken beat, viewer takeaway, visible proof, and one hero relationship;
- explicit budget and remote-model entitlement when Seedance is planned.

Stop at planning when a factual or rights binding is missing. Never invent a source, authorization, evaluation score, or approval.

## Choose the delivery endpoint

Use the independent **external generation material pack** when the user wants everything needed for another video platform: research, angle, narration, VOX image logic, accepted start/end keyframes, exact still prompts, provider-neutral video prompts, negative prompts, exact overlay timing, and hash-backed QC. This is the default for “给我提示词和图片物料，我去其他平台生成视频.” A local animatic may not substitute for these images.

The topic must be present in the generated visual relationships, not only in narration, filenames, or post overlays. Require a per-shot topic binding, claim-to-visual proof objects, prompt anchor terms, and a generic-swap rejection. A keyframe that still works after replacing the requested subject with another company, model, country, or event is a generic template and fails.

The external compiler also emits `workflow/vox-video-generation-plan.json`. It is provider-neutral and records whether remote generation is explicitly authorized. Compilation never makes a remote video call; a remote mutation is a separate, ledger-backed execution step. The plan must preserve an executable local layered-motion fallback.

Use the independent **dynamic motion blueprint** only when the user explicitly wants choreography, timing, and local motion planning without requiring generated image materials. It does not call remote video, final TTS, the parent workflow, or write `vox-production-state.json`.

Use the full production state machine below only when the requested endpoint includes final imagery, final narration, remote generated motion, publication review, or a publishable MP4. A valid dynamic blueprint may later be adapted into full production, but never auto-advance or copy its derived stage into the full state.

### Build a dynamic motion blueprint

Research and author a source-bound motion brief. Treat runtime frames as `durationSeconds × fps`; never treat a number of still images as the production unit. Bind each narration beat to claims, visible proof, authored shot states, independently addressable layers, frame-indexed tracks, semantic events, audio motifs, a route/fallback, and a provider-neutral prompt handoff.

Compile without generating video:

```bash
node scripts/compile-vox-dynamic-blueprint.mjs \
  --brief /absolute/vox-motion-brief.json \
  --out /absolute/vox-dynamic-package

node scripts/validate-vox-dynamic-blueprint.mjs \
  --run /absolute/vox-dynamic-package \
  --require-stage prompts-ready
```

The compiler emits `workflow/vox-dynamic-blueprint.json`, narration, a claim/visual matrix, audio cue sheet, provider-neutral shot prompts, and a timeline review board. A state is a meaning-bearing endpoint on a shot, not a required image. Generated stills and video remain optional bounded route inputs.

Render a local, frame-seekable animatic when choreography proof is requested:

```bash
node scripts/render-vox-motion-animatic.mjs --run /absolute/vox-dynamic-package
node scripts/validate-vox-dynamic-blueprint.mjs \
  --run /absolute/vox-dynamic-package \
  --require-stage validated
```

The animatic uses deterministic local text and frame-indexed HTML motion, adds only motivated review sound effects, and extracts evidence frames from the rendered MP4. It proves timing and choreography, not final generated imagery, final narration, rights approval, or publication readiness. Never call it a finished video unless the full production gates below pass.

### Build an external generation material pack

Compile the researched external-generation brief first:

```bash
node scripts/compile-vox-external-generation-pack.mjs \
  --brief /absolute/vox-external-brief.json \
  --out /absolute/vox-external-pack
```

Generate every start keyframe with Codex Image 2 from the saved prompt. Generate the end keyframe as a constrained edit of that exact start image. Register both images with explicit QC using `register-vox-external-keyframe.mjs`, then require:

```bash
node scripts/validate-vox-external-generation-pack.mjs \
  --run /absolute/vox-external-pack \
  --require-stage materials-ready
```

Do not call a prompt-only package, local animatic, or set of generic framework pages `materials-ready`. The handoff must contain real accepted image pairs and the exact provider-neutral prompt for every shot. Every external prompt is narration-bound in three lines: exact spoken beat, viewer takeaway, and visible proof. The narration is semantic context only; generated pixels remain text-free. Every overlay is deterministic-post owned and fits inside its shot time window.

Before handing the pack to an external platform, run the provider adapter audit:

```bash
node scripts/validate-vox-provider-prompts.mjs \
  --run /absolute/vox-external-pack \
  --manifest /absolute/vox-external-pack/workflow/vox-google-flow-prompt-manifest.json \
  --provider google-flow-first-last
```

The audit checks provider-supported duration, start/end reference roles, static composition lock, narration/takeaway/visible-proof binding, ordered action windows, camera separation, end-state settling, text ownership, negative constraints, accepted image pairs, and overlay timing. It does not claim that a provider has rendered a successful clip; inspect every generated MP4 and keep the declared deterministic fallback.

## Start or resume a staged run

Use the orchestrator as the default entry point:

```bash
node scripts/run-vox-production.mjs \
  --brief /absolute/vox-brief.json \
  --out /absolute/run \
  --stop-after planning
```

Supported stops are `planning`, `aesthetic`, `anchors`, `layers`, `motion-ready`, and `review-ready`. The command may prepare work orders and return `complete: false`; that is a truthful handoff, not an error. Resume with the same brief and run after satisfying the named blocker.

Use `--dry-run` to plan without remote generation. Use `--force` only while the run remains `planned`; it may never replace accepted media, reviews, or human approvals.

For compiler-only use:

```bash
node scripts/compile-vox-package.mjs --brief /absolute/vox-brief.json --out /absolute/run
node scripts/validate-vox-package.mjs --out /absolute/run --require-stage planned
```

## Production state machine

Advance only when `validate-vox-package.mjs` derives the requested state from evidence:

`planned → aesthetic-approved → anchors-ready → layers-ready → motion-ready → audio-ready → parent-handoff-ready → review-ready → human-review → publish-ready`

Do not advance by manually editing `stage`, `status`, or `pass`. A state claim ahead of its artifacts fails validation. Any upstream hash change invalidates downstream evidence.

### 1. Plan claims, scenes, routes, and fallbacks

Use exactly one primary route per scene:

- `deterministic`: exact maps, charts, timelines, mechanisms, labels, dates, numbers, citations, and subtitles;
- `generative`: bounded atmosphere or character/environment motion without factual pixel text;
- `hybrid`: generated plate or subject plus deterministic local overlays;

Authorized archive or field footage is intentionally not a VOX primary route in this image-first Skill. If needed, hand it to the parent workflow as separately reviewed supporting B-roll; never let an unimplemented route silently fall back to generated anchors.

Generated imagery never owns factual proof. Every route, including `deterministic`, still passes through the aesthetic test and an approved anchor: that anchor is the composition/material target for the user's image-first workflow, while exact factual pixels remain locally rendered. The compiler emits the claim matrix, routing, style system, still prompts, Image 2 work orders, layer plan registry, provenance ledger, Seedance plan, cost plan, parent brief, and production state.

### 2. Prove the aesthetic direction

Select one reference for one visual problem. Save metadata, rights boundary, hash when available, and measurable decomposition—not Pinterest pixels without authorization.

Generate one original style test from the three-stage still prompt:

1. complete full-bleed base plate with topic-specific color, paper texture, torn/cut edges, depth, and no blank footer;
2. normally 3–5 core assets, or 5–8 semantically justified assets for a dense collage, distributed across depth planes and designed for later animation;
3. composition/fusion contract for hero relationship, reading path, overlap, gamut, shadows, caption safety by contrast, and layer separation.

Use the built-in `image_gen` tool for Codex Image 2. Node cannot call that contextual tool directly; `workflow/vox-image-work-orders.json` is the typed handoff. Inspect the image at full resolution.

Create run-local reference-study and review-input JSON, then record the result:

```bash
node scripts/record-vox-aesthetic-review.mjs \
  --run /absolute/run \
  --study /absolute/run/workflow/vox-reference-study-input.json \
  --review /absolute/run/workflow/vox-aesthetic-review-input.json
```

Require average score ≥88, every dimension ≥80, full bleed, no blank footer, no generated readable text/logo/pseudo-UI, no copied source layout, separable layers, and `approved-style-master`. A failed example remains iteration evidence only.

### 3. Generate and register still anchors

Generate every pending still-anchor work order with `image_gen`. Preserve exact text for local SVG/HTML. Regenerate malformed or fused assets; do not repair a weak composition by adding more random decoration.

Create a run-local QC JSON that names reviewer/time/provider/model and passes:

- `fullBleed`
- `noBlankFooter`
- `noGeneratedReadableText`
- `compositionPass`
- `continuityPass`
- `layerCutabilityPass`

Register each accepted anchor, selecting exactly one composition/material target:

```bash
node scripts/register-vox-image-asset.mjs \
  --run /absolute/run \
  --kind anchor \
  --id scene-01-anchor \
  --scene scene-01 \
  --asset /absolute/generated.png \
  --materialize /absolute/run/assets/anchors/vox-scene-01-anchor.png \
  --qc-file /absolute/run/workflow/vox-scene-01-anchor-qc.json \
  --composition-target
```

The registrar recomputes dimensions and hashes and updates the canonical anchor and provenance manifests. It never defaults QC to pass.

### 4. Build separable layers and deterministic motion

Resume with `--stop-after layers` after anchors pass. The orchestrator creates route-aware v2 plans and layer work orders for every scene. Deterministic scenes use local SVG/HTML generators; generative and hybrid scenes use isolated Image2 assets plus deterministic exact-text/evidence overlays.

Use the approved composite only as the composition/material target. Generate a clean environment plate and complete isolated subjects at matching angle and light. Do not use a flattened composite as the runtime page or destructively crop occluded objects.

Each layer requires a semantic role, unique z-order, one frame-clocked motion responsibility, visibility target, overlap cap, clean silhouette, seam check, provenance reference, and either a verified asset/hash or deterministic generator contract. Keep exact text, paths, charts, dates, labels, and citations deterministic.

Validate every required scene:

```bash
node scripts/validate-layered-assets.mjs \
  --run /absolute/run \
  --plan /absolute/run/workflow/vox-scene-01-layered-motion-plan.json
```

Only mark the corresponding `vox-layer-manifest.json` scene `approved` after its validation report passes. Use frame index as the canonical clock and retain at least three representative state-change frames.

For every generative or hybrid scene, `run-vox-production.mjs` then materializes the approved background and hero layers into `assets/motion/vox-<scene>-local-layered.mp4` with `render-vox-layered-scene.mjs`. This is the deterministic motion fallback and proves the isolated assets reach runtime pixels; exact text remains parent-owned.

### 5. Generate bounded Seedance motion

Use Seedance for 6–10 second plates, not an entire video. Preserve the approved anchor, prohibit text/new subjects/logos/factual pixels, allow at most one creative retry, and keep a deterministic fallback.

Initialize the ledger:

```bash
node scripts/seedance-task-ledger.mjs init \
  --plan /absolute/run/workflow/vox-seedance-shot-plan.json \
  --ledger /absolute/run/workflow/vox-seedance-task-ledger.json
```

Use `seedance-api.mjs` with `--run` for every network mutation. The default provider is `agent-plan`; credentials stay in `ARK_API_KEY` and are sent only to allowlisted official endpoints. Persist task ID before bounded polling, download immediately, and reconcile request/response/output hashes.

Register an artifact only after provider success and a run-local per-shot QC file proves the shot ID/hash, decodability, duration, endpoint stability, caption safety, identity/composition stability, and no text/extra subjects/factual contradiction. The QC input supplies at least three `evidenceTimestamps` and matching named `evidenceStates`; the ledger extracts those frames from the accepted MP4 itself and binds every frame to the artifact hash:

```bash
node scripts/seedance-task-ledger.mjs record-artifact \
  --ledger /absolute/run/workflow/vox-seedance-task-ledger.json \
  --shot-id scene-01-motion \
  --file /absolute/run/assets/motion/vox-scene-01.mp4 \
  --qc-file /absolute/run/workflow/vox-scene-01-motion-qc.json
```

Acceptance never defaults to pass. After the retry cap, activate the declared fallback with an explicit reason.

### 6. Generate or delegate narration

Default to the parent workflow's local TTS/timing unless the brief explicitly selects Agent Plan TTS. For Agent Plan:

```bash
node scripts/agent-plan-tts.mjs \
  --run /absolute/run \
  --text-file /absolute/run/script/vox-narration.txt \
  --out /absolute/run/assets/audio/vox-narration.mp3 \
  --receipt /absolute/run/logs/vox-agent-plan-tts-receipt.json
```

The wrapper requires terminal success, reconstructs and hashes MP3 audio, probes duration, records usage, and writes pending audio QC. Listen for pronunciation and timing, then record the review with `record-vox-audio-review.mjs`. TTS generation alone is not `audio-ready`.

### 7. Hand off to the parent renderer

The Skill emits `workflow/vox-parent-brief.json` and a hash-bound `workflow/vox-parent-handoff.json`. Only the orchestrator may set it `ready-for-parent` after aesthetics, anchors, layers, motion, and audio pass.

Use the separately installed `codex-video-workflow` for canonical narration timing, subtitles, local HTML/SVG motion, FFmpeg composition, covers, delivery packaging, and general media QC. Pass only run artifacts. Never patch or change its defaults.

Inspect the exact parent command first, then execute it through the read-only adapter:

```bash
node scripts/invoke-vox-parent-workflow.mjs --run /absolute/run
node scripts/invoke-vox-parent-workflow.mjs --run /absolute/run --execute
```

The adapter requires `parent-handoff-ready`, expands very short briefs to at least three narration beats without losing source-scene lineage, passes semantic layer responsibilities and accepted Seedance or local layer-composite motion plates, preserves optional Agent Plan audio, and verifies that the parent Skill source hashes did not change. Deterministic anchors remain reference-only and generated bitmap insertion is disabled. The adapter writes `workflow/vox-parent-input-bindings.json` before invocation and only writes a passing `workflow/vox-parent-consumption.json` when the parent design plan selects the exact source motion, all semantic units, deterministic bitmap policy, and active layered-motion scene.

Parent QC cannot waive VOX factual, aesthetic, generated-text, provenance, cost, or isolation failures.

Before parent handoff, record source/asset authorization and the disclosure decision with `record-vox-rights-review.mjs`. The command recomputes every local asset hash; non-local or incomplete assets cannot pass.

### 8. Final review and publication

Before `review-ready`, require:

- nonempty `renders/final.mp4`;
- passing parent `logs/qc.json` and delivery manifest;
- `workflow/vox-final-review.json` with at least three unique, decodable evidence frames, each carrying a distinct timestamp and named visual state;
- correct facts/text, no blank footer or generated pseudo-text/logo, stable composition, continuous layers, caption safety, meaningful motion, no extra subjects, and audio sync;
- recomputed local hashes and complete provenance.

Record the visual review with `record-vox-final-review.mjs`; the review input declares timestamps and named states, and the recorder extracts all evidence frames directly from `renders/final.mp4`, rejecting duplicate visual states. After explicit human approval, use `record-vox-human-approval.mjs` to validate all upstream gates and advance the state. The script cannot manufacture approval: its input must identify the approver/time and explicitly accept every publication concern.

Only a human approval manifest covering facts, rights, pronunciation, generated-content disclosure, cover, and final pixels may advance to `publish-ready`. Never label a fully automated run publish-ready.

## Output ownership

This Skill owns only VOX-prefixed workflow/prompt/log/screenshot files plus VOX-named media below the selected run:

- `workflow/vox-*.json`
- `workflow/vox-video-generation-plan.json`, `workflow/vox-chatcut-handoff.json`
- `prompts/vox-stills/*`, `prompts/vox-layers/*`, `prompts/vox-seedance/*`
- `prompts/vox-motion/*`, `prompts/vox-transitions/*`
- `prompts/vox-keyframes/*`, `prompts/vox-video/*`
- `assets/anchors/vox-*`, `assets/layers/<scene>/vox-*`, `assets/motion/vox-*`, `assets/audio/vox-*`
- `delivery/vox-*`
- `assets/style/vox-*`, `assets/parent-inputs/vox-*`
- `script/vox-*`, `logs/vox-*`, `screenshots/vox-*`

Parent outputs remain parent-owned. Never overwrite another Skill or a non-VOX artifact.

## Verification before handoff

Run:

```bash
node scripts/self-test-isolation.mjs
node scripts/self-test-contract-gates.mjs
node scripts/self-test-dynamic-blueprint.mjs
node scripts/self-test-external-generation-pack.mjs
node scripts/validate-vox-package.mjs --out /absolute/run --require-stage <stage>
node scripts/validate-vox-dynamic-blueprint.mjs --run /absolute/package --require-stage <stage>
node scripts/validate-vox-external-generation-pack.mjs --run /absolute/pack --require-stage materials-ready
```

Also run Skill Creator `quick_validate.py`, syntax-check every script, compare source and active install recursively, and forward-test the Skill on a fresh temporary run before claiming the update complete.
