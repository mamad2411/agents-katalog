# backend/src/recovery

Boot-time crash recovery plus two periodic sweeps. `../recovery.ts` is the facade and also holds the pre-listen chain (`recoverOrphanedTasks`), `startBootWorktreeSweep` and step 4. Not here: task-DB backup/restore (`../taskCache/CLAUDE.md`); call sites (`../server/startup.ts`).

## Boot order

Other docs cite these step numbers — keep them stable.

1. `restoreAllProjectsFromBackup` — repair task DB files before any task cache read.
2. `recoverPendingSnapshots` — restore copy-based working-tree snapshots left by crashed merge/finalize work.
3. `sweepOrphanedWorktrees` (`worktreeSweep.ts`) — **after listen, not awaited** (pre-listen, 1000+ legacy orphans kept the UI on "Scanning…"); step 6 waits for it. Removes only Lattice-managed worktrees no active task owns, two at a time:
   - uncommitted edits are archived first (`worktree/discardArchive.ts`; never auto-restored by step 2); if archiving fails the orphan stays;
   - unmerged `lattice/*` branches come from ONE `for-each-ref --no-merged=HEAD` (per-branch `rev-list` only if that fails; unreadable = unmerged). An orphan with unmerged commits keeps its **branch** (`keepBranchIfUnmerged` — the only copy of the work) but loses its checkout; an Open/Backlog task (may be re-run) keeps both;
   - then, detached, `sweepWorktreeResidue` (below).
