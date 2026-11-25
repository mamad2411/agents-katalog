---
name: h3-local-setup
description: Set up and tune MiniMax H3 for local inference in ComfyUI — checkpoint and quantization choice, text encoder, VRAM tiers, sampler and scheduler, SageAttention version, caching, and troubleshooting. Use when the user is installing H3, hitting OOM, getting black frames, corrupted output, silent or garbled audio, or slow generation, or asking which settings, quant, encoder, or GPU they need.
---

# H3 Local Setup

## Step 1 — Establish the hardware reality

Ask or check: GPU and VRAM, **GPU architecture**, system RAM, disk type.

Architecture matters as much as VRAM — see the Ampere trap in Step 2.

**System RAM and disk are part of the inference path.** Weights stream disk → RAM → VRAM. Reference
configuration is 32 GB RAM plus NVMe. On a SATA SSD or 16 GB of RAM the bottleneck is I/O, not the
GPU, and no sampler setting fixes that.

| VRAM | Realistic target |
|---|---|
| 8–12 GB | 640×352, short durations, NF4 or INT8. Expect long waits |
| 16 GB | 832×480 comfortably |
| 24 GB | ~0.3 MP fits entirely in VRAM; beyond that ComfyUI offloads to RAM and still works |
| 32 GB+ | 1344×768, the local ceiling |

Measured on a 24 GB Ampere card: 0.5 MP / 5 s / 15 steps with SageAttention = **2 min 54 s**;
1152×640 / 15 s = **~22 min**; 1024×1024 / 15 s with heavy RAM offload = **~45 min**.

**Attention cost scales with duration, not just resolution.** If you OOM at 15 s, try the same
resolution at 5 s before stepping resolution down.

## Step 2 — Pick the right files

**Diffusion model: `int8_convrot` pruned.** ~2× faster than fp8 with ~0.9% relative quantization
error. There is no reason to run inference on the unpruned model. Caveat: **train on the checkpoint
you will infer on** — pruning compresses `adaln_proj`, so a LoRA trained on full BF16 produces severe
artifacts when applied to a pruned build, and turbo LoRAs targeting full adaLN layers may not apply
at all.

**Text encoder — check your architecture first:**

| GPU | Encoder |
|---|---|
| Ampere (RTX 30-series) | **INT8 ConvRot.** NVFP4 has no fp4 hardware here, falls back to an uncalibrated path, and is both slower and visibly worse — with no error |
| Ada / Blackwell (40/50-series) | NVFP4-AWQ is fine and much smaller |
| Any, low disk | NVFP4 works purely as a storage format on any GPU |

**Checkpoints fail closed:** `fl2va` (T2V + keyframes) and `ref2va` (references). "Node type not
found" means the wrong checkpoint, not a broken install.

For GGUF, read `reference/troubleshooting.md` first — three specific traps live there, including the
`-mmproj` sidecar the stock loader silently refuses to merge.

## Step 3 — Sampler and scheduler: pick your trade-off

There is no universally correct scheduler. There is a trade-off:

| Scheduler | Visuals | Audio |
|---|---|---|
| `simple` | Muddier, softer fine texture | **Clean** |
| `beta` | Better texture and cinematic realism | **Destroyed** — static or garbled |

H3's whole premise is joint audio-video, so **`simple` is the correct default.** Choose `beta` only
when you know the audio will be replaced.

| Sampler | Scheduler | Steps | Use |
|---|---|---|---|
| `res_multistep` | `simple` | 8–20 | **Standard path.** Best audio |
| `euler` | `beta` | 4–8 | Turbo LoRA, visuals-first |
| `euler` | `simple` | 4 | Dual-clock turbo path |

`res_multistep` is the biggest free win: ~21 sigma points match 50-step Euler quality at the same
seed, roughly 2.4× fewer forward passes.

**Three settings that break audio outright, no error:**
- SDE noise / `eta` above 0.0 — any stochastic or ancestral sampler
- `denoise` below 1.0, including latent inpainting
- Custom shift values. 12.0 video / 3.0 audio is a model constant

## Step 4 — Speed stack

**SageAttention `2.2.0`.** Not 1.x (Triton-based, black output on Blackwell). Not 3 — it silently
degrades quality versus 2.2.0. On Blackwell the `--use-sage-attention` flag is **not** equivalent to
KJNodes' `Patch Sage Attention KJ`; use the node, between UNETLoader and BasicGuider, starting on
`auto`. If frames come back black, set `sageattn_qk_int8_pv_fp16_cuda`. The wheel must match your
PyTorch/CUDA build exactly.

Attention-level speedups are **safe for audio** — they optimize the maths without skipping sampling
steps.

**CUDA 13.0.** One reproducible report: 6:10 → 1:37.

**Caching, last and knowingly.** EasyCache and Spectrum do not account for the audio schedule — that
is why they warp voices — and on the video side they introduce geometric artifacts, ruin fingers, and
dampen physics. If you use EasyCache, wire it to **both** the scheduler and the basic guider, and
place it before the guider in the chain. Disable it for anything audio-critical.

**EasyCache and Spectrum cannot be stacked.** Spectrum predicts a block that EasyCache then skips,
and you get `RuntimeError: native MiniMax H3 final transformer block was not executed`. Pick one.

**Manual block swap is obsolete for inference** — ComfyUI's dynamic offloading streams weights
smarter. Block swap still matters for training.

**Evict the text encoder before sampling.** The encoder (~16.5 GB even at Q4) and the DiT (~25 GB) do
not co-fit on a 32 GB card; without eviction the DiT loads partially and streams ~19 GB from RAM every
step. Conditioning is computed before sampling, so eviction is safe. Measured: **~60 min → ~15 min**.

## Step 5 — Verify before blaming settings

Read `reference/troubleshooting.md` and match the symptom. Two traps worth knowing up front:

- A cache custom node can corrupt H3 output **merely by being present** in `custom_nodes`, even
  unused. Delete the folder; do not update it.
- The float16/bfloat16 dtype warning about falling back to pytorch attention is **expected**.

## Step 6 — Confirm what the prompt depends on

Resolution in **multiples of 32**, short side ≤768 locally. This is not cosmetic: a non-multiple can
silently crop or warp rather than erroring, which is why 1280×720 is impossible and you use
**1280×704**.

Frames follow the `17n + 5` grid at 24 fps. For Ref2VA set width and height explicitly, and choose
`ref_image_size` deliberately — `match` downscales only, `max` gives an independent 2048 px short
side with the best identity fidelity and a large slowdown.
