# backend/src/routes/workflows

The HTTP edges of the workflow subsystem. `routes/workflows.ts` composes these
two per-concern sub-routers (their mount order is not significant; route
order inside `runs.ts` is). Run state itself lives in `../../workflowRuns.ts`;
these modules are thin handlers over it.

## Modules

- `crud.ts` — workflow-**definition** CRUD: `GET`/`POST /api/workflows`,
  `PATCH`/`DELETE /api/workflows/:id`. Backed by `../../workflows.ts`. No run
  state.
- `runs.ts` — run lifecycle: `POST /api/workflows/:id/run` (optional
  harness/Pi-model override), `POST /api/workflow-runs/:runId/steps/:n/complete`,
  `POST /api/workflow-runs/:runId/cancel`, `GET /api/workflow-runs/active?project=`,
  and `GET /api/workflow-runs/:runId`.

## Run-route gotchas

- **Recovery gates every lifecycle route** (start, complete, cancel, active,
  by-id read). Middleware awaits `../../workflowRuns/recoveryReadiness.ts`
  `waitForWorkflowRecovery` for at most 10 seconds, then returns **503** with
  `code: 'workflow-recovering'` and `Retry-After: 2` if unavailable. Ready means
  persisted runs have been re-registered; redispatched work may still be running.
- **One active run per project:** start returns **409** `active-run-exists`
  before any spawn when the project is busy. The legacy `requireNoActiveRun`
  body field is ignored. This guard provides no durable start idempotency after
  completion/cancellation; retrying an ambiguous start can create another run.
- **By-id lookup:** register `GET /api/workflow-runs/:runId` **after `/active`**
  so `active` is not parsed as an id. Returns `{ run }`, including recent
  finished runs retained in memory (`MAX_FINISHED_RUNS_PER_PROJECT`, currently
  20 per project, in `../../workflowRuns/state.ts`). Finished history does not
  survive restart; eviction also yields **404**. A 404 does not prove an earlier
  start never executed. This read honours the optional ownership pin below.

## Completion acknowledgement

`POST /api/workflow-runs/:runId/steps/:n/complete` rejects malformed indexes
(anything other than decimal digits forming a safe integer) with **400**;
an unknown run gets **404**, without acknowledging completion. For known runs,
duplicate/stale callbacks are handled by the engine's idempotent advance.

Sources starting with `claude-stop-hook` await `recordStopReceived` to durably
record the Stop **before** arming the quiescence gate and answering
`{ ok: true, gated: true }`; acknowledgement does not mean the step advanced.
The Stop checkpoint logs write failures and still allows the in-memory gate.
Explicit curl / Pi extension / Codex completions take the immediate path,
awaiting the advance before `{ ok: true }`. Advancement awaits terminal
teardown before dispatching the next step (or releases bookkeeping when
`keepWorkflowStepTerminals` is enabled). Runs advance through callbacks, not
task-state polling. Checkpoint and quiescence details belong in
[workflowRuns/CLAUDE.md](../../workflowRuns/CLAUDE.md).

## Project pin

`PATCH`/`DELETE /api/workflows/:id`, `POST /api/workflows/:id/run`,
`POST /api/workflow-runs/:runId/cancel`, and `GET /api/workflow-runs/:runId`
look their record up globally and honour an optional `?project=` via
`../projectParam.ts` `requireOwnedByRequestedProject` (the same canonical-path
compare as the tasks routes' `requireTaskInRequestedProject`): a non-empty
project that doesn't own the workflow/run is a 404 with a "different board"
hint, before any write/spawn or returning the run. Absent/empty → unpinned.
Ownership regression coverage: `../../__tests__/workflowProjectPin.test.ts`.

## Stability

The Stop-hook callback paths/shapes are part of the agent contract — don't change
them when refactoring. `runs.ts` takes `backendOrigin` (for the curl callback
baked into the spawned session).

Command reference (cwd `backend/`): `npm run build`, `npm test`,
`npx tsc --noEmit`. See [the test guide](../../__tests__/CLAUDE.md);
recovery/callback coverage includes `workflowDurability.test.ts`,
`workflowRunResume.restore.test.ts` (and its sibling `workflowRunResume.*`
suites), and `workflowStopHookGate.test.ts` there.
