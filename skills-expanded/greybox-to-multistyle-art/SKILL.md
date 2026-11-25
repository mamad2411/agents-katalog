---
name: greybox-to-multistyle-art
description: Batch-transform one gameplay greybox into playable prototypes in multiple art styles. Use for style exploration, image-conditioned assets and native Godot/Unity integration with WorkBuddy, Claude Code or Codex. Also supports scoped greybox creation, local art revisions and editable Blender spaces when requested.
---

# One greybox, multiple playable art styles

**Version `0.15.3`.** One self-contained source package; no MCP, model switch or subagent is required. Keep installed files read-only and use the project's existing engine, assets and task records. [Status and limits](references/candidate-status.md) distinguish local execution tests from real host/provider qualification.

## Default: one gameplay greybox, multiple art styles

**从同一玩法灰盒，批量换皮多种美术风格的可玩原型。** Read the existing playable baseline once, select multiple styles, design their spaces and assets, finish the priority style's complete native sample, then batch the remaining selected styles through production and native delivery. Preserve the gameplay, shared inputs and every promised style. Batch work follows dependencies, accepted samples and actual account capacity; it is not a promise that all styles launch simultaneously or without user decisions.

For first use, follow [English quickstart](references/quickstart-en.md) or [中文快速开始](references/quickstart-zh.md). The user supplies the project, style goals and target device; the agent inspects the native entry, current controls/camera and existing PLAN/PROGRESS/FOCUS. A usable greybox enters art directly. Incomplete evidence needs inspection, not reconstruction. Native gameplay/space and selected concepts retain their separate authority.

For full-scene art, read [asset route decisions](references/asset-routes.md) after concept selection and before final native authoring. Explicitly assign generated, reused, procedural or hybrid sources to the concept's important forms; show the asset board and assembly plan before H3. Cheap native proxies do not automatically become final assets. Missing generation setup or paid authorization leaves the affected model work pending while the agent prepares its references, route and cost proposal.

Route by **intent × observed project state × requested endpoint**; the main workflow does not override a narrower request. For [greybox creation/revision or Blender spaces](references/greybox-authoring.md), stop at the requested native baseline or editable `.blend`; a spatial endpoint needs no game runtime. [Local art corrections](references/visual-harness.md) reuse the accepted direction and read the relevant method directly. Discussion ends with the requested proposal; [resume](references/continuity.md) preserves the original endpoint and task IDs. Explicit single-style work stays single-style. UE is [experimental](references/ue-greybox-experimental.md). Use [intake routing](references/intake-routing.md) when the branch is unclear.

Follow [host setup](references/hosts-v04.md) to verify the complete package, reuse a suitable installation and prepare only the current operation. Direct Python CLI is the default; native image tools can serve the image branch. Configure an external image service only when needed. A tool listing does not prove generation, pixel inspection or display.

For a new long-running art case, use [task context](references/task-context.md) to pin the actual package, Python and project in the existing PLAN, then continue through `task-context run`. On handoff or tool/model change, check the current context; refresh only affected operational facts. Unknown host facts remain unknown. Inspect the existing ledger's recovery route before choosing the executor; a legacy `run.json` is not a supplier queue.

Load the current method, not the whole reference directory:

```sh
python3 "$SKILL/scripts/greybox.py" knowledge next --stage concept
# For a known modeling asset, load only its category's necessary guidance:
python3 "$SKILL/scripts/greybox.py" knowledge next --stage references --asset-category humanoid
# On resume, the existing FOCUS includes current reading/navigation:
python3 "$SKILL/scripts/progress.py" focus --project "$PROJECT" --case "$CASE"
```

`knowledge next` selects short methods and optional topics; it never interprets images, generates, approves or dispatches work. The agent identifies the visual requirement and selects the relevant topic. Read only its `read_next` files. Intake ambiguity uses [routing](references/intake-routing.md); task recovery uses [continuity](references/continuity.md). Preserve original service IDs and resolve unknown submissions before any repeat.

When a concept or visible gap depends on materials, light, reflection, transparency, atmosphere or motion, use [scene effects](references/scene-effects.md) during design. Connect the visible requirement to geometry, assets, materials, light or effects and their necessary inputs; load `knowledge next --stage spatial --topic scene-effects` when needed. Reuse a suitable recipe, operate a documented native feature, or answer a route-changing uncertainty with a small native probe. A wrapper's limit calls for another suitable route; it is not the engine's capability limit. Choose effort by visual contribution, gameplay relevance, uncertainty and cost; simple scenes can keep simple rendering. No extra approval or automatic renderer switch follows from this routing.

## Current-stage methods

| Stage | Read and produce | Internal check before continuing |
|---|---|---|
| S0–S1 baseline | [Intake](references/intake-routing.md): source, camera, gameplay and visual freedom | Separate measured facts, inference and design; preserve working content |
| S2–S3 concepts / H1 | [Concept method](references/concept-authoring.md): default 8–10 exploration directions, or the user's count; separately record the selected delivery styles | Inspect each output for spatial relationships, real form/construction invention and requested style; check the first result before repeating a new method |
| S4–S6 atlas/design / H2 | [Spatial method](references/spatial-contract.md), [feature analysis](references/visual-feature-analysis.md) when interpreting the selected target, and [scene comparison](references/scene-comparison.md): key views, interfaces and cheap native composition probe | Compare target and actual whole scene before H3; record visible gaps in dominant forms, environment, light and contact |
| S7 references / H3 | [Reference method](references/modeling-references.md): record assets/views once, then `boards start` compiles page jobs; WorkBuddy uses `boards workbuddy start` to register its native scope in the same operation; then [assembly method](references/hybrid-production.md) | Consume the returned page jobs; preserve pending calls, crop every locatable slot, repair ROIs and review qualification separately; incomplete or failed views do not count as finished |
| S8–S9 sample / H4 | [Assembly method](references/hybrid-production.md); [scene comparison](references/scene-comparison.md) and [visual diagnosis](references/visual-harness.md) | Current target/native views and observations for every agreed critical feature; unresolved gaps block expansion |
| S10 delivery / H5 | [Review and decisions](references/human-decisions.md) | Current evidence and every promised style/space; record remaining defects |

