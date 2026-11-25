---
name: unrealmotion
description: Create silent motion-graphics explainers from a prompt through ImageGen references, actual Three.js reconstruction, causal motion and deterministic MP4 rendering. Use for process explainers, cutaways, reassembly, product films, kinetic typography and data visualization; not for footage-only editing.
---

# UnrealMotion

Deliver a playable MP4 and the scene source from the user's prompt. The active coding agent is the creative engine; the bundled scripts retrieve references, serve the scene, capture frames, and encode video. No separate language model, API key, or paid video service is needed. This is Three.js, not Unreal Engine.

Resolve `<skill>` to the directory containing this file; run package commands there. Use a new `<project>` directory for each production, preserving prior work. If dependencies are missing: `npm ci` and `npx playwright install chromium`. Check `node <skill>/scripts/unrealmotion.mjs doctor`. Node 22+, Python 3.10+, FFmpeg and ffprobe are required; Python packages are needed only to retrieve full dataset code.

## From prompt to film

1. Infer subject, action, intended message, language, duration, format, and realism from the request. **For explainers, read [imagegen-threejs.md](references/imagegen-threejs.md) and [explainers.md](references/explainers.md). Use ImageGen → real Three.js model → silent video**, starting with `--mode explainer`: default 60 seconds, 1080×1920, 30 fps. Keep the established simple pastel cutaway style unless the user explicitly changes it. The prompt determines the subject, model, story and motion recipe; a bundled demo is not default content. Short showcases retain 12 seconds, 1920×1080 at 60 fps. Honor requested formats and assets. Proceed with reasonable assumptions; no required template/approval questionnaire.
2. Read [art-direction.md](references/art-direction.md) and [motion-library.md](references/motion-library.md). For new explainers, read [dynamic-story.md](references/dynamic-story.md): read [continuous-camera.md](references/continuous-camera.md) and use a connected world with an actual continuous 3D camera route, calm readable pacing and 2–4 consistent ImageGen references for distinct explanatory contexts. Read [text-motion.md](references/text-motion.md) for dynamic copy and [data-motion.md](references/data-motion.md) when quantities help the explanation. Choose a scene foundation and motion profile, then author a compact `plan.json`: identity-defining geometry, material palette, shot timings, subject actions, camera trajectory, transitions, local assets and provenance. An adjective such as “realistic” needs concrete evidence: proportions, surface response, contact, coherent light, and motion.
3. Search the bundled **4,146-entry HF catalog**, using English subject/material/mechanism terms. Read [dataset.md](references/dataset.md) to retrieve 1–3 relevant code examples when structural detail would help. Inspect actual HTML/JS construction, not only titles. Cite scene ids in `plan.json`. Do not copy reasoning traces. The dataset is a reference corpus, not a trained or fine-tuned model.
   For industrial/object assets with limited storage, read [simready-imagegen.md](references/simready-imagegen.md): search the 2,677-entry NVIDIA metadata catalog and retrieve only a relevant budgeted thumbnail/license. This feeds ImageGen appearance references and original mesh reconstruction; never download the whole USD/texture corpus. For teardown/reassembly, also read [reassembly.md](references/reassembly.md).
4. Create the project. For an explainer, **generate and inspect the prompt-specific ImageGen reference bundle, specify stable named parts in `reconstruction.json`, and build actual Three.js volumes in `model.mjs`**. Save exact prompts/provenance in `asset-plan.json`. Author `storyboard.json` with the question, causal progression, per-beat action/copy, 3D camera and resolution. Retain one mesh hierarchy per physical object through cutaways, reassembly and operation; use persistent named scene roots for connected contexts, with world placements and a continuous `cameraPath`. Bind every beat to its actual reference IDs. No raster-plane/cropped-image substitute. For showcases, author `scene.mjs` directly. The CLI is an authoring starter, not a semantic prompt interpreter; a changed title over an unrelated model is not completion.
5. Preview, scrub, run QA, and inspect representative frames at native resolution. Follow [quality.md](references/quality.md): check fidelity, mechanics/anatomy, materials, framing, copy, transitions and meaningful motion in the latter half. Correct failures and repeat the affected checks. Record a truthful `review.json`, tied to the source hash.
6. Render with `--final`, verify metadata, and deliver the MP4, editable project and concise verification note. A request for a finished film authorizes local export. If the user requests only a preview, deliver that instead. Do not substitute source HTML or a contact sheet for a requested video.

