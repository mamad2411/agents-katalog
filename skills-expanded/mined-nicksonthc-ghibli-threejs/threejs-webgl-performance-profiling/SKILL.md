---
name: threejs-webgl-performance-profiling
description: Profiles and speeds up a heavy three.js WebGL scene with multi-pass rendering (refraction/reflection pre-passes, GTAO, bloom, shadows, thousands of instances) — honest GPU timing with gl.finish and a default-framebuffer readPixels, per-pass on/off toggles, triangles-per-mesh reports, shader-compile hitch warm-up, one shared shadow render per frame, render layers, distance culling and LOD, no-recompile light fading, program-cache keys, adaptive resolution and GLB compression. Use when the user says the scene is slow, stutters, hitches on first dive/click, fps dropped, asks for a performance pass, frame budget, or "report frame cost per pass".
---

# three.js WebGL performance profiling

A method, not a list of tricks: measure honestly, find the biggest cost, cut it without
visible loss, re-measure in the same session. Stack: three.js `WebGLRenderer` +
`EffectComposer` (vanilla or R3F), often with water pre-passes and post-processing.

## When to use
- "It's slow / janky / hitches", "profile the render passes", "report frame cost per pass".
- A one-off stall the first time something appears (diving, opening, night toggle).
- Before and after adding a heavy feature (foliage, water, fur, simulation).

## Paste-ready prompt
> Profile each render pass of `{{entry file}}` with synchronous timing (`gl.finish()` then a
> 1-pixel `readPixels` of the **default framebuffer**, warm-up render first, median of ~12
> runs) and list triangles per mesh (× instance count, with cast-shadow flag). Toggle each
> pass (AO, bloom, water, shadows, pixel ratio) on/off in alternating cycles. Cut the biggest
> costs without visible loss, then report before and after at the same size in the same session.

## Implementation

### Measure honestly
- **Timing:** run a warm-up render first (it includes shader compiles), then take the
  median of ~12 runs. Sync with `gl.finish()` followed by a `readPixels` of the default
  framebuffer. A `readPixels(RGBA, UNSIGNED_BYTE)` on a **HalfFloat** target is
  `INVALID_OPERATION`, which silently gives you CPU-submit time only.
- **Hitches:** measure with direct `frame()` calls + `gl.finish()`, not
  `requestAnimationFrame` — direct calls work in a hidden tab and give compile cost exactly.
- **fps toggles:** single runs vary ±5 fps. Toggle a feature on/off in alternating cycles
  and compare medians (26 crafted trees cost ~2 fps; a 256² × 225-tap wake simulation showed
  no measurable difference). See `references/profile-passes.mjs`.
- In a hidden/background tab `requestAnimationFrame` stalls: tweens freeze and FPS reads 0.
  Don't mistake that for a bug. An MCP/automation tab must be visible or an rAF-based
  evaluate hangs.
- Re-measure the baseline and the new build **in the same session at the same size**.
- **Other devices:** profile them in headless Chrome before changing anything: CDP
  `Emulation.setCPUThrottlingRate` (4× for a mid phone, 2.5× for a budget laptop),
  `Network.emulateNetworkConditions` (9 Mbps / 150 ms for 4G), a phone viewport, and an init
  script that spoofs `UNMASKED_RENDERER_WEBGL`, `hardwareConcurrency` and `deviceMemory` so
  the tier logic runs as it would there. Record time to ready, bytes by kind, `longtask`
  entries and the program count (`renderer.info.programs.length`). Keep the old build on a
  second port and interleave runs; single runs swing by seconds on a loaded machine.

### Triangles per mesh
Log the top offenders after load (`?stats` flag):
```js
const costs = []
scene.traverse(o => { if (o.isMesh) costs.push({ name:o.name || o.material.name,
  triangles:(o.geometry.index?.count || o.geometry.attributes.position.count)/3*(o.count || 1), shadow:o.castShadow }) })
console.log(JSON.stringify(costs.sort((a, b) => b.triangles - a.triangles).slice(0, 15)))
```
The first bottleneck here was a 5k-triangle blob × 2000 instances. Also watch
`renderer.info.render.calls/triangles` per frame.

### Structural rules
- **One shadow render per frame:** `renderer.shadowMap.autoUpdate = false`; set
  `shadowMap.needsUpdate = true` once per frame before the pre-passes, so refraction,
  reflection and main passes share it.
