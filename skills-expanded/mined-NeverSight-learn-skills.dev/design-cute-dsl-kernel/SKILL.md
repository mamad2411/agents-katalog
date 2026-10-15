---
name: design-cute-dsl-kernel
description: >
  CuTe Python DSL kernel workflow, CuteKernel runtime wrapper, suitability gate, tiling
  guidance, and CuTe-specific pitfalls. Use when: (1) planning or implementing a kernel
  in the CuTe Python DSL, (2) the optimization needs more explicit control than cuTile
  exposes but should remain in a Python-driven workflow, (3) defining package naming for
  cute-dsl kernels, (4) documenting CuTe Python DSL design choices, (5) recording
  language-specific knowledge for CuTe Python DSL.
---

# CuTe Python DSL Kernel Design

Always also load `/design-kernel` for shared naming, versioning, and workflow.
Also load `/cute-dsl-ref` for API reference, execution model, and architecture operations.

## When To Use CuTe Python DSL

Use CuTe Python DSL (`cute-dsl`) when cuTile's public control surface is no longer sufficient, but a Python-authored kernel workflow is still appropriate.

### Suitability Gate

CuTe DSL is the right choice when the next optimization requires any of these controls that cuTile does **not** expose:

- **Thread/warp/warpgroup identity** -- explicit control over which threads do what
- **Intra-CTA synchronization** -- barriers, named barriers, arrive/wait patterns
- **Warpgroup scheduling** -- producer/consumer warpgroup roles, persistent warpgroup loops
- **TMA pipeline control** -- explicit multi-stage async copy pipelines with barrier synchronization
- **Cluster programming** -- cross-CTA shared memory access, distributed shared memory
- **Register-level data movement** -- explicit register-to-register shuffles, warp-level primitives
- **Custom epilogues** -- fused post-processing with fine-grained control

### When to stay in cuTile instead

If the optimization is still expressible through tile sizes, CTA remapping, `occupancy`/`num_ctas` hints, latency hints, or `allow_tma` flags, stay in cuTile. CuTe DSL adds complexity -- use it only when that complexity is load-bearing.

### Hard design constraint

When profiling shows 1 CTA/SM, low eligible warps, and the fix requires explicit warpgroup or barrier scheduling, cuTile cannot close the gap. This is the canonical trigger to switch to CuTe DSL.

## Naming And Layout

- Public language key: `cute-dsl`
- Python package path: `cute_python`
- Kernel layout: `src/mla_var3/kernel/cute_python/<layer>/<design>/<design>[_vN]/`
- Module: `<design>[_vN].py`
- Wrapper: `CuteKernel`

## CuteKernel Runtime Pattern

The runtime wrapper lives at `src/mla_var3/runtime/cute_kernel.py`.

CuTe DSL kernels use a **two-level host/device pattern**:
1. A `@cute.jit` host function sets up TMA descriptors, computes the grid, and launches the kernel
2. A `@cute.kernel` device function contains the GPU code

The `CuteKernel` dataclass wraps this pattern:

```python
from mla_var3.runtime.cute_kernel import CuteKernel

# In KernelPlan.plan():
def plan(self, *inputs):
    # Build a closure that captures inputs and calls the host function
    def launch_fn(tiling):
        # Convert tensors, set up TMA descriptors, compute grid
        host_fn(tiling, *converted_inputs)

    return CuteKernel(
        kernel_fn=device_kernel,       # The @cute.kernel function (for naming)
        launch_fn=launch_fn,           # Closure: (tiling) -> launches kernel
        input_tensors=list(inputs),
        output_tensors=[output],
        tiling=self.tiling,
        autotune_configs=self._autotune_configs(),
        algorithmic_flops_bytes_fn=self._algorithmic_flops_bytes,
    )
```

### Key differences from CtKernel

| Aspect | CtKernel (cuTile) | CuteKernel (CuTe DSL) |
|--------|-------------------|----------------------|
| Launch mechanism | `grid_fn` + `args_fn` + cuTile compiler | `launch_fn` closure wrapping `@cute.jit` host |
| Compilation | cuTile bytecode + MLIR | CuTe DSL JIT (cached automatically) |
| Autotuning | `autotune_launch()` from cuda.tile_experimental | `triton.testing.do_bench_cudagraph` per config |
| Grid setup | `grid_fn(cfg) -> (x, y, z)` | Inside `launch_fn` / host function |
| TMA descriptors | Implicit (cuTile handles) | Explicit setup in host function |

