---
name: triton-kernel-programming
description: Hands-on implementation template and API reference for writing, tuning, debugging, and benchmarking Triton GPU kernels. Covers the full triton.language API surface, autotuning patterns, profiling workflows, and production integration.
tags: [triton, gpu-kernel, matmul, softmax, fused-kernel, autotuning, cuda, rocm, benchmarking, deep-learning]
---

# Triton Kernel Programming

## Overview

This skill provides a hands-on reference for building production Triton kernels. It covers the `triton.language` API, autotune decorators, the `@triton.jit` compilation model, debugging/interpreter workflows, and `triton.testing` benchmarks.

## When to Use

Use this skill when:
- Implementing any custom GPU compute kernel in Triton
- Optimizing inference latency for small-batch transformer operations
- Fusing operations (e.g., matmul + activation, attention with softmax)
- Porting CUDA kernels to Triton for easier maintenance

Do not use for:
- Standard PyTorch operations that already run fast (use `torch.compile`)
- Distributed or multi-GPU parallelism patterns
- CPU-bound workloads

## Installation

```bash
# Triton ships with PyTorch ≥2.0. Install latest:
pip install -U triton

# Or build from source for latest features:
git clone https://github.com/triton-lang/triton.git
cd triton
pip install -r python/requirements.txt
pip install .

# For profiling:
pip install nvitools  # NVIDIA profiling helpers
pip install torch_tb_profiler  # PyTorch profiling
```

## Core API Reference

### `@triton.jit` Decorator

Compiles a Python function into a GPU kernel. All code inside must be valid Triton (subset of Python + `triton.language` ops).

```python
@triton.jit
def kernel(  # ← compiled kernel
    ptr,              # runtime arguments: pointers, scalars
    BLOCK: tl.constexpr,  # constexpr: baked in at compile time
):
    pid = tl.program_id(axis=0)  # SPMD program index
    ...
```

### `triton.language` (tl) — Key Operations

| Category | Operation | Description |
|----------|-----------|-------------|
| **Indexing** | `tl.program_id(axis)` | SPMD program index along axis 0, 1, or 2 |
| **Ranges** | `tl.arange(start, end)` | 1D range tensor for vectorized addressing |
| **Arithmetic** | `tl.sum`, `tl.max`, `tl.min`, `tl.argmax` | Block reduction along axis |
| **Arithmetic** | `tl.dot(a, b)` | Block matrix multiply (triggers tensor cores) |
| **Activation** | `tl.exp`, `tl.log`, `tl.sigmoid`, `tl.tanh` | Element-wise math |
| **Activation** | `tl.sqrt`, `tl.abs`, `tl.where` | Element-wise ops |
| **Memory** | `tl.load(ptr, mask=, other=)` | Vector load from global memory |
| **Memory** | `tl.store(ptr, val, mask=)` | Vector store to global memory |
| **Memory** | `tl.atomic_add(ptr, val)` | Atomic add (for reductions) |
| **Cast** | `tensor.to(tl.float16)` | Type conversion |
| **Cast** | `tl.cast(tensor, tl.float32)` | Explicit type conversion |
| **Debug** | `tl.device_print("x:", x)` | Runtime print |
| **Debug** | `tl.device_assert(cond, "msg")` | Runtime assertion |
| **Debug** | `tl.static_print(x)` | Compile-time print |
| **Debug** | `tl.static_assert(cond, "msg")` | Compile-time assert |

### Memory Operations — Masking Best Practice

```python
# Always mask loads/stores for safety:
mask = offsets < n_elements
x = tl.load(ptr + offsets, mask=mask, other=0.0)
# 'other' provides a safe default for out-of-bounds positions

# For matmul inner loop, use other=0.0 for partial tiles:
a = tl.load(a_ptrs, mask=offsets_k[None, :] < K - k, other=0.0)
b = tl.load(b_ptrs, mask=offsets_k[:, None] < K - k, other=0.0)
```

## Complete Kernel Templates

### Template 1: Element-wise Fusion (e.g., LayerNorm)

