---
name: webgraphics
description: Expert WebGPU + Three.js (TSL/node materials) guidance for high-performance 3D, shaders, compute, and post-processing on the web. Use when building or reviewing graphics-heavy frontend experiences.
source: https://github.com/JetBrains/skills/tree/main/webgpu-threejs-tsl
---

# Webgraphics

Production-grade WebGPU + Three.js (r170+) practices: WebGPU renderer init with WebGL2 fallback, Three Shader Language (TSL) node materials, compute pipelines, post-processing, and GPU profiling. WebGPU is GA in Chrome/Edge (and shipping behind enable in other browsers); always design for capability detection and device loss.

## Stack Baseline (2026)

| Component | Default | Notes |
| --- | --- | --- |
| Three.js | r170+ | TSL stable; `WebGPURenderer` exported as the recommended path forward. |
| Renderer | `WebGPURenderer` (with WebGL2 fallback) | `await renderer.init()` is now mandatory. |
| Shaders | TSL (Three Shader Language) | Node-based, TS-friendly, compiles to WGSL/GLSL. |
| Postprocessing | `three/addons/postprocessing` (PostProcessing node, `EffectComposer`) | TSL-native effect chains. |
| Compute | TSL `compute()` + `StorageBufferAttribute` / `StorageInstancedBufferAttribute` | GPU-driven simulations, particles. |
| GPGPU | `WebGPURenderer.computeAsync(...)` | Replace WebGL2 GPGPU swap textures. |
| Models | glTF 2.0 + KTX2 + Draco/Meshopt | `GLTFLoader` + `KTX2Loader` (BasisU). |
| Color management | sRGB workflow on by default (Three r152+) | `renderer.outputColorSpace = SRGBColorSpace`. |
| Tooling | Vite 6 + `vite-plugin-glsl` (if you mix GLSL); SPECTOR.js / WebGPU Inspector | Profiling. |

## When to Use

- Setting up Three.js with WebGPU.
- Building shader-driven visuals with TSL.
- Designing compute-driven particles or simulations.
- Composing post-processing pipelines.
- Reviewing GPU limits, fallbacks, performance, or memory pressure.

## Instructions

### 1. Renderer Init: Async, Capability-Checked, With Fallback

```ts
import * as THREE from "three";
import { WebGPURenderer } from "three/webgpu";

async function createRenderer(canvas: HTMLCanvasElement) {
  const supportsWebGPU = !!navigator.gpu;
  const renderer = new WebGPURenderer({
    canvas,
    antialias: true,
    forceWebGL: !supportsWebGPU,                            // graceful WebGL2 fallback
    powerPreference: "high-performance",
  });
  await renderer.init();                                    // REQUIRED for WebGPU

  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(canvas.clientWidth, canvas.clientHeight, false);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.0;

  // Device-loss recovery (WebGPU only)
  const device = (renderer as any).backend?.device as GPUDevice | undefined;
  device?.lost.then(async (info) => {
    console.warn("WebGPU device lost:", info.message, info.reason);
    if (info.reason !== "destroyed") {
      // Tear down + rebuild the renderer
      await rebuildScene(canvas);
    }
  });

  return renderer;
}
```

Always:

- `await renderer.init()` before the first `render()`/`renderAsync()`.
- Check `navigator.gpu` and choose a fallback path you actually tested.
- Handle `device.lost` (driver crash, OS reset, tab backgrounded too long).
- Cap `pixelRatio` at 2 to avoid over-rendering on high-DPI displays.

### 2. Render Loop: `setAnimationLoop` + Async Render

```ts
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);

renderer.setAnimationLoop(async () => {
  controls.update();
  await renderer.renderAsync(scene, camera);                // WebGPU: async submit
});

window.addEventListener("resize", () => {
  const { clientWidth: w, clientHeight: h } = canvas;
  renderer.setSize(w, h, false);
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
});
```

In WebGPU, `renderAsync` returns a promise resolved when the frame is submitted. `setAnimationLoop` integrates with `requestAnimationFrame` and pauses on tab visibility loss.

### 3. TSL Node Materials: Compose Shaders in TypeScript

TSL (Three Shader Language) lets you write shaders as composable node graphs in TS, with type-checked operators, that compile to WGSL or GLSL. Prefer TSL over raw `ShaderMaterial`/WGSL strings for new code.

```ts
import { MeshStandardNodeMaterial } from "three/webgpu";
import {
  uv, time, vec3, mix, sin, normalLocal, positionLocal, Fn,
} from "three/tsl";

const stripes = Fn(([scale, speed]) =>
  sin(uv().y.mul(scale).add(time.mul(speed))).mul(0.5).add(0.5)
);

const material = new MeshStandardNodeMaterial();
material.colorNode = mix(vec3(0.1, 0.2, 0.8), vec3(1, 1, 1), stripes(20, 1.5));
material.emissiveNode = stripes(20, 1.5).mul(0.4);
material.normalNode = normalLocal;                          // example: keep mesh normals
material.roughnessNode = 0.4;
```

