---
name: port-to-mlx
description: Use when porting CUDA-first or Linux-first code to Apple Silicon MLX/Metal. Covers Triton/CUDA kernel porting to MLX Metal (sparse ops, atomics, custom VJP, mx.fast.metal_kernel), PyTorch nn.Module to mlx.nn.Module conversion, 3D Gaussian Splatting rasterization (tile-based rendering, SH evaluation, EWA splatting, GLM convention handling, hybrid autodiff backward), vision foundation models (SAM + CLIP multi-backend with auto-detect factory pattern, mlx_clip, mlx_sam3, PyTorch MPS fallback), IsaacLab simulator backends, Stereolabs ZED stereo cameras, Intel RealSense depth processing (CUDA→MLX filters, point cloud, alignment), NVIDIA Triton Inference Server to MLX (server architecture, mlx-lm integration, OpenAI-compatible API, production hardening), ragged tensor patterns, packaging splits, benchmark harnesses, and macOS install/CI paths. Apply whenever replacing CUDA, Triton, Warp, or Linux assumptions with MLX, Metal, CPU fallback, or mac-native adapters.
---

# Port To MLX

Use this skill when extending the IsaacLab MLX/mac-sim port, the zed-sdk-mlx stereo camera port, the realsense-mlx depth processing port, the triton-mlx inference server port, or porting similar CUDA-first / Linux-first systems to Apple Silicon.

## Goals

- Preserve user-facing workflow shape where practical.
- Move CUDA, Warp, V4L2, and Isaac Sim assumptions behind explicit backend interfaces.
- Prefer capability-gated unsupported errors over import-time crashes or silent failures.
- Keep the public macOS path installable with `uv` and runnable without Isaac Sim or Linux-only deps.
- For stereo camera work: MLX is the preferred compute backend; CPU/OpenCV is fallback only.

## MANDATORY: Check MLX Version Before Starting

**EVERY TIME you start a port, you MUST check the latest MLX release on GitHub before writing any code:**

```bash
# Check latest release — DO THIS FIRST
curl -s https://api.github.com/repos/ml-explore/mlx/releases/latest | jq -r '.tag_name, .published_at'
# Or: visit https://github.com/ml-explore/mlx/releases
```

**Why:** MLX ships new features and breaking changes frequently (monthly releases). Assuming an old API wastes hours. The nn module surface has expanded dramatically — v0.31+ has modules that v0.22 didn't.

### Latest Known Versions (as of 2026-03-18)

| Package | Version | Release Date | PyPI |
|---------|---------|-------------|------|
| **mlx** | 0.31.1 | 2026-02-28 | `pip install mlx>=0.31.0` |
| **mlx-metal** | 0.31.1 | 2026-02-28 | Auto-installed with mlx |
| **mlx-lm** | 0.31.1 | 2026-03-11 | `pip install mlx-lm>=0.31.0` |

### MLX v0.31+ nn Module Inventory (COMPLETE)

These are ALL available as of v0.31. Do NOT reimplement from scratch:

| Category | Available Modules |
|----------|------------------|
| **Linear** | `nn.Linear` |
| **Convolution** | `nn.Conv1d`, `nn.Conv2d`, `nn.Conv3d` |
| **Normalization** | `nn.LayerNorm`, `nn.BatchNorm`, `nn.RMSNorm`, `nn.GroupNorm` |
| **Recurrent** | `nn.LSTM`, `nn.GRU`, `nn.RNN` |
| **Attention** | `nn.MultiHeadAttention`, `nn.Transformer` |
| **Pooling** | `nn.AvgPool2d`, `nn.MaxPool2d` |
| **Embedding** | `nn.Embedding` |
| **Dropout** | `nn.Dropout` |
| **Activations** | `nn.ReLU`, `nn.GELU`, `nn.SiLU`, `nn.Softmax`, `nn.Sigmoid`, `nn.Tanh` |
| **Positional** | `nn.RoPE`, `nn.SinusoidalPositionalEncoding` |
| **Container** | `nn.Sequential` |
| **Optimizers** | `optim.SGD`, `optim.Adam`, `optim.AdamW`, `optim.RMSprop`, `optim.Adagrad`, `optim.Lion` |
| **LR Schedule** | `optim.linear_schedule`, `optim.cosine_decay`, `optim.step_decay` |

**Key convention:** MLX Conv2d uses **NHWC** (channels last), NOT NCHW like PyTorch. All image tensors must be transposed.

## Port Formula

Classify every blocker into one bucket before editing:

### IsaacLab Buckets
- tensor/runtime: `torch.cuda`, device placement, RNG, checkpointing, training loops
- kernels: Warp, CUDA helpers, tensor kernels, raycast/camera kernels
- simulator: stepping, articulation state IO, contacts, terrains, resets
- sensors/rendering: raycast, camera, depth, segmentation, RTX-only surfaces
- planners/extensions: cuRobo, Kit extensions, ROS CUDA transports

### Stereolabs ZED Buckets
- capture: V4L2 → AVFoundation, UVC → IOKit sideband, device controls
- compute: CUDA SGBM/stereo → MLX cost-volume stereo, Metal compute shaders
- display: OpenGL/GTK viewers → Metal/SDL2/CAMetalLayer viewers
- transport: Linux IPC → POSIX shared memory with seqlock double-buffer
- tools: Linux CLI tools → macOS-native replacements with capability gating

Apply the matching replacement:

- tensor/runtime → `ComputeBackend=mlx`
- kernels → MLX ops first, Metal kernels second, CPU fallback only for bring-up
- simulator → `SimBackend=mac-sim`
- sensors/planners/extensions → capability-gated adapters, never hard imports
- capture → AVFoundation + optional IOKit UVC sideband for controls
- compute → MLX stereo pipeline (cost-volume, soft-argmin, guided filter)
- display → SDL2 or native Metal view (not cv2.imshow for production)
- transport → POSIX shm with seqlock, semaphore signaling preferred over polling

## Working Rules

1. Start from import safety.
   Make modules importable on macOS without `isaacsim`, `omni.*`, `carb`, `pxr`, or `warp` unless that module is explicitly upstream-only.
2. Add seams before rewrites.
   Prefer `ComputeBackend`, `KernelBackend`, `SimBackend`, `SensorBackend`, and `PlannerBackend` adapters over scattered conditionals.
3. Keep the public knobs stable.
   Current public runtime knobs are `--compute-backend`, `--kernel-backend`, and `--sim-backend`.
4. Split packaging.
   The base package must stay backend-neutral. CUDA/IsaacSim and MLX/macOS dependencies belong in extras.
5. Benchmark every new mac-native slice.
   Add or extend benchmark entrypoints so M-series throughput can be measured repeatedly.
6. Record each success.
   Append concrete wins and learned patterns to `references/progress_log.md`.
7. Keep every public surface in sync for new tasks.
   When a mac-native task lands, update the config-only entrypoint, lazy task registry, public wrapper, shared CLI support, benchmark groups, semantic baseline, CI workflow, and README in the same tranche.
8. Treat planner and ROS replacements as prototypes until proven otherwise.
   Document them as compatibility seams, not parity layers, until they have task-level integrations and hardware-backed validation.

## ZED-Specific Working Rules

9. Capability-gate unsupported device controls honestly.
   macOS AVFoundation does NOT expose: `exposureDuration`, `iso`, `setExposureModeCustom`, `deviceWhiteBalanceGains`, `setWhiteBalanceModeLocked(with:)`, `setExposureTargetBias`. Only mode toggling (auto/locked) works. Do not fake parity.
10. IOKit UVC sideband is a stretch goal, not a requirement.
    Sending UVC GET_CUR/SET_CUR via IOKit alongside AVFoundation streaming is possible but undocumented. Gate behind `--enable-uvc-controls`.
