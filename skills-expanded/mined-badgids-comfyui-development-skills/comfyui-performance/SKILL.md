---
name: comfyui-performance
description: Use for ComfyUI inference performance, benchmark design, kernel behavior, VRAM/RAM use, caching, loading time, throughput, latency, or regressions involving ComfyUI core, comfy-kitchen, or benchmark tooling.
metadata:
  version: "00.01.11"
---
# ComfyUI Performance

Performance claims require measurements on a defined environment.

## Sources

Use target/current:

- `Comfy-Org/ComfyUI`;
- `Comfy-Org/comfyui-benchmark`;
- `Comfy-Org/comfy-kitchen`;
- `Comfy-Org/comfy-model-tools` for current model packaging or conversion behavior when relevant;
- `Comfy-Org/comfy-quants` for current offline quantization formats and export behavior when relevant;
- relevant profiling/tests and dependency versions.

## Procedure

1. Record hardware, OS, driver/runtime, Python, PyTorch, ComfyUI commit, model, precision, workflow, and warm/cold state as relevant.
2. Establish a baseline before changing code.
3. Change one performance variable at a time where possible.
4. Measure repeated runs and report variance, not a single flattering result.
5. Separate prompt/setup/load time from steady-state execution when meaningful.
6. Track memory use alongside speed if an optimization trades one for the other.
7. Validate output correctness after optimization.
8. For model conversion or quantization work, verify that the target ComfyUI loader actually supports the produced artifact before making compatibility claims.

## Do not

- claim a speedup from code inspection alone;
- compare different workflows/models/hardware as if they were equivalent;
- hide OOMs, fallback paths, or reduced-quality settings in benchmark conclusions.

## Acceptance gate

Before claiming a performance improvement:

- record the test environment and target commit;
- record a baseline before the change;
- repeat the after measurement under equivalent conditions;
- report variance and relevant memory use;
- verify output correctness did not regress;
- do not claim a speedup from code inspection alone.

