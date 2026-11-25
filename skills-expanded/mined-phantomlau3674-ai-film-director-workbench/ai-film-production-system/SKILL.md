---
name: ai-film-production-system
description: Project-level production control for AI short films and case-informed AI drama pipelines using the v2 generic film protocol. Use when working with a movie root, project state, constraints, task queues, character/scene/prop bibles, shot plans, prompt specs, assets, manifests, provider batches, Dreamina/Seedance-style batches, review trackers, scorecards, timelines, FFmpeg export packages, playlists, AI drama production gates, and final releases. Do not use for isolated prompt writing, pure creative brainstorming, external provider execution, or live generation control.
---

# AI Film Production System

This skill owns project truth and production gates. It does not write final AI
video prompts in chat. Final prompt text comes from the isolated
`ai-video-prompt-generator` LLM generator.

## Required Reading

- `references/v2-production-protocol.md` before changing project state.
- `references/manifest-contract.md` before editing manifests.
- `references/theory/README.md` before changing film-theory production
  diagnostics, review checks, or theory-linked failure taxonomy.
- `references/ai-drama-production-hypotheses.md` before designing,
  optimizing, or gating Douyin-style AI dramas, AI microdramas, AI
  manju/manhua-video, serial AI shorts, or public-case methodology migrations.
- `references/director-dense-prompt-production-method.md` before approving
  complete timed prompts with micro-actions, camera geometry, visibility,
  continuity, transition, dialogue, sound, static action-tableau, cross-video
  handoff, representation-layer, or semantic-color contracts.
- `references/storyboard-blender-seedance-workflow.md` before designing or
  reviewing storyboard-board, Blender/blockout previs, first/last-frame,
  control-pass, camera-path, or Seedance/Dreamina/Jimeng-style workflows.
- `references/director-grade-asset-workflow.md` before planning a multi-shot
  film's character plates, environment plates, scene director packs, shot
  control packs, or multimodal provider selections.
- `references/asset-prompt-authoring-method.md` before writing or reviewing
  prompts for character, costume, environment, prop, creature, vehicle,
  palette, storyboard, staging-map, start/end-frame, or static action-key
  assets.
- `templates/manifest.schema.json`, `templates/assets.schema.json`,
  `templates/constraints.schema.json`, `templates/shot_plan.schema.json`, and
  bible/provider schemas when changing validators.

## Project Contract

One movie root contains:

```text
_project/
  PROJECT.yaml
  CURRENT.yaml
  manifests/
  decisions/
  audits/
  constraints/
    film_theory_contract.default.json
    scorecard_theory_rules.default.json
  episode-plans/
  task-board/
  failure-taxonomy/
  providers/
01_script/
  shot_plans/
02_assets/
  refs/
  registry/
    assets.jsonl
    audio_assets.jsonl
  bibles/
    characters/
    scenes/
    props/
  audio/
  subtitles/
03_prompts/
  specs/
  generated/
  preflight/
  lint/
04_jobs/
  dreamina/runs/
  providers/runs/
05_review/
  trackers/
  diagnostics/
  scorecards/
06_edit/
  playlists/
  timelines/
  releases/
  exports/
99_archive/
```

## v2 Workflow

1. Apply the asset necessity gate, then register only justified assets with
   exact duties. Every registered asset needs a named production job and at
   least one consumer (`used_by`) or reuse scope. Do not scaffold every asset
   family for an exploratory or quiet shot:

```bash
python scripts/register_asset.py C:/movie/film-root \
  --path 02_assets/refs/scenes/example.png \
  --asset-type scene \
  --asset-kind environment_master \
  --priority primary \
  --visual-duty environment_geography \
  --role "Recurring location master" \
  --production-job "Lock connected-room geography, scale, materials, and motivated light" \
  --must-lock "entrances, exits, walkable paths, material zones" \
  --must-not-lock "shot-specific cast blocking, storyboard arrows, final camera path" \
  --reuse-scope "SCENE_04 all shots"
```

