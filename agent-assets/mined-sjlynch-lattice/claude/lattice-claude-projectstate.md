# projectState helpers

Keep [../projectStateManager.ts](../projectStateManager.ts) as the public import
surface (it re-exports `flushAllProjectStatePersists`); these helpers are
private. The manager owns canonical cache keys, single-flight loads,
per-project write locks and subscriber coalescing/isolation, and composes the
helpers below, passing them already-canonical keys and callbacks bound to its
own (overridable) `runProjectWrite` / `writeStateNow`. Domain stores own
validation, mutation semantics and the strategy for loading known projects.

- **Disk preservation** ([diskPersistence.ts](./diskPersistence.ts)): among read
  failures, only `ENOENT` creates default state. Other failures propagate and
  leave the project unloaded; never cache unread data as an empty store.
  A parse/deserialization exception preserves the original bytes to a
  `.corrupt-*` sidecar (rename first, copy of the read contents as fallback),
  then returns defaults. If preservation fails, the manager marks that project
  write-protected until restart after manual recovery. Both async and sync
  writers must refuse to overwrite it.
- **Publication**: both writers use temp-to-rename publication so readers see
  a complete old or new file. The async writer delegates to `atomicWriteFile`
  with Windows rename retries. The synchronous exit writer cannot await those
  retries; a locked target fails, cleans up its temp, and is logged by the
  manager's exit flush.
- **Lookup and mutation** ([listLookup.ts](./listLookup.ts)): read-only
  cross-project lookup is unlocked; it scans cache, invokes the caller's
  load-known-projects fallback on a miss, then scans again. Mutations use
  `withLockedItemAcrossProjects`: resolve the project, acquire its write lock,
  then re-find the item in the live cache. Never mutate a pre-lock list/index;
  the item may have changed or vanished while waiting (return `null` if gone).
  Canonicalization and lock ownership stay with the manager/caller; the helper
  consumes supplied callbacks. `runProjectWrite` is an in-process lock keyed by
  store name plus canonical project. See the task store's
  [crash-safety contract](../taskCache/CLAUDE.md#crash-safety-contract) for
  disk-before-cache updates.
- **Persist scheduling** ([persistScheduler.ts](./persistScheduler.ts)):
  `PersistScheduler` owns the debounce timers (the manager's protected
  `persistTimers` map, shared), dirty generations, `persistLatest` and the
  synchronous exit write. The manager's `schedulePersist`,
  `cancelPendingPersist`, `flushPersist`, `flushAllPendingPersists` and
  `flushPendingPersistsSync` keep their signatures and delegate; `flushPersist`
  still cancels through the manager's `cancelPendingPersist`.
- **Exit-flush registry** ([exitFlush.ts](./exitFlush.ts)): the once-only
  process `exit` hook over schedulers with pending persists (tracked only for
  `flushOnExit` stores), and the weakly held set of every store behind
  `flushAllProjectStatePersists`.
- **Load/flush lifetime**: concurrent cold reads share the manager's load
  promise; mark loaded only after populating cache. A fired debounce timer does
  **not** mean its disk write completed. Dirty generations remain until a
  successful write of that generation finishes; a newer mutation stays dirty.
  `flushOnExit` is opt-in only for stores whose disk shape equals cached state
  and which do not override `writeStateNow` (the sync path bypasses it).
  Restart drain explicitly awaits `flushAllProjectStatePersists`, including
  pending/in-flight writes, because Windows termination skips exit handlers;
  see [restart-drain guidance](../restartDrain/CLAUDE.md#protocol).

Existing behavior coverage:
[projectStateManager.test.ts](../__tests__/projectStateManager.test.ts) and
[projectStateNotifyCoalesce.test.ts](../__tests__/projectStateNotifyCoalesce.test.ts).
Reference commands, with `backend/` as cwd (documentation only; task agents
must not execute tests, builds or type-checks):

```sh
npm run build
npm test
npx tsc --noEmit
```
