# backend/src/routes/tasks

The task router, split by concern. `../tasks.ts` composes five sub-routers in
this order: worktreeModified → activity → crud → run → hooks. Per-route table:
[ROUTES.md](../ROUTES.md). Storage, worktrees and the spawn queue live in
`../../taskCache/`, `../../worktree/`, `../../spawnQueue/`.

## Map

**Graph overlays** — read-only against the disposable worktree (plain `exec`,
never `projectGit`):

- `activity.ts` — `POST /:id/activity` (Claude Pre/PostToolUse hook →
  `task-activity` WS focus beam). Owns the worktree→project path mapping and
  the exported `isManaged` filter that `../agentActivity.ts` and
  `worktreeModifiedParsers.ts` import — keep one copy.
- `worktreeModified.ts` — `GET /api/tasks/worktree-modified` (files changed by
  in_progress / ready_to_merge tasks, for `W`). Route wiring only; work lives
  in `worktreeModified{Service,Git,Cache,Constants,Parsers}.ts`. Keep the
  response shape, TTL and git timeout; loads are single-flighted per project
  and probe ≤ 8 worktrees at once (two git processes each).

**CRUD** — `crud.ts` wires routes (and the shared `textOrMarkdownBody`
parser) to handlers re-exported from `crudHandlers.ts`, a compatibility
barrel: `crud.ts` and tests import that path, so keep it stable.

- `crudList.ts` — list / summary / search / projects / get adapters, plus
  `partitionByProject`, the foreign-task integrity filter every
  project-scoped read runs.
- `listQuery.ts` — the pure progressive-disclosure pipeline behind
  `GET /api/tasks` and `/summary`; `buildListOutcome` turns a response over
  `LIST_RESPONSE_CEILING_BYTES` (256 KB) into a 413 carrying the summary.
  Stages in `listQuery{Types,Parse,Select,Sizing,Envelope,Summary}.ts`, deps
  one way: types ← parse/select/sizing ← envelope/summary ← outcome.
- `taskSearch.ts` — `GET /api/tasks/search`: AND-of-terms substring, title×3
  scoring. Defaults to EVERY lane, unlike the list (history is where the
  matches are).
- `crudCreate.ts` — create / batch-create (JSON array, `{tasks}`, markdown).
- `crudUpdate.ts` — patch / bulk-update / upsert / append-summary, over
  `crudUpdate{Body,Validation,Upsert}.ts` (markdown-or-JSON bodies, upfront
  validation, `classifyUpsertTarget`).
- `crudTransition.ts` — bulk transition (by `ids` or `fromStatus`) + reorder.
- `crudDelete.ts` — delete + cancel-queued-run. `markdownBatch.ts` — the
  markdown task grammar + `serializeTasksAsMarkdown`.

**Run / merge** — `run.ts` composes runRoute → resumeRoute → mergeRoute.

- `runRoute.ts` / `resumeRoute.ts` — `/:id/run` (pin + `isFreshlyRunnable`)
  and `/:id/resume`, both → `{accepted, queued}`.
- `startTask.ts` — `startTaskById` (worktree → pty → in_progress flip), shared
  with the workflow Start step; `startWithdrawal.ts` — withdrawal checks,
  teardown (`discardOrphanedSpawn`), CAP-parked checkouts.
- `resumeTask.ts` — the resume spawn. `colorSlot.ts` — stable palette slot,
  reserved until the flip lands.
- `harnessFactory.ts` — `selectHarnessCommand`: harness → run/resume command +
  pty `createSession` (injectable `proxyCreateSession` boundary).
- `mergeRoute.ts` — `POST /:id/merge`: 409 while a merge run / manual merge /
  post-merge hook is active. `manualMergeService.ts` (`runManualMerge`:
  project `run.lock`, fresh vs. already-conflicted, hook gate),
  `mergeResponses.ts`, `manualMerge{Guards,Locks,Types}.ts`.
