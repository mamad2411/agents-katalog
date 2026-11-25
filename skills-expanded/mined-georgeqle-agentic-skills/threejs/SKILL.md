---
name: threejs
description: Three.js/R3F animation guardrails — useFrame loop, tween libraries, shader-based animation, render-loop timing
type: planning
version: v0.0
invocation: sub-skill
parent: animation-design-planner
---

# Three.js / R3F Implementation Guardrails

Invoke as `$animation-design-planner frameworks/threejs`.

This subskill provides Three.js and React Three Fiber animation guardrails for step 5 of `$animation-design-planner`. It is invoked automatically when the parent detects `three`, `@react-three/fiber`, or R3F in the project. All baseline guardrails from the parent (transform/opacity preference, reduced-motion, focus/pointer/scroll/z-index rules) still apply.

## Guardrails

### Render loop and useFrame

- All animation must run inside the render loop. Never use `setInterval`, `setTimeout`, or manual `requestAnimationFrame` with R3F.
- `useFrame((state, delta) => ...)` — multiply all increments by `delta` for frame-rate independence.
- Use `state.clock.elapsedTime` for oscillations (sin/cos), `delta` for velocity-based movement.
- The `priority` parameter orders multiple `useFrame` hooks — document any non-zero values and the reason.
- Plain Three.js: use `renderer.setAnimationLoop(callback)` with `Clock.getDelta()`.
- Never mutate React state inside `useFrame` — mutate refs directly to avoid re-renders every frame.

### Tween library integration

- Simple A→B interpolation: `maath/easing` (`damp`, `damp3`, `dampE`) inside `useFrame` — always pass `delta`.
- Complex multi-step sequences: GSAP `.to()` targeting ref properties is acceptable for visual-only props, not for state-dependent logic.
- Avoid tween.js with R3F — it requires a manual `TWEEN.update()` call inside the render loop.
- Physics-driven animation: use `@react-three/rapier` or `cannon-es` instead of easing curves for physically plausible motion.

### Disposal and cleanup

- Geometries, materials, and textures created outside the scene graph need manual `.dispose()` in `useEffect` cleanup.
- Particle systems with dynamic geometry: track instances in a ref array and dispose on despawn or unmount.
- Swapping materials: dispose the old material before replacing — property assignment does not auto-dispose.
- `useLoader` / `useGLTF` cache by URL (safe for reuse), but `.clone()`'d materials are your responsibility to dispose.
- InstancedMesh: geometry and material are shared — dispose once on full unmount, not per instance.

### Frame budget

- 16.6ms at 60fps for all JS + animation + GPU work. Every millisecond counts.
- Profile with R3F `<Perf>` or Stats.js. Plan fallback strategies: reduce particle count, lower LOD, disable shadows.
- Use `state.performance.current` (from `@react-three/drei`'s `AdaptiveDpr`/`AdaptiveEvents`) for adaptive quality.
- Frame-skip pattern for periodic updates (UI labels, health bars): run expensive logic every N frames using a counter, not every frame.
- Never allocate objects inside `useFrame` — pre-allocate `Vector3`, `Quaternion`, and `Matrix4` in refs outside the loop.

### Proof expectations

- Sustained target framerate verified via `<Perf>` overlay or Stats.js.
- Delta-time independence: animation speed is consistent at 30fps (throttled DevTools) and 60/144fps.
- After unmount: `renderer.info.memory.geometries` and `.textures` return to pre-mount counts.
- Disposed objects produce no visible artifact (no white/pink squares, no console warnings).
- Interrupted tweens on unmount do not throw or attempt to update disposed objects.
