---
name: forgeax-engine-ecs
description: >-
  ForgeAX archetype ECS, schedules, resources, and shared numeric kernels. Use when
  defining components, queries, systems, relationships, fixed-step simulation, or World recovery.
---

# forgeax-engine-ecs

> **A World's simulation schedules are `Update` for variable-rate work and `FixedUpdate` for fixed-rate work.** Register with a schedule token first, then advance both through `world.update(deltaSeconds)`. A non-simulation domain (the renderer) declares its phases with `defineSchedule(name)` and runs them explicitly with `world.run(token)`, which never advances time.

## One-screen takeoff

```ts
import { FixedUpdate, Time, Update, World, defineComponent } from '@forgeax/engine-ecs';

const Position = defineComponent('Position', { x: 'f32' });
const Velocity = defineComponent('Velocity', { x: 'f32' });
const world = new World({ time: { fixedDeltaSeconds: 1 / 60, maxStepsPerUpdate: 4 } });

world.addSystem(Update, {
  name: 'integrate-variable',
  queries: [{ write: [Position], read: [Velocity] }],
  fn: (current, [moving]) => {
    const delta = current.getResource(Time).delta;
    for (const row of moving) {
      row.mut(Position).x += row.get(Velocity).x * delta;
    }
  },
}).unwrap();

world.addSystem(FixedUpdate, {
  name: 'simulate-fixed',
  queries: [],
  fn: () => { /* deterministic fixed-rate work */ },
}).unwrap();

world.update(1 / 60).unwrap();
```

A retained Query also supports synchronous `query.forEach(row => { ... })`.
It reuses that Query's borrowed cursor instead of allocating another iterator.
Read the row during the callback; do not suspend or retain it. Callback failure
closes without advancing a temporal observation, and same-Query reentry is
rejected. Use numeric batches/spans for numerical kernels and the existing row
iterator when traversal must be suspended or exited early.

`Time` and `FixedTime` are World-owned resources. Systems read them; hosts never write time resources directly.

For owner-package numeric reads into existing scratch, use
`world[worldRead].copyArray` from `@forgeax/engine-ecs/world-read`. It resolves the
live row and returns the current count, or `undefined` without writing for a
missing field or insufficient target. Inline fields avoid transient row views;
variable fields retain live pool lookup. Keep ordinary gameplay on World/Query.

## Cordis owns lifecycle; ECS runs the hot path

`createWorldContext(world, plugins?)` creates a native DeepSeek Cordis realm and
`worldPlugin(world)` supplies its single World service. Plugins use `ctx.effect` to install/remove systems, resources,
simulation participants, resource descriptors, or transform publishers. Context does not copy components,
query rows, or frame data.

```ts
import { Update, createWorldContext } from '@forgeax/engine-ecs';
import type { Plugin } from '@forgeax/engine-plugin';

const movementPlugin: Plugin = {
  name: 'movement',
  inject: ['world'],
  apply(ctx) {
    ctx.effect(() => {
      ctx.world.addSystem(Update, Movement).unwrap();
      return () => ctx.world.removeSystem(Update, Movement.name).unwrap();
    });
  },
};

const context = await createWorldContext(world, [movementPlugin]);
await context.fiber.restart();
```

Fiber determines whether an ECS contribution exists; `world.update(deltaSeconds)` still runs schedules, queries, SoA
access, and Commands directly. Do not query Context inside systems or register per-entity/per-frame data as services.

## Saved paths and distance following

Install `pathPlugin()` from `@forgeax/engine/path` in the World realm. Author `Path` and `PathFollower` in an ordinary keyed SceneAsset and deliver it through Pack/GUID. `FixedUpdate` advances signed world-unit distance before Scene propagation. For physics entities choose desired motion, add `DesiredPathPose`, and consume it in the existing motor.

Use [`packages/path/README.md`](../../packages/path/README.md) for axes, scale, reimport and closed error recovery. Validate with its independent accuracy and World performance gates; use [`apps/perf/path-follow`](../../apps/perf/path-follow) for actual Pack/browser and RHI evidence.

## Curve-driven joint chains

