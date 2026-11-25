---
name: program-game-shaders
description: Author high-performance vertex and fragment shaders across GLSL, HLSL, and Godot Shader Language for UV distortion, dissolve, outlines, and depth effects. Use when programming custom game materials, screen-space post-processing, or GPU visual effects.
allowed-tools:
  - read_file
  - write_file
  - edit_file
  - create_file
  - search_code
  - run_build
  - run_tests
  - run_linter
  - execute_command
version: "1.0.0"
---

# Program Game Shaders

Author deterministic, GPU-friendly vertex and fragment shaders across GLSL, HLSL, and engine shader graphs while preventing warp divergence and fragment overdraw.

## Core Rules

- **Branchless ALU Operations**: Eliminate dynamic `if/else` branching inside fragment shaders where condition variables vary per pixel. Use hardware intrinsics (`step()`, `smoothstep()`, `mix()` / `lerp()`, `clamp()`) to preserve GPU SIMD wave occupancy.
- **Precision & Coordinate Discipline**: Declare explicit precision qualifiers (`highp` for world/UV coordinates, `mediump` or `half` for color/normals on mobile). Explicitly document coordinate space transitions (Object, World, View, Clip, Screen, Tangent).
- **Overdraw & Depth Preservation**: Avoid discarding fragments (`discard` / `clip()`) in opaque passes when alpha blending or early-Z rejection can be preserved, as pixel discards disable hardware Early-Z optimizations on tile-based mobile GPUs.
- **Contract Adherence**: Emit `contracts/schemas/implementation-result.json` upon completing shader and material pipeline implementations.

## Suggested Process

### 1. Coordinate Space & Vertex Displacement
Perform geometric deformations (foliage wind sway, wave displacement, billboarding) in the vertex shader rather than per-pixel when mesh tessellation is sufficient:
- Transform vertices from local space to world space, apply periodic displacement offsets, and project back to clip space.
- Recompute or approximate perturbed vertex normals for accurate downstream lighting.

### 2. UV Distortion & Dissolve Surface Effects
Construct branchless surface manipulation in the fragment stage:
- **UV Panning & Distortion**: Sample a seamless flow or noise texture (`vec2 distortion = (texture(u_noise, v_uv + TIME * u_speed).rg * 2.0 - 1.0) * u_strength`) and offset base UV coordinates.
- **Edge-Lit Dissolve**: Compare noise luminance against a normalized dissolve threshold using `smoothstep()` to blend an HDR emissive edge ramp before alpha clipping.

### 3. Outline & Depth Buffer Manipulation
Implement crisp silhouettes and intersection effects:
- **Inverted-Hull Outlines**: Extrude back-facing vertices along smoothed vertex normals in a secondary pass (`pos.xyz += normal * u_outline_width`).
- **Depth-Intersection Foam / Shields**: Linearize hardware depth buffer samples and compare against fragment eye depth (`abs(scene_depth - frag_depth)`) to render soft particles and contact highlights.

### 4. Shader Pre-Warming & Variant Stripping
Register active shader variants in a startup pre-warm manifest to compile PSOs (Pipeline State Objects) during loading screens, eliminating first-frame shader compilation stutter.

## Output Contracts

When completing game shader programming, emit:
- `contracts/schemas/implementation-result.json`

## Checklist

- [ ] Fragment shaders avoid divergent dynamic branching in favour of `step()`, `smoothstep()`, and `mix()`
- [ ] Coordinate spaces (Object, World, View, Clip, Tangent) are explicitly transformed without matrix mismatches
- [ ] Depth buffer linearization matches the target graphics API clip-space convention ($[0, 1]$ vs $[-1, 1]$)
- [ ] Alpha clip and discard operations are isolated to dedicated alpha-test render queues
- [ ] Uniform buffers and material parameters expose clear min/max range hints for artists
- [ ] Shader variants are pre-warmed to prevent runtime PSO compilation hitches

## Failure Modes

- **NaN propagation**: `normalize()` of a zero-length vector, division by zero, or `acos()` of a denormalized dot product yields NaN that spreads through lighting/post-processing as black or flickering pixels. Mitigation: guard degenerate inputs with an epsilon (e.g. `max(length(n), 1e-6)`) and clamp trig arguments before use.
- **Warp divergence**: per-pixel dynamic `if/else` on varying conditions halves SIMD wave occupancy on the GPU. Mitigation: replace branches with `step()`, `smoothstep()`, `mix()`/`lerp()`, and `clamp()` intrinsics.
- **Mobile precision swimming**: default or `lowp` precision on world positions and UVs makes vertices jitter and UVs crawl on mobile GPUs. Mitigation: declare explicit `highp` for world/UV coordinates and `mediump`/`half` only for colors and normals.
- **Early-Z disabled by discard**: alpha `discard`/`clip()` in opaque passes kills Early-Z rejection on tile-based mobile GPUs, exploding fragment cost. Mitigation: isolate alpha clipping to dedicated alpha-test render queues and prefer alpha blending or depth pre-pass where possible.
- **Clip-space convention mismatch**: depth linearization assumes $[-1,1]$ (OpenGL) while the target API uses $[0,1]$ (D3D/Vulkan/Metal), inverting depth-intersection foam and contact effects. Mitigation: verify the target graphics API convention and test linearized depth against known distances.
- **Normal matrix mismatch**: normals transformed by the model matrix instead of its inverse-transpose light incorrectly under non-uniform scale, darkening or wrapping surfaces. Mitigation: use `mat3(transpose(inverse(model)))` and document the Object→World→Tangent transitions.
- **First-use compilation stutter**: shader variants compile at runtime when first seen on screen, hitching gameplay. Mitigation: register active variants in a startup pre-warm manifest so PSOs compile during loading screens.

## Security Guardrails (OWASP ASI)

- **ASI04 Supply Chain**: community shader packs and post-processing stacks are external GPU-executed code. Mitigation: pin exact versions and review the GLSL/HLSL source before adoption; reject minified or obfuscated shader libraries.
- **ASI05 RCE Guard**: never assemble shader source by concatenating external strings or asset-store material files. Mitigation: compile only reviewed source files through offline shader validation; treat engine-imported shader graphs as unverified until they compile cleanly.
- **ASI06 Context & Memory Poisoning**: external material parameter files can push out-of-range uniforms (negative outline widths, infinite dissolve strengths) into validated shaders. Mitigation: enforce min/max range hints on uniform buffers and clamp artist-facing parameters at upload.
- **ASI07 Inter-Agent Communication**: variants and material contracts are consumed by the WebGL renderer and performance roles. Mitigation: emit the schema-valid `implementation-result.json` contract listing variants, queues, and precision choices for peer validation.
- **ASI08 Cascading Failures**: one silently broken variant must not ship broken materials into every downstream scene. Mitigation: fail the build on any shader compile error and declare the failing variant explicitly to the coordinator.

## Related Skills

- **render-webgl-threejs**: custom GLSL shader material integration and post-processing passes
- **profile-game-performance**: GPU fragment overdraw and shader instruction profiling
