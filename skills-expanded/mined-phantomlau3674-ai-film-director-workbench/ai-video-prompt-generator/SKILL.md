---
name: ai-video-prompt-generator
description: Generate AI video prompts from clean structured prompt specs, validate prompt specs, run an isolated OpenAI-based prompt generator, and lint prompt outputs for viewpoint, action, reference, dialogue, negative prompt, audio prompt, safety tags, and legacy-contamination failures. Use when producing or repairing Flow/Veo/Omni/Runway/Kling/Dreamina-ready shot prompts from project data.
---

# AI Video Prompt Generator

This skill no longer writes final prompts directly inside the Codex chat context.
It consumes a clean `prompt_spec.json`, validates it, calls an isolated LLM
prompt generator, and lints the output.

## Required Reading

Read only what the task needs:

- `references/v2-core-protocol.md` for the generic v2 prompt contract.
- `references/prompt_spec.schema.json` before creating or changing specs.
- `references/output-contract.md` before consuming generator output.
- `references/seedance-provider-prompting.md` when the target provider is
  Dreamina, Seedance, Jimeng, or another Seedance-like multimodal video surface.
- `references/director-dense-seedance-protocol.md` when the requested clip is a
  continuous take, timed multi-beat sequence, dialogue scene, transformation,
  occlusion transition, action tableau, cross-video continuation,
  representation-layer change, or other director-dense prompt.
- `references/asset-duty-handoff.md` when the prompt uses character,
  environment, prop, palette, storyboard, staging, frame, source-video, voice,
  or cadence assets.
- `director_profiles/*.md` only for the selected director profile.

Do not load old project examples, deprecated compatibility rules, or chat
history into the generator. Project-specific examples belong in the movie root,
not inside this generic skill.

## Workflow

1. Build or receive a `prompt_spec.json` from project truth.
   Choose `validation_policy.stage` before adding detail:
   `exploration` for creative discovery, `proof_shot` for a runnable experiment,
   `batch` for repeatable production, or `release` for final delivery. Missing
   creative contracts are warnings in the first two stages and blockers in the
   last two. Legacy specs without this field remain `batch` for compatibility.
   Choose `prompt_density_policy.mode` deliberately:
   `compact_motion` for one controllable event, or `director_dense` for a
   complete timed execution contract. Long output is valid in director-dense
   mode; completeness, not brevity, is the gate.
   Also choose `prompt_density_policy.control_source`:
   `prompt_owned`, `asset_delegated`, `existing_video_delta`, or
   `dialogue_audio`. A compact prompt may carry several inherited beats only
   when approved assets or a source clip own those beats and the spec names
   the inherited and text-owned controls. Do not expand a one-delta edit or
   voice cue into a scene rewrite.
   Treat director contracts as modules, not a form to fill. Use only the
   modules that reduce a real ambiguity or known failure risk for this shot.
   Consume approved asset duties; do not paste upstream character/scene/prop
   generation briefs into the video motion prompt. Canonical asset creation
   remains with `ai-film-production-system`; this skill binds those assets to
   the shot and protects them from cross-duty contamination.
   If `existing_video_delta` or `dialogue_audio` already has an authoritative
   source picture, skip still/storyboard generation. An empty
   `storyboard_prompt` is then correct control allocation, not missing work.
2. Run:

```bash
python scripts/validate_prompt_spec.py path/to/prompt_spec.json
```

3. Only when the shot needs a new still storyboard, keyframe, reference image,
   or start frame, generate the image prompt with the dedicated storyboard
   generator. Skip this step for source-owned picture work:

```bash
python scripts/generate_storyboard_prompt.py \
  --spec path/to/prompt_spec.json \
  --director high_action_physics \
  --output-dir path/to/output
```

Use the resulting `<shot_id>.storyboard_prompt.txt` for image generation. This
stage must not produce `motion_prompt` or `prompt_text`. Before the LLM call,
the generator projects the production spec into still-image truth: a neutral
start frame receives the frozen starting composition, POV geometry, visible
subjects/props, positive style, and reference duties, while action arcs,
background motion, end states, sound, failure lists, and negative policy remain
outside the still prompt. `action_tableau` keeps only its static topology and
causal evidence.