Use `@forgeax/engine/animation/spline-ik` for an explicit root-to-tip chain driven by an ordinary saved `Path`. Install `splineIKPlugin()` beside Scene and Animation; saved `SplineIK` entity references remain instance-local. Author base-pose systems between `animation/restore-spline-base` and `animation/solve-spline-ik`; Scene and Skin consume the committed Transform pose. Use [the Animation contract](../../packages/animation/README.md#spline-ik) for length, axes, twist, scale and stale-binding failures, and [the frozen qualification](../../scripts/dev-verify/roi-24-spline-ik/README.md) for actual acceptance status. Keep rig composition with its owner; unqualified same-joint spring/physical ordering is not an implicit engine service.

## Shared Kernel

```ts
import { Update, defineSharedKernel, type QuerySpan } from '@forgeax/engine-ecs';

function integrate(spans: readonly QuerySpan[]): void {
  for (const span of spans) span.mut(Position).x.fill(1);
}

world.addSystem(Update, defineSharedKernel(kernelModuleUrl, {
  name: 'integrate-shared',
  queries: [{ write: [Position] }],
  run: integrate,
})).unwrap();
```

Use `World({ storage: 'shared' })` only inside a selected shared Engine realm. A Kernel must be an independently loadable named module function with explicit read/write descriptors and numeric table fields. Optional, change-detection, sparse, object, DOM, GPU, and structural access is ineligible. Small work and pre-dispatch pool failure run inline; any failure after a possible shard write poisons the World and forbids retry. Recovery belongs to `app.execution.rebuild()`, not ECS mutation of the old identity.

## Schedule-scoped registration

All five scheduling mutations take the schedule token as their first argument. `Update` and `FixedUpdate` are nominal tokens, not strings.

```ts
import {
  FixedUpdate,
  Update,
  defineSystem,
  defineSystemSet,
} from '@forgeax/engine-ecs';

const Gameplay = defineSystemSet({ name: 'gameplay' });
const Movement = defineSystem({ name: 'movement', queries: [], fn: () => {} });
const Cleanup = defineSystem({ name: 'cleanup', queries: [], fn: () => {} });

world.addSystem(Update, Movement).unwrap();
world.addSystems(Update, Gameplay, [Movement, Cleanup]).unwrap();
world.configureSets(Update, { set: Gameplay }).unwrap();
world.removeSystem(Update, 'cleanup').unwrap();
world.replaceSystem(Update, 'movement', {
  name: 'movement',
  queries: [],
  fn: () => {},
}).unwrap();
```

A system belongs to the schedule selected at registration. Use `after: [FixedUpdate]` or `before: [FixedUpdate]` only as the intrinsic fixed-anchor edge inside `Update`; do not use it to smuggle a system between schedules.

### Migration from the pre-token form

The old single-schedule forms are deleted. Add the appropriate first argument (`Update` or `FixedUpdate`) to every registration and pass the host-measured `deltaSeconds` to each update call. The final shapes are `world.addSystem(Update, system)`, `world.addSystems(Update, set, systems)`, `world.configureSets(Update, options)`, and `world.update(deltaSeconds)`.

### Domain schedules

A non-simulation owner (the renderer's Render World) declares phases with `defineSchedule('Name')`, registers systems by passing that token to `addSystem`, and executes them with `world.run(token)`. Names `Update`, `FixedUpdate` and the empty string are rejected. A run orders only its own schedule, flushes its commands, never advances `Time`, and is never driven by `world.update`. Game code stays on `Update`/`FixedUpdate`.

## Time policy and resources

```ts
import { FixedTime, Time, World } from '@forgeax/engine-ecs';

const world = new World({
  time: {
    fixedDeltaSeconds: 1 / 60,
    maxStepsPerUpdate: 4,
    maxDeltaSeconds: 0.1,
  },
});

world.update(0.2).unwrap();
const variable = world.getResource(Time);
const fixed = world.getResource(FixedTime);

console.log(variable.delta, variable.elapsed, variable.maxDeltaSeconds);
console.log(fixed.delta, fixed.tick, fixed.maxStepsPerUpdate);
console.log(fixed.droppedSeconds, fixed.droppedUpdates);
```

`world.update(deltaSeconds)` validates a finite non-negative delta, clamps it by `maxDeltaSeconds`, runs `Update` once, and drains `FixedUpdate` in fixed increments. If the cap prevents full catch-up, `FixedTime.droppedSeconds` and `FixedTime.droppedUpdates` report the discarded work. They are observable metrics, not errors and not an app-level clamp.

Use `Time.delta` for variable-rate integration and `Time.elapsed` for absolute-time behavior. Use `FixedTime.delta` for deterministic fixed simulation. A manually constructed World can run a zero-delta frame with `world.update(0)`.

## Scope failures and Result handling

Every schedule mutation, `world.update` and `world.run(token)` returns `Result`. Handle errors by their closed `code` union:

```ts
const result = world.addSystem(Update, fixedOnlySystem);
if (!result.ok) {
  switch (result.error.code) {
    case 'schedule-scope-mismatch':
      console.error(result.error.hint);
      break;
    case 'system-before-unknown':
    case 'system-after-unknown':
    case 'system-set-not-registered':
      console.error(result.error.hint);
      break;
  }
}
```

`'schedule-scope-mismatch'` means a target system, set, or fixed anchor belongs to the other schedule. `world.run(token)` returns the same code when the domain token (from `defineSchedule`) has no registered system in this World, so register a system on that domain token before running it. Keep dependent systems and sets in the same scope; do not catch and ignore the failure or add a compatibility registration path.

## Numeric workspace lifetime

Use `world.frameArena.alloc(TypedArrayConstructor, count)` for synchronous
scratch inside `update`/`run`; initialize the elements read. It survives fixed
ticks and command drains, then expires on outer scope close. Group contiguous
synchronous domain runs with `withFrameArena`; never carry scratch across await,
yield, transport, snapshots or GPU completion.
Returning a Promise/iterator from a system or scope poisons the World; schedule
suspended work through its existing owner instead.

For system-owned cross-frame numeric buffers, use `world.buffers.alloc`,
`view`, `resize` and `release`. Bind release to the real plugin owner. Borrow a
lease for an independently completing reader; owner release retires storage,
and the last lease return permits reuse. Resize requires no active leases.
Public grants never revive with raw slot reuse. Components retain their schema
and World write paths. Read the [ECS memory contract](../../packages/ecs/README.md#numeric-memory-services)
for budgets, trim, borrowed-view limits and observation coverage.

## Query model

`world.query(descriptor)` is the only query constructor. It returns `Result<Query, QueryCreationError>`.

| Role | Meaning | Row access |
|:--|:--|:--|
| `read` | required data, immutable intent | `row.get(Component)` |
| `write` | required data, mutation intent | `row.mut(Component)` |
| `optional` | data may be absent | `row.get(Component)` returns value or `undefined` |
| `with` / `without` | presence-only filter | no data access |
| `changed` / `added` | query-owned observation filter | no extra data permission |

`for...of query` is canonical. A yielded `QueryRow` is transient; consume it in the loop and retain `row.entity` when later work needs identity. Structural mutation invalidates active iteration with a structured ECS error.

```ts
const query = world.query({ read: [Health], with: [Enemy] }).unwrap();
for (const row of query) console.log(row.entity, row.get(Health).value);
```

Use `query.spans()` only for dense, table-only descriptors. It rejects optional
data and sparse components with `query-span-unavailable`; `changed` and `added`
filters are supported and yield only matching contiguous runs. Span columns
are zero-copy transient TypedArray views and become invalid after a structure
epoch change.

For a read-only query with sparse membership or optional numeric data, use
`query.batches().unwrap()`. Each batch exposes original physical columns through
`read(Component, field)` and `stride(Component, field)`. A `range` batch uses
`start <= row < end`; an `indexed` batch uses the valid `rows[0..count)` prefix.
Index entities and columns with the physical row. Resolve optional columns once
per batch; `undefined` means absent, while zero remains a value. Current batches
reject write and changed/added descriptors explicitly. Keep their existing row,
span or projection routes. Read/index arrays are borrowed, and structural
mutation inside the raw loop is prohibited. Retained Query validation removes
repeated setup allocation; traversal/batch allocation remains. Compare the
[actual-API benchmark](../../packages/ecs/bench/query-batches.mjs) before migration.

Relationship sources remain writable through `World.set` and row mutation so
the ECS owner can update the source, materialized target list, and backpointer
together. Relationship targets are read-only projections. Numeric writable
spans and the internal derived writer reject only relationship source/target
fields that appear in the descriptor's write set; a relationship input listed
only in `read` remains eligible (Scene reads `ChildOf` while writing
`GlobalTransform`). Use a row or World source write for relationship changes.
Liveness, cycle, capacity, version, and epoch failures are reported at the
owner boundary before relationship facts are committed.

```ts
const query = world.query({ write: [Position], read: [Velocity] }).unwrap();
for (const span of query.spans().unwrap()) {
  const position = span.mut(Position).x;
  const velocity = span.get(Velocity).x;
  for (let i = 0; i < span.length; i++) position[i] = (position[i] as number) + (velocity[i] as number);
}
```

`query.combinations(k)` derives K-way iteration from the same query.

## Storage choice

`defineComponent` uses table storage unless the token explicitly declares a zero-field sparse tag.

```ts
const Enemy = defineComponent('Enemy', {});
const Selected = defineComponent('Selected', {}, { storage: 'sparse' });
```

Use table storage for every data component and for stable identity tags. Use sparse only for frequently flipped membership. Sparse tags still participate in Archetype identity, hooks, cardinality, scene round-trip, inspection, and ordinary row queries, but Archetypes that differ only by sparse membership share the same physical Table.

Sparse tags have no fields, so they belong in `with`, `without`, `changed`, or `added`, never `read`, `write`, or `optional`. A sparse predicate makes `query.spans()` return `query-span-unavailable` with reason `sparse-component`; use read-only numeric batches when eligible, or row iteration for semantic/writable/temporal access. A writable relationship source or target makes both `query.spans()` and the internal derived writer return `query-span-unavailable` with reason `relationship-component`; route source changes through `World.set`, `row.mut`, or structural commands so the materialized mirror stays atomic. `Disabled` is always a table tag.

### Array fields: replace or write a range

`World.set` replaces an `array<T>` field as one value (O(length)). To change a few elements of a large array, such as moving one row of `Instances.transforms`, write the window in place:

```ts
world.setArrayRange(entity, Instances, 'transforms', row * 16, matrix).unwrap();
```

The length never changes (resize with `set`). An out-of-range window or a non-array field returns `array-range-out-of-bounds` with no mutation. Consumers read `readArrayRangesChangedSince(world, entity, component, field, since)` from `@forgeax/engine-ecs/projection`: merged element ranges after an epoch, or `'whole'` when the history cannot prove them. The renderer uses it so a moved instance row costs O(1) instead of O(N). A write covering the whole field reports `'whole'` and keeps no range history.

For O(changes) loops over many entities, prefer `setArrayRange` or a scalar `set` for hot writes, and use a sparse tag, not a table tag, for membership that flips every frame.

## Required components

Declare intrinsic structural dependencies once on the component schema:

```ts
const GlobalTransform = defineComponent('GlobalTransform', { world: 'array<f32, 16>' });
const Transform = defineComponent('Transform', { x: 'f32' }, {
  requires: [GlobalTransform],
});
```

`World.spawn`, `World.addComponent`, and deferred `Commands` materialization
expand `requires` transitively at the structural boundary. Explicit data for a
required component wins; missing identities are appended once. This is generic
ECS behavior, so scene/import helpers must not duplicate it and systems must
not perform per-frame repair scans. Removing a requirement does not cascade;
an owner that does so explicitly gets the owning domain's structured invariant
error on the next use.

## Systems and structural mutation

Systems receive the owning `World`, a tuple of persistent Query objects, and deferred `Commands`. Use `commands` for structural changes; the schedule flushes them at defined boundaries.

```ts
import { Update, defineComponent } from '@forgeax/engine-ecs';

const Health = defineComponent('Health', { value: 'f32' });
world.addSystem(Update, {
  name: 'remove-dead',
  queries: [{ read: [Health] }],
  fn: (_world, [health], commands) => {
    for (const row of health) {
      if (row.get(Health).value <= 0) commands.despawn(row.entity);
    }
  },
}).unwrap();
```

`Commands.spawn` takes the same component-data entries as `World.spawn` and
returns a pending handle; each entry is `{ component, data }`. The batch is
validated before flush, then the pending row is materialized once:

```ts
const pending = commands.spawn(
  { component: Transform, data: { pos: [0, 0, 0] } },
  { component: ChildOf, data: { parent } },
);
void pending;
```

For a generic exclusive relationship, the direct convenience signature passes
the relationship component and its declared source-field data explicitly:
`world.reparent(child, newParent, RelationshipSource, sourceData)`.
`sourceData` must set that schema's source field to `newParent`; the
relationship component and its source-field data are required. The same owner
path is also reached by `world.set(child, RelationshipSource, data)` or an
exclusive `addComponent`.

Expected command/preparation failures leave the World healthy and can be
retried after correcting the input. An unknown exception after a row or
derived range may have been written poisons the World; stop using that World
and let `app.execution.rebuild()` create the replacement rather than retrying
the old identity.

For component schema, storage, relationship, reflection, and errors, read `packages/ecs/README.md` and `packages/ecs/src/`. Scheduling is token-first and query construction has one entry; no compatibility overload exists.

## Visibility inspection quick start

```ts
const render = await _import('@forgeax/engine/render');
const query = world.query({ read: [render.Visibility] }).unwrap();
for (const row of query) console.log(row.get(render.Visibility).state);
const effective = render.resolveVisibility(world).effective(entity);
```

| Observation | Read from | Do not infer |
|:--|:--|:--|
| Current | `QueryRow.get` and `Visibility.state` | Final render participation |
| Effective | `resolveVisibility(world)` | Camera or picking state |
| Invalid write | `Result.error.code`, `.expected`, `.hint`, `.detail` | A message-only failure |

If a write fails, use the reflected enum labels to choose a valid value and
retry `world.set`. If effective resolution reports hierarchy diagnostics, repair
the scene relation before retrying. The app host only transports JSON-safe
reflection; ECS remains the component owner.

Out of scope: renderer culling, camera, picking, app lifecycle, assets, and VFX
shadow policy. Route each question to its owning package skill.

## Mobility declaration

`Mobility { kind }` (from `@forgeax/engine/scene`) declares whether an entity
moves; absent means movable. Write `static` for placed level geometry that
never moves, and leave runtime spawns movable.

```ts
world.spawn(
  { component: Transform, data: {} },
  { component: Mobility, data: { kind: MobilityKindValue.static } },
);
const stop = subscribeMobilityDiagnostics((w, d) => console.log(d.code, d.detail.entity));
```

| Code | Cause | Repair |
|:--|:--|:--|
| `mobility-static-moved` | `Transform` of a `static` entity changed after its declaring frame | Declare `movable` (rendering stays correct meanwhile) |
| `mobility-invalid-kind` | `stationary` on a `MeshFilter` entity (lights only) | Use `static` or `movable` |
| `mobility-physics-conflict` | `static` with `RigidBody` `dynamic`/`kinematic` | Declare `movable`, or make the body `static` |

Each diagnostic is reported once per `(World, code, entity)` and carries
`detail.entity` plus `detail.sceneEntityRef` for authored scene members.
`Mobility` and `RigidBody` never derive each other. Details:
`packages/scene/README.md` §Mobility.

## Render capture authoring boundary

`CubeCamera` and `ReflectionProbe` are ECS authoring facts paired with
`Transform`; they carry update intent, bounds, and stable revisions, not GPU
resources. The render owner derives six face cameras, target generations,
bounded PMREM work, material selection, and recovery from those facts. Keep
target/source/readback tokens and `FrameReceipt` observation in the Renderer
contract rather than adding them to World components.

## Simulation record/restore seam

Use the ECS owner when deterministic fixed-tick state must be restored into a
fresh target and compared semantically. The minimum path is
`source.simulationRecord()` -> `target.simulationRestore(record)` ->
`simulationCompare({ facts })`.

`trace` contains ordered fixed-tick input samples. A `participant` is one ready,
versioned owner for portable external state. Every numeric report fact declares
a non-negative `tolerance`. Expected failures are closed errors; switch on
`code` and read `expected`, `hint`, and narrowed `detail`.

The App, Preview, and Remote boundaries expose only the inspection summary and
the schema at `packages/app/schema/simulation-inspection.schema.json`. They do
not own record/schema state or provide restore/replay actions. Do not use this
seam for network rollback, disk persistence, RHI tape replay, game replay, or
pixel comparison.
