---
name: split-image-assets
description: Use when turning a source image into a reusable production asset package with independent transparent PNG layers, masks, cleaned background, structured metadata, inspection previews, QA evidence, and manual-review flags. Use for image decomposition, asset splitting, sprite-sheet preview generation, mask/background asset packaging, and workflows where a 2x2 preview must not replace reusable assets.
---

# Split Image Assets

## Mission

Turn a source image into a reusable, inspectable asset package.

This skill is not a one-shot image prompt. Its main output is an asset package with transparent PNGs, masks, cleaned background, metadata, previews, and QA evidence. A 2x2 sprite sheet is only a preview artifact.

This skill is not a professional segmenter. It does not promise production-grade automatic segmentation by itself. Its job is to receive, normalize, inspect, package, and validate results from professional upstream tools or manual workflows. If mature upstream extraction is unavailable, the run must stay in draft-only packaging rather than claiming production extraction.

Structure the work as four layers: capability preparation, whole-image planning, segmentation/generation execution adapter, and quality adjudication. Capability preparation decides whether the run can be production-capable. Whole-image planning decides which objects are worth raster effort at all and which route each object should follow. The execution adapter normalizes professional upstream outputs or approved generated candidates into package-owned assets, masks, and provenance. Quality adjudication separates structural validation from visual quality warnings, user/manual acceptance, and production reuse claims.

Before extraction, explicitly state the quality target tier for the run:

- `structural-valid`: package contract, provenance, previews, and evidence are complete
- `usable-draft`: candidate assets are organized and reviewable, but not yet signoff-ready
- `visual-acceptance-ready`: current assets are intended to support final visual acceptance

## Default Execution Contract

Conservative continuous execution is the default execution model. Keep the workflow moving unless a real stop condition is present.

Progress updates are commentary only. They report what is happening, what changed, and what remains, but they do not ask for confirmation by themselves and they do not pause execution.

Only the three formal stop classes may exit the workflow. Medium/high-risk semantic divergence is not a fourth stop class; it is the reason a branch may require a `user-decision` stop when the next choice would materially change package semantics, reuse boundaries, or acceptance claims and existing instructions do not settle it.

Every exit must include all of the following:

- `Why This Needs a Human`
- `Recommendation`
- `Options and Impact`
- `What I Will Do After Confirmation`

## Iron Rules

```text
ANALYZE BEFORE EXTRACTING
EXTRACTION CAPABILITY GATE
PREFLIGHT TOOLING RECOMMENDATION GATE
DO NOT START EXTRACTION BEFORE TOOLING PREFLIGHT IS REPORTED AND RECORDED
WHOLE-IMAGE PLANNING BEFORE EXPENSIVE OBJECT WORK
GRANULARITY ALIGNMENT GATE
GENERATION ROUTING GATE
CONFIRMATION GATE
PROGRESS UPDATES ARE COMMENTARY, NOT CONFIRMATION GATES
ONLY THREE EVENT TYPES MAY PAUSE EXECUTION
NO FORMAL GATE MAY BE SATISFIED BY AGENT DEFAULTING
INFERRED-FROM-USER MEANS EVIDENCE-BACKED USER INTENT, NOT AGENT GUESSING
PROFESSIONAL SEGMENTER FIRST
SEMANTIC LAYERS BEFORE RECTANGLES
QUALITY-GATED PIPELINE
DECISION SYNC BEFORE AMBIGUOUS SPLITS
DO NOT DEFAULT TO ONE-PASS EXTRACTION
REUSABLE ASSETS BEFORE PREVIEWS
TRANSPARENT PNGS ARE PRODUCTION ASSETS
SOURCE-SPACE MASKS ARE NORMAL
STAGE INTERMEDIATES
PREVIEWS ARE INSPECTION ARTIFACTS
NEVER HIDE UNCERTAINTY
```

## Interaction State Machine

Execution only pauses in three cases:

- `user-decision`
- `external-blocker`
- `formal-approval`

Everything else stays in `Running` and should be reported as commentary only. Progress summaries, tool output notes, and “still working” updates are not confirmation gates and must not stop the workflow.

Use these states consistently:

- `Running`: analysis, import, preview generation, scoring, QA inspection, validation, and evidence capture
- `AwaitingDecision`: a real user choice is required and will change package semantics
- `AwaitingExternalBlocker`: the workflow cannot proceed without tools, outputs, credentials, installs, or another external prerequisite
- `AwaitingApproval`: the workflow has enough evidence to request a formal approval gate such as pilot approval, final acceptance, or candidate promotion
- `Completed`: the current run has reached a real terminal outcome

When the workflow exits from `AwaitingDecision`, `AwaitingExternalBlocker`, or `AwaitingApproval`, the stop message must include `Why This Needs a Human`, `Recommendation`, `Options and Impact`, and `What I Will Do After Confirmation`. Do not exit with a bare question.

## Asset Value Scoring Gate

