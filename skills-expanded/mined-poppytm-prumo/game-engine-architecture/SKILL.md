---
name: game-engine-architecture
description: Entity Component System (ECS), fixed delta time game loops, subsystem decoupling, memory pools, and multi-threaded task graphs
---
# Game Engine Architecture & Subsystems

## 1. Entity Component System (ECS) Architecture
Organize game state using data-oriented design: Entities as lightweight IDs, Components as pure plain-old-data (POD) structs stored contiguously in memory, and Systems as stateless logic iterating over component arrays.

## 2. Deterministic Game Loop with Fixed Delta Time
Implement a semi-fixed or fixed timestep game loop (accumulator pattern) for physics and gameplay logic to ensure identical behavior across diverse monitor refresh rates. Separate render interpolation from physics simulation.

## 3. Subsystem Decoupling & Interfaces
Decouple core engine subsystems (Rendering, Physics, Audio, Input, Animation) using explicit interfaces or event buses. Prevent circular dependencies between gameplay logic and lower-level graphics hardware drivers.

## 4. Memory Allocation & Pooling Strategies
Ban frequent dynamic allocations (new/malloc) during active gameplay frames. Use custom memory allocators: stack allocators for per-frame scratch memory, and object/pool allocators for projectiles and particles.

## 5. Multi-Threaded Task Graphs
Execute engine subsystems concurrently using a job system / task graph with work-stealing thread pools. Isolate rendering command submission from gameplay state simulation.

## 6. Asset Lifecycle & Virtual Resource Management
Manage textures, meshes, and sound banks using handle-based resource systems with reference counting. Support background asynchronous streaming and level loading.

## 7. Coordinate Systems & Spatial Partitioning
Standardize engine coordinate conventions (right-handed vs. left-handed, Y-up vs. Z-up). Accelerate spatial queries and frustum culling using BVH, octrees, or spatial hashing.

## 8. State Machine & Scene Graph Hierarchies
Model game progression with a pushdown finite state machine (FSM). Implement scene hierarchies with dirty flags to minimize redundant global matrix computations.

## 9. Developer Tooling & Debug Overlays
Embed real-time diagnostic overlays: frame time graph, draw call counters, memory allocation trackers, and collision wireframe renderers.

## 10. Deterministic Replay & Save State Architecture
Design engine state serialization to support byte-for-byte deterministic replays and atomic snapshot saving/loading.