Why TSL:

- **Type-safe**: TS catches missing channels, swizzle errors.
- **Reusable**: `Fn(...)` defines a function callable from any material/effect.
- **Cross-backend**: same code works on WebGPU + WebGL2.
- **Fewer materials**: compose features instead of writing variants per use case.

Drop to WGSL/GLSL only when TSL can't express what you need (esoteric ops, third-party shader port). Wrap raw shader code in a function and unit-test the surrounding TS that builds it.

### 4. Geometry, Instancing, and Mesh Discipline

- Use `InstancedMesh` for >100 copies of the same geometry; one draw call.
- Use `BatchedMesh` (Three r155+) for many distinct meshes that share a material - far cheaper than separate `Mesh`es.
- Merge static geometry with `BufferGeometryUtils.mergeGeometries` when objects don't move independently.
- Reuse `BufferGeometry` and `Material` across meshes; never recreate per frame.
- Dispose what you create:

  ```ts
  geometry.dispose();
  material.dispose();
  texture.dispose();
  renderer.dispose();
  ```

  In a React/Vue lifecycle, dispose in `useEffect` cleanup / `onUnmounted`. Three does NOT garbage-collect GPU resources for you.

### 5. Compute Shaders for GPU-Driven Work

GPU compute is where WebGPU shines: particles, fluid sims, boids, image processing.

```ts
import { storage, instanceIndex, Fn, vec3, time } from "three/tsl";
import { StorageInstancedBufferAttribute } from "three/webgpu";

const COUNT = 200_000;

const positionsBuffer = new StorageInstancedBufferAttribute(COUNT, 3);
const velocitiesBuffer = new StorageInstancedBufferAttribute(COUNT, 3);

const positions = storage(positionsBuffer, "vec3", COUNT);
const velocities = storage(velocitiesBuffer, "vec3", COUNT);

const computeUpdate = Fn(() => {
  const p = positions.element(instanceIndex);
  const v = velocities.element(instanceIndex);
  v.addAssign(vec3(0, -0.0098, 0));                         // gravity
  p.addAssign(v);
});

await renderer.computeAsync(computeUpdate().compute(COUNT));
```

Then bind `positions` to a particle material's `positionNode`. The whole simulation runs on the GPU; the CPU only schedules.

Rules:

- Workgroup size matters: TSL picks defaults; for hand-tuned WGSL, profile with WebGPU Inspector.
- Avoid CPU readback (`mapAsync`) on the hot path - it stalls the pipeline. Read back only when you must (e.g., picking).
- Double-buffer state (read from A, write to B) to avoid race conditions if you read your own writes within a pass.

### 6. Post-Processing with Node Effects

```ts
import { PostProcessing } from "three/webgpu";
import { pass, mrt, output, emissive } from "three/tsl";
import { bloom } from "three/addons/tsl/display/BloomNode.js";

const post = new PostProcessing(renderer);
const scenePass = pass(scene, camera).setMRT(mrt({ output, emissive }));
const colorPass = scenePass.getTextureNode("output");
const emissivePass = scenePass.getTextureNode("emissive");

post.outputNode = colorPass.add(bloom(emissivePass, 1.0, 0.5));
post.renderAsync();                                         // replaces renderer.renderAsync
```

Cheap effects (bloom, tone map, vignette) are usually fine; expensive ones (SSAO, SSR, TAA) need budget. Always measure frame time with effects on vs off.

### 7. Textures and Models

- **KTX2 (BasisU)** compressed textures are the default for shipped assets. 4-6x smaller, GPU-native.
  ```ts
  const ktx2 = new KTX2Loader().setTranscoderPath("/basis/").detectSupport(renderer);
  ```
- **Draco** or **Meshopt** for geometry compression in glTF.
- Generate mipmaps for repeating textures (`texture.generateMipmaps = true`).
- Set `colorSpace`: `SRGBColorSpace` for color textures, `NoColorSpace` for normal/roughness/data.
- Pre-warm shaders: call `renderer.compileAsync(scene, camera)` before the first frame to avoid a hitch.

### 8. Performance Budget and Profiling

Targets (mid-range laptop GPU, 1080p):

- 60 FPS sustained -> 16.6ms frame budget; aim for <8ms GPU + <4ms CPU.
- Mobile-first scenes: 30 FPS budget = 33ms; cap effects accordingly.

Tools:

- **`renderer.info`** (`render.calls`, `render.triangles`, `memory.geometries`).
- **WebGPU Inspector** (Chrome extension) for pipeline + shader inspection.
- **SPECTOR.js** for WebGL fallback debugging.
- **Performance API** (`performance.now()`) for CPU timings.
- **`renderer.resolveTimestampsAsync()`** for GPU timings (where supported).

