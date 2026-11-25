---
name: render-webgl-threejs
description: Architect interactive WebGL2 and WebGPU 3D scenes using Three.js or React Three Fiber with compressed GLTF streaming, PBR materials, and post-processing pipelines. Use when building browser 3D games, WebGPU render loops, or EffectComposer pipelines.
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

# Render WebGL Threejs

Build high-framerate WebGL2 and WebGPU interactive 3D scenes with compressed asset streaming, physically based rendering (PBR), merged post-processing passes, and deterministic VRAM lifecycle management.

## Core Rules

- **Archetype & Backend Pairing**: Match renderer and post-processing to the scene archetype — `WebGPURenderer` + TSL (`MeshStandardNodeMaterial` / `THREE.PostProcessing`) for WebGPU-first pipelines, or `WebGLRenderer` + `pmndrs/postprocessing` `EffectComposer` for WebGL2 compatibility, handling `webglcontextlost`/`webglcontextrestored` and `device.lost` deterministically. Use `frameloop="demand"` + `invalidate()` for idle product configurators and `useThree((s) => s.renderer)` in R3F v9.
- **Anti-AI-3D-Slop Visual & Loop Craft**: Never ship flat `ambientLight` + single white `directionalLight` on `#000000` voids or fisheye `fov 75` `[0,0,5]` cameras. Calibrate PMREM HDRI + 3-point lighting, `AgX`/`ACESFilmic` tone mapping, bounding-sphere camera framing (`fov 35–45`), tight `near`/`far` frustum, grounded contact shadows, and **zero per-frame heap allocations** (`new THREE.Vector3()`, `.clone()`, `setState()`) inside `useFrame`/RAF loops.
- **Color-Space & Compressed Streaming**: Apply `THREE.SRGBColorSpace` strictly to albedo/emissive maps and `THREE.NoColorSpace` (Linear) to normal, roughness, metalness, AO, and packed ORM maps (`flipY = false` for glTF). Enforce Draco/Meshopt geometry compression + KTX2/Basis Universal GPU textures with local bundled WASM decoders.
- **Explicit Full VRAM Disposal**: JavaScript GC and `material.dispose()` do NOT free attached textures. Traverse every node on unmount to dispose every `BufferGeometry`, `Material`, **all texture map properties** (`map`, `normalMap`, `roughnessMap`, `metalnessMap`, `aoMap`, `emissiveMap`), `RenderTarget`s, and `PMREMGenerator`s.
- **Contract Adherence**: Emit `contracts/schemas/implementation-result.json` upon completing WebGL/WebGPU/Three.js rendering slices.

## Suggested Process

### 1. Renderer, Color Space, Camera & Pixel Ratio Setup
Configure the renderer, camera frustum, and tone mapping for consistent cross-device fidelity:
- Set `renderer.toneMapping = THREE.AgXToneMapping` (or `ACESFilmicToneMapping`), `outputColorSpace = THREE.SRGBColorSpace`, and `NoColorSpace` on data/normal/ORM textures.
- Frame product views with `fov 35–45`, bounding-sphere fit, tight `near`/`far` bounds, and `Math.min(window.devicePixelRatio, 2.0)`.

### 2. Asynchronous GLTF Streaming & Instancing
Load 3D scenes via `GLTFLoader` configured with `DRACOLoader`, `MeshoptDecoder`, and `KTX2Loader`:
- Convert repeated static props, foliage, and projectiles into `THREE.InstancedMesh` or `THREE.BatchedMesh` to collapse hundreds of draw calls into a single GPU submission.

### 3. PBR Material & Environment Lighting Calibration
Configure `MeshStandardMaterial` / `MeshPhysicalMaterial` using pre-filtered PMREM environment maps (`PMREMGenerator`):
- Pack metallic, roughness, and ambient occlusion into a single ORM texture (`roughnessMap` = G, `metalnessMap` = B, `aoMap` = R) to halve texture sampler lookups.

### 4. Post-Processing Consolidation & Loop Hygiene
- Merge WebGL2 bloom/vignette/grading into a single `pmndrs/postprocessing` `EffectPass`, or use Three.js node `PostProcessing` (TSL) on `WebGPURenderer` — never chain unmerged full-screen blits.
- Hoist scratch vectors/matrices outside `useFrame`/RAF ticks (`frameloop="demand"` when idle) and respect `prefers-reduced-motion`.

