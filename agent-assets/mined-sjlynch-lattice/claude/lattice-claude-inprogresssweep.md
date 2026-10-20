# In-progress recovery sweep

Periodic recovery for `in_progress` tasks whose PTY is dead and whose branch
has commits, covering missed completion callbacks (Pi's extension and the
explicit `/complete` curl are best-effort). The stable public facade
is [../inProgressSweep.ts](../inProgressSweep.ts); preserve its exports.
See the [parent recovery guide](../CLAUDE.md) for the boot pipeline.

## Navigation

| File | Responsibility |
|---|---|
| [../inProgressSweep.ts](../inProgressSweep.ts) | Public loop, sweep, result type and interval exports. |
| [config.ts](config.ts) | Five-minute age gate and default 60-second interval. |
| [scheduler.ts](scheduler.ts) | Singleton timer lifecycle and overlapping-tick prevention. |
| [sweep.ts](sweep.ts) | Candidate collection, bounded probing, verdict accounting and no-commit cache. |
| [eligibility.ts](eligibility.ts) | Read-only `decideAutoComplete` and typed skip/complete verdicts. |
| [complete.ts](complete.ts) | Fresh-task checks, Pi diagnostic and crash-safe task mutation. |

## Pass and eligibility

- The first tick waits one full interval; starting the loop is idempotent and
  the timer is unref'd. `runInProgressSweepTick` skips overlapping ticks (a
  pass is one git spawn per candidate, so a big board or wedged git would
  stack passes) and releases its guard even if a pass throws.
- Reuse one authoritative live-session snapshot from
  [../liveSessions.ts](../liveSessions.ts) for the pass. `null` means the
  detached executor is unreachable or unprobeable: skip the whole pass and
  retry next tick. It is not evidence that PTYs are dead.
- Collect known projects' `in_progress` tasks, then probe at most eight tasks
  concurrently through `../concurrency.ts`. Catch errors per task; a failed
  project's task listing is logged and skipped without blocking other projects.
- Keep `eligibility.ts` read-only and mutation ownership in `complete.ts`.
  Skip `reviewing` / `rerun` tasks: their review owns completion after PTY exit.
  Missing `worktreePath` or `branch`, age below `MIN_AGE_MS`, a live PTY at the
  exact normalized worktree cwd, a failed `branchCommitCount` probe, or zero
  commits ahead of the project's HEAD must each prevent auto-completion.
  Age uses `startedAt`, falling back to `createdAt`; cwd normalization is
  case-insensitive on Windows. A dead PTY alone is insufficient.
- `sweep.ts` caches `no-commits` verdicts by `(task id, branch)` for ten minutes
  (`NO_COMMITS_BACKOFF_MS`). During backoff it skips probing and warning;
  repeated no-commit probes keep the warning quiet. Other evaluated verdicts
  clear that entry, and each finished pass prunes keys to current candidate
  task/branch pairs. The cache does not automatically resume tasks. (That
  state can't change until the user resumes the task; re-probing it every
  minute cost a git spawn + a log line per stuck task per pass.)
- `too-young` and `session-live` are silent, uncounted skips. Other eligibility
  skips are accounted for; no-commit skips remain counted during backoff.

## Mutation boundary

- After the awaited commit probe, `autoCompleteStuckTask` re-reads the task.
  Require it to exist, still be `in_progress`, and match the snapshot's
  `updatedAt`, `worktreePath` and `branch`. Otherwise return `stale` silently
  and let a later pass re-evaluate it. These checks protect changes from a
  concurrent Resume, lane move, deletion or real completion callback.
- The Pi shutdown sentinel supplies diagnostic context for the log.
- Use `updateTaskCrashSafe` for `in_progress` -> `ready_to_merge`, setting
  `completedAt`. It persists disk before updating cache; a failed or missing
  update is an error outcome, not a successful flip.

## Contract references

- [inProgressSweepEligibility.test.ts](../../__tests__/inProgressSweepEligibility.test.ts)
  covers eligibility skips and a committed, old task with no live PTY.
- [inProgressSweepComplete.test.ts](../../__tests__/inProgressSweepComplete.test.ts)
  covers unchanged-task completion, stale snapshots and failed writes.
