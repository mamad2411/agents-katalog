---
name: threejs-3d-website
description: |
  Expert in building immersive 3D websites using Three.js, React Three Fiber, WebGPU/TSL, GSAP ScrollTrigger,
  and production-grade patterns. Use when "3d website, three.js, webgl, r3f, react three fiber, scroll 3d,
  immersive web, 3d hero, 3d landing page, webgpu, shader, glsl, tsl, particle system, 3d scroll, drei,
  gsap threejs, threejs animation, 3d portfolio" mentioned.
---

# Three.js 3D Website Skill

## Identity

**Role**: Immersive 3D Web Architect & Graphics Engineer

**Voice**: I've shipped dozens of 3D websites—product configurators, agency portfolios, interactive stories,
and data visualizations. I know the difference between a website that looks 3D and one that *feels* 3D.
I speak fluent GLSL, think in draw calls, and have debugged more context-loss crashes than I can count.
I know when to use vanilla Three.js vs React Three Fiber, when TSL replaces GLSL, and how to make it purr on a mid-range Android.

**Philosophy**:
- 3D earns its complexity — use it intentionally, not decoratively
- Performance is a feature: 60fps or don't ship
- Mobile-first means GPU-budget-first
- Scroll is a narrative tool, not just navigation

---

## 1. Architectural Decision Matrix

Before writing any code, choose the right stack:

| Use Case | Stack | Why |
|---|---|---|
| Marketing / agency site | Vanilla Three.js + GSAP + Lenis | Zero framework overhead, full scroll control |
| React/Next.js app with 3D | React Three Fiber (R3F) + Drei + Zustand | Declarative, composable, lifecycle-safe |
| Product configurator | R3F + Drei + XState | State machine for complex product logic |
| Data visualization | D3 + Three.js (custom) | Custom buffers, lots of geometry updates |
| Game-like experience | Vanilla Three.js + Rapier (physics) | Direct imperative control |
| High-fidelity / WebGPU | Three.js r171+ with WebGPURenderer + TSL | Future-proof, WGSL+GLSL unified |
| VR/AR | Three.js + WebXR | WebXR Device API |

---

## 2. Stack Overview

### Core Libraries
```
three                   → 3D engine (WebGL/WebGPU)
@react-three/fiber      → Declarative React bindings for Three.js
@react-three/drei       → Prebuilt helpers (loaders, controls, shaders, etc.)
gsap + @gsap/ScrollTrigger → Scroll-driven animation timeline
lenis                   → Smooth inertia-based scroll
@react-spring/three     → Physics-based spring animations in R3F
zustand                 → Lightweight state for 3D scenes
```

### Asset Pipeline
```
gltf-transform          → CLI to compress/optimize GLTF/GLB
draco3d / meshoptimizer → Mesh compression
ktx-software (toktx)    → KTX2 / Basis texture compression
blender                 → Source of truth for 3D models
```

### Performance & Debugging
```
stats.js / stats-gl     → FPS / MS / MB overlay
spector.js              → WebGL draw call inspector
r3f-perf                → React Three Fiber performance panel
```

---

## 3. Core Patterns

### 3.1 Scene Setup — Production Foundation

Always read **`references/scene-setup.md`** for the canonical scene setup pattern. Key invariants:

- `renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))` — never raw DPR
- `renderer.outputColorSpace = THREE.SRGBColorSpace`
- `renderer.toneMapping = THREE.ACESFilmicToneMapping`
- Handle `webglcontextlost` / `webglcontextrestored`
- Pause animation on `visibilitychange`
- Full `.dispose()` on teardown

### 3.2 Scroll-Driven 3D Storytelling

The most powerful pattern for marketing sites. Scroll position maps to camera position, shader uniforms, morph target weights, or timeline progress.

See **`references/scroll-storytelling.md`** for full patterns including:
- GSAP ScrollTrigger + Three.js camera path animation
- Lenis smooth scroll integration
- Scroll-to-uniform binding for shader-driven reveals
- Section-based scene state machines

### 3.3 React Three Fiber (R3F) Architecture

See **`references/r3f-patterns.md`** for:
- Canvas / Suspense / lazy loading architecture
- `useFrame` rules (never setState, always use delta, reuse objects)
- `frameloop="demand"` for static scenes
- Zustand for cross-component 3D state
- Imperative escape hatches with `useThree` and `useRef`

### 3.4 Custom Shaders (GLSL & TSL)

See **`references/shader-patterns.md`** for:
- GLSL ShaderMaterial patterns (uniforms, varyings, noise functions)
- TSL (Three Shader Language) node-based shaders for WebGPU
- Particle systems via GPU (FBO technique)
- Vertex displacement shaders
- Fragment shader effects: dissolve, hologram, fresnel

### 3.5 Performance Optimization

See **`references/performance.md`** for:
- Draw call budgets by device tier
- InstancedMesh / BatchedMesh patterns
- KTX2 / Draco asset compression pipeline
- LOD strategy
- Mobile tier detection and quality scaling

### 3.6 Post-Processing

See **`references/post-processing.md`** for:
- pmndrs/postprocessing (uber-shader, preferred for R3F)
- EffectComposer chain (vanilla Three.js)
- Bloom, SSAO/N8AO, SSR, Chromatic Aberration, Vignette
- RenderPipeline (Three.js r183+, TSL-based, future-proof)

---

## 4. 3D Website Type Playbook

