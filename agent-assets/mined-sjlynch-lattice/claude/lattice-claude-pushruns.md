# backend/src/pushRuns

One-off agent sessions for the QA-lane **Push** button (commit pending changes,
then push) and workflow **Push** (push existing commits only; leave uncommitted
user work untouched). Both spawn an agent in throwaway scratch that `cd`s into
the project, follows its selected `PUSH_INSTRUCTIONS.md` brief, and calls back
on completion. Workflow Push uses `effectiveStepHarness` / `effectiveStepPiModel`
(run override, then step selection); the QA-lane button defaults to Claude.
`../pushRuns.ts` is the public shim; served by `routes/pushRuns.ts`
(`/api/push-runs`). Keep the two briefs distinct despite the shared lifecycle.

## Shared contract (`../homeScratch/`)

The path guard, session-setup lifecycle, and bounded recursive cleanup are no
longer hand-rolled here — they live in **`backend/src/homeScratch/`**, the
canonical home-scoped-scratch contract shared by pushRuns / qaRuns /
postMergeHooks. This dir's `paths.ts` / `session.ts` / `cleanup.ts` are now thin
wrappers that pass the `push`/`[pushRuns]`/`push session` config into that
factory. **A change to the path guard or cleanup goes in `homeScratch/`, not
here.**

## Mirror contract

`qaRuns/` is a near-clone of this directory — same skeleton, same
persisted-registry / home-scoped-scratch / path-guard / Stop-hook / boot-sweep
contract (now backed by the shared `../homeScratch/` builder). Keep shared
lifecycle fixes aligned; push brief selection here and qaRuns' `verdict.ts`
(qa → done auto-promotion) stay feature-specific. Log prefixes, id prefixes
and scratch dirnames belong in the `createHomeScratchPaths` config. New run
types should reuse `../homeScratch/` — **including** its path guard, part of
the repo's `.git`-deletion defence layer (see the root `CLAUDE.md`).

## Files (the shared skeleton)

- `paths.ts` — one `createHomeScratchPaths(...)` call wired with the
  `push`/`[pushRuns]`/`push session` config; re-exports `assertSafePushSessionPath`, plus the
  `pushPaths` object the builder consumes. The **path-safety guard** itself lives
  in `../homeScratch/paths.ts`: it refuses any id that fails the id regex, any
  dir not strictly under the home scratch root, or any dir that lands inside the
  project repo — what bounds the recursive cleanup so it can never reach `.git`.
- `cleanup.ts` — thin wrapper over `cleanupHomeScratchSession` (the shared
  bounded recursive delete: kill the PTY holding the dir handle, strip reparse
  points, then `fsRmWithRetries` for Windows EBUSY/EPERM, gated through
  `assertSafePushSessionPath` + `assertNotReparsePoint`). On failure it leaves
  the dir for the boot sweep rather than forcing the delete.
- `session.ts` — `startPushSession` / `setupPushSession`, thin wrappers over the
  shared `homeScratch/` builders: `startPushSession` goes through the
  `createHomeScratchAgentSession(spec)` mirror factory (which owns the command,
  `interactive` queue band, presence-node registration, and cleanup wiring);
  `setupPushSession` is the materialize-only `setupHomeScratchSession`. Only the
  push-specific brief, hook install, and registry record (`recordPushRun`) stay
  here — passed to the factory's `start` per call. The spec is built per spawn
  with the selected harness, normalized Pi model, and project Codex yolo toggle.
  `qaRuns/session.ts` mirrors
  the lifecycle (its `spec` adds `isQaRun: true`).
  `PushBrief = 'qa-lane' | 'workflow'`: `renderPush` defaults to `qa-lane` and
  resolves the editable `push` template; `workflow` selects `workflow-push`.
  `startPushSession` forwards `opts.brief`; the QA-lane route omits it, and
  `setupPushSession` also uses the default. The caller in
  [`workflowRuns/controlSteps/push.ts`](../workflowRuns/controlSteps/push.ts)
  explicitly passes `brief: 'workflow'` to push existing commits without
  staging or committing user work. Keep that explicit: the separate `workflow`
  ownership metadata does not select the brief.
- `stopHook.ts` — installs Claude and Codex Stop hooks and Pi shutdown/activity
  extensions (→ `/api/push-runs/:id/done`); defines the stable `pushAgentId`.
  Pi's quit gate is enabled because `/done` kills the session's PTY; `/fork`
  and `/reload` must preserve it. Pi/Codex briefs also ask for an explicit POST
  as the last action so Pi does not sit idle after its turn.
- `instructions.ts` — `renderPushInstructions` interpolates the template
  selected by `session.ts` into `PUSH_INSTRUCTIONS.md`; both `push` and
  `workflow-push` use this renderer. Its standalone default is `push`.
- `registry.ts` — the in-memory run map (+ lifecycle event fan-out) whose
  **running** runs are mirrored to `~/.lattice/per-project/<hash>/push-runs.json`
  (`pushRunStore`, `../homeScratch/persistence.ts`). The push agent's pty
  survives a backend restart in the detached terminal-server, so boot recovery
  (`recovery/oneOffRunResume.ts`) puts back a run whose pty is still alive —
  its `/done` then lands normally instead of 404ing — and settles one whose pty
  is gone (`markPushRunLost`: `lost` + done) after a grace for the callback
  outbox. A run records its `serverId` and, when a workflow Push step spawned
  it, `workflowRunId` + `workflowStepIndex`: `findRunningPushRunForWorkflowStep`
  is how a Push step re-dispatched after a restart attaches to that session
  instead of pushing a second time (a `lost` run is never attachable). Harness,
  Pi model and Codex yolo selection are persisted for attachment and presence.
  Legacy records without a harness retain their Claude default. A push
  whose genuine `/done` lands after it was settled `lost` is corrected to
  completed (`markPushRunCompleted`), and a re-dispatched Push step whose push
  already FINISHED (its `/done` replayed before the re-dispatch) completes
  without pushing again (`findCompletedPushRunForWorkflowStep`).
  `forgetPushRun` evicts a finished run.
- `types.ts` — `PushRun` / `PushSession`.

## Scratch

`~/.lattice/per-project/<hash>/push/<id>/` — rooted through the shared
`projectHash` / `homeProjectDir` storage key, which can retain a legacy binding;
see [project identity](../PROJECT_IDENTITY.md). Scratch stays **outside** the
repo so recursive cleanup can never reach the project tree. At boot, a dir
whose pty did not survive is swept
(`recovery/pushSessionSweep.ts`); a live one belongs to a re-adopted run.

## Command reference

From `backend/`: `npm run build`, `npm test`, `npx tsc --noEmit`. For a
HOME-isolated single-file test invocation, see [test guidance](../__tests__/CLAUDE.md).