Asset value scoring happens before extraction. The goal is to decide whether an object should exist as a raster asset at all, not to justify extraction after the fact.

Apply an editability-first bias:

- ordinary text, button labels, numeric values, and form values should default to `rebuild_downstream`
- logo wordmarks, decorative text, and other visual-fidelity-critical text may route to `extract_asset`
- ambiguous high-complexity text-like objects should route to `requires_user_confirmation`

This is a normal running stage, not a default pause gate. Ordinary text defaults do not stop the workflow. Only a true `requires_user_confirmation` outcome should pause and ask whether the object should be rebuilt downstream or preserved as a visual asset.

## Workflow

1. Read `references/workflow.md`.
2. Create or inspect the package directory.
3. Initialize the package with `scripts/init_asset_package.py` when a package does not already exist.
4. Run the Preflight Tooling Recommendation Gate before selecting a recipe or starting extraction:
   - run `scripts/check_extraction_environment.py`
   - report `segmentation`, `matting`, `reconstruction`, `environment`, `production_capable`, `missing_for_production`, `missing_roles`, `recommended_installs`, and `why_it_matters`
   - distinguish installed tooling, runtime-ready tooling, and production-ready capability
   - explain which missing upstream roles affect the run: detection, segmentation, alpha refinement/matting, and background reconstruction
   - proactively recommend installing or activating missing professional upstream tools
   - ask whether to continue with `install-or-activate-tools`, `external-professional-outputs`, or `draft-packaging-only`
   - record the decision in `metadata.capability`, `metadata.confirmation.tooling_preflight`, and `metadata.decision_log[]`
   - do not continue into extraction until this decision is recorded
5. Read `references/pipeline-recipes.md` and `references/grounded-sam-pipeline.md` and select an extraction recipe before extraction.
   - read `references/default-route-chains.md` when route planning needs a default provider chain
6. Run the Granularity Alignment Gate before cutting pixels:
   - module-level, component-level, atomic-layer, or production-editable reconstruction
   - high-signal subset or full-image batch strategy
   - text/labels/buttons extracted as images or rebuilt downstream as live text/UI
   - carrier/glyph split, grouping, or conditional policy
   - exact background recovery required or approximate `background_clean.png` accepted as `needs-review`
   - animation-ready independent layers required or static reuse enough
7. For complex UI or graphic compositions, start with a high-signal subset instead of trying to atomize the entire image at once. Good first-pass targets are logos, nav icons, status dots, pins, checkboxes, chart marks, badges, and other small foreground elements whose masks can be inspected clearly.
   - high-signal subset examples do not by themselves authorize choosing a micro-asset package; keep the package aligned to the confirmed semantic branch and `resource_family`
   - for complex UI, run a pilot object first and stop for confirmation unless the pilot gate is explicitly recorded as `not-required`
8. For UI, dashboard, badge, tile/glyph, or dense interface images, read `references/ui-atomic-split.md` and create a semantic split plan before extraction.
   - classify each target as `ui-carrier`, `ui-glyph`, `carrier-glyph-pair`, `soft-edge-logo-brand-mark`, `outlined-illustration-logo`, `flat-support-plate`, or `photo-object-matte`
   - choose the upstream orchestration and repair path from that object type before cutting pixels
9. Run the Asset Value Scoring Gate before extraction:
   - classify each candidate as text-like or non-text
   - assign `text_role` and `text_render_class`
   - score `editability_score`, `visual_complexity_score`, and `asset_value_score`
    - set `decision_routing.recommended_action`
    - resolve `decision_routing.final_action`
    - only extract a production raster asset when `final_action=extract_asset`
10. Create or refresh `plan_manifest.json` before formal extraction or generation:
    - record the whole-image planning state separately from `metadata.json`
    - record per-object `planned_route`
    - use the planning routes `extract`, `reconstruct`, `generate`, `rebuild_downstream`, and `support_only`
    - record route signals for `recoverability_low`, `object_is_reconstruction_like`, `quality_target_high`, and `segmentation_cost_unfavorable`
    - record attempt budgets, token budget hints, pilot grouping, and protected-object approval requirements
11. Run the Generation Routing Gate before expensive object work:
    - `3/4` route signals may continue directly to a generated-candidate setup when no protected-object rule blocks the route
    - `2/4` route signals require a one-question `user-decision` stop
    - `0-1/4` route signals continue on the non-generation path
    - missing segmentation tooling alone must not justify a generated delivery path
