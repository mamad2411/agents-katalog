---
name: paper-disposable-world
description: "拋棄式世界與可重置競技場：VoidChunkGenerator、WorldCreator、流水號命名與殘留資料守衛、非同步複製模板（暫存後原子改名）、卸載後安全刪除、26.x dimensions 存檔路徑、預產生池，以及就地還原（變更格子基準表分批還原 + 殘留實體清掃）/ Throw-away Paper worlds and resettable arenas: void generator, serial naming with stale-data guard, async template copy with atomic rename, safe unload and delete, 26.x dimensions storage layout, pre-generated pool, and budgeted in-place reset with debris sweep"
---

# Paper Disposable World

## Skill Name

`paper-disposable-world`

## Purpose

Minigames, duels, and dungeons need "use and throw away" worlds, or arenas that are restored after every match. This skill provides two routes:

1. **World swapping**: copy `arena_<n>` from a template folder, load it, use it, unload it, delete it; an idle pool of worlds can be pre-generated.
2. **In-place reset**: do not swap worlds; record which blocks a match changed, restore them in per-tick budgeted batches when it ends, and sweep leftover entities.

Both routes follow the same principle: **world operations happen only on the main thread; only file IO (copy, delete) goes async**.

The three most dangerous silent failures are all guarded against in the template:

- `createWorld` **silently loads whatever data already exists** for the name (a crashed arena) or generates new terrain over an incomplete folder -> check the world's real data folder first (on 26.x it is `<main world>/dimensions/minecraft/<name>`, not next to the main world)
- A crash halfway through copying or deleting leaves a half folder under a real world name -> **copy into `<name>.copying` and rename atomically; rename to `<name>.deleting` before deleting**, and purge the suffixed debris at startup
- Unloading a world that still has players -> teleport players away first, and call `unloadWorld` only after confirming

## Paper Version Requirements

- Paper 1.21.11 / 26.3; pure Paper API, no Paperweight needed
- **GameRule**: the old constants in `org.bukkit.GameRule` (`DO_DAYLIGHT_CYCLE`, `DO_MOB_SPAWNING`, etc.) are `@Deprecated` in both versions, and vanilla rules were changed to snake_case registry keys (`advance_time`, `spawn_mobs`...). This template always uses `Registry.GAME_RULE.get(NamespacedKey.minecraft(key))`, which is identical in both versions and does not depend on the old constants; a key that cannot be found only logs a warning and does not make world creation fail
- No deprecated API: `ChunkGenerator#shouldGenerateBedrock()` (no effect since 1.19.2), `WorldCreator#keepSpawnLoaded(TriState)` (no effect since 1.21.9, marked for removal) and the `Block#getBlockKey` family (only encodes y -512..511) are not used; `ChangeRecorder` packs its own block keys
- **World storage (verified on a running Paper 26.3 server)**: 26.x stores every world created with `WorldCreator` as a dimension of the main world, `<main world>/dimensions/minecraft/<name>/`, with no `level.dat` of its own and the world UUID in `data/paper/metadata.dat`; 1.21.11 uses `<world container>/<name>/` with `level.dat` and `uid.dat`. `WorldFolders.dataRoot` picks the right parent, so the template runs unchanged on both. Templates are not portable between the two layouts
- **Spigot**: Paper only — uses `Entity#teleportAsync` and Paper's world storage layout

## Triggers

- 「拋棄式世界」「臨時世界」「競技場重置」「arena reset」「disposable world」「temporary world」
- 「WorldCreator」「複製世界模板」「copy world folder」「unloadWorld」「刪除世界資料夾」
- 「虛空世界」「void generator」「ChunkGenerator」「遊戲規則」「GameRule」
- 「還原方塊」「baseline」「changed blocks」「殘留實體」「掉落物清理」

## Inputs

| Parameter | Example | Description |
|------|------|------|
| `base_package` | `com.example.arena` | Package the template lives in |
| `name_prefix` | `arena_` | World folder prefix (**reserved for this mechanism; do not share it with real worlds**) |
| `template_folder` | `plugins/Arena/templates/duel_map` | Template: a copy of an arena's data folder (`World#getWorldPath()`) saved on the **same** MC version (contains `region/`) |
| `pool_size` | `2` | Number of idle worlds to pre-generate |
| `reset_mode` | `swap` / `in-place` | World swapping, or in-place reset |
| `blocks_per_tick` / `nanos_per_tick` | `2000` / `2_000_000` | Per-tick block count and time budget for in-place reset |