11. MLX stereo performance priorities (ranked):
    - Eliminate Python-loop bilateral filter (use O(1) guided filter or skip)
    - Use `pyramid_factor=2` or higher for live mode
    - Async double-buffer MLX pipeline (overlap GPU+CPU)
    - Replace cv2.imshow with SDL2 or Metal view
    - Zero-copy shared memory reads
    - Native Metal viewer process (high effort, high reward)
    - Raw Metal compute shader (only if 60fps needed)
12. Config persistence at `~/zed/settings/mlx_live_stereo.json` (JSON format).
    Depth demo auto-loads saved config. CLI flags override.
13. Shared memory protocol: POSIX shm_open, 64-byte C-compatible header, double-buffered slots, seqlock sequence counter.

## Default Workflow

1. Scan for direct imports or assumptions:
   ```bash
   rg -n "torch\\.cuda|import warp|from warp|import omni|from omni|import carb|from carb|import pxr|from pxr|import isaacsim|from isaacsim" <paths>
   ```
   For ZED port:
   ```bash
   rg -n "V4L2|v4l2|linux/videodev|ioctl|VIDIOC_" <paths>
   ```
2. Decide whether the target is:
   - shared code that must be import-safe on macOS
   - upstream-only code that should be lazy-gated
   - a feature that needs a mac-native replacement
3. Patch the narrowest seam that removes the hard dependency.
4. Add tests for:
   - import safety
   - runtime selection/capability reporting
   - the new MLX/mac-sim behavior
5. Run focused validation:
   - backend tests
   - smoke scripts
   - install smoke with `uv`
   - benchmark smoke if performance-facing
6. Append the outcome to `references/progress_log.md`.

## ZED Port Recipe

### Camera Controls on macOS

macOS AVFoundation API reality (doc-grounded, verified 2026-03-14):

| Control | macOS AVFoundation | Alternative |
|---------|-------------------|-------------|
| Auto/locked exposure toggle | YES (10.7+) | — |
| Auto/locked white balance toggle | YES (10.7+) | — |
| Manual exposure duration/ISO | NO (iOS-only) | IOKit UVC sideband |
| Manual white balance gains | NO (iOS-only) | IOKit UVC sideband |
| Exposure compensation/bias | NO (iOS-only) | IOKit UVC sideband |
| Gain control | NO (nowhere) | IOKit UVC sideband |
| ROI metering | API exists, devices return false | — |

**IOKit UVC Sideband Architecture** (stretch goal):
```
AVFoundation ──────→ Video streaming (untouched)
IOKit USB sideband ─→ UVC control requests (exposure, gain, WB)
```
- Target Camera Terminal (ID=1) and Processing Unit (ID=2)
- Control selectors: CT_AE_MODE=0x02, CT_EXPOSURE_ABS=0x04, PU_GAIN=0x04, PU_WB_TEMP=0x06, PU_WB_AUTO=0x0B
- Do NOT claim streaming interfaces — only control endpoint
- Gate behind `--enable-uvc-controls` flag

### Live MLX Stereo Performance

Current baseline: ~14-15 FPS at 720p on ZED 2i / M5 Mac.

Optimization priority (ranked by leverage):

| Rank | Action | Complexity | Expected Gain |
|------|--------|-----------|---------------|
| 1 | Set `refinement_radius=0` for live | Trivial | +5-10 FPS |
| 2 | Confirm `pyramid_factor=2` default | Trivial | +8-15 FPS |
| 3 | Async double-buffer MLX pipeline | Medium | +3-5 FPS |
| 4 | SDL2 display instead of cv2.imshow | Low-Medium | +2-4 FPS |
| 5 | Zero-copy SHM read (numpy view) | Low | +0.5-1 FPS |
| 6 | Native Metal viewer process | High | +3-5 FPS |
| 7 | Raw Metal compute shader | Very High | +10-20 FPS |
| 8 | Semaphore SHM signaling | Low-Medium | +1-2 FPS latency |

### Tune-Stereo Replacement

The old `zed_open_capture_depth_tune_stereo` (OpenCV SGBM) is replaced by:
- `scripts/live_mlx_disparity.py` — MLX live tuner with interactive trackbars
- `zed_mlx/live_config.py` — Config dataclass, JSON serialization, validation
- Config at `~/zed/settings/mlx_live_stereo.json`
- Depth demo auto-loads saved config

### Port Completeness Matrix

| Surface | Classification | Notes |
|---------|---------------|-------|
| Raw video capture | Native parity | AVFoundation, validated ZED 2i |
| Sensor capture | Native parity | Same hidapi path |
| Video/sensor sync | macOS replacement | Timestamp-fallback (no hw gate) |
| Calibration loading | Native parity | Same ~/zed/settings/ path |
| Rectification | Native parity | Same OpenCV remap |
| Video example | Native parity | AVFoundation + OpenCV display |
| Multi-camera | macOS replacement | Needs validation |
| Camera control | Capability-gated partial | Mode toggle only |
| Depth example | macOS replacement | MLX disparity (routed) |
| Tune-stereo | macOS replacement | MLX live tuner |
| Point-cloud export | Native parity | MLX + PLY |
| Point-cloud viewer | Deferred | Export only |
| ROS2 wrapper | Deferred | After base stability |

## Task Port Recipe (IsaacLab)

### Locomotion tasks with terrain or raycasts

1. Start from the existing flat-task reduction and preserve the observation/reward/reset contract first.
2. Generalize the terrain API instead of special-casing the task:
   - `sample_heights(...)`
   - `surface_normals(...)`
   - `out_of_bounds(...)`
   - optional `env_ids` threading for flattened contact or raycast queries
3. Keep the first rough-terrain path analytic and deterministic.
4. Update sensor diagnostics and semantic baselines in the same pass.

### Manipulation tasks

1. Start with the joint-position or direct-actuation variant before IK/OSC or cuRobo-dependent paths.
2. Preserve user-facing task IDs and config flow through the lazy registry even if the mac-native implementation is reduced.
3. Prefer deterministic analytic kinematics and explicit object/grasp state over partial simulator emulation for the first slice.
4. Expose early manipulation slices as eval/manual paths first; only claim trainability after checkpoint, replay, and benchmark contracts exist.
5. When promoting a manipulation task from eval-only to trainable, land the whole surface together.
6. The second manipulation slice should reuse the first slice's PPO/checkpoint contract unless there is a real task-specific reason to diverge.

### Semantic drift and benchmark contracts

1. Any time a benchmarked task contract changes, regenerate the semantic baseline from a deterministic `full` benchmark run.
2. Immediately rerun `test_mac_semantic_drift.py` after refreshing the baseline.
3. If a task is deterministic but the baseline differs, treat it as a stale baseline problem and fix the baseline in the same tranche.

## High-Value Targets

### IsaacLab
- package setup files that still force torch/CUDA-era dependencies
- public imports that still trip Isaac Sim imports
- shared task/config loaders that assume `isaacsim`
- simulator contracts missing articulation/root-state operations needed by more tasks
- CI lanes that do not prove the macOS install path end to end

### ZED Stereo
- bilateral filter Python loop in `_edge_aware_refine` (biggest perf bottleneck)
- `cv2.imshow` display path (replace with SDL2/Metal)
- `bytes()` copy in `shm_frame.py` (zero-copy numpy view)
- poll-based SHM reads (replace with semaphore signaling)
- IOKit UVC sideband PoC for camera controls

## Validation Commands

