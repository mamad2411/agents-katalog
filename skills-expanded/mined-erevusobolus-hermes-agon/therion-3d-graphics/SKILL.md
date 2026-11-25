---
name: therion-3d-graphics
description: Therion 3D & graphics domain — Three.js, Babylon.js, WebGL, WebGPU, GLSL/HLSL/WGSL shaders, WebXR, physics engines (Rapier, Cannon-es), and 3D visualization.
version: 1.0.0
agents:
  - THERION_3D_WEB_SPECIALIST
  - THERION_SHADER_PROGRAMMER
  - THERION_WEBGPU_ENGINEER
  - THERION_PHYSICS_ENGINEER
  - THERION_WEBXR_SPECIALIST
keywords:
  - three.js
  - babylon.js
  - webgl
  - webgpu
  - glsl
  - hlsl
  - wgsl
  - shader
  - webxr
  - vr
  - ar
  - spatial computing
  - rapier
  - cannon-es
  - physics
  - collision
  - 3d
  - rendering
  - compute shader
  - gpu
  - scene graph
  - mesh
  - material
  - lighting
  - post-processing
  - xr
routing:
  priority: high
  match_on:
    - three.js
    - babylon.js
    - webgl
    - webgpu
    - glsl
    - hlsl
    - wgsl
    - shader
    - vertex shader
    - fragment shader
    - compute shader
    - webxr
    - vr
    - ar
    - augmented reality
    - virtual reality
    - spatial computing
    - xr
    - rapier
    - cannon-es
    - physics engine
    - rigid body
    - collision detection
    - 3d scene
    - 3d rendering
    - mesh
    - material
    - lighting
    - pbr
    - post-processing
    - particle system
    - gpu compute
    - rendering pipeline
    - animation pipeline
    - skeleton animation
    - gltf
    - glb
    - 3d viewer
    - 3d visualization
    - data visualization 3d
    - procedural geometry
    - ray marching
    - screen space
    - deferred rendering
    - forward rendering
---

# Therion 3D & Graphics Domain Skill

## Domain Purpose

Authoritative domain for all 3D graphics and rendering engineering within Therion. Covers the full spectrum of web-based 3D: high-level 3D engines (Three.js, Babylon.js), low-level GPU programming (WebGL, WebGPU), shader authoring (GLSL, HLSL, WGSL), immersive experiences (WebXR — VR & AR), physics simulation (Rapier, Cannon-es), and general 3D visualization for data, products, and games. This skill ensures performant, cross-platform, and visually excellent 3D across Therion projects.

---

## Agent Table

| Agent | Role | Expertise |
|---|---|---|
| `THERION_3D_WEB_SPECIALIST` | **3D Web Engine Architect** | Three.js and Babylon.js architecture, scene graph management, materials & lighting pipelines, PBR workflows, post-processing, glTF/GLB loading optimization, 3D viewer UIs, animation systems (skeletal, morph target, keyframe), particle systems, LOD management, instanced rendering, render-to-texture, model optimization, cross-engine tradeoffs and migration. |
| `THERION_SHADER_PROGRAMMER` | **Shader & Visual FX Engineer** | GLSL (WebGL), HLSL (WebGPU/DirectX), WGSL (WebGPU native), custom vertex/fragment/compute shaders, screen-space effects, ray marching, signed distance fields, procedural generation, post-processing chains (bloom, DOF, SSAO, motion blur), custom material authoring, GPU-based particle simulations, noise & fractal algorithms, color grading and tonemapping, shader performance optimization, cross-API shader porting, spirv reflection. |
| `THERION_WEBGPU_ENGINEER` | **WebGPU & Compute Pipeline Specialist** | WebGPU API architecture, buffers & bind groups, render and compute pipelines, shader modules (WGSL), GPU-optimized data structures, compute shader workloads (particles, physics, image processing, sorting), indirect draw calls, timestamps & queries, cross-adapter compatibility, fallback strategies (WebGL2 polyfill), wgpu-native for desktop, GPU resource management and leak prevention, device/lost recovery, profiling with GPU timing. |
| `THERION_PHYSICS_ENGINEER` | **Physics Simulation Engineer** | Rapier WASM integration (3D & 2D), Cannon-es (ammo.js alternative), rigid body dynamics, collision detection (broadphase + narrowphase), joints & constraints (ball, hinge, fixed, prismatic, spring), raycasting, character controllers, triggers & sensors, continuous collision detection (CCD), sleeping & island management, physics debug rendering, deterministic simulation, WASM compilation & threading, physics-kinematic hybrid setups, WASM memory management. |
| `THERION_WEBXR_SPECIALIST` | **XR / Spatial Computing Specialist** | WebXR Device API, immersive VR (room-scale, seated) and AR (hit-test, plane detection, mesh detection, anchors), XR interaction (controllers, hand tracking, gaze-based), locomotion patterns (teleport, smooth movement, snap turn), XR UI (spatial panels, ray-input, world-space menus), performance profiling for XR (reprojection, foveated rendering, fixed foveated rendering), WebXR layers, depth sensing, pass-through camera, AR lighting estimation, WebXR + Three.js/Babylon.js integration, XR accessibility. |

---

## Domain Principles

1. **Performance is the Constraint** — 3D rendering operates under strict frame budgets (16ms for 60fps, 11ms for 90fps VR). Profile with GPU timers, Spector.js, and browser devtools. Never ship unoptimized draw calls or unbounded GPU memory.

2. **Cross-Platform Always** — Target the widest viable adapter set. WebGPU where available, WebGL2 as fallback, WebGL1 as last resort. Test on all three major GPU vendors (NVIDIA, AMD, Intel) and Apple Silicon.

