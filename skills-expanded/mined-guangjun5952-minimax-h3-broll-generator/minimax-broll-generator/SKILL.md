---
name: minimax-broll-generator
description: Accept a transcript or talking-head video, optionally transcribe the video into a timestamped transcript, choose v1 simple, v2 rich, or v3 balanced prompt rules, identify semantic beats that need B-roll, match Guangjun T01–T21 packaging templates, request truthful source assets, generate MiniMax-H3 shots after explicit approval, and automatically edit them back onto the source video by timestamp. Use when the user asks to解析口播视频、生成带时间戳逐字稿、拆解口播、规划B-roll、匹配包装模板、选择简洁/丰富/平衡提示词、生成无背景音乐且仅含音效的包装、调用MiniMax-H3、自动剪辑口播配画面或输出成片。
---

# MiniMax-H3 B-roll Generator

Turn a transcript or talking-head video into an approval-gated B-roll production plan and, when a source video is supplied, a timestamp-driven final edit. Preserve the visual grammar of Guangjun's T01–T21 templates and preserve the original spoken audio throughout the final assembly.

## Non-negotiable gate

- Never submit a paid API request before the user has reviewed the shot list and explicitly approved specific shot IDs.
- Never interpret “continue”, “looks good”, silence, or approval of the workflow as approval to generate videos.
- Require all three conditions for a real API call:
  1. The current conversation contains explicit approval for named shot IDs or “all shots”.
  2. `plan.approval.status` and each selected shot's approval status are `approved`.
  3. `scripts/minimax_h3.py` is invoked with `--approved`.
- Never approve or submit a shot while a linked required asset is still marked `missing`.
- API keys must come only from `MINIMAX_API_KEY`. Never store a key in a plan file, prompt, review, manifest, or source code.
- Never let generated B-roll replace, regenerate, or time-stretch the source speech track.
- Every generated shot must forbid music, melody, singing, voice-over, and dialogue. Permit only synchronized foley and restrained environmental sound. If a render contains music, reject it or mute its audio before editing.

## Required references

- Read [prompt-versions.md](references/prompt-versions.md) at the start of every invocation.
- Read [template-routing.md](references/template-routing.md) before classifying or styling shots.
- Read [extended-template-library.md](references/extended-template-library.md) whenever T11–T21 may apply.
- After the user selects a profile, read exactly the matching complexity reference: [template-complexity-v1-simple.md](references/template-complexity-v1-simple.md), [template-complexity-v2.md](references/template-complexity-v2.md), or [template-complexity-v3-balanced.md](references/template-complexity-v3-balanced.md).
- Read [asset-intake.md](references/asset-intake.md) before asking for, recording, or validating external assets.
- Read [prompt-system.md](references/prompt-system.md) before writing prompts.
- Read [plan-schema.md](references/plan-schema.md) before creating or editing a plan.
- Read [minimax-api.md](references/minimax-api.md) before any API operation or troubleshooting.
- Read [video-input-and-editing.md](references/video-input-and-editing.md) whenever the user supplies a talking-head video or requests automatic editing.

## Workflow

### 0. Choose the input mode

- Before asking for the prompt profile, ask whether the user wants to provide `逐字稿` or `口播视频`, unless one is already supplied.
- For a transcript, preserve the existing workflow and never invent timestamps.
- For a talking-head video, inspect the file, then run `scripts/transcribe_video.py` to create a timestamped transcript. Preserve the exact path in `source.video_path` and the transcription artifact in `source.transcript_path`.
- Review obvious transcription uncertainty, product names, English terms, numbers, and named entities with the user before routing. Correcting the transcript resets downstream prompts and approvals.
- Use schema `1.6` for new video-input or automatic-edit projects. Read [video-input-and-editing.md](references/video-input-and-editing.md).

### 1. Ask for the prompt version

- Before segmentation, routing, asset requests, prompt writing, or plan creation, ask the user to choose `v1 简洁清晰`, `v2 丰富动效`, or `v3 平衡清晰（推荐）`.
- Skip the question only when the user already selected one in the same request.
- Do not silently default, infer a choice from an older task, or write all three versions unless explicitly asked for a comparison.
- Record the choice as top-level `prompt_profile` using `v1_simple`, `v2_rich`, or `v3_balanced`. Use schema `1.6` for new plans; schema `1.5` remains valid for legacy transcript-only plans.
- If the user changes versions after prompts exist, rewrite prompts and complexity plans, reset all approvals to `pending`, regenerate the review, and rerun dry-run.

### 2. Segment the transcript

