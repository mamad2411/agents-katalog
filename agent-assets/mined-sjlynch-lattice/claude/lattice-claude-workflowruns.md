# backend/src/workflowRuns

The workflow-run engine behind the `../workflowRuns.ts` facade (start / cancel
/ restore / redispatch). Agent steps advance on Stop-hook / `session_shutdown`
/ explicit-curl callbacks, never by task-state polling; control workers wait
on board state and call `completeWorkflowStep` themselves. Not here:
definitions + `{{var}}` interpolation (`../workflows/`), routes
(`../routes/workflows/`), boot IO (`../recovery/workflowRunResume.ts`).

## Map

**Run registry / state**
- `types.ts` — the run wire types (`WorkflowRun`, `WorkflowStepExecution`,
  `WorkflowRunEvent`): types only, node-free (the frontend re-exports them via
  `../shared/wireTypes.ts`); `state.ts` re-exports them.
- `state.ts` — the `runs` map, `notify`, `checkpointWorkflowRun`, round
  helpers. Sole source of `/ws/workflow-runs` payloads: keep event shapes
  (esp. `step-spawned`) stable.
- `split.ts` - start-only expansion; source resolution failures produce persisted notes.
- `definition.ts` — the frozen per-run definition copy + validated read-back.
- `execution.ts` — group policy (`nextStepGroup`, `openStepGroup`) +
  per-member state helpers.
- `teardown.ts` — cancel/error cleanup of every active member; `failRun.ts` /
  `runErrored.ts` — `failWorkflowRun` / `markRunErrored`, outside the facade so
  `dispatch.ts`, `advance.ts` and workers needn't import it.

**Agent-step dispatch / spawning**
- `dispatch.ts` — `dispatchStep` (kind → spawner / Run tests /
  `executeControlStep`), `dispatchGroup`. Takes `completeWorkflowStep` as a
  parameter; never imports `advance.ts` (cycle).
- `stepSpawner.ts` — `spawnWorkflowStep` (`prepareStepScratch` →
  `writeStepAssets` → `installStepCallbacks` → `spawnStepSession`) into
  `<project>/.lattice/workflow-steps/<runId>/step-<N>/`; `opts.runTests` is
  the Run tests variant. New completion harness: `AgentHarness` (`../shared/`;
  `WorkflowStepHarness` aliases it), `buildWorkflowStepCommand`
  (`commandBuilder.ts`), `installStepCallbacks`,
  `renderStepCompletionInstructions`.
- `stepSpawner.ts` also reads task-writing rules and recent Spec gaps before
  rendering `{{task_writing_guidance}}`; any settings/task read failure yields
  empty guidance (`readTaskWritingGuidance`).
- `stepMarkdown.ts` — `renderStepMarkdown` (WORKFLOW_STEP.md, template
  `../instructionTemplates/templates/workflowStep.ts`), `effectiveStepHarness`
  / `effectiveStepPiModel`, `renderStepCompletionInstructions`.
- `projectDirtyState.ts` — the dirty-checkout warning atop WORKFLOW_STEP.md:
  planners read the working tree but their tasks run from HEAD. Best-effort
  (any failure → no warning).
- `stepTools.ts` — pre-run tools (v1 `opengrep` → `OPENGREP_FINDINGS.md` +
  `{{tool_reports}}`); `begin`/`end`/`abortStepPreRun` per run/member. A tool
  that can't run never fails its step; scans serialize per project so sibling
  members don't collide on the one scan slot.
- `sessionSpawner.ts` — `enqueueWorkflowStepSession` (spawn queue, presence,
  `step-spawned`), `kill`/`releaseWorkflowStepSession`,
  `cancelWorkflowStepSessions`.
- `renderHelperScript.ts` + `create-task-template.cjs` — the per-step
  `create-task.cjs` (create, `--summary`/`--list`/`--find`/`--get`; a
  dash-leading first arg is refused). The `.cjs` is a copied runtime asset;
  boot crashes without it (`../../CLAUDE.md`).