3a. `resumeInterruptedOneOffRuns` (`oneOffRunResume.ts`) — **before listen**, so a callback (or outbox replay) never meets an unknown id: re-adopts push / QA / post-merge-hook runs whose pty survived. See [oneOffRunResume/CLAUDE.md](oneOffRunResume/CLAUDE.md).
3b. `sweepOrphaned{Push,Qa,PostMergeHook}Sessions` (`pushSessionSweep.ts` etc.) — reclaim scratch dirs whose `/done` cleanup lost its EBUSY race, never fired, or whose session died, via `homeScratch/sweep.ts`: live-PTY cwds kept, bounded to `~/.lattice/per-project/<hash>/{push,qa,post-merge-hooks}/`. After 3a, so a dir with no live PTY is truly stale.
3c. `sweepStaleClaudeProjectEntries` (`claudeConfigSweep.ts`) — prune `~/.claude.json` `projects[<cwd>]` entries for a vanished Lattice worktree/scratch cwd (each spawn pre-seeds one; nothing else removes them). After 3b, so just-reclaimed dirs count. GLOBAL, under `claudeTrust.ts`'s config mutex; the long-lived terminal-server also prunes every 5 min.
3d. `sweepOrphanedClaudeConfigTempFiles` → `claudeTrust.sweepOrphanedClaudeConfigTemps` — delete `~/.claude.json.lattice-<pid>-<ts>.tmp` (and `mcpSecrets.json`) temps of a hard-killed writer; skips temps < 60 s old so a live terminal-server's in-flight write is never touched.
4. Branch repair (`recoverTaskIfBranchWasDeleted`) — a `ready_to_merge` task whose branch is gone moves to `qa` (finalize cleanup already ran; `mergedAt` re-stamped so an older QA verdict can't promote it). **Only on a confirmed absence** (`.git` exists, `checkBranchExists` exit-0-no-match); a git failure or missing `.git` leaves the task alone, per task (a transient refs error read as "deleted" lost unmerged commits).
4a. `resumeInterruptedWorkflowRuns` (`workflowRunResume.ts`) — after listen, **before** step 5. Applies `classifyWorkflowRunResume` (phases, parallel groups, Stop re-arm: [workflowRuns/CLAUDE.md](../workflowRuns/CLAUDE.md) "Surviving a restart") to each run in `per-project/<hash>/workflow-runs.json`: live agent step → re-adopted (`adoptWorkflowStepSession` + presence node) so its pending `/complete` advances the run; control step → re-dispatched (re-runnable, as step 5 relies on), a Push re-attaching to its live push session (3a) instead of pushing twice; `pending` → re-dispatched unless a session is positively alive; `completing` → completes without replaying the prompt; lost Run tests → advances (`advancePastLostTestStep`); other lost agent step → errored, never left hanging.
   - One probe per sweep; `null` ("couldn't ask") re-adopts, so a wedged terminal-server can't mass-error healthy runs.
   - Register every persisted run (and surviving parallel member) of a project before the first redispatch checkpoints its file, or that write drops unloaded siblings. Members are classified independently, each with its own retry budget; a lost member fails the run and cancels its siblings.
   - `markAgentReadopted` at registration, before callbacks are released (live-subagent tracking died, so the Stop gate needs `READOPTED_SETTLE_MS` of silence); other outcomes drop the mark. A Stop the dead process held (`run.stopReceived`) is re-armed — the idle agent won't Stop again.
   - Settles per run once its dispatch is applied (a re-dispatched step counts at `waitForStepPreRunBegin`), so a minutes-long Opengrep pre-run doesn't hold steps 5 / 5a and outbox replay.
5. `resumeInterruptedMergeRuns` (`mergeRunResume.ts`) — after listen (resolvers call the API). Skipped for a project with an active merge run or **active workflow run** (its Merge step owns the pipeline; a second run would double-process tasks). Resumes on a stale (dead-PID) run lock — or the interrupted-run marker step 2 leaves when it retires one (`projectRunLock/interruptedRun.ts`) — labelled `merge-run` or `workflow-merge:*` / `workflow-push:*` (`isResumableInterruptedRunLock`; fallback when a workflow's mirror is gone; a paused retry budget blocks it), only while `ready_to_merge` tasks remain (else the stale lock is retired; `clearStaleLockOrThrow` re-checks liveness). `manual-merge` and workflow `Start` locks are deliberately not resumed. `startMergeRun` is awaited up to run registration so 5a sees the run (else an owed hook raced it and fired twice).
5a. `fireOwedPostMergeHooks` (`owedPostMergeHooks.ts`) — after 4a + 5: fire a hook a pre-restart merge still owes (`postMergeHooks/owed.ts`) unless an active merge or workflow run, a held or stale-resumable run.lock, or an uncleared interrupted-run marker owns the project (that merge fires it; a hook now would edit main under its snapshot).
6. `resumeQueuedTaskRuns` (`queuedRunResume.ts`) — after step 3: re-enqueues spawn-queued runs (`Task.runQueued`), so a half-created worktree is reconciled by the re-run, not reclaimed.
6a. `resumeInterruptedTaskReviews` (`taskReviewResume.ts`) — after listen,
   requeues in-progress `reviewing` records and finishes interrupted `rerun`
   teardown intents. Per-task single flight dedupes completion replays; the
   four-wide review queue bounds CLI work. Open reruns use step 6 normally.
   `sweepTaskReviewScratch` reclaims guarded orphan scratch while preserving
   active reviews; its per-task scratch lock also serializes against CLI setup.

## Worktree residue sweep

`worktreeResidueSweep.ts` reclaims what a part-failed `git worktree remove --force` leaves on Windows (a locked file, e.g. a running `esbuild.exe`, stopped it after git dropped the registration and `.git`). It may delete only direct children of a known project's `~/.lattice/worktrees/<hash>/` that are: unregistered; unowned by an active/queued task; without a live pty; without a `.git` marker, or with only a `.git` FILE naming a `<commonDir>/worktrees/<id>` of this repo that is gone while the common dir is intact; not a reparse point; older than 10 min. Same carve-out as `worktree/reconcile.ts`'s `fs.rm`, re-checking `.git` + registration right before each guarded delete. A locked dir backs off in memory (30 min doubling, ≤ 8 h); `notifyDiskSpaceFreed()` after any attempt. Never touches unknown projects' hash dirs or legacy `<repo>/.lattice/worktrees`.

`worktreeResidueGitMarker.ts`'s `entryExists` reads any non-ENOENT error as "present" (keep the dir); `worktree/reconcile.ts`'s same-named function rethrows — do not merge them.

`worktreeResidueSweepLoop.ts` — passes every 30 min and on a disk wait (`requestWorktreeResidueSweep` from `diskPressureMerge.ts`, ≤ 1 per 2 min). Single-flight plus a per-project guard against the boot pass; skips a project with no `.git` or zero task records, and the whole pass when the terminal-server is unreachable.

## Other files

- `inProgressSweep.ts` / `inProgressSweep/` — periodic (60 s) auto-complete of an `in_progress` task whose PTY is dead and whose branch has commits. See [inProgressSweep/CLAUDE.md](inProgressSweep/CLAUDE.md).
- `retryBudget.ts` — durable replay journal (`per-project/<hash>/recovery-attempts.json`).
- `liveSessions.ts` — `collectLiveSessionCwds` (`null` = terminal-server unreachable: "can't tell" ≠ "none"), `hasLiveSessionAtOrUnder`, `normalizeCwd` (case-insensitive on Windows).
- `projectIteration.ts` — `forEachKnownProjectSafely`; `concurrency.ts` — `forEachWithConcurrency`.

## Safety invariants

- Recovery is best-effort: log a failed phase/project and keep booting.
- Iterate projects only via `forEachKnownProjectSafely` (one broken project can't block others). It and the per-task loops fan out 8 wide (`forEachWithConcurrency`; a serial walk delayed `listen` by seconds). Keep per-item try/catch inside the callback — the helper doesn't swallow errors.
- Never run stale merge-run resume before the server is listening.
- Retry budget: charge each automatic workflow redispatch and boot merge replay durably **before** side effects (a process-killing failure still costs its attempt); three interrupted attempts at an unchanged checkpoint pause replay (persisted reason + run error event). Not attempts: session adoption, durable completion advancement, a control-step re-run that only waits on a just-re-adopted session (`isWaitingOnLiveSession` — charging it paused healthy runs after three restarts). Step/task-lane progress and changed remaining merge-task IDs reset budgets; only an explicit user `POST /api/merge-runs` resets the merge allowance (never internal callbacks or auto-restarts).
- A paused workflow's stale control lock must not bypass its budget via the step-5 fallback. An invalid journal is preserved and blocks automatic replay, never an explicit `POST /api/merge-runs` (reset failure logged, run proceeds); `GET /api/merge-runs/recovery?project=…` shows it.
- No raw recursive deletes: worktree removal goes through `cleanupWorktreeForTask` / `git worktree remove`. The one exception is `worktreeResidueSweep.ts` — do not widen what it may delete.
- Worktree reclamation needs a readable, nonempty task inventory and an authoritative terminal-session inventory: a corrupt task DB may load empty, so zero task records preserve every checkout. Preserve queued tasks' checkouts and live PTY cwds (descendants too); compare ownership paths case-insensitively on Windows.
- Honor explicit git worktree locks; count only successful cleanup as reclaimed; use `worktree list --porcelain -z` for exact paths. Never globally prune missing registrations during the sweep (skipped active or user-managed checkouts may be offline); exact orphan removal handles its own registration, even for a manually deleted dir.

Tests: named after the module — grep it in `backend/src/__tests__/`.