H1 selects actual images and the priority style; H2 accepts design; H3 authorizes concrete production; H4 accepts a complete playable sample for expansion; H5 accepts the exact complete playable delivery. Reuse unchanged scoped user decisions, combine presentations where useful and never add approval for routine commands. A scoped native spatial delivery uses its own endpoint criteria rather than the playable H5 CLI. Serial self-review is available when independent review cannot run; record its actual reviewer/limitation. No agent review supplies user acceptance. Read [human decisions](references/human-decisions.md) for these handoffs.

## Production invariants

- **Two authorities:** native gameplay/space controls behavior, scale and interfaces; selected concepts control art. Resolve conflicts explicitly. Temporary silhouettes/colors are not art requirements. Do not turn every greybox edge into a locked contour.
- **Real inputs:** concept exploration normally uses one real 3D structural view. Write concrete design actions and targeted ambiguities. Modeling-reference generation receives actual approved style images. Record submitted images/order/prompt and output identity; a reference mentioned in prose is insufficient.
- **Every new AI mesh is image-conditioned**, using an approved isolated image or coherent multiview. No text-to-3D fallback. Preserve intrinsic patterns when cleaning references. Supplier/model/version/face count follow the user's effective policy and H3. G1 omits `enablePbr`; existing Turbo assets retain provenance and may be reused.
- **Asset routes cannot disappear:** classify form separately from native surface/light/effects; dominant forms need explicit generated/reuse/procedural evaluation and actual evidence for a procedural match. Selected AI/hybrid routes require actual image-conditioned operations and completed original model tasks before sample acceptance. Keep blocked work pending; do not replace it silently with code geometry or relabel a form as environment. Follow the same checkpoint when using direct host tools.
- **Complete compositions:** allocate principal forms, functional objects, environment, light, contact and connectors. Precise interfaces can use controlled geometry; dominant appearance needs a qualified generated, reused or authored route. A single attractive asset is not H4.
- **Select many, deepen one:** keep all selected styles promised, complete the priority style's agreed sample, then release later styles. Finite rooms cover the agreed room/core loop; continuous spaces retain global layout and deepen a connected sample with entry/exit and touching transitions.
- **Concrete review:** open actual pixels, check the few relevant criteria, record `pass`, `fail` or `unclear` with a visible observation. An unclear critical condition cannot pass. Fix the responsible layer and recheck affected evidence; do not tighten every constraint or regenerate good assets to repair one join. Repeated no-progress attempts change method within the existing repair allowance.
- **Incremental storage and continuity:** one case/shared/style workspace, canonical hashed assets, small source diffs and relevant evidence. Keep development/native-verified/human-accepted pointers distinct. Never copy whole projects, caches or asset trees for review. Upgrades do not relabel historical evidence; runtime-bound acceptance may need affected revalidation.
- **Learn from actual use:** record sourced [usage observations](references/usage-feedback.md) for meaningful failures, user corrections and changed repair methods during the task. Distinguish creative choices from rescue, and project workarounds from Skill fixes. At failure, pause, handoff and completion, show the current recap path and coverage gaps; check successful stages for missed rescue too. Keep the readable recap concise and full history in JSON. Carry unresolved issues forward on resume; export feedback and a local Issue draft when requested. Missing data stays unknown; no whole-conversation reread or extra reviewer is needed.

## Open details only when needed

Multi-task image/model work uses the [common executor](references/execution-contract.md):
queue authorized ready tasks; refill confirmed account capacity without batch
barriers; release generation slots at remote terminality before download; retain
unknown attempts and recover original IDs; extend adapters instead of ad-hoc
batch loops; isolate network actions with total deadlines so model/request stalls
cannot stop autonomous dispatch. Native tools use their actual host claim/record
path; independent dispatch needs separate evidence. More agents do not expand an
account's capacity or make an agent-driven channel autonomous.

Methods link their own protocols. Use [workflow contract](references/workflow-vnext.md) when writing checkpoints; [workspace](references/project-layout.md) for ownership; [production control](references/production-control.md) for pilots, combinations and repair lineage; [orchestration](references/orchestration.md) for parallel work. Native integration uses the selected [engine adapter](references/engine-adapters.md); [characters](references/character-pipeline.md) and Blender are conditional on the actual task.

Provider configuration/quotes use [capability preflight](references/capability-preflight.md) and [suppliers](references/suppliers.md) only when needed. Setup, balances and adapters never authorize paid work. Use actual existing authorization, retain unknown provider jobs and continue independent ready work.

Report the visible result, largest unresolved gap and next action. Keep technical checks, native behavior, visual judgment, performance and human acceptance separate. The package does not automatically judge images or guarantee student-model quality.
