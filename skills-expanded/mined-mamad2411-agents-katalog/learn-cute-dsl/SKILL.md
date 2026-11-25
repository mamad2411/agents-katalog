---
name: learn-cute-dsl
description: >
  Workflow for learning CuTe Python DSL by reading, importing, profiling, and extracting
  reusable patterns from CUTLASS Blackwell example kernels. Use when: (1) studying
  CUTLASS CuTe DSL reference implementations, (2) importing CUTLASS examples into the
  project runtime infrastructure, (3) building CuTe DSL knowledge base entries from
  profiling experiments, (4) understanding CuTe DSL API patterns, TMA pipelining,
  warpgroup scheduling, or persistent kernel structure.
---

# Learn CuTe DSL from CUTLASS Examples

A structured workflow for building CuTe Python DSL fluency by reading CUTLASS Blackwell
examples, optionally importing them into the project's runtime infrastructure, profiling
them, and distilling reusable patterns into the knowledge base.

## Example Source

Vast examples live under `third_party/cutlass/examples/python/CuTeDSL`. Documentation is in `docs/cute-dsl/` (CuTe Python DSL) and `docs/cutlass-cpp/cute/` (CuTe C++ concepts).

| Category | Examples | Subdirectory |
| -------- | -------- | ------------ |
| MLA decode | `mla_decode_fp16.py`, `mla_decode_fp8.py`, `mla_helpers.py` | `mla/` |
| Attention | `fmha.py`, `fmha_bwd.py` | (top-level) |
| Mixed attention | `mixed_input_fmha_decode.py`, `mixed_input_fmha_prefill_*.py` | `mixed_input_fmha/` |
| GEMM (basic) | `dense_gemm.py` | (top-level) |
| GEMM (pipelined) | `dense_gemm_software_pipeline.py` | (top-level) |
| GEMM (persistent) | `dense_gemm_persistent.py`, `dense_gemm_persistent_prefetch.py` | (top-level) |
| GEMM (dynamic persistent) | `dense_gemm_persistent_dynamic.py` | (top-level) |
| GEMM tutorials | `fp16_gemm_0.py` through `fp16_gemm_6.py` | `tutorial_gemm/` |
| Block-scaled GEMM | `dense_blockscaled_gemm_persistent.py`, `*_prefetch.py`, `*_amax.py` | (top-level) |
| Mixed-input GEMM | `mixed_input_gemm.py`, `grouped_mixed_input_gemm.py` | `mixed_input_gemm/` |
| Epilogues | `custom_epilogue_dense_gemm.py`, `activation_custom_epilogue_dense_gemm.py` | `epilogue/` |
| Reduction | `reduce.py`, `rmsnorm.py` | (top-level) |
| Dependent launch | `programmatic_dependent_launch.py` | (top-level) |
| Mamba2 | `mamba2_ssd.py` | `mamba2_ssd/` |
| Blockwise GEMM | `blockwise_gemm.py`, `contiguous_grouped_gemm.py` | `blockwise_gemm/` |

Other examples can be provided by the user directly.


## Workflow

```text
1. SELECT    -> Pick examples based on learning goals
2. READ      -> Read and annotate, identify CuTe DSL patterns
3. IMPORT    -> (Optional) Wrap in CuteKernel + KernelPlan for profiling
4. PROFILE   -> Profile imported kernels, compare with existing cuTile versions
5. EXTRACT   -> Distill reusable CuTe DSL patterns and anti-patterns
6. DOCUMENT  -> Update knowledge base (docs/knowledge/languages/cute-dsl/)
```

---

## Step 1: SELECT

Pick examples based on what you need to learn.