- Split by semantic beat, not punctuation alone.
- Prefer 3–10 second beats. Keep a longer sentence intact when splitting would destroy meaning.
- Preserve the exact transcript text for every segment.
- If timestamps are absent, use ordered segment IDs and leave times `null`; do not invent precise timestamps.
- If timestamps came from the talking-head video, only merge adjacent transcript segments. Set the merged start to the first start and merged end to the last end; never estimate or rewrite timing by reading speed.

### 3. Decide whether a visual is needed

Assign every segment one route:

1. `A_ROLL` — personal judgment, emotional turn, caveat, direct address, or a line whose credibility depends on the speaker.
2. `REAL_EVIDENCE` — product UI, article, paper, source, chart, quotation, logo, or factual proof. Never fabricate these with AIGC.
3. `EXISTING_MEDIA` — a real product/person/place/process already present in the user's library.
4. `HYPERFRAMES` — deterministic typography/evidence/compositing that must be exact, editable, transparent, or tied to real UI.
5. `MINIMAX_H3_PACKAGING` — the beat is best communicated by a complete T01–T21-style text-led editorial motion-graphics shot, with exact approved on-screen words and supporting visual material.
6. `MINIMAX_H3` — physical action, atmosphere, conceptual metaphor, environment, role scene, transition plate, or a clean moving hero subject where text is not the primary information carrier.

Do not force B-roll onto every sentence. A segment needs B-roll only when the visual adds information, clarifies a process, provides proof, establishes context, or creates a necessary pacing reset.

### 4. Route through T01–T21

- Choose one `template_id` or `NONE` for each non-A-roll segment.
- Respect the fallback rules in [template-routing.md](references/template-routing.md).
- First decide the primary information carrier: `TEXT_PACKAGING`, `CINEMATIC_PLATE`, `REAL_EVIDENCE`, or `A_ROLL`.
- Prefer `MINIMAX_H3_PACKAGING` for a hook, central concept, short conclusion, verified number, simple relation, chapter overview, or parallax statement whose meaning would be lost without visible words.
- Use `MINIMAX_H3` only when action, place, object, atmosphere, or spatial behavior carries the meaning without typography.
- Keep brand marks, quotations, citations, product UI, long evidence, exact charts, and true-alpha overlays in Hyperframes or real capture.

### 5. Audit and request assets

- Inspect all user-supplied files and known library paths before asking for anything.
- For every non-A-roll segment, identify whether it needs a talking-head plate, product video/image, UI recording, logo, evidence document, reference image, portrait, map data, timeline data, diagram topology, technical specifications, font, brand guide, or background plate.
- Add every needed item to top-level `asset_requests` using [plan-schema.md](references/plan-schema.md).
- Group missing requests into required blockers and optional fidelity improvements. Ask once, concisely, with the affected segment/shot, reason, and acceptable format.
- Never use MiniMax-H3 to fabricate a missing proof source, real product result, UI, logo, historical portrait, location claim, chronology, or technical relationship.
- If the user explicitly waives a required asset, change the concept to an obvious metaphor and require AIGC disclosure.

### 6. Write the generation prompt

- Write one continuous shot per generated clip; do not describe a montage.
- Apply the selected profile's phase, element, text, motion, camera, noise, and reading-hold budgets from [prompt-versions.md](references/prompt-versions.md).
- Describe subject, action, environment, composition, depth, camera path, lighting, materials, color, timing, and end state.
- Use at most three compatible camera instructions.
- For `cinematic_plate`, create clean negative space and explicitly forbid readable text.
- For `motion_graphics` or `hybrid_packaging`, declare the exact `on_screen_text`, hierarchy, position, font appearance, tracking, line height, colors, material layers, text entrance, profile-specific reading hold, camera curve, and end state. Explicitly forbid every other word and every glyph-like background texture.
- Keep H3 typography within the selected profile's text budget. Otherwise split the shot, generate a no-text plate, or route to Hyperframes.
- Never ask H3 to invent supporting copy. All visible wording must come from the transcript or user-approved structured data.
- When a supplied image is essential to composition or identity, prefer `image_to_video` and link its asset request; do not substitute a text-only approximation.
- When public reference video, audio, or image URLs are essential, use `multimodal_to_video` with `reference_media`; keep identity-critical real assets out of text-only approximation.
- Keep the final API prompt under 2000 characters.
- For `MiniMax-H3` v2, default to 16:9, 2K, 6 seconds unless the user changes the production settings. V2 accepts only 768P or 2K.
- End every generated-shot prompt with an audio contract that allows only specific synchronized foley and restrained environmental sound. Explicitly forbid background music, melody, beat, singing, speech, dialogue, and voice-over.
- Add `audio_design.music: false`, `audio_design.dialogue: false`, a non-empty `audio_design.sfx` list, and `audio_design.generated_audio: "sfx_only"` to every shot.

