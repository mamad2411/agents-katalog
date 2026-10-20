# backend/src/terminalRegistry

The durable terminal-tab registry: what brings the sidebar's tabs — and the
harness conversation inside each — back after a backend restart, a closed
browser, a `Ctrl+C` of the dev server, or a reboot. Facade: `../terminalRegistry.ts`.
Not here: the ptys themselves (`../terminal/`), the spawn chokepoint that
creates records (`../terminalServerClient/`), the frontend reconciliation
(`frontend/src/terminal/terminalRegistrySync.ts`).

## Map

Model and store:

- `types.ts` — `TerminalRecord`, `TerminalOwner` (each owner documented), events.
- `store.ts` — `TerminalRegistryStore` over `per-project/<hash>/terminals.json`;
  `endWhere` serves the kill paths (`terminalProxy.ts`, tab DELETE) + exit watcher.
- `recordCodec.ts` — untrusted-file codec (a record missing anything
  load-bearing is dropped, not repaired) + retention prune.
- `labels.ts` — tab labels over `../shared/terminalLabels.ts` (shared with the
  frontend, so a restored tab reads like the original).
- `startupSupersede.ts` — `endSupersededStartupRecords` (below).

Session identity:

- `sessionIdentity.ts` — `assignHarnessSessionId` pins the conversation at
  launch (Claude `--session-id <uuid>`, Pi `--session-id lattice-<uuid>`);
  `agentSessionFromCommand` reads it back off a live pty's command.
- `codexDiscovery.ts` — learns a Codex thread id after the fact (no pre-set
  flag): candidate pick, registry write, polling.
- `codexRolloutScan.ts` — rollout parsing, bounded reads, shared caches; depends
  only on `harnessPaths.ts` + `sessionFiles.ts`, never the store/coordinator.
- `codexTaskActivity.ts` — display-only graph beams for task/merge Codex
  sessions on the hosted JS runner (its nested calls bypass CLI hooks).
- `harnessPaths.ts` / `sessionFiles.ts` — where each harness keeps transcripts
  and the IO over them (incl. `findClaudeConversationId`).

Restore and relaunch:

- `restore.ts` — `restoreProjectTerminals`: per-record decision (matrix in its
  header), `checkOwner`, `tryAdoptOrphan`.
- `restoreRelaunch.ts` — `enqueueRelaunch` (spawn-queue thunk), `planRelaunch`,
  `markRelaunchFailed`; imports only the `RestoreDeps` TYPE back (no cycle).
- `restoreCommand.ts` — `buildRestoreCommand` + `RESTORE_NUDGE` (matrix in header).
- `commandParse.ts` — tokenizer with per-harness value-taking flags.
- `interruption.ts` — `detectInterruption` / `decideInterruption` (evidence
  rules in header); re-exports `sessionFiles.ts`.
- `watch.ts` — every 3 s: exit tracking, Codex task activity; its
  terminal-activity subscription (keeps that poller always on) stamps `lastBusy`.

## Surfaces

`routes/terminalTabs.ts` (`/api/terminal-tabs`), `ws/endpoints/terminalTabs.ts`
(`/ws/terminal-tabs`, `TerminalRegistryEvent`). Settings: `restoreTerminalsOnOpen`
(`always` | `ask` | `never`), `restoreNudgeAgents` (default on),
`restoreNudgeUserTabs` (default off). `Task.agentSession` is copied from the
spawn so `routes/tasks/resumeTask.ts` can truly resume a matching harness.

## Invariants

Ownership and identity:

- The BACKEND is the sole creator of records (`recordSpawnedTerminal`,
  `../terminalServerClient/recordSpawn.ts`); the frontend only patches
  decorations. The backend-minted id is the tab id; every spawn site returns it
  (`terminalId`) alongside `serverId`.
- Never touch a pty of another executor instance; "can't list sessions" is
  never "no sessions" (an unreachable executor changes nothing).
- Never stack a session flag on a command that already names a session
  (`--resume`, `-c`, …).
- `launch` is the command BEFORE Lattice injection, and a relaunch never
  overwrites it (else the next restore resumes a resume). Codex title config,
  system-prompt files and task-worktree `--strict-mcp-config --mcp-config=…`
  (from `launch.mcpScope`) are re-injected by the spawn chokepoint — never
  bake them into `buildRestoreCommand`.
- Exported names stay importable from both the facade and their module
  (callers and tests use both).

Ending, closing, retention:

- `end()` REMOVES a record for `exit` / `closed` / `killed` / `owner-finished`
  and KEEPS it with its marker for `cwd-missing` / `restore-failed` (the UI
  shows why; the user can retry). Re-ending for the same reason keeps the
  original `ended.at`, so retention counts from the first failure.
- Ended records are pruned (`ENDED_RETENTION_MS`, 7 days) only when the file is
  loaded — once per project per process — and never a `closePending` one.
- Registered DELETE calls `requestClose()` BEFORE any kill IO: durably marks
  `closed` + `closePending`, keeps the pty identity, emits only an upsert until
  kill/404 confirms absence. An uncertain kill returns a retryable 503 (same tab
  id). Only a confirmed `closed` end discards it; restore/discovery writes
  can't clear the intent; only `recordRelaunch()` (real spawn bookkeeping) may
  hand a late pty to the tombstone, which stays reclaimable.

Restore:

- Single-flighted per project **including while its relaunch thunks run**
  (second pass → `already-running`), the lock release identity-checked so an
  old pass's guard timer can't drop a newer lock, held at most
  `RELAUNCH_LOCK_MAX_HOLD_MS` (10 min). Safe to re-run.
