# backend/src/mergeRuns/resolverSpawn

Conflict-resolver spawn subsystem for merge runs. `../resolverSpawn.ts` is the
re-export facade (existing `./resolverSpawn.js` imports keep working). Spawn
*mechanics* stay separate from the *policy* that drives them. The waiter these
park on, its liveness bound and the flagged-conflict retry are documented in
[../CLAUDE.md](../CLAUDE.md).

## Map

- `park.ts` — `parkOnConflictResolver`: registers the bounded waiter
  (`../waiterLiveness.ts` `awaitResolverWaiter`), then **drops the per-task
  merge lock** and returns the `WaiterReleaseReason`.
- `spawn.ts` — spawn / notify / record mechanics: `spawnAndRecord`,
  `recordAndSpawn`, `respawnResolverForFlaggedConflict`.
- `existingResolver.ts` — `findExistingResolverSession`: the live resolver pty
  in a worktree (agent harness + `MERGE_INSTRUCTIONS.md` prompt + exact cwd).
  Shared by the flagged-conflict respawn and the manual `/merge`
  already-conflicted path, so neither starts a second writer.
- `handleOutcome.ts` — `handleResyncOutcome`: per `ResyncOutcome`, finalize
  (push `run.merged`), park on a resolver, cancel the run after a stash
  conflict, or record a `run.errored` entry. A non-signalled park release goes
  to `../resolverWaitFailure.ts` (preserve and stop — see the parent doc).

## Invariants

- **Release the per-task lock before waiting, after registering.** The
  resolver's `/complete` → `finalizeResolvedTask` takes that same lock to
  re-sync, FF main and signal the waiter; holding it across the park makes
  finalize lose `tryAcquire`, return `already-finalizing` without signalling,
  and the run hangs forever (resolver pty stranded — only finalize's worktree
  cleanup kills it). The waiter entry is recorded synchronously first, so a
  racing signal can't be missed. Because the lock is already released here,
  the merge-conflict outcome stays `'awaiting-resolver'` however the wait ends
  — callers must not release it again.
- Resolvers spawn through `queuedCreateSession` on the `priority` band
  (headroom above softCap, so a run can always get its resolver), deduped per
  `mr-resolver:<runId>:<taskId>`, with the run's cancellation `AbortSignal`
  (`../cancellation.ts`) and a 10-minute capacity timeout. Cancellation removes
  queued spawns; an allocation already in flight is awaited and its terminal
  reclaimed before the caller proceeds. An unconfirmed stop keeps the exact
  session ID and underlying error in the diagnostic.
- A spawn failure returns `spawn-error` and the task is errored — never
  notify `conflict` / register a waiter for a resolver that was never spawned
  (the run would block forever). `run.conflicted` is updated only on a
  successful spawn, so a task isn't counted both conflicted and errored.
- `inWorktree` (merge-conflict resolvers, never stash ones) passes `taskId` +
  `mcpScope: 'task-worktree'`: the task's reduced Lattice toolset and only the
  Lattice MCP (`../../mcp/CLAUDE.md`).
- Each spawned resolver's `{sessionId, lastProgressAt}` is mirrored on the run
  record (`run.resolvers`), so restart adoption keeps the progress timeout.
- `respawnResolverForFlaggedConflict` probes the detached terminal-server
  first: a live `MERGE_INSTRUCTIONS.md` agent at the exact normalized worktree
  cwd is **reattached** (keeping its prior `run.resolvers` entry); an
  unprobeable server (`null`) fails the attempt safely; only a confirmed
  absence spawns another. A normal task agent or shell must never be adopted
  as a resolver.
