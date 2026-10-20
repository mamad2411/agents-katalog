# backend/src/server

Named backend bootstrap helpers used by `index.ts` after process guards are installed.

- `config.ts` — computes `PORT` (`backendPort()`), default project root
  (`LATTICE_DEFAULT_ROOT` overrides it — the isolated e2e instance uses a
  scratch dir), and the `backendOrigin` field of `getBackendServerConfig()`.
- `bootGuards.ts` — `runBootGuards()`, awaited at the very top of `index.ts`
  (before `installProcessGuards`, i.e. before crash-log adoption, Pi setup, the
  terminal-server handshake and recovery). Refuses — message + exit 1 — when
  the backend's code dir or cwd is inside a `.lattice/worktrees/` checkout
  (override `LATTICE_ALLOW_WORKTREE_BACKEND=1`, only with an isolated HOME and
  ports), and when the port is already held: a throwaway bind on
  `127.0.0.1:PORT` (ms, unlike a connect probe that Windows takes ~2 s to
  refuse), then `/api/health` names a live Lattice backend vs a foreign holder.
  Check-then-recover, not a held claim: `listen()` still happens after
  recovery, so two backends started within the same few seconds are not
  caught — a stray one started beside a long-running live one is. Imports only
  node builtins. Tests: `__tests__/bootGuards.test.ts`.
- `app.ts` — builds the Express app, mounts middleware/routes, and installs the global JSON error middleware last.
  The first routers mounted are the restart-drain admission gate (new
  workflow / merge / task / push / QA starts answer 503 `backend-restarting`
  while the dev runner prepares a restart) and the token-guarded
  `/api/internal/restart-drain/*` handshake — see `../restartDrain/CLAUDE.md`.
  Known request-body parser errors retain their 4xx status and return actionable
  JSON. Their log includes bounded route metadata only: the parser error's body
  and message may contain private or very large submitted summaries. Express's
  own 4xx client errors (e.g. an undecodable `:param` percent-escape → 400)
  keep their status the same way, unless they set `expose: false`. Unexpected
  route failures still log the error and return 500; sent headers delegate to
  Express's final handler.
- `http.ts` — creates the HTTP server and attaches the WS dispatcher.
- `startup.ts` — boot ordering / invariants:
  1. fire-and-forget harness detection plus best-effort Pi setup
     (`ensurePiSubagentsInstalled()`, `ensurePiMcpInstalled()`, and
     `reconcilePiModelsJson()`); these must never block listen or throw out of
     startup;
  2. `runPreListenStartupRecovery()` awaits `ensureTerminalServer()`, then
     `startSpawnQueue()` to prime terminal-session accounting, then
     `recoverOrphanedTasks()` (including one-off run adoption) while the API
     is still closed;
     security review ownership/presence is also recovered before listen through
     `opengrep/reviewRecovery.ts`, so delayed callbacks find their durable record;
  3. establish `beginWorkflowRecovery()` before `listen()` on `127.0.0.1` only
     (not `localhost`, not LAN-visible);
  4. after listen, `runBootRecoveryChain()` starts
     `resumeInterruptedWorkflowRuns()`. The `/api/workflows/:id/run` +
     `/api/workflow-runs` lifecycle routes wait for registry readiness (bounded
     wait, then 503 `workflow-recovering`). `workflowRunResume.ts` calls
     `onRegistryReady` once all recovered records and surviving terminal
     ownership are installed, **before** iterating redispatch decisions. This
     releases requests to an authoritative registry before full recovery
     settles, so callbacks need not wait behind lengthy pre-run work;
  5. once workflow dispatch decisions are applied, the chain awaits
     `resumeInterruptedMergeRuns()`, then `fireOwedPostMergeHooks()`, and finally
     starts `startCallbackOutboxLoop()` when that chain settles. Merge-run resume
     skips projects with an active workflow, which owns their merge pipeline.
     Redispatched agent pre-run work carries on detached; it must not delay
     merge-run resume, owed hooks or outbox replay. Replay waits for run
     adoption / redispatch so undelivered callbacks find their owners.

  In parallel with that post-listen chain, `resumeRunsAfterListen()` starts
  `startBootWorktreeSweep()` → `resumeQueuedTaskRuns()`: expensive orphan
  cleanup stays after listen, and queued tasks wait for cleanup to finish.
  Periodic sweeps, the low-disk monitor and terminal-registry watch also start
  here; `ensureCallbackScript()` runs immediately, independently of replay.
  The security review orphan sweep runs here too, preserving running reports
  for the review watchdog before reclaiming their guarded scratch directories.
  Task second opinions also resume after listen (`resumeInterruptedTaskReviews`),
  without blocking workflow adoption or the queued-run recovery chain.
  Recovery policy belongs to [recovery/CLAUDE.md](../recovery/CLAUDE.md),
  workflow lifecycle policy to [workflowRuns/CLAUDE.md](../workflowRuns/CLAUDE.md),
  and callback delivery to [callbackOutbox/CLAUDE.md](../callbackOutbox/CLAUDE.md).

Command reference (documentation only; cwd: `backend/`): `npm run build`, `npm test`,
`npx tsc --noEmit`. See [__tests__/CLAUDE.md](../__tests__/CLAUDE.md) for
isolation requirements; `bootRecoveryPreRunNonBlocking.test.ts` covers the
detached pre-run invariant.