| Learning goal | Start with |
| ------------- | ---------- |
| CuTe DSL basics (grid, TMA, MMA) | `tutorial_gemm/fp16_gemm_0.py` through `fp16_gemm_6.py` |
| Software pipelining | `dense_gemm_software_pipeline.py` |
| Persistent kernel structure | `dense_gemm_persistent.py` |
| Warpgroup specialization | `dense_gemm_persistent_prefetch.py` |
| TMA pipelining for attention | `fmha.py` |
| MLA decode (direct reference) | `mla/mla_decode_fp16.py` + `mla/mla_helpers.py` |
| MLA decode with FP8 | `mla/mla_decode_fp8.py` |
| Cluster programming | `dense_gemm_persistent_dynamic.py` |
| Custom epilogues | `epilogue/custom_epilogue_dense_gemm.py` |
| Dependent kernel launch | `programmatic_dependent_launch.py` |

Before reading, write down specific questions. Examples:

- "How does the MLA decode kernel set up TMA descriptors for the KV cache?"
- "How are warpgroups assigned producer/consumer roles in persistent GEMM?"
- "What barrier pattern does FMHA use for the K-loop pipeline?"

---

## Step 2: READ

For each selected example, read the full source and annotate these CuTe DSL-specific aspects:

### Host side (`@cute.jit`)

1. **TMA descriptor creation** -- which tensors get TMA descriptors, what are the tile shapes?
2. **Grid and cluster dimensions** -- how is the grid computed, is clustering used?
3. **Shared memory size** -- how is the SMEM budget calculated from pipeline stages and tile shapes?
4. **Launch parameters** -- `max_register_count`, cluster shape, SMEM carveout

### Device side (`@cute.kernel`)

1. **Thread/warp/warpgroup identity** -- how are roles assigned?
2. **Pipeline structure** -- number of stages, barrier initialization, producer/consumer loops
3. **TMA operations** -- `cute.copy(tma_desc, ...)`, arrival patterns
4. **MMA operations** -- accumulator setup, MMA loop body, epilogue
5. **Synchronization** -- `cute.barrier_arrive()`, `cute.barrier_wait()`, `cute.cluster_barrier_*`
6. **Shared memory layout** -- allocation, swizzling, partitioning across warpgroups

### Pattern checklist

While reading, flag instances of:

- [ ] TMA multi-stage pipeline (how many stages, barrier per stage)
- [ ] Warpgroup specialization (which warpgroups produce, which consume)
- [ ] Persistent kernel main loop (work tile scheduling, exit condition)
- [ ] Online softmax or streaming accumulation
- [ ] Register-level accumulator management
- [ ] Shared memory swizzle patterns
- [ ] Cluster-level communication (distributed shared memory)
- [ ] Epilogue pattern (in-register, through SMEM, or fused)
- [ ] Boundary handling (predication, masking for partial tiles)
- [ ] Pipeline drain (how the last pipeline stages are flushed)

### Cross-reference

Check whether patterns already exist in the knowledge base:

- `docs/knowledge/optimizations/` -- shared patterns (e.g., pipeline-driven-low-occupancy)
- `docs/knowledge/languages/cute-dsl/` -- existing CuTe DSL overlays

Note whether the example confirms, refines, or contradicts existing knowledge.

---

## Step 3: IMPORT (Optional)

Import a CUTLASS example into the project to make it runnable through the standard CLI and profiling infrastructure.

### When to import

- You want to profile the example on your hardware
- You want a starting point for a custom CuTe DSL kernel
- The example covers a workload comparable to existing cuTile kernels (e.g., MLA decode)

### When NOT to import

- You only need to understand the pattern, not benchmark it
- The example has complex dependencies or helper infrastructure that doesn't map cleanly

### Import procedure

1. **Create the kernel package**:

   ```
   src/mla_var3/kernel/cute_python/<layer>/<design>/<design>/
   ```

   Example for CUTLASS MLA decode FP16:

   ```
   src/mla_var3/kernel/cute_python/mla/cutlass_mla_decode/cutlass_mla_decode/
   ```

2. **Create the KernelPlan subclass** (`cutlass_mla_decode.py`):

   - `prepare_inputs()` -- allocate tensors matching the example's expected shapes (Q, KV cache, output)
   - `reference_fn()` -- PyTorch reference for correctness
   - `_autotune_configs()` -- tiling parameters from the example
   - `_algorithmic_flops_bytes()` -- roofline analysis
   - `plan()` -- return a `CuteKernel` wrapping the example's host/device functions

