---
name: design-procedural-generation
description: Designs deterministic procedural content generation (PCG) pipelines using seeded PRNG streams, multi-octave Perlin and Simplex noise, cellular automata cave shaping, and graph-based dungeon room layouts. Use when generating procedural levels, terrain heightmaps, roguelike dungeons, or seeded loot tables.
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

# Design Procedural Generation

Architect deterministic, replayable procedural generation pipelines that combine isolated PRNG seed streams, coherent noise fields, cellular automata smoothing, and validated dungeon graph topologies.

## Core Rules

- **Strict Seed & Stream Isolation**: Never call global unseeded random functions (`Math.random()`, global `rand()`). Instantiate isolated deterministic PRNG streams (`PCG32`, `SplitMix64`, `Xoshiro256**`) per subsystem (e.g. `terrain_rng`, `dungeon_rng`, `loot_rng`) derived from a master seed so cosmetic particle rolls never alter level layout.
- **Playability & Connectivity Guarantees**: Every generated map or dungeon must pass an automated flood-fill or `A*` reachability check verifying that entrances, key objectives, and exits form a fully connected, traversable graph.
- **Zero Main-Thread Stalls**: Execute heavy procedural generation, mesh synthesis, and tilemap baking on background worker threads or across time-sliced coroutines during loading transitions.
- **Contract Adherence**: Emit `contracts/schemas/implementation-result.json` upon completing procedural generation implementations.

## Suggested Process

### 1. Hierarchical Seed Derivation
Hash the user-facing master seed string into subsystem sub-seeds (`seed_layout`, `seed_biomes`, `seed_encounters`, `seed_loot`). Record the master seed and generator version in save files and replay logs for instant reproduction of edge-case layouts.

### 2. Coherent Noise & Cellular Automata Synthesis
For continuous terrain and biomes, combine multi-octave Simplex or OpenSimplex2 fractal Brownian motion (fBM) with domain warping:
$$h(x, y) = \sum_{i=0}^{N-1} \text{amp}^i \cdot \text{noise}\left(\text{freq}^i \cdot x, \text{freq}^i \cdot y\right)$$
For organic cave systems, initialize a seeded binary grid and apply $4\text{--}6$ cellular automata birth/survival smoothing passes (`B5678/S45678`).

### 3. Deterministic Dungeon Room & Graph Layout
Generate structured dungeons via Binary Space Partitioning (BSP), Delaunay triangulation with Minimum Spanning Trees (MST), or Wave Function Collapse (WFC) constraint propagation. Reintroduce a controlled percentage ($10\text{--}20\%$) of non-MST edges to create tactical loops instead of purely linear corridors.

### 4. Reachability Validation & Fallback Regeneration
Run a breadth-first flood fill from the spawn point to verify $100\%$ reachability of critical rooms and items. Automatically carve connecting tunnels for isolated caverns or re-roll with a deterministic salt increment if constraints fail.

## Output Contracts

When completing procedural generation implementation, emit:
- `contracts/schemas/implementation-result.json`

## Checklist

- [ ] All random choices use isolated, deterministic PRNG streams derived from a master seed
- [ ] Identical seeds produce bitwise-identical level layouts across runs and target platforms
- [ ] Multi-octave Simplex/Perlin noise and cellular automata passes are parameterized and tunable
- [ ] Dungeon layout graphs guarantee traversable paths between spawn, objectives, and exits
- [ ] Generation runs asynchronously or within bounded loading budgets without UI freezes
- [ ] Headless test suite validates 1,000+ random seeds for zero soft-locks or unreachable rooms

## Failure Modes

- **Global RNG contamination**: a stray `Math.random()` or global `rand()` call shifts the stream so identical master seeds produce different level layouts. Mitigation: instantiate isolated deterministic PRNG streams (`PCG32`, `SplitMix64`, `Xoshiro256**`) per subsystem and ban global random entirely.
- **Unreachable generation**: BSP/WFC output isolates a key room or exit, soft-locking the run. Mitigation: gate every map behind a flood-fill/`A*` reachability check and auto-carve tunnels or re-roll with a deterministic salt increment on failure.
- **Cross-platform desync**: floating-point differences in noise evaluation break bitwise-identical layouts between target platforms. Mitigation: run the multi-seed headless suite on every target platform and use fixed-point math where divergence appears.
- **Main-thread stall**: heavy mesh synthesis and tilemap baking run synchronously, freezing the loading screen. Mitigation: execute generation on background worker threads or time-sliced coroutines within bounded loading budgets.
- **WFC non-convergence**: constraint propagation hits a contradiction and loops indefinitely. Mitigation: impose an iteration budget and fall back to a deterministic salt re-roll instead of retrying forever.
- **Unrecorded seed/version**: the save file omits the master seed or generator version, making reported edge-case layouts unreproducible. Mitigation: persist master seed and generator version in saves and replay logs at generation time.
- **Cosmetic-loot stream coupling**: a particle VFX roll consumes the loot stream, changing drops when effects change. Mitigation: derive separate `terrain_rng`, `dungeon_rng`, `loot_rng` sub-seeds from the master seed so subsystems never share a stream.

## Security Guardrails (OWASP ASI)

- **ASI04 Supply Chain**: third-party noise libraries and WFC/tile content packs are external inputs to generation. Mitigation: pin versions, verify schema and provenance before adoption, and regression-test seeds after any dependency bump.
- **ASI05 RCE Guard**: WFC tile constraints and generator configs authored as content must never be evaluated as code. Mitigation: load generation definitions as schema-validated data files; reject constraint scripts or executable payloads inside tile packs.
- **ASI06 Context & Memory Poisoning**: master seeds read from save files or replay logs are untrusted inputs; a tampered seed can trigger pathological generation or crash the baker. Mitigation: validate seed format, length, and ranges before derivation; reject malformed seeds with a fresh default seed.
- **ASI07 Inter-Agent Communication**: generation output feeds save-persistence, AI navmesh baking, and scene streaming roles. Mitigation: emit the schema-valid `implementation-result.json` contract including seed and generator version so downstream roles reproduce the same world.
- **ASI09 Human-Agent Trust Exploitation**: do not claim "1,000+ seed validation" without running it. Mitigation: report the actual headless seed-sweep coverage and any soft-lock incidents found.

## Related Skills

- **implement-save-persistence**: serializing master seeds and delta world modifications in save files
- **author-game-ai**: baking runtime Navigation Meshes or A* grids over generated geometry
- **manage-scene-lifecycle**: streaming generated level chunks additively without frame stalls