## Outputs

- `VoidChunkGenerator.java` - chunk generator that generates nothing
- `ArenaNames.java` - serial naming (reuses numbers, skips ones in use)
- `ArenaRules.java` - game rules applied right after creation
- `WorldFolders.java` - data-folder location per version, copy template (skips the world UUID file and `session.lock`, atomic rename), delete (rename first)
- `DisposableWorlds.java` - main flow for create / copy / unload / delete
- `ArenaPool.java` - pre-generated world pool
- `ChangeRecorder.java` - records changed blocks (baseline map)
- `ArenaResetService.java` - budgeted batch restore
- `DebrisSweeper.java` - leftover entity sweep (sweep everything on reset / periodic sweep)
- `ArenaPlugin.java` - wiring and lifecycle

## Build Setup

See [`references/paper-api-platform.md`](references/paper-api-platform.md). Only `paper-api` is needed:

```groovy
dependencies {
    compileOnly 'io.papermc.paper:paper-api:26.3.build.258-stable' // 1.21.11: '1.21.11-R0.1-SNAPSHOT'
}
```

## Code Template

The full source lives in [`template.md`](template.md) (about 1,150 lines, compiled against Paper 1.21.11 and 26.3 in CI). **Read `template.md` before writing any code for this skill**, and copy from it instead of rebuilding the classes from the table below.

| File | Package | Role |
|------|---------|------|
| `VoidChunkGenerator.java` | root | Void chunk generator (nothing generated) |
| `ArenaNames.java` | root | Serial arena world names (`arena_1` …) |
| `ArenaRules.java` | root | Difficulty and game rules (by registry key) applied right after creation |
| `WorldFolders.java` | root | Template copy, world folder deletion, world detection |
| `DisposableWorlds.java` | root | Create and destroy disposable worlds |
| `ArenaPool.java` | root | Pool of pre-generated idle worlds |
| `ChangeRecorder.java` | root | Records each changed block's original `BlockData` |
| `DebrisSweeper.java` | root | Removes leftover entities (items, arrows, TNT minecarts) |
| `ArenaResetService.java` | root | In-place reset within a per-tick budget, then sweep |
| `ArenaPlugin.java` | root | Wiring and limits (pool size, per-tick budget) |

## Recommended Directory Structure

```
src/main/java/com/example/arena/
├── ArenaPlugin.java
├── world/                       ← world swapping route
│   ├── DisposableWorlds.java
│   ├── ArenaPool.java
│   ├── ArenaNames.java
│   ├── ArenaRules.java
│   ├── WorldFolders.java        ← the only class doing blocking file IO
│   └── VoidChunkGenerator.java
└── reset/                       ← in-place reset route
    ├── ChangeRecorder.java
    ├── ArenaResetService.java
    └── DebrisSweeper.java
plugins/Arena/templates/duel_map/   ← template = copy of an arena's data folder from the same version (region/, data/ ...)
```

(The templates in `template.md` all sit in `com.example.arena` so each file compiles on its own; a real project can split packages following this structure.)

## Choosing a Route

| | World swapping (copy + unload + delete) | In-place reset (record + restore) |
|---|---|---|
| Best for | Large-scale destruction, important block entity contents, large arenas | Small arenas, limited destruction, rapid back-to-back matches |
| Cost per match | Copy a folder (can be hidden by pre-generation) | Proportional to the number of changed cells |
| Restore completeness | Complete (including chest contents and chunk entities) | Restores block types only; container contents, sign text, and heads need separate handling |
| Risk | Disk space, Windows file locks | Change sources that go unrecorded (see Fallback) |
| Overflow handling | - | `overflowed` -> fall back to world swapping |

The two routes can be combined: normally reset in place, and when `ChangeRecorder.overflowed(world)` is true, destroy the world and take a fresh one from the pool.

## NMS Fast Path

