---
name: profile-kernel
description: >
  GPU kernel profiling workflow across supported kernel implementation languages. Provides commands
  for all 4 profiling modes (annotation, event, ncu, nsys), metric interpretation tables,
  bottleneck identification rules, and the output contract for returning compact results to the
  orchestrator.
  Use when: (1) profiling a kernel version, (2) interpreting profiling artifacts/reports,
  (3) comparing kernel versions, (4) identifying bottlenecks and optimization opportunities,
  (5) documenting performance in the development log.
---

# GPU Kernel Profiling

## GPU Clock Protocol

Always lock clocks before profiling. Always run one profiling at a time.

```bash
bash scripts/lock-gpu-clock.sh           # before profiling
bash scripts/reset-gpu-clock.sh          # after done
```

## Device Peaks

Shared profiling guidance should not hard-code a single device. Read the active device context from `params.json`, runtime profiling artifacts, and the configured peak-spec sources in `src/mla_var3/conf/devices.json`.

Use device-specific reference files in `docs/devices/` only when the measurement context matters. Ridge point remains:

```text
ridge_point = peak_tflops / peak_gbps
```

## Profiling Mode Decision Tree

| Mode | `--prof_type` | When to use | Output root |
|------|--------------|-------------|-------------|
| Annotation | `annotation` | **Default first pass.** Roofline + NCU metrics + comparison tables | `out/profiles/annotation/` |
| Event | `event` | Quick iteration timing (carries Python overhead) | `out/profiles/event/` |
| NCU | `ncu` | Deep investigation: full NCU sections, source annotations, optimization suggestions | `out/profiles/ncu/` |
| NSYS | `nsys` | Pipeline overlap, stream concurrency, launch ordering | `out/profiles/nsys/` |

**Selection rule**: Start with `annotation`. Use `event` for fast A/B comparison (not suitable for KernelPipeline/ConcurrentKernels). Use `ncu` when you need source-level analysis, Nsight Compute optimization suggestions, or CUDA insights. Use `nsys` for `ConcurrentKernels` overlap and stream concurrency analysis.

## Profiling Commands

### CLI entry point (all modes)

```bash
python -m mla_var3.kernel <kernel_package> [<version>] \
    --b=32 --s=16 --t=4096 --prof_type=<mode>

# Language-specific path when needed:
python -m mla_var3.kernel.<language_python_package>.mla.<kernel_package> [<version>] \
  --b=32 --s=16 --t=4096 --prof_type=<mode>
```

### Python API

```python
# Annotation
from mla_var3.runtime.profiling.annotation import annotation_profile_plan
prof_result = annotation_profile_plan(plan, out_dir=..., version=..., bench_runs=...)

# NCU
from mla_var3.runtime.profiling.ncu import ncu_profile_plan
prof_result = ncu_profile_plan(plan, out_dir=..., version=..., bench_runs=...)

# NSYS
from mla_var3.runtime.profiling.nsys import nsys_profile_plan
prof_result = nsys_profile_plan(plan, out_dir=..., version=..., bench_runs=...)
```
Notice that version is optional, and allows you to specify a custom version. This retrieves the right `KernelPlan` of the specified version, and uses that, NOT the `plan` passed to the function. This is just a convenience to automatize version profiling.
Alternatively, you can directly build the plan object using the class of the version to be profiled, and ignore the version argument. 
**Important**: sometimes, after auto-tuning, there might be some errors. In this case, you can simply re-run the command, the best autotune config is already cached and everything should work.

### Benchmark scripts

Benchmark scripts in `tests/benchmark/` are curated experiment drivers. Some accept CLI args, others are fixed scripts to copy and edit.

```bash
python -m tests.benchmark.bench_mla_var6_plus       # base version
python -m tests.benchmark.bench_mla_var6_plus_v4    # specific version
python -m tests.benchmark.bench_all_mla             # compare all kernels (slow)
```

## Output Artifacts

All modes write to `out/profiles/<mode>/<kernel>/<params>/<timestamp>/` if not ouptut directory is specified.

### Common artifacts (all modes)

