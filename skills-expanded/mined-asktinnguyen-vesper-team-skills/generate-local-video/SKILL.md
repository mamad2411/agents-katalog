---
name: generate-local-video
description: Generate videos locally with the installed MiniMax H3 ComfyUI pipeline on this Windows computer. Use for text-to-video, image-to-video, first/last-frame video, or reference-driven image/video/audio generation; for starting or checking the local H3 server; and for locating completed local video outputs. Use the H3 Context Loop for multi-scene or audio-continuous productions, and the H3 clip chain only for unattended final-frame extensions.
---

# Generate Local Video

Use the verified ComfyUI installation at `C:\ComfyUI-H3`. It contains MiniMax H3 FL2VA and Ref2VA INT8 ConvRot models, the Qwen3-VL-32B Heretic conditioning encoder, audio/video VAEs, and prepared workflows.

## Run the workflow

1. Run `python C:\Users\Admin\.codex\skills\generate-local-video\scripts\h3_control.py doctor`. Stop and report the missing item if this fails; do not redownload models automatically.
2. Run `python C:\Users\Admin\.codex\skills\generate-local-video\scripts\h3_control.py start`. This starts ComfyUI at `http://127.0.0.1:8188` in a hidden background process and waits for health readiness.
3. Choose the production path before loading a workflow:
   - Use a prepared single-clip workflow for one self-contained 4–15 second shot.
   - Use `$h3-context-loop` for two or more connected scenes, character continuity across a scene change, generated-audio continuity, per-scene review, rerolls, or resumable assembly. It carries and trims a 22-frame video/audio overlap.
   - Use `$h3-clip-chain` only for an unattended extension where a previous final frame is sufficient. It does not carry the previous clip's motion or generated-audio tail, so it is a poor fit for narrative scene changes.
4. For a single clip, choose the prepared workflow:
   - `video_minimax_h3_t2v.json` for text-to-video.
   - `video_minimax_h3_i2v.json` for first frame, last frame, or both.
   - `video_minimax_h3_r2v.json` for appearance, style, motion, video-editing, continuation, or audio references.
5. Use the browser/computer-control capability to open ComfyUI, load the selected JSON from `C:\ComfyUI-H3\user\default\workflows`, set inputs, and queue the prompt. Do not rebuild the graph when a prepared workflow fits.
6. Run `python C:\Users\Admin\.codex\skills\generate-local-video\scripts\h3_control.py queue` to monitor. If active, provide the user a concise update at least every 60 seconds and repeat; never block silently on a long shell sleep.
7. Run `python C:\Users\Admin\.codex\skills\generate-local-video\scripts\h3_control.py outputs --limit 5` when the queue clears. Verify that the newest video exists and has a nonzero size, then return it with an absolute-path Markdown media link.

## Configure generation

Read [references/h3.md](references/h3.md) before choosing a mode or changing model, duration, resolution, reference roles, or continuation method.

Ask only for information that cannot be inferred safely. A prompt-only request defaults to T2V, a supplied endpoint image defaults to I2V, and media requested as identity/style/motion/audio guidance requires R2V.

Preserve the workflow's preselected model filenames. Start with the workflow preview resolution and the minimum useful duration when the user has not specified quality; raise resolution or duration only when requested because H3 renders are computationally expensive.

For prompt enhancement, use the installed `MiniMax H3 Prompt Guide`, `MiniMax H3 Generation Tail Loader`, and `MiniMax H3 Prompt Enhancer (Qwen3-VL)` nodes. The tail is optional for ordinary H3 conditioning.

## Operate safely

- Keep the server bound to `127.0.0.1`; do not expose it to the LAN or internet without explicit authorization.
- Do not update ComfyUI, dependencies, nodes, drivers, or model weights during a generation request.
- Do not install SageAttention automatically. Native CUDA 13 INT8 ConvRot kernels are verified; SageAttention is optional and version-sensitive.
- Do not overwrite or delete prior outputs. ComfyUI generates unique output names.
- Treat a queued render as potentially multi-minute work. Continue monitoring until completion or a concrete error.
- On failure, run `python C:\Users\Admin\.codex\skills\generate-local-video\scripts\h3_control.py logs --tail 120`, report the relevant error, and preserve the queue and output files for diagnosis.
