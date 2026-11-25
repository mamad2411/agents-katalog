---
name: architect-ecs-systems
description: Architect data-oriented Entity Component System (ECS) architectures, archetype storages, and cache-friendly query schedules. Use when implementing high-entity simulations, DOD architectures, or parallel systems in Bevy, Flecs, or Unity DOTS.
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

# Architect ECS Systems

Design and implement data-oriented Entity Component System (ECS) architectures that optimize CPU cache locality, eliminate heap fragmentation, and scale to tens of thousands of simultaneous simulation entities.

## Core Rules

- **Data-Oriented Cache Locality**: Store components in contiguous memory buffers (archetypes or sparse sets). Design components as Plain Old Data (POD) structs without pointers or virtual function dispatch tables.
- **Explicit System Scheduling**: Organize systems into deterministic execution stages (e.g. `PreUpdate`, `Update`, `PostUpdate`, `FixedUpdate`). Disallow circular execution dependencies between systems.
- **Parallel Safety & Borrow Rules**: Systems with non-overlapping mutable component queries must be capable of executing in parallel threads. Read-only queries can execute concurrently across any number of systems.
- **Contract Adherence**: Emit `contracts/schemas/implementation-result.json` upon completing ECS architecture implementations.

## Suggested Process

### 1. Archetype & Component Decomposition
Decompose entity state into minimal, composable POD components:
- `Position(Vector3)`, `Velocity(Vector3)`, `Health(float, float)`, `RenderMesh(MeshId)`
Avoid monolithic "God components" containing both simulation and presentation state.

### 2. Query Pipeline & Filter Design
Construct zero-allocation entity queries with archetype filtering:
- Query entities matching `(With<Velocity>, With<Position>, Without<StaticGeometry>)`
Iterate components sequentially to leverage hardware prefetching and SIMD vectorization.

### 3. Stage Scheduling & Dependency Ordering
Assign systems to pipeline stages. Ensure structural changes (entity creation, entity deletion, adding/removing components) are deferred via command buffers to stage boundaries to prevent archetype table mutations during iteration.

### 4. Headless Deterministic Benchmark
Implement automated test cases verifying that query schedules produce deterministic simulation state across ticks. Measure memory throughput and cache misses via profiling harnesses.

## Output Contracts

When completing ECS architecture implementation, emit:
- `contracts/schemas/implementation-result.json`

## Checklist

- [ ] Components are designed as contiguous POD structs without heap allocations
- [ ] Systems execute within explicitly sequenced schedule stages
- [ ] Structural entity commands are deferred to frame/stage synchronization points
- [ ] Component queries iterate contiguous arrays without pointer chasing
- [ ] Parallel systems have validated disjoint mutable borrow access
- [ ] Headless test runner validates deterministic simulation output

## Failure Modes

- **Mutation during iteration**: structural changes (spawn/despawn, add/remove component) mutate archetype tables while a query is iterating, invalidating iterators and corrupting entity handles. Mitigation: defer structural changes through command buffers flushed only at stage boundaries.
- **Circular system dependencies**: systems scheduled in a dependency cycle deadlock or reorder nondeterministically between ticks. Mitigation: build an explicit acyclic dependency graph per schedule and fail the build on cycles.
- **Parallel data race**: two systems with overlapping mutable component queries run on parallel threads and produce torn writes. Mitigation: validate disjoint mutable borrow access at schedule construction; allow full concurrency only for read-only queries.
- **God component regression**: simulation and presentation state collapse back into one monolithic component, reintroducing pointer chasing and cache misses. Mitigation: keep components minimal POD structs without pointers or vtables; re-measure cache misses after refactors.
- **Simulation desync**: nondeterministic system ordering or iteration produces divergent world state across runs, breaking replays and netcode rollback. Mitigation: run the headless deterministic benchmark so tick outputs match across executions.
- **Sync-point spike**: a huge batch of deferred structural commands flushes in a single stage, hitching the frame. Mitigation: amortize command buffer flushes and cap structural changes per stage.

## Security Guardrails (OWASP ASI)

- **ASI04 Supply Chain**: Bevy/Flecs/Unity DOTS packages and engine plugins are external dependencies pulled into the simulation core. Mitigation: pin exact versions and verify against the pack schema before adoption; reject drifted or unverified packages.
- **ASI05 RCE Guard**: schedules and queries must never be composed from dynamic strings or external config without validation. Mitigation: construct system registration in code or schema-validated declarative files only.
- **ASI06 Context & Memory Poisoning**: entity/component data deserialized from saves, network snapshots, or mods enters archetypes directly. Mitigation: validate component payloads against component schemas before insertion; treat deserialized state as untrusted.
- **ASI08 Cascading Failures**: a system error mid-stage must not let downstream systems consume a half-mutated world. Mitigation: abort the tick, restore the last consistent world state, and declare failure explicitly to the coordinator.
- **ASI07 Inter-Agent Communication**: the architecture is consumed by gameplay and performance roles downstream. Mitigation: emit the schema-valid `implementation-result.json` contract so peers can validate schedule and storage decisions.

## Related Skills

- **develop-gameplay-systems**: kinematic gameplay systems and hierarchical state machines
- **profile-game-performance**: CPU cache line profiling and memory bandwidth monitoring
- Companion reference: `references/data-oriented-design-and-archetype-ecs.md`
- Companion example: `examples/bevy-flecs-combat-system.rs`
