---
name: cute-dsl-ref
description: >
  CuTe Python DSL API reference and implementation patterns for NVIDIA GPU kernel programming.
  Provides execution model, core API table, key constraints, common patterns, and documentation
  index. Use when: (1) writing or modifying CuTe DSL kernel code, (2) looking up CuTe DSL API
  syntax, (3) implementing attention/GEMM/MLA patterns in CuTe DSL, (4) understanding CuTe DSL
  execution model and compilation pipeline, (5) checking what CuTe DSL can and cannot do.
---

# CuTe Python DSL Reference

## Execution Model

CuTe Python DSL is the Python surface for NVIDIA's CuTe layout algebra. Unlike cuTile's block-level abstraction, CuTe DSL exposes **explicit thread/warp/warpgroup control**, TMA pipelines, barrier choreography, and shared memory management.

### Two-Level Host/Device Pattern

Every CuTe DSL kernel has two functions:

1. **`@cute.jit` host function** — runs on CPU, sets up TMA descriptors, computes grid, allocates shared memory, launches the kernel
2. **`@cute.kernel` device function** — runs on GPU, contains the actual computation

```python
import cutlass
import cutlass.cute as cute

@cute.kernel
def my_kernel(tiled_mma: cute.TiledMma, ...):
    tidx, _, _ = cute.arch.thread_idx()
    bidx, bidy, _ = cute.arch.block_idx()
    # ... GPU code

@cute.jit
def host_fn(a: cute.Tensor, b: cute.Tensor, c: cute.Tensor):
    # Setup TMA descriptors, compute grid, allocate SMEM
    my_kernel(...).launch(grid=grid_shape, block=block_shape, smem=smem_bytes)
```

### Compilation Pipeline

Three-stage JIT compilation:
1. **Pre-Staging**: Python AST rewriting
2. **Meta-Stage**: Python interpreter executes meta-programs (compile-time constants resolved)
3. **Object-Stage**: Compiler backend generates PTX → SASS

JIT artifacts are cached automatically. Control with `CUTE_DSL_CACHE_DIR` and `CUTE_DSL_DISABLE_FILE_CACHING`.

### Key Difference from cuTile

| Aspect | cuTile | CuTe DSL |
|--------|--------|----------|
| Abstraction level | Block-level (no thread identity) | Thread/warp/warpgroup level |
| TMA | Implicit (`allow_tma=True`) | Explicit descriptor setup in host |
| Shared memory | Compiler-managed | Explicit allocation and layout |
| Synchronization | None exposed | Barriers, arrive/wait, named barriers |
| Pipeline | None exposed | Explicit multi-stage async pipelines |
| MMA | `ct.mma(A, B, C)` on tiles | `cute.gemm(tiled_mma, d, a, b, c)` on partitioned fragments |
| Compilation | cuTile bytecode → MLIR | CuTe DSL JIT → PTX → SASS |

---

## Core API Table

### Decorators and Compilation

| API | Purpose | Key params |
|-----|---------|-----------|
| `@cute.kernel` | Device kernel decorator | function name must match module filename |
| `@cute.jit` | Host JIT function decorator | — |
| `kernel(...).launch(grid, block, smem, cluster)` | Launch kernel | `grid=(x,y,z)`, `block=(threads,1,1)`, `smem=bytes`, `cluster=(cx,cy,cz)` |
| `cute.compile(fn, *args, options="...")` | Ahead-of-time compile | `"opt-level=3"`, `"keep-ptx"`, etc. |

### Thread/Block/Grid Indexing

| API | Purpose |
|-----|---------|
| `cute.arch.thread_idx()` | Returns `(tidx, tidy, tidz)` |
| `cute.arch.block_idx()` | Returns `(bidx, bidy, bidz)` |
| `cute.arch.block_dim()` | Block dimensions |
| `cute.arch.grid_dim()` | Grid dimensions |
| `cute.arch.warp_idx()` | Warp index within block |
| `cute.arch.block_idx_in_cluster()` | Block index within cluster (Hopper+) |

### Layout and Tensor Construction

