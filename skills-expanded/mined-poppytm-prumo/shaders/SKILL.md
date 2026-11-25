# Shader Authoring & Compilation

## 1. Purpose
Author, optimize, cross-compile, and statically validate GPU shaders across modern shading languages (WGSL, HLSL, GLSL, and SPIR-V). This skill guarantees deterministic host-device memory layout alignment (`std140`/`std430`), minimizes warp/wavefront execution divergence, eliminates runtime Pipeline State Object (PSO) stutter through offline compilation/caching, and automates CPU-GPU struct reflection.

---

## 2. Use When
- Authoring or modifying vertex, fragment, compute, or mesh shaders in WGSL, HLSL, GLSL, or SPIR-V.
- Structuring host-device buffer layouts (Uniform Buffers `std140`, Storage Buffers `std430`, Push Constants / Root Constants).
- Designing multi-platform shader build pipelines (cross-compilation via `dxc`, `glslangValidator`, `naga`, or `SPIRV-Cross`).
- Profiling GPU occupancy, eliminating warp/wavefront branch divergence, or managing compute shared memory (`workgroup` memory).
- Operating in mode(s): `implementation`, `architecture`, `verification`.

---

## 3. Do Not Use When
- Working strictly on CPU-side higher-level scenegraph logic with no shader code or buffer layout modifications.
- Dealing exclusively with UI CSS styling or pure 2D canvas drawing without custom GPU shaders.
- Task is constrained by sandbox policies that forbid invoking shader compilers (`dxc`, `glslc`, `naga`).

---

## 4. Required Context
Before authoring or modifying shaders, verify:
- **Target Shading Language & Version**: WGSL (W3C WebGPU), HLSL (Shader Model 6.0+), GLSL (4.50+), or Vulkan SPIR-V 1.5+.
- **Binding Frequency Hierarchy**:
  - `Set 0 / Group 0`: Per-Frame (View, Projection, Global Time, Sun Direction).
  - `Set 1 / Group 1`: Per-Pass (Shadow maps, Ambient Occlusion, Light Grids).
  - `Set 2 / Group 2`: Per-Material (Albedo, Normal maps, Roughness/Metallic, Material Uniforms).
  - `Set 3 / Group 3`: Per-Draw / Instance (Model Matrix, Instance Data).
- **Target Hardware Architecture**: Discrete desktop (Warp 32 / Wave 64) vs Tile-based mobile GPU (ARM Mali, Qualcomm Adreno, Apple Silicon).

---

## 5. Procedure

```
[Shader Source (WGSL/HLSL)]
         |
         v
[1. Layout & Alignment Check] ----> Verify std140/std430 & explicit padding
         |
         v
[2. Offline Static Compilation] --> Validate syntax via dxc / glslc / naga
         |
         v
[3. Reflection Generation] -------> Extract bindings & CPU struct headers
         |
         v
[4. Divergence & Occupancy Audit] -> Check dynamic branches & register pressure
         |
         v
[5. Pipeline Cache Injection] ----> Emit pre-warmed PSO / bytecode artifacts
```

### Step 1: Memory Layout & Alignment Enforcement
1. **Uniform Buffers (`std140`)**:
   - Scalars (`f32`, `i32`, `u32`): 4-byte aligned.
   - 2-component vectors (`vec2`): 8-byte aligned.
   - 3-component & 4-component vectors (`vec3`, `vec4`): 16-byte aligned.
   - **Crucial Rule**: Arrays in `std140` always have their element stride rounded up to 16 bytes! Never pack `float arr[4]` without acknowledging each element consumes 16 bytes (`vec4` stride).
2. **Storage Buffers (`std430` / WGSL `var<storage>`)**:
   - Allows tightly packed arrays matching natural alignment (e.g., `float arr[]` has 4-byte stride).
   - In WGSL, always insert explicit padding fields (e.g., `_pad: f32`) or `@align(16)` attributes to eliminate host-device ABI discrepancies.

