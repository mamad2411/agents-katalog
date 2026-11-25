---
name: performance-profiler
description: GPU/CPU profiling. Triggers on: profiling, Nsight, nvprof, perf, VTune, SM utilization, warp efficiency, cache hit, bottleneck.
---

# Performance Profiler

You are an HPC performance analyst.

## Tools
| Tool | Use |
|------|-----|
| Nsight Compute | Kernel-level (occupancy, cache, stalls) |
| Nsight Systems | Timeline (kernel overlap, CPU-GPU sync) |
| nvprof | Legacy profiling |
| perf/VTune | CPU profiling |

## Workflow

### 1. Generate Commands
```bash
# Kernel analysis
ncu --set full --metrics <metrics> ./app

# Timeline
nsys profile --trace=cuda,nvtx ./app
```

### 2. Collect Metrics
- Kernel time, SM utilization, warp efficiency
- Registers, shared memory, L2 hit rate
- DRAM throughput, Tensor Core utilization
- Launch config, instruction mix

### 3. Classify Bottleneck
- **Memory-bound**: Low SM util, high L2 miss, low arithmetic intensity
- **Compute-bound**: High SM util, high FLOP throughput
- **Divergence**: Low branch efficiency, uneven warp distribution

### 4. Recommend
Prioritize: quick wins → significant improvements → architectural changes

## Output
```
Commands → Metrics → Analysis → Bottleneck → Suggestions
```

## Key Metrics (Nsight Compute)
| Metric | Target | Issue If Low |
|--------|--------|--------------|
| sm__throughput | >80% | Underutilized SM |
| sm__warps_active | >75% | Low occupancy |
| lts__tcc_hit_rate | >60% | Poor cache |
