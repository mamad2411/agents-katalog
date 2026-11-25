---
name: re-light
description: >-
  Relight or re-scene a short talking-head / B-roll clip by transferring lighting and environment from an AI-generated reference still onto the video. Use when the user drops a video path and asks to "relight this", "change the lighting", "put me in [a scene/place]", "drop me into [environment]", "re-scene this clip", "make this look cinematic", or invokes /re-light. Two Fal.ai calls: nano-banana-2 relights one frame, Kling O3 Pro pushes that look onto the whole clip with audio preserved. Clips must be 3-10 seconds.
---

# re-light Skill

Replicates the Higgsfield "change the light in any video" workflow on raw Fal.ai — no wrapper. Two model calls with a human approval gate between them:

1. **nano-banana-2/edit** relights / re-scenes a single frame (cheap, ~$0.10). Subject identity stays locked — that's why NB2, not Seedream.
2. **Kling O3 Pro video edit** transfers that exact look onto the whole clip, frame-to-frame, **audio preserved**. ~$0.168/sec.

> **Model note:** O3 Pro is the default — it markedly beats O1 on lip-sync and face stability for the *same* per-second price. O1 stays available via `--model o1` as a faster/cheaper draft.

## Hard constraints

- **Clip must be 3–10 seconds.** Kling's edit endpoint caps at 10s. `prep` rejects anything outside this — tell the user to trim to a ≤10s segment first. (Auto-chunking long clips is a deliberate v2 non-feature.) Because the `video` step tail-pads ~0.5s before Kling, clips ≤ ~9.5s get full tail protection; a 9.5–10s clip still works but pads less (it warns).
- **Frame-exact output, any input fps (automatic).** Kling always returns **24fps** and quantizes the clip length, dropping the final ~0.1–0.2s — which would desync dialogue. The `video` step handles this end to end: it probes the source's exact fps + frame count, freeze-pads the tail before Kling, then conforms Kling's 24fps result back to the source's **exact fps, frame count and length** and remuxes the **original** audio. Works for any rate (23.976 / 24 / 25 / 29.97 / 30 / 50 / 59.94 / 60). The output matches the input frame-for-frame — **never hand-trim or re-conform it.** It prints `exact_length_match` and the frame counts; if that's ever `false`, surface it.
- **Audio is always kept** (`keep_audio: true` on the Kling call; the deliverable then carries the pristine original audio, length-matched). Standing rule for this skill.
- This is a **short-clip / hero-shot / B-roll** tool by nature. Relighting a full piece-to-camera monologue can still drift slightly on the mouth — set that expectation; it shines on B-roll and short hero shots.

## Cross-platform

Runs on macOS, Windows, and Linux. Invoke the script with the platform's Python:
- **macOS / Linux:** `python3 ~/.claude/skills/re-light/scripts/relight.py …`
- **Windows:** `python %USERPROFILE%\.claude\skills\re-light\scripts\relight.py …`

The script self-bootstraps: if `fal-client` is missing it pip-installs it; if there's no system `ffmpeg`, it pip-installs a bundled one (`imageio-ffmpeg`) — no admin rights, no fuss. Credentials reuse `FAL_KEY` when present, and also read the existing GenMedia fal.ai config at `~/.genmedia/config.json` when GenMedia is already set up. The local GenMedia CLI (`genmedia upload`) is also used as a fallback uploader if `fal-client` upload fails.

## Step 0 — Setup (first run only)

If `config.json` does not exist in the skill folder, this is a first run:
1. **Ask the user where to save outputs**, offering the default **`~/Documents/Relight`**. One question, accept the default if they don't care.
2. Run setup with their answer (installs deps + writes config). Idempotent — safe to re-run:

```bash
python3 ~/.claude/skills/re-light/scripts/relight.py setup --output-dir "<their choice or ~/Documents/Relight>"
```

It prints a JSON readiness line (`output_dir`, `ffmpeg`, `fal_key`, `fal_key_source`, `genmedia_cli`). If `fal_key` is `MISSING`, tell the user to run `genmedia setup` or set `FAL_KEY` (Mac/Linux: add `export FAL_KEY="<key>"` to `~/.zshrc`; Windows: `setx FAL_KEY "<key>"`) — don't set it for them. If `config.json` already exists, skip Step 0 entirely.

## Workflow

### Step 1 — Read intent

