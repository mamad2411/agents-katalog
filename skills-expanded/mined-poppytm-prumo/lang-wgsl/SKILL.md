---
name: lang-wgsl
description: W3C WebGPU Shading Language (WGSL) engineering, strict struct alignment & padding rules, explicit address spaces, workgroup synchronization with workgroupBarrier(), atomic operations, and naga/wgpu CI validation.
---

# WGSL WebGPU Soundness & Shader Engineering Contract

## 1. Title and Description
**WGSL WebGPU Soundness & Shader Engineering Contract (`lang-wgsl`)**
Governs the authoring, optimization, memory layout, and validation of shaders written in WebGPU Shading Language (WGSL). Guarantees cross-platform portability across Vulkan, Metal, Direct3D 12, and WebGPU in browsers by enforcing memory alignment, compute barrier semantics, atomic safety, and static analysis under Naga/Tint.

## 2. Purpose
Prevent silent GPU crashes, host-GPU buffer layout desynchronization, race conditions in compute shaders, and driver-specific shader compilation rejections across varied hardware architectures.

## 3. Prerequisites
- WGSL syntax conforming to the official W3C Recommendation.
- Toolchain: Naga CLI (`cargo install naga-cli`) or Tint (`dawn` compiler tools).

## 4. Inputs
- WGSL shader sources (`*.wgsl`).
- Host-side buffer definitions in Rust (`bytemuck`, `encase`), C++, or TypeScript.
- Target pipeline stage: Vertex, Fragment, or Compute.

## 5. Outputs
- Schema-valid, verified WGSL shader source code.
- Explicit struct definitions with verified field offsets and padding.
- Validation artifacts from Naga/Tint.
- Verification report conforming to `templates/wgsl-verification-report.md`.

## 6. Execution Steps

### Step 1: Memory Layout & Struct Alignment Rules
WebGPU enforces strict memory alignment rules based on the Vulkan memory model. Host applications and WGSL structs must have identical byte offsets:
1. **Scalar Alignments**:
   - `f32`, `i32`, `u32`: Alignment = 4 bytes, Size = 4 bytes.
   - `f16` (when `enable f16;` is active): Alignment = 2 bytes, Size = 2 bytes.
2. **Vector Alignments**:
   - `vec2<T>`: Alignment = 8 bytes, Size = 8 bytes.
   - `vec3<T>`: **Alignment = 16 bytes, Size = 12 bytes** (CAUTION: leaves a 4-byte padding hole!).
   - `vec4<T>`: Alignment = 16 bytes, Size = 16 bytes.
3. **Matrix Alignments**:
   - `mat3x3<f32>`: Consists of 3 column vectors of `vec3<f32>` -> Alignment = 16 bytes, Size = 48 bytes.
   - `mat4x4<f32>`: Consists of 4 column vectors of `vec4<f32>` -> Alignment = 16 bytes, Size = 64 bytes.
4. **The `vec3` Padding Hazard**:
   - Never place a scalar immediately after a `vec3<f32>` assuming it packs into the remaining 4 bytes without testing host serialization.
   - Preferred practice: Use `vec4<f32>` or insert explicit padding fields (`_pad: f32`) with `@align(16)` attributes.

### Step 2: Explicit Address Spaces & Access Modes
Declare every binding variable with its explicit address space and access mode:
- `var<uniform> u_camera: CameraUniforms;` (read-only, size <= 64KB, cached in GPU constant cache).
- `var<storage, read> s_instances: array<InstanceData>;` (read-only unbounded buffer).
- `var<storage, read_write> s_particles: array<Particle>;` (read/write storage buffer).
- `var<workgroup> s_cache: array<f32, 64>;` (shared across threads in the same compute workgroup).
- `var<private> v_color: vec4<f32>;` (per-invocation private global).

### Step 3: Compute Shader Workgroup Sizing & Schedulers
1. **Workgroup Size Tuning**:
   - Use `@workgroup_size(X, Y, Z)`. Total invocations `X * Y * Z` should generally be a multiple of 32 (NVIDIA warp size) or 64 (AMD wavefront size).
   - Common balanced defaults: `@workgroup_size(64, 1, 1)` or `@workgroup_size(16, 16, 1)` for 2D images.
   - Maximum invocations per workgroup must not exceed 256 for universal WebGPU mobile/desktop compatibility.

### Step 4: Workgroup Synchronization & Atomics
1. **Workgroup Memory Barrier**:
   - When multiple invocations write to `var<workgroup>` memory, invoke `workgroupBarrier()` before any thread reads the shared data.
   - Semantics: Guarantees that all writes to `workgroup` memory by all threads in the workgroup are complete and visible to all other threads in that workgroup.
2. **Atomic Operations**:
   - Use `atomic<u32>` or `atomic<i32>` for counters and histograms.
   - Call built-ins: `atomicAdd(&counter, 1u)`, `atomicMin`, `atomicMax`, `atomicExchange`.
   - Never perform non-atomic reads or writes on shared locations concurrently without barriers.