| API | Purpose | Notes |
|-----|---------|-------|
| `cute.make_layout(shape, stride)` | Create layout | Core abstraction: maps coordinates → indices |
| `cute.make_ordered_layout(shape, order)` | Create with stride order | e.g., `order=(1,0)` for column-major |
| `cute.make_identity_layout(shape)` | Identity layout | For predication |
| `cute.make_tensor(ptr, layout)` | Create tensor view | Pairs pointer + layout |
| `cute.make_fragment(layout, dtype)` | Allocate register tensor | For accumulators |
| `cute.make_fragment_like(src, dtype)` | Register tensor matching source | — |
| `cute.make_ptr(dtype, addr, memspace)` | Tagged pointer | `cute.AddressSpace.smem/gmem` |
| `cute.from_dlpack(tensor)` | Convert PyTorch/JAX tensor | Returns `cute.Tensor` with `.mark_layout_dynamic()` |

### Layout Algebra

| API | Purpose |
|-----|---------|
| `cute.size(t, mode=None)` | Total size or modal size |
| `cute.shape(t)` | Get shape tuple |
| `cute.stride(t)` | Get stride tuple |
| `cute.rank(t)` | Number of modes |
| `cute.local_tile(tensor, tiler, coord, proj)` | Extract block's tile |
| `cute.logical_divide(tensor, divisor)` | Divide into tile + rest |
| `cute.composition(layout1, layout2)` | Compose layouts |
| `cute.complement(layout)` | Complement layout |
| `cute.coalesce(layout)` | Simplify layout |
| `cute.flatten(t)` | Flatten tensor/layout |
| `cute.group_modes(layout, start, end)` | Group modes together |
| `cute.tile_to_shape(tile, shape)` | Tile to target shape |
| `cute.ceil_div(a, b)` | Ceiling division |

### MMA Operations

| API | Purpose | Notes |
|-----|---------|-------|
| `cute.make_tiled_mma(op)` | Create tiled MMA from operation | e.g., `tcgen05.MmaF16BF16Op(...)` |
| `tiled_mma.get_slice(thread_idx)` | Get thread's partition | Returns `ThrMma` |
| `thr_mma.partition_A(tensor)` | Partition A operand | Thread-level view |
| `thr_mma.partition_B(tensor)` | Partition B operand | Thread-level view |
| `thr_mma.partition_C(tensor)` | Partition C operand | Thread-level view |
| `tiled_mma.partition_shape_C(shape)` | Shape of C partition | For fragment allocation |
| `tiled_mma.make_fragment_A(tensor)` | Make A fragment | Register allocation |
| `tiled_mma.make_fragment_B(tensor)` | Make B fragment | Register allocation |
| `tiled_mma.make_fragment_C(shape)` | Make C fragment | Register allocation |
| `cute.gemm(tiled_mma, d, a, b, c)` | Execute MMA: d = a @ b + c | Dispatches to hardware MMA |

### Copy and TMA Operations

| API | Purpose | Notes |
|-----|---------|-------|
| `cute.make_tiled_copy(atom)` | Create tiled copy | For bulk data movement |
| `cute.copy(atom, src, dst, **kw)` | Execute copy | `tma_bar_ptr=`, `mcast_mask=` |
| `cute.basic_copy(src, dst)` | Element-wise copy | No atom needed |
| `cute.prefetch(atom, src)` | Prefetch TMA descriptor | — |
| `cute.nvgpu.make_tiled_tma_atom_A(op, tensor, smem_layout, tile, mma)` | Create TMA atom for A | Host-side only |
| `cute.nvgpu.make_tiled_tma_atom_B(op, tensor, smem_layout, tile, mma)` | Create TMA atom for B | Host-side only |

### Shared Memory

| API | Purpose |
|-----|---------|
| `cutlass.utils.SmemAllocator()` | Create SMEM allocator |
| `smem.allocate_tensor(dtype, layout, align, swizzle)` | Allocate tensor in SMEM |
| `smem.allocate(struct_type)` | Allocate struct in SMEM |

### Tensor Memory (SM100 only)

| API | Purpose |
|-----|---------|
| `cutlass.utils.TmemAllocator(...)` | Create TMEM allocator |
| `tmem.allocate(num_cols)` | Allocate columns |
| `tmem.wait_for_alloc()` | Wait for allocation |
| `tmem.retrieve_ptr(dtype)` | Get pointer |
| `tmem.free(ptr)` | Free memory |