12. Choose the default provider chain for the resolved route before broad upstream execution:
    - use `references/default-route-chains.md`
    - choose the route default first, then apply any explicit `object_type` override
    - this is the route default plus object_type override rule for provider selection
    - allow `plan_manifest.provider_preferences` to override the default only when the preferred provider is valid for the route
    - write a package-owned provider plan summary with `scripts/describe_provider_plan.py` before broad request generation so the selected provider, selection source, alternative providers, capability fit, and expected consume mode are explicit
    - write provider work-item status with `scripts/describe_provider_work_items.py` so each object has an explicit next action such as `prepare-generation-brief`, `prepare-provider-request`, `await-provider-result`, or `consume-provider-result`, without losing the capability-fit explanation
    - build provider request manifests with `scripts/prepare_provider_request.py`; `--provider-id` is optional when the default chain is acceptable
    - provider requests and results must satisfy the selected provider's registry-specific input/output contract, not just the generic JSON schema
    - for `generate` routes, write a package-owned brief first with `scripts/prepare_generation_brief.py`
    - keep provider requests and results under `_staging/providers/<provider-id>/<object-id>/`
    - record provider result manifests with `scripts/record_provider_result.py`
    - do not let provider bridge scripts write `metadata.json` directly; final package truth still changes only through explicit consumers
    - treat the provider bridge layer as the standard path between planning and import/compare/promotion
    - consume provider results through `scripts/consume_provider_result.py` when the result should enter import or staged-candidate flow
    - when one staged provider result is unambiguous, `consume_provider_result.py` may infer `--provider-id` and `--mode` from the bridge result plus plan defaults
    - for external-manifest providers, prefer `artifacts.provider_manifest` plus `consume_provider_result.py --mode import-manifest`
13. Analyze the source image before extraction:
    - visual hierarchy from background to foreground
    - main object
    - secondary objects
   - background type
   - occlusion
   - complex edges
   - transparent, reflective, fuzzy, smoky, or low-contrast regions
   - recommended split plan
14. When UI elements combine a carrier shape and a symbol, split them as tile/badge/panel background plus foreground glyph/symbol when independent reuse or clean edge review matters.
15. When the split plan has an ambiguous decision point, an uncertain text-like preservation choice, or a subjective reuse boundary, run the appropriate confirmation gate before extracting. Read `references/confirmation-prompts.md` for grill-me style prompt templates.
   - only real user decisions, genuine external blockers, and formal approvals may pause execution
   - if prior instructions already settle the branch, record the evidence-backed decision instead of asking again
   - ordinary progress updates remain commentary and do not pause execution
16. Read `references/quick-contract.md` for the short contract view, then `references/asset-package-contract.md` when you need the full package contract. Update `metadata.json` with the visual hierarchy, recommended split plan, `extraction_pipeline`, and object inventory.
   - record `metadata.granularity.mode`, `metadata.granularity.user_confirmed`, and `metadata.granularity.notes`
   - for UI or dense compositions, also record `metadata.granularity.scope_strategy`, `text_handling`, `carrier_glyph_policy`, `background_expectation`, and `layer_independence`
   - record per-object `value_scoring`, `decision_routing`, `rebuild_intent`, and `text_semantics`
   - record object `asset_class` and `reuse_status` so draft candidates, support layers, and production-ready atomic assets cannot be confused
17. Produce or collect reusable assets:
    - transparent PNGs for individual objects
    - source-space masks
    - cleaned background
    - optional shadows and grouped object layers
   - for UI carriers, use `scripts/generate_ui_carrier_candidates.py` when reconstruction candidates are needed
   - for hard-edge UI glyphs, use `scripts/generate_ui_glyph_cleanup_candidates.py` when cleanup variants are needed
   - for small assets under roughly 128 px, prefer `scripts/upscale_repair_downscale.py` before final cleanup when quality matters
   - use `scripts/score_candidate_assets.py` before compare when candidate count or quality variance is high
    - for generated-route objects, create a package-owned generation brief before generation begins and keep generated output in candidate state until compare/promotion/acceptance evidence exists
18. Put external model outputs, candidate masks, refinement files, temporary manifests, generation briefs, and provider bridge request/result manifests in `_staging/` while active, then `_archive_intermediate/` when retained for traceability.
   - use `scripts/archive_intermediates.py` when you want a deterministic archive step
   - use `scripts/describe_candidate_work_items.py` when staged repair candidates exist and you need an explicit next step for compare versus promotion
19. Normalize professional upstream results with `scripts/import_external_assets.py`. Treat this as the default production path:
   - professional upstream
   - `scripts/import_external_assets.py`
   - `scripts/build_previews.py`
   - `scripts/build_quality_previews.py`
   - `scripts/record_quality_review.py`
   - `scripts/validate_asset_package.py`
   - `scripts/export_asset_manifest.py`
20. Record per-layer segmentation quality evidence: semantic boundary, mask source, alpha source, edge checks, background residue checks, and reuse readiness.
21. Use `scripts/record_quality_review.py` to record semantic analysis, quality gates, object quality checks, formal gate decisions, and manual QA status after inspection instead of hand-editing JSON.
   - use formal gate writes only for real decision/approval state
   - keep commentary and review progress out of `metadata.decision_log[]` and `metadata.confirmation`