- The on-open pass never retries `cwd-missing` / `restore-failed` (it
  re-reported the same drop every reload and reset retention); only the
  explicit "Restore tabs" (`?retry=1` → `retryFailed`) does.
- Relaunch only `user` (cwd exists) and `task` (still `in_progress` with its
  worktree) owners. `merge` NEVER — the merge-run recovery / a re-clicked merge
  spawns its own resolver, and a racing relaunch puts two Claudes on one
  conflict. `startup` never (`useStartupTerminals` re-seeds). One-shot runs
  (push / QA / post-merge / workflow step / security review) are never
  resurrected — ended `owner-finished`; their own recovery
  owns them (a restore must not launch a second security review). Any owner's
  still-live pty is adopted.
- Orphan adoption takes only an unclaimed AGENT pty with the same cwd +
  harness (shells / startup commands would claim any pty in the folder), never
  one live on another record (even one excluded from the pass); retried records
  adopt too, so nothing spawns beside a live pty. Adoption clears `ended` /
  `relaunching` before `restored`; an orphan replaces `agentSession` with its
  command's (even unknown), clears `lastBusy`, restarts Codex discovery.
- A relaunch clears the dead `serverId` first (every client shows "restoring";
  no pane attaches to a dead id), queues at `batch` priority, re-checks the
  record before spawning, kills a pty whose tab closed mid-spawn, throws
  `SpawnCapacityError` on CAP so the queue retries, and ends `restore-failed`
  at the FIRST failure's `at`.
- A `--resume` relaunch claims its conversation (in-process, before any
  await) and is refused — `restore-failed` naming the holder — while another
  live tab runs it (Claude tabs resolved via `findClaudeConversationId`): an
  in-tab `/resume` points a new tab at a dead tab's conversation, and two
  processes on one transcript interleave and corrupt it.

Watch:

- Read sessions LIVE (`proxyListSessionsOrNull`), never the activity poller's
  shared snapshot (`proxyListSessionsShared`): a snapshot predating a spawn
  reports it missing, and the verdict "ended — exit" deletes the record. Even a
  live read has that window, so a record written at/after the view's
  `listedAt` (`isNewerThanLiveView`) is exempt: the watch defers its exit to the
  next tick; restore treats it as live (adopt, never relaunch beside it).
- Missing pty + same instance ⇒ exited ⇒ end; different instance ⇒ leave for
  restore. `noteBusy` stamps only a record still on the pty its snapshot named.

Startup tabs:

- `endSupersededStartupRecords`: a new `startup` record ends older records of
  the same `startupId` only when their pty is definitely dead (no `serverId`,
  or another executor instance) — else each restart under `never` / a declined
  `ask` left another dead tab. Same-instance ones are left to the exit watcher
  (ending a live one orphans a process with no tab to kill it).
- The frontend startup stale-drop
  (`frontend/src/components/sidebar/hooks/startupSeedPlan.ts`) must skip
  registered tabs — closing a dead-pty tab there DELETEs the record and leaves
  nothing to restore.

Codex discovery:

- Codex writes its rollout on the FIRST TURN, so discovery polls until the id
  is known or the record ends (backoff, 24 h backstop), and restore tries once
  more before relaunching an id-less tab (else `resume --last` — the folder's
  newest thread, maybe another tab's).
- Fresh pick = earliest unclaimed thread that STARTED within
  `CODEX_FRESH_START_WINDOW_MS` of launch (an idle tab mustn't claim a later
  tab's thread); after a `resume --last` relaunch, the NEWEST by mtime.
- Creation floor = record `createdAt`, never the relaunch time (resume appends
  to the ORIGINAL rollout, in its original day-dir); only the mtime pre-filter
  keys on `restoredAt ?? createdAt`. Adopted orphans persist their own
  `codexDiscovery` bounds. A scan discards its evidence if the record changed
  pty / provenance while it read.
- The listing cache is keyed by `(root, days)` only (`days` clamped 2..120;
  entries replaced, never evicted) — another key dimension makes it unbounded.
  The meta cache is a capped FIFO. A truncated first line (metadata can exceed
  8 KB; read up to 256 KB) never pins a conversation.

Claude conversation and nudge:

- The pinned Claude id names the PROCESS, not necessarily the conversation:
  after an in-tab `/resume` its lines land in the OTHER conversation's
  transcript. `findClaudeConversationId` scans the cwd's transcripts modified
  since the tab's CREATION (not its last relaunch), newest first, for the last
  line whose `session_id` is the pinned id; the relaunch resumes and records
  that conversation (`source: 'transcript-scan'`).
- `decideInterruption`: nudge only on open + non-idle; any idle evidence
  vetoes; unknown never nudges. Task/merge tabs nudge unless
  `restoreNudgeAgents` is off; user tabs only with `restoreNudgeUserTabs`.
- `codexTaskActivity.ts` never changes task state or controls a pty; close,
  ambiguous identity, completed tasks and replacement ptys suppress it, and
  replay before a relaunch's timestamp is ignored.

## Pointers

- Tests: grep `terminalRestore`, `terminalRegistry`, `terminalTabs`,
  `terminalStartup`, `codex` in `backend/src/__tests__/`
  (`terminalRestoreTranscripts` uses real on-disk Claude / Pi / Codex files).
- Related: `../terminal/CLAUDE.md`, `../terminalServerClient/CLAUDE.md`,
  `../spawnQueue/CLAUDE.md`, `frontend/src/terminal/CLAUDE.md`.