Common wins:

- Cull off-screen objects (`Frustum`, `OcclusionQuery` if available).
- LOD with `THREE.LOD` (or distance-based mesh swaps).
- Lower shadow map resolution + tight `shadow.camera` frustum.
- Bake static lighting where possible.
- Avoid per-frame allocations in the render loop.

### 9. Resize, DPR, and Color Handling

```ts
const dpr = Math.min(window.devicePixelRatio, 2);
renderer.setPixelRatio(dpr);
```

- High DPR multiplies fragment cost by `dpr^2`. Cap aggressively for fullscreen scenes.
- Use a `ResizeObserver` on the canvas instead of `window.resize` for embedded canvases.
- Tone mapping (`ACESFilmicToneMapping`, `AgXToneMapping`) is required for HDR-style PBR; otherwise colors will look washed out.

### 10. Accessibility and Inclusive Design

- Provide a non-WebGL fallback (image, video, captions).
- Honor `prefers-reduced-motion` - reduce camera shake, particle counts, autoplay animations.
- Provide keyboard controls in addition to pointer/touch.
- Color-blind safe palettes; avoid encoding info in color alone.
- Avoid flashing >3Hz (epilepsy risk).

### 11. React/Vue Integration

- React: use **react-three-fiber** (`@react-three/fiber`) + **drei** for declarative scenes; integrates well with R3F's WebGPU branch.
- Vue: **TresJS** (`@tresjs/core`) for declarative Vue 3 scenes.
- In both, dispose resources on unmount and avoid recreating geometries/materials inside render functions.

## Common Pitfalls

| Anti-pattern | Why it hurts | Fix |
| --- | --- | --- |
| Skipping `await renderer.init()` | First `renderAsync` throws | Always await before first frame |
| No fallback when `navigator.gpu` is undefined | App crashes on Safari/older browsers | `forceWebGL: true` fallback or feature-gated UI |
| No `device.lost` handler | Permanent black canvas on driver crash | Listen + rebuild scene |
| Recreating geometry/material every frame | GPU upload churn, GC pressure | Build once, reuse |
| Forgetting `dispose()` | GPU memory leak across SPA route changes | Dispose in cleanup |
| Raw WGSL/GLSL strings copied across materials | Drift, no type safety | TSL functions composed once |
| `setPixelRatio(window.devicePixelRatio)` unbounded | 4x render cost on retina/4K | Cap at 2 |
| Reading buffers back to CPU each frame | Stalls pipeline | Stay GPU-side; readback only on demand |
| Loading PNG/JPG textures uncompressed | Big downloads, slow upload, more VRAM | KTX2 + BasisU |
| `colorSpace` defaults wrong on data textures | Wrong normals/roughness | `NoColorSpace` for data |
| One material per object | Many shader compiles, draw calls | Share materials, instance meshes |
| Heavy postprocessing without measurement | Frame drops | Profile with/without each pass |
| Ignoring `prefers-reduced-motion` | A11y violation, motion sickness | Branch on the media query |

## Output Format

When applying this skill, deliver:

1. Renderer init plan (WebGPU + fallback + device-loss handling).
2. Asset pipeline decisions (KTX2, Draco/Meshopt, glTF).
3. Material/shader plan (TSL nodes, shared functions).
4. Compute/simulation design with buffer layout.
5. Post-processing chain with cost estimate per pass.
6. Performance budget + profiling checkpoints.
7. Lifecycle/dispose plan for SPA integration.
8. A11y notes (reduced motion, keyboard, fallback).

## Authoritative References

- Three.js manual: https://threejs.org/manual/
- Three.js WebGPU docs: https://threejs.org/docs/#manual/en/introduction/How-to-use-WebGPU
- TSL (Three Shader Language) wiki: https://github.com/mrdoob/three.js/wiki/Three.js-Shading-Language
- Three.js examples (TSL + WebGPU): https://threejs.org/examples/?q=webgpu
- WebGPU spec: https://www.w3.org/TR/webgpu/
- WGSL spec: https://www.w3.org/TR/WGSL/
- WebGPU Samples: https://webgpu.github.io/webgpu-samples/
- WebGPU Inspector (DevTools): https://github.com/brendan-duncan/webgpu_inspector
- KTX2 / BasisU: https://github.khronos.org/KTX-Specification/
- glTF 2.0: https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html
- react-three-fiber: https://r3f.docs.pmnd.rs/
- TresJS: https://tresjs.org/
- web.dev WebGPU intro: https://developer.chrome.com/docs/web-platform/webgpu/
- MDN WebGPU API: https://developer.mozilla.org/en-US/docs/Web/API/WebGPU_API