---
name: godot-performance
description: Find and fix performance problems in Godot 4.7 - profilers and monitors, frame budgets, MultiMesh and server APIs for thousands of objects, WorkerThreadPool and thread groups, GDScript/C# hot paths, draw calls, lights, LOD, physics cost, loading and memory leaks. Use when the game stutters, FPS is low, loading is slow or memory grows.
license: MIT
compatibility: Godot 4.7+ (GDScript and C#).
metadata:
  author: godot-agent-skills
  version: "1.1.0"
---

# Performance (4.7)

**Measure first.** Never optimize blind. A budget of 16.6 ms per frame (60 FPS) or 8.3 ms (120 FPS) covers script, physics, rendering on the CPU and GPU.

## Tools
- Editor Debugger: **Profiler** (script functions; start it, play, then sort by self time), **Visual Profiler** (CPU vs GPU per render pass), **Monitors** (FPS, process/physics time, objects, nodes, **orphan nodes**, draw calls, video memory), Network Profiler, and **ObjectDB snapshots** (4.6+: diff two snapshots to find leaks).
- Code: `Performance.get_monitor(Performance.TIME_PROCESS)`, `RENDER_TOTAL_DRAW_CALLS_IN_FRAME`, `OBJECT_NODE_COUNT`, `OBJECT_ORPHAN_NODE_COUNT`. Add your own with `Performance.add_custom_monitor(&"game/enemies", callable)`.
- Native profilers (4.6+): Tracy, Perfetto (Android default) and Apple Instruments can see GDScript, C# and GDExtension frames. Use them for frame-time spikes.
- CLI: `--profiling`, `--gpu-profile`, `--print-fps`, `--benchmark`. Use `--fixed-fps 60 --quit-after N` for repeatable runs.
- Leaks: orphan nodes are nodes removed from the tree but never freed. `Node.print_orphan_nodes()`, `get_orphan_node_ids()` (4.5+).

## CPU: do less work
- Disable processing you don't need: `set_process(false)`/`set_physics_process(false)` when idle. `VisibleOnScreenEnabler2D/3D` pauses off-screen actors. Timers beat per-frame polling.
- Per-frame code is the hot path. Cache nodes in `@onready`/`_Ready`. Use `StringName` literals (`&"jump"`) for actions, groups and method names. Don't call `get_tree().get_nodes_in_group()` every frame. Use typed GDScript (typed opcodes are faster).
- Signals and `call_group` are cheap for events, but don't emit them per entity per frame for thousands of entities.
- **Thousands of things:** stop using one Node per thing.
  - Visuals: `MultiMeshInstance3D/2D` (one draw call; write `multimesh.buffer` in bulk), or GPU particles.
  - Logic: plain arrays and structs in one manager script (data-oriented), not a script per entity.
  - Physics: `PhysicsServer2D/3D` bodies and areas without nodes, or one raycast batch per frame.
  - Rendering without nodes: `RenderingServer` instances and canvas items.
- Physics: keep `physics_ticks_per_second` at 60 unless the game needs more. Use simple primitive shapes, and avoid `ConcavePolygonShape3D` on moving bodies. Layers and masks cut pair checks. Let bodies sleep (`can_sleep`).

## Threads
- `WorkerThreadPool.add_task(callable)` / `add_group_task(callable, count)` (parallel for), then `wait_for_task_completion(id)`. That's better than raw `Thread` for most jobs.
- Scene-tree rule: nodes inside the tree may only be touched from the main thread, unless they're in a **thread group** (`process_thread_group = PROCESS_THREAD_GROUP_SUB_THREAD`, which processes that subtree in parallel and uses `call_deferred_thread_group` for cross-group calls). From worker threads, hand results back with `call_deferred` / `Callable.call_deferred()`. Assert with `Thread.is_main_thread()` (4.7).
- Shared data: guard it with `Mutex`, or give each worker its own slice and merge on the main thread.
- Background loading: `ResourceLoader.load_threaded_request(path, "", true)` uses sub-threads for dependencies.

## GPU and rendering
- Draw calls: merge static meshes and share materials, because each unique material on a mesh surface adds calls. Use MultiMesh for repeats and texture atlases in 2D.
- Lights and shadows are the usual GPU hogs. Use few shadowed omni and spot lights, keep `directional_shadow_max_distance` small, and bake static lighting (LightmapGI).
- Overdraw: big transparent particles and full-screen alpha. Use alpha scissor or hash for foliage and smaller particle quads.
- Scale detail: LOD (`mesh_lod_threshold`), `visibility_range_*`, occlusion culling, and resolution scaling (FSR, MetalFX) on weak GPUs. Pick the right renderer: Mobile or Compatibility for low-end (see `godot-3d-rendering`).
- Shader hitches: shader baker (export option), fewer material variants.

## Loading and memory
- `preload` loads at script load and blocks. Use it only for small things you always need. `load` is lazy. Threaded loading suits levels.
- `ResourceLoader` caches resources. Reuse them, and don't `duplicate()` shared resources unless you need per-instance state.
- Textures: VRAM-compressed import (default for 3D; enable for big 2D). Mipmaps for 3D. Limit max size per platform. Audio: Ogg streams for long tracks.
- Free what you spawn: `queue_free()` and pools for bullets. Watch the orphan count stay flat.

## GDScript vs C#
- GDScript is fine for gameplay. Move tight math loops (pathfinding, procgen, simulations) to C# or GDExtension, and still batch API calls.
- C#: avoid per-frame allocations (LINQ, closures, string formatting, `new Godot.Collections.Array`). Every Godot API call crosses an interop boundary, so batch them. Packed arrays copy when they cross that boundary.

## Platform budgets (rule of thumb)
Mobile: < 100–150 draw calls, 1 shadowed light, Mobile or Compatibility renderer, 30–60 FPS target. Web: Compatibility renderer, single-threaded unless the export uses threads (needs cross-origin isolation headers), and keep downloads small. Desktop or console: Forward+, profile on the minimum-spec hardware.

Perf HUD + custom monitors, MultiMesh crowd, parallel group task, server-side bullets (compiled by the tests): [references/patterns.md](references/patterns.md)
