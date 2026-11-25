---
name: a-frame-optimization
description: Optimize A-Frame and WebXR scene performance including draw call reduction, asset management, scripting efficiency, and scene culling strategies. Use this skill whenever the user mentions A-Frame, WebXR, VR scene performance, frame rate drops, draw calls, Three.js tick handlers, or asks how to make an A-Frame project faster, smoother, or more efficient — even if they don't use the word "optimize".
---

# A-Frame Performance Optimization

A-Frame sits on top of Three.js and runs in the browser, so performance work spans two layers: the A-Frame component system (DOM-based, high-level) and the underlying Three.js renderer (low-level, real-time). High-frequency operations must often bypass A-Frame's DOM to avoid string-parsing overhead. Focus on reducing draw calls first — they are almost always the primary bottleneck in WebXR.

## Monitor Before You Optimize

Add the `stats` component to `<a-scene>` to get a real-time HUD showing FPS, draw calls, geometries, and vertex counts:

```html
<a-scene stats>
  <!-- your scene -->
</a-scene>
```

Always measure before changing anything. Draw call count and frame time tell you where to focus.

## 1. Reduce Draw Calls

Every unique mesh + material combination typically costs one draw call. Target **under 300** for general web; high-end VR headsets may sustain 500–1,000.

### Merge Static Geometries

Combine meshes that share the same material and never move into a single draw call using a geometry merger:

```html
<script src="https://unpkg.com/aframe-geometry-merger-component/dist/aframe-geometry-merger-component.min.js"></script>

<a-entity geometry-merger="preserveOriginal: false">
  <a-box color="red"></a-box>
  <a-box position="1 0 0" color="red"></a-box>
</a-entity>
```

### Use GPU Instancing for Repeated Objects

For scenes with many identical objects (trees, grass, crowd members), instancing renders all copies in one draw call:

```html
<script src="https://unpkg.com/aframe-instanced-mesh/dist/aframe-instanced-mesh.min.js"></script>

<a-entity instanced-mesh="asset: #tree-gltf; count: 500"></a-entity>
```

### Atlas Textures

Combine multiple small textures into a single atlas image so all objects sharing parts of that image use one material — and one draw call — instead of many.

## 2. Manage Assets Efficiently

Asset quality directly affects GPU memory, load time, and render cost.

**Texture dimensions** — Keep all textures at power-of-two resolutions (256, 512, 1024, 2048…). Non-POT textures force the GPU to resize at runtime and cannot be mipmapped correctly.

**Bake lighting** — Avoid real-time dynamic lights and shadow maps. Pre-bake lighting and shadows into textures in Blender or a similar tool. A single baked texture replaces multiple real-time light calculations per fragment.

**Simplify materials** — Use `MeshBasicMaterial` or `MeshLambertMaterial` for objects that don't need physically-based rendering. The default `MeshStandardMaterial` (PBR) runs significantly more expensive shaders per pixel:

```javascript
// In an A-Frame component, access the Three.js mesh directly
const mesh = el.getObject3D('mesh');
if (mesh) {
  mesh.material = new THREE.MeshBasicMaterial({ map: mesh.material.map });
}
```

## 3. Optimize Components and Scripting

### Bypass `.setAttribute()` in Tick Handlers

`setAttribute()` triggers A-Frame's full attribute pipeline — string parsing, schema validation, and DOM updates — every call. For values updated every frame (position, rotation), go directly to Three.js:

```javascript
// ❌ Slow — parses strings every frame
el.setAttribute('position', { x: 1, y: 0, z: 0 });

// ✅ Fast — direct Three.js object mutation
el.object3D.position.set(1, 0, 0);
el.object3D.rotation.y += 0.01;
```

### Throttle Tick Handlers

Most logic doesn't need to run at 90 fps. Use `AFRAME.utils.throttleTick` to cap execution rate:

```javascript
AFRAME.registerComponent('my-component', {
  tick: AFRAME.utils.throttleTick(function (time, delta) {
    // Runs at most every 100ms (~10 fps) instead of every frame
    this.updateLogic();
  }, 100)
});
```

