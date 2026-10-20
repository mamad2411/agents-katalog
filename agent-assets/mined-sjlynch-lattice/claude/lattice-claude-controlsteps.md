# backend/src/workflowRuns/controlSteps

Workers for the `start` / `merge` / `push` control steps, which drive the
task pipeline from the backend. The dispatcher (run.lock + kind routing) is
`../controlStep.ts`. Not here: the Run tests agent step
([testStep](../testStep/CLAUDE.md)), the push session
([pushRuns](../../pushRuns/CLAUDE.md)), post-merge hooks
([postMergeHooks](../../postMergeHooks/CLAUDE.md)).

| Step | Waits for | Then |
|------|-----------|------|
| `start` | — | Open → In Progress (spawned or queued) |
| `merge` | the run's round before **any** merge; Phase C hook; re-check | Ready-to-Merge → QA (inner merge runs) |
| `push` | Ready-to-Merge empty | push `main`'s existing commits (no commit) |

## Map

- `start.ts` — `runStartStep` (the Task Board **Run All** path; one
  `workflow-task-spawned` tab per task); harness picker in `startHarness.ts`.
- `merge.ts` — `runMergeStep`: `drainReadyToMerge`, `noProgressError`,
  Phase C, `raceWorkflowRunEnd`, `waitForMergeRunFinished`.
- `push.ts` — `runPushStep` = `adoptOrDrain` (re-dispatch short-circuits, else
  the drain) + `createPushSessionWatch` (owns subscriptions, timer, admission
  AbortController and the single `killAndAbandon()`; disposed in `finally`).
