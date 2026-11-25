---
name: minimax-h3-director-suite
description: Direct, storyboard, preview, retake, and experimentally accelerate local ComfyUI MiniMax H3 renders using MiniMax H3 Director and Spectrum. Use when a MiniMax H3 project needs a visual timeline, per-shot reference/audio tracks, live whole-shot denoise previews, range retakes, or controlled native-versus-Spectrum sampling A/B tests. Do not use Nunchaku as a MiniMax H3 accelerator; it is only relevant to separately requested supported image models.
---

# MiniMax H3 Director Suite

Use this skill with `$minimax-video-series` for chapter manifests, exact-frame continuation, acceptance, assembly, and publishing. Use `$minimax-h3-native-audio-music-video` when the source song must be preserved exactly.

## Preflight

Run the local probe before editing a workflow or rendering:

```powershell
& 'C:\Users\Admin\ComfyUI\.venv\Scripts\python.exe' `
  'C:\Users\Admin\.codex\skills\minimax-h3-director-suite\scripts\verify_plugin_suite.py' --strict
```

If the node directories exist but the API check fails, restart ComfyUI once and inspect its startup log. Do not reinstall, update, or replace the working H3 Torch/CUDA stack to resolve a missing node.

Read [references/plugin-operating-modes.md](references/plugin-operating-modes.md) before creating a Director timeline, using Spectrum, or considering Nunchaku.

## Direct with MiniMax H3 Director

1. Use the Director for a single 4–15 second window, a storyboarded shot, or a local retake—not as a replacement for the series manifest.
2. Connect the H3 model(s), MiniMax text encoder, video VAE, and audio VAE when using Ref2VA audio references. Connect both FL2VA and Ref2VA models only when the timeline needs both modes; Director lazily loads only the selected one.
3. Keep the global prompt limited to stable identity, style, world, and exclusions. Put chronological changes into timeline shot zones. Inspect the compiled prompt output before sampling.
4. Route `model` through Spectrum only for an approved benchmark, then through Preview Override, then into the guider/sampler. Route `positive`, joint `latent`, dimensions, frame length, and fps from Director to their matching H3 nodes. Route `combined_audio` only when generated/timeline-mixed audio is intended.
5. Use Preview Override with `latent2rgb (fast)` for routine progress. Use VAE preview only when detail needs inspection, with a connected video VAE and an overhead cap.
6. Use Retake Stitch only with the Director `retake_info` paired to the decoded retake frames. Keep base audio when the story or music must remain unchanged.

Keep exact-frame series handoffs under `$minimax-video-series`; accept and extract continuation frames from the accepted individual video, never from a timeline preview or combined master.

## Use Spectrum only through controlled A/B tests

Create an unchanged native control first. Then render one candidate with the same prompt, seed, model, image/audio references, frame grid, sampler, and output geometry. Compare the complete decoded video and audio before accepting it.

- Start with the conservative preset: blend `0.50`, degree `4`, ridge `0.10`, window `2.0`, flex `0.75`, warmup `5`, tail `1`, max history `8`, `system_ram`, debug enabled for the benchmark.
- Use only Euler, RES multistep, or RES multistep CFG++. Let unsupported samplers fall back to native behavior; do not claim an acceleration result from a fallback.
- Treat the candidate as a different trajectory, not a lossless optimization. Reject it for action, eye, finger, identity, timing, audio, or terminal-frame regressions.
- Keep `system_ram` first. Use VRAM history only after measuring free headroom at the actual generation peak; it adds multi-gigabyte history pressure and may not improve wall time.
- Do not use Spectrum for an accepted continuity-critical chapter until its native A/B result is acceptable for that exact workflow. Record the enabled state and every parameter in the manifest.

## Nunchaku boundary

Nunchaku is installed as a separate ComfyUI component, but it does not implement MiniMax H3 nodes or accelerate H3. The current local Torch 2.13 runtime has no matching Nunchaku binary wheel. Do not invoke its wheel-installer node, install a lower-Torch wheel, add its broad dependency bundle, or alter the H3 environment for an H3 task.

Use Nunchaku only when the user separately requests a supported FLUX, Qwen Image, or Z-Image workflow and authorizes a compatible isolated environment. It is not part of a MiniMax H3 graph.

## Operating rules

- Preserve the native H3 workflow as the production baseline.
- Do not put Director's generated/timeline-mixed audio in place of `MiniMaxH3NativeAudioLock` when exact source-song preservation is required.
- Render short windows and use the existing series pipeline for longer stories.
- Keep render parameters, plugin revisions, preview choice, Spectrum settings, acceptance evidence, and retake ranges in the project record.
- Never promote a Spectrum candidate, retake, or continuation frame without visual review.
