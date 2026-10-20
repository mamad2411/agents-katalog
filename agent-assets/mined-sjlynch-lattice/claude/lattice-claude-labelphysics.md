# forceGraph/labelPhysics

The floating-label repulsion physics, split by concern. Shared by all three
label overlays (LOC `Z`, health `H`, Alt names) — each owns a registry (a
`Set<{label, line}>`) and they differ only in the minimum separation. Reached
through the parent facade `../labelRepulsion.ts` (a thin re-export), driven
per-frame by `../labelRepulsionFrames.ts` (scene frame driver + the idle
controller's `labelPhysics` reason). Nothing here touches React, the graph
instance, or the idle controller — it's pure geometry/state. This doc also
holds the parent's label texture/registry rules ("Label resources" below).

## Model

Each label is a sprite hovering over its node with a connector line down to it.
Two forces, in the node's local XZ plane: a gentle **home spring** pulling the
label back to its anchor (`HOME_K`) and **pairwise repulsion** pushing
overlapping labels apart (`PUSH_K`, tapering to zero at the requested
separation). Velocity is integrated with per-frame friction (`FRICTION`) and
snaps to rest once force + speed stay under threshold for `REST_FRAMES`.

## Per-frame tick (`repelLabels(registry, minDist, onDetached?)`)

1. `cleanupStaleRegistryEntries` — drop entries whose sprite was unparented.
   For a label whose node root has left the scene (e.g. a hidden-ext digest),
   it also calls the owning overlay's `onDetached`: `releaseNameLabelEntry` /
   `releaseMetricLabelEntry`. That drops the label-texture refcount (trimming
   the cache at once, unless a batched blanket clear's deferred trim is
   pending) and disposes the entry's connector geometry. This is the per-entry
   release path beside `clearAllLabelRegistries`.
2. `ensureCapacity(count)`, then snapshot each label's world XZ + collect
   entries into the shared scratch buffers in one pass.
3. Seed `fx`/`fz` with the home-spring force (overwrites, so no separate zero).
4. `buildSpatialGridFromScratch` + `pairwiseGrid` accumulate repulsion.
5. Per label: `integrateLabelState` (friction/rest), apply velocity to the
   sprite, `updateConnectorEndpoint` re-anchors the connector's upper end.
6. Returns `true` when every label is at rest (so the driver can release the
   idle reason and let the loop pause).

## Modules

- `types.ts` — shared shapes: `RepulsionEntry` (`{label, line}`), `LabelState`
  (`{vx, vz, restFrames}`), `WorldXZ`. In their own module to avoid cycles.
- `physics.ts` — every tuning constant (the only knobs): `HOME_K`, `PUSH_K`,
  `FRICTION`, rest thresholds (`REST_VEL`/`REST_FORCE` + pre-squared `*_SQ`
  variants that let the hot loop skip `Math.hypot`), `REST_FRAMES`, and the
  zero-distance jitter epsilons.
- `integration.ts` — per-label velocity/rest integration, connector
  re-anchoring, and the sprite-keyed `stateMap` WeakMap. The WeakMap itself does
  not retain sprite keys; collection still depends on releasing other strong
  references, including scene ownership and the last-frame scratch `entries`.
  Dropping a registry entry alone does not guarantee collection.
  `integrateLabelState` uses squared magnitudes to avoid two `hypot`s per label
  per frame.
- `repel.ts` — the per-frame `repelLabels` entry point (the tick above), tying
  scratch buffers + grid + integration together. If the registry is empty
  after stale-entry cleanup, calls `resetRepulsionScratch()` and returns `true`.
- `spatialGrid.ts` — uniform grid (cell = `minDist`) + pairwise phase: each
  label only checks its 3×3 neighbourhood (O(N·k), not O(N²)). The grid is the
  shared `../linkedCellGrid.ts` (packed **integer** cell keys, so the hot loop
  allocates no per-cell key strings; pooled buckets; the build stashes each
  label's integer `(cx, cz)` for the pairwise pass). This module keeps its own
  `floor(world / cellSize)` rounding and pair math. `accumulatePairwiseForces`
  is a legacy entry kept for the tests.
- `scratchBuffers.ts` — module-level reused typed arrays (`worldX`/`worldZ`/
  `fx`/`fz`), the `entries`/`tmpVec` temporaries, and the module-level
  `labelGrid` (a `LinkedCellGrid` owning its cell scratch + recycled bucket
  pool). `ensureCapacity(n)` grows the typed arrays in lockstep; they are live
  `let` exports, so consumers must read them fresh after `ensureCapacity`
  rather than caching the reference.
  `resetRepulsionScratch()` clears `entries` immediately, dropping last-frame
  label/line references while retaining typed-array capacity and grid/bucket
  reuse. Keep these buffers reusable rather than rebuilding arrays each frame.

The stop callback in `../labelRepulsionFrames.ts` also calls
`resetRepulsionScratch()`: once an overlay stops, there may never be another
frame to overwrite/trim `entries`. Releasing scratch references does not dispose
resources. Per-label connector geometry disposal and shared/refcounted
texture/material ownership belong to overlay teardown (below and the
[parent invariants](../CLAUDE.md#load-bearing-invariants-do-not-violate)).

## Label resources

Owned by the parent's label modules, documented here (GPU/heap-leak guards):
`../measuredLabelTexture.ts` (shared measuring context, fresh rasterized
textures), `../labelTexture.ts` (cache keying, refcounts, free-entry eviction,
texture/paired-material/canvas teardown), `../labelSpriteResources.ts` (shared
label materials, colors, line materials, connector geometry templates,
`disposeLabelMaterial`), `../floatingLabelSprite.ts` (`makeFloatingLabelSprite`/
`makeConnectorLine`/`disposeLabelEntry`), `../labelSync.ts` (in-place Alt delta
walker, no `graph.refresh()`), `../hooks/refresh.ts` (registry clears).

- Balance every `buildMeasuredLabelTexture` with a `releaseLabelTexture`. Never
  dispose shared label resources per node.
- `../labelsOverlay.ts` (Alt names) and `../metricOverlayFactory.ts` (LOC +
  health, one shared cache) keep module-level caches that survive remounts and
  project switches, capped at `maxEntries: 256` AND `maxFreeBytes:
  LABEL_TEXTURE_FREE_BYTES_BUDGET` (8 MB of canvas pixels, width×height×4 at
  draw time) for FREE entries only. Eviction takes the oldest free entry first
  (O(1) via the cache's `free` set); in-use (refcount > 0) entries are never
  counted, evicted, zeroed or disposed. The agent-label cache uses the same byte
  budget.
- `labelsOverlay.MAX_NAME_LABELS` (300) caps name labels IN USE — a select-all +
  Alt otherwise allocated a ~150–300 KB canvas + GPU texture per node — and
  `labelSync` strips before it adds so the budget frees first.
- A cache miss finishes drawing before eviction/insertion. Eviction and owner
  teardown zero each owned canvas's dimensions to release native pixels without
  waiting for GC; retained free entries and live/shared labels keep theirs.
- Connector line materials are a `createSpriteMaterialCache` disposed at graph
  teardown (an undisposed one pinned the dead renderer). Each connector gets its
  own `clone()`d geometry — the only thing `disposeLabelEntry` frees (harmless
  repeat for library-replaced objects). `AgentOverlay.destroy` frees the
  agent-label cache.
- **Blanket release:** `clearAllLabelRegistries` (`../hooks/refresh.ts`); never
  `.clear()` a registry. `'batched'` mode (`clearLabelsAndRefresh`, and
  `useGraphDataSync`'s structural swap and `!data` reset) releases refcounts
  *without evicting*: on-screen labels move to `free` in order and the rebuild
  re-acquires them, so no new canvases. Misses and single releases don't evict
  while the batch is open. One deferred trim (`LABEL_TRIM_DELAY_MS`) then runs
  after the library's debounced digest has re-run `nodeThreeObject`; a newer
  batched clear reschedules it, and a batch that left nothing free schedules
  none. The default `'teardown'` mode (graph teardown's `clearLabels`) evicts
  EVERY free entry, so module caches hold no free canvases after destroy.
- **Per-entry release** trims at once: the Alt delta walker's toggle and the
  repulsion `onDetached` (tick step 1 above).
- The library's `_deallocate` disposes each replaced node object's geometry,
  material and `material.map` on `refresh()`/`graphData()`/`_destructor`, so a
  re-acquired texture re-uploads from its retained canvas.
- Gauges: `../graphMemGauges.ts` plus the label-cache byte gauges. Coverage:
  `labelTextureCache.test.ts`.

## Tests

- `frontend/src/__tests__/repulsionScratchReset.test.ts` — a live tick fills
  `entries`; an empty registry tick returns `true` and releases all scratch
  entry references (no forced-GC or GPU-disposal assertion).
- `frontend/src/__tests__/labelRepulsion.test.ts` — deterministic zero-distance
  jitter/pairwise forces, rest integration, and connector endpoint epsilon
  updates; asserts behavior rather than grid-key form.

## Commands

From `frontend/`: `npm run build` (build), `npm test` (tests), `npx tsc -b`
(type-check).