## Output Contracts

When completing WebGL and Three.js rendering implementation, emit:
- `contracts/schemas/implementation-result.json`

## Checklist

- [ ] Renderer clamps DPR to at most 2.0 and handles WebGL context loss/restoration events
- [ ] GLTF pipeline uses Draco/Meshopt geometry compression and KTX2 GPU textures
- [ ] Repeated meshes use `InstancedMesh` or `BatchedMesh` to keep draw calls within budget
- [ ] PBR materials share ORM channel-packed textures and pre-filtered PMREM lighting
- [ ] Post-processing effects are merged into minimal full-screen render passes
- [ ] Geometries, materials, textures, and render targets execute `.dispose()` on unmount

## Failure Modes

- **Context loss crash**: `webglcontextlost` is unhandled, so a mobile tab suspend or GPU driver reset leaves a permanent black canvas. Mitigation: handle `webglcontextlost`/`webglcontextrestored` and re-create or re-upload GPU resources on restore.
- **VRAM leak on unmount**: `BufferGeometry`, `Material`, `Texture`, and `WebGLRenderTarget` are never `.dispose()`d, so GPU memory climbs until the context dies. Mitigation: enforce explicit disposal on every unmount/despawn path; never rely on JS garbage collection for GPU resources.
- **High-DPI fill-rate collapse**: unclamped `devicePixelRatio` (3x–4x on quad-HD phones) quadruples fragment work and tanks frame rate. Mitigation: clamp with `Math.min(window.devicePixelRatio, 2.0)`.
- **Draw call explosion**: repeated props, foliage, and projectiles are rendered as individual meshes, blowing the draw call budget. Mitigation: convert repeated static meshes to `THREE.InstancedMesh`/`BatchedMesh` to collapse them into single GPU submissions.
- **Main-thread decode stall**: uncompressed GLTF geometry and textures decode on the main thread, freezing interaction for seconds during streaming. Mitigation: enforce Draco/Meshopt geometry compression and KTX2/Basis textures so assets stay compressed and decode off the main thread.
- **Post-process blit chain**: bloom, vignette, and grading run as separate full-screen passes, exhausting the fragment budget. Mitigation: merge effects into a single `EffectComposer` `EffectPass` instead of chained render-target blits.
- **Color space mismatch**: linear colors are written to an sRGB-expecting display (or tone mapping is missing), washing out or darkening PBR output. Mitigation: set `outputColorSpace = SRGBColorSpace` with `ACESFilmicToneMapping` and calibrate PMREM environment lighting against them.

## Security Guardrails (OWASP ASI)

- **ASI04 Supply Chain**: Three.js, React Three Fiber, `pmndrs/postprocessing`, and their minor-revision API churn are external dependencies in the render path. Mitigation: pin exact versions in the lockfile and re-run the render tests on every bump.
- **ASI05 RCE Guard**: Draco/Meshopt/KTX2 decoders are WASM binaries; loading them from third-party CDNs executes foreign code in the page. Mitigation: bundle decoders from pinned, verified package sources only and reject runtime decoder URLs from untrusted origins.
- **ASI06 Context & Memory Poisoning**: remotely streamed GLTF scenes and textures are untrusted content entering the renderer. Mitigation: validate scene structure and asset URLs against an allowlist before handing them to loaders; never let embedded GLTF extensions (scripts, cameras) auto-execute.
- **ASI07 Inter-Agent Communication**: rendering slices are consumed by shader and performance roles for further optimization. Mitigation: emit the schema-valid `implementation-result.json` contract so peers can verify compression, instancing, and disposal decisions.
- **ASI09 Human-Agent Trust Exploitation**: do not claim a mobile 60FPS target is met from desktop-only checks. Mitigation: report frame rates only from the actual target-class devices and state untested platforms honestly.

## Related Skills

- **program-game-shaders**: custom GLSL vertex/fragment shaders and post-processing effects
- **profile-game-performance**: WebGL/WebGPU draw call batching and VRAM disposal profiling
- Companion reference: `references/webgpu-threejs-pbr-pipeline.md`
- Companion example: `examples/production-threejs-webgpu-scene.ts`