### Autotuning

CuteKernel iterates over `autotune_configs`, benchmarks each via `do_bench_cudagraph`, and selects the fastest. Failed configs are caught and skipped.

### Compile

CuTe DSL JIT caches artifacts automatically. The `compile()` method creates the output directory but does not extract explicit artifacts (can be extended per-kernel).

## Tiling Dataclass Guidance

CuTe DSL tilings typically include fields that cuTile tilings do not:

```python
@dataclass
class Tiling:
    # Standard tile dimensions
    tile_m: int
    tile_n: int
    tile_k: int

    # CuTe DSL-specific fields
    num_warpgroups: int          # Warpgroups per CTA (typically 2-4)
    num_pipeline_stages: int     # Async copy pipeline depth
    num_tma_buffers: int         # TMA double/triple buffering
    cluster_m: int = 1           # Cluster shape (M dimension)
    cluster_n: int = 1           # Cluster shape (N dimension)

    def validate(self, pd) -> bool:
        # Validate against problem dimensions and device limits
        ...
```

The exact fields depend on the kernel design. The `validate` method should check that tile dimensions divide evenly into problem dimensions and that resource usage (registers, SMEM) stays within device limits.

## Architecture Compatibility Check

Kernels may target architecture-specific instructions that require a specific SM version. The "Blackwell" marketing name spans multiple SM versions with **different instruction sets**:

- **SM100** (B200, B300) — datacenter GPUs, supports `tcgen05` MMA, TMEM, full cluster features
- **SM120** (GeForce RTX 5090, RTX 5080) — consumer Blackwell, uses `sm_120a`, does **not** support `tcgen05` ops

A kernel using `tcgen05` ops requires SM100 and will **not** run on an RTX 5090 (SM120) despite both being "Blackwell".

Before running, compiling, or profiling a CuTe DSL kernel, always verify the available device:

```bash
nvidia-smi --query-gpu=name --format=csv,noheader
```

Then match the GPU name to its SM version. If the kernel's target SM version does not match, **skip the run/profiling step**. Do not attempt execution — it will either fail at compile time or produce misleading results. Record the architecture requirement in the kernel's devlog and note the skip.

## Common Pitfalls

- Never hallucinate CuTe DSL APIs -- verify against the `/cute-dsl-ref` skill, `docs/cute-dsl/` documentation, or CUTLASS example kernels
- `@cute.kernel` function name MUST match the module filename (same rule as cuTile)
- TMA descriptor setup is host-side only -- do not attempt TMA operations inside `@cute.kernel` without proper `@cute.jit` host setup
- Register budget: 255 max/thread, validate against the active device's SM limits via `docs/devices/` and `src/mla_var3/conf/devices.json`
- Shared memory varies by SM version: SM100 (B200/B300): up to 228 KB/SM, 227 KB/block opt-in; SM120 (RTX 5090): 96 KB -- do not assume "Blackwell" means datacenter SMEM limits
- Pipeline stage count affects SMEM usage (each stage needs its own buffer) -- validate total SMEM before increasing stages
- Barrier synchronization errors are silent and cause incorrect results, not crashes -- always test with `--check`
- Cluster programming requires the launch to use cluster-compatible grid dimensions

## Reference Resources

- **API reference**: Load `/cute-dsl-ref` for the core API table, execution model, and architecture operations
- **Official documentation**: `docs/cute-dsl/` (CuTe Python DSL) and `docs/cutlass-cpp/cute/` (CuTe C++ concepts)
- **Example kernels and learning paths**: Load `/learn-cute-dsl` for a categorized index of CUTLASS example kernels

## Knowledge Links

- Shared optimization knowledge: `docs/knowledge/optimizations/`
- Shared anti-patterns: `docs/knowledge/anti-patterns/`
- CuTe Python DSL overlays: `docs/knowledge/languages/cute-dsl/`

## Development Log Entry

Use `docs/kernels/<kernel>.md` and record the implementation location using the Python package path form:

```text
src/mla_var3/kernel/cute_python/mla/<kernel>/<kernel>[_vN]/
```