### Pool Frequently Spawned Entities

Creating and destroying entities (projectiles, particles, pickups) generates garbage that causes GC pauses. Pre-allocate a pool and reuse instances:

```html
<a-entity pool="mixin: bullet; size: 20"></a-entity>
```

```javascript
// Acquire from pool instead of creating
const bullet = document.querySelector('[pool]').components.pool.requestEntity();
bullet.setAttribute('visible', true);

// Return to pool when done
document.querySelector('[pool]').components.pool.returnEntity(bullet);
```

## 4. Scene Structure and Culling

**Replace `<a-sky>` with `background`** — `<a-sky>` creates a large sphere geometry that costs draw calls and vertex processing. For solid or gradient backgrounds, use the `background` component instead:

```html
<!-- ❌ Unnecessary geometry -->
<a-sky color="#87CEEB"></a-sky>

<!-- ✅ Zero geometry cost -->
<a-scene background="color: #87CEEB">
```

**Limit raycaster scope** — By default, raycasters test against every object in the scene. Restrict them to a specific class:

```html
<a-entity raycaster="objects: .interactive" cursor></a-entity>

<!-- Only objects with class="interactive" are ray-tested -->
<a-box class="interactive" position="0 1.5 -3"></a-box>
```

**Enable frustum culling on large models** — A single large GLTF (an entire building, a city block) cannot be culled as a unit; the whole thing renders even when mostly off-screen. Break large assets into smaller logical pieces so the renderer can skip the ones outside the camera frustum.

## Quick Reference

| Problem | Solution |
|---|---|
| Too many draw calls | Geometry merger, instancing, texture atlasing |
| Shader cost too high | Switch to `MeshBasicMaterial` / bake lighting |
| Tick handler CPU spike | `throttleTick`, bypass `setAttribute` |
| GC stutters | Object pooling |
| Sky is wasteful | Replace `<a-sky>` with `background` component |
| Raycaster lag | Scope to `.interactive` class |
| Large model not culling | Split into smaller mesh pieces |

## Related Skills

- **threejs-3d-webgpu** — Understanding Three.js internals and WebGPU rendering pipelines helps you make lower-level optimization decisions and take advantage of cutting-edge GPU features.
- **physics** — Physics engines (Cannon.js, Ammo.js) can be expensive; knowing physics principles helps you choose lightweight approximations or pre-computed solutions.
- **trigonometry** — Essential for camera culling, frustum calculations, and determining when objects are truly visible before rendering.
- **geometry** — Mesh simplification, LOD strategies, and spatial partitioning rely on geometric reasoning to reduce polygon counts and draw calls.
- **linear-algebra** — Matrix transformations, camera projection math, and instancing all depend on solid linear algebra foundations.
- **web-visual-effects** — Optimized post-processing, bloom, glow, and other effects must be composited efficiently to avoid expensive full-screen passes.
- **svg-graphics** — For 2D UI overlays in VR/XR, SVG-to-canvas or DOM-to-WebGL techniques can be more performant than 3D text or complex meshes.

**When to use this skill vs related skills:**
- Use **threejs-3d-webgpu** when you need to understand the underlying rendering pipeline or want to implement custom shaders and GPU techniques.
- Use **physics** when optimizing physics simulations or when you need to replace real-time physics with baked animations or simpler approximations.
- Use **trigonometry** when optimizing culling, camera angles, or any spatial calculations that can reduce unnecessary rendering.
- Use **geometry** when you need to simplify meshes, implement LOD, or apply spatial partitioning to reduce draw calls.
- Use **linear-algebra** when working with transformations, instancing, or any math that can be offloaded to the GPU for better performance.
- Use **web-visual-effects** when optimizing post-processing effects or screen-space shaders that can be costly if not implemented efficiently.
- Use **svg-graphics** when you need to render 2D UI elements in VR/XR without the overhead of 3D meshes or when you can leverage the efficiency of SVG rendering for HUDs and overlays.  
