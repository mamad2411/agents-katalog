---
name: seedance-2-5-director-workbench
description: "Turn stories, scripts, products, characters, locations, reference media, or continuation requests into a managed AI-video production package: visual DNA, versioned assets, character/location/product sheets, keyframes, storyboard boards, cinematic shot design, and paste-ready Seedance 2.5 prompts. Use for Seedance 2.5, Dreamina/Jimeng video direction, Codex image generation for film assets, shot lists, three-view/six-grid/nine-grid boards, asset continuity, video edit/extension, or consented real-person identity consistency routed through PhotoMaker V2, PuLID-FLUX, LivePortrait, or ConsisID."
x-alice-class: assist
---# Seedance 2.5 Director Workbench

Build the project as a small production system, not as one oversized prompt. Separate story diagnosis, reusable assets, per-shot keyframes, deterministic director boards, video-model routing, and final delivery.

## Start Here

1. Inspect the user's story, existing files, reference media, project state, and requested deliverable.
2. Choose an output depth:
   - **Prompt-only**: diagnose and return a paste-ready prompt; do not generate images.
   - **Workshop**: create project state, asset plan, shot list, keyframe prompts, and final job packet.
   - **Production**: generate requested assets with Codex imagegen, register files, compose boards, preflight, and package the result.
   - **Continuation**: load the previous project, preserve locked assets and ending state, and create only newly required assets and shots.
3. Create or load `project.json` with `scripts/project_ops.py` before producing multiple assets or shots.
4. Read only the references needed for the task. Use `references/director-workflow.md` for the end-to-end pipeline.

## Route Identity Before Generating

Set one identity mode:

| Identity mode | Meaning | Default image route | Seedance use |
|---|---|---|---|
| `fictional` | Original fictional character | Codex imagegen | Eligible |
| `synthetic_actor` | Designed, non-real synthetic performer | Codex imagegen | Eligible |
| `consented_local_identity` | User or explicitly authorized recognizable person | PhotoMaker V2; PuLID fallback | Character media stays local |

For `consented_local_identity`:

- Generate identity-consistent stills locally with PhotoMaker V2 or PuLID-FLUX.
- Use LivePortrait for talking-head, blinking, expression, and small head-motion animation.
- Use ConsisID only for requested full identity-preserving local video; mark it as a slow experimental RTX 3060 route.
- If a recognizable face is rejected at Seedance upload, set `seedance_eligible=false`. Preserve the scene, camera, motion, timing, and sound plan; stop resubmitting that identity asset.
- A hybrid shot may use Seedance for identity-independent background/action plates and a local consented-identity post pipeline. Record every source in the asset manifest.

Read `references/identity-pipeline.md` before building a real-person job.

## Use Codex Imagegen Correctly

Invoke the built-in imagegen skill/tool when the user requests actual images. Do not call an image API from these Python scripts.

- New image: generate one distinct asset per tool call.
- Edit: inspect the local image first, then pass it as the explicit edit reference.
- State each reference role: identity, clothing, pose, composition, lighting, location, product geometry, or style.
- Copy every accepted generated file into the project's current asset version and register it with `project_ops.py add-file`.
- Keep machine references clean: no labels, arrows, panel numbers, UI, or explanatory text.
- Add exact labels only in a director board created by `compose_board.py`.
- Select an image quality profile before generation. Machine references use `clean_reference`; cinematic keyframes use `clean_cinematic` unless visible film grain is an explicit art direction.
- Treat rain, fog, dust, sparks, and hologram particles as scene elements with a bounded depth/region. Do not let them become full-frame sensor noise or contaminate faces and flat materials.
- A prompt-only request must remain prompt-only.

Read `references/image-quality-recovery.md` when the request mentions noise, grain, blur, unclear detail, JPEG artifacts, pixelation, mosaic blocks, upscaling, or face restoration.

## Build Assets in Production Order

Use this order unless the user requests a narrower task:

1. Visual DNA, palette, contrast, texture, period, and mood board.
2. Character identity anchor.
3. Character front/side/back three-view.
4. Character 3×2 sheet: front full body, three-quarter, back, waist-up, hands, face.
5. Location five-view or 3×3 environment sheet, including reverse angle.
6. Props/products: geometry views, scale reference, material close-ups, and interaction state.
7. Hero Frame.
8. One independent clean keyframe per shot.
9. Deterministic director storyboard board with exact shot labels and parameters.
10. Seedance or local-identity job packet.

Create only reusable assets that appear in at least three shots, define identity, control continuity, or solve a known generation ambiguity. Read `references/asset-factory.md` for prompts, views, IDs, and versioning.

## Direct the Story Into Shots

Convert internal narration into visible action, eye line, body language, object handling, environment response, lighting change, and sound. Do not translate prose sentence by sentence.