### Step 5: Texture Sampling & Control Flow Restrictions
1. **Uniform Control Flow for Implicit Derivatives**:
   - Operations that calculate screen-space derivatives (e.g. `textureSample`, `dpdx`, `dpdy`) must **only** be executed in uniform control flow.
   - Never call `textureSample` inside non-uniform conditional branches (`if (thread_id == 0)`). If sampling inside divergent code, use `textureSampleLevel` with an explicit mip level.

### Step 6: Automated CI Validation with Naga
Every shader must be validated through static analysis:
```bash
naga path/to/shader.wgsl
```
Naga validates type soundess, struct padding, entry point signatures, and resource bindings, converting to SPIR-V, MSL, or HLSL.

## 7. Verification
```bash
# 1. Naga syntax and type check
naga src/shaders/*.wgsl

# 2. Check for vec3 padding alignment traps
grep -n "vec3<" src/shaders/*.wgsl
```

## 8. Fallbacks & Failure Recovery
| Failure Class | Root Cause | Deterministic Remediation |
|---|---|---|
| Struct Offset Mismatch | Host `struct` size does not match WGSL struct size due to padding | Add explicit `@align(16)` or `@size(N)` attributes to WGSL fields, or use `vec4<f32>` instead of `vec3<f32>`. |
| Derivative in Non-Uniform Control Flow | `textureSample` called inside dynamic conditional block | Switch to `textureSampleLevel(texture, sampler, coords, 0.0)` or move sampling outside the branch. |
| Memory Race in Workgroup | Reading `var<workgroup>` without synchronization | Insert `workgroupBarrier()` between the write loop and the read loop. |
| Buffer Out of Bounds | Storage buffer index exceeds bind group array length | Use `arrayLength(&buffer)` built-in to bounds-check dynamically: `if (id >= arrayLength(&buffer)) { return; }`. |

## 9. Constraints
- **Zero non-standard extensions without capability checks**: Never use optional extensions without declaring `enable <extension>;` and verifying adapter support.
- **Never rely on compiler struct packing**: Always calculate and verify explicit byte alignments for Uniform and Storage buffers.
- **No unbounded recursion**: WGSL forbids recursion; loops must have deterministic termination conditions.

## 10. Examples

### Anti-Pattern: Alignment Trap & Race Condition in Compute
```wgsl
// BAD: Unaligned struct fields, missing workgroupBarrier, unbounded array write
struct BadUniform {
    position: vec3<f32>, // 12 bytes used, 4 bytes padding!
    time: f32,           // Trailing hole trap
    color: vec3<f32>,    // Misaligned on some hardware
};

var<workgroup> temp_data: array<f32, 64>;

@compute @workgroup_size(64)
fn bad_compute(@builtin(local_invocation_id) local_id: vec3<u32>) {
    temp_data[local_id.x] = f32(local_id.x) * 2.0;
    // RACE: No barrier! Thread 0 reads temp_data[1] before Thread 1 finishes writing!
    let neighbor = temp_data[local_id.x + 1u]; 
}
```

### Idiomatic Pattern: Rigorous Alignment & Safe Parallel Reduction
```wgsl
// GOOD: Explicit 16-byte aligned structs, workgroupBarrier synchronization
struct ComputeParameters {
    @align(16) base_scale: vec4<f32>,
    @align(16) element_count: u32,
    _pad0: u32,
    _pad1: u32,
    _pad2: u32,
};

@group(0) @binding(0) var<uniform> params: ComputeParameters;
@group(0) @binding(1) var<storage, read> input_data: array<f32>;
@group(0) @binding(2) var<storage, read_write> output_sum: array<f32>;

var<workgroup> shared_cache: array<f32, 64>;

@compute @workgroup_size(64, 1, 1)
fn main(
    @builtin(global_invocation_id) global_id: vec3<u32>,
    @builtin(local_invocation_id) local_id: vec3<u32>,
    @builtin(workgroup_id) group_id: vec3<u32>
) {
    let tid = local_id.x;
    let gid = global_id.x;

    // 1. Guard against buffer overrun
    if (gid < params.element_count) {
        shared_cache[tid] = input_data[gid] * params.base_scale.x;
    } else {
        shared_cache[tid] = 0.0;
    }

    // 2. Synchronize before cooperative reduction
    workgroupBarrier();

    // 3. Parallel reduction in workgroup shared memory
    for (var s: u32 = 32u; s > 0u; s = s >> 1u) {
        if (tid < s) {
            shared_cache[tid] += shared_cache[tid + s];
        }
        workgroupBarrier();
    }

    // 4. First thread writes reduced workgroup sum
    if (tid == 0u) {
        output_sum[group_id.x] = shared_cache[0];
    }
}
```