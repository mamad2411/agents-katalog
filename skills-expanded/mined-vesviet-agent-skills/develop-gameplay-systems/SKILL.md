---
name: develop-gameplay-systems
description: Build deterministic, high-performance gameplay systems, character controllers, state machines, and combat mechanics across game engines. Use when implementing player movement, mechanics, physics interactions, or game loops.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_build, run_tests, run_linter, execute_command]
version: "1.0.0"
---

# Develop Gameplay Systems

Implement modular, testable gameplay systems and character controllers that maintain deterministic simulation, clean component boundaries, and strict frame-rate independence.

## Core Rules

- **Fixed Timestep Determinism**: Always update physics, collision detection, and spatial queries inside fixed tick loops (`_physics_process` in Godot, `FixedUpdate` in Unity, sub-stepped ticks in Unreal/custom engines). Never bind movement speed directly to variable render delta times.
- **Hierarchical State Isolation**: Model player states (Idle, Run, Jump, Fall, Attack, Stunned) via explicit state machines. Transitions must be driven by verified inputs and conditions, never by ambient variable mutations.
- **Zero GC in Hot Loops**: Pre-allocate collision queries, raycast hit buffers, and vectors. Do not instantiate heap objects, closures, or temporary arrays inside update loops.
- **Contract Adherence**: Emit `contracts/schemas/implementation-result.json` when completing gameplay system slices.

## Suggested Process

### 1. Frame Budget & Timestep Setup
Define target fixed tick rate ($60\text{Hz}$ or $120\text{Hz}$). Ensure kinematic velocity integration follows:
$$\vec{x}_{t+1} = \vec{x}_t + \vec{v}_t \cdot \Delta t_{\text{fixed}}$$
Apply gravity and terminal velocity limits consistently.

### 2. State Machine Assembly
Implement state interfaces with explicit `Enter()`, `Update(delta)`, `FixedUpdate(fixed_delta)`, and `Exit()` lifecycles. Ensure state transitions broadcast events rather than tightly coupling downstream components.

### 3. Spatial Query & Collision Layering
Configure distinct physics collision layers (Player, Enemies, WorldGeometry, Projectiles, Triggers). Use non-allocating raycasts (`PhysicsServer2D/3D`, `Physics.RaycastNonAlloc`) with layer masks to prevent unnecessary broadphase checks.

### 4. Headless Verification
Write unit tests for state transitions and math logic. Run tests via headless engine runner or test harness to verify zero state regressions.

## Output Contracts

When completing a gameplay system implementation, emit:
- `contracts/schemas/implementation-result.json`

## Checklist

- [ ] Movement and physics logic executes exclusively in fixed timestep functions
- [ ] Character controller handles slope limits, wall sliding, and ceiling bonks cleanly
- [ ] State machine enforces single-active-state invariants and validated transitions
- [ ] Collision matrix prevents unnecessary layer pair checks
- [ ] No allocations occur inside `Update` or `FixedUpdate` hot loops
- [ ] Headless test suite passes with zero exit errors

## Failure Modes

- **Frame-rate dependent movement**: movement speed binds to variable render delta times, so players at $144$ FPS move faster than at $60$ FPS. Mitigation: run velocity integration exclusively inside fixed tick loops (`_physics_process`, `FixedUpdate`) using $\vec{x}_{t+1} = \vec{x}_t + \vec{v}_t \cdot \Delta t_{\text{fixed}}$.
- **Ambient state mutation**: an unrelated system writes a player-state flag directly, triggering an untraceable transition (e.g. instant `Stunned` without the stun event). Mitigation: allow transitions only through verified input conditions on the state machine; broadcast transition events instead of shared-flag writes.
- **Broken single-active-state invariant**: two states run simultaneously or none at all, enabling double-jump exploits or dead input. Mitigation: enforce single-active-state invariants with validated transition tables and assert them in unit tests.
- **GC spikes in hot loops**: raycast hit arrays, closures, or temporary vectors allocated inside `Update`/`FixedUpdate` cause frame hitches. Mitigation: pre-allocate collision queries and vectors; use `RaycastNonAlloc`/`PhysicsServer` with reusable buffers.
- **Collision in render update**: spatial queries run in `_process`/`Update`, missing or duplicating checks at variable rates. Mitigation: keep all collision detection and spatial queries inside the fixed tick.
- **Slope/wall confusion**: the controller treats steep walls as walkable ground or slides down valid slopes. Mitigation: separate slope-limit checks from wall-slide logic and cover both with headless test cases.
- **Silent refactor regressions**: a state machine refactor breaks transitions without any visible error. Mitigation: run the headless test suite and require zero exit errors before reporting completion.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: player input packets and mod-loaded scripts are untrusted external content that must never rewrite simulation rules or state-transition tables. Mitigation: treat inputs as data feeding validated transitions; never let external content redefine mechanics at runtime.
- **ASI05 RCE Guard**: never evaluate logic strings from mods, network messages, or level content inside the game loop. Mitigation: resolve behaviors through pre-registered state handlers; reject executable payloads.
- **ASI06 Context & Memory Poisoning**: restored character state from saves or network snapshots can carry NaN velocities or out-of-bounds positions that poison the simulation. Mitigation: validate deserialized state (finite values, sane magnitudes) before the first fixed tick.
- **ASI07 Inter-Agent Communication**: gameplay slices are consumed by game-feel, engine-integration, and asset roles. Mitigation: emit the schema-valid `implementation-result.json` contract so peers integrate against validated behavior.
- **ASI09 Human-Agent Trust Exploitation**: do not report the implementation as tested without a clean run. Mitigation: state the actual headless test result, including any skipped or failing cases.

## Related Skills

- **tune-game-feel**: layered audiovisual responsiveness and timing buffers
- **integrate-game-engine**: engine lifecycle integration and headless runner execution
- **optimize-3d-assets**: mesh and texture budget conformance
- Companion reference: `references/deterministic-gameplay-state-machines.md`
- Companion example: `examples/kinematic-character-controller.gd`
