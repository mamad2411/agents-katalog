# backend/src/spawnQueue

Backend-side admission controller for agent spawns. `../spawnQueue.ts` is the
public facade; focused modules live here (mirrors the `mergeRuns.ts` +
`mergeRuns/` convention).

## Why it exists

Under heavy "Run All" / multi-workflow fan-out, agent spawns used to hit the
terminal-server's hard session cap and be **dropped** (a workflow step
errored; tasks silently failed to spawn). The queue replaces that hard
rejection with a durable deferral: a requested spawn either runs now or waits
for a slot — it is never lost. The terminal-server's `MAX_TERMINAL_SESSIONS`
is now only a runaway backstop; the queue's `softCap` is the real governor.

## Modules

- `types.ts` — `SpawnPriority`, `EnqueueSpawnArgs/Result`, `SpawnQueueSnapshot`,
  and `SpawnCapacityError` / `isSpawnCapacityError`. No I/O.
- `config.ts` — `SPAWN_QUEUE_CONFIG`: `priorityReserve`, poll cadence, and a
  boot-only `softCap` placeholder. The effective `softCap` is
  `globalSettings.maxConcurrentAgents`: `startSpawnQueue` (`../spawnQueue.ts`)
  applies it at boot and PATCH `/api/global-settings` updates it live via
  `setSpawnQueueSoftCap`. `LATTICE_MAX_CONCURRENT_AGENTS` only seeds that
  setting's default (24) in `../globalSettings.ts`.
- `accounting.ts` — `SpawnAccounting`: **pure**, no I/O, fully unit-tested
  (`__tests__/spawnQueueAccounting.test.ts`). Owns the headroom bands and the
  poll-reconciliation rule.
- `state.ts` — `SpawnQueueState` + the `queueState` singleton: the request
  registry (dedupe-keyed), pending sort, drain-reentrancy flags.
- `drain.ts` — `drainQueue()`: admit pending spawns while there is headroom,
  run each thunk, fold the outcome back into the accounting.
- `poll.ts` — the `GET /sessions` loop; runs only while the queue has
  pending/reserved work. Reconciles the total session count and the agent
  subset (`countAgentSessions`).

## Contract / invariants

- A spawn is one **thunk** doing the FULL spawn unit (worktree/dir setup +
  exactly one `proxyCreateSession`). Gating the whole unit — not just the pty
  — is what stops "Run All" creating 100 worktrees up front.
- One admitted thunk = one reserved slot. `effectiveLive = liveCount +
  reserved.length`. `batch` admits below `softCap`; `priority`/`interactive`
  may use `softCap + priorityReserve`.
- **Poll reconciliation never over-admits.** On a poll requested at `Treq`,
  drop only reservations that were `spawned` *before* `Treq` — those are
  definitely in the polled count. The safe error direction is a one-cycle
  under-admit.
- **CAP is not a failure.** A terminal-server hard-cap rejection (`code:
  'CAP'`, surfaced as `SpawnCapacityError`) releases the reservation, freezes
  admissions until the next successful poll, and re-queues the request at the
  front of its band. `done` stays pending across CAP retries.
- **Disk space is not a failure either.** A thunk whose worktree would cross
  the free-space reserve throws `SpawnDiskSpaceError` (`worktree/diskSpace.ts`).
  The queue releases the reservation and re-queues the request with a
  per-request backoff (`waitingForDisk.retryAt`, 30 s) — admissions are NOT
  frozen, so spawns that need no new disk (resolvers, resumes) keep flowing.
  `notifyDiskSpaceFreed()` (called by `cleanupWorktreeForTask` after a
  successful `git worktree remove`) cuts every backoff short. Outside the queue,
  `isSpawnDeferral(err)` (CAP or disk) is what `runSpawnThunk` and the workflow
  Start step check, so a disk wait never counts as a failed start. The first
  disk deferral of a task run also asks `diskPressureMerge.ts` to merge the
  project's parked Ready-to-Merge tasks (skipped while a workflow / merge run /
  post-merge hook is active; opt-out `globalSettings.autoMergeOnLowDisk`).