22. Build inspection previews with `scripts/build_previews.py`.
23. Build segmentation-quality previews with `scripts/build_quality_previews.py`.
24. Run `scripts/audit_visual_quality.py` for warning-only checks such as hard alpha edges, loose crops, large masks, and support plates miscounted as atomic assets.
25. Read `references/qa-standards.md` and inspect the package.
26. Validate structure with `scripts/validate_asset_package.py`.
27. Export a downstream layer manifest with `scripts/export_asset_manifest.py` after validation.
28. Read `references/manual-review.md` before assigning `pass`, `needs-review`, or `blocked`.

## Script Boundaries

The bundled scripts are deterministic packaging helpers. They do not perform segmentation, matting, inpainting, object recognition, or AI image generation.

Use external image tools, AI image editing, manual editing, or user-provided cutouts for the actual extraction work. Good default pipelines are Grounded-SAM/SAM2 style detection and segmentation, matting refinement with rembg/BiRefNet/RMBG-style tools, inpainting or manual paint repair for hidden background, and Qwen-Image-Layered style RGBA layer proposals when the source is a designed composition. Then use this skill to keep the package structure, previews, metadata, and QA evidence consistent.

Pillow, OpenCV, and skimage are not primary segmenters for production splitting. Use them for alpha compositing, PNG writing, source-space mask persistence, repair/refinement helpers, preview generation, metadata, and manifest packaging. Do not silently downgrade a production request to bbox or coordinate crops when the mature segmenter path is missing.

`scripts/import_external_assets.py` is the standard adapter for professional upstream outputs. Use it to copy SAM2, rembg, BiRefNet, RMBG, Qwen-Image-Layered, LayerDiffuse, manual, or user-provided assets into the package while recording object metadata and upstream tool provenance. This adapter path is the primary production workflow, not a side path.

`scripts/describe_provider_plan.py`, `scripts/describe_provider_work_items.py`, `scripts/prepare_provider_request.py`, `scripts/record_provider_result.py`, `scripts/consume_provider_result.py`, and the provider bridge helpers standardize how planned object routes talk to upstream providers. Use them to normalize provider planning, work-item status, requests, and results into `_staging/providers/` before import, compare, or promotion. This bridge layer should come before broad native-runner expansion.

`scripts/describe_provider_plan.py` is the planning-side bridge helper. Use it after `plan_manifest.json` is ready and before broad request generation so the package owns an explicit `_staging/providers/provider_plan.json` summary of route defaults, object-type overrides, valid plan preferences, selected providers, and alternative provider chains.

That provider-plan summary should also tell the operator whether the selected provider is preferred or merely tolerated for the current object type, which route-required capability tags it covers, and which consume mode is expected if the bridge succeeds.

`scripts/describe_provider_work_items.py` is the next-step bridge helper. Use it after provider planning to write `_staging/providers/provider_work_items.json` so each object records bridge artifact readiness, inferred consume mode when possible, and the recommended next command. Like the candidate-side surface, it should keep `recommended_command` for compatibility and may also expose `recommended_command_variants[]` plus a grouped `recommended_task` object when one provider bridge step has a stable task envelope.

`scripts/prepare_generation_brief.py` is the package-owned helper for generate routes. It writes `_staging/generation_briefs/<object-id>.json` plus `_staging/generation_briefs/<object-id>_reference_inputs.json`, and `prepare_provider_request.py` should fail closed for generate routes when those inputs do not exist yet.

For generated candidates, `consume_provider_result.py --mode stage-candidate` should also write a sibling provider-stage manifest under `_staging/repair_candidates/<object-id>/`. That stage manifest is the bridge between provider result evidence and later generated-reconstruction promotion.

`scripts/check_extraction_environment.py` is the preflight tooling recommendation gate. It checks optional module presence, runtime readiness, and production-ready capability for segmentation, matting, reconstruction, generation, and environment support. It does not install anything. For reconstruction, runtime support such as `torch` or `onnxruntime` is not enough by itself; only a dedicated reconstruction tool path should count as `production_ready=true`. For generation, raw image generation availability is not enough by itself; the provider must support object-level constrained generation plus transparent asset delivery before it can count as `production_ready=true`.

The capability report distinguishes module-installed from runtime-ready from production-ready states, lists `missing_for_production`, `missing_roles`, `recommended_installs`, and `why_it_matters`, and explains missing upstream role impact so an agent does not confuse partial local tooling with production readiness. `manual_redraw_path` is a human workflow, not automatic runtime capability, and should lead to `manual redraw required` or `approximate reconstruction only`, not to `production_capable=true`. Missing segmentation tooling alone must not be used as the reason to route an object into generated delivery.

`scripts/build_quality_previews.py` creates QA evidence images such as mask overlays and alpha inspection previews. These previews are inspection artifacts; they do not upgrade a package to `pass` by themselves.