- **Layers:** keep above-water-only foliage on layer 1 and render the refraction pass with
  layer 0 only. **Enable layer 1 on the shadow camera**, or the leaves stop casting shadows.
  Ground cover (grass, foreground flowers) gets a layer of its own that the mirror camera
  skips below the top tier: in the reflection it is a fringe of blades at the bank edge for
  the cost of the whole meadow again (a phone frame went from 11.8–13M to 7.4M triangles).
- **Variant multipliers:** count `renderer.info.programs.length`. `renderer.clippingPlanes`
  on a planar reflection gives every material a second, clipped program (about half of ~540
  here); clip with an **oblique near plane** on the mirror camera instead (see
  threejs-webgl-realistic-water). One variant, no per-pixel cost.
- **Shadow casters:** thousands of instances must not cast shadows. Only trees inside the
  sun's ±13 m shadow square cast; the square follows the view (snapped).
- **Culling:** bake node transforms, then `computeBoundingSphere()` + a pad (~.35 m for wind
  sway) so frustum culling works on instanced foliage. Add coarse distance culling (every
  0.25 s, radii matched to where fog is ~94 %).
- **LOD:** swap in a sparse index buffer (`sparseGeometry(g, groupSize, stride)` keeps every
  n-th card group) past ~33 m, back under ~27 m (hysteresis), checked every 0.2 s. Choose
  fur shell counts by distance (24/14/6/3/0).
- **Streaming:** build terrain chunks nearest-first, 2 per frame.
- **No recompiles at runtime:** create night/extra lights at build time with intensity 0
  and fade them. Adding a `PointLight` later recompiles every lit material on that frame.
  Prefer one real point light that follows the nearest source over N lights.
- **Program cache:** materials with identical `onBeforeCompile` source share a program. If you
  inject something only one material needs (a leaf-clearing `discard`), add a key such as
  `houseClip:true` to its `customProgramCacheKey`, or the other material gets it too. The
  reverse also holds: per-slot tint *uniforms* on otherwise identical materials keep one program.
- **Avoid extra passes:** swap a transmissive material (cornea, glass) for transparent
  clearcoat physical — transmission adds a whole extra render pass.
- **Quality tiers:** pick `low | medium | high` once, before anything is built, from the
  unmasked GPU string (read on a throwaway context and hand it straight back with
  `WEBGL_lose_context`: phones cap live contexts), `hardwareConcurrency`, `deviceMemory`
  and touch. What worked: software renderers, ≤ 2 cores or ≤ 2 GB → low; phones (coarse
  pointer, short screen side < 600 px) → low; tablets → medium on an Apple GPU with ≥ 4 GB,
  else low; Intel UHD / HD / Iris, Mali, Adreno, PowerVR → low; Ryzen APUs and integrated
  Arc → medium (low at ≤ 4 cores or ≤ 4 GB); Apple, NVIDIA, Radeon RX / Pro, discrete Arc →
  high; unknown → medium. `?quality=` forces one; show tier, GPU and compile time under
  `?debug`. Knobs per tier (high / medium / low): pixel budget 4.2M / 1.4M / 0.78M, DPR cap
  2 / 1.25 / 1, adaptive floor .70 / .55 / .40, AO and SMAA off on low, shadow map
  2048 / 2048 / 1024, grass ×1 / 1 / .55, flowers ×1 / 1 / .85, meadow in the reflection on
  high only, water grid 330 / 330 / 240 segments. Thin only where it doesn't show: the
  flower carpet reads thin below ~.85, grass at .55 doesn't.
- **Pixel budget, not DPR:** `ratio = min(devicePixelRatio, tier DPR, √(budget / (w·h)))`
  × the adaptive scale, so a 4K monitor is bounded too. On the high tier (not touch) never go
  below `min(1, ratio)`: a strong desktop keeps one rendered pixel per CSS pixel.
- **Adaptive resolution:** smooth frame ms (`avg = avg·.9 + ms·.1`; ignore samples while
  loading and frames ≤ 0 or > 1500 ms). Above 28 ms drop the scale ×0.9 after 90 samples and
  10 s since the last change; above 45 ms (under ~22 fps) react fast: ×0.8 after 20 samples
  and 2.5 s — waiting 180 frames at 5 fps is a minute of freeze. Floor = the tier's. Raise
  +.05 below 18 ms, 30 s after the last change; reset on `visibilitychange`.
- **Visitor's choice:** offer Auto / HD / Smooth, remember it (`localStorage`, in try/catch)
  and apply it by reloading with `?quality=` — the tier is read before anything is built.
  HD = the high tier with an 8.3M-pixel budget (up to DPR 2), a 4096 shadow map and adaptive
  scaling off; Smooth = low.