3. **Shader Portability Matters** — Write WGSL for WebGPU primary; maintain portable GLSL for WebGL fallback. Prefer mathematical equivalence over visual tricks that break across APIs. Use spirv-cross or naga for cross-compilation when practical.

4. **Asset Pipeline Discipline** — All 3D assets go through a pipeline: source → optimization → runtime format. Compress models (Draco, meshopt), resize textures (KTX2/Basis Universal), strip unused data. No raw Blender exports in production.

5. **Physics Must Be Deterministic (Where Needed)** — Use fixed timestep simulation (typically 60Hz or 120Hz). Separate physics ticks from render frames. Use Rapier's deterministic mode for multiplayer or replays. Never build gameplay logic at frame rate.

6. **XR is a First-Class Target** — Every 3D scene should consider an XR mode from the start. XR is not a porting exercise — design for room-scale, standing, and seated from the beginning. Respect XR ergonomics (comfort, nausea prevention, reachability).

7. **Memory is Managed, Not Leaked** — GPU resources (buffers, textures, pipelines, samplers) must be explicitly created and destroyed. No implicit GPU memory management on the web. Track allocations, use `dispose()` patterns, and handle device loss gracefully.

8. **Accessibility in 3D** — 3D applications must be operable without stereoscopic vision or fine motor control. Provide audio cues, text alternatives, non-VR fallback modes, colorblind-friendly palettes, and adjustable movement speeds.

9. **Instrument Everything** — Every renderer includes frame timers, draw-call counters, memory tracking, and shader compile-time logging. A 3D app without diagnostics is unshippable. Use Spector.js, RenderDoc, and browser GPU profiling.

10. **Graceful Degradation** — When WebGPU is unavailable, degrade to WebGL2. When physics WASM fails to load, degrade to a simpler simulation or fallback state. When XR session fails, fall back to desktop 3D. Never crash — always provide a fallback path.

---

## Routing Keywords

The following keywords route queries to this domain skill and its agents:

| Keyword | Routed Agent |
|---|---|
| `three.js`, `babylon.js`, `3d scene`, `scene graph`, `mesh`, `material`, `pbr`, `lighting`, `gltf`, `glb`, `animation`, `skeleton`, `morph target`, `particle`, `lod`, `instanced mesh`, `render texture`, `post-processing stack`, `3d viewer`, `orbit controls`, `camera`, `raycaster` | `THERION_3D_WEB_SPECIALIST` |
| `glsl`, `hlsl`, `wgsl`, `shader`, `vertex shader`, `fragment shader`, `compute shader`, `screen space`, `post-processing`, `bloom`, `ssao`, `dof`, `motion blur`, `ray marching`, `sdf`, `signed distance field`, `procedural`, `noise`, `fractal`, `fragment`, `spirv`, `shader toy`, `tonemapping`, `color grading` | `THERION_SHADER_PROGRAMMER` |
| `webgpu`, `compute pipeline`, `gpu compute`, `wgpu`, `naga`, `bind group`, `buffer management`, `indirect draw`, `gpu particles`, `gpu sorting`, `gpu image processing`, `adapter`, `device`, `surface`, `swap chain`, `wgsl module`, `storage buffer`, `uniform buffer`, `compute shader`, `workgroup` | `THERION_WEBGPU_ENGINEER` |
| `rapier`, `cannon-es`, `physics`, `rigid body`, `collision`, `collider`, `joint`, `constraint`, `raycast`, `character controller`, `trigger`, `sensor`, `ccd`, `sleeping`, `island`, `kinematic`, `deterministic simulation`, `fixed timestep`, `wasm physics`, `broadphase`, `narrowphase` | `THERION_PHYSICS_ENGINEER` |
| `webxr`, `vr`, `ar`, `augmented reality`, `virtual reality`, `spatial computing`, `xr`, `immersive session`, `hit test`, `anchor`, `plane detection`, `mesh detection`, `hand tracking`, `controllers`, `teleport`, `snap turn`, `room scale`, `foveated rendering`, `reprojection`, `depth sensing`, `xr layers`, `xr ui`, `spatial ui`, `ray input`, `pass-through`, `light estimation`, `xr accessibility` | `THERION_WEBXR_SPECIALIST` |

---

## Example Commands

```
# Route to a specific agent via @mention
@THERION_3D_WEB_SPECIALIST set up a Three.js scene with PBR lighting and glTF model loading

@THERION_SHADER_PROGRAMMER write a custom WGSL fragment shader for a toon outline effect

@THERION_WEBGPU_ENGINEER design a compute pipeline that runs 100k particle physics steps per frame

@THERION_PHYSICS_ENGINEER set up Rapier with a character controller and kinematic platform

@THERION_WEBXR_SPECIALIST build an AR experience using plane detection and hit-test anchors in Three.js

# Cross-cutting queries (routes to THERION_3D_WEB_SPECIALIST, may delegate)
What's the best approach — Three.js or Babylon.js — for a data-vis dashboard with 10k animated meshes?
Design a WebGPU-first rendering architecture that falls back cleanly to WebGL2
How should I structure a glTF asset pipeline from Blender to production with Draco compression?
Build a 3D model viewer with orbit controls, glTF loading, and PBR lighting

# Shader-specific cross-cutting
I need a GPU particle system using compute shaders — advice on data layout and workgroup sizing?
Port a GLSL raymarching shader to WGSL — what are the key differences?

# Physics + rendering integration
@THERION_PHYSICS_ENGINEER coordinate with @THERION_3D_WEB_SPECIALIST to wire Rapier rigid bodies to Three.js meshes

# Full XR pipeline
@THERION_WEBXR_SPECIALIST coordinate with @THERION_3D_WEB_SPECIALIST and
@THERION_SHADER_PROGRAMMER to build an immersive VR experience with custom shaders
```