User gives a video path + either a **scene description** ("put me in the jungle", "noir office", "golden-hour rooftop") or a **reference image** of the scene/lighting they want. Derive a 3–5 word kebab-case `title` slug yourself.

### Step 2 — prep (validate + grab a frame)

```bash
python3 ~/.claude/skills/re-light/scripts/relight.py prep \
  --video "<path>" --title "<slug>" [--frame-time <sec>]
```

Returns JSON: `folder`, `frame_path` (auto-selected sharpest frame), `duration`, `width`, `height`, `aspect_ratio`, `sharpness`, and `candidates` (top frames ranked sharp→soft, each with `time`/`path`/`sharpness`).
- prep samples several frames and **auto-picks the sharpest** to reject motion blur — not the midpoint, not random.
- On a duration error, relay it plainly — don't work around the 3–10s cap.
- **Read the chosen `frame_path`.** Sharpness can't tell if the eyes are closed or the mouth is mid-word — so also Read the top 2–3 `candidates`, and if the auto-pick has closed eyes / a bad expression, re-run `prep --frame-time <that candidate's time>` to lock the better one.

### Step 3 — Write the relight prompt, then run the image step

Look at the frame, then write a **scene prompt that relights it cinematically WITHOUT changing the shot**. This is a video relight: the still must stay pixel-aligned with the source frame so the Kling pass can map it onto the moving footage. The engine hard-locks geometry (`IDENTITY_LOCK`, always on) and appends a film-craft layer — so spend your words on lighting + background. Always:
- **🔒 Never re-compose — this is the rule that makes it actually work.** Same camera angle, framing, crop, distance, subject size, head pose and expression as the source frame. Do NOT ask to move, zoom, stand him up, or off-center the subject. A still whose framing differs from the footage **breaks the video transfer** (Kling gets contradictory geometry → mangled output). Only lighting + background change.
- **Override the original flat lighting — the #1 thing that sells the look.** You can dramatically reshape the *light* on a locked frame — that's the craft, not moving the camera. Specify a shaped, directional key: "a hard key from high front-left rakes across his face so one side is sculpted and the other falls into deep shadow (chiaroscuro), cool rim from behind for separation." Flat/even/frontal = amateur; directional + high key-to-fill ratio = cinematic.
- **Replace the background** to match the requested scene, in soft shallow-DoF bokeh behind him.
- **Protect the face (baked in — reinforce it).** The engine always applies skin fidelity (`SKIN_FIDELITY`): no added wrinkles/texture/age, warm healthy tones. Never prompt "pores / skin texture / wrinkles / grain on skin" — those age the subject and make skin grey. For cool or neon scenes especially, keep a **warm key or warm bounce on the face** so skin doesn't read sickly.
- **Name a palette** — the grade (teal-and-steel, amber dusk, cool noir…) with warm natural skin.
- Pass `--no-cinematic` only for a deliberately flat/documentary look. (The geometry lock stays on regardless.)

```bash
python3 ~/.claude/skills/re-light/scripts/relight.py image \
  --frame "<frame_path>" --folder "<folder>" \
  --aspect-ratio "<aspect_ratio from prep>" \
  --prompt "<relight prompt>" \
  [--reference "<scene reference image path>"]
```

If the user gave a reference image, pass `--reference`; in the prompt, call the subject frame "the first image" and the reference "the second image."

### Step 4 — APPROVAL GATE (do not skip)

Read the returned `still_path` and show the user. **Wait for explicit approval before the video step** — that pass costs real money (~$0.168/sec). Changes? Re-run Step 3 (pennies per regen). Only proceed on a clear go.

### Step 5 — video (push the look onto the clip)

```bash
python3 ~/.claude/skills/re-light/scripts/relight.py video \
  --video "<original video path>" --still "<approved still_path>" --folder "<folder>" \
  --prompt "<transfer prompt>" \
  [--model o3-pro|o1] [--pad-seconds 0.5]
