# backend/src/workflowRuns/testStep

The workflow **Run tests** step (`kind: 'test'`): an **agent** step with a
fixed brief that runs the project's tests on the main checkout, fixes what it
can, commits the fixes and reports. The facade's `dispatchStep` routes `'test'`
to `dispatchRunTestsStep` (never `executeControlStep`); the spawn (step dir,
spawn queue), hooks, `/complete` route and Claude quiescence gate are the agent
step's, unchanged (`../stepSpawner.ts` takes `opts.runTests`). Covered by
the split `__tests__/workflowRunTestsStep.*.test.ts` suites (shared harness
`__tests__/helpers/workflowRunTestsStep.ts`).

## Modules

- `runTestsStep.ts` — the orchestration and public surface. `dispatchRunTestsStep`
  → detached `runRunTestsWorker`, which runs its phases in order
  (`preflightSkipNote` → `acquireWithWait` → `captureStartState` →
  `buildRunTestsBrief` → `armTimeoutOnSpawn` → `spawnWorkflowStep`); `finalizeRunTestsStep` (from the
  advance), `abortRunTestsStep` (cancel / fail), `resumeRunTestsStep` (boot
  readopt), `noteRunTestsStep` (notes from outside the worker). IO goes through
  `RunTestsDeps` (`setRunTestsDepsForTest`), which it hands to the phase
  modules below. `completeStep` is passed in, as for `executeControlStep`, so
  nothing here imports the facade.
- `lockWait.ts` — the lock label, `acquireWithWait` (+ its give-up note) and the
  timeout (`armTimeoutOnSpawn` / `armTimeout` → kill, note, advance). Reads the
  deps live through `LockWaitContext`: its waits and timers outlive the call.
- `startState.ts` — the skip rule (`preflightSkipNote`), `captureStartState`
  and `buildRunTestsBrief`.
- `runTestsLifecycle.ts` — internal entry tracking, lookups, the shared
  `isCurrent` / `progress` helpers and timer / subscription cleanup, separate
  from full teardown that releases the lock.
- `brief.ts` — renders `RUN_TESTS.md` from the `run-tests` instruction template
  (`../../instructionTemplates/templates/runTests.ts`); completion wording is
  `renderStepCompletionInstructions` from `../stepMarkdown.ts`.
- `checkoutGit.ts` — read-only `projectGit` probes (HEAD, detached, status, the
  step's commits). Every failure reads as "unknown".
- `userWip.ts` — `git status --porcelain=v1 -z` parsing, `USER_WIP.txt`
  read/write, `wipCovers` (an untracked `dir/` covers what's under it).
- `runTestsState.ts` — `~/.lattice/per-project/<hash>/run-tests.json`
  (`{lastHead, lastFinishedAt}`), atomic, home-scoped.
- `recentTasks.ts` — the brief's "recently merged" list (`qa`/`done` tasks since
  `lastFinishedAt`, else since the run started; newest first, ≤ 30).
- `summary.ts` — bounded `TEST_SUMMARY.md` read (≤ 8 KB), the commits
  post-check (warns when a step commit touched a `USER_WIP.txt` path), the
  step-summary composer.

## Invariants

- **Never stops the workflow** (D4). Every failure is "note + advance": a skip,
  a setup throw, `onSpawnError`, the timeout, a terminal lost over a restart
  (`../resumeDecision.ts` → `advance` → `noteRunTestsStep`), a completion
  checkpoint that keeps failing (the stop-hook gate retries every
  `RUN_TESTS_GATE_RETRY_MS`; the worker's own `advance` every 30 s). Its own
  failures never error the run.
- **Skip rules**: a detached HEAD (merges fast-forward the checked-out branch —
  `assertMainOnBranch`), or HEAD equal to `lastHead` in `run-tests.json`. An
  unborn / unreadable HEAD runs.
- **Lock**: the project `run.lock` as `workflow-test:<runId>`, **non-lendable**,
  held for the whole step: a manual Merge / Merge All gets a 409 naming the
  step; resolver finalize / snapshots / out-of-run post-merge hooks wait
  (`withProjectMutation` / `waitForExclusiveProjectHold`); the dev runner defers
  restarts for any `workflow-*` label without its 15-minute force. A busy lock is
  retried for up to 10 min, then note + skip. Released on **every** exit
  (advance → finalize, cancel / fail → abort) and before the next step
  dispatches. After a restart `resumeRunTestsStep` re-takes it (the dead
  backend's is stale → stealable).
- **Start state is captured under the lock**: start HEAD + `USER_WIP.txt`, then
  `run.testStep = {stepIndex, startHead}` is checkpointed.
- **The user's WIP is never touched; fixes commit by explicit path only.** The
  brief (`run-tests` template) forbids editing / staging / committing any
  `USER_WIP.txt` path and has the agent commit with
  `git commit -m … -- <paths>` — never `git add -A` / `.`, `stash`, `reset`,
  `checkout`, `restore`, `clean`, `push` or `--no-verify` — so nothing the
  user staged is swept in. Keep that wording when editing the template; the
  post-check (`summary.ts`) flags a step commit that touched a WIP path.
- **Timeout** (`timeoutMinutes`, default 60) runs from the pty spawn — armed on
  the step's `step-spawned`, so spawn-queue / resource-governor wait doesn't
  count. `spawnedAt` is persisted so a re-adopting backend re-arms the
  remainder. On timeout: kill the session, list `git status` minus
  `USER_WIP.txt` (never reverted), note, advance.
- `finalizeRunTestsStep` runs in the advance for every `'test'` step, before the
  next dispatch: stores `run.stepSummaries[i]`, and only after the agent's own
  completion writes `run-tests.json` with HEAD **at the finish** (so the step's
  own fix commits don't read as "merged since"). A skipped / failed / timed-out
  / lost step verified nothing and records nothing.
- The worker re-checks `isCurrent` after every await and tears down (lock,
  timer, subscription) when the run moved on. Nothing here reverts, stashes or
  resets the user's checkout.
