---
name: wgpu-shader
description: Use when implementing or debugging wgpu rendering and shader stages for preview or export pipelines, including GPU/CPU parity checks and performance tuning.
---

# WGPU Shader

## Use This Skill When
- Building shader stages for exposure, contrast, temperature, tint, highlights, or shadows.
- Debugging render artifacts, precision issues, or pipeline ordering.
- Optimizing preview latency and GPU memory movement.

## Required Inputs
- Target pipeline stage and expected visual effect.
- Input/output color-space expectation.
- Performance target for the operation.

## Workflow
1. Define stage contract: input texture format, output format, uniforms.
2. Implement shader with deterministic parameter mapping.
3. Validate against a CPU reference on sample images.
4. Instrument GPU timings for p50 and p95.
5. Optimize bandwidth and pass count only after correctness.

## Guardrails
- Minimize CPU-GPU round trips.
- Keep shader parameters versioned with app-side structs.
- Reject visual change without before/after evidence.

## Output Contract
- Shader code + pipeline binding updates.
- Validation notes against reference output.
- Timing snapshot with target comparison.