Each shot record should carry:

`shot_id`, `sequence_id`, `duration`, `action`, `dialogue`, `shot_size`, `camera_angle`, `camera_move`, `lens_mm`, `lighting`, `palette`, `transition`, `start_state`, `end_state`, `asset_refs`, `backend`, and inferred `seedance_mode`.

Keep causality and ending state explicit. A continuation starts from the prior ending state; story continuation is not automatically Seedance `video_extension`. Use `video_extension` only when footage must continue directly from a source video's boundary frame.

Read `references/storyboard-language.md`. Search `references/cinematic-style-patterns.md` for the relevant scene type, camera move, lighting pattern, performance beat, dialogue, fight, product, or micro-expression pattern rather than loading the whole library unnecessarily.

## Route Seedance 2.5 Mode

Choose the mode before writing the final prompt:

| Intent | Mode |
|---|---|
| Generate with no media reference | `t2v` |
| Generate from original character/location/keyframe/audio/video references | `omni_reference` |
| Change an existing video while retaining its timeline | `video_edit` |
| Continue before or after an existing video boundary | `video_extension` |

For every reference, declare what to use, fidelity, and what not to copy. Keep the final Seedance job at 4–30 seconds and 720p. `video_edit` inherits source duration/aspect behavior; `video_extension` requires an extension direction and inherits source aspect ratio. Do not invent 4K, genre, or platform-level start/end-image parameters for Seedance 2.5.

Read `references/seedance-2-5-modes.md` and use `references/prompt-templates.md` for the final packet.

## Manage Project State

Common commands:

```powershell
python scripts/project_ops.py init --root <project-dir> --title "Project title" --identity-mode fictional --backend codex_imagegen
python scripts/project_ops.py add-asset --project <project-dir> --type character --name "Lead"
python scripts/project_ops.py add-file --project <project-dir> --id CHR001 --path <generated-image>
python scripts/project_ops.py bump-asset --project <project-dir> --id CHR001 --note "New wardrobe; identity unchanged"
python scripts/project_ops.py add-shot --project <project-dir> --sequence SEQ001 --duration 6 --action "Visible action" --asset CHR001 --asset LOC001
python scripts/project_ops.py validate --project <project-dir>
```

Never overwrite an accepted version. Modify hair, wardrobe, prop, scene, or one shot by bumping only the affected asset and dependent shots. Preserve prompts, source hashes, job state, and failure logs.

## Compose Boards

```powershell
python scripts/compose_board.py --layout three-view --mode machine --input front.png --input side.png --input back.png --output character_machine.png
python scripts/compose_board.py --layout 3x2 --mode director --input 01.png --input 02.png --input 03.png --input 04.png --input 05.png --input 06.png --label "SH001" --label "SH002" --label "SH003" --label "SH004" --label "SH005" --label "SH006" --title "Sequence 01" --output storyboard.png
```

Use at most four storyboard panels per generated storyboard image when an image model is asked to create a board. Prefer independent keyframes and compose the final board with Pillow.

## Run Preflight

Before delivery:

```powershell
python scripts/director_preflight.py --project <project-dir>
python scripts/director_preflight.py --project <project-dir> --json
python scripts/local_identity_adapter.py probe
python scripts/local_identity_adapter.py recommend --task still --reference-count 3
```

Fix all errors. Warnings require a conscious decision. Never claim a generated path, uploaded job, or successful render unless it exists and was verified.

## Deliver

Return, as applicable:

1. Story diagnosis and selected structure.
2. Visual DNA and continuity locks.
3. Asset/role/version map.
4. Shot list with timing and end states.
5. Generated asset paths and director board paths.
6. Paste-ready Seedance 2.5 prompt and parameters.
7. Local PhotoMaker/PuLID/LivePortrait/ConsisID job packet when Seedance is ineligible.
8. Preflight result, unresolved warnings, and exact next command.

## References

- `references/image-quality-recovery.md` — clean-reference/cinematic quality locks, negative prompts, artifact diagnosis, and restoration routing.

- `references/director-workflow.md` — end-to-end execution and failure recovery.
- `references/asset-factory.md` — asset sheets, imagegen prompts, IDs, and dependency rules.
- `references/storyboard-language.md` — shot fields, timing, camera, performance, and continuity.
- `references/seedance-2-5-modes.md` — mode semantics, limits, reference grammar, edit/extension behavior.
- `references/identity-pipeline.md` — consented local identity model matrix, hardware, licensing, and hybrid routing.
- `references/prompt-templates.md` — copy-ready production templates.
- `references/cinematic-style-patterns.md` — large searchable style/prompt pattern library from the supplied skill.
- `references/source-provenance.md` — adopted sources and decisions.
- `references/evaluation-cases.md` — acceptance and regression cases.
