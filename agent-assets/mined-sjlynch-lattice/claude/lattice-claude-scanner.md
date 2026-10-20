# backend/src/scanner

Pipeline that turns a project root into the `{nodes, links}` graph used by
the 3D force-directed view and the health overlays. No facade: import the phase
module you need (`scanner/scan.ts` is the entry point).

## Phases

A scan runs through these phases, in order — each produces the input for
the next:

1. **`ignore.ts`** — `loadGitignore(root)` builds an `ignore` matcher
   that combines `IGNORE_DIR_NAMES`, the root `.gitignore`, and
   common-gitdir `info/exclude` (`readInfoExclude`; resolved through a linked
   worktree's `commondir`). `info/exclude` is where Lattice records its own
   managed files, so the scan honours it as git does.
2. **`collectSourceTree.ts`** — `collectSourceTree(root, ig)` walks the
   tree gitignore-aware and returns `{files, directories}` (every
   directory crossed, plus every file whose extension is in
   `SOURCE_EXTS`). `collectSourceFiles` is the files-only shortcut.
3. **`fileMetrics.ts`** — `computeFileMetrics(files, {cache, isCancelled})`
   runs three passes: (1) main-thread stat + `(mtime,size)` cache/memo lookup;
   (2) misses analyzed in an **isolated worker thread** via
   `healthWorkerRunner.ts`; (3) in-thread `readForAnalysis` + `analyzeFile`
   fallback for **only the returned `unhandled` tail**. Returns `FileMetric[]`
   in input order for the next two phases.
   - **`readForAnalysis.ts`** — single-file read + LOC count + minified/
     oversize content-drop guard (`isMinifiedForAnalysis`, shared with the
     watcher). Each job carries its stat'd `size`, so a file over
     `LOC_MAX_BYTES` is never read (the post-read length check stays as a
     backstop for a file that grew; the watcher's `readFileForAnalysis` does
     the same with `stat.size`). The worker imports this + `analyze.js`;
     `fileMetrics.ts` re-exports it for back-compat.
   - **Worker loading/fallback** — `runHealthAnalysis(jobs, {onResult, …})`
     spawns an inline-eval worker that dynamic-imports compiled `analyze.js` +
     `readForAnalysis.js` by URL, without inheriting a TS loader. Under tsx/`src`
     the `.js` siblings may be absent: initialization failure returns jobs as
     `unhandled`. Worker construction failure, unexpected death or respawn-budget
     exhaustion likewise returns the unprocessed tail for in-thread fallback.
     Worker factory + `moduleUrls` are injectable test seams.
   - **Worker program** — [healthWorkerSource.ts](healthWorkerSource.ts) holds
     the scan's eval source and message protocol; `healthWorkerRunner.ts` remains
     the parent resource owner.
   - **Handled outcomes/watchdog** — completed `analysis: null` results are
     failed/skipped analyses, excluded from fallback. The per-file stall watchdog
     (default 10 s, reset on each completed file) terminates the worker, reports
     the culprit as `analysis: null`, skips it and excludes it from `unhandled`;
     remaining jobs continue on a fresh worker within the respawn budget.
   - **Ownership/teardown** — each `HealthAnalysisRun` owns its current batch
     worker, watchdog and optional cancellation poll. `finish()` settles once,
     clears both timers and terminates the worker; callbacks from stale workers
     are fenced by worker identity. Cancellation also terminates the worker and
     returns its unprocessed tail, but `computeFileMetrics` rechecks cancellation
     and throws before fallback. The worker and watchdog are not unref'd while
     the scan awaits them, and the worker is not kept for process lifetime.
     Spawn/terminate/timer primitives are shared via
     [../health/analysisWorker.ts](../health/analysisWorker.ts); the shared warm
     analyzer's lifetime and policy belong to the
     [health/watcher guide](../health/watcher/CLAUDE.md).
   - **Negative memo** — module-level `unanalyzable` retains absolute-path keys
     with only mtime/size/optional LOC metadata for stat'd failed/skipped analyses.
     An unchanged tuple avoids repeat reads/analysis; a changed tuple triggers
     another attempt without itself deleting the old entry. A failed/skipped
     result replaces that metadata; successful analysis removes the entry.
     This process-lifetime negative memo is separate from the positive persistent
     `HealthCache`, with no eviction cap or per-scan reset.
4. **`coupling.ts`** — `computeCoupling(metrics, aliases, roots)` feeds the
   per-file `imports` lists into `computeCrossFile` to produce the
   cross-file `CouplingMap` (fan-in/fan-out plus dead-code reachability from
   the entry-point `roots` `scan.ts` computes via `detectRoots`).
5. **`graphAggregate.ts`** — `aggregate(metrics, coupling, {root,
   directories})` applies cross-file numbers back onto each file's
   `HealthMetrics` and emits the final `{root, nodes, links}` graph.
   `commonRoot` is the fallback when no explicit root is passed;
   `ensureDirectoryNode` lazily seeds intermediate directory nodes for
   any file whose parent wasn't in the walked directory list.
6. **`scan.ts`** — `scan(root)` captures a watcher publication ticket before
   its first await. It clones the live watcher cache when available (including
   edits whose disk save is still debounced), runs the phases above, prunes,
   and commits only if no event, newer scan, or watcher creation intervened.
   Accepted scans seed the existing watcher/cache owner; persistence remains
   fire-and-forget. Cancellation is checked during tree collection, per-file
   work, and before publication.
7. **`coordinator.ts`** — HTTP callers share one in-flight scan per canonical
   project and watcher revision. Cancellation releases only that subscriber;
   the last disconnect cancels and evicts the underlying scan immediately.
   New callers never join cancelled work, and settled results are not cached.

## Conventions

- Output shape is stable — `scan()` must keep returning the same
  `{root, nodes, links}` graph the frontend already consumes.
- Cache writes (`HealthCache.save`) are best-effort and non-blocking;
  never `await` them in the scan response path.
- Phase boundaries are the seams: a new metric → extend
  `fileMetrics.ts`; a new cross-file signal → extend `coupling.ts`; a
  new graph shape → extend `graphAggregate.ts`. Don't reach across.

## Reference checks

Existing contracts: [scannerFileMetrics.test.ts](../__tests__/scannerFileMetrics.test.ts)
(negative memo/LOC/re-attempt) and
[scannerHealthWorkerRunner.test.ts](../__tests__/scannerHealthWorkerRunner.test.ts)
(watchdog, fallback, cancellation and termination).

Backend reference commands (cwd `backend/`): `npm run build`, `npm test`,
`npx tsc --noEmit`.