- `shared.ts` — `emitControlProgress` (the one `step-control-progress`
  shaper; pre-run tools and Run tests use it too), `subscribeOnce` (settles
  once, even if fired during subscription), and re-exports of the waits in
  `mergeWorkWait.ts`, `laneWait.ts` (Push's drain) and `postMergeHookWait.ts`;
  `waitPrimitives.ts` is their cycle-free leaf (`isRunEndedEvent`,
  `createWaitSettler`, re-armable `createUnrefTimer`).

Tests: `__tests__/workflow{Start,Merge,Push}*`, `workflowRunRound`, and those
named below.

## The run-lock (load-bearing)

- `../controlStep.ts` waits out repo maintenance (a merge run's `git gc
  --auto`; merging beside a repack leaves a full pack copy on Windows), skips
  the lock if the run was cancelled meanwhile, then holds `run.lock` as
  `workflow-<kind>:<runId>`, so restarts defer and a manual `/merge` can't race.
- Released in a `finally` — even on throw — **before** `completeStep`, since
  the next control step acquires its own lock inside that call.
- **Every wait inside a worker MUST be bounded.** A worker that blocks forever
  never reaches the `finally`: the lock leaks, every later merge run / control
  step for the project blocks, and restarts stay deferred. Injectable
  `ControlStepWorkerDeps` pin release-on-throw (`workflowLaneWaitTimeout`).
- Inner merge runs use `lockMode: 'inherit'` (they'd deadlock on this lock).

## Waits

- Subscribe to the task store (and workflow-run events) **before** the initial
  read, so a transition in the gap isn't missed; a run leaving `running`
  resolves the wait promptly (`isRunEndedEvent`).
- Timeouts are **no-progress** bounds, never totals: re-armed whenever work
  moves forward, so a slow batch never trips (a total cap once stranded a
  whole batch at ready_to_merge), while a stalled lane (an agent died without
  committing; the in-progress sweep refuses `no-commits`) still **rejects**,
  erroring the run and freeing the lock. Merge: `TASK_DRAIN_TIMEOUT_MS`,
  `PHASE_C_HOOK_TIMEOUT_MS` (30 min); Push: `PUSH_DRAIN_TIMEOUT_MS` (15 min).
  They also bound a hung initial read.
- Task-read and progress-callback failures reject the wait and release its
  subscriptions — never a detached rejection (`processGuards` would exit).

**`waitForMergeWork`** resolves once **no task in the run's round**
(`roundTaskIds`; a legacy run counts every task) is pending — `in_progress`,
persisted `runQueued`, or a live `task-run:<id>` request — so the round merges
together; don't regress to waking on the first ready task while siblings run.
Tasks outside the round, and Open/Backlog tasks with no admission marker,
never block.
- **Deadlock guard:** when ready work exists and *every* pending round task is
  a start held for disk (`runWaitingForDisk`), wake anyway —
  `diskPressureMerge` leaves workflow projects alone, so only this merge can
  free those worktrees.
- Polls as a fallback (queue settlement has no task-store event; a failed
  spawn clears its flag before its live request disappears); a newer store
  event supersedes an outstanding read.
- Progress is tracked per task (queued → running counts even at an unchanged
  total; the highest phase is kept), so metadata updates can't extend a stall.

**`waitForPostMergeHookIdle`** also waits through the trigger's pre-record
pending marker and keeps its first idle subscription one event-loop turn
(the task-QA-notify → hook-record gap). Its subscriber is deliberately **not**
project-filtered: `getActiveHookForProject` canonicalizes the path while
`ev.run.projectPath` is raw, so a `!==` filter would drop our own events.

## `start.ts`

- **Round membership:** every Open task it handles (started, queued, or left
  to an existing queued run) joins `roundTaskIds`, checkpointed **before the
  first launch**, so a restart can't forget a member and let Merge merge
  around it.
- **Harness** mirrors Run All: a run `harnessOverride` (+ Pi
  `piModelOverride`) pins every task; else the project default (`interleave`
  alternates claude/pi).
- **Hard cap (do not regress):** spawns pass `throwOnCapacity: true`, so
  `SpawnCapacityError` throws *before* the in_progress flip — the task stays
  **Open** (no agentless in_progress or orphan pty — the stuck lane that hung
  Merge), is re-queued via `enqueueTaskRun`, and counts as deferred.
- **Queue admission (do not regress):** direct starts bypass
  `maxConcurrentAgents` and the CPU/RAM governor (50 tasks once launched 50
  agents), so each start first asks `batchAdmissionHold()`; when held, the
  task goes to `enqueueTaskRun` as deferred. Disk deferrals
  (`SpawnDiskSpaceError`, `isSpawnDeferral`) take the same path.
- **Only successful admission counts as deferred:** a rejected enqueue is a
  per-task failure (its error kept for the all-failed guard); later tasks
  still run; partial success advances; nothing started *and* nothing deferred
  throws. A known queued run stays deferred without another enqueue.
- **Never start a task the queue is already starting (do not regress):** a
  queued run keeps its task `open` until its pty spawns, so it still looks
  runnable; a second start killed the first run's pty + worktree or put two
  agents on one task (`-r2`). Skip as deferred anything with `runQueued`, a
  live `task-run:<id>` request (`hasSpawnRequest`, checked *after* the
  admission-hold await) or a start in flight (`isTaskStartInFlight`). The
  reverse race is serialized in `startTaskById` (`../../routes/tasks/CLAUDE.md`).
- **Cancellation owns only pending direct launches:** re-check run status and
  current step after every await and before enqueue / events. Each direct
  `startTaskById` gets an AbortSignal tied to workflow end/advance so its
  withdrawal checkpoints reclaim an unestablished checkout/PTY. Established
  agents and accepted queue requests keep their lifecycle — never cancel a
  shared `task-run:` key to stop a workflow.

## `merge.ts`

- `drainReadyToMerge` waits on `waitForMergeWork` before **every** merge
  round, so an In Progress gap or a task spawning mid-merge can't end the step
  early; ready tasks outside the round merge along. After a disk-held wake the
  next iteration waits for the starts it unblocked.
- **Id-set progress guard:** abort (`noProgressError`) when a full merge run
  leaves the ready_to_merge id-set unchanged — a persistently erroring task
  stays in the lane, so compare ids, not error counts, or the loop never ends.
- Workflow cancel → the inner merge run is cancelled.
- **Phase C (do not regress):** never report `merge complete` while a
  post-merge hook runs for the project — the run would finish and the frontend
  queue would start the next workflow on top of the hook agent. Hooks fired
  *by* a merge run are covered (`mergeRuns.ts` awaits `runPostMergeHook`
  before `finishRun` — keep that order); hooks fired outside a run
  (`awaitPostMergeHookOutsideRun`) or still owed after a restart
  (`fireOwedPostMergeHook`, raced against cancellation) are not. It can't
  live in the queue: `assertNoActiveWorkflowRun` counts runs, not hooks, and
  its 409 retry fires only when a run finishes.
- After Phase C it re-checks tasks; new or just-settled work loops back
  through the drain and the hook gate.

## `push.ts`

- Harness/model: `effectiveStepHarness` / `effectiveStepPiModel` (run
  override wins). Brief: `{ brief: 'workflow' }` — never `git add` / `commit`:
  uncommitted files on the main checkout are the user's WIP, and workflow
  output is already committed.
- **Subscribe before spawn:** `done` and run-ended subscribers attach before
  `startPushSession` (a fast `/done` or cancel can't slip past); `serverId`
  arrives via `attach(session)`.
- **`PUSH_STEP_TIMEOUT_MS` (15 min)** for a harness stalled without `/done`:
  kill the pty, settle the push run (`abandonPushRun`) and **throw** — the run
  errors, never "push complete". A `/done` already landed isn't a timeout; a
  cancel that lands first stays cancelled.
- **`step-spawned` carries the registry `terminalId`** (or `findTerminalId` by
  `serverId` when adopted): the `/done` cleanup closes only that record's tab;
  without it the frontend minted a tab that never closed.
- **`forgetPushRun` in `finally`:** nothing else polls a workflow push, so it
  would leak for the process lifetime.
- **Cancel/admission race (do not regress):** the watch's AbortController
  reaches `queuedCreateSession` (via the homeScratch adapters), so cancel /
  timeout withdraw a pending request and cleanup completes without capacity
  returning. If PTY creation already started, await its response and confirmed
  reclamation — never abandon the startup promise. The post-spawn re-check
  (cancel between PTY delivery and `attach`) awaits the kill and emits neither
  `step-spawned` nor `push complete`.
- **Re-dispatch attaches, never double-pushes:** a restart kills the step but
  not its pty. Sessions carry `workflow: {runId, stepIndex}`; `adoptOrDrain`
  finishes at once if that push already completed, else re-attaches a live one
  (no drain, fresh timeout). A push recovery found dead is `lost` and never
  attached (push afresh); an attached one settled `lost` later fails the step
  (`oneOffRunResume`).
