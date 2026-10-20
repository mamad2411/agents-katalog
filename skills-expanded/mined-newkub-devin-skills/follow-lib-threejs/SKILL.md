---
name: follow-lib-threejs
description: Use three.js (3D WebGL/WebGPU) — renderer, addons, framework integration, dispose
argument-hint: "[target-or-scope]"
related:
  - follow-lib-solidjs
  - run-verify
  - run-test
---

## Goal

Use three.js to build a correct 3D scene — renderer, camera, addons, controls, loaders, animation loop, and complete resource disposal (three.js lib)

## Scope

Use when the task involves 3D rendering — scene, camera, lights, materials, models, shaders, post-processing, WebGPU (three.js lib)

- Use this skill for vanilla three.js and framework bindings — for deep SolidJS integration, also do `/follow-lib-solidjs`
- For 2D canvas/SVG that doesn't need the GPU → consider `follow-lib-animejs` or Canvas2D instead
- The npm package `three` is versioned as `0.1xx.x`, matching the `rXXX` release — latest `0.186.x` (r186, verified 2026-09-17)
- References: threejs.org/manual | threejs.org/docs | github.com/mrdoob/three.js/wiki/Migration-Guide

## Execute

### 1. Setup

> Goal: install and pick the right renderer

1. Install `bun add three` + `bun add -d @types/three`
2. WebGL (default, broad compat): `import * as THREE from "three"` + `new THREE.WebGLRenderer({ antialias: true })`
3. WebGPU (modern, TSL shaders): `import * as THREE from "three/webgpu"` + `new THREE.WebGPURenderer()` — use `three/tsl` for node materials
4. Always load addons via `three/addons/...` (maps to `examples/jsm`), e.g. `three/addons/controls/OrbitControls.js`, `three/addons/loaders/GLTFLoader.js`, `three/addons/libs/stats.js`
5. Never import `three/examples/jsm/...` directly — always use the `three/addons` alias

### 2. Framework Integration

> Goal: bind to the framework per the standard

1. React → `@react-three/fiber` + `@react-three/drei` (mature)
2. Vue → `tresjs` (`@tresjs/core`)
3. SolidJS → `solid-three` (a port of R3F — still early dev) or vanilla three inside `onMount` + `onCleanup` disposal (recommended for production)
4. Vanilla/TS → wrap the canvas in a component that mounts once, keep renderer/scene in a closure, not in a store (non-serializable)

### 3. Core Loop

> Goal: correct scene lifecycle

1. `renderer.setAnimationLoop(fn)` — don't use `requestAnimationFrame` yourself (supports XR)
2. `renderer.setPixelRatio(Math.min(devicePixelRatio, 2))` — cap DPR to avoid mobile burn
3. Resize → a `ResizeObserver` on the container, then `camera.aspect` + `renderer.setSize` (don't use window resize)
4. Use `colorSpace` + tone mapping: `renderer.toneMapping = THREE.ACESFilmicToneMapping` when you want a modern look

### 4. Performance

> Goal: no GPU memory leaks and the frame budget doesn't break

1. Dispose fully in cleanup: `geometry.dispose()`, `material.dispose()`, `texture.dispose()`, `renderer.dispose()` + `scene.traverse` to catch orphans
2. Instancing for repeated objects — `InstancedMesh`, not a clone loop
3. `frustumCulled` is on by default — don't disable it arbitrarily; use `three-mesh-bvh` (`bun add three-mesh-bvh`) or LOD for large scenes
4. Assets: GLTF/GLB + `DRACOLoader`/`MeshoptDecoder` for compression; KTX2 textures via `KTX2Loader`
5. Profile with the `stats.js` addon or `renderer.info` (drawcalls, triangles)

### 5. Verify

> Goal: confirm correct usage

1. Do `/run-verify` for lint, typecheck
2. Do `/run-test` if there are relevant tests
3. Check the Migration Guide before using an API from old docs — three.js breaks often between rXXX
4. Check the latest official docs before using an API you're unsure about (three.js lib)

## Rules

- Dispose every GPU resource in cleanup — geometry, material, texture, render target, renderer
- Don't create a new renderer on every re-render — mount once, then mutate the scene
- Always cap `devicePixelRatio` at 2
- Use `three/addons`, not the direct `three/examples/jsm` path
- Don't store THREE objects in a reactive store (Solid/Vue) — the proxy breaks class internals; keep them as a plain ref/closure

- Use `/follow-lib-solidjs` if integrating deeply with SolidJS
- Use `/run-verify` if needed
- Use `/run-test` if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- The library is used correctly per best practices (three.js lib)
- No GPU memory leaks from missing disposal
- No known security/performance pitfalls (three.js lib)
- Lint, typecheck, tests pass