### Synchronization

| API | Purpose |
|-----|---------|
| `cute.arch.mbar.init(barrier_ptr, count)` | Initialize barrier |
| `cute.arch.mbar.arrive(barrier_ptr)` | Arrive at barrier |
| `cute.arch.mbar.wait(barrier_ptr, phase)` | Wait at barrier |
| `cute.arch.mbar.arrive_and_expect_tx(barrier_ptr, bytes)` | Arrive with expected TX bytes |
| `cute.arch.mbar.try_wait(barrier_ptr, phase)` | Non-blocking wait |
| Pipeline classes (see references) | Multi-stage async pipelines |

### Math (Element-wise on TensorSSA)

| API | Purpose | API | Purpose |
|-----|---------|-----|---------|
| `cute.exp(x)` | e^x | `cute.exp2(x)` | 2^x |
| `cute.log(x)` | ln(x) | `cute.log2(x)` | log2(x) |
| `cute.sqrt(x)` | sqrt | `cute.rsqrt(x)` | 1/sqrt(x) |
| `cute.sin(x)` | sin | `cute.cos(x)` | cos |
| `cute.tanh(x)` | tanh | `cute.erf(x)` | erf |

All math functions accept `fastmath=True` for approximate hardware intrinsics.

### Tensor Operations

| API | Purpose |
|-----|---------|
| `cute.full(shape, val, dtype)` | Fill with value |
| `cute.zeros_like(tensor)` | Zero tensor matching shape |
| `cute.where(cond, x, y)` | Conditional select |
| `cute.any_(tensor)` | Logical any |
| `cute.all_(tensor)` | Logical all |

### Debugging

| API | Purpose |
|-----|---------|
| `cute.printf(fmt, ...)` | Device-side printf |
| `cute.print_tensor(tensor)` | Print tensor contents |
| `print(...)` | Compile-time print (meta-stage only) |

---

## Key Constraints

1. **`@cute.kernel` function name must match module filename** — same rule as cuTile
2. **TMA descriptors are host-side only** — create in `@cute.jit`, pass to `@cute.kernel`
3. **Register budget: 255 max/thread** — validate with `docs/devices/` specs
4. **SMEM limits vary by device and SM version** — SM100 (B200/B300): 228 KB/SM, 227 KB/block opt-in; SM120 (RTX 5090): 96 KB
5. **Pipeline stages consume SMEM** — each stage needs its own buffer; validate total
6. **Barrier sync errors are silent** — cause incorrect results, not crashes; always test with `--check`
7. **Cluster dimensions must be compatible with grid** — cluster shape must evenly divide grid
8. **`print()` is compile-time only** — use `cute.printf()` for device-side output
9. **No early-exit breaks in loops** — use predication instead
10. **32-bit layout algebra** — shapes/strides limited to 32-bit integers
11. **Architecture support**: Ampere (SM80) and above; SM100 (B200/B300) for full features including `tcgen05` and TMEM
12. **Architecture-specific kernels**: Some kernels target a specific SM version (e.g., `tcgen05` MMA ops require **SM100**, not just "Blackwell"). The "Blackwell" marketing name spans multiple SM versions with different instruction sets:
    - **SM100** (B200, B300) — datacenter GPUs, supports `tcgen05` MMA, TMEM, full cluster features
    - **SM120** (GeForce RTX 5090, RTX 5080) — consumer Blackwell, uses `sm_120a`, does **not** support `tcgen05` ops

    Always check the device before running, compiling, or profiling: `nvidia-smi --query-gpu=name --format=csv,noheader`. Then match against the kernel's target SM version — the GPU name alone is not sufficient; you must know which SM version it maps to. If the SM version does not match, **skip the run/profiling step** rather than attempting execution that will fail or produce misleading results.

## Control Flow

| Construct | Behavior | Notes |
|-----------|----------|-------|
| `for i in range(N)` | Unrolled if N is static | Standard Python range |
| `for i in cutlass.range(N)` | Runtime loop | Generates MLIR loop |
| `for i in cutlass.range_constexpr(N)` | Compile-time unroll | N must be static |
| `if cutlass.const_expr(cond)` | Compile-time branch | Eliminated at compile time |
| `if cond` | Runtime branch | Both branches must type-check |

