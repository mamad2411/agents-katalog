---
name: minimax-video-series
description: Generate, direct, edit, review, resume, verify, assemble, and publish local image-to-video stories with ComfyUI MiniMax H3 and the Qwen3-VL Heretic INT8 encoder. Use for single image-to-video clips, exact-last-frame continuation series, long chaptered video projects, rerenders and sequence editing, continuity/self-review, contact sheets and manifests, combined masters, web encodes, or updates to the Unquiet Archive site.
---

# MiniMax Video Series

Use the installed MiniMax H3 ComfyUI pipeline as a supervised, resumable production system. Treat every generated chapter as a pending take until it passes visual review. Never propagate a rejected final frame.

For supplied-song music videos, exact audio preservation, vocal lip-sync direction, or RIFE delivery, also use `$minimax-h3-native-audio-music-video`. Its Ref2VA/native-audio graph is different from this skill's standard FL2VA generation graph.

For Director timelines, whole-shot previews, local range retakes, or controlled Spectrum acceleration A/B tests, also use `$minimax-h3-director-suite`. Keep its experimental sampler results separate from accepted native continuity takes until they pass review.

## Load only what the task needs

- Read [references/configuration.md](references/configuration.md) before creating or changing a series config.
- Read [references/official-h3-workflow.md](references/official-h3-workflow.md) when choosing T2VA, I2VA, FL2VA, or L2VA, or when changing runtime profiles.
- Read [references/minimax-h3-official-prompt-contract.md](references/minimax-h3-official-prompt-contract.md) before writing timed shots, camera moves, dialogue, singing, voiceover, visible text, or generated audio.
- Read [references/direction-and-review.md](references/direction-and-review.md) when planning prompts, transitions, identity locks, or evaluating a take.
- Read [references/archive-site.md](references/archive-site.md) only when staging or publishing the archive site.

## Known local installation

- ComfyUI: `C:\Users\Admin\ComfyUI`
- API: `http://127.0.0.1:8188`
- GPU baseline: RTX 5090 32 GB; default working format is 640 x 800, 362 frames, 24 fps, 20 steps.
- Archive source: `C:\Users\Admin\minimax-video-gallery`
- Current production reference: `C:\Users\Admin\ComfyUI\generate_unquiet_series_30.py`
- Current output: `C:\Users\Admin\ComfyUI\output\video\unquiet-series`

Do not assume the server, models, paths, GPU state, or prompt schema are unchanged. Run prompt lint and preflight first.

## Core workflow

### 1. Inspect and preflight

Copy [assets/series.example.json](assets/series.example.json) into the project area and customize it. Resolve the frame grid, lint every prompt, and inspect the exact compiled text before rendering:

```powershell
python "$env:USERPROFILE\.codex\skills\minimax-video-series\scripts\h3_prompt.py" profile --duration 15 --aspect 4:5 --quality preview
python "$env:USERPROFILE\.codex\skills\minimax-video-series\scripts\h3_prompt.py" lint --config C:\path\series.json
python "$env:USERPROFILE\.codex\skills\minimax-video-series\scripts\h3_prompt.py" compile --config C:\path\series.json --chapter 1
```

Then run:

```powershell
python "$env:USERPROFILE\.codex\skills\minimax-video-series\scripts\series_pipeline.py" preflight --config C:\path\series.json
```

If ComfyUI is unavailable, inspect the existing process and installation before starting it. Start the known local server from the ComfyUI directory with the existing arguments; do not reinstall working components casually. Verify the required model files and node classes rather than trusting filenames alone.

### 2. Direct the complete sequence before rendering

Write a chapter beat for every 15-second unit. Give each chapter:

- one narrative change;
- one principal physical action;
- at most one secondary environmental reaction;
- a motivated transition or clean final tableau;
- a final 12–15-frame near-still hold;
- audio ambience with no intelligible dialogue unless requested.

Prefer structured `shots` when using multiple cuts, camera grammar, dialogue, singing, voiceover, or visible text. Keep chapter titles, movement labels, review notes, and other manifest metadata out of the generated prompt. The compiler emits only visible or audible direction using the official three-field contract.

Use T2VA or L2VA only for the first standalone/prequel chapter. Default continuation chapters to I2VA; select FL2VA only when a deliberate compatible `last_frame` is supplied.

For longer stories, group 5–10 chapters into movements with a dramatic question, reversal, and end condition. Keep the identity/style lock global; put only the changing action in chapter prompts.

When continuing a legacy series whose old manifest predates this skill, establish the external boundary before the first new render:

```powershell
python "$env:USERPROFILE\.codex\skills\minimax-video-series\scripts\series_pipeline.py" bootstrap --config C:\path\chapters-41-45.json --source-video C:\path\chapter-40.mp4 --source-chapter 40
```

This extracts the configured final frame into the new config's `initial_frame` and records the source video, frame index, and SHA-256 provenance. Do not call Chapter 41 a verified continuation without this record.
Bootstrap refuses a nonadjacent source chapter or an existing different initial frame. Use its explicit override flags only after inspecting the collision.