2. Parse script text into an episode-plan scaffold when the task starts from a
   script file:

```bash
python scripts/build_episode_plan.py C:/movie/film-root \
  --script 01_script/script.md \
  --output _project/episode-plans/episode_plan.json \
  --set-current
```

3. Capture constraints, task queue, and bibles before shot specs
   when the task starts from script or outline.

   For theory-informed projects, record the film-theory contract as production
   intent, not as art-school compliance. It may define reality mode, image
   regime, genre promise, spectator-position audit policy, and waivable
   diagnostic gates.

   For case-informed AI drama projects, record the scene or episode promise,
   first visible tension, continuity engine, anchor duties, final
   hold/handoff, differentiation note, and platform-risk notes as project truth
   before prompt generation.

   For storyboard/Blender/Seedance workflows, register storyboard frames,
   blockout videos, control passes, camera metadata, and reference media duties
   before prompt generation. Treat Blender/previs as a control source, not as
   story truth.

   Also name the complexity owner: `prompt_owned`, `asset_delegated`,
   `existing_video_delta`, or `dialogue_audio`. Long text is appropriate when
   text owns multi-beat execution. Compact text is appropriate only when an
   approved asset or source clip owns the omitted detail.

   When assets must be created, author each asset from its downstream
   production question. Record `must_lock`, `must_not_lock`, reuse scope,
   invariants, and consumer shots. Character sheets, environment masters,
   staging maps, prop sheets, palettes, storyboards, and clean start/end frames
   are different control sources; do not ask one decorative image to replace
   all of them.

4. Build a shot-plan scaffold when the user has not already split shots:

```bash
python scripts/build_shot_plan.py C:/movie/film-root \
  --episode-plan _project/episode-plans/episode_plan.json \
  --output 01_script/shot_plans/shot_plan.json \
  --set-current
```

5. Track async work in the task queue:

```bash
python scripts/manage_tasks.py add C:/movie/film-root \
  --layer prompt --title "Generate prompt for SHOT001"
python scripts/manage_tasks.py next C:/movie/film-root --layer prompt
```

6. Validate project layers and prompt specs:

```bash
python scripts/validate_project_layers.py C:/movie/film-root
python scripts/validate_preflight.py C:/movie/film-root \
  --spec 03_prompts/specs/SHOT.prompt_spec.json
```

7. Generate prompt output with `ai-video-prompt-generator`.

8. Build or update a manifest row pointing to:

- `shot_spec_path`
- `prompt_output_path`
- registered `reference_images`
- provider, generation, audio/subtitle, and review state

9. Prepare a provider-neutral or Dreamina batch only after preflight passes:

```bash
python scripts/prepare_provider_batch.py C:/movie/film-root \
  --manifest _project/manifests/manifest_v2.jsonl \
  --batch-id YYYYMMDD-HHMMSS_batch

python scripts/prepare_dreamina_batch.py C:/movie/film-root \
  --manifest _project/manifests/manifest_v2.jsonl \
  --batch-id YYYYMMDD-HHMMSS_batch \
  --slots SHOT001
```

10. Build timeline/export packages only from reviewed clips:

```bash
python scripts/build_timeline.py C:/movie/film-root \
  --manifest _project/manifests/manifest_v2.jsonl \
  --timeline-id rough_cut
python scripts/prepare_ffmpeg_export.py C:/movie/film-root \
  --timeline 06_edit/timelines/rough_cut.json \
  --export-id rough_cut
```

## Gates

Set the project or prompt validation stage explicitly. During `exploration` and
`proof_shot`, the director contracts below are modular guidance and unresolved
items are warnings unless they make the request unsafe or structurally invalid.
During `batch` and `release`, relevant unresolved items become blockers. Do not
require a contract that has no bearing on the shot's actual ambiguity or risk.

- No prompt spec: do not generate.
- Invalid prompt spec: do not generate.
- Missing reference asset registration: do not batch.
- Missing or malformed constraints, episode plan, provider profile, task board,
  or bibles: fix the project layer before production.