### 7. Create the approval artifacts

Create both:

- `broll-plan.json` following [plan-schema.md](references/plan-schema.md).
- `broll-review.md` generated by the review tool.

Validate and render the review:

```bash
python3 scripts/plan_tool.py validate broll-plan.json
python3 scripts/plan_tool.py review broll-plan.json --output broll-review.md
```

Show the user the recommended route, reason, prompt, mode, duration, resolution, and estimated number of paid generations. Stop and wait for approval.

### 8. Record explicit approval

Only after the user explicitly approves named shots, run:

```bash
python3 scripts/plan_tool.py approve broll-plan.json \
  --shots B001,B003 \
  --confirmation CONFIRM_MINIMAX_H3_COST
```

Use `--shots all` only when the user explicitly approves all generatable shots. Re-run `review` and show the approved subset before submission when approval wording is ambiguous.

### 9. Dry-run before spending

Always inspect the exact outgoing payloads first:

```bash
python3 scripts/minimax_h3.py broll-plan.json \
  --output-dir generated-broll \
  --dry-run
```

Dry-run does not require an API key and never accesses the network.

### 10. Generate approved videos

After the dry-run is correct and the approval remains valid:

```bash
python3 scripts/minimax_h3.py broll-plan.json \
  --output-dir generated-broll \
  --approved
```

The script submits sequentially, polls task status, downloads results, and writes `generation-manifest.json`. `MiniMax-H3` uses v2; non-H3 legacy models retain the v1 path. Report failures without silently retrying a different model or changing prompts.

### 11. Inspect and assemble the final edit

- Visually inspect every generated shot for text, continuity, flicker, and unwanted music before assembly. A render containing music fails the `sfx_only` contract.
- For a talking-head project, run `scripts/assemble_edit.py` only after all selected shots have downloaded and passed review.
- Use the segment `start_sec` and `end_sec` values as the only edit timing source. Default to `fullscreen_replace`; keep `A_ROLL` segments untouched.
- Preserve the original talking-head audio at full level. Mix only approved B-roll foley/environment at the plan's low SFX gain. Never use generated dialogue or music.
- If a shot's audio is uncertain, pass `--generated-audio mute`; the final edit will keep the original speech without that shot's sound effects.
- Export the final MP4 and `edit-manifest.json`. Verify duration, audio presence, frame size, and that every inserted shot matches its approved time range.

## Quality rules

- Enforce the selected profile mechanically through schema `1.6` for new plans; never mix v1 text limits with v2 motion density or label a v2 plan as v3.
- All profiles keep one primary semantic focus, exact text whitelisting, a stable reading end state, and deterministic fallback for brand/evidence-critical text.
- High-density templates should use a deliberately composed image-to-video first frame or supplied real media whenever identity, evidence, or layout matters.
- Favor editorial paper, dark archive, real material texture, controlled red annotation, and restrained blue accents.
- Keep the reading zone stable. Avoid constant rotation, elastic camera motion, and linear robotic pans.
- Use continuous eased camera movement and layered depth for T09-derived shots.
- Do not add decorative English, fake parameters, fake research, fake product screens, or meaningless microcopy.
- A text-led shot must contain at least one exact on-screen phrase and keep it sharp, near-front-facing, high contrast, and still enough to read for at least 1.2 seconds.
- MiniMax-H3 cannot guarantee exact local font files or error-free Chinese glyphs. Mark typography shots for text QA; reject and regenerate misspelled, duplicated, or invented words. Use Hyperframes when exact text is legally, factually, or brand-critical.
- Do not generate identifiable people without appropriate permission.
- Flag any shot that could be mistaken for documentary evidence as `aigc_disclosure_required: true`.

## Failure handling

- If `MiniMax-H3` is rejected by the endpoint, stop and show the exact API response. Do not automatically substitute another model.
- If H3 rejects a TokenPlan/Credit key, require a pay-as-you-go interface key with H3 access before retrying.
- Override only when the user supplies a valid replacement: `MINIMAX_VIDEO_MODEL` or plan-level `api.model`.
- If a task fails moderation, preserve the failed task record and ask the user before materially changing the concept.
- If the download URL expires, retrieve the file metadata again using the existing `file_id`; do not regenerate the video.
