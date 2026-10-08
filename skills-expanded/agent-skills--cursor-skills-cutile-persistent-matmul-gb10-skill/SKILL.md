# cuTile Persistent MatMul on GB10 DGX Spark

## Overview

Persistent kernels keep a tile block alive and process multiple output tiles in a strided loop. This is the dominant pattern for peak GEMM throughput in cuTile.

## Key pattern

```python
import cupy as cp
import cuda.tile as ct

@ct.kernel
def persistent_matmul(A, B, C, tm, tn, tk):
    bid = ct.bid(0)
    num_bid_m = ct.cdiv(A.shape[0], tm)
    num_bid_n = ct.cdiv(B.shape[1], tn)
    upper_bound = num_bid_m * num_bid_n
    num_blocks = ct.num_blocks(0)

    for current_bid in range(bid, upper_bound, num_blocks):
        bidx = ...  # swizzled 2-D tile index
        bidy = ...
        acc = ct.full((tm, tn), 0, dtype=ct.float32)
        for k in range(ct.num_tiles(A, axis=1, shape=(tm, tk))):
            a = ct.load(A, (bidx, k), (tm, tk)).astype(ct.tfloat32)
            b = ct.load(B, (k, bidy), (tk, tn)).astype(ct.tfloat32)
            acc = ct.mma(a, b, acc)
        ct.store(C, (bidx, bidy), acc.astype(C.dtype))
```

## Launch

```python
num_sm = cp.cuda.runtime.getDeviceProperties(0)['multiProcessorCount']
num_blocks = min(2 * num_sm, (M // tm) * (N // tn))
ct.launch(stream, (num_blocks, 1, 1), persistent_matmul, (A, B, C, tm, tn, tk))
```

## Tuning notes

- Use FP16 inputs and FP32 accumulation for max Tensor Core throughput.
- Launch **2 waves of blocks** (`2 * num_sm`); fewer waves leaves SMs idle, too many waves adds scheduling overhead.
- Tile sizes 64×64×32 or 64×64×64 are good starting points.
- Use `ct.tfloat32` for FP32 inputs to ensure Tensor Core use.

## Verification

Compare against `A.astype(cp.float32) @ B.astype(cp.float32)`. Tolerance ~1.0 for FP16 1024³.

## Reference

- `cuda-blackwell-labs/projects/37_cutile_advanced/`
- https://github.com/NVIDIA/cutile-python/blob/main/samples/MatMul.py
- https://docs.nvidia.com/cuda/cutile-python/performance.html

