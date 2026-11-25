---
name: huggingface-on-apple-silicon
description: Use when loading a HuggingFace model on a Mac (Apple Silicon) fails with `RuntimeError: Invalid buffer size: X.XX GB` from `caching_allocator_warmup` in `transformers/modeling_utils.py`. Triggered by `device_map="auto"` placing a model on MPS that exceeds Metal's per-buffer limit. The env var `PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0` does NOT fix this — switch to `device_map="cpu"` instead.
---

# HuggingFace Model Loading on Apple Silicon

## Symptom

Loading a HuggingFace model on a Mac fails before any weights actually load:

```
File ".../transformers/modeling_utils.py", line 4832, in caching_allocator_warmup
    _ = torch.empty(int(byte_count // 2), dtype=torch.float16, device=device, requires_grad=False)
RuntimeError: Invalid buffer size: 15.44 GB
```

The reported buffer size roughly equals the model size in bytes (≈ params × 2 for bf16/fp16).

## Cause

`device_map="auto"` on a Mac places the model on MPS (the Metal backend). Modern `transformers` then calls `caching_allocator_warmup`, which tries to pre-allocate a **single contiguous buffer** sized to the entire device's share of weights. Metal rejects allocations larger than its per-buffer cap (`MTLDevice.maxBufferLength`) — on a 24 GB unified-memory M-series Mac that cap sits around 14–16 GB.

7B-parameter models in bf16 (~14 GB) sit right at this line. 13B+ models cannot fit in a single MPS buffer on any current Mac.

## The trap: `PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0` does NOT help

This is the first fix everyone (including LLMs) reaches for. It does not work.

That env var controls PyTorch's *soft* allocator cap (a fraction of recommended working-set size). The "Invalid buffer size" error comes from **Metal itself** rejecting a single buffer above `maxBufferLength`. PyTorch never gets a chance to apply its watermark — Metal refuses the allocation first.

Setting `PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0` will reproduce the **exact same error**. Don't spend a round-trip on it.

## Fix

Force the model onto CPU:

```python
model_kwargs = {"device_map": "cpu", "torch_dtype": torch.bfloat16}
model = SomeModel.from_pretrained(model_name, **model_kwargs)
```

Slower than MPS, but unified memory means a 14 GB model fits comfortably alongside the OS on a 24 GB machine. For a one-off demo or batch job this is the right answer.

If you need accelerator speed, the alternatives are:
- **Quantize**: 4-bit via `bitsandbytes` (limited Mac support) or pre-quantized GPTQ/AWQ checkpoints
- **Smaller model**: Qwen2-VL-2B instead of -7B, etc.
- **Split**: `device_map={"vision_tower": "mps", "language_model": "cpu", ...}` to keep individual MPS buffers below the limit
- **Different machine**: M-series ≥36 GB raises the cap, or move to CUDA

## Quick rule of thumb

| Model size in bf16 | 24 GB M-series | 36 GB M-series | 64 GB+ M-series |
|---|---|---|---|
| ≤ 4 B (~8 GB) | MPS OK | MPS OK | MPS OK |
| 7 B (~14 GB) | **CPU only** | MPS OK | MPS OK |
| 13 B (~26 GB) | won't fit | **CPU only** | MPS OK |
| 30 B+ | won't fit | won't fit | quantize |

"CPU only" = MPS will fail this exact `Invalid buffer size` error.

## Watch for the follow-up: missing `torchvision`

Once the model loads on CPU, vision-language models often surface a second error:

```
ImportError: Qwen2VLVideoProcessor requires the Torchvision library but it was not found
```

The processor pulls in `torchvision` even though it wasn't a direct dependency. Add it to your inline `dependencies` block, version-matched to your torch pin:

| torch | torchvision |
|---|---|
| 2.4.0 | 0.19.0 |
| 2.5.x | 0.20.x |
| 2.6.x | 0.21.x |

When in doubt: `uv pip install torch==X.Y.Z torchvision --resolution=highest` and let the resolver pick the matching version.

## Diagnostic recipe

```bash
# 1. Confirm you're on Apple Silicon with limited RAM
sysctl hw.memsize machdep.cpu.brand_string

# 2. Estimate model size: params × 2 bytes for bf16/fp16
#    Qwen2-VL-7B → ~14 GB → won't fit MPS on a 24 GB Mac

# 3. Apply CPU fix and re-run
#    Edit: device_map="auto" → device_map="cpu"

# 4. If a torchvision ImportError appears next, add it to deps and re-run
```

## Does not apply to

- CUDA / Linux machines (different allocator, no Metal cap)
- Models small enough that warmup buffer fits — most ≤4B-param models are fine on MPS
- The error `MPS backend out of memory` (different cause: cumulative allocation, not single-buffer cap; that one *can* sometimes be addressed by `PYTORCH_MPS_HIGH_WATERMARK_RATIO`)
