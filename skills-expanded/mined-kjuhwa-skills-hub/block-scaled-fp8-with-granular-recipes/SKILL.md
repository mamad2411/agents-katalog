---
name: block-scaled-fp8-with-granular-recipes
description: Store FP8 block scales separately at a configurable (gran_m, gran_n, gran_k) granularity, then transform into MN-major TMA-aligned layout before kernel dispatch.
category: fp8-quantization
version: 1.0.0
version_origin: extracted
tags: [fp8, block-scaling, quantization, tma, layout-transform, mxfp8]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/deepseek-ai/DeepGEMM.git
source_ref: main
source_commit: 7f2a703ed51ac1f7af07f5e1453b2d3267d37d50
source_project: DeepGEMM
source_paths:
  - csrc/apis/layout.hpp
  - csrc/jit_kernels/impls/smxx_layout.hpp
imported_at: 2026-04-18T13:12:58Z
---

# Block-Scaled FP8 With Granular Recipes

## What / Why
Per-tensor FP8 scaling loses too much accuracy on activations with long tails; per-element is unaffordable. Block scaling stores one FP32 (or packed UE8M0) scale per `(gran_m × gran_k)` (or `gran_n × gran_k`) block. Users pick the recipe — `(1, 128)` for per-token activations, `(128, 128)` for weights, etc. — trading scale-storage overhead against accuracy. The kernel expects the scales in MN-major, TMA-aligned layout; a transform pass converts user-supplied scales before dispatch.

## Procedure
1. **Define the recipe** as a 3-tuple `(gran_m, gran_n, gran_k)` for each operand:
   - A scales: shape `[ceil(m / gran_m), ceil(k / gran_k)]`.
   - B scales: shape `[ceil(n / gran_n), ceil(k / gran_k)]`.
2. **Validate inputs.** Scales must be contiguous, FP32 (or packed UE8M0 on SM100). Reject mis-aligned strides early.
3. **Pad for TMA alignment.** Round the leading dim to the nearest 128 (SF padding); zero-fill the tail.
4. **Transpose to MN-major.** TMA descriptor assumes the M (or N) axis is the contiguous one — swap axes via `transform_sf_into_required_layout()`.
5. **Pack UE8M0 (SM100 only).** Convert 4 FP32 scales into one `int32` via the UE8M0 encoder; this halves SF bandwidth.
6. **Emit descriptor.** Build the TMA descriptor from the transformed/packed tensor and pass to the kernel alongside A/B descriptors.

## Key design points
- Fine granularity (e.g., `(1, 32)`) → best accuracy, highest scale-storage overhead.
- Coarse granularity (e.g., `(128, 128)`) → cheap but loses channel-wise variation; OK for weights, bad for activations.
- The kernel does not read the recipe directly; it infers layout from the SF descriptor. So recipe lives in host code.
- For MXFP8 / UE8M0 on SM100, scales are always packed; for SM90 E4M3, scales stay FP32.

## References
- `csrc/apis/layout.hpp` — public recipe-aware layout functions.
- `csrc/jit_kernels/impls/smxx_layout.hpp` — MN-major transform + TMA padding.
- `deep_gemm/utils/layout.py` — Python-side `per_token_cast_to_fp8` that emits scales in the expected layout.