- **GLB weight:** lossless WebP textures, then Draco, in one script run after every export
  (see threejs-blender-glb-pipeline). A textured bridge went 1.97 → 0.16 MB; four heavy
  models went 13.97 → 2.17 MB on Draco alone. Prefer Draco over meshopt when
  shaders read object-space `position`.
- **Start downloads in `<head>`:** import map first (on minified builds), a `modulepreload`
  per module in the graph, and a tiny inline script that `fetch()`es every GLB and JSON (see
  threejs-cinematic-loading-screen); the scene later parses the buffers with
  `GLTFLoader.parseAsync`, and `DRACOLoader.preload()` fetches the decoder alongside. Model
  fetches started at 0.17 s instead of 1.5 s on a phone profile.
- **Lost context:** on `webglcontextlost` call `preventDefault()` (three re-uploads on
  restore; re-render anything rendered once, e.g. the PMREM environment) and offer a reload
  button if it has not come back after ~2.5 s. Catch the renderer constructor and say
  "WebGL 2 is off or missing" on the loading screen instead of a frozen 0 %.

### Shader-compile warm-up
The one-second hitch on the first dive under water was **compilation**, not render cost.
Make the render loop a named `frame()`; during load render one frame from the underwater
view and one from above before the loading screen lifts. Measured with `?nowarm`: first dive
163 ms cold → 10 ms warmed.

Warm-up frames alone compile on the main thread, one program after another (~2.5 s for ~270
programs on an M-series Mac, far longer on Direct3D and phones, loading screen frozen). With
`KHR_parallel_shader_compile`, compile **before** the warm-up instead:
- Call `renderer.compile(group, camera, scene)` in ~6 slices with a `setTimeout(0)` between,
  then poll `program.isReady()` on the new entries of `renderer.info.programs` every 30 ms,
  driving the progress bar. Without the extension skip this; the warm-up compiles as before.
- `compile()` walks the target scene's lights on every call, so one call per object is
  quadratic (0.6 s at 4× CPU). A slice is a fake group over a share of `scene.children`:
  `{ traverse: fn => part.forEach(o => o.traverse(fn)), traverseVisible: () => {} }`. If it
  hands the lights over again, every variant is compiled for twice the lights.
- Bind the half-float target the passes draw into (`setRenderTarget`) before `compile()`:
  programs drawn into a target are linear and untoned, a different variant from the screen.
- Until the scene is built and compiled, `frame()` renders nothing behind the opaque loading
  screen and only streams work in (terrain chunks). Result here: 270 programs in parallel
  before the warm-up plus 59 in it, against 436 one by one; the longest freeze on an
  Android-like profile went 2.3 → 1.0 s.

Without the extension the main thread still blocks for seconds while shaders compile at
load — automation calls time out in that window; wait ~15 s before probing.

## Budgets that worked (upper bounds)
Frame ~20 ms at 2.5K; GTAO ≈ 8 ms at half-res (8 samples, 8 denoise samples); shadow pass
≈ 3.5 ms. Later `gl.finish()` timing put the composer at 8–18 ms and every other pass under
5 ms. Grass: 10 tris × 100k ≈ 1.0M; 163 shrubs ≈ 150k; a 290-culm bamboo grove ≈ 270k (+2 %).

## Pitfalls
- CPU-submit time masquerading as GPU time (HalfFloat `readPixels`, no `gl.finish`).
- Comparing numbers from different sessions, window sizes or a background tab.
- Multiplying light intensities in place every frame (compounding to 1e167) — write absolute values.
- Translucent / additive objects (rays, motes, mist, water sheets) in the GTAO pass cost time
  *and* print as hard sheets; hide them for the AO pass.
- `frame(T)` with `T` below the page clock gives a negative `dt`: fades run backwards (clear
  weather wound up to 40 % rain). Capture at a clock above `performance.now()`.
- jsDelivr's `three.module.min.js` imports `./three.core.js` (unminified): remap that URL to
  `three.core.min.js` in the import map, and put the import map before any `modulepreload`.

## Verify
Report a before/after table: per-pass ms (median), fps median, draw calls, triangles, GLB
MB, first-interaction hitch ms. Screenshot the same views before and after to prove "no
visible loss".

## References
- `references/profile-passes.mjs` — Playwright script: median frame time with passes toggled.
- `references/gpu-timing.js` — in-page synchronous per-pass timer.

## Related skills
threejs-headless-visual-verification · threejs-postprocessing-anime-grade ·
threejs-open-world-streaming · threejs-procedural-vegetation · threejs-blender-glb-pipeline ·
threejs-webgl-realistic-water · threejs-cinematic-loading-screen