- **The resource governor brakes fan-out under load** (`resourceGovernor.ts`).
  `softCap` is a fixed ceiling; beneath it, `batch` spawns are held while
  smoothed system CPU (≈20 s EWMA from `os.cpus()` deltas, sampled on every
  drain) is ≥ 90% — released below 75% — or free RAM is under max(2 GB, 5%).
  Never below `MIN_LIVE_AGENTS` (2) live **agents**, so outside load can't
  starve Lattice to zero. The floor counts `accounting.effectiveAgents()` —
  sessions whose cwd is under a `.lattice` dir (task worktrees / resolvers,
  workflow steps, push / QA / post-merge scratch; `countAgentSessions`) plus
  the queue's reservations — never raw ptys: sidebar shells, a `npm run dev`
  startup terminal or another project's tabs once held every Run All forever
  on a low-RAM machine with zero agents running. `priority` / `interactive`
  are never held. Held requests just stay pending (the 1.5 s poll re-checks). State is on
  `GET /api/spawn-queue` as `governor`; opt out with
  `globalSettings.resourceGovernor: false`. Added after a 50-agent cap on a
  large repo pinned the CPU at 100% and froze the desktop (2026-09-22).
- **Cancellation reaches in-flight requests.** Every request owns an
  `AbortController` (an `EnqueueSpawnArgs.signal` is forwarded into it) and the
  thunk receives its signal. `cancelSpawn` drops a pending request (returns
  `'pending'`) or aborts an in-flight one (`'in-flight'`); an aborted request
  is never re-queued by a CAP / disk deferral, so a cancelled run cannot come
  back later. A new enqueue for the key of an aborted in-flight request does
  NOT dedupe onto it: the new request takes the key but is not admitted until
  the old thunk settles (`predecessor`), so two thunks for one key never run
  at once; settling is identity-checked (`settle`) so the late one can't
  evict its successor. Task runs pass the signal to `startTaskById`, which
  backs out (worktree + pty torn down) instead of starting a cancelled run.
- **Poll failure freezes admissions.** `proxyListSessionsOrNull()` returns `null`
  (not `0`) when the terminal-server is unreachable; the queue keeps the last
  count and admits nothing until a poll succeeds.
- **A request leaves the queue only through `settle()`** (`state.ts`). A thunk
  that never settles holds its slot forever, keeps the poll loop alive and makes
  every restart drain report `ready:false`. Time-bound every new spawn site's
  thunk; today `createSession`'s 30 s cap is the only bound.
- `drainQueue()` is non-reentrant (`isDraining` / `drainAgain`).
- **A restart drain pauses ALL admission** (`../restartDrain/`, checked at
  the top of `admitWhilePossible`): the dev runner is about to kill the
  process, and a thunk admitted now would die half-way. Pending requests stay
  pending (task runs / workflow steps are durable across the restart; the
  awaited kinds fail with the process like any restart). `batchAdmissionHold`
  reports the hold too. The drain's end (cancel / TTL) re-drains via
  `onRestartDrainEnded` in `../spawnQueue.ts`. The restart handshake's settle
  waits for the in-flight count to reach zero.
- The queue is in-memory. Task-run durability across a backend restart comes
  from the persisted `Task.runQueued` flag + `recovery/queuedRunResume.ts`.

## Adding a new spawn site

Pick the band: `batch` for fan-out work (task runs, workflow steps),
`priority` for things that unblock an in-flight run (merge-conflict
resolvers, post-merge hook), `interactive` for user-initiated one-offs
(push, security review).

Two consumer shapes, both in use:

- **Await the result** — `queuedCreateSession({ kind, priority, dedupeKey,
  opts })` (`../queuedCreateSession.ts`) wraps a single `proxyCreateSession`
  and resolves with the usual `CreateSessionResult`. Use it when the caller
  needs the session synchronously (merge resolvers, post-merge hook, push).
  Lightweight per-site setup runs before the call.
- **Fire-and-forget** — call `enqueueSpawn` directly with a thunk that does
  the spawn and emits whatever WS event delivers the terminal (task runs →
  `task-spawned`, workflow steps → `step-spawned`). Use it when the heavy
  setup should be paced too (task runs: git worktree) or the caller must not
  block (workflow advance).

A thunk may throw `SpawnCapacityError` on a cap rejection; `queuedCreateSession`
does this for you, and helpers like `startTaskById` do it via `throwOnCapacity`.