- `_shared.ts` — `requireTaskStatus` (400 on the wrong lane), `logTaskRouteError`.
- `requestUtils.ts` — project resolution + pins (`?project=`, else a JSON
  body's `project`; non-absolute → 400), status checks, `normalizeBody`.
  `projectValidation.ts` — create needs an absolute path to a git repo.

**Queued spawns** — `queuedSpawn.ts`, a compatibility barrel (routes,
`recovery/queuedRunResume.ts`, the workflow Start step and tests import it),
over `queuedSpawnAdmission.ts` (dedupe keys, persisted run-queue policy +
`CLEARED_RUN_QUEUE_STATE`, `TaskStartWithdrawnError`), `queuedSpawnFailure.ts`
(`runSpawnThunk`) and `queuedSpawnEnqueue.ts` (enqueue + cancel).

**Hooks** — `hooks.ts` + `hooks/` + `finalizeResolved.ts`: `/complete`,
`/merged`, `/merge-aborted`, `/stash-resolved`. See
[hooks/CLAUDE.md](hooks/CLAUDE.md).

## Invariants

Routing and contract:

- Static paths (`/summary`, `/search`, `/transition`, `/worktree-modified`, …)
  register before `/api/tasks/:id`, or the segment is captured as an id.
- Paths, methods, status codes, response shapes and idempotency are public
  contract (Stop hooks, resolver curls, the MCP server) — don't change them
  when refactoring.
- `/run` and `/resume` **enqueue**: `accepted` means admitted, not started; the
  pty arrives on `task-spawned` (a non-CAP failure on `task-spawn-failed`). A
  client must not re-POST.

List / markdown:

- **The list defaults are the point** (active lanes, compact, newest 100,
  self-pricing envelope, 413 ceiling): an unbounded list was ~320k tokens on a
  mature board. Don't loosen them.
- `format=markdown` shares the pipeline except clipping: that doc round-trips
  through `/upsert`, which REPLACES descriptions, so clipping would destroy
  task text. A `limit`-capped listing carries `truncated=N/M` in frontmatter.
- Keep the markdown / `text/plain` body handling. Grammar: a metadata-only
  heading (`# {id=t_1, status=done}`) has an EMPTY title — "keep the title" on
  PATCH / an id-bearing upsert block, a 400 on create. A markdown PATCH parses
  in `singleTask` mode (later `#` headings are description, not dropped
  tasks). `serializeTasksAsMarkdown` backslash-escapes structure-like lines and
  the parser strips one backslash outside fences, so GET `?format=markdown` →
  POST `/upsert` is a no-op.

Delete / cancel:

- Delete and cancel-queued-run both clear spawn-queue state, so a removed or
  cancelled task can't later spawn a worktree. Cancel also aborts a run the
  queue already admitted (answers `inFlight: true`).
- Delete passes `keepBranchIfUnmerged`: a `lattice/*` branch with commits not
  on HEAD (the only copy of that work) survives, and the response adds
  `keptBranch: {name, unmergedCommits, hint}` (`keptBranchPayload`; the MCP
  `delete_task` leads with the hint), else `{ok: true}`.
- Delete takes the **per-task `mergeLocks` lock** after the pin check, before
  any side effect, held across worktree teardown + record removal — else it
  pulls a worktree from under a live `git merge` or erases the record
  mid-finalize, landing deleted work on main. A held lock is waited for up to
  `TASK_DELETE_LOCK_WAIT_MS` (5 s, `acquireBriefly`, as `/merge-aborted`), then
  **409** `{error, merging: true}` (the board toasts it). Seam:
  `createTaskDeleteHandler({cleanupWorktree, lockWaitMs})`.

Queued spawn / start:

- **Crash-safe retry accounting**: the attempt counter is bumped disk-first
  (`updateTaskCrashSafe`) BEFORE the spawn, so a process-crashing spawn still
  counts; a CAP re-queue undoes the bump; any other failure clears the
  run-queue state. Each queued thunk does the FULL spawn (worktree + pty).
- **A cancel / delete / lane change made during a start wins**:
  `startTaskById` re-checks after the checkout, before a CAP re-queue, and at
  the final `in_progress` flip — a compare-and-set under the task lock
  (`updateTaskWith`). A withdrawn start tears down its worktree + pty (keeping
  a checkout another start already claimed) and throws
  `TaskStartWithdrawnError` (`runSpawnThunk` neither toasts it nor touches
  run-queue state; a deleted task throws a plain Error). A CAP-rejected pass
  parks a teardown on the request signal, so a cancel before the retry still
  reclaims the checkout. The palette slot is picked inside that flip; a
  stored `colorIndex` is kept only while no other active task or reservation
  holds it.
- **At most one start per task at a time, whatever the entry point**: the
  task stays `open` until the flip, so a workflow Start step and a `/run`
  admitted during its checkout both pass `isFreshlyRunnable`, and the second
  setup's reconcile kills the first agent. The in-process `startsInFlight`
  chain (`isTaskStartInFlight`) makes the second wait, then withdraw if the
  task was claimed or run as a retry if the first failed
  (`startTaskConcurrent.test.ts`).
- **Only a successful terminal allocation flips a task to In Progress**. CAP
  always defers (whatever the legacy `throwOnCapacity`). Any other allocation
  error leaves the prepared checkout intact and propagates with no retry or
  cleanup (an uncertain outcome may have a live agent; an explicit retry goes
  through setup's reconciliation). `harnessFactory.ts` rejects with the
  original diagnostic for returned errors, not just thrown ones
  (`taskTerminalAllocation.test.ts`).

Resume:

- **Harness default**: a body with no valid `harness` resumes under the
  harness the task ran with (`Task.harness` via `resolveResumeHarness`), and
  a Pi resume reuses the recorded `piModel` (any resume: the recorded `effort`,
  and `model` while the harness is unchanged); only a task with no recorded
  harness falls back to Claude. An explicit body harness wins, and what the
  resume spawned is written back. Don't reintroduce "default to Claude" — it
  silently moved Pi/Codex tasks onto Claude.
- **Conversation resume policy**: `buildTaskResumeCommand` keeps the
  conversation and unrelated flags but replaces the old Pi `--model` / Codex
  yolo flags with the resolved Pi model and current `codexYolo`. Explicit task
  Resume only — keep it out of `buildRestoreCommand`, whose tab restoration
  must preserve the original launch flags (`taskResumePolicy.test.ts`).
- **Resume withdrawal**: re-checks status, worktree/branch identity and start
  time after preparation and at allocation settlement (plus the queue's
  AbortSignal); metadata is committed only after a final check under
  `updateTaskWith`. A withdrawn late allocation is killed by its own serverId
  via `terminalProxy`; resume cleanup never discards the existing checkout or
  older ptys. Withdrawal is `TaskStartWithdrawnError` (no event, no toast).

Merge: `/merge` on a task still mid-merge with a live resolver pty
(`findExistingResolverSession`) hands that resolver back (`existingResolver:
true`, `MERGE_INSTRUCTIONS.md` untouched) — never a second one; an
unreachable terminal-server falls through to the spawn.

## Tests

Named after the module — grep it in `backend/src/__tests__/`; plus
`taskResumeWithdrawal`, `resumeHarnessDefault`, `taskDeleteMergeLock`.