`scripts/audit_visual_quality.py` creates `_staging/quality/quality_audit.json` and `_staging/quality/qa_audit_contact_sheet.png`. It is a warning-only visual audit for risks such as `edge-halo`, `color-residue`, `detached-fragments`, `smear-artifact`, `over-flat-reconstruction`, `style-mismatch-reconstruction`, `hard-alpha-risk`, `support-layer-misclassified`, and `carrier-glyph-cross-contamination`. It does not replace manual review and does not set `qa.status=pass`.

`scripts/record_quality_review.py` is the standard manual-review adapter. Use it to write `metadata.analysis`, append `metadata.extraction_pipeline.quality_gates`, update per-object `quality_checks`, set `metadata.qa.status`, and append `qa_report.md` notes after inspection. It refuses `qa.status=pass` unless every required object quality check is `pass`.

`scripts/export_asset_manifest.py` creates `asset_manifest.json` for downstream renderers, animation pipelines, design tools, or manual review. It records package-relative asset paths sorted by `composition_order`; it does not validate visual quality or replace `metadata.json`.

`scripts/archive_intermediates.py` moves active `_staging/` outputs into `_archive_intermediate/<run-id>/`, writes an `archive_manifest.json` for traceability, and rewrites `metadata.audit.quality_audit_path` / `previews.qa_audit_contact_sheet` when those audit artifacts are archived.

`scripts/compare_candidate_assets.py` is the standard compare helper for high-risk repairs. Use it to turn staged repair candidates into a compare artifact plus metadata evidence before promotion.

`scripts/promote_candidate_asset.py` is the deterministic promotion helper for high-risk repairs. Use it when `_staging/repair_candidates/` contains multiple staged candidate assets and one should become the current package-owned asset without hand-editing `metadata.json`. Candidate promotion should come from `_staging/repair_candidates/`, not an arbitrary package path.

When compare evidence already records `selected_candidate_id` and `selection_reason`, `scripts/promote_candidate_asset.py --comparison-id ...` may reuse those values instead of requiring them to be repeated manually. Missing compare-side selection evidence must still fail closed.

`scripts/describe_candidate_work_items.py` is the candidate-stage explainer. Use it to write `_staging/repair_candidates/candidate_work_items.json` so each object records whether candidate stage is still empty, compare evidence is needed, candidate selection is still pending, promotion is ready, or candidate work is already complete. That artifact should now keep `recommended_command` for compatibility, surface `recommended_command_variants[]` when the next step has meaningful yes/no/skip branches, and expose a higher-level `recommended_task` object when a lifecycle branch group exists. Each variant should be machine-readable enough to expose its `phase`, `intent`, branch flag/value, default recommendation status, required user-supplied fields, fields it writes, and expected next action on success.

When compare evidence exists but no selected candidate has been recorded yet, `scripts/describe_candidate_work_items.py` should recommend `scripts/record_candidate_selection.py` before it recommends approval or promotion. That selection adapter should record `selected_candidate_id`, `selection_reason`, and a decision-log entry without pretending candidate promotion has already been approved.

When compare evidence already selects a candidate but `metadata.confirmation.candidate_promotion` is still pending, `scripts/describe_candidate_work_items.py` should recommend the low-burden promotion-decision adapter before it recommends `promote_candidate_asset.py`.

That candidate-stage explainer should also surface staged candidate provider identities and flag mixed-provider candidate pools before compare, so generated-route repair work does not become provider-blind again.

For generated-route candidate pools, `scripts/describe_candidate_work_items.py` should also recommend compare commands that match the real provider-aware auto-discovery rules: use a plain auto-discovery compare command for single-provider pools, use the plan-preferred provider scope when an explicit generation provider preference is valid, and otherwise require an explicit `--provider-id` choice instead of pretending route-default compare is safe.

`scripts/record_candidate_promotion_approval.py` is the low-burden approval adapter for that handoff. Use it when compare evidence already owns the selected candidate or the compare set contains exactly one candidate, and you want to record the `candidate_promotion` gate without manually reconstructing the full `record_quality_review.py` decision payload.

`scripts/record_candidate_selection.py` is the low-burden candidate-selection adapter for the earlier compare step. Use it when compare evidence exists but the winner has not yet been recorded. It may reuse a single-candidate compare set, or resolve one provider-specific comparison through `--provider-id`, but it must still fail closed when the compare result is ambiguous.

`scripts/apply_candidate_selection_decision.py` is the thin lifecycle wrapper for that same handoff. Use it when you want one deterministic command to record the compare winner and optionally continue into a yes/no promotion decision. It should reuse `record_candidate_selection.py` first and then pass through `apply_candidate_promotion_decision.py` only when promotion is intentionally requested.

`scripts/apply_candidate_promotion_decision.py` is the next-step orchestration adapter for that handoff. Use it when you want one deterministic command to record a yes/no candidate-promotion decision and, for `yes`, continue directly into `promote_candidate_asset.py`.

When route evidence is already clear, `scripts/apply_candidate_promotion_decision.py` may infer `delivery_class` from the planned route or current object delivery state, and it may generate a deterministic default `repair_note`. If the route truth is not strong enough, it must still fail closed and require an explicit `--delivery-class`.