The bottleneck of in-place reset is the Bukkit wrapper and lighting update that `Block#setBlockData` incurs per cell. For very large cell counts (hundreds of thousands), write `LevelChunk` / `LevelChunkSection` directly, then recompute lighting and notify clients in one pass; see [`nms-chunk-access`](../../nms/nms-chunk-access/SKILL.md). The Paper API version is enough for most minigames; do not introduce Paperweight up front just because it "might get large".

## Thread Safety

| Operation | Thread |
|------|-------|
| `WorldCreator.createWorld()`, `unloadWorld`, `setGameRule`, `teleportAsync` calls | **Main thread** |
| `getBlockAt` / `setBlockData` / `getEntitiesByClasses` / `remove()` | **Main thread** |
| `ChangeRecorder` events and `drain` | Main thread (fields need no locks) |
| `WorldFolders.copyTemplate` / `deleteWorld` | **Async** (blocking IO); `closeAllSync` is the exception at shutdown |
| `teleportAsync` completion callback | Main thread (guaranteed by Paper), but still re-validate that the world exists |

- Async lambdas carry only `Path` / `String`, never `World` or `Player`
- Returned futures always complete on the main thread, so callers can touch Bukkit objects directly
- At `onDisable` the scheduler no longer accepts new tasks: finish up synchronously with `closeAllSync()`, and do not `runTask` again
- See [`references/paper-threading.md`](references/paper-threading.md)

## Fallback

| Error | Cause | Fix |
|------|------|------|
| World becomes an empty new map, or an old match's blocks reappear | `createWorld` generated over an incomplete folder, or loaded stale data left by a crash | `requireFresh` refuses when data for the name exists under `WorldFolders.dataRoot`; `purgeStaleAsync` clears it at startup |
| Debris folder is loaded as a world | A copy or delete was interrupted under the real name | Copy to `.copying` then rename; rename to `.deleting` before deleting; `purgeStaleAsync` removes the suffixed debris |
| Two worlds with the same UUID / `session.lock` error | The template's UUID file (26.x `data/paper/metadata.dat`, 1.21.11 `uid.dat`) or `session.lock` was copied | The `SKIP` set in `WorldFolders` |
| On 26.x stale arenas are never cleaned and templates are rejected | Code built paths from `getWorldContainer()`; 26.x keeps every world under `<main world>/dimensions/minecraft/` and has no per-world `level.dat` | Resolve paths with `WorldFolders.dataRoot` / `World#getWorldPath()`; validate templates by `region/` |
| A legacy world folder dropped into the server root disappears on 26.x | Paper imports a `<container>/<name>` folder that has `level.dat` into `dimensions/` on `createWorld`, then deletes the original | Build 26.x templates from a 26.x arena's `getWorldPath()`; do not reuse 1.21.11 templates |
| Terrain turns vanilla after loading a copied world | The custom generator is not saved with the world | Pass `generator(...)` on every load |
| `unloadWorld` returns false | The world still has players, or it is the default world | `teleportAsync` them away first and confirm `getPlayers().isEmpty()`; never unload `getWorlds().get(0)` |
| Deleting a folder throws `AccessDeniedException` on Windows | Region files were just unloaded and the file lock is not yet released | Retry the delete after a few seconds' delay; `purgeStaleAsync` at startup cleans up the rest |
| `All N arena names are in use` | Worlds were not destroyed (leak) | Check that every end path calls `destroy`; raise `max` |
| Game rules not taking effect / log warns unknown rule | Key renamed between versions | Verify keys by listing them with `javap` or `Registry.GAME_RULE`; the old constants are deprecated, do not use them |
| Some blocks still missed after restore | A change source not covered by events (command blocks, other plugins changing blocks directly) | Other plugins' changes do not fire events -> switch that arena to world swapping; or additionally scan the region and compare against the baseline |
| Chest / shulker box contents are empty after restore | The baseline records only `BlockData` | When container contents matter, use world swapping, or additionally record `TileState` snapshots |
| Restore makes the server lag | Budget too large | Lower `maxBlocksPerTick` / `maxNanosPerTick`; for huge arenas use `nms-chunk-access` |
| Leftover arrows, TNT minecarts, dropped items | Entities are not blocks | `DebrisSweeper.sweepAll` on reset; `sweepStale` periodically during a match |
