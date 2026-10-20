# Backend dev-runner helpers

[../dev.mjs](../dev.mjs) wires boot: self-heal deps → initial compile/assets → start
`dist/index.js` → arm dist/dependency watches and `tsc -w` → supervise → shutdown.
The user owns dev-server operation; agents must not start, stop or restart it.
Preserve exported APIs/types, exact logs, startup behavior and async error paths.
Sibling `.d.mts` files, where present, mirror helper contracts for TypeScript consumers.

## Process and resource ownership

The runner owns backend/compiler children, dist/dependency watches and supervision timers.
The compiler owns its program/source watches; the detached terminal-server owns PTYs/native resources.
Close handles/pipes and cancel timers with their owner. Track Node/native memory by process;
see the [frontend guide for browser OOM](../../../frontend/README.md#browser-memory-troubleshooting).

## Boot, compilation and backend recovery

- [deps.mjs](deps.mjs) checks every declared dependency against its lockfile, sharing root preflight's manifest-driven checks.
- [compileAssets.mjs](compileAssets.mjs) runs initial compile/copy; either failure aborts boot.
  Attempt [asset copying](../copy-assets.mjs) before every spawn (warn/continue on respawn failure); re-export `startTscWatch`.
- [compilerLifecycle.mjs](compilerLifecycle.mjs) repairs only the compiler: retries 1/2/5/10/30 s,
  then visibly pauses compilation while retaining app/PTYs. Automatic retries reset only after
  five minutes following successful compilation, not one success line. Dependency repair
  restarts/resumes with a fresh budget and expected old exit, spending no retry. Live-child
  operation errors keep that child tracked; never admit two compilers writing `dist/`.
- [tscWatch.mjs](tscWatch.mjs) parses English, non-pretty status with anchored lines/localized clocks.
  Compile start/errors/death/repair fence all restarts and polls; only zero errors opens the gate.
  Bound stdout/stderr diagnostics with PID, Node/platform and decoded exit; record on `close`
  (1 s fallback), repair on `exit`. Recovery uses source `dynamicPriorityPolling`; Windows recursive
  directory watches stay native. This does not identify the failure's cause.
- [backendLifecycle.mjs](backendLifecycle.mjs) tracks spawn/error/exit and kill. Unexpected
  exits back off 2/5/10/30/60 seconds, then every 60 seconds; reset after five minutes uptime.
  Permitted dist changes retry sooner. Timers re-check shutdown, current child and compiler gate.
  Successful compiles can start a missing backend; observe spawn failures, retain children after
  failed kills and unref crash-respawn timers.
- Post-boot [deps watch](../../../scripts/depsWatch.mjs) is wired in [dev.mjs](../dev.mjs).
  Failed installs log and wait for file changes or forced `deps-recheck` (`i`). After success, replace
  the compiler, then force restart on its next successful compile even for identical bytes; locks still defer.

Regression owners: [depsCheck](../../src/__tests__/depsCheck.test.ts), [depsWatch](../../src/__tests__/depsWatch.test.ts),
[compiler lifecycle](../../src/__tests__/devCompilerLifecycle.test.ts), [dependency restart](../../src/__tests__/devCompilerRestart.test.ts),
[tsc watch](../../src/__tests__/devTscWatch.test.ts), [backend lifecycle](../../src/__tests__/devBackendLifecycle.test.ts).

## Restart admission and output versions

- [restartPolicy.mjs](restartPolicy.mjs) owns live-run.lock deferral, 250 ms debounce, 3 s poll and
  compile gating. Idle polls skip lock scans; stop clears both timers and fences callbacks. Keep runLocks re-exports.
- [restartOutputState.mjs](restartOutputState.mjs) owns per-policy output baselines and compile
  sequences. Policy owns admission: successful compiles catch up missed events/downtime;
  identical completed bytes clear obsolete deferrals.
- [distSignature.mjs](distSignature.mjs) checks file AND directory mtimes (create/delete counts);
  unreadable output is unknown and fails open. Hash only at completed compile/baseline/spawn
  boundaries, never per metadata event or idle poll. Capture version after asset copy, before
  spawn; commit only on actual `spawn`, never an accepted kill or a later partial-output read.
  Compile-sequence catch-up handles newer output; spawn generation fences stale drain decisions.
- [distWatcher.mjs](distWatcher.mjs) uses recursive `fs.watch` with chokidar fallback;
  handle construction/runtime errors and close failures. Forward event type/filename.
  Metadata-only events must neither restart nor arm deferral; preserve attributable logs.

Regression owners: [dist verification](../../src/__tests__/distRestartVerify.test.ts), [dist watcher](../../src/__tests__/devDistWatcher.test.ts),
[compiler recovery integration](../../src/__tests__/devCompilerRecoveryIntegration.test.ts).

## Locks and drain decisions

- [runLocks.mjs](runLocks.mjs) scans home per-project locks using `node:` builtins, never dist.
  Ignore foreign-host/dead/provably recycled PIDs; unknown OS start time counts alive. Compare
  to lock `startedAt` (1 s slack); cache per `(pid, startedAt, ownerId)`, avoiding repeat probes; evict vanished keys.
- Workflow locks (`workflow-*`, including Run tests) defer indefinitely. The 15-minute
  backstop targets wedged, re-runnable merge/manual-merge holders. Hold when EVERY lock
  matches the backend PID and its report says parked on a live resolver/post-merge agent;
  unavailable/non-parked reports permit force. Agent steps hold no lock; persisted runs/PTYs
  are re-adopted. Logs name hash, label, PID and lock start time.
- [parkedProbe.mjs](parkedProbe.mjs) owns per-policy single-flight queries/exact sorted lock-set
  keys; freshness starts on answer arrival (60 s TTL), refreshed at half TTL during holds.
- [restartHandshake.mjs](restartHandshake.mjs) asks the backend to pause spawn/run-lock admission
  in a TTL drain (skip if no backend). Settle 5 s after locks clear; wait ≤45 s for transitions, then flush state.
  A lock acquired during drain re-defers; cancel on that race, compile fencing, changed spawn
  generation or refused restart. Cancel is best effort; TTL releases lost drains.
  Missing token, unreachable backend, 404, timeout or not-ready fails open. Handshake and terminal
  `/shutdown` read existing `~/.lattice/terminalServerToken` for `x-lattice-terminal-token`;
  never create/rotate it. Backend routes reject browser Origin.

Regression owners: [deferral/liveness](../../src/__tests__/restartPolicyDefer.test.ts), [handshake/parked/output races](../../src/__tests__/devRestartHandshake.test.ts).
Backend owners: [restart drain](../../src/restartDrain/CLAUDE.md), [run locks](../../src/projectRunLock/CLAUDE.md).

## Stop and diagnostic retention

[devShutdown.mjs](devShutdown.mjs) shares one stop: mark shutdown, close dist/deps watches,
stop restart timers/compiler repairs, then kill backend (cancelling crash respawn). Soft `r`/`d`
stops drain first (10 s settle/15 s request), preserve terminal-server/PTYs and skip lock re-check
(orchestrator admitted it). Real SIGINT/SIGTERM skips drain, requests terminal `/shutdown` once,
and interrupts a soft drain. Delete stdin-control env marker before inheritance. `onExit` waits
for shutdown/terminal termination; never call full-stop `shutdown()` there. With no backend child,
exit explicitly. Shutdown wins over pending spawns/repairs/callbacks.

[exitStatus.mjs](exitStatus.mjs) decodes child exits for `~/.lattice/logs/dev-runner.log`; this runner
records backend deaths invisible to the outer supervisor. Unsigned `4294967295` is exit -1, not
proof of a native fault. [liveLog.mjs](liveLog.mjs) removes mirrors for requested kills/clean exits;
retain unexpected nonzero/signal exits for [no-JS crash adoption](../../src/crashLog/CLAUDE.md).
Regression owners: [shutdown](../../src/__tests__/devShutdown.test.ts), [control](../../src/__tests__/devControl.test.ts), [exit status](../../src/__tests__/devExitStatus.test.ts).