When no compare evidence exists yet but exactly one staged candidate exists, both `scripts/record_candidate_promotion_approval.py` and `scripts/apply_candidate_promotion_decision.py` may use that direct single-candidate path instead of forcing a synthetic compare step. Multi-candidate no-compare situations must still fail closed.

When provider-specific compare records or staged candidates exist in the same object pool, both adapters may take `--provider-id` so they can resolve the right compare evidence or the unique staged candidate for that provider. If `--provider-id` still maps to multiple compare records or multiple staged candidates, the adapters must fail closed and require a more explicit user choice.

`scripts/describe_candidate_work_items.py` should also surface staged candidate provider identities and explicitly flag mixed-provider candidate pools before compare, so generated-route candidate work does not become provider-blind again.

`scripts/promote_candidate_asset.py` should also fail closed until `metadata.confirmation.candidate_promotion` is `confirmed` or `not-required` from a real user-backed source. The helper and the runtime guard should agree.

## Pipeline Quality Rule

Every reusable layer must have provenance. Record which tool or manual process created the mask, which process created or refined alpha, which stage repaired the background, the layer's `composition_order`, and which quality gates were inspected.

Every object layer must also declare `asset_class` and `reuse_status`. Use `asset_class=atomic` plus `reuse_status=production-ready` only for inspected reusable assets. Use `candidate` plus `draft-candidate` for imported or unreviewed upstream results. Use `grouped-support`, `background-support`, or `preview-reference` plus `support-only` for plates, grouped UI chrome, backgrounds, contact sheets, and other support/reference layers.

Every object layer must also declare `object_type`, `delivery_class`, `current_asset_revision`, and when relevant `selected_candidate_id`, `repair_history[]`, `candidate_comparisons[]`, and `active_reconstruction_method`. This keeps the current promoted asset distinct from rejected or archived repair candidates and forces UI/logo assets onto the right repair path.

The package also uses a separate `plan_manifest.json` planning surface. Use it for whole-image route planning, object-level `planned_route`, route signals, attempt budgets, pilot grouping, protected-object approval requirements, and generated-route reasoning before expensive object work begins. Do not silently collapse the planning taxonomy into current `decision_routing.final_action`.

Record the split decision that governed the run. `metadata.granularity` is required so future agents can see whether the package was aligned to module, component, atomic-layer, production-editable, or draft expectations and whether the user confirmed that scope.

Record the quality target that governed the run. `metadata.quality_target.tier` should stay aligned to `structural-valid`, `usable-draft`, or `visual-acceptance-ready`, and `qa.status=pass` requires `visual-acceptance-ready`.

For UI and dense compositions, do not batch-extract the full image before granularity scope is explicitly confirmed or clearly derivable from prior user instructions. Record the high-signal subset strategy, text handling, carrier/glyph policy, background expectation, and layer independence inside `metadata.granularity`.

Record the tooling preflight decision that governed the run. `metadata.capability` is required so future agents can see whether the run was production-capable, what upstream roles/tools were missing, which user choice was made, and why missing tools affect quality. `qa.status=pass` requires extraction-capable `metadata.capability.production_capable=true` whenever the package still claims non-generated reusable layers. Generated-only pass paths must instead carry `metadata.capability.generation.production_ready=true` plus object-scoped generation-routing evidence. Draft-only or unrecorded tooling preflight must stay `needs-review` or `blocked`.

Draft-only packages must not look production-complete. Mark unreviewed cutouts as draft candidates, mark plates and `background_clean` as support-only when appropriate, and report production-ready assets separately from draft candidate assets and support-only layers.

The validator checks evidence, not aesthetics. A package can pass structural validation only when it records `metadata.extraction_pipeline`, ordered stages, structured upstream tools, quality gates, object-level `layer_kind`, `composition_order`, `semantic_boundary`, `mask_source`, `alpha_source`, and `quality_checks`, plus generated inspection previews and segmentation-quality previews for every reusable object layer.

Do not set `qa.status` to `pass` when any required object quality check is `needs-review`, `blocked`, or `unknown`.

## Semantic Layer Rule

Do not treat rectangular crops as asset splitting. A package with only page regions, grid cells, or convenient bounding boxes is not complete even when every crop has an alpha channel.

First identify the image's semantic layer hierarchy: background/backplate, frame or chrome, primary subjects, secondary objects, connection layers, labels, buttons or controls, shadows, and decorative details. Extract or reconstruct those layers separately. Use a rectangle only as the storage bbox around a semantic mask, never as the reason an asset exists.

If the hidden background cannot be recovered from one flattened image, create an honest `background_clean.png` approximation or leave the package `needs-review`/`blocked`; do not claim exact recovery.

