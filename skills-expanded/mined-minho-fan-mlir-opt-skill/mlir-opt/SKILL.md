---
name: mlir-opt-skill
description: >
  Use when optimizing MLIR GPU performance, compiling PyTorch or linalg/tensor MLIR to PTX,
  writing Transform dialect schedules, tuning auxiliary pass pipelines, benchmarking MLIR kernels
  against PyTorch, or diagnosing linalg/torch-mlir GPU codegen.
---

# mlir-opt-skill

This file is the router. Keep it small: use it to choose tools and experience files,
then read the referenced module for details.

## First Reads

| Need | Read |
|---|---|
| Tool commands and workflow step mapping | `tools/TOOLS.md` |
| Compilation flags and examples | `tools/compilation/COMPILATION.md` |
| Benchmark/NCU flags and grid anomaly handling | `tools/measurement/MEASUREMENT.md` |
| Experience log and debug log commands | `tools/experience/EXPERIENCE.md` |
| All optimization experience indexes | `experience/EXPERIENCE.md` |
| Source-backed file map | `experience/source_map.md` |
| Final report template | `reference/final_report.md` |

## Hard Boundary

Optimization level policy:
- High-level IR is where the main optimization work belongs. Linalg/tensor IR keeps
  operator structure explicit, is easier to match with Transform handles, and still
  has a large scheduling space: fusion order, per-op tiling, per-dimension tiling,
  block/warp/thread mapping, packing/padding, promotion, vector/MMA, async/TMA, and
  operator-specific choices.
- Different operators may need different high-level schedules. Encode those choices
  in `vN/transform.mlir` while the payload IR is still structured enough to match and
  control precisely.
- Low-level IR is where the structure is already committed. Use traditional passes
  there for generic compiler work: canonicalization, CSE, cleanup, bufferization
  repair, alias folding, index sinking, outlining, lowering setup, and conservative
  repair.
- Overall flow: apply Transform dialect schedules first on high-level IR, then run the
  auxiliary pass pipeline for low-level cleanup and finalization. The main optimization
  artifact is `transform.mlir`; `pass_pipeline.txt` supports it.

Allowed optimization mechanisms:
- write or edit `vN/transform.mlir`;
- edit `vN/pass_pipeline.txt` only as an auxiliary low-level mechanism for cleanup,
  bufferization, outlining, lowering setup, and conservative repair;
- fix tools/runtime when semantics and ABI are preserved.

Pure GPU execution policy:
- `host_ops` are not an accepted fallback. Any residual host-side compute loop
  (`scf.parallel`, `scf.for`, or `affine.for` outside `gpu.module`) or host-side
  `memref.copy` in generated GPU host MLIR is a failed iteration that must be
  repaired.
- `ptx_config.py`, `benchmark.py`, and `ncu_profile.py` must reject configs that
  require `host_ops`. Correct results must be produced entirely by generated PTX
  GPU kernels launched through `gpu.launch_func`.
- If a frontend pattern such as inference BatchNorm leaves scalar/vector cleanup on
  the host, fix the high-level model/lowering path, e.g. BN folding, constant
  precomputation, Transform scheduling, or pass-pipeline repair. Do not replay it
  from Python/host code.

Do not hand-write or directly edit payload GPU/NVGPU/NVVM/PTX/CUDA/Triton kernels as an
optimization shortcut. In particular, do not create custom `gpu.module`, `gpu.func`,
`nvgpu.mma.sync`, shared-memory kernel bodies, or PTX by hand. Treat Transform dialect
as the first-class scheduling interface for optimization. Pass pipelines support the
schedule; they are not the primary search space. If Transform cannot express the needed
schedule, record the limitation instead of bypassing MLIR.

## Workflow

The loop is:

```text
env check -> PyTorch/linalg MLIR -> identify ops -> vN compile -> correctness ->
NCU profile -> classify -> route -> hypothesize -> record -> next vN
```

Use `tools/TOOLS.md` for exact commands. Use `tools/compilation/COMPILATION.md` for
`pytorch_to_mlir.py`, `mlir_tool.py`, and `ptx_config.py` details.