- `scratchDirectory.ts` — `pruneOldWorkflowRuns` (newest
  `WORKFLOW_RUN_RETENTION` + every running run; path- and reparse-guarded).

**Completion / persistence / recovery**
- `stopHookGate.ts` — the Claude Stop-hook quiescence gate
  (`../agentQuiescence.ts`).
- `advance.ts` — `completeWorkflowStep`: in-flight join, member settlement,
  group join, `completeRun`, next-group dispatch.
- `persistence.ts` — the `per-project/<hash>/workflow-runs.json` mirror of
  running runs (atomic, debounced, never throws, removed when idle);
  `runCodec.ts` — its pure codec.
- `resumeDecision.ts` — pure boot policy `classifyWorkflowRunResume` →
  `readopt` / `redispatch` / `complete` / `error` / `advance` (lost Run tests
  terminal) / `skip`.
- `recoveryReadiness.ts` — the "during recovery" gate below.

**Control + Run tests steps**
- `controlStep.ts` — `runControlStepWorker`: repo-maintenance wait, run.lock,
  kind → worker, release, settle. Workers:
  [`controlSteps/CLAUDE.md`](./controlSteps/CLAUDE.md).
- `testStep/` — the Run tests step:
  [`testStep/CLAUDE.md`](./testStep/CLAUDE.md).

Tests: feature-named `__tests__/workflow*.test.ts`.

## Invariants

**Starting**
- **One active run per project, always.** `assertNoActiveWorkflowRun` →
  `WorkflowRunConflictError` → **409** `active-run-exists`, before any run
  record / notify / spawn. No opt-out (legacy `requireNoActiveRun` is
  ignored); the frontend queue requeues on the 409; only boot recovery resumes
  several. It counts workflow runs, **not** post-merge hooks — hook exclusion
  is Merge's Phase C (`controlSteps/`).
- A run freezes its definition (incl. variables): editor changes never alter
  an executing or recovered run; a record without one uses the legacy lookup.
  An all-frozen workflow is refused before any run record.
- **Every run records its task round** (`roundTaskIds`): tasks Open or In
  Progress at start — read *before* the guard, since nothing may await between
  `assertNoActiveWorkflowRun` and `runs.set` (two starts could both pass) —
  plus every task the Start step handles. Merge waits for the whole round; a
  run without a readable round counts every task.

**Grouping / briefs**
- Groups run in order. Only adjacent `parallel: true` `agent` (planning) steps
  form a group; `splitGroup` isolates expanded members of a serial parent.
  Start / Merge / Run tests / Push are always barriers, even
  frozen. `nextStepGroup` forms authored boundaries *before* skipping frozen
  members (a frozen unmarked agent still separates groups; a frozen marked
  member is skipped in place). Every member goes through the spawn queue.
- The planner-only "How this step works" section stays **above**
  `{{step_prompt}}` claiming precedence, and Claude's completion line must not
  say "after creating all the tasks described above" — planners dismissed both
  as boilerplate and implemented the work themselves.

**Advancing**
- Completion is **idempotent**: stale callbacks are ignored, duplicates join
  the in-flight promise. A member checkpoints `completing` before terminal
  handling, then `completed` inside a per-run join lock; a failed first
  checkpoint restores the prior phase so the callback can retry.
- The successor dispatches once, after **every** active member is durably
  completed and its terminal handling settled, and is checkpointed `pending`
  first. `currentStepIndex` stays the first runnable member (compatibility);
  `activeStepIndices` / `groupEndIndex` / `stepStates` drive runs.
- **Terminal handling precedes the next dispatch**: `killWorkflowStepSession`
  awaits allocation + kill (`codex --yolo` never self-exits); with
  `keepWorkflowStepTerminals`, `releaseWorkflowStepSession` drops bookkeeping
  but leaves the PTY (`workflowStepSpawnFailure.test.ts`).