### 3. Render one chapter

```powershell
python "$env:USERPROFILE\.codex\skills\minimax-video-series\scripts\series_pipeline.py" render --config C:\path\series.json --chapter 1
```

The command records a pending take and creates a versioned six-frame review sheet. It does not unlock the next chapter.

### 4. Self-review before continuation

Open the review sheet with the local image viewer and inspect the video itself when motion or audio is ambiguous. Apply the rubric in [references/direction-and-review.md](references/direction-and-review.md). State the concrete evidence for acceptance or rejection.

Accept only when the opening inherits the source image, identity and anatomy remain stable, the requested action and camera grammar read correctly, requested cuts occur at plausible times, style remains coherent, audio behavior matches the compiled fields, and the final frame is usable as the next shot.

Accept and extract the exact continuation frame:

```powershell
python "$env:USERPROFILE\.codex\skills\minimax-video-series\scripts\series_pipeline.py" accept --config C:\path\series.json --chapter 1 --notes "Stable identity; clean bark wipe."
```

Reject nondestructively and rerender with a revised prompt or seed:

```powershell
python "$env:USERPROFILE\.codex\skills\minimax-video-series\scripts\series_pipeline.py" reject --config C:\path\series.json --chapter 1 --reason "identity drift"
```

Rejected files go to `rejects/`; do not delete them. Change one high-impact variable at a time: first tighten framing/exclusions, then action count, then seed.

### 5. Continue and checkpoint

Repeat render → inspect → accept/reject chapter by chapter. Every five chapters:

```powershell
python "$env:USERPROFILE\.codex\skills\minimax-video-series\scripts\series_pipeline.py" contact-sheet --config C:\path\series.json --from 1 --to 5
python "$env:USERPROFILE\.codex\skills\minimax-video-series\scripts\series_pipeline.py" verify --config C:\path\series.json
```

Review the movement-level sheet for repeated camera grammar, pacing plateaus, color/identity drift, and escalation. Revise future prompts without rewriting accepted history unless the user asks.

### 6. Assemble and edit nondestructively

Concatenate accepted chapters without recompression:

```powershell
python "$env:USERPROFILE\.codex\skills\minimax-video-series\scripts\series_pipeline.py" concat --config C:\path\series.json --from 1 --to 10 --output C:\path\movement-01.mp4
```

Use chapter replacement, ordering, range masters, and playlist structure as the primary edit. Avoid adding crossfades between exact-frame continuations; the in-shot transition is already the edit. Use a hard cut only for a deliberate time/place rupture.

Create a constrained web copy only when a single file is actually needed:

```powershell
python "$env:USERPROFILE\.codex\skills\minimax-video-series\scripts\series_pipeline.py" web-encode --input C:\path\master.mp4 --output C:\path\master-web.mp4 --max-bytes 24500000
```

Prefer an individual-file playlist for long series. Do not crush a ten-minute master below the archive limit when a seamless playlist preserves much better quality.

### 7. Verify delivery

Run `verify` after all accepts and after any replacement. Require:

- expected chapter count and accepted state;
- H.264 video, AAC stereo audio, configured dimensions and frame rate;
- duration close to `length / fps`;
- exact SHA-256 matches for every stored final-frame handoff;
- no file over its intended hosting limit.

Do not claim exact continuity from visual similarity. The verifier must extract the same indexed frame using the same ffmpeg path and compare the resulting PNG bytes.

### 8. Stage or publish the archive

When publishing is requested, read [references/archive-site.md](references/archive-site.md), then stage accepted media and posters:

```powershell
python "$env:USERPROFILE\.codex\skills\minimax-video-series\scripts\series_pipeline.py" stage-site --config C:\path\series.json
```

Update the site copy and chapter metadata, run its lint/test/build checks, then invoke `sites:sites-hosting` and follow its current instructions. Reuse the existing project ID. Publishing is an external change: perform it only when the user asks for publishing/uploading or the active request clearly includes it.

## Operating rules

- Preserve user files and accepted takes. Rerenders create new attempts; rejection moves only the active pending take.
- Keep seeds, exact prompts, transitions, media metadata, states, paths, review notes, and attempts in the manifest.
- Keep stable `(S1)`, `(S2)`, ... identities in the top-level speakers registry. Preserve user-provided dialogue, lyrics, punctuation, language, and visible text verbatim.
- Treat prompt-lint errors as render blockers. Resolve warnings deliberately and record exceptions.
- Persist accepted-video, initial-frame, and continuation-frame SHA-256 values; keep legacy-boundary provenance under `upstream`.
- Resume from the manifest; do not infer state from the newest filename when an active attempt is recorded.
- Never render chapter N+1 from a pending or rejected chapter N.
- Never use the combined master as the continuity source. Extract from the accepted individual chapter at the configured final frame index.
- If a requested transformation is too complex for one clip, split it into more chapters instead of stacking actions.
- Keep user-facing progress concise: chapter/movement completed, review decision, rerender reason, and final verified deliverables.