```

- Transfer prompt references the still as `@Image1`, e.g. *"Place the person from @Video1 into the environment and lighting of @Image1; match the background and the [describe] lighting; preserve identity, exact lip and mouth movements, clothing, and all original motion and timing."*
- **Animate the background subtly.** The engine bakes in an ambient-motion clause (subject stays locked, only the scene moves) — but *name the specific movers you see in the still*: e.g. haze/smoke drifting, a couple of lights slowly panning, beams shimmering, water rippling, foliage swaying, embers rising, clouds creeping. Keep it slow and chill — alive, not busy. `--no-motion` for a deliberately static background.
- **Default `o3-pro`.** Only drop to `--model o1` if the user wants a faster/cheaper draft.
- **Frame-exact length is automatic** (see Hard constraints). The `video` step pads → runs Kling at 24fps → conforms back to the source's exact fps/frame-count/length and remuxes the original audio. The saved `relit-NN (C).mp4` already matches the input frame-for-frame — hand it over as-is, **don't trim or re-conform.** Intermediates (`_kling-input.mp4`, `_kling-raw.mp4`) are auto-deleted on a clean run. `--pad-seconds` only needs raising if a clip still loses its tail (it won't, normally).
- After it saves, give the user the output path. Audio is already baked in. Mention it matches the source length frame-for-frame.

### Cost (quote before the video step — same for O3 Pro and O1)

Kling is billed on the **padded** length (source + ~0.5s), so a clip costs roughly the next row up:

| Clip length | Kling video (padded) | + still | All-in |
|---|---|---|---|
| 3s | ~$0.59 | ~$0.10 | ~$0.70 |
| 5s | ~$0.92 | ~$0.10 | ~$1.00 |
| ~9.5s | ~$1.68 | ~$0.10 | ~$1.80 |

## Output structure (mirrors media-gen)

```
~/Documents/Relight/2026-06-16-relight-jungle/
├── relight.md            # prompts, models, params, timestamps
├── source-frame (C).png  # extracted reference frame
├── still-01 (C).png      # nano-banana relit still
└── relit-01 (C).mp4      # final relit clip, audio preserved
```

Regenerating within a session increments the index (`still-02 (C).png`, `relit-02 (C).mp4`). The `relit-NN (C).mp4` is already conformed to the source's exact fps/length; the `_kling-input.mp4` / `_kling-raw.mp4` intermediates are auto-deleted on a clean run (left behind only if the conform failed, for debugging).

## Rules of thumb

- **Approval gate is non-negotiable** — never run the video step without the user seeing and approving the still.
- **Identity first.** If NB2 drifts the face, re-roll the still; don't push a bad reference to video.
- **Output already matches the source frame-for-frame.** The video step pads → Kling (24fps) → conforms back to exact source fps/frames/length + original audio. Never hand-trim or re-conform the result — that's what was breaking dialogue sync before. If `exact_length_match` is `false`, say so and inspect rather than papering over it.
- **Don't widen scope to >10s clips.** Reject and tell them to trim. That's the design, not a bug.
- **Preserve the `(C)` suffix** on output filenames per global filename rule.
- **Errors:** `FAL_KEY not set` → user adds it to `~/.zshrc` (Mac/Linux) or `setx` (Windows). A `404` on a model → the `fal_id` drifted; check fal.ai/models and update the constant in `relight.py`. Dependency installs are automatic; if one fails (locked-down Python), the error prints the exact manual `pip install` command.

## Security & Permissions

**What this skill does:**
- Runs `ffmpeg`/`ffprobe` locally (system, or a pip-bundled `imageio-ffmpeg` it auto-installs) to validate clip duration, extract one reference frame, tail-pad the source before the Kling pass, and conform the result back to the source's exact fps/frame-count/length
- Auto-installs missing Python deps (`fal-client`, `imageio-ffmpeg`) from PyPI into the active interpreter, retrying with `--user` before giving up
- Uploads the source frame, the optional reference image, and the source video to Fal.ai, and calls two Fal models (`nano-banana-2/edit`, `kling-video o3/o1 edit`) using `FAL_KEY`
- Downloads the generated still and video (HTTPS-only — non-HTTPS result URLs are refused) into the configured output folder
- Reads `FAL_KEY` from the environment; on Unix only, recovers it from the user's shell profile if absent; if still missing, reads the fal.ai key from GenMedia's local `~/.genmedia/config.json` without printing it
- Uses the local GenMedia CLI as an upload fallback (`genmedia upload`) when direct `fal-client` upload fails

**What it does NOT do:**
- Does not post anywhere, touch any social account, or send data to any service other than Fal.ai and PyPI (for the one-time dependency install)
- Does not modify the original source clip
- Does not run shell strings (all subprocess calls use argument lists, not `shell=True`) and never logs or prints the API key
