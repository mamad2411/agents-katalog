---
name: minimax-h3-low-vram-video
description: Deploy, run, troubleshoot, and quality-optimize MiniMax H3 local text-to-video, image-to-video, reference-to-video, native audio, and social-media video workflows on Windows PCs with constrained NVIDIA VRAM or system RAM. Use when users mention MiniMax H3/Hailuo H3 local deployment, ComfyUI H3 models, 8GB GPUs, insufficient memory or pagefiles, blurry faces, low-resolution H3 output, Real-ESRGAN video upscaling, or producing publication-ready MP4 files.
---

# MiniMax H3 Low-VRAM Video

Deploy and operate MiniMax H3 through official ComfyUI nodes on constrained Windows hardware. Prefer native detail, stable execution, and verified media output over nominal resolution alone.

## Workflow

1. Inspect CPU, RAM, GPU/VRAM, free disk space, pagefiles, NVIDIA driver, and existing ComfyUI/Python versions.
2. Read [references/decision-guide.md](references/decision-guide.md) before selecting models or resolution.
3. Read [references/installation.md](references/installation.md) for a new deployment or system-level pagefile change.
4. Read [references/prompt-guide.md](references/prompt-guide.md) when composition, faces, motion, audio, image conditioning, or reference conditioning matters.
5. Read [references/troubleshooting.md](references/troubleshooting.md) when startup, model loading, sampling, decoding, muxing, or output validation fails.
6. Install official ComfyUI portable and official H3 model files. Record file sizes and verify published hashes when available.
7. Configure low-memory startup flags and a large fixed pagefile. Reboot if Windows has not activated the new pagefile.
8. Validate `/system_stats`, `/object_info`, model visibility, quantization backends, and DynamicVRAM before submitting a long job.
9. Generate a short conservative proof at 608x352 or 864x480. Verify H.264 video, AAC stereo audio, frame count, duration, and complete decoding.
10. Raise H3 native resolution according to the decision guide. For faces, improve composition before adding resolution.
11. Preserve the native H3 result. Create a separate 1080p publishing copy only when needed.
12. Use `scripts/upscale_video_realesrgan.py` for frame-streamed Real-ESRGAN enhancement when system RAM cannot hold all frames at once.

## Guardrails

- Treat disk capacity and virtual memory as different resources. Hundreds of GB of free disk do not replace an active pagefile.
- Never claim that an interpolated 1080p file contains native 1080p detail.
- Do not start with 1344x768 on an unverified 8GB setup. Prove the whole encode path first.
- Keep the trained H3 duration grid: 24 fps and frame lengths `17k+5`; 124 frames is about 5.17 seconds and sits in the trained range.
- Preserve H3's native stereo audio unless the user explicitly requests replacement.
- Avoid crowds, wide shots, rapid cuts, and tiny faces when facial detail matters. Use one or two foreground subjects in a medium close shot with stable camera motion.
- Save native and enhanced outputs under different names. Never overwrite the native master.
- Inspect logs during long jobs. Distinguish slow offloading from a hang by checking process life, queue state, step progress, RAM, VRAM, and free virtual memory.

## Recommended Low-Memory Startup

Use the portable embedded Python and start ComfyUI with:

```text
--windows-standalone-build --enable-dynamic-vram --fast-disk --cache-none --reserve-vram 1.0 --disable-pinned-memory
```

Disable auto-launch for unattended/API runs. Keep a browser launch only in the user-facing batch file.

## Model Set

Prefer the official quantized functional set:

- FL2VA INT8 diffusion model for text/image first-last-frame video generation
- REF2VA INT8 diffusion model for reference-conditioned generation
- Qwen3-VL 32B MiniMax H3 NVFP4/AWQ text encoder
- MiniMax H3 FP16 video VAE
- MiniMax H3 FP32 audio VAE

Do not substitute similarly named files without checking node compatibility and quantization metadata.

## Face-Quality Strategy

Apply these changes in order:

1. Increase face pixel coverage: one or two subjects, medium close shot, foreground focus.
2. Reduce motion and identity changes: slow push-in, no rapid cuts, maintain the same facial structure.
3. Request concrete detail: sharp eyes, natural skin texture, hair strands, coherent hands, controlled highlights.
4. Raise native H3 canvas: 864x480, then 1152x640, then 1344x768 after resource validation.
5. Create a 1920x1080 publishing copy with modest enhancement. Do not expect super-resolution to repair malformed anatomy or identity drift.

## Verification Contract

Before delivery, report:

- Exact output path
- Native versus enhanced status
- Width, height, fps, duration, and decoded frame count
- Video codec and average bitrate
- Audio codec, sample rate, and channel count
- Generation time and whether OOM/retry occurred

Decode the complete video and audio streams, not just container metadata. Extract at least one representative frame for visual inspection when facial quality is a key requirement.

## Reusable Upscaling

Run:

```powershell
python scripts/upscale_video_realesrgan.py --input INPUT.mp4 --output OUTPUT.mp4 --model RealESRGAN_x4plus.pth --width 1920 --height 1080
```

The script processes one frame at a time with overlapping tiles, writes a temporary video master, then remuxes the original audio. Read its `--help` before changing tile size or encoder quality.