```python
@triton.jit
def layernorm_kernel(
    input_ptr, output_ptr, weight_ptr, bias_ptr,
    row_stride, n_cols, eps,
    BLOCK_SIZE: tl.constexpr,
):
    pid = tl.program_id(0)
    row_start = pid * row_stride
    offsets = row_start + tl.arange(0, BLOCK_SIZE)
    mask = tl.arange(0, BLOCK_SIZE) < n_cols

    x = tl.load(input_ptr + offsets, mask=mask, other=0.0)
    
    # Mean
    mean = tl.sum(x, axis=0) / n_cols
    # Variance
    x_shifted = x - mean
    var = tl.sum(x_shifted * x_shifted, axis=0) / n_cols
    # Normalize
    x_norm = x_shifted / tl.sqrt(var + eps)
    # Scale + shift
    w = tl.load(weight_ptr + tl.arange(0, BLOCK_SIZE), mask=mask)
    b = tl.load(bias_ptr + tl.arange(0, BLOCK_SIZE), mask=mask)
    y = x_norm * w + b
    
    tl.store(output_ptr + offsets, y, mask=mask)
```

### Template 2: Flash Attention-Style Softmax with Online Safe Computation

```python
@triton.jit
def fused_attention_kernel(
    q_ptr, k_ptr, v_ptr, output_ptr,
    stride_qh, stride_qd,
    stride_kh, stride_kd,
    stride_vh, stride_vd,
    stride_oh, stride_od,
    H, D,
    BLOCK_D: tl.constexpr,
    BLOCK_N: tl.constexpr,
):
    pid_h = tl.program_id(0)  # head index
    
    offs_d = tl.arange(0, BLOCK_D)
    offs_n = tl.arange(0, BLOCK_N)
    
    # Load Q block for this head
    q_ptrs = q_ptr + pid_h * stride_qh + offs_d[:, None] * stride_qd
    q = tl.load(q_ptrs)  # (BLOCK_D, 1)
    
    # Online safe softmax over KV sequence
    m_i = tl.full([BLOCK_N], -float('inf'), dtype=tl.float32)
    z_i = tl.zeros([BLOCK_N], dtype=tl.float32)
    acc = tl.zeros([BLOCK_D, BLOCK_N], dtype=tl.float32)
    
    for start_n in range(0, N, BLOCK_N):
        k_ptrs = k_ptr + pid_h * stride_kh + offs_n[None, :] * stride_kd + start_n * stride_kd
        k = tl.load(k_ptrs, mask=offs_n[None, :] < N - start_n, other=0.0)
        
        # S = Q @ K^T
        s = tl.dot(q.T, k)  # (1, BLOCK_N)
        
        # Online safe softmax
        m_ij = tl.maximum(m_i, s)
        p = tl.exp(s - m_ij)
        alpha = tl.exp(m_i - m_ij)
        acc = acc * alpha + p * k.T  # weighted accumulate
        z_i = z_i * alpha + p
        m_i = m_i * 0 + m_ij  # broadcast update
    
    output = acc / z_i
    
    # Store
    out_ptrs = output_ptr + pid_h * stride_oh + offs_d[:, None] * stride_od
    tl.store(out_ptrs, output)
```

### Template 3: FP8 GEMM with Split-K (Inference-Optimized)

