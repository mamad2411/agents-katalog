---
name: manage-scene-lifecycle
description: Orchestrate scene hierarchies, asynchronous level streaming, additive scene loading, and resource disposal lifecycles. Use when managing scene transitions, additive loading, VRAM cleanup, or dependency injection across scenes.
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

# Manage Scene Lifecycle

Architect and coordinate scene lifecycles, additive level streaming, transition animations, and explicit resource disposal across production game engines.

## Core Rules

- **Asynchronous Non-Blocking Streaming**: Never freeze the main render thread during scene transitions or asset loading. Load scenes in background threads or via asynchronous promises while displaying smooth transition feedback.
- **Explicit Lifecycle Hooks**: Enforce clean lifecycle callbacks for every scene and level chunk: `OnPreload()`, `OnInitialize()`, `OnActivate()`, `OnDeactivate()`, and `OnDisposed()`.
- **Zero VRAM/RAM Leaks**: Disconnect all signal observers, event listeners, and timers before unloading a scene. Force explicit disposal of orphan textures, meshes, and audio streams to prevent memory creep.
- **Contract Adherence**: Emit `contracts/schemas/implementation-result.json` when implementing scene management systems.

## Suggested Process

### 1. Scene Coordinator Architecture
Create a root scene manager service decoupled from individual level nodes. Implement scene stacks for menus, HUD overlays, pause screens, and active gameplay levels.

### 2. Additive Level Streaming
Partition large worlds into spatial streaming volumes or grid chunks. Additively load adjacent chunks based on player camera bounding boxes and asynchronously unload distant sectors.

### 3. Transition & Pre-Warming Orchestration
Coordinate screen fades, loading screens, and shader pre-warming:
- Fade out screen and mute scene audio buses.
- Unload previous scene entities and invoke garbage collection during transition blackouts.
- Instantiate new scene hierarchy and await first draw before fading in.

### 4. Dependency Injection & Service Scoping
Pass runtime dependencies (player session, save data reference, audio manager) explicitly to loaded scenes via injection context rather than relying on global mutable singletons.

## Output Contracts

When completing scene lifecycle management, emit:
- `contracts/schemas/implementation-result.json`

## Checklist

- [ ] Scene loading executes asynchronously without stalling the main render thread
- [ ] Additive level chunks load and unload cleanly based on player proximity
- [ ] All signals, event bus subscriptions, and timers disconnect upon scene unload
- [ ] Unused textures and mesh buffers are explicitly purged from GPU VRAM
- [ ] Dependencies are injected cleanly into newly instantiated scene root nodes
- [ ] Loading screen and transition animations maintain stable frame pacing

## Failure Modes

- **Main-thread stall**: a scene transition loads synchronously on the render thread, freezing the frame and the transition animation. Mitigation: stream scenes in background threads or async promises while showing smooth transition feedback.
- **Signal and listener leaks**: a scene unloads without disconnecting observers, leaving dangling event handlers that fire on destroyed nodes and creep memory. Mitigation: disconnect all signals, event bus subscriptions, and timers in `OnDeactivate()`/`OnDisposed()`.
- **VRAM creep**: orphan textures, meshes, and audio streams survive chunk unloads until long sessions run out of GPU memory. Mitigation: explicitly purge orphaned resources on unload and track VRAM budgets per streaming sector.
- **Hook order violation**: `OnActivate()` fires before `OnInitialize()` or a deactivated scene keeps receiving ticks, producing half-initialized state. Mitigation: enforce the ordered lifecycle (`OnPreload -> OnInitialize -> OnActivate -> OnDeactivate -> OnDisposed`) exclusively through the coordinator.
- **Pop-in without pre-warming**: the fade-in reveals a scene whose shaders have not compiled yet, causing a blank flash or hitch. Mitigation: pre-warm shaders and await the first drawn frame during the transition blackout before fading in.
- **Singleton state bleed**: global mutable singletons carry stale scene state (old player session flags) into freshly loaded scenes. Mitigation: pass dependencies via explicit injection context scoped to each scene load.
- **Streaming thrash**: a player pacing along a chunk boundary repeatedly loads and unloads the same sectors, thrashing I/O. Mitigation: apply hysteresis margins to streaming volumes so unload radii exceed load radii.

## Security Guardrails (OWASP ASI)

- **ASI05 RCE Guard**: scene and chunk identifiers used to construct load paths can originate from level scripts or mods. Mitigation: validate scene paths against a registered scene manifest before instantiation; reject traversal patterns.
- **ASI06 Context & Memory Poisoning**: dependencies injected into scenes (save data reference, session state) are shared cross-scene memory; stale or tampered references must not silently re-enter new scenes. Mitigation: validate injected context at `OnInitialize()` and reset scene-scoped caches on unload.
- **ASI08 Cascading Failures**: a failed chunk load must not leave a half-streamed world running. Mitigation: declare the failure, roll back to the last complete scene state, and surface the error to the coordinator before gameplay continues.
- **ASI07 Inter-Agent Communication**: the coordinator mediates between engine, persistence, and camera/UI systems during transitions. Mitigation: emit the schema-valid `implementation-result.json` contract so peers bind to the declared lifecycle and streaming API.
- **ASI09 Human-Agent Trust Exploitation**: do not claim leak-free unloads from inspection alone. Mitigation: back zero-leak claims with post-unload resource/VRAM profiling evidence across repeated transitions.

## Related Skills

- **integrate-game-engine**: engine project structure and asset importer presets
- **implement-save-persistence**: preserving persistent state across scene reloads
