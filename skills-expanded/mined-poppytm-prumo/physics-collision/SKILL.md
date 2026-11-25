# Physics & Collision Systems

## Purpose
Implement deterministic spatial partitioning, broadphase/narrowphase collision detection, and rigid body dynamics with strict frame-time budgets, zero per-frame heap allocation, and reproducible simulation output across fixed-timestep ticks.

## Use when
- Implementing broadphase acceleration structures (uniform grids, sweep-and-prune, BVH, octrees) for scenes with hundreds or more dynamic bodies.
- Implementing narrowphase contact generation (SAT, GJK/EPA) and constraint solvers (sequential impulses) for rigid bodies.
- Diagnosing tunneling, jitter, resting-contact instability, or frame-time spikes in an existing physics step.
- Operating in mode(s): `implementation`.

## Do not use when
- Designing entity lifecycles, component storage, or transform hierarchies without contact dynamics (use `scene-graph`).
- Tuning rendering pipelines, shaders, or GPU resource binding (out of scope for this skill).
- Authoring gameplay rules layered on top of stable physics queries (use gameplay code with physics raycasts as input).

## Required context
- Engine architecture specification (fixed vs variable timestep, 2D vs 3D, single-threaded vs job-parallel step).
- Target hardware / GPU constraints (frame budget in ms, SIMD width, cache line size, console TRC timing rules).
- Benchmark fixtures (deterministic scene seeds, body counts, contact-heavy vs sparse scenarios).

## Procedure
1. **Fix the timestep**: integrate at a fixed `dt` (e.g. 1/60 s) with an accumulator; clamp frame delta to avoid spiral of death (max 4 substeps). Never integrate with raw variable frame time.
2. **Select broadphase by scene profile**: uniform spatial hash for evenly distributed bodies; sweep-and-prune for coherent frame-to-frame motion; dynamic AABB tree (BVH) for highly non-uniform scenes. Target broadphase < 15% of the physics budget.
3. **Generate contacts in narrowphase**: AABB overlap test first, then shape-pair dispatch (circle/polygon, sphere/box, convex-convex via GJK+EPA). Apply contact slop (~0.5 mm) and Baumgarte-free split-impulse correction to kill resting jitter.
4. **Solve constraints with sequential impulses**: iterate velocity solver 4–8 iterations, then positional correction; warm-start accumulated impulses from the previous tick for stable stacks.
5. **Prevent tunneling**: enable continuous collision detection (swept shapes or raycast fallback) for any body whose per-tick displacement exceeds half its smallest extent.
6. **Verify determinism and budget**: run the same seeded scene twice and diff contact/rigidbody state bit-exactly; profile per-phase timings and assert total step < budget (e.g. 2 ms at 60 FPS).

## Decision rules
- **Fixed timestep mandatory**: variable-dt integration is prohibited for simulated bodies; interpolation renders between ticks instead.
- **Zero hot-loop allocation**: no heap allocation inside the per-tick broadphase, narrowphase, or solver loops; pre-size pair/contact buffers.
- **Sleeping enabled**: bodies below linear/angular sleep thresholds for N ticks must sleep and skip integration until woken by contact or explicit impulse.
- **Never mutate during query**: physics queries (raycasts, overlaps) during callbacks must be deferred or read-only; structural changes apply between substeps.

## Evidence required
- Benchmark log on reference fixtures: per-phase timings (broadphase, narrowphase, solver), body/pair/contact counts, FPS at 60/120 Hz targets.
- Determinism proof: two seeded runs produce identical body transforms and contact counts.
- Passing execution log from `scripts/verify.sh`.

## Output contract
- Optimized engine subsystem (broadphase + narrowphase + solver with bounded buffers).
- Deterministic benchmark evidence (timings, determinism diff, tunneling regression scene).
- Visual test fixtures (contact-heavy stack scene, high-speed projectile scene, sparse scene).

## Stop conditions
- Broadphase + narrowphase + solver meet the frame-time budget on all benchmark fixtures with zero hot-loop allocations.
- Seeded determinism verified and tunneling/jitter regression scenes pass.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to lead architect if the frame budget cannot be met without changing public physics API semantics (e.g. dropping CCD or solver iterations).
- Escalate immediately upon discovering nondeterminism rooted in platform floating-point or threading behavior.
