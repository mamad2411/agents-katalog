# backend/src/restartDrain

The backend half of the **dev-runner restart handshake**. The dev runner
(`backend/scripts/dev/restartPolicy.mjs` + `restartHandshake.mjs`) restarts
`dist/index.js` on every rebuild — for Lattice developing itself, that is every
merged task that touches `backend/src`. The kill is `TerminateProcess` on
Windows: no exit handler, no signal handler, no flush. Before the handshake a
restart landed wherever it landed — typically a few seconds after a workflow
control step released its `run.lock`, i.e. right inside the advance that
dispatches the next step, or while the frontend queue was starting the next
workflow.

## Protocol

1. Dev runner decides to restart (dist changed, no live `run.lock`, and — if a
   lock was just held — `LOCK_SETTLE_MS` since it cleared).
2. `POST /api/internal/restart-drain/prepare {reason, ttlMs, budgetMs}`:
   - `gate.ts` `beginRestartDrain` — the drain is **always TTL-bounded**
     (default 90 s, max 5 min; the runner sends ~95 s). A runner that dies, or
     changes its mind without calling `/cancel`, can't leave the backend frozen.
   - `settle.ts` `settleForRestart` — wait (poll 100 ms, 3 consecutive quiet
     samples, `budgetMs` ≤ 120 s) until no **tracked transition** and no
     **admitted spawn-queue thunk** is in flight, then flush the workflow-run
     mirror and every `ProjectStateManager` store (`tasks.json`,
     `merge-runs.json`, `workflows.json`, `terminals.json`). Flushes even when
     the budget ran out.
   - answers `{ready, pending[], waitedMs, flushed, pid, drain}`; the drain
     stays ON — the kill is expected next.
3. Runner re-scans run.locks (unless forcing): a lock taken meanwhile →
   `POST /cancel` and re-defer. Otherwise restart. Any handshake failure (no
   token file, backend down, 404 from an older backend, timeout, `ready:false`)
   → restart anyway, with a log line naming why (**fail open**).

## What the drain blocks

| Gate | Where | Behaviour while draining |
|------|-------|--------------------------|
| Spawn-queue admission (all bands) | `spawnQueue/drain.ts` | requests stay `pending`; durable ones survive the restart (`Task.runQueued`, a workflow step's `pending` phase). The drain's end re-drains the queue. `batchAdmissionHold` reports a hold so the workflow Start step queues instead of starting directly. |
| `acquireProjectRunLock` | `projectRunLock/acquire.ts` | **waits** for the drain to end — covers every in-process run-lock operation (control steps, Run tests, merge runs started internally, resumes). |
| Top-level "start X" HTTP | `routes/restartDrain.ts` `buildRestartDrainAdmissionGate` (mounted first in `server/app.ts`) | `POST /api/workflows/:id/run`, `/api/merge-runs`, `/api/tasks/:id/{merge,run,resume}`, `/api/push-runs`, `/api/qa-runs` → **503** `code: backend-restarting` + `Retry-After: 5`. Nothing was done yet; the frontend retries a 503 through a restart (`frontend/src/api/retry.ts`). |

Not blocked: Stop-hook `/complete` callbacks, cancels, reads, and sidebar
`POST /api/terminals` (user-interactive; its pty lives in the detached
terminal-server and survives, and the create is a tracked transition).

## Tracked transitions (`gate.ts`)

`beginRestartTransition(label)` / `trackRestartTransition(label, promise)` —
always on, independent of the drain. **Call the function `beginRestartTransition`
returns on every path (`try/finally`)**: a leaked entry never clears, so every
later `/prepare` waits out its full settle budget (the runner sends 45 s) and
answers `ready:false`. Current sites:

- `workflowRuns.ts` — `startWorkflowRun` (run in memory → first checkpoint +
  dispatch) and every `completeWorkflowStep` advance (the `completions` promise).
- `workflowRuns/controlStep.ts` — the lock **hand-off**: begun just BEFORE the
  control step releases its `run.lock`, ended when `completeStep` returns. The
  lock can't be held across `completeStep` instead (the next control step
  acquires its own lock from inside that call), so this is what closes the
  instant where neither the lock file nor anything else said "mid-transition".
- `terminalServerClient/createSession.ts` — every `proxyCreateSession` (pty
  created → registry record written).
- `opengrep/reviewSession.ts` — review setup/admission through the durable PTY
  ownership update, with a `finally` release on failure and queued cancellation.
  `POST /api/opengrep/reviews` is also a top-level admission-gated start; turn
  callbacks, reads and cancellations remain available during drain.

A transition that legitimately runs long (an advance whose next step runs an
Opengrep pre-run scan, a multi-GB worktree checkout in an admitted spawn) just
exhausts the budget → `ready:false` → fail-open restart; each of those has a
boot-recovery path. Keep new transitions SHORT and bounded; never track a whole
long-running worker.

## Lock-holder report (`lockHolders.ts`)

`GET /api/internal/restart-drain/lock-holders` → `{pid, holders: [{hash,
project, parkedOn, detail}]}`. `parkedOn` is `conflict-resolver` when a live
merge run is parked on a resolver waiter whose pty is alive (or whose liveness
can't be probed / spawn is still queued — `mergeRuns/waiterLiveness.ts` bounds
those), `post-merge-hook` for a running hook with a live pty, else `null`. The
dev runner's `MAX_DEFER_MS` backstop skips forcing only when EVERY held lock's
hash is parked and its pid is this process; a backend it can't ask gets
forced as before.

## Auth

Internal-only: the router refuses any request with an `Origin` header (403 —
even the Lattice UI's own origin) and requires the backend-only loopback token
in `x-lattice-terminal-token` (401), constant-time compared — the same token
file (`~/.lattice/terminalServerToken`) and header the terminal-server's
mutating routes use, which the dev runner already reads for its shutdown call.

## Tests

`__tests__/restartDrain.test.ts` (gate, TTL, tracker, settle, spawn-queue and
run-lock gates, control-step hand-off, lock holders, HTTP auth + 503 gate) and
`__tests__/devRestartHandshake.test.ts` (the dev-runner side).