4. For image-to-video, multi-image video, or text-to-video motion, generate the
   video motion prompt with the dedicated motion generator:

```bash
python scripts/generate_motion_prompt.py \
  --spec path/to/prompt_spec.json \
  --director high_action_physics \
  --storyboard-prompt path/to/output/SHOT.storyboard_prompt.json \
  --output-dir path/to/output
```

Use the resulting `<shot_id>.motion_prompt.txt` for video generation. This
stage must not rewrite the still image prompt. Omit `--storyboard-prompt` when
the source video/current frame already owns the picture.

5. For adapters that still need one combined compatibility payload, generate
   prompt output:

```bash
python scripts/generate_prompt.py \
  --spec path/to/prompt_spec.json \
  --director high_action_physics \
  --output-dir path/to/output
```

For Seedance/Dreamina-like providers, `generate_prompt.py` internally uses
separate storyboard and motion LLM passes. Use `--dry-run` for deterministic
local checks without API calls.

6. Lint the combined prompt output:

```bash
python scripts/lint_prompt_output.py \
  --spec path/to/prompt_spec.json \
  --prompt-json path/to/output/SHOT.prompt.json
```

## Environment

`generate_prompt.py` uses the OpenAI SDK:

- `OPENAI_API_KEY` is required unless `--dry-run` is used.
- `PROMPT_LLM_MODEL` is required unless `--model` or `--dry-run` is used.
- `PROMPT_LLM_TEMPERATURE` defaults to `0.6`.
- For OpenAI-compatible providers, pass `--base-url` and `--api-key-env`, or
  pass `--env-file` and use a provider-prefixed model such as
  `volcengine/doubao-seed-2.0-lite`.
- Volcengine Coding Plan defaults to
  `https://ark.cn-beijing.volces.com/api/coding/v3` when the model prefix is
  `volcengine/`, `doubao/`, or `ark/`; it reads `VOLCENGINE_API_KEY`.
- `MODEL_NAME` is accepted as a fallback when `PROMPT_LLM_MODEL` is not set.

## Contract

The generator may use only the spec and selected director profile. It must not:

- invent story beats not present in the spec;
- read movie folders, manifests, skills, or chat history;
- merge multiple smallest events into one prompt;
- turn embodied POV into absent POV;
- omit action arcs, background motion layers, or reference duties that the spec
  supplies.

For `director_dense`, preserve every supplied temporal beat and micro-action
detail. In exploration/proof-shot work, do not invent empty contracts or force
all possible sections. In batch/release work, unresolved required contracts are
blockers. A long prompt is not a failure by itself.

For `asset_delegated`, preserve the storyboard/start-frame/reference pack as
the controlling source and write only the unresolved motion, continuity, or
sound controls. For `existing_video_delta`, name the source video, requested
delta, and preservation rule; do not restage unrequested details. For
`dialogue_audio`, bind line, speaker, voice, delivery, timing, and visible
reaction without inventing unrelated blocking.

For `storyboard_frame_mode: action_tableau`, preserve body orientation,
visible/hidden anatomy, contact/containment, prop state, pose dynamics, causal
traces, environmental motion evidence, narrative read, and interpretation
guards. Do not flatten a partial-body pose into a generic standing/sitting pose.

Codex remains the coordinator: it prepares specs, validates them, calls the
generator, lints the result, and hands approved prompt outputs to production.
Prompt JSON must keep `prompt_text`, `negative_prompt`, `audio_prompt`,
`risk_notes`, `safety_notes`, and `reference_duties` as separate fields.

For Dreamina/Seedance-style providers, prompt output is split:

- `storyboard_prompt` generates still storyboard/reference/start-frame images.
- `motion_prompt` moves that image in video generation.
- `prompt_text` remains a video-provider compatibility field and should equal
  `motion_prompt`.

Do not paste internal rationale, failure taxonomies, or unbounded negative
prompts into provider-facing fields. Director-facing execution sections are
allowed when they directly control or verify the generated clip.