Correctness/precision policy:
- The accepted correctness mode is the tolerance or precision mode requested or approved
  by the user for the run.
- For NVIDIA Tensor Core routes, use the Tensor-Core-appropriate tolerance for the
  selected generated instruction path. The strict default FP32 tolerance is not the
  gate for accepting a Tensor Core candidate unless the user explicitly requires it.
- Generated TF32 MMA (`mma.sync...tf32`) that passes the Tensor-Core-approved tolerance
  is a successful completed result. Do not split reporting into "TF32 correctness
  passed" versus "FP32 correctness passed" categories.
- Still state the precision mode and exact `--atol` / `--rtol` in reports so the
  result is reproducible.

Sequential iteration rule:
- create only the current iteration directory;
- `v0` is initialized once from `experience/workflow/initialization_template.md`;
- every later `vN+1` is derived from the immediately previous completed or repaired
  iteration, not from a batch of independent candidates;
- `best_pipeline.txt` is for final tracking, not for choosing the next starting point.

## Fixed Output Contract

Use this exact output layout. Directory names and artifact filenames are part of the
skill contract: do not rename, move, merge, split, omit, or invent alternatives. If a
step is intentionally skipped, create the expected report file with the skip reason
instead of creating an ad-hoc filename.

```text
<output_dir>/
|-- env_check.md
|-- model_linalg.mlir
|-- v0/
|   |-- pass_pipeline.txt
|   |-- hypothesis.txt
|   |-- gpu.mlir
|   |-- kernels.ptx
|   |-- config.json
|   |-- benchmark.md
|   |-- ncu_summary.md
|   |-- ncu_details.md
|   `-- transform.mlir
|-- v1/
|   `-- same fixed files as v0
|-- vN/
|   `-- same fixed files as v0
|-- best_pipeline.txt
|-- best_transform.mlir
|-- benchmark.md
`-- final_report.md
```

Fixed file meanings:
- `env_check.md`: Step 1 environment record.
- `model_linalg.mlir`: Step 2 source lowering; generate once and treat as read-only
  during optimization iterations.
- `vN/pass_pipeline.txt`: the exact auxiliary pass pipeline for iteration `vN`.
- `vN/hypothesis.txt`: one hypothesis, expected effect, and reason for any skipped
  expected report.
- `vN/gpu.mlir`, `vN/kernels.ptx`, `vN/config.json`: Step 3 generated artifacts.
- `vN/benchmark.md`: Step 4 correctness and fast timing result.
- `vN/ncu_summary.md`, `vN/ncu_details.md`: Step 5 NCU result, or a short skip record
  when NCU is intentionally skipped because profiling would be invalid.
- `vN/transform.mlir`: always present and always passed to
  `mlir_tool.py --transform-schedule`. It contains the high-level Transform component
  of the iteration. For conservative initialization or repair iterations, use a
  minimal semantics-preserving Transform schedule that matches/anchors the target ops;
  do not write an `n/a` placeholder.
- `best_pipeline.txt`, `best_transform.mlir`, top-level `benchmark.md`, and
  `final_report.md`: final measured best and report artifacts.

Final reporting rules:
- use `reference/final_report.md` and keep its sections and tables stable;
- write `n/a` in non-applicable fields instead of deleting fields;
- `best_transform.mlir` must contain the measured best iteration's Transform schedule;
  do not write an `n/a` placeholder;
- do not add names such as `final.md`, `report_v2.md`, `best.ptx`, or `out.ptx`;
- do not overwrite previous `vN` directories when trying a new hypothesis.

## v0 Initialization

Before writing `v0/transform.mlir` or `v0/pass_pipeline.txt`, read:

1. `experience/operators/_index.md` and the matching operator module.
2. `experience/workflow/initialization_template.md`.
3. `experience/workflow/pipeline_reference.md` only if phase order or a template detail
   is unclear.