- `params.json` — Full kernel parameter set (dtype, b, s, t, h, d, k, p). **Always read this** to confirm the profiling configuration, especially for NCU and NSYS modes whose `report.md` does not embed parameters.
- `tiling/<stage>.json` — Autotuned tiling config per stage
- `tiling/<stage>/autotuning.json` — Copied autotuning history from `.cache/kernel-autotune/...`, colocated with the selected tiling so you can inspect the explored configurations without leaving the profiling output directory
- `compiled/<stage>/` — MLIR and bytecode compilation artifacts

### Per-mode artifacts

Each mode produces different artifacts. See the per-mode reference for full details:
- [mode-annotation.md](references/mode-annotation.md) — report.md with per-kernel NCU metrics, roofline comparison, tiling;
- [mode-event.md](references/mode-event.md) — report.md with end-to-end roofline summary;
- [mode-ncu.md](references/mode-ncu.md) — report.md (compact diagnosis + NCU recommendations), report-verbose.md (full NCU sections), annotated source, per-kernel SASS metrics, PTX source files;
- [mode-nsys.md](references/mode-nsys.md) — report.md with timeline and overlap analysis;

## Metric Interpretation

| Metric | Healthy | If unhealthy → Issue | Optimization hint |
|--------|---------|---------------------|-------------------|
| TC Util | >60% | Memory or latency bound | Check DRAM%, occupancy |
| DRAM Throughput | >70% | Compute or latency bound | Check TC%, occupancy |
| Achieved Occupancy | >25% | Register/smem pressure | Reduce tile size, occupancy hint |
| L2 Hit Rate | >80% | Poor data reuse | Swizzle, larger tiles, data layout |
| Local Spilling | 0 bytes | Register overflow | Smaller tiles, fewer accumulators |
| Waves/SM | >1.0 | Underfilled GPU | More blocks, reduce per-block resources |

## Bottleneck Classification

| Pattern | Classification | Focus |
|---------|---------------|-------|
| DRAM% high + TC% low | **Memory-bound** | Data reuse, TMA hints, head grouping |
| TC% high + DRAM% low | **Compute-bound** | Kernel efficiency, tile sizes |
| Both low | **Latency-bound** | Occupancy, reduce spilling, more blocks |
| L2 hit < 80% | **Locality issue** | Swizzle scheduling, tile size adjustment |

## Profiler Output Contract

After profiling, return results to the orchestrator in this exact format.
Always read `params.json` to populate the configuration fields accurately.

```markdown
## Profile: [kernel] [version]

### Configuration
| b | s | t | dtype |
|---|---|---|-------|
| X | X | X | bfloat16 |

### Stages
| Stage | Duration (us) | TC% | DRAM% | Occ% | Bottleneck | Key Issue |
|-------|---------------|-----|-------|------|------------|-----------|

### Bottleneck: [Memory/Compute/Latency]-bound
Root cause: [2 sentences max]

### Top 3 Opportunities (ranked by estimated impact)
1. [name] — est. X% gain — trigger: [metric=value]
2. ...
3. ...

### vs Baseline (if applicable)
| Metric | Previous | Current | Change |
|--------|----------|---------|--------|
```

## Development Log Performance Template

Update the kernel's devlog (e.g., `docs/kernels/mla-var6-plus.md`) with:

```markdown
**Performance** (<device>, locked clocks if applicable, bfloat16, b=X, s=X, t=X):

| Metric            | Value   | vs Previous |
| ----------------- | ------- | ----------- |
| Duration          | X.XX μs | Y% faster   |
| Achieved TFLOPs/s | X.XX    | +Z%         |
| Achieved GB/s     | X.XX    | +Z%         |
| Occupancy         | XX%     | --          |
| TC Util           | XX%     | --          |

**Bottleneck**: [Memory-bound / Compute-bound / Latency-bound]

**Issues**:
- [Remaining problems]

**Insights**:
- [Key lessons — why optimization worked or didn't]
- [Guidance for next iteration]
```

## Detailed References

- **Annotation mode**: [references/mode-annotation.md](references/mode-annotation.md) — artifacts, report structure, reading guide
- **Event mode**: [references/mode-event.md](references/mode-event.md) — artifacts, limitations, reading guide
- **NCU mode**: [references/mode-ncu.md](references/mode-ncu.md) — artifacts, annotated source, per-kernel SASS metrics and PTX source files, reading guide
- **NSYS mode**: [references/mode-nsys.md](references/mode-nsys.md) — artifacts, CSVs, visualization, reading guide