- **Claude Stop-hook completions are quiescence-gated**: `Stop` fires early and
  repeatedly while subagents run, and advancing on it ran steps in parallel.
  Only `claude-stop-hook-*` is gated (curl / Pi / Codex / control steps advance
  directly). The gate tracks subagents by `agent_id` (not a count), waits for a
  Stop *after* a subagent ends (`awaitingTurnEnd`), counts every `wf:` / `pmh:`
  hook event as a signal, and gives re-adopted sessions `READOPTED_SETTLE_MS`.
- Every step gets all three completion backstops (Claude Stop hook, Pi
  extension, Codex `hooks.json`) whatever its harness, so a mid-run harness
  switch can't lose the callback.
- **A held Stop survives a restart**: the route awaits `recordStopReceived`
  before answering (nothing resends it); recovery re-arms `{ rearm: true }`
  from BOOT if the gate was busy at its last checkpoint (`stopReceived.busy`;
  downtime is not silence), else from the later of `.at` / `.activeAt`; the
  boot placeholder never counts as busy. Post-merge hooks mirror this. A
  failing completion checkpoint retries 3×, then leaves a visible error (Run
  tests keeps retrying).

**Failure / cancellation**
- A rejected queued spawn errors its still-current planning-step run; Run
  tests' `onSpawnError` notes and advances instead. CAP retries stay pending; a
  late rejection must preserve a cancellation or a newer step.
- Cancellation is authoritative and kills (`teardown.ts`) regardless of
  terminal retention; queued `wf-step:<runId>:<step>` thunks re-check status /
  membership before and after `proxyCreateSession`.
- **Terminal transitions checkpoint immediately** (cancel, `failWorkflowRun`,
  `markRunErrored`, `markWorkflowStepSpawnErrored`): `notify` only schedules
  the debounced mirror, and a restart in that gap re-dispatched a finished
  step. Setup and post-checkpoint advance failures go through
  `failWorkflowRun`; an error after the run left `running` keeps its state.
- Control steps release run.lock **before** `completeStep`, inside a
  restart-drain transition (`../restartDrain/`); the detached worker guards
  every await (an unobserved rejection kills the backend via `processGuards`).

**Surviving a restart**
- **A run must survive the backend process.** The dev runner defers only while
  a `run.lock` is held (control + Run tests steps); a lost run silently drops
  its agent's later `/complete`. Keep the mirror current on every run mutation
  and `restoreWorkflowRun` idempotent (never clobber a live run). Restarts
  drain first: start / advance are tracked transitions, spawns wait `pending`,
  and `POST /api/workflows/:id/run` answers 503 `backend-restarting`.
- Mirror writes/deletes serialize per project and a flush awaits writes in
  flight (a late running-state write must not resurrect a finished run).
- Phases `pending` / `spawning` / `running` / `completing`: required writes
  precede launch/teardown. `pending` (incl. mid pre-run scan) re-dispatches;
  `spawning` with no terminal errors; `stepSessionAlive: null` re-adopts;
  `completing` advances without replaying the prompt; control steps are
  re-dispatched (re-runnable).
- v3 mirrors snapshot group state deeply at enqueue; recovery handles each
  member independently and re-arms every held Stop. Completed members never
  replay; invalid group state errors visibly rather than replaying serially
  (`workflowParallelSteps.test.ts`).
- During recovery lifecycle requests wait (then 503 + Retry-After), unknown
  callbacks get 404 (never acknowledge an unknown run), and WS hellos carry
  `recovering: true` until an authoritative one.
- **A finished run stays readable by id** (`GET /api/workflow-runs/:runId`)
  until `MAX_FINISHED_RUNS_PER_PROJECT` evicts it — the frontend's
  `fetchWorkflowRun` tells "completed while disconnected" from "lost" with it.