Do not default to the old weak SCF baseline for matmul, conv, pooling, or large
reductions. Prefer an operator-specific Transform seed when the guide provides one;
otherwise pair a conservative Transform schedule with the GPU-friendly auxiliary
pipeline to establish a correct base. A useful v0 should already:
- preserve Linalg/tensor structure long enough for legal fusion;
- use identity-layout bufferization for dense tensors when legal;
- avoid block=1 huge-grid launches;
- include index sinking and dead-kernel cleanup;
- leave a clean base for vectorization, shared memory, MMA/WGMMA, async copy, and
  later Transform schedule refinements.

Use minimal SCF lowering only as the auxiliary pass component for debugging or
tiny/simple elementwise-only graphs, and still pair it with `transform.mlir`.

## Operator Routing

After Step 2 creates `model_linalg.mlir`, identify ops:

```bash
grep -oP 'linalg\.\w+' <out_dir>/model_linalg.mlir | sort | uniq -c | sort -rn
```

Then read:

| Payload | Experience |
|---|---|
| Matmul/GEMM-like | `experience/operators/matmul/_index.md`; for Tensor Core routes, `experience/operators/matmul/mma_wgmma.md` |
| Conv | `experience/operators/conv/_index.md` |
| Reduction, softmax, norm, gather | `experience/operators/reduction/_index.md` |
| Elementwise | `experience/operators/elementwise/_index.md` |
| Pooling | `experience/operators/pooling/_index.md` |
| Multi-op graph/fusion | `experience/operators/fusion/_index.md` |

For matmul-like multiply-accumulate, read `experience/operators/matmul/mma_wgmma.md`
before scalar/affine auxiliary tuning. If PTX lacks `mma.sync`/`wgmma.mma_async` or NCU
Tensor Core utilization is zero, the next performance hypothesis should be Transform
MMA/WGMMA work unless the dtype/chip route is unsupported.

## Diagnose And Route

After a correct measured iteration:

1. Classify bottleneck with `experience/performance/bottleneck_guide.md`.
2. Read the matching detail guide:
   - `experience/performance/memory_bound.md`
   - `experience/performance/compute_bound.md`
   - `experience/performance/latency_bound.md`
3. Read `experience/workflow/optimization_router.md`.
4. Query learned outcomes with `tools/experience/experience_log.py recommend`.
5. Compose exactly one next hypothesis; see `experience/workflow/optimization_loop.md`.

Every optimization iteration combines `transform.mlir` for the high-level scheduling
decision with `pass_pipeline.txt` for supporting cleanup, broad generic fusion, index
sinking, symbol cleanup, bufferization repair, outlining/lowering setup, and
conservative affine/SCF repair. Use `transform.mlir` for optimization decisions:
op-specific scheduling, per-dimension tiling, block/warp/thread tiling,
packing/padding, promotion, vectorization/MMA, async/TMA, epilogue fusion order, or
row/tile-resident reductions.

## PTX

Efficient PTX instructions are validation targets for generated code, not source to
write by hand.

Read:
- `experience/ptx/_index.md` for PTX module routing;
- `experience/ptx/vectorization.md` before adding vectorization;
- `experience/ptx/instruction_families.md` for efficient PTX instruction families;
- `experience/ptx/validation.md` to accept or reject a PTX-focused hypothesis;
- `experience/lowering/gpu_to_nvvm_ptx.md` for Phase 4 lowering and bare-pointer ABI.

## Failure Handling

On compile, lowering, config, correctness, or measurement failure:

1. Read `experience/workflow/debugging.md`.
2. Use `tools/experience/debug_log.py check "<symptom>"`.
3. If new, record it with `tools/experience/debug_log.py add`.
4. Repair the current iteration before moving on.

Do not profile a pathological launch. If `config.json` shows block size 1 with huge grid,
repair launch shape before NCU; see `tools/measurement/MEASUREMENT.md`.

## Recording

Record every iteration outcome before choosing the next one:

- success, failure, neutral outcomes: `tools/experience/EXPERIENCE.md`;
- stopping criteria and one-variable rule: `experience/workflow/optimization_loop.md`;
- final report guidance: `tools/experience/EXPERIENCE.md` and the actual measured artifacts.