3. **Create `__main__.py`**:

   ```python
   from .cutlass_mla_decode import CutlassMlaDecodeKernel

   if __name__ == "__main__":
       kernel_plan = CutlassMlaDecodeKernel()
       kernel_plan.benchmark_kernel_argparse()
   ```

4. **Create `__init__.py`** at each package level

5. **Handle helper modules**: If the example uses helpers (e.g., `mla_helpers.py`), either:
   - Copy into the kernel package and adjust imports
   - Import from the CUTLASS path (fragile but faster for exploration)

6. **Test correctness**:

   ```bash
   source .venv/bin/activate && python -m mla_var3.kernel cutlass_mla_decode --prof_type=disabled --check
   ```

---

## Step 4: PROFILE

### Architecture compatibility check

Before profiling, verify the available device matches the kernel's target architecture:

```bash
nvidia-smi --query-gpu=name --format=csv,noheader
```

Many CUTLASS examples (especially those in `mla/`, and any using `tcgen05` MMA ops) target **SM100** (B200, B300 datacenter GPUs) specifically. Be aware that "Blackwell" is a marketing name spanning multiple SM versions with **different instruction sets**:

- **SM100** (B200, B300) — datacenter GPUs, supports `tcgen05` MMA, TMEM, full cluster features
- **SM120** (GeForce RTX 5090, RTX 5080) — consumer Blackwell, uses `sm_120a`, does **not** support `tcgen05` ops

A kernel using `tcgen05` ops will **not** run on an RTX 5090 (SM120) despite both being marketed as "Blackwell". Match the GPU name to its actual SM version, not the marketing generation.

If the kernel's target SM version does not match the available device, **skip the PROFILE step entirely** — execution will either fail at compile time or produce misleading results. In that case, proceed directly to Step 5 (EXTRACT) with insights from reading the source code only, and note the architecture mismatch in any documentation.

### Profiling sequence

1. Lock GPU clocks: `bash scripts/lock-gpu-clock.sh`
2. Annotation mode first:

   ```bash
   source .venv/bin/activate && python -m mla_var3.kernel <kernel> \
       --b=32 --s=1 --t=4096 --prof_type=annotation
   ```

3. NCU deep dive if annotation reveals interesting patterns:

   ```bash
   source .venv/bin/activate && python -m mla_var3.kernel <kernel> \
       --b=32 --s=1 --t=4096 --prof_type=ncu
   ```

### Focus areas

Since the goal is learning (not just benchmarking), focus on understanding **how** the kernel achieves its performance:

- **Pipeline efficiency**: Are TMA copies fully overlapped with compute? Check for idle bubbles in the nsys timeline.
- **Warpgroup utilization**: Are all warpgroups busy? Check scheduler statistics in NCU.
- **Register pressure vs occupancy tradeoff**: How many registers per thread? Is low occupancy intentional?
- **SMEM usage**: How much of the available SMEM budget is used? How many pipeline stages fit?
- **MMA throughput**: What fraction of peak TC utilization is achieved?

### Compare with cuTile versions

If the imported kernel covers a workload that exists in cuTile (e.g., MLA decode), compare:

| Metric | cuTile version | CUTLASS CuTe DSL | Delta | Insight |
| ------ | -------------- | ----------------- | ----- | ------- |
| Duration (us) | | | | |
| TC% | | | | |
| DRAM% | | | | |
| Occupancy | | | | |
| Registers/thread | | | | |
| SMEM/block (KB) | | | | |

Differences reveal what explicit control (warpgroup scheduling, TMA pipelining) buys over cuTile's block-level abstraction.

---

## Step 5: EXTRACT

Distill observations into reusable CuTe DSL patterns.

### Classification

