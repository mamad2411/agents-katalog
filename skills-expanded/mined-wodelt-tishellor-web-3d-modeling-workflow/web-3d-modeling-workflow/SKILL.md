---
name: web-3d-modeling-workflow
description: Build and refine HTML/WebGL/Three.js scenes, reference-matched dioramas, and procedural assets. Prioritize composition, shape, materials and lighting; verify geometry, interaction and delivery with risk-based browser QA. Also supports reusable asset systems and measured performance work. Not for Blender-only pipelines or static 2D illustrations.
---

# Web 3D Modeling Workflow

Deliver the requested visual result in a usable, physically coherent scene. Algorithms, instance counts, audit files and time spent are implementation evidence, not evidence of resemblance.

## Choose the work route first

Choose from the user's deliverable, not scene complexity. Record the route briefly; no approval question is needed for a routine route choice.

| Route | Trigger | First reading | Main outcome |
| --- | --- | --- | --- |
| Reference reconstruction | Recreate a supplied image in a local or embedded 3D scene | [reference-first.md](references/reference-first.md) | Camera, silhouette, materials, light and recognizable detail |
| Original scene | Build a new scene without a defining reference | [blockout-and-asset-resolution.md](references/blockout-and-asset-resolution.md), relevant sections | Coherent design, supports, access and intended interaction |
| Reusable asset/system | Library, procedural generator, source-pattern study or reusable package | [workflow.md](references/workflow.md) | Construction, support, lifecycle and provenance contracts |
| Repair or optimization | Existing defect, slow rendering or integration problem | [pitfalls.md](references/pitfalls.md) or [web-3d-frontend-integration.md](references/web-3d-frontend-integration.md), affected topic | Reproduce, identify the owner, fix and recheck |

QA mode is separate from the work route. Use `fast` for local changes, `milestone` at coherent stages, and `local-final` for delivery. Use `audited-release` only for an explicitly requested audit/evidence package; a quality-first request or ordinary deployment does not imply it. See [qa-modes.md](references/qa-modes.md).

This route and its scope rules govern reading order and evidence depth in supporting references. Full production procedures are available when needed; they are not a checklist to execute wholesale on every local scene.

## Reference reconstruction priorities

Follow [reference-first.md](references/reference-first.md):

1. Inspect the image; record visible facts, uncertain inferences, camera/scale anchors, major objects, materials and support risks in a compact reference analysis.
2. Establish the camera and major masses. Reserve circulation and structural clearances before detailing. Macro and semantic proxies can share one simple scene.
3. Identify up to three largest visible mismatches in a fixed comparison view. Fix their owning camera, shape, material or light before expanding lower-impact systems.
4. Resolve recognizable assemblies and large/medium/small detail. Choose techniques because their visible result fits the reference, not because their algorithms are elaborate.
5. Show the first coherent usable preview as a progress milestone, then finish remaining visual and reliability checks. A preview is not a claim of completion.

“Quality first” means continue resolving meaningful visual and functional deficits. It does not require unlimited invisible polish, repeated full audits or turning a one-off scene into an asset framework. Respect explicit requests for extreme close-up detail or exported production geometry.

## Essential correctness

- Respect allowed directories, asset restrictions, existing code and delivery boundaries. Do not inspect prohibited files. If assets are forbidden, use custom construction and skip asset-catalog/source-mining tasks. Rendering libraries and content assets are distinct; disclose dependencies accurately.
- Keep axes, major dimensions, anchors, support heights, seeds and effect limits in shared configuration; use project types or JSDoc as appropriate. Do not migrate frameworks solely to satisfy a template.
- Supports must touch their surfaces; roofs/walls must enclose intended solids; parts need meaningful connections and clearances. Do not hide penetrations with camera-dependent visibility. Separate trunk clearance from crown overlap.
- Validate actual rendered geometry and instance transforms, not only declared envelopes. Check finite positions **and normals**, required attributes, nonzero normals, winding/closure for required solids and critical support contacts. Classify thin leaves, textile, water and decals as intentional sheets.
- Use stable semantic assembly IDs. Batch repeated parts while retaining ownership. Missing hero features cannot be excused by high instance counts or generic filler.
- Seed procedural systems independently where reproducibility matters. Define support/scatter masks before increasing density.
- Material identity must survive without post-processing. Geometry owns silhouette and meaningful seams; textures own surface-scale detail. Lighting must remain accountable to environment, key and practical sources.
- Use one renderer owner and scheduler; handle resize, visibility, reduced motion, failure and cleanup. Couple post-processing camera parameters to the actual render, including zoom, export and the first frame.
- Match shader patches to the pinned runtime, check insertion anchors and compile exercised variants. For view-dependent black blocks, isolate post passes and inspect invalid geometry/normals and non-finite HDR samples. A fallback filter does not prove the source defect is resolved.
- Preserve core geometry, materials, lights and shadows across exposed quality/mood states. Optimize duplicated work before removing visible content.