### IsaacLab
```bash
PYTHONPATH=.:source/isaaclab:source/isaaclab_rl .venv/bin/pytest \
  scripts/tools/test/test_bootstrap_isaac_sources.py \
  source/isaaclab/test/backends/test_runtime.py \
  source/isaaclab/test/backends/test_task_registry.py \
  source/isaaclab/test/backends/test_kernel_inventory.py \
  source/isaaclab/test/backends/test_portability_utils.py \
  source/isaaclab/test/backends/test_planner_compat.py \
  source/isaaclab/test/backends/test_ros2_bridge.py \
  source/isaaclab/test/backends/test_mac_benchmark_suite.py \
  source/isaaclab/test/backends/test_mac_semantic_drift.py \
  source/isaaclab/test/backends/test_mac_cartpole.py \
  source/isaaclab/test/backends/test_mac_cartpole_showcase.py \
  source/isaaclab/test/backends/test_mac_cart_double_pendulum.py \
  source/isaaclab/test/backends/test_mac_quadcopter.py \
  source/isaaclab/test/backends/test_mac_anymal_c.py \
  source/isaaclab/test/backends/test_mac_anymal_c_rough.py \
  source/isaaclab/test/backends/test_mac_franka_reach.py \
  source/isaaclab/test/backends/test_mac_franka_lift.py \
  source/isaaclab/test/backends/test_mac_h1.py \
  source/isaaclab_rl/test/test_import_safety.py \
  source/isaaclab_rl/test/test_mlx_wrapper.py -q
```

### ZED Stereo
```bash
# Full test suite
cd zed-sdk-mlx && .venv/bin/pytest tests/ -q

# Live smoke (requires connected ZED camera)
make smoke-zed-terminal
make live-mlx-disparity-terminal

# Benchmark
make mlx-stereo-benchmark
make mlx-stereo-eval
```

## Learned Patterns

- A conservative generic `mac-sim` capability snapshot is useful, but task benchmarks should also report the concrete simulator adapter contract for the implemented slice.
- Public install safety improves quickly once package extras are separated from base requirements.
- Import safety is the first forcing function: if a module cannot import on macOS without Isaac Sim, no later MLX work can use it reliably.
- For unsupported features, lazy-gate imports and raise `UnsupportedBackendError` or `UnsupportedRuntimeFeatureError` at use sites.
- When a new mac-native task lands, update every public surface in the same tranche.
- Rough-terrain ports are cheapest when the terrain API is generalized early.
- The first manipulation slice should reduce scope aggressively.
- Planner and ROS replacements should stay framed as prototype compatibility seams until hardware-backed validation.
- Semantic drift failures are often stale-baseline failures, not broken tasks.
- Promotion from eval-only to trainable is a whole-surface change.
- RL wrapper packages should not force framework dependencies at package install time.
- Config dataclasses should live outside heavy runtime/controller modules.
- For ZED stereo: the bilateral filter Python loop is the single biggest perf bottleneck — kill it or replace with O(1) guided filter.
- For ZED stereo: `pyramid_factor=2` with `refinement_radius=0` roughly doubles FPS with minimal quality loss.
- For ZED stereo: macOS camera control APIs are fundamentally limited — capability-gate honestly, don't fake parity.

---

## Triton/CUDA Kernel → MLX Metal Porting (Pointelligence Pattern)

This section captures battle-tested patterns from porting PointCNN++ (5 Triton kernels, 4 CUDA kernels, full ResNet backbone) to MLX. Use these patterns for any project with custom CUDA/Triton sparse ops.

### Kernel Porting Buckets

Classify each kernel before porting:

| Type | Triton/CUDA Pattern | MLX Replacement | Complexity |
|------|---------------------|-----------------|-----------|
| **Elementwise indexed** | `out[i] = f(a[idx[i]], b[idx[i]])` | Vectorized: `a[idx] - b[idx]` then reduce | EASY |
| **Scatter-reduce** | `atomicAdd(out[idx], val)` | `mx.array.at[idx].add(val)` or numpy `np.add.at` | MEDIUM |
| **Blocked scatter** | Tiled iteration + atomic flush | Python block loop + scatter per block | MEDIUM |
| **Segment reduce** | Per-segment sum/mean/max/min | `repeat_interleave_indices` → segment_ids → scatter | MEDIUM |
| **Sparse matmul** | Gather-multiply-scatter with atomics | Blocked: gather block, contract, scatter-add | HARD |
| **Warp-level ops** | `__shfl_sync`, `__ballot_sync` | Not available in `mx.fast.metal_kernel`; use shared memory or SIMD groups in C++ extension | HARD |

### MLX API Quick Reference