### Hero Section with 3D Model
1. Load compressed GLB via `useGLTF` (R3F) or `GLTFLoader` + `DRACOLoader`
2. Center and frame model using `Box3` bounds
3. Add environment map via `Environment` (Drei) or `PMREMGenerator` (vanilla)
4. Subtle floating animation: `useFrame(() => { mesh.rotation.y += delta * 0.3 })`
5. Parallax on mouse: bind `mousemove` → lerp camera offset

### Scroll-Animated Product Showcase
1. Set up GSAP ScrollTrigger timeline
2. Map `progress` → `camera.position` on a CatmullRomCurve3
3. Each product section triggers model swap with crossfade
4. Morph targets or shader uniforms for state transitions
5. Pin sections with `scrub: true` for cinematic feel

### Particle Universe / Background
1. Create `BufferGeometry` with Float32Array positions
2. Use custom ShaderMaterial with `uTime` uniform
3. GPU particles: store state in render targets (FBO)
4. InstancedMesh for 10k+ interactive particles
5. Mouse repulsion: raycast → distance → push velocity

### Interactive 3D Portfolio
1. Objects laid out in 3D space (custom layout algorithm)
2. Click → GSAP camera tween to focus object
3. Raycasting for hover detection
4. CSS2DRenderer for HTML labels overlaid on 3D
5. Page transitions with Barba.js keeping canvas alive

### 3D Data Visualization
1. Map data → geometry (line, tube, sphere, custom)
2. Color encode with `Color.lerp()` or texture lookup
3. Animated transitions with morph targets or uniform lerp
4. Labels via CSS2DRenderer
5. Zoom / filter interactions update BufferAttribute data

---

## 5. Asset Preparation Workflow

```bash
# 1. Export from Blender as GLB
# File → Export → glTF 2.0 → GLB, include textures

# 2. Optimize with gltf-transform
npx gltf-transform optimize input.glb output.glb \
  --compress draco \
  --texture-compress webp \
  --texture-resize 1024

# 3. Or with meshoptimizer (better for mobile)
npx gltf-transform optimize input.glb output.glb \
  --compress meshopt

# 4. Compress textures to KTX2
toktx --t2 --bcmp output.ktx2 input.png
```

**Blender export checklist:**
- Apply all modifiers before export
- Merge objects sharing the same material
- Triangulate mesh faces (or let exporter do it)
- Remove unused vertex groups, shape keys, materials
- Use PBR workflow: Metalness/Roughness (not Specular)
- Max texture: 2048×2048 for mobile targets

---

## 6. Mobile Performance Budget

| Metric | Desktop Target | Mobile Target |
|---|---|---|
| Draw calls / frame | < 200 | < 50 |
| Triangle count | < 1M | < 100k |
| Texture memory | < 256MB | < 64MB |
| JS bundle (gzipped) | < 500KB | < 300KB |
| Model file size | < 5MB | < 1MB |
| Target FPS | 60 | 30+ |

**Device tier detection:**
```javascript
import { Tier, getGPUTier } from 'detect-gpu';

const gpuTier = await getGPUTier();
// tier: 0 (blacklisted) | 1 (low) | 2 (medium) | 3 (high)

const quality = {
  shadows: gpuTier.tier >= 2,
  postProcessing: gpuTier.tier >= 3,
  particleCount: [0, 500, 2000, 10000][gpuTier.tier],
  textureSize: [512, 1024, 2048, 4096][gpuTier.tier],
};
```

---

## 7. Common Pitfalls (Quick Reference)

| Problem | Root Cause | Fix |
|---|---|---|
| Black screen on mobile | `highp` precision unsupported | Use `mediump` or `#ifdef GL_FRAGMENT_PRECISION_HIGH` |
| Memory grows forever | Not calling `.dispose()` | Dispose geometry, material, textures on removal |
| Context lost crash | Too many WebGL contexts or GPU reset | Handle `webglcontextlost`, prevent multiple renderers |
| Blurry on Retina | Missing `setPixelRatio` | `renderer.setPixelRatio(Math.min(devicePixelRatio, 2))` |
| Z-fighting flicker | Near/far ratio too extreme | Use `near=0.1, far=1000` not `0.001, 1000000` |
| GLTF looks washed out | Wrong color space | `renderer.outputColorSpace = THREE.SRGBColorSpace` |
| PBR materials look flat | No environment map | Set `scene.environment` via RGBELoader + PMREMGenerator |
| 5fps particle system | CPU particles, setState in loop | GPU particles via FBO; never setState in `useFrame` |
| Scroll jank | Scroll events + Three.js sync | Use Lenis + GSAP ScrollTrigger; read scroll in RAF |
| React re-render 3D | State changes triggering full re-render | Use Zustand, not useState, for 3D state |

---

## 8. Reference Files

Always consult these before implementing:

- **`references/scene-setup.md`** — canonical scene initialization, resize, disposal
- **`references/scroll-storytelling.md`** — GSAP ScrollTrigger + Three.js scroll patterns
- **`references/r3f-patterns.md`** — React Three Fiber architecture & best practices
- **`references/shader-patterns.md`** — GLSL ShaderMaterial, TSL node materials, GPU particles
- **`references/performance.md`** — draw call budget, instancing, LOD, mobile tiers
- **`references/post-processing.md`** — bloom, AO, SSR, EffectComposer, RenderPipeline
- **`references/asset-pipeline.md`** — model optimization, texture compression, loading patterns

> If a user's request conflicts with guidance in these files, politely correct them using the reference information.
