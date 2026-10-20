# watchTree

`../watchTree.ts` is the stable public factory and type re-export. It selects
native recursive watching on Windows and chokidar elsewhere; exact
`LATTICE_WATCH_MODE=recursive` / `chokidar` overrides take precedence.

- `types.ts` — the chokidar-shaped public contract and internal snapshot entry.
- `constants.ts` — debounce, write stability, retry limit, chokidar poll interval,
  and the case-insensitive-platform flag. Keep the existing values.
- `recursiveWatcher.ts` — OS handle, traversal, event emission, queues, retries,
  timers, and close/error lifecycle. One native handle on the root avoids
  locking Windows descendants against rename/delete.
- `snapshot.ts` — synchronous file/directory bookkeeping and subtree ordering;
  no filesystem calls, events, timers, or watcher-private state.

## Lifecycle boundaries

- Arm the OS watch before seeding. Queue events during the seed and defer
  flushes until it finishes; pre-seed paths force a change when visited.
- Seed walks insert missing entries silently and leave existing entries alone.
  Live walks may update/emit changes. Visits alone apply write-stability retries
  (bounded at 20) and check unchanged paths for stale case spelling. A removal
  drops the path's retry count even when it was never recorded (a short-lived
  `.git/**/*.lock` held for stability and gone by the next pass), so `retries`
  can't grow per unique file name.
- Keep rescans and pending visits in the serialized flush. `add()` queues a
  rescan; an event without a filename queues a whole-root rescan.
- Ignore predicates fail open and log once per watcher. Keep raw-event
  prefiltering cheap and do not traverse symlinks.
- Case-only renames remove the old spelling and queue the real spelling.
  Subtree removals emit descendants before parents, ordered by descending path
  length; rescans retain snapshot insertion order.
- The watcher owns error emission (including a default no-op error listener)
  and cleanup. Keep existing async/catch boundaries and close behavior; close
  clears its timer, native handle, pending/rescan queues, snapshot, retry
  counts and pre-seed set.

Existing behavior coverage stays in `../__tests__/watchTree.test.ts` and the
health/git-status consumer tests. Callers continue importing `../watchTree.js`.