---

## Blackwell Datacenter MMA Operations (tcgen05) — SM100 only

> **SM100 required.** `tcgen05` ops are available on B200/B300 (SM100) only. They are **not** available on consumer Blackwell GPUs like RTX 5090 (SM120/`sm_120a`).

```python
from cutlass.cute.nvgpu import tcgen05

# Create MMA operation for SM100 (B200/B300) tensor cores
op = tcgen05.MmaF16BF16Op(
    dtype=cutlass.Float16,           # Input type
    acc_dtype=cutlass.Float32,       # Accumulator type
    shape=(128, 128, 64),            # M x N x K tile shape
    cta_group=tcgen05.CtaGroup.ONE,  # ONE or TWO CTAs
)

tiled_mma = cute.make_tiled_mma(op)
```

| Operation | Input types | Shapes |
|-----------|-------------|--------|
| `MmaF16BF16Op` | FP16/BF16 → FP32 | Various M×N×K |
| `MmaF8F6F4Op` | FP8/FP6/FP4 → FP32 | Narrow precision |
| Block-scaled variants | With scale factors | See examples |

---

## Common Patterns

### GEMM with TMA Pipeline (Simplified)

```python
@cute.kernel
def gemm_kernel(tiled_mma, tma_a, tma_b, smem_a, smem_b, gmem_c, ...):
    tidx, _, _ = cute.arch.thread_idx()
    bidx, bidy, _ = cute.arch.block_idx()

    # Get thread's MMA partition
    thr_mma = tiled_mma.get_slice(tidx)

    # Allocate accumulator in registers
    acc = tiled_mma.partition_shape_C(tile_shape)
    tCrC = cute.make_fragment(acc, cutlass.Float32)

    # K-loop with TMA pipeline
    for k_tile in range(num_k_tiles):
        # TMA copy: global → shared (async)
        cute.copy(tma_a, gA_tile, sA_tile, tma_bar_ptr=barrier)
        cute.copy(tma_b, gB_tile, sB_tile, tma_bar_ptr=barrier)

        # Wait for TMA to complete
        cute.arch.mbar.wait(barrier, phase)

        # Partition shared memory for this thread
        tCsA = thr_mma.partition_A(sA)
        tCsB = thr_mma.partition_B(sB)

        # MMA: accumulate into registers
        cute.gemm(tiled_mma, tCrC, tCsA, tCsB, tCrC)

    # Epilogue: write back to global memory
    cute.basic_copy(tCrC, gC_partition)
```

### Warpgroup Specialization (Producer/Consumer)

```python
warp_idx = cute.arch.warp_idx()
is_producer = warp_idx < num_producer_warps

if is_producer:
    # Issue TMA copies for upcoming pipeline stages
    for stage in range(num_stages):
        cute.copy(tma_atom, src, dst, tma_bar_ptr=barriers[stage])
        cute.arch.mbar.arrive_and_expect_tx(barriers[stage], bytes_per_stage)
else:
    # Consume data from shared memory, execute MMA
    for stage in range(num_stages):
        cute.arch.mbar.wait(barriers[stage], phase)
        cute.gemm(tiled_mma, acc, sA_stage, sB_stage, acc)
```

### Persistent Kernel Loop

```python
@cute.kernel
def persistent_kernel(tiled_mma, num_tiles, ...):
    bidx, _, _ = cute.arch.block_idx()
    num_blocks = cute.arch.grid_dim()[0]

    tile_id = bidx
    while tile_id < num_tiles:
        # Process tile
        # ... TMA copy, MMA, epilogue ...
        tile_id += num_blocks
```

---

## Detailed References

- **Architecture operations** (thread indexing, TMA, MMA atoms, barriers, SMEM/TMEM): See [references/architecture-ops.md](references/architecture-ops.md)
- **Official documentation index**: See [references/docs-index.md](references/docs-index.md)
- **Example kernels**: See the `/learn-cute-dsl` skill for a categorized example source index