| Need | MLX API | Notes |
|------|---------|-------|
| Custom Metal kernel | `mx.fast.metal_kernel()` | JIT compiled, source as string |
| C++ extension | Subclass `mlx::core::Primitive` + CMake | For complex kernels needing atomics |
| Atomics in Metal | `mlx_atomic<T>`, `atomic_fetch_add_explicit` | Via MLX's `atomic.h` header |
| Scatter-add | `arr.at[indices].add(values)` | Returns new array (functional) |
| Custom autograd | `@mx.custom_function` + `.vjp` | Replaces `torch.autograd.Function` |
| nn.Module | `mlx.nn.Module` with `__call__` | Parameters auto-discovered |
| Version check | `importlib.metadata.version("mlx")` | NOT `mlx.__version__` (doesn't exist) |
| GPU sync | `mx.eval(tensor)` | Required for timing/materialization |
| No int64 scatter | Cast to int32 for GPU scatter ops | MLX Metal backend limitation |

### The Blocked Scatter-Add Pattern (CRITICAL)

This is the single most important pattern. MVMR, VVOR, and segment reduces all use it.

**Problem:** Triton/CUDA use `atomicAdd` to accumulate results from multiple threads into shared output slots. MLX doesn't have atomic scatter in pure Python.

**Solution: Blocked iteration with scatter-add**

```python
BLOCK = min(T, 4096)
output = mx.zeros((n_o, ...))

for t_start in range(0, T, BLOCK):
    t_end = min(t_start + BLOCK, T)

    # 1. Gather inputs for this block
    a_block = a[a_idx[t_start:t_end]]
    b_block = b[b_idx[t_start:t_end]]
    o_block = o_idx[t_start:t_end]

    # 2. Compute (elementwise/contract/outer product)
    products = compute(a_block, b_block)

    # 3. Scatter-add to output
    output = output.at[o_block].add(products)

return output
```

**Key insight:** `mx.array.at[indices].add(values)` handles duplicate indices correctly — it accumulates. This replaces CUDA `atomicAdd` without explicit atomics.

**Block size tuning:**
- Too small → Python loop overhead dominates
- Too large → intermediate tensors cause OOM
- 4096 is a good default; tune based on `G * M * C` product

### Custom VJP Pattern for Sparse Ops

Every differentiable sparse op needs a `@mx.custom_function` wrapper:

```python
@mx.custom_function
def my_sparse_op(x, indices, lengths):
    return _forward(x, indices, lengths)

@my_sparse_op.vjp
def my_sparse_op_vjp(primals, cotangents, output):
    x, indices, lengths = primals
    grad_output = cotangents

    # Compute grad_x based on op type:
    # SUM: scatter grad_output back to x positions
    # MEAN: scatter grad_output / length
    # MAX: scatter grad_output * (x == output) mask
    grad_x = _backward(grad_output, x, indices, lengths, output)

    return (grad_x, None, None)  # None for non-differentiable args
```

**Circular dependency handling (MVMR ↔ VVOR):**
MVMR backward needs VVOR, VVOR backward needs MVMR. Use late imports inside VJP functions:
```python
@my_mvmr.vjp
def mvmr_vjp(primals, cotangents, output):
    from pointelligence_mlx.sparse_engines.vvor import sparse_vector_vector_outer_product_reduction
    # ... use VVOR for grad_a
```

### repeat_interleave Pattern (Ragged Tensor Core)

MLX doesn't have `torch.repeat_interleave`. This is the universal replacement:

```python
def repeat_interleave_indices(repeats):
    """[2, 0, 3, 1] → [0, 0, 2, 2, 2, 3]"""
    offsets = cumsum_exclusive(repeats)
    output_size = int(mx.sum(repeats).item())
    marker = mx.zeros((output_size,), dtype=mx.int32)

    # Set markers at segment boundaries
    valid_mask = repeats > 0
    valid_offsets = offsets[valid_mask_indices]
    marker = marker.at[valid_offsets].add(mx.ones_like(valid_offsets))

    return mx.cumsum(marker) - 1  # 0-indexed segment IDs
```

This single function powers: segment IDs for reduce, neighbor list expansion, batch index computation, and triplet building.

### nn.Module Translation Cheatsheet

| PyTorch | MLX | Notes |
|---------|-----|-------|
| `nn.Module` | `mlx.nn.Module` | |
| `forward()` | `__call__()` | MLX convention |
| `nn.Parameter` | Direct attribute | Auto-discovered |
| `register_buffer` | `self.name = mx.array(...)` | No registration needed |
| `module.train()/eval()` | No equivalent | Handle BN manually |
| `nn.Linear(in, out)` | `mlx.nn.Linear(in, out)` | Direct match |
| `nn.BatchNorm1d` | Custom RaggedBatchNorm | For variable-length batches |
| `F.relu(x)` | `mlx.nn.relu(x)` | |
| `nn.Sequential` | Custom `MultiSequential` | For `(x, metadata)` tuples |

### Packaging with uv (Not pip)

Always use `uv` for MLX projects:
```bash
uv venv .venv --python 3.12
uv pip install -e ".[dev]"
```
- Avoids `--break-system-packages` issues
- 10-100x faster than pip
- Better dependency resolution

### pyproject.toml Pattern

```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"  # NOT _legacy:_Backend

[project]
dependencies = ["mlx>=0.31.0", "numpy>=1.24.0", "scipy>=1.10.0"]

[project.optional-dependencies]
dev = ["pytest>=7.0", "pytest-benchmark>=4.0", "torch>=2.6.0"]
```

### Testing Pattern: Cross-Framework Validation

```python
def check_all_close(mlx_result, reference, atol=1e-5, rtol=1e-5):
    """Compare with relative tolerance scaling (matches PyTorch test patterns)."""
    actual = np.array(mlx_result)
    expected = np.array(reference)  # works with torch.Tensor, np.ndarray, mx.array
    scale = max(1.0, np.abs(expected).max())
    actual_atol = atol * scale
    assert np.allclose(actual, expected, atol=actual_atol, rtol=rtol)
```

**Default tolerances per op type:**
- Distance ops: atol=1e-5
- Segment reduce (sum/mean): atol=1e-4
- Segment reduce (max/min): atol=1e-6
- Sparse matmul (MVMR/VVOR): atol=1e-2 (atomic add ordering)
- Layer/model outputs: atol=1e-3 to 1e-4

### Gradient Check (No torch.autograd.gradcheck)

MLX has no built-in gradcheck. Use finite differences:
```python
def check_gradient(fn, args, argnums, eps=1e-4, atol=1e-2):
    grad_fn = mx.grad(scalar_fn, argnums=argnums)
    analytical = grad_fn(*args)
    # Central finite differences per element (O(N) evals)
    # For large tensors: random projection check (O(K) evals)
```

### MLX Gotchas (Learned the Hard Way)

1. **`mlx.__version__` doesn't exist** — use `importlib.metadata.version("mlx")`
2. **No int64 on GPU** — cast to int32 for scatter ops
3. **No boolean indexing** — use `argsort` with sentinel values instead of `x[mask]`
4. **`mx.eval()` is mandatory** — without it, lazy graph grows unbounded; parameters don't materialize between training steps
5. **No `torch.repeat_interleave`** — use the marker+cumsum approach above
6. **No `torch.searchsorted`** — use numpy fallback: `np.searchsorted(np.array(sorted), np.array(query))`
7. **No `torch.cdist`** — compute manually: `((a[:, None] - b[None, :]) ** 2).sum(-1).sqrt()`
8. **No `torch.unique_consecutive`** — `mx.unique` is always sorted (which is what you want)
9. **No `torch.segment_reduce`** — implement via scatter ops (this IS the port)
10. **`mx.fast.metal_kernel()` template params** — use constant buffers, not template args
11. **Functional API** — `arr.at[idx].add(val)` returns a NEW array; no in-place mutation
12. **Float16 handling** — large_segment_reduce must upcast to float32 for accumulation, clamp output to float16 range (65504)

### Multi-Agent Porting Workflow

For large ports (5+ kernels), use this parallelization pattern:

```
Phase 1 (sequential): Foundation → Testing Harness → Core Utilities
Phase 2 (parallel):   All kernel PRDs simultaneously (they share only Phase 1 deps)
Phase 3 (sequential): Integration layers → Model → Training
```

Each kernel agent gets: function signature, numpy reference impl, test parameters, tolerance spec. They work independently and are validated against the full suite after completion.

### PRD-Driven Port Structure

For any kernel-heavy port, create individual PRDs with:
1. Exact function signatures and tensor shapes
2. Algorithm description with pseudo-code
3. MLX implementation strategy (pure Python → Metal kernel → C++ extension phases)
4. Acceptance criteria with numerical tolerances
5. Dependencies and blocking relationships
6. GO/NO-GO gates for critical kernels

### Pointelligence Port Stats (Reference)

- 12 PRDs, 28 source files, 16 test files, ~8400 LOC
- 334 tests, all passing
- 5 sparse kernels: MVMR, VVOR, indexed_distance, indexed_segment_reduce, large_segment_reduce
- Full ResNet backbone: 10 model variants
- End-to-end training verified (loss decreases)
- Completed in single session with multi-agent parallelization

---

## Intel RealSense → MLX Port (realsense-mlx)

This section covers porting Intel RealSense SDK (librealsense) CUDA processing kernels and depth filters to MLX for Apple Silicon.

### Architecture Decision

**Wrap, don't replace.** `pyrealsense2` handles camera capture via libuvc on macOS (already works). We only port the **compute/processing layer** to MLX:
- CUDA format conversions → MLX vectorized ops
- CUDA point cloud deprojection → MLX precomputed grids + broadcast
- CUDA depth-color alignment → MLX matmul + gather
- CPU depth filters (spatial, temporal, decimation, hole-fill) → MLX vectorized

### RealSense Port Buckets

| Bucket | Source | MLX Replacement | Difficulty |
|--------|--------|----------------|------------|
| Format conversion | 10 CUDA kernels (cuda-conversion.cu) | Vectorized bitwise/arithmetic | EASY |
| Point cloud | CUDA deproject (cuda-pointcloud.cu) | Precomputed coord grids + broadcast multiply | MEDIUM |
| Alignment | 5 CUDA kernels (cuda-align.cu) | Vectorized matmul + sort-based scatter-min | HARD |
| Spatial filter | CPU recursive (spatial-filter.cpp) | Row-parallel scan | MEDIUM-HARD |
| Temporal filter | CPU stateful (temporal-filter.cpp) | Vectorized alpha blend + state mgmt | MEDIUM |
| Decimation | CPU median/mean (decimation-filter.cpp) | Reshape + mx.median / mx.mean | EASY |
| Hole filling | CPU neighbor (hole-filling-filter.cpp) | Neighbor gather + min/max | EASY |
| Disparity | CPU division (disparity-transform.cpp) | Elementwise mx.where + division | TRIVIAL |
| Colorizer | CPU histogram + LUT (colorizer.cpp) | CPU histogram + MLX LUT gather | EASY-MEDIUM |

### Key Pattern: Precomputed Coordinate Grids

The SSE pointcloud optimization pattern applies perfectly to MLX:
```python
# Precompute ONCE per intrinsics change (cache)
x_grid = (mx.arange(W) - ppx) / fx  # (W,)
y_grid = (mx.arange(H) - ppy) / fy  # (H,)

# Per frame: broadcast multiply (fast)
z = depth.astype(mx.float32) * depth_scale
X = x_grid[None, :] * z  # (H, W)
Y = y_grid[:, None] * z  # (H, W)
points = mx.stack([X, Y, z], axis=-1)  # (H, W, 3)
```

### Key Pattern: Sort-Based Scatter-Min (Alignment)

CUDA `atomicMin` has no MLX equivalent. Workaround:
```python
# Sort by target index, then take first (min) per segment
order = mx.argsort(target_indices)
sorted_vals = values[order]
# Segment boundaries → numpy fallback for scatter-min
np.minimum.at(output, np.array(sorted_indices), np.array(sorted_vals))
```

### Key Pattern: Recursive Filter (Spatial)

Sequential dependency prevents full vectorization. Process all rows in parallel, sequential within each row:
- Horizontal pass: left→right then right→left (all rows parallel)
- Vertical pass: top→bottom then bottom→top (all columns parallel)
- May need Metal kernel for competitive performance

### RealSense-Specific Gotchas

1. **libuvc on macOS**: RealSense uses `FORCE_RSUSB_BACKEND` (libuvc) on Apple, NOT V4L2
2. **Depth format is uint16**: Always 2 bytes per pixel, 0 = invalid/no data
3. **Disparity is float32**: Intermediate processing domain for spatial/temporal filters
4. **Intrinsics change rarely**: Cache coordinate grids per intrinsics, not per frame
5. **Temporal filter is stateful**: Must maintain frame history as MLX arrays on device
6. **Histogram is sequential**: Colorizer histogram must stay on CPU, only LUT lookup goes to MLX
7. **Alignment scatter has duplicates**: Multiple depth pixels can map to same color pixel → need min selection

### RealSense Port Completeness Matrix

| Surface | Status | Notes |
|---------|--------|-------|
| Camera capture | ✅ Already works | pyrealsense2 + libuvc on macOS |
| Format converters | PRD-01 | 10 CUDA kernels → MLX |
| Point cloud | PRD-02 | CUDA deproject → MLX |
| Depth filters (×5) | PRD-03 | CPU/CUDA → MLX |
| Alignment | PRD-04 | CUDA align → MLX |
| Colorizer | PRD-05 | CPU → MLX |
| Display viewer | PRD-06 | OpenCV → SDL2/Metal |
| Integration tests | PRD-07 | Full test suite |
| Benchmarks | PRD-08 | Performance validation |

### Validation Commands (RealSense)
```bash
cd realsense-mlx
uv venv .venv --python 3.12
uv pip install -e ".[dev]"
.venv/bin/pytest tests/ -q
```

---

## Triton Inference Server → MLX Port (Server/Service Pattern)

This section captures patterns from porting NVIDIA Triton Inference Server (v2.67.0dev) to Apple Silicon. Unlike kernel/compute ports (Pointelligence, ZED), this is a **server architecture port** — replacing CUDA infrastructure in a production inference serving system.

### Triton Port Buckets

| Bucket | NVIDIA Original | MLX Replacement |
|--------|----------------|-----------------|
| **inference backend** | CUDA/TensorRT model execution | `mlx_lm.stream_generate()` with sampler API |
| **memory management** | CUDA IPC, pinned memory, GPU pools | Unified memory (no copies), `mx.get_active_memory()` |
| **model loading** | custom C++ backend loaders | `mlx_lm.load()` → (model, tokenizer) |
| **metrics/profiling** | DCGM GPU metrics, NVTX tracing | `mx.get_active/peak/cache_memory()`, prometheus-client |
| **server core** | C++ (libevhtp HTTP, gRPC async) | Python-first (FastAPI + uvicorn) |
| **protocols** | KServe v2 + OpenAI-compatible | OpenAI-compatible REST (drop-in for any OpenAI SDK) |
| **deployment** | Docker/Linux containers | macOS native, `uv pip install -e .` |

### Key Architectural Decision: Python-First

The upstream Triton is a C++ server with Python frontends. For the MLX port, we chose **Python-first**:
- FastAPI + uvicorn replaces C++ libevhtp/gRPC
- No C++ compilation required (huge dev velocity win)
- MLX/mlx-lm are Python-native — no FFI overhead
- Apple Silicon unified memory eliminates the CPU↔GPU data transfer bottleneck that justifies C++

This is the right call for Apple Silicon because:
1. Unified memory means no memcpy overhead (the main reason Triton uses C++)
2. Python GIL doesn't matter — inference is GPU-bound, released during Metal execution
3. `mlx_lm.stream_generate()` already handles KV-cache, sampling, tokenization
4. FastAPI async handles concurrent requests without threading

### mlx-lm API (v0.31+) — Critical Breaking Changes

The `mlx-lm` API changed significantly between versions. Key findings:

```python
# OLD API (pre-0.30) — BROKEN, do not use
from mlx_lm.utils import generate_step  # ❌ Moved
generate_step(prompt, model, temp=0.7)  # ❌ temp/top_p kwargs removed

# NEW API (v0.31+) — correct
from mlx_lm import stream_generate, generate
from mlx_lm.sample_utils import make_sampler, make_logits_processors

# Sampling is now via callable sampler
sampler = make_sampler(temp=0.7, top_p=0.9)

# Penalties via logits processors
processors = make_logits_processors(
    repetition_penalty=1.1,
    frequency_penalty=0.5,
    presence_penalty=0.3,
)

# stream_generate yields GenerationResponse dataclass
for response in stream_generate(model, tokenizer, prompt, max_tokens=256,
                                 sampler=sampler, logits_processors=processors):
    print(response.text, end="")
    # response.token, response.logprobs, response.prompt_tokens,
    # response.generation_tokens, response.generation_tps,
    # response.peak_memory, response.finish_reason
```

**GenerationResponse fields (v0.31+):**
- `text: str` — decoded text segment
- `token: int` — token ID
- `logprobs: mx.array` — log probabilities
- `prompt_tokens: int` — prompt token count
- `generation_tokens: int` — generated token count
- `generation_tps: float` — tokens per second
- `peak_memory: float` — peak memory in GB
- `finish_reason: Optional[str]` — "length", "stop", or None

### mlx.metal.* Deprecation (MLX v0.22+)

```python
# OLD — deprecated, will be removed
mx.metal.get_active_memory()
mx.metal.get_peak_memory()
mx.metal.get_cache_memory()

# NEW — use these
mx.get_active_memory()
mx.get_peak_memory()
mx.get_cache_memory()
```

### Server Port Recipe

For porting any CUDA inference server to MLX:

1. **Start Python-first** — Don't port the C++ core. Build a new Python server.
2. **Use mlx-lm** — Don't reimplement model loading/generation. Use `mlx_lm.load()` and `mlx_lm.stream_generate()`.
3. **OpenAI API target** — The OpenAI REST API is the universal client interface. Implement it with FastAPI.
4. **Model repository = directory of HuggingFace models** — Each subdirectory with `config.json` is a model.
5. **Unified memory eliminates shared memory complexity** — No CUDA IPC, no pinned memory, no GPU memory pools.
6. **Production hardening checklist:**
   - Prometheus metrics (prometheus-client)
   - Health checks (/health/live, /health/ready)
   - Request ID middleware (X-Request-ID)
   - Concurrency limiter (asyncio.Semaphore → 429 on overload)
   - API key auth (optional Bearer token)
   - Graceful shutdown (SIGINT/SIGTERM signal handlers)
   - Structured logging (JSON format option)
   - Model warm-up (dummy forward pass on load)
   - OpenAI-compatible error format for all errors

### OpenAI-Compatible SSE Streaming Pattern

```python
async def stream_chat(engine, request):
    completion_id = f"chatcmpl-{uuid4().hex[:12]}"
    created = int(time.time())

    # First chunk: role only
    yield format_sse({"choices": [{"delta": {"role": "assistant"}}]})

    # Content chunks
    async for chunk in engine.generate_stream(...):
        if chunk.text:
            yield format_sse({"choices": [{"delta": {"content": chunk.text}}]})

    # Final chunk: finish_reason
    yield format_sse({"choices": [{"delta": {}, "finish_reason": "stop"}]})
    yield "data: [DONE]\n\n"

def format_sse(obj):
    return f"data: {json.dumps(obj)}\n\n"
```

### Model Repository Discovery Pattern

```python
def discover_models(repo_path: Path) -> list[ModelSpec]:
    for item in repo_path.iterdir():
        if not item.is_dir() or item.name.startswith("."):
            continue
        config_path = item / "config.json"
        if config_path.exists():
            config = json.loads(config_path.read_text())
            model_type = config.get("model_type", "unknown")
            # Detect quantization from config
            quant = config.get("quantization_config", {}).get("bits")
            yield ModelSpec(name=item.name, path=str(item), ...)
```

### Model Memory Estimation (Before Loading)

```python
def estimate_memory(config: dict) -> int:
    """Rough memory estimate in bytes."""
    H = config.get("hidden_size", 4096)
    L = config.get("num_hidden_layers", 32)
    I = config.get("intermediate_size", H * 4)
    V = config.get("vocab_size", 32000)
    params_per_layer = 4*H*H + 3*H*I  # attention + MLP
    total_params = L * params_per_layer + 2 * V * H
    bits = config.get("quantization_config", {}).get("bits", 16)
    return int(total_params * (bits / 8) * 1.1)  # 10% overhead
```

### Concurrency Control for Apple Silicon

Apple Silicon has limited GPU memory. Use asyncio.Semaphore to prevent OOM:

```python
class ConcurrencyLimiter:
    def __init__(self, max_concurrent: int = 4):
        self._semaphore = asyncio.Semaphore(max_concurrent)

    async def acquire(self) -> bool:
        return self._semaphore.locked() is False  # non-blocking check
        # Or: await self._semaphore.acquire() for blocking
```

Return 429 Too Many Requests in OpenAI error format when saturated.

### Multi-Agent Porting Workflow (Server Pattern)

For server ports, the parallelization is different from kernel ports:

```
Phase 1 (sequential): Foundation + Testing Harness
  - pyproject.toml, project structure, conftest.py
  - Mock fixtures for engine, model manager, tokenizer

Phase 2 (parallel): All modules simultaneously
  - Model Manager (discovery, loading, unloading)
  - Inference Runtime (generate, stream, embed)
  - Engine Adapter (OpenAI ↔ MLX bridge)
  - API Routers (chat, completions, embeddings, models, health)
  - Memory Manager (Metal tracking)
  - Model Repository (config parsing, polling)

Phase 3 (parallel): Production hardening
  - Metrics (Prometheus)
  - Auth (API key middleware)
  - Concurrency (Semaphore limiter)
  - Logging (structured JSON)
  - Error handling (OpenAI error format)
  - Model warm-up and caching

Phase 4 (sequential): Integration + E2E tests
```

### Triton-MLX Port Stats (Reference)

- 13 PRDs, 28 source files, 25 test files, ~4500 LOC
- 160 tests, all passing
- 6 parallel agents for production hardening phase
- Full OpenAI SDK compatibility verified (streaming + non-streaming)
- Model: Llama-3.2-1B-Instruct-4bit, load time ~2.3s, 838MB Metal memory
- Completed in single session with multi-agent parallelization
- Repo: `github.com/RobotFlow-Labs/triton-mlx`

### Triton-MLX Gotchas (Learned the Hard Way)

13. **`mlx_lm` generate API changed completely** — v0.31+ uses `sampler` callable, not `temp`/`top_p` kwargs. `generate_step` moved and requires different parameters.
14. **`mx.metal.*` deprecated** — use `mx.get_active_memory()` etc. (no `.metal.` prefix)
15. **Model warm-up is essential** — First inference after `mlx_lm.load()` is 5-10x slower (Metal shader compilation). Always do a dummy forward pass on load.
16. **FastAPI TestClient works with OpenAI SDK** — `OpenAI(base_url="http://testserver/v1", http_client=test_client)` enables SDK-level testing without a running server.
17. **SSE requires exact format** — `data: {json}\n\n` with double newline. First chunk must have `role` only. Last data line is `data: [DONE]\n\n`.
18. **`stream_generate` handles EOS internally** — It breaks on EOS tokens automatically; you just need to detect `finish_reason` in the response.
19. **Chat template fallback** — Not all tokenizers support `apply_chat_template`. Always have a simple concatenation fallback.
20. **Unified memory = no shared memory complexity** — CUDA IPC, pinned memory pools, and GPU memory pools from upstream Triton are completely unnecessary on Apple Silicon.

---

## 3D Gaussian Splatting Rasterizer → MLX Port (diff-gaussian-rasterization)

This section covers porting the INRIA GRAPHDECO differentiable Gaussian splatting rasterizer from CUDA to MLX. The original has 5 CUDA kernels, ~4300 LOC, using CUB, GLM, and cooperative_groups.

### 3DGS Kernel Porting Buckets

| CUDA Kernel | Type | MLX Strategy | Complexity |
|---|---|---|---|
| `preprocessCUDA` (per-Gaussian) | Elementwise | Pure MLX vectorized ops | MEDIUM |
| `computeCov3D` (quat→cov) | Elementwise | Pure MLX: `M = s[:,None] * R; Sigma = M^T @ M` | EASY |
| `computeCov2D` (EWA projection) | Elementwise | Pure MLX: Jacobian + matrix product | EASY |
| `computeColorFromSH` (SH→RGB) | Elementwise | Pure MLX: degree-by-degree eval | EASY |
| `duplicateWithKeys` + CUB sort | Sort/scatter | `np.lexsort` on (tile_id, depth) pairs | MEDIUM |
| `identifyTileRanges` | Segment boundaries | `np.diff` + boundary detection | EASY |
| `renderCUDA` forward (tile alpha blend) | Tile-based with shared mem | NumPy tile loops (Phase 1) → Metal kernel (Phase 2) | HARD |
| `renderCUDA` backward (reverse alpha) | Tile-based with atomics | NumPy tile loops (Phase 1) → Metal kernel (Phase 2) | HARD |

### Key Pattern: GLM Convention Avoidance

**CRITICAL LESSON:** GLM uses column-major storage with column-vector convention. Manually porting GLM matrix derivatives (especially `dL_dM = 2.0f * M * dL_dSigma`) is extremely error-prone. The `*` operator in GLM performs standard matrix multiply, but the column-major storage means indices map differently than row-major C/Python.

**Solution:** For any function that is already implemented as pure MLX ops in the forward pass, use `mx.grad()` for the backward pass instead of manually porting the CUDA backward:

```python
def compute_cov3D_backward(scales, scale_modifier, rotations, dL_dcov3D):
    """Use MLX autodiff through forward — correct by construction."""
    from .projection import compute_cov3D

    def loss_scales(s):
        cov = compute_cov3D(s, scale_modifier, rotations)
        return mx.sum(dL_dcov3D * cov)

    def loss_rotations(r):
        cov = compute_cov3D(scales, scale_modifier, r)
        return mx.sum(dL_dcov3D * cov)

    return mx.grad(loss_scales)(scales), mx.grad(loss_rotations)(rotations)
```

**When to manually port CUDA backward vs. use MLX autodiff:**
- **Use MLX autodiff** when the forward pass is pure MLX ops (cov3D, cov2D, SH eval, projection)
- **Manually port** when the forward involves non-differentiable operations (sorting, tile assignment, discrete culling) or when the backward has a fundamentally different algorithm (reverse-order tile traversal with accumulated state)

### Key Pattern: Column-Major Matrix Indexing

CUDA/GLM stores 4x4 matrices column-major as flat `float[16]`:
```
matrix[0]=m00  matrix[4]=m01  matrix[8]=m02   matrix[12]=m03
matrix[1]=m10  matrix[5]=m11  matrix[9]=m12   matrix[13]=m13
matrix[2]=m20  matrix[6]=m21  matrix[10]=m22  matrix[14]=m23
matrix[3]=m30  matrix[7]=m31  matrix[11]=m32  matrix[15]=m33
```

**In MLX, keep the flat (16,) array and index directly:**
```python
def transform_point_4x3(points, matrix):
    m = matrix  # keep flat, do NOT reshape
    x, y, z = points[:, 0], points[:, 1], points[:, 2]
    tx = m[0] * x + m[4] * y + m[8] * z + m[12]
    ty = m[1] * x + m[5] * y + m[9] * z + m[13]
    tz = m[2] * x + m[6] * y + m[10] * z + m[14]
    return mx.stack([tx, ty, tz], axis=-1)
```

**Do NOT reshape to (4,4)** — it causes broadcasting errors and index confusion between row-major and column-major.

### Key Pattern: Tile-Based Sorting Without CUB

CUB radix sort is replaced with numpy lexsort:

```python
# Expand visible Gaussians to tile-Gaussian pairs
gaussian_ids = np.repeat(visible_ids, tiles_per_gaussian)
expanded_depths = np.repeat(vis_depths, tiles_per_gaussian)

# Sort by (tile_id, depth) — lexsort sorts by last key first
sort_order = np.lexsort((expanded_depths, tile_ids))

# Build per-tile ranges from sorted boundaries
changes = np.concatenate([[0], np.where(np.diff(sorted_tile_ids) != 0)[0] + 1, [total]])
for i in range(len(changes) - 1):
    ranges[sorted_tile_ids[changes[i]]] = (changes[i], changes[i+1])
```

### Key Pattern: @mx.custom_function for Rasterization VJP

The rasterize pipeline has non-differentiable steps (sorting, tile assignment, culling), so `mx.grad` can't autodiff through the whole thing. Use `@mx.custom_function` with a custom VJP:

```python
@mx.custom_function
def rasterize_diff(means3D, colors, opacities, ...):
    # Forward: preprocess → sort → render
    return rendered_image

@rasterize_diff.vjp
def rasterize_vjp(primals, cotangents, output):
    # 1. Re-run forward to get intermediate state (cov, sorted lists, etc.)
    # 2. Render backward (reverse traversal) → dL/dmean2D, dL/dconic, dL/dcolor, dL/dopacity
    # 3. Preprocess backward (use mx.grad for cov3D/SH, manual for projection)
    return (dL_dmeans3D, dL_dcolors, dL_dopacity, dL_dscales, dL_drotations, ...)
```

**Pack non-differentiable settings into an array** to work with `@mx.custom_function`:
```python
settings_packed = mx.array([H, W, tanfovx, tanfovy, scale_mod, sh_deg, use_sh, prefiltered])
```

### Key Pattern: Hybrid Backward (Manual Render + Autodiff Preprocess)

The backward pass is best split into two stages:
1. **Render backward** — Must be manually implemented (reverse-order tile traversal with accumulated alpha state). This produces `dL/dmean2D`, `dL/dconic`, `dL/dcolor`, `dL/dopacity`.
2. **Preprocess backward** — Use `mx.grad()` through the pure MLX forward functions for `cov3D`, `cov2D`, and SH. Only the projection gradient (NDC→pixel coordinate chain) needs manual implementation.

### 3DGS Port Phases

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 1 | Pure Python/MLX forward pass + numpy renderer | Reference implementation |
| Phase 2 | `@mx.custom_function` VJP + backward pass | Needed for training |
| Phase 3 | Metal kernels for renderer (16x16 tile blocks with shared memory) | Performance |
| Phase 4 | Cross-validation vs CUDA reference + benchmark suite | Quality |

### 3DGS-Specific Gotchas

21. **GLM column-major ≠ numpy/MLX row-major** — Never reshape a flat (16,) column-major matrix to (4,4) in MLX. Access elements with flat indices matching the CUDA code exactly.
22. **`mx.zeros_like(arr, dtype=...)` not supported** — Use `mx.zeros(arr.shape, dtype=...)` instead.
23. **`mx.array.squeeze(-1)` on (1,1) → scalar** — Use `arr[:, 0]` to get `(1,)` shape reliably.
24. **Use MLX autodiff for backward when possible** — Manually porting GLM matrix calculus is error-prone. If the forward is pure MLX, use `mx.grad()` and it's correct by construction.
25. **Tile sorting is CPU-bound** — The `np.lexsort` approach works but is a bottleneck for >100K Gaussians. A Metal kernel for radix sort would be the Phase 3 optimization.
26. **The renderer forward/backward MUST be manually ported** — The tile-based alpha blending with shared memory and reverse-order traversal can't be auto-differentiated. This is the hardest kernel to port.
27. **`mx.eval()` before numpy conversion** — Always materialize MLX arrays before passing to numpy for the sorting/rendering stages.

### 3DGS Port Stats (Reference)

- Source: 5 CUDA kernels, 4 .cu files, 8 .h files, ~4300 LOC
- MLX port: 5 Python modules, 2 test files, ~2000 LOC
- 14 tests, all passing (forward + backward)
- Forward: pure MLX ops for preprocessing, numpy for tile rendering (Phase 1)
- Backward: hybrid (MLX autodiff for cov3D/SH, manual for render, projection)
- Repo: `github.com/RobotFlow-Labs/diff-gaussian-rasterization-mlx`
- Upstream: `github.com/graphdeco-inria/diff-gaussian-rasterization`

## References

- IsaacLab learned patterns and wins: `references/progress_log.md`
- ZED stereo supervision doc: `zed-sdk-mlx/claude_supervision.md`
- ZED stereo progress log: `zed-sdk-mlx/references/progress_log.md`
- Pointelligence MLX port: `github.com/RobotFlow-Labs/pointelligence-mlx`
- RealSense MLX PRDs: `realsense-mlx/prds/`
- librealsense source: `librealsense/` (Intel RealSense SDK v2.57.6)
- Triton-MLX port: `github.com/RobotFlow-Labs/triton-mlx`
- Upstream Triton: `github.com/triton-inference-server/server` (v2.67.0dev)
- 3DGS MLX port: `github.com/RobotFlow-Labs/diff-gaussian-rasterization-mlx`
- Upstream 3DGS: `github.com/graphdeco-inria/diff-gaussian-rasterization`
- ANIMA Skuld SAM+CLIP MLX: `github.com/RobotFlow-Labs/project_skuld`
- ANIMA TYR Multi-View 3D Tracker MLX: `github.com/RobotFlow-Labs/project_tyr`
- MLX releases: `github.com/ml-explore/mlx/releases` (CHECK THIS FIRST)

---

## Vision Foundation Models → MLX Port (SAM + CLIP Pattern)

This section covers porting SAM (Segment-Anything) and CLIP from PyTorch CUDA to MLX for open-vocabulary segmentation on Apple Silicon. Validated in ANIMA Skuld (OVerSeeC) project.

### Architecture: Backend Factory Pattern

For vision model ports where multiple backends must coexist, use a **factory + auto-detect** pattern instead of scattered conditionals:

```python
# backend.py — single entry point
def detect_device() -> str:
    """MLX > CUDA > MPS > CPU priority."""
    if _is_apple_silicon() and _has_mlx():
        return "mlx"
    if _has_torch_cuda():
        return "cuda:0"
    if _is_apple_silicon() and _has_torch_mps():
        return "mps"
    return "cpu"

def create_clip_encoder(device: str):
    device = resolve_device(device)  # "auto" → concrete
    if device == "mlx":
        from .clip_encoder_mlx import CLIPEncoderMLX
        return CLIPEncoderMLX()
    from .clip_encoder import CLIPEncoder
    return CLIPEncoder(device=device)
```

**Key insight:** The factory returns objects with identical APIs — callers never know which backend they're using. The `similarity()` method returns numpy arrays from both backends.

### Available MLX Packages for Vision Models (as of 2026-03)

| Model | MLX Package | Install | API Style |
|-------|-------------|---------|-----------|
| **CLIP** | `mlx_clip` (harperreed) | `pip install mlx_clip` or `pip install git+https://github.com/harperreed/mlx_clip.git` | `clip.text_encoder(texts)`, `clip.image_encoder(path)` |
| **CLIP** | `ml-explore/mlx-examples/clip` | Clone + local import | `model(**inputs)` → `.text_embeds`, `.image_embeds` |
| **SAM 3** | `mlx_sam3` (Deekshith-Dade) | `pip install git+https://github.com/Deekshith-Dade/mlx_sam3.git` | `SAM3().segment(image)` |
| **SAM** | PyTorch on MPS | `pip install segment-anything` | Standard SAM API on `"mps"` device |

### CLIP MLX Gotchas

28. **`mlx_clip.image_encoder()` expects a file path, not numpy array** — Must save to temp file first:
    ```python
    with tempfile.NamedTemporaryFile(suffix=".png") as f:
        Image.fromarray(image).save(f.name)
        embedding = clip.image_encoder(f.name)
    ```
29. **Return types differ** — PyTorch CLIP returns `torch.Tensor`, mlx_clip returns `mlx.core.array`. Always normalize to numpy at the API boundary:
    ```python
    emb_np = np.array(embedding)
    norms = np.linalg.norm(emb_np, axis=-1, keepdims=True)
    return emb_np / (norms + 1e-8)
    ```
30. **HuggingFace model IDs for conversion** — `mlx_clip` auto-converts from HF: `MLXClip("openai/clip-vit-large-patch14")`. First load is slow (weight conversion), subsequent loads are cached.

### SAM MLX Gotchas

31. **mlx_sam3 is SAM 3 (not SAM 1)** — Different model architecture. The output format may differ from `segment_anything.SamAutomaticMaskGenerator`. Write an adapter:
    ```python
    class _MLXSam3Generator:
        def generate(self, image):
            results = self._model.segment(image)
            return [{"segmentation": r["mask"].astype(bool),
                     "area": int(r["mask"].sum()),
                     "predicted_iou": r.get("iou", 0.9)} for r in results]
    ```
32. **PyTorch SAM on MPS is a strong fallback** — On Apple Silicon, `segment-anything` with `model.to("mps")` runs well. Use this when mlx_sam3 isn't installed:
    ```python
    def _try_load_torch_mps(self):
        model = sam_model_registry[vit_type](checkpoint=ckpt_path)
        model.to("mps")  # Apple GPU via PyTorch
    ```
33. **SAM checkpoints are PyTorch format (.pth)** — Even for MPS fallback, use the same Meta checkpoint URLs. No conversion needed for MPS.

### Config Pattern for Multi-Backend Vision

```yaml
segmentation:
  device: "auto"  # "auto" | "mlx" | "cuda:0" | "mps" | "cpu"
```

Use `"auto"` as default in config — it resolves at runtime via `detect_device()`. This means:
- On Mac with MLX installed → uses MLX natively
- On Mac without MLX → uses PyTorch MPS (still fast)
- On Linux with NVIDIA GPU → uses CUDA
- Anywhere else → CPU fallback

### Import Safety Rules (Vision Models)

All vision model imports MUST be lazy (inside methods, not at module top):
```python
# GOOD — import-safe on any platform
def _load(self):
    try:
        from mlx_clip import mlx_clip
    except ImportError:
        raise ImportError("Install mlx_clip: ...")

# BAD — crashes on import if mlx not installed
import mlx.core  # Top-level import
```

### Testing Multi-Backend Vision Code

```python
# Test that factory returns correct type for each backend
def test_create_clip_encoder_cpu():
    encoder = create_clip_encoder("cpu")
    assert isinstance(encoder, CLIPEncoder)  # PyTorch version

@pytest.mark.skipif(not _has_mlx(), reason="MLX not installed")
def test_create_clip_encoder_mlx():
    encoder = create_clip_encoder("mlx")
    assert isinstance(encoder, CLIPEncoderMLX)

# Test interface compatibility (both backends have same methods)
def test_clip_interface():
    for cls in [CLIPEncoder, CLIPEncoderMLX]:
        assert hasattr(cls, "encode_text")
        assert hasattr(cls, "encode_image")
        assert hasattr(cls, "similarity")
```

### ANIMA Skuld Port Stats (Reference)

- Source: PyTorch CUDA SAM + CLIP (2 files, ~160 LOC)
- MLX port: 4 new files (backend.py, clip_encoder_mlx.py, sam_wrapper_mlx.py, test_backend.py), ~600 LOC
- 85 tests passing, 13 new backend tests
- Backend priority: MLX → CUDA → MPS → CPU (auto-detect)
- Config change: `device: "cuda:0"` → `device: "auto"`
- Repo: `github.com/RobotFlow-Labs/project_skuld`

### ANIMA TYR Port Stats (Reference)

- Source: PyTorch multi-view 3D point tracker (ResNet+Fusion+Transformer+LSTM)
- MLX port: 8 new files (backend, backbone_mlx, fusion_mlx, update_mlx, mvtracker_mlx, loss_mlx, trainer_mlx, train_mlx.py), ~1500 LOC
- 39 tests passing (28 PyTorch + 11 MLX)
- Backend priority: MLX > CUDA > MPS > CPU (auto-detect factory)
- MLX 0.31.1: used native nn.LSTM, nn.Conv2d (NHWC), nn.MultiHeadAttention, nn.MaxPool2d, nn.BatchNorm
- Full gradient flow verified: nn.value_and_grad through backbone+fusion+transformer+LSTM+heads
- Repo: `github.com/RobotFlow-Labs/project_tyr`

### TYR MLX Gotchas

34. **`self.update` conflicts with `nn.Module.update()`** — MLX's `nn.Module` has a built-in `update()` method for parameter updates. Naming an attribute `self.update` causes `AttributeError: object has no attribute 'update'`. Rename to `self.knn_update` or similar.
35. **MLX LSTM hidden state is `(1, hidden_size)` not `(batch, hidden_size)`** — When N (batch dim) changes between calls (e.g., variable number of fused 3D points), you cannot carry hidden state across. Either fix N or reset hidden state per frame.
36. **NHWC everywhere** — MLX Conv2d expects `[B, H, W, C]`. When porting PyTorch models, transpose ALL image tensors at the boundary: `arr.transpose(0, 1, 3, 4, 2)` for `[K,T,C,H,W] -> [K,T,H,W,C]`.
37. **Loss functions for `nn.value_and_grad` must NOT be `nn.Module`** — Use plain callable classes or functions. `nn.value_and_grad(model, loss_fn)` takes the model as first arg to differentiate; the loss_fn should be a plain function that calls the model.
38. **Always check MLX GitHub releases before starting** — `https://github.com/ml-explore/mlx/releases`. The nn module inventory expanded dramatically: v0.31+ has LSTM, GRU, MaxPool2d, Transformer, which earlier versions lacked. Don't reimplement what already exists.