Pillow crops, bbox masks, manual-estimated crop masks, or coordinate-only cuts are draft evidence by default. They cannot support `qa.status=pass` unless a human has confirmed the crop-only layer through `record_quality_review.py --confirm-crop-layer` and the object records `manual_review_confirmed=true`.

Likewise, helper-only extraction sources such as Pillow crop alpha, OpenCV threshold masks, or skimage thresholding cannot support `qa.status=pass` on their own unless a human explicitly confirms that layer.

Background clean plates, support plates, grouped structural UI regions, and inpainted/reconstructed areas may be useful deliverables, but they must be marked approximate when they are approximate and must record `reconstruction_provenance`. Keep them `needs-review` unless a human explicitly accepts that layer.

Approximate reconstructed carriers or clean plates should use `delivery_class=approximate-reconstruction`. Do not hide them inside `production-ready` naming or counts.

Generated object delivery is a distinct truth class. During rollout, use `delivery_class=generated-reconstruction` only when the package can also retain generated-route evidence such as provider/tool identity, brief reference, candidate comparison evidence, promotion approval, and selection rationale.

Source-space masks are expected: `masks/*.png` should normally match the original source dimensions for overlay QA and provenance tracing. A black mask with a small white component is valid when the object is small. Store the tight reusable visual result in `assets/*.png`; store the full-source QA mask in `masks/*.png`.

## Decision Sync Rule

Use these formal confirmation gates instead of vague “ask when needed” behavior. Each gate must map to one of the three allowed pause categories and must never rely on `agent-defaulted`.

- `Granularity Alignment Gate`
  - Pause category: `user-decision`
  - Trigger: complex UI, dashboard, dense composition, or any run where split scope affects reuse boundaries.
  - Ask: “Should this package target component-level, atomic-layer, or production-editable reconstruction?”
  - Recommended answer: `atomic-layer` for reusable UI atoms; `production-editable` when downstream rebuild matters.
  - Metadata effect: update `metadata.granularity.mode`, `scope_strategy`, `text_handling`, `carrier_glyph_policy`, `background_expectation`, `layer_independence`, and record a formal decision-log entry.
- `Generation Routing Gate`
  - Pause category: `user-decision`
  - Trigger: an object falls into the ambiguous `2/4` generate band, a protected object would otherwise route to `generate`, or a route switch would materially change the delivery truth class.
  - Ask: “Should this object continue on extraction/reconstruction, or switch to generated-reconstruction candidate flow?”
  - Recommended answer: `generate` only when source recovery is weak, the object is reconstruction-like, and the package can remain explicit about generated delivery.
  - Metadata effect: update `plan_manifest.json`, `metadata.confirmation.generation_routing`, and record an object-scoped formal decision-log entry for every generated-route object.
- `Approximate Reconstruction Acceptance Gate`
  - Pause category: `user-decision`
  - Trigger: background/carrier repair requires inferred pixels or manual redraw.
  - Ask: “Is an approximate reconstructed layer acceptable for this package?”
  - Recommended answer: yes only when the layer can stay `needs-review` or is explicitly accepted for the target use.
  - Metadata effect: keep `delivery_class=approximate-reconstruction`, record `reconstruction_provenance`, `active_reconstruction_method`, `metadata.confirmation.approximate_reconstruction`, and a formal decision-log entry.
  - Required wording before promotion: `This is still approximate because hidden pixels are inferred.`
- `Pilot Object Gate`
  - Pause category: `formal-approval`
  - Trigger: complex UI, dashboard, badge/tile/glyph, or approximate reconstruction work that should not widen without a representative pilot.
  - Ask: “Should I use this representative object as the pilot before broader extraction?”
  - Recommended answer: yes for dense UI or reconstruction-heavy work.
  - Metadata effect: update `metadata.confirmation.pilot_object` and keep the wider batch blocked until the gate is `confirmed` or evidence-backed `not-required`.
- `Final Acceptance Gate`
  - Pause category: `formal-approval`
  - Trigger: the package is about to claim `qa.status=pass`, `visual-acceptance-ready`, or `production-ready`.
  - Ask: “Does the current package meet the requested granularity and cleanliness well enough to mark pass?”
  - Recommended answer: keep `needs-review` unless the current boundaries, cleanliness, and approximations have actually been accepted.
  - Metadata effect: update `metadata.confirmation.final_acceptance` and record a formal decision-log entry.
- `Candidate Promotion Acceptance Gate`
  - Pause category: `formal-approval`
  - Trigger: a candidate is about to replace the current asset revision.
  - Ask: “Should candidate X become the current revision for this object?”
  - Recommended answer: yes only after compare evidence or a direct-promotion rationale exists.
  - Metadata effect: update `selected_candidate_id`, `current_asset_revision`, `repair_history[]`, `candidate_comparisons[]`, `metadata.confirmation.candidate_promotion`, and the QA report.

Carrier/glyph grouping is not a separate gate. It is one decision branch inside `Granularity Alignment Gate`, and should be recorded there rather than creating a fourth decision type.