## Check reliability early

At the first coherent scene, exercise controls already exposed: orbit, continuous zoom, camera presets, supported pan, mood/quality changes, resize, reload and return from a hidden tab. Inspect console/shader health. Test new controls when introduced; do not postpone all interaction until final screenshots.

For local preview, verify the page **and entry/dynamic modules** load. Use a supported persistent preview mechanism, or a detached local server where permitted; do not assume a temporary command survives tool/task termination. Keep the intended interface/port local and provide a restart command. Recheck reachability before handoff; do not claim unattended uptime without evidence.

## Conditional video review for dynamic scenes

Prefer **GPT6-Astra (`gpt-6-astra`) or another model with video-reading capability** for recording and reviewing motion that static screenshots cannot establish. Verify that the current session can actually inspect temporal video content; the model name alone is not evidence of an available video input tool. Do not switch models or spawn another agent merely to enable this workflow.

At a meaningful animation milestone, a suspected motion defect, or final review of a motion-critical scene, consider recording the actual running scene and inspecting its continuous motion. Skip video for static changes, already-covered motion, or when it adds no useful evidence. Read [video-motion-review.md](references/video-motion-review.md) for capability checks, recording, diagnosis, and before/after verification. Frame extraction plus telemetry is a useful fallback, but must not be described as native video review or used to imply unobserved temporal behavior passed.

## Read specialist guidance only for the current decision

Read the relevant section when its owning problem arises; do not batch-load every file whose subject appears in the image.

| Decision | Reference |
| --- | --- |
| Detailed reference schema or strict analysis validation | [reference-image-analysis.md](references/reference-image-analysis.md) |
| Dimensions, support, OBBs, topology and placement | [geometry-and-placement.md](references/geometry-and-placement.md) |
| Roofs, glazing, joinery, signs and recognizable props | [detail-and-material-patterns.md](references/detail-and-material-patterns.md) |
| Missing lived-in/detail categories | [real-world-detailing.md](references/real-world-detailing.md) |
| Materials, indirect light, post effects and measured costs | [look-development-and-performance.md](references/look-development-and-performance.md) |
| Procedural construction and reusable hero contracts | [procedural-hero-assets.md](references/procedural-hero-assets.md) |
| Allowed existing assets actually useful to the task | [local-web-3d-asset-library.md](references/local-web-3d-asset-library.md) |
| Requested/needed source-pattern adaptation | [source-pattern-mining.md](references/source-pattern-mining.md) |
| Physical motion, wind, mood transitions and clipping | [animation-lighting-visibility.md](references/animation-lighting-visibility.md) |
| Capability-gated video diagnosis and acceptance of continuous motion | [video-motion-review.md](references/video-motion-review.md) |
| Renderer integration, shader versions and lifecycle | [web-3d-frontend-integration.md](references/web-3d-frontend-integration.md) |
| Retail circulation and fixture contents | [retail-layout-and-merchandising.md](references/retail-layout-and-merchandising.md) |
| Rain impacts and source/surface timing | [rain-and-surface-interaction.md](references/rain-and-surface-interaction.md) |
| Local acceptance and applicable check details | [qa-acceptance.md](references/qa-acceptance.md) |
| Explicit audited evidence package | [conformance-gate.md](references/conformance-gate.md) |

Templates and validators remain in `assets/` and `scripts/`; [workflow.md](references/workflow.md) explains the full production route. Reuse project checks rather than copying every template. Use an existing scene-tool preview/commit API when available; never bypass a failed transaction by editing state underneath it. Use Sites when `.openai/hosting.json` makes it the project owner; hosting remains subject to user scope.

## Local completion and stopping

Inspect the canonical scene, relevant blind spots and changed states; close applicable P0/P1 defects, run syntax/type/build checks appropriate to the actual stack, and verify the live URL. A static local scene need not undergo package promotion, full performance benchmarking or physical-motion audits.

Every extended check or polish iteration needs a reason: **observed defect or uncovered required risk → owner → expected visible/functional improvement → focused recheck**. Use before/after views for subtle claimed visual improvements. Do not invent new audits after agreed checks are clean.

Stop when important reference features and requested interactions are present, no known blocking visual/physical/runtime defect remains, and applicable checks pass. Reuse unaffected evidence. If remaining differences are optional or below the intended viewing scale, disclose them briefly and deliver; do not keep working solely because more detail is possible. Never mark an unresolved rendering or support failure as optional polish.

User feedback is valuable but is not an implicit mandatory approval gate. Unless the user explicitly requires sign-off, perform available visual review and continue authorized work; do not fabricate human approval or stop waiting for one.