- High-motion batch/release spec without `action_arc`: do not generate.
- Crowd/battle/sports/dance/mount spec without `background_motion_layers`: do
  not generate.
- High-motion spec without start/end/action reference or waiver: do not
  generate.
- Missing editability contract: warn during exploration/proof; block batch and
  release.
- Case-informed AI drama without scene/episode promise, first visible tension,
  continuity engine for multi-shot work, anchor duties, or platform-risk note:
  do not batch beyond isolated proof shots.
- Public-case methodology without source date, provenance level, and skin
  removal: do not promote it to reusable skill guidance.
- Public-case methodology without failed-sample comparison: do not describe it
  as a formula, rule, or causal explanation.
- Director-dense prompt without contiguous time coverage and complete
  micro-action chains: do not batch.
- Compact multi-beat prompt without an approved controlling storyboard,
  start/end-frame pack, reference pack, source video, or explicit complexity
  owner: do not batch.
- Director-dense prompt with continuous-take/cut, allowed/forbidden camera,
  visibility/reveal, music/silence, or reference-usage conflicts: surface the
  conflict during exploration; resolve or waive it before batch generation.
- Do not reject a director-dense prompt merely because it is long. Reject it
  when clauses have no control duty, required local actions are missing, or the
  prompt is physically contradictory.
- Do not treat a provider `SUCCESS` status as creative acceptance. Record
  review, instruction adherence, artifacts, editability, and repair history.
- Do not turn lexical keyword collisions or unverified metadata-field
  differences into hard failures without scope and product-semantics review.
- Provider submission over a verified model/version capacity limit: compile a
  shorter provider prompt from the saved director contract before submission;
  preserve state chains, camera landing, reference duties, and handoff.
- Action-tableau storyboard with ambiguous visible/hidden anatomy, unsupported
  containment/contact, or no visible causal/environmental evidence: do not use
  as a start frame.
- Multi-shot clip that changes physical/inverted/stylized/schematic/media layer
  without a representation-layer contract, or continues a prior clip without
  an explicit handoff contract: do not batch.
- New prompt or Blender/previs workflow without saved run evidence: mark it
  experimental and do not use it as a batch gate.
- Complex action, multi-person blocking, or camera-path-dependent shots without
  `visual_staging_contract`, registered control media, or an explicit waiver:
  do not batch.
- Blender/previs requested only for "cinematic feeling" without a control duty:
  do not add Blender work.
- Prompt output not linted: do not submit to Dreamina.
- Cancelled task: do not resume without an explicit `manage_tasks.py resume`.
- Review not accepted: do not enter final release.

## Film Theory Layer

Film theory is used as a production diagnostic layer:

- episode plans may record narrative design, scene turn, knowledge delta, and
  causal links;
- shot plans may record viewer question/answer, camera motivation, visual axis,
  blocking, edit contract, sound contract, and AI risk mitigation;
- scorecards may include observable theory-linked checks;
- failure taxonomy may link symptoms to theory cards and repair actions.
- AI drama diagnostics may record visible tension, promise payoff,
  continuity-engine health, anchor-duty completeness, final hold/handoff
  legibility, differentiation from trend skin, and platform risk.

Do not turn theory into a universal hard gate. Hard stops belong to production
truth: invalid schemas, missing assets, missing bibles under strict mode,
broken identity, broken action causality, missing editability, unsafe or
unlicensed release context, and rejected review. Theory guidance should usually
be warning-level, review-level, or waived with an explicit project reason.

## Responsibility Split

- This skill owns project files, assets, manifests, gates, batches, review
  status, scorecards, timelines, playlists, releases, and film-theory production
  diagnostics.
- `ai-video-prompt-generator` owns prompt spec validation, isolated LLM prompt
  generation, and prompt-output linting.
- `dreamina-cli` owns external generation, query, download, credits, and run
  ledgers.