Medium/high-risk semantic divergence is not a fourth pause class either. It is the reason a branch may require a `user-decision` stop when reuse boundaries, text ownership, approximation truthfulness, or final claims would materially change and prior instructions do not already settle the branch.

When a split decision affects reuse boundaries, editability, animation readiness, localization, approximate reconstruction acceptance, candidate replacement, or final delivery claims, pause and run a one-question confirmation step before continuing that branch.

This is a confirmation-driven workflow, not passive ambiguity handling. Ask one question at a time, include the recommended answer, resolve one branch before moving on, and inspect the source image, metadata, and prior user instructions before asking. Do not batch unrelated questions unless the user explicitly asks for a full alignment round.

`inferred-from-user` means the answer is already supported by durable user evidence such as earlier instructions, approved metadata, or a prior accepted policy. It does not mean the agent guessed what the user probably wants.
Global autonomy instructions do not by themselves satisfy semantic gates. If the branch is being recorded as `inferred-from-user`, the evidence must resolve the exact branch being recorded, including the relevant `resource_family` when semantic narrowing is the question.

Ask when deciding:

- whether a visually connected region should stay grouped or become separate reusable layers
- whether labels, buttons, text, or UI chrome should be extracted as images or rebuilt downstream
- whether uncertain edges, hidden background, or reconstructed pixels can be accepted as `needs-review`
- whether to prefer exact source preservation, editable layers, animation-ready layers, or quick draft assets
- whether a low-confidence automated mask should be retried with another upstream tool or sent to manual review
- whether structurally valid output should remain `needs-review` until the user accepts its cleanliness and granularity
- whether a warning is a true defect, an expected stylistic signal, or mixed and needs human judgment
- whether a `resource_family` choice should narrow the semantic branch inside `Granularity Alignment Gate`

If the answer can be determined from the source image, existing metadata, or user-provided requirements, inspect that evidence first. If ambiguity remains, ask exactly one focused question and wait for the answer before continuing that branch. Progress updates are commentary, not confirmation gates.

Record formal gate outcomes in `metadata.decision_log[]` with `stage`, `pause_category`, `question`, `recommended_answer`, `recorded_answer`, `decision_effect`, `decision_source`, `evidence_ref`, and `blocking`. For the hard workflow gates, also update `metadata.confirmation`, including `candidate_promotion`.

## Reference Routing

- Read `references/workflow.md` for the full staged workflow.
- Read `references/pipeline-recipes.md` before choosing or documenting the extraction path.
- Read `references/default-route-chains.md` before selecting the default provider chain for a resolved route.
- Read `references/provider-contract.md` when you need the provider bridge request/result contract.
- Read `references/shared-task-contract.md` when you need the shared recommendation schema for candidate/provider work items.
- Read `references/grounded-sam-pipeline.md` before accepting or running professional upstream outputs.
- Read `references/ui-atomic-split.md` before planning complex UI, dashboard, badge, tile/glyph, or control-heavy images.
- Read `references/quick-contract.md` for the short package contract view.
- Read `references/asset-package-contract.md` before creating, renaming, or validating files.
- Read `references/qa-standards.md` before claiming an asset is reusable.
- Read `references/manual-review.md` when confidence is low, edges are complex, objects overlap, or background repair is uncertain.
- Read `references/confirmation-prompts.md` when a decision needs user confirmation or should be recorded from prior instructions.

## Output Expectations

At minimum report:

- package path
- source image
- plan manifest path
- provider plan summary path
- provider work-item summary path
- provider chain summary
- provider capability fit summary
- tooling preflight result
- production_capable: true/false
- generation capability result
- missing upstream roles/tools
- user choice: install/activate tools, external professional outputs, or draft-packaging-only
- quality implication of missing tools
- quality target tier and why it is not higher yet
- granularity mode, whether it was user-confirmed or inferred, split scope notes, and whether text/UI chrome is extracted or rebuilt downstream
- object types and the chosen upstream orchestration per type
- confirmation decisions recorded in `metadata.decision_log`
- visual hierarchy and recommended split plan
- extraction pipeline recipe, stages, upstream tools, and quality gates
- planned object routes and route reasoning for generated candidates
- route-required capability tags, selected provider capability tags, expected consume mode, and object-type fit
- provider requests/results written to `_staging/providers/`
- provider result consumer path used
- candidate work-item summary path
- primary segmenter, matting tool, and helper tools
- generation provider class and whether it is production-ready
- asset_class/reuse_status policy used for this run
- object inventory
- generated or collected assets
- previews
- quality preview evidence
- visual quality audit result and warning count
- downstream asset manifest
- validation result: structural package valid or structurally invalid
- visual quality result: pass, needs-review, or blocked
- production-ready assets
- accepted approximate reconstructions
- accepted generated reconstructions
- draft candidate assets
- support-only layers
- QA status: `pass`, `needs-review`, or `blocked`
- manual-review flags and next correction points