| Type | Destination |
| ---- | ----------- |
| Shared algorithmic/hardware pattern | `docs/knowledge/optimizations/<name>.md` |
| Shared failure mode | `docs/knowledge/anti-patterns/<name>.md` |
| CuTe DSL API pattern or implementation detail | `docs/knowledge/languages/cute-dsl/optimizations/<name>.md` |
| CuTe DSL trap or pitfall | `docs/knowledge/languages/cute-dsl/anti-patterns/<name>.md` |

Most patterns from CUTLASS examples will be **CuTe DSL-specific** (the API patterns, TMA setup idioms, barrier choreography). Shared patterns (algorithmic insights like pipeline-driven scheduling) may already exist from cuTile work.

### Extraction criteria

Document a pattern if it:

- **Transfers** to other CuTe DSL kernels (not just this one example)
- **Is non-obvious** from the CuTe DSL documentation alone
- **Has performance implications** visible in profiling or architecturally clear
- **Refines** an existing shared pattern with CuTe DSL-specific implementation details

### Pattern template

```markdown
# [Pattern Name]

## When to Apply
- [CuTe DSL kernel type, workload shape, bottleneck condition]

## Mechanism
[How the pattern works in CuTe DSL -- reference specific APIs]

## Affected Metrics
- [Metric 1]
- [Metric 2]

## Implementation
```python
# CuTe DSL code snippet, generalized from the CUTLASS example
```

## Source
[CUTLASS example name and path]

## Performance Evidence
Source: [example name, device, configuration]
| Config | Metric | Value | Context |
|--------|--------|-------|---------|

## Generalization
[Device-agnostic takeaway]

## Pitfalls
- [CuTe DSL-specific failure modes]

## Interactions
- [How this interacts with other CuTe DSL patterns]
```

---

## Step 6: DOCUMENT

1. Write pattern files to `docs/knowledge/languages/cute-dsl/optimizations/` or `anti-patterns/`
2. Update the index in `/optimization-catalog-cute-dsl`
3. If a pattern is shared (not DSL-specific), write to `docs/knowledge/optimizations/` and update `/optimization-catalog`
4. If you imported and profiled a kernel, write a devlog entry in `docs/kernels/`:

```markdown
# [Kernel Name] (Imported from CUTLASS)

## Overview
[What this kernel does and why it was imported for study]

## Source
Original: `third_party/cutlass/examples/python/CuTeDSL/<path>`
Imported: `src/mla_var3/kernel/cute_python/mla/<design>/`

## Performance
[Profiling results table]

## Patterns Extracted
- [Pattern] -> `docs/knowledge/languages/cute-dsl/optimizations/<name>.md`

## Insights
[What was learned that informs future CuTe DSL kernel design]
```

---

## Recommended Learning Paths

### Path A: CuTe DSL fundamentals

For building basic fluency before writing any MLA kernel:

```text
1. tutorial_gemm/fp16_gemm_0.py  -> Minimal kernel: grid, TMA load, MMA, store
2. tutorial_gemm/fp16_gemm_3.py  -> Software pipelining basics
3. tutorial_gemm/fp16_gemm_6.py  -> Full persistent GEMM with warpgroup specialization
4. dense_gemm_software_pipeline.py -> Production-quality pipelining
5. dense_gemm_persistent.py      -> Persistent scheduling pattern
```

### Path B: MLA-specific patterns

For directly studying how CUTLASS implements MLA:

```text
1. mla/mla_helpers.py            -> Shared utilities, tensor layouts, TMA setup
2. mla/mla_decode_fp16.py        -> FP16 MLA decode with full pipeline
3. mla/mla_decode_fp8.py         -> FP8 variant (quantization handling)
4. fmha.py                       -> Attention forward (different design choices)
```

### Path C: Advanced patterns

For specific optimization techniques:

```text
1. dense_gemm_persistent_prefetch.py  -> Prefetching in persistent kernels
2. dense_gemm_persistent_dynamic.py   -> Dynamic tile scheduling + clusters
3. epilogue/custom_epilogue_dense_gemm.py -> Fused epilogue patterns
4. programmatic_dependent_launch.py   -> Dependent kernel launch
```
