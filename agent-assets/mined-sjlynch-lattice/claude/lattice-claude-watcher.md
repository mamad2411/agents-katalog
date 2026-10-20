# backend/src/health/watcher

Per-project health watcher construction, event analysis, and scan publication.
[../watcher.ts](../watcher.ts) owns canonical-root singleton slots, in-flight
`ensureWatcher` promise memoization (failed builds are evicted), the public API
(`subscribeHealth`, `beginWatcherScan`, `watcherScanRevision`, `HealthUpdate`,
test helpers), and shutdown cache flushing. [../../watchTree.ts](../../watchTree.ts)
owns the filesystem backend: recursive `fs.watch` on win32 and chokidar
elsewhere by default, exposing the same tree events.

## Lifetime (memory invariant)

Per-project watchers are never closed. The `subscribeHealth` unsubscribe only
removes the callback from `subscribers`; only `_resetWatchersForTest` calls
`watcher.close()`. Every project opened in a backend process therefore keeps,
for the life of that process:

- the tree watcher's state — on win32 a `RecursiveTreeWatcher` snapshot of
  every non-ignored path ([../../watchTree/recursiveWatcher.ts](../../watchTree/recursiveWatcher.ts));
- the per-file `metrics` and `imports` maps;
- a full `HealthCache`.

There is no eviction on project switch or last unsubscribe. Any per-file state
added here grows with every file in every project ever opened in the process.

## Module map

| File | Responsibility |
| --- | --- |
| `setup.ts` | `createWatcher`: cache/config/root inputs, cross-file analyzer, tree watcher and event wiring; receives the facade's shutdown-hook registrar. |
| `cacheHydration.ts` | Seed imports/metrics maps from cache so the first event has the existing graph context. |
| `handlers.ts` | Stamp add/change/unlink events, reload config, publish guarded file results/removals, schedule cross-file work. |
| `fileAnalysis.ts` | Stat/cache lookup, gated reads, LOC count, source decoding, isolated analysis/fallback, guarded cache writes. |
| `subscribers.ts` | `broadcast`: isolate each subscriber's exception so fan-out continues. |
| `revision.ts` | `WatcherRevision`: per-path publication tokens and project-wide scan revision/pending-event tracking. |
| `scanPublication.ts` | `ScanPublication`: capture scan ownership, copy live cache, conditionally seed watcher maps/cache/root inputs. |
| `isolatedAnalyze.ts` | Shared warm `IsolatedAnalyzer`, serial job queue, stall watchdog, failure/cooldown policy and disposal. |
| `types.ts` | `ProjectWatcher`, `Subscriber`; re-exports the `HealthUpdate` union (`updated`, `removed`, `rescan`), declared node-free in `../types.ts` for the frontend. |

## Event and scan flow

Tree event → revision stamp → guarded config/file analysis → maps/cache →
[../crossFileAnalyzer.ts](../crossFileAnalyzer.ts) recomputation → subscribers.
Add/change schedules one trailing-edge cross-file pass (150 ms); originators
and other files whose cross-file fields changed receive `updated` broadcasts.
Unlink deletes maps/cache, broadcasts `removed`, then schedules recomputation.
New/removed membership invalidates cached roots and the present-file set;
content-only edits preserve those memoized identities.

[../../scanner/scan.ts](../../scanner/scan.ts) calls `beginWatcherScan` before
its first await and calls `finish` in `finally`. `scanPublication.ts` captures
the watcher slot (including absence), revision, and latest-scan token. Commit
requires no cancellation, no newer scan, the same slot, and, when a watcher
exists, a matching revision with no pending events. Recheck after awaiting
creation; a watcher created during a scan must not receive its older snapshot.
A successful commit replaces maps, seeds/prunes the long-lived watcher cache,
invalidates its revision and starts a flush (or flushes the scan cache if no
watcher exists). It hands freshly resolved package.json entry targets and
entry globs to `CrossFileAnalyzer.setRootInputs`, refreshing roots even when
the watcher booted with an empty cache.

## Contracts to preserve

- Stamp events before config/read/analysis awaits; check `isCurrent` after
  asynchronous work and before publishing maps/cache. Finish tokens in
  `finally`. Older work must never resurrect an unlinked file or replace a
  newer edit. `change` forces analysis; only add/initial work may use the cache.
- Directory add/remove invalidates the scan revision synchronously;
  `setup.ts`'s `createDirectoryRescanCoalescer` emits one trailing-edge
  directory `rescan` per 100 ms burst (excluding the project root itself).
- [../configReloader.ts](../configReloader.ts) separately fences ignore/alias
  assignment across async reads. Root `.gitignore`/`tsconfig*` changes trigger
  rescan, watcher re-add and recomputation; nested tsconfigs reload aliases
  and recompute only. Nested `.gitignore` changes are ignored.
- In-progress scans must not share mutable metrics with the watcher or each
  other. Copy the live cache, including unsaved edits: targeted copies of
  `metrics`, its `smells` array, and `imports` protect against in-place analysis.
- Keep `HealthCache.save()` debounced and best-effort; flush on scan commit
  and shutdown. [../cacheFile.ts](../cacheFile.ts) orders reads and writes
  across cache instances, so hydration waits behind an already queued flush.
  A commit that re-seeds unchanged entries leaves the cache clean (no write).
- `fileAnalysis.ts` holds a machine-wide eight-slot gate across file read and
  analyzer hand-off for all projects ([../../concurrencyLimit.ts](../../concurrencyLimit.ts));
  the `(mtime,size)` cache check stays outside it. Keep size/minification guards.
- Reuse one warm worker with one job in flight; its per-file stall watchdog
  skips a hung job and resumes queued work on a fresh worker.
  Shared worker/timer primitives live in [../analysisWorker.ts](../analysisWorker.ts);
  watcher protocol and respawn policy stay in `isolatedAnalyze.ts`.
- Only `WorkerUnavailableError` enables the guarded in-thread `analyzeFile`
  fallback. A `null` analysis/watchdog result skips the file: never retry it
  in-thread, where pathological input could freeze the backend event loop.
- Three spawn failures/unexpected deaths trigger a 60 s cooldown, then retries
  resume. Initialization failure (unloadable compiled `analyze.js`) is permanent.
- Worker and watchdog are unref'd. On SIGINT/SIGTERM the facade disposes the
  analyzer (clear watchdog, terminate worker, reject in-flight/queued jobs),
  then time-boxes cache flushing before exit; `beforeExit` only flushes caches.