## Local commands

```sh
node <skill>/scripts/unrealmotion.mjs templates
node <skill>/scripts/unrealmotion.mjs create <project> --prompt "Film kamera titanium, lensa merakit presisi" --template optical-studio --motion precision-assembly
# Author project/scene.mjs, project/project.json and project/plan.json for the brief.
node <skill>/scripts/unrealmotion.mjs preview <project>
node <skill>/scripts/unrealmotion.mjs qa <project>
# Inspect output/qa/contact-sheet.png AND native-resolution frame PNGs, then write review.json.
node <skill>/scripts/unrealmotion.mjs render <project> --final
node <skill>/scripts/unrealmotion.mjs probe <project>/output/video.mp4
```

`--width`, `--height`, `--duration`, `--fps`, `--supersample` are creation options. New explainers use version 2 stories with `--pace calm --assets multi`; choose `--pace dynamic` or `--assets single` when the brief warrants it. Existing version 1 projects remain supported. Use `--output <new.mp4>` to preserve an export; `--force` replaces an explicitly chosen output. An optional `--audio <local.wav>` pads/trims a supplied audio track to the video. Do not add synthetic narration or music unless requested. Preview prints a loopback URL with play/pause and frame scrubbing; it is not a public deployment.

The default explainer foundation is `imagegen-explainer`: prompt-specific reference → Three.js model → story → video. `water-system-explainer` is the earlier SVG motion study only. Showcase foundations are `optical-studio`, `architectural-light`, `kinetic-editorial`, `pelagic-bloom`, and `mechanical-reassembly`. Showcase camera profiles: `cinematic-orbit`, `precision-assembly`, `macro-dolly`, `continuous-flow`, `editorial-spring`. Explainers choose follow-the-flow, cutaway operation, reassembly, threshold/response or comparison motion with an authored camera path. Recipes do not change the established style. See [motion-library.md](references/motion-library.md).

## Non-negotiable production properties

- Every visible state derives from requested frame/time, including shaders, particles, rig poses, material changes and copy. Preserve `createScene(config) → {update(seconds, normalizedTime), draw(), inspect()}`; see [runtime.md](references/runtime.md). No cumulative rotations, physics stepping, random sampling during updates, or real-time screen recording for final delivery.
- Keep local assets, pinned packages, seeded scene generation, one color pipeline, consistent physical scale and stable object identities. The renderer blocks external requests. Load models, textures and fonts before readiness; missing assets are failures.
- Model actual volumes and attachments. Use bevels, coherent parts, correct pivots, justified roughness/metalness, soft contact shadows and controlled reflections. Render transparent surfaces carefully. A pile of primitives, stick anatomy, floating pieces, broken rigs, or a rotating generic object does not satisfy a detailed brief.
- For photoreal humans, animals, branded objects, or likeness-critical scenes, use appropriate licensed/user-supplied models, textures, and rigged assets when procedural geometry cannot meet the brief. Record source/license. Inspect attachment, joints, silhouette, contact and occlusion throughout the action. Do not quietly replace realism with simple geometric actors. State any material fidelity limit plainly.
- Subject action must carry the story: mechanisms operate, material flows, parts assemble, structure unfolds, or information transforms. Camera orbit and drifting particles alone are insufficient. Avoid rigid constant-speed transforms; use acceleration, follow-through, stagger where motivated, and velocity-continuous camera paths.
- An explainer must answer its question through a complete visual sequence. Longer duration, extra captions and a showcase reel do not replace cause/effect, readable explanation, an appropriate illustration/model and coherent scene handoffs. Honor silent requests; do not add audio setup.
- Match reference complexity and style. Prefer simple coherent geometry, pastel surfaces and clear cutaways for this workflow; do not invent a new art direction or add decorative detail. ImageGen guides appearance; it does not recover hidden CAD, exact dimensions or NVIDIA simulation metadata.
- Automated QA checks technical properties. It does **not** certify beauty, photorealism, accurate anatomy, or physical correctness. Mark visual checks passed only after inspecting their evidence. Report what was actually tested.

## Optional existing engines

Default to the included Three.js renderer. For a user's existing Remotion or HyperFrames project, read [engine-interop.md](references/engine-interop.md) and retain its native frame/seek contract. Their runtimes are optional, independently licensed, and not bundled or tested merely by mentioning them. The source studies behind this skill, exact revisions, and licensing distinctions are in [source-study.md](references/source-study.md).
