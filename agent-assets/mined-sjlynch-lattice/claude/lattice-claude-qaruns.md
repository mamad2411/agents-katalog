# backend/src/qaRuns

QA-lane "run an end-to-end test" sessions (per-task ▶ and lane-wide, shown when
the `qaPlaywright` toggle is on). A one-off Playwright-enabled Claude session
spawns from home-scoped scratch, `cd`s into the project, drives the merged
feature end-to-end with the Playwright browser tools, appends a human-readable
PASS/FAIL to the task via `/append-summary`, then posts a *structured* verdict
to `POST /api/qa-runs/:id/verdict` before stopping. `../qaRuns.ts` is the public
shim; served by `routes/qaRuns.ts`.

## Mirror of `pushRuns/`

Same skeleton (`paths` / `cleanup` / `session` / `stopHook` / `instructions` /
`registry` / `types`) with the same in-memory-registry, home-scoped-scratch
(`~/.lattice/per-project/<hash>/qa/<id>/`, **outside** the repo), path-guard and
boot-sweep (`recovery/qaSessionSweep.ts → sweepOrphanedQaSessions`) contract.
The path guard, session-setup lifecycle, and bounded cleanup are shared via
**`../homeScratch/`** — `paths.ts` / `cleanup.ts` / `session.ts` here are thin
wrappers passing the `qa`/`[qaRuns]`/`qa session` config (and `isQaRun: true`)
into those builders. `session.ts` specifically goes through the
`createHomeScratchAgentSession(spec)` mirror factory (shared command / queue /
presence-node / cleanup wiring); only the QA brief, hook install, and
`recordQaRun` write stay here, and the `spec` carries `isQaRun: true`. **See
`pushRuns/CLAUDE.md` and `homeScratch/CLAUDE.md` for
that shared shape** — including that the registry's running runs are mirrored
to `~/.lattice/per-project/<hash>/qa-runs.json` (`qaRunStore`) and re-adopted
by `recovery/oneOffRunResume.ts` when their pty survives a backend restart
(else settled after a grace and their scratch swept), and that
`assertSafeQaSessionPath` is part of the repo's `.git`-deletion defence layer.
**Edit one, check the other.**

Differences from pushRuns:

- **`verdict.ts` (qaRuns-only).** `applyQaVerdict` records the agent's verdict
  and, on a **confident PASS**, auto-advances the task `qa → done` (guarded:
  only when the task is still in the `qa` lane); a FAIL or an unsure PASS leaves
  it for a human. pushRuns has no `verdict.ts` — its `/done` Stop callback is
  pure cleanup. **The qa → done transition has two triggers, mirroring how
  in_progress → ready_to_merge fires from the model's explicit curl AND the
  reliable Stop hook / Pi completion extension** (so it never hinges on the
  model remembering): `applyQaVerdict` is the agent's explicit `/verdict` curl
  (the fast path, applied while the run is still tracked), and
  `applyRecordedQaVerdict` is the **`/done` Stop-hook backstop** — it re-applies
  whatever verdict was recorded, so the transition still fires if the explicit
  curl never landed (it failed, the agent forgot it, or it raced `/done`). Both
  funnel through the idempotent `promoteOnConfidentPass`, so either firing — or
  both — advances the task exactly once. Idempotency covers the concurrent case
  too: a per-run in-flight promise makes a `/verdict` and `/done` that land
  together share one promotion (only one reports `moved: true`), instead of
  both passing the `movedToDone` check before either `updateTask` resolved. A run that stops with **no** recorded
  verdict is left in QA for a human (the Stop hook can't synthesize a pass/fail),
  same as a fail or an unsure pass. So `/done` is no longer pure cleanup; it is
  the QA analogue of the Claude Stop hook / Pi extension that closes the lane.
- **The verdict survives a restart.** `recordQaVerdict` / `markQaRunMovedToDone`
  go through the registry's `update`, so the mirror carries them: a `/done`
  after a backend restart (or a replay from the callback outbox) still
  promotes a confident PASS, and boot recovery settling a run whose pty died
  applies the recorded verdict exactly as `/done` would
  (`applyRecordedQaVerdict` → done).
- **A verdict only promotes the build it tested.** `promoteTask` skips a task
  whose `mergedAt` is newer than the run's `createdAt` (dragged out, reworked,
  merged back into QA while the run went on), and `applyRecordedQaVerdict`
  never re-applies a run already `done` — so a second Stop from a stay-open QA
  terminal, a replayed `/done`, or boot recovery can't ship reworked code on a
  stale PASS. This relies on every landing in QA stamping a fresh `mergedAt`:
  `stampTimestamps` clears it when a task moves back to a pre-merge lane, and
  boot's deleted-branch recovery (`recovery.ts`) always re-stamps it.
- **One QA session per task.** `POST /api/qa-runs` returns **409** while the
  task already has a run starting (the route's in-flight set, since a run is
  only recorded once its pty spawned) or `running` with a live pty
  (`routes/qaRuns/startGuard.ts` `findActiveQaRunForTask`, via
  `listRunningQaRuns` + the terminal-server probe). Two sessions would drive
  the same dev server and either one's confident PASS promotes the task. A run
  whose pty is gone (tab closed, so no `/done`) doesn't block a re-test; an
  unreachable terminal-server counts a tracked run as live. The frontend
  mirrors it (`useQaRuns`): a task with a run whose tab is still open shows a
  spinning "testing…" button that focuses that tab instead of starting another.
- **Never set `taskId` on a QA run's terminal.** The task is already in the `qa`
  lane, and the frontend's `useTaskTerminalCleanup` closes every terminal tagged
  with a qa/done/deleted task — it would kill the session it just spawned.
- **Spawn sets `isQaRun: true`** so the MCP injection chokepoint adds the
  QA-scoped Playwright (with the lane's headed/headless choice); ordinary task
  spawns never set it.
- **`forgetQaRun` never drops a still-`running` run.** The frontend poller
  calls it (via `DELETE /api/qa-runs/:id`) on any transient `GET :id` hiccup,
  and evicting a live run before its `/verdict` lands silently breaks the
  qa → done auto-advance (the bug that left passed tasks stuck in QA). Only
  `done` runs are forgotten.