```python
@triton.autotune(
    configs=[
        triton.Config({'BLOCK_SIZE_M': 64, 'BLOCK_SIZE_N': 128, 'BLOCK_SIZE_K': 64, 'SPLIT_K': 4}, num_warps=4),
        triton.Config({'BLOCK_SIZE_M': 32, 'BLOCK_SIZE_N': 128, 'BLOCK_SIZE_K': 64, 'SPLIT_K': 8}, num_warps=4),
        triton.Config({'BLOCK_SIZE_M': 16, 'BLOCK_SIZE_N': 64, 'BLOCK_SIZE_K': 128, 'SPLIT_K': 16}, num_warps=8),
    ],
    key=['M', 'N', 'K'],
    prune_configs_by={
        'early_config_prune': lambda configs, named_args: [
            c for c in configs if c.kwargs['BLOCK_SIZE_M'] * c.kwargs['SPLIT_K'] <= 128
        ],
    },
)
@triton.jit
def fp8_gemm_splitk_kernel(
    a_ptr, b_ptr, c_ptr, partial_ptr,
    M, N, K,
    stride_am, stride_ak,
    stride_bk, stride_bn,
    stride_cm, stride_cn,
    BLOCK_SIZE_M: tl.constexpr,
    BLOCK_SIZE_N: tl.constexpr,
    BLOCK_SIZE_K: tl.constexpr,
    SPLIT_K: tl.constexpr,
):
    pid = tl.program_id(0)
    num_pid_m = tl.cdiv(M, BLOCK_SIZE_M)
    k_block_id = pid // num_pid_m
    pid_m = pid % num_pid_m
    
    offs_m = pid_m * BLOCK_SIZE_M + tl.arange(0, BLOCK_SIZE_M)
    offs_n = tl.arange(0, BLOCK_SIZE_N)
    offs_k = k_block_id * BLOCK_SIZE_K + tl.arange(0, BLOCK_SIZE_K)
    
    a_ptrs = a_ptr + (offs_m[:, None] * stride_am + offs_k[None, :] * stride_ak)
    b_ptrs = b_ptr + (offs_k[:, None] * stride_bk + offs_n[None, :] * stride_bn)
    
    acc = tl.zeros((BLOCK_SIZE_M, BLOCK_SIZE_N), dtype=tl.float32)
    
    for k in range(0, K // SPLIT_K, BLOCK_SIZE_K):
        a = tl.load(a_ptrs, mask=offs_k[None, :] < K // SPLIT_K - k, other=0.0)
        b = tl.load(b_ptrs, mask=offs_k[:, None] < K // SPLIT_K - k, other=0.0)
        acc += tl.dot(a, b)
        a_ptrs += BLOCK_SIZE_K * stride_ak
        b_ptrs += BLOCK_SIZE_K * stride_bk
    
    # Write partial sum
    partial_idx = k_block_id * M + pid_m * BLOCK_SIZE_M
    partial_ptrs = partial_ptr + partial_idx
    tl.store(partial_ptrs, tl.sum(acc, axis=1)[:, None])
```

## Autotuning Strategy

### When Autotuning Is Essential

| Scenario | Autotune Impact |
|----------|----------------|
| Variable input shapes (VLLM, serving) | Critical — cache per shape |
| Fixed production shapes | Run once, freeze config |
| Memory-bound ops (softmax, norms) | Less critical — memory access pattern dominates |
| Compute-bound ops (GEMM) | Critical — 2–5x perf difference between configs |

### Config Design Heuristics

```python
# Rule of thumb: product of tile dimensions should fit in registers
# BLOCK_SIZE_M * BLOCK_SIZE_N * element_size <= register_budget

# For NVIDIA A100/H100 (fp16 matmul):
configs = [
    # Balanced: good all-around
    triton.Config({'BLOCK_SIZE_M': 128, 'BLOCK_SIZE_N': 128, 'BLOCK_SIZE_K': 32}, num_warps=4, num_stages=3),
    # Throughput: large tiles for compute-bound
    triton.Config({'BLOCK_SIZE_M': 128, 'BLOCK_SIZE_N': 256, 'BLOCK_SIZE_K': 64}, num_warps=8, num_stages=4),
    # Latency: small tiles for memory-bound / small M
    triton.Config({'BLOCK_SIZE_M': 32, 'BLOCK_SIZE_N': 64, 'BLOCK_SIZE_K': 32}, num_warps=4, num_stages=2),
    # AMD MI300X: use fewer warps, may need waves_per_eu
    triton.Config({'BLOCK_SIZE_M': 64, 'BLOCK_SIZE_N': 64, 'BLOCK_SIZE_K': 32}, num_warps=4, num_stages=0),
]
```

