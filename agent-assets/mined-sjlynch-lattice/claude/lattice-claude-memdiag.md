# memDiag — memory debug output

Periodic, low-noise memory sampling for the three long-lived processes, built
to catch leaks that only show up after hours. Read this before adding a cache,
registry, listener set or GPU resource that lives longer than a request.

## What the user sees

Every `LATTICE_MEM_LOG_MS` (default 5 min, first sample after 1 min, `0`
disables) the `npm run dev` console gets one line per process:

```
[mem] backend up 5h12m · rss 219MB (+38MB) · heap 102MB/140MB · ext 9MB (buffers 2MB) · handles 61 (TCPSocketWrap 30, Timeout 18, FSEventWrap 6) · executor rss 280MB, ptys 12, pty threads 12 · grew since start: tasks.loadedTasks +40 · RISING: watch.paths 9000→15000
[mem] browser#k3x9 up 2h04m · js heap 312MB/400MB (limit 4096MB) · dom 8200 · gl geo 1200 · gl tex 340 · xterm 7 · ws 11 · hmr 23
```

- `grew since start` — the gauges that grew most since the process's first sample.
- `RISING:` — a metric that never decreased across the last 6 samples (~30 min)
  and grew meaningfully (bytes: ≥ max(8 MB, 10%); counts: ≥ max(4, 20%)). GC
  saw-tooth never qualifies; this is the leak-shaped signal.
- Full samples (every gauge) append to `~/.lattice/logs/mem-<label>.jsonl`
  (`backend`, `terminal-server`, `browser`; rotated to `.prev.jsonl` at 2 MB).
  Diff hours of them after the fact.
- `GET /api/debug/memory` — everything right now (incl. V8 heap spaces and the
  last sample from each browser tab). `POST /api/debug/heap-snapshot` writes a
  `.heapsnapshot` to `~/.lattice/logs/` (newest 4 kept; blocks the backend for
  seconds) — take two, load both in Chrome DevTools → Memory → Comparison.
- Browser: `window.__latticeMem()` prints every gauge (`console.table`);
  `localStorage['lattice.debug.memLogMs']` sets that tab's cadence (`'0'` off).

## Files

- `../memDiag.ts` — facade: `startMemDiag(label)`, `registerMemGauge`,
  `registerMemProbe` (async, prefixed gauges — the backend's `executor.*`),
  `memDiagReport`. Imported by the terminal-server, so it must stay free of
  backend-only imports.
- `gauges.ts` — the registry. Dependency-free (fingerprinted executor code
  imports it). A throwing / non-finite reader reports `-1`.
- `sample.ts` — `process.memoryUsage()` + `getActiveResourcesInfo()` by type +
  gauges; `sampleSeries` flattens to `mem.*` / `handles.*` / gauge names.
- `trend.ts` — `MemTrend` (the `RISING` rule). `format.ts` — the line.
- `logFile.ts` — JSONL append + rotation. `heapSnapshot.ts` — on-demand snapshot.
- `browser.ts` — `POST /api/debug/client-memory` parse/trend/print (backend-only;
  at most 8 tabs tracked). The browser half is `frontend/src/debug/memDiag.ts`.
- `executorProbe.ts` — reads the terminal-server's authed `GET /memory`
  (its stdio is ignored, so its own line only reaches its crash ring/live
  mirror and `mem-terminal-server.jsonl`).

## Adding a gauge (do this for every long-lived collection)

Register beside the collection, at module scope:
`registerMemGauge('area.thing', () => things.size)`. Rules:

- O(1)-cheap, side-effect free; a sum over a bounded set is fine at a 5-min
  cadence, a walk of a whole project tree is not.
- Every `createEmitter` (../emitter.ts) already reports `listeners.<label>`;
  a subscriber count that only climbs is a subscription leak.
- Name byte-valued gauges with a `mem.` segment (`ws.mem.buffered`,
  `terminal.mem.scrollback`) — the formatter and trend thresholds key off it.
- Per-instance resources (a graph renderer, a store instance) return/keep the
  unregister and call it at teardown (frontend `registerMemGauge` returns it).
- Executor-side gauges go in fingerprinted files; add any new executor import
  to `../terminalFingerprint.ts` `FINGERPRINT_FILES`.

## Known memory facts (keep current)

- Every pty costs ~10–12 MB of executor RSS that `heapUsed` never shows: node-pty
  (`useConptyDll`) runs one conout Worker thread per pty. node-pty itself never
  stops that thread; `../terminal/conoutWorker.ts` does, on exit.
  `executor.terminal.conoutWorkers` must track `executor.terminal.sessions`.
- Every known project's task board is resident from boot (recovery's
  `loadAllKnown`) and never evicted, done/deleted tasks included
  (`tasks.loadedProjects`, `tasks.loadedTasks`) — a fixed cost that grows with
  history, not a leak.
- Browser: each mounted terminal pane holds a 20 000-line xterm buffer; at most
  `MAX_BACKGROUND_PANES` hidden panes stay mounted
  (`frontend/src/components/sidebar/hooks/useMountedTerminalIds.ts`). In-use
  Alt name labels are capped at `MAX_NAME_LABELS`.
- The Lattice tab runs the Vite dev build and hot-swaps modules on every merge;
  ES module records are never freed (`vite.hmrUpdates` — a full reload resets).

Tests: `../__tests__/memDiag.test.ts`.