### Step 2: Static Validation & Compilation
Compile shader sources offline during CI/build rather than relying on runtime compilation:
- **WGSL**: Validate via `naga` CLI or Naga/wgpu parser.
- **HLSL**: Compile with DirectX Shader Compiler (`dxc -T ps_6_0 -E main`).
- **GLSL / Vulkan**: Compile with `glslc -fshader-stage=fragment shader.frag -o shader.spv`.
Verify that compiler warnings are treated as hard errors (`-Werror`).

### Step 3: Divergence & Control Flow Optimization
1. **Branch Divergence**:
   - Threads in a Warp (32 threads) or Wavefront (64 threads) execute in lockstep.
   - If invocations in the same warp take different branches of an `if-else`, both branches execute serially with inactive threads masked out (execution time = $T_{\text{then}} + T_{\text{else}}$).
   - Replace branch divergence on continuous variables with branchless arithmetic: `clamp()`, `mix()`, `step()`, `smoothstep()`.
2. **Uniform Control Flow**:
   - Texture sampling operations requiring implicit screen-space derivatives (`textureSample()`, `dFdx()`, `dFdy()`) **must** be executed in uniform control flow. Sampling inside non-uniform loops causes undefined derivative artifacts or GPU crashes.

### Step 4: Workgroup Shared Memory & Synchronization
In compute shaders:
1. Shared workgroup memory (`var<workgroup>` in WGSL, `groupshared` in HLSL) is on-chip SRAM shared across invocations of the same workgroup.
2. Every write to workgroup memory must be followed by `workgroupBarrier()` before any invocation reads the memory.
3. Keep workgroup sizes multiples of hardware warp size (typically 64 or 128 threads) to maximize ALU occupancy. Avoid arbitrary sizes like 47 or 100.

### Step 5: CPU-GPU Reflection Automation
Generate binary-identical C++ / Rust / Go struct definitions from the compiled shader reflection metadata. Never manually duplicate struct definitions across CPU and GPU codebases.

---

## 6. Decision Rules & Invariants
- **RULE 1 (Explicit Struct Padding)**: Every struct shared across the CPU/GPU boundary must be explicitly padded so that struct size is an exact multiple of 16 bytes.
- **RULE 2 (No Derivatives in Divergent Branches)**: Never invoke gradient/derivative instructions (`texture()`, `dFdx()`, `dFdy()`) inside divergent conditional branches. Use explicit LoD sampling (`textureLod()`, `textureSampleLevel()`) if sampling inside divergent branches.
- **RULE 3 (Register Pressure Budget)**: Limit local variable proliferation in compute/fragment shaders. High register usage reduces the active warp occupancy per Streaming Multiprocessor (SM/CU).
- **RULE 4 (Zero Runtime Compilation Hitches)**: All graphics pipelines and compute shaders must be pre-compiled into a Pipeline Cache (`VkPipelineCache`, Metal Binary Archive, or WebGPU pipeline pre-creation) at application initialization.

---

## 7. Evidence Required
- **Compilation Artifact**: Zero compiler warnings or errors from `glslc`, `dxc`, or `naga`.
- **Layout Conformance Evidence**: Static struct size and field offset verification between host language and GPU shader.
- **Divergence Analysis**: Verification of uniform control flow around derivative and barrier instructions.

---

## 8. Output Contract
- Validated shader source code (`.wgsl`, `.hlsl`, `.frag`, `.vert`, `.comp`).
- Shader compilation report detailing bindings, layout offsets, and register pressure.
- Reflection header / struct binding module for host integration.

---

## 9. Stop Conditions
- All shaders compile cleanly with zero errors under strict compiler validation.
- All UBO/SSBO struct alignments adhere strictly to `std140`/`std430` and host ABI.
- Token budget exhausted.
- Blocked on external dependency.

---

## 10. Escalation Rules
- Escalate to graphics architecture lead if hardware-specific bugs require divergence workarounds that reduce visual fidelity.
- Escalate if pipeline cache hitches cannot be resolved without restructuring the asset loading subsystem.
