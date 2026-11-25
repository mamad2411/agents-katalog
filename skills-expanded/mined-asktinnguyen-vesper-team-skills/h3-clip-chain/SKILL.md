---
name: h3-clip-chain
description: Chain MiniMax H3 clips into a single long-form video with an automated final-frame continuation loop and a live HTML progress tracker. Use for an unattended, simple, multi-minute H3 extension, a "10 minute video" from a short prompt, automatic segment-to-segment rendering, or a progress dashboard. Use `$h3-context-loop` instead for multi-scene production, generated-audio continuity, reviewable rerolls, or continuity that needs more than the previous final frame.
---

# MiniMax H3 clip chain

Render a short source clip once, then keep extending it into a long video: each
next segment starts from the previous clip's final frame and reuses the same
workflow. A companion dashboard tracks every segment live. This is a fast,
unattended final-frame handoff; it does not carry the preceding video-motion or
generated-audio context, so do not use it for a controlled narrative seam.

## Prerequisites

- MiniMax H3 ComfyUI running on `127.0.0.1:8188` (see the `generate-local-video`
  skill for how to start it and validate models).
- `ffmpeg` on PATH (or pass `--ffmpeg`).
- A Python 3 interpreter.
- One single-clip MiniMax H3 workflow JSON (I2V or R2V). It must have the roles
  listed in [references/configuration.md](references/configuration.md):
  a `SaveVideo` node, a `MiniMaxH3ImageToVideo`/`MiniMaxH3ReferenceToVideo` node,
  a prompt source, an optional `LoadImage` reference, and a `RandomNoise` seed.

## 1. Run the chain driver

```bash
python scripts/chain_driver.py \
  --workflow path/to/workflow.json \
  --prompt "your scene prompt" \
  --minutes 10 \
  --run-dir ./my_run
```

- Omit `--prompt` to keep the workflow's existing prompt for segment 1.
- Pass `--beats-file beats.json` (a JSON array) to rotate your own per-segment
  action beats; otherwise a generic set is used.
- Use `--subject base.png` to set the segment 1 reference image explicitly.
- `--dry-run` prints the detected graph and API payload for segment 1 without
  submitting anything — a good first check on a new workflow.

The driver writes `manifest.jsonl` and `chain.log` into `--run-dir`, saves each
clip under the ComfyUI output preview prefix, and finally concatenates everything
into `<prefix>_final.mp4` in the run dir.

## 2. Monitor with the tracker

```bash
python scripts/tracker_server.py --run-dir ./my_run --port 8321
```

Then open `http://127.0.0.1:8321`. The dashboard shows a progress strip, the
currently rendering segment with a live elapsed timer and its starting frame, a
tile per clip with status, and in-page playback. It polls `/api/progress` every
3 seconds.

## Launching hidden on Windows

`scripts/start_driver.ps1 <args...>` and `scripts/start_tracker.ps1 -RunDir <dir>`
launch either process in a hidden background window with redirected logs.

## Behavior and safety

- Resume-safe: rerun the same `--run-dir` to continue from the last completed clip.
- A failed render logs its status and halts the loop instead of wasting GPU time.
- Write every beat as a small variation of the same ongoing action, and end it in
  a pose the next segment can plausibly inherit from one image. Use
  `$h3-context-loop` when a beat requires a precise new location, action,
  character state, camera move, music, or dialogue handoff.
- On a long build, keep updates to the user flowing: poll `chain.log` or the
  tracker endpoint and report progress at least every minute.
- Do not widen server exposure, update models, or queue other work into the same
  ComfyUI instance while a chain is running.

Full option tables and workflow auto-detection rules live in
[references/configuration.md](references/configuration.md).