## Profiling Workflow

### Step-by-Step: Profile and Optimize

```python
# 1. Warmup: run once to trigger JIT compilation
output_triton = my_kernel(x, y)

# 2. Benchmark with triton.testing
import triton.testing
ms, min_ms, max_ms = triton.testing.do_bench(
    lambda: my_kernel(x, y),
    quantiles=[0.5, 0.2, 0.8],
    warmup=100,  # iterations
    rep=100,     # measurement iterations
)

# 3. Compare to reference
ms_torch, _, _ = triton.testing.do_bench(lambda: torch.matmul(a, b))

# 4. Compute TFLOPS
tflops = lambda ms: 2 * M * N * K * 1e-12 / (ms * 1e-3)
print(f"Triton: {tflops(ms):.2f} TFLOPS | Torch: {tflops(ms_torch):.2f} TFLOPS")
```

### CUDA Graph Integration (Production)

```python
# After autotuning has selected the best config, capture a CUDA graph:
import torch

def capture_gemm_graph(a, b):
    # Warm up with the production shape
    _ = triton_matmul(a, b)
    torch.cuda.synchronize()
    
    # Capture graph
    graph = torch.cuda.CUDAGraph()
    with torch.cuda.graph(graph):
        c = triton_matmul(a, b)
    
    return graph, c

# Replay for inference — eliminates 1-2ms JIT overhead per launch
graph.replay()
```

## Debugging Cheatsheet

| Problem | Symptom | Fix |
|---------|---------|-----|
| Wrong output | Off-by-one in offsets | Check `mask` logic, use `%` modulo for boundaries |
| NaN output | Numerical instability | Subtract max before exp; check division by zero |
| Slow kernel (memory-bound) | Low bandwidth util | Increase tile sizes, check `_b128` in ISA |
| Slow kernel (compute-bound) | Low TFLOPS | Check tensor core usage in PTX; try `num_stages` tuning |
| Compilation error | `@triton.jit` function issue | Check for unsupported Python constructs (no dictionaries, no dynamic indexing) |
| `compute-sanitizer` errors | Out-of-bounds access | Check mask coverage for partial tiles |
| High launch overhead | CPU-side latency | Use CUDA Graphs for production inference |

## Quality Gates

| Gate | Command/Check | Expected |
|------|--------------|----------|
| Correctness | `torch.max(torch.abs(ref - triton_out))` | `< 0.01` (fp16) or `< 0.5` (fp8) |
| Autotuning | `TRITON_PRINT_AUTOTUNING=1` env var | Best config printed |
| Tensor core usage | Check PTX for `wgmma`/`mma` | Present for matmul kernels |
| Memory coalescing | Check ISA for `global_load_dwordx4` | Present in hot loop |
| LDS usage | `grep "triton_gpu.shared"` from MLIR dump | `< 64 KB` |
| Occupancy | Compute from VGPR/LDS counts | `> 50%` for compute-bound |
| Speedup | `triton.testing.do_bench` | `> 1.5x` over naive PyTorch |

## Cross-References

- `triton-kernel-build-design` guideline — full design patterns, memory hierarchy, and optimization reference
- Official tutorials: https://triton-lang.org/main/getting-started/tutorials/
- `dataset-curation-manifest` — when building data-loading kernels
- `embedding-analysis` — for understanding embedding compute patterns

## References

| Resource | Link |
|----------|------|
| Triton Python API | https://triton-lang.org/main/python-api/ |
| Triton Autotune | https://triton-lang.org/main/python-api/generated/triton.autotune.html |
| Triton Tutorials | https://triton-lang.org/main/getting-started/tutorials/ |
| PyTorch User-Defined Triton | https://docs.pytorch.org/tutorials/recipes/torch_compile_user_defined_triton_kernel_tutorial.html |
| Triton Exercises | https://lweitkamp.github.io/triton_exercises/print.html |
| TK-GEMM (Llama3 FP8) | https://pytorch.org/blog/accelerating-llama3 |
