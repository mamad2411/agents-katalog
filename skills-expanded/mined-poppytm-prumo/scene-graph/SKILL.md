# Scene Graph & ECS

## Purpose
Implement entity-component-system (ECS) architectures and hierarchical scene graphs with cache-friendly component storage, correct world-transform propagation, and deterministic iteration order suitable for fixed-timestep simulation and multithreaded systems.

## Use when
- Designing archetype- or sparse-set-based component storage for high entity counts with frequent add/remove.
- Implementing parent-child transform hierarchies with dirty-flag propagation and cycle detection.
- Diagnosing frame spikes from structural changes, iterator invalidation, or transform update storms.
- Operating in mode(s): `implementation`.

## Do not use when
- Implementing contact generation or rigid body solvers (use `physics-collision`).
- Tuning render-pipeline state sorting or GPU resource management (out of scope for this skill).
- Modeling pure UI layout without entity simulation semantics (use UI layout tooling instead).

## Required context
- Engine architecture specification (archetype vs sparse-set ECS, AoS vs SoA layout, single vs multithreaded systems).
- Target hardware / GPU constraints (L1/L2 cache sizes, SIMD width, frame budget for scene update).
- Benchmark fixtures (entity counts, add/remove churn rate, hierarchy depth, system mix).

## Procedure
1. **Choose storage by access pattern**: archetype tables (packed SoA columns) for dense, system-iterated components (transform, velocity); sparse sets for rarely-present tags (selected, disabled). Keep hot components under ~64 bytes per row for cache-line efficiency.
2. **Separate structure from data**: entity IDs are generational indices (index + generation counter); destroying an entity bumps generation so stale handles fail validation instead of aliasing recycled rows.
3. **Propagate transforms top-down with dirty flags**: mark subtrees dirty on local change; recompute `world = parent_world * local` in breadth-first order once per tick; detect parent cycles at attach time and reject them.
4. **Schedule systems deterministically**: fixed system order per phase (input → simulation → transform sync → render extract); structural changes (add/remove component) defer to command buffers applied at phase boundaries, never mid-iteration.
5. **Parallelize safely**: partition archetype chunks across jobs by disjoint component sets; transform hierarchy sync stays single-threaded or uses level-by-level wavefronts to respect parent-before-child ordering.
6. **Verify with churn benchmarks**: spawn/destroy N entities per frame while systems iterate; assert no iterator invalidation, no stale-handle resurrection, and update time within budget.

## Decision rules
- **Generational handles mandatory**: raw array indices as entity references are prohibited.
- **No structural mutation during iteration**: add/remove/attach operations inside a system loop must go through a deferred command buffer.
- **One transform write path**: world matrices are written only by the hierarchy sync pass; gameplay and physics write local transforms.
- **Deterministic system order**: system execution order is explicit configuration, never plugin-registration order.

## Evidence required
- Benchmark log: entity counts, churn rate, per-system timings, hierarchy depth tested.
- Stale-handle and cycle-rejection test results.
- Passing execution log from `scripts/verify.sh`.

## Output contract
- Optimized engine subsystem (ECS storage + hierarchy sync + system scheduler).
- Deterministic benchmark evidence (churn test, ordering test, timing profile).
- Visual test fixtures (deep hierarchy scene, 10k-entity stress scene, churn scene).

## Stop conditions
- Scene update meets the frame-time budget on all benchmark fixtures with deterministic system order verified.
- Generational-handle safety and cycle rejection proven by tests.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to lead architect if the budget requires changing public ECS API semantics (e.g. removing deterministic ordering guarantees).
- Escalate immediately upon discovering memory unsafety from handle aliasing or data races in parallel systems.
