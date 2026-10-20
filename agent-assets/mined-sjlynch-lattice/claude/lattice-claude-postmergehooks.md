# backend/src/postMergeHooks

Optional per-project **post-merge hook**: after a merge (per-task `/merge` or a "Merge All" run), Lattice spawns the user-configured harness with their prompt as a one-off agent, and the merge is **not** complete until that agent calls back — so a workflow Merge step / per-task merge response stays gated on it. Same scratch-dir + Stop-hook + registry-waiter shape as `pushRuns/`. `../postMergeHooks.ts` is the public facade. The home-scoped scratch contract (path guard, session setup, bounded cleanup, boot-sweep shell, run mirrors) is shared with push/QA runs: [../homeScratch/CLAUDE.md](../homeScratch/CLAUDE.md).

## Map

- `paths.ts` — one `createHomeScratchPaths(...)` call; scratch at `~/.lattice/per-project/<hash>/post-merge-hooks/<id>/` (`pmh_*`, outside the repo). `assertSafePostMergeHookPath` refuses any id/dir not strictly under that root or inside the project, so the bounded recursive cleanup can never reach the repo.
- `sessionSetup.ts` — `setupPostMergeHookSession`: thin wrapper over `setupHomeScratchSession` (mkdir, `seedClaudeTrust`, completion plumbing, brief).
- `trigger.ts` — `triggerPostMergeHook`: decide, claim, launch; returns an outcome immediately (callers block via the waiter).
- `session.ts` — `runPostMergeHookGate` (trigger + `waitForPostMergeHook`, owed-debt rounds), `endPostMergeHook`, `abortPostMergeHookForServerId`, `POST_MERGE_HOOK_MAX_WAIT_MS`.
- `registry.ts` — run registry (one running per project, newest 5 finished kept), `started`/`progress`/`finished` events, `getActiveHookForProject` / `getActiveHookForServerId`, per-run waiters resolved by `/complete` + `/abort` (`waitForPostMergeHook(id, maxWaitMs?)` → `'finished'` | `'expired'`), the `postMergeHookStore` mirror, and the re-export of `pendingTriggers.ts` (import it from here).
- `pendingTriggers.ts` — pre-record pending-trigger gate (per-project counter + listeners) that Phase C watches.
- `launchAbort.ts` — per-hook `AbortController` for the launch window; released once the launch is over.
- `stopHook.ts` — completion backstops, `postMergeHookAgentId` (`pmh:<id>`), activity-hook URL for graph beams.
- `stopHookGate.ts` — the Claude Stop-hook quiescence gate (post-merge analogue of `workflowRuns/stopHookGate.ts`).
- `commands.ts` / `instructions.ts` — launch command and the `POST_MERGE_HOOK.md` brief.
- `owed.ts` — durable owed-hook marker (below).
- `cleanup.ts` — wrapper over `homeScratch/cleanup.ts`; called from `/complete`, `/abort`, queued spawn failure and the boot sweep (`recovery/postMergeHookSweep.ts`, keeps live-PTY cwds).
- `types.ts` — `PostMergeHookRun` / `PostMergeHookSession` / `PostMergeHookStatus`.

## Launch invariants

- The trigger marks a pending trigger **synchronously, before reading settings**, cleared in `finally` — Phase C watches it so an uncached settings read can't masquerade as idle.
- Skips: `no-prompt`; `disabled` when `postMergeHookEnabled === false` even with a prompt (`isPostMergeHookEnabled` defaults ON); `already-running` (`getActiveHookForProject`).
- Re-check that gate and synchronously reserve + record the run immediately before the first setup await: the atomic claim that stops two callers spawning parallel hooks and keeps the hook visible to Phase C and the waiter for the whole launch window. A setup/spawn failure marks the run `errored` instead of throwing. Keep this own trigger/gate/waiter rather than push/QA's `startHomeScratchAgentSession`.
- Spawn on the spawn-queue `priority` band with a **per-hook** dedupe key (`post-merge-hook:<hookId>` — a per-project key handed a new hook an aborted hook's still-queued request) and the hook's launch `AbortSignal`.
- The pty runs with **`cwd = scratchDir`** (Claude reads its Stop hook, Pi its `.pi/extensions/`, from cwd); the brief's step 1 `cd`s into the project. Don't reintroduce `cwd = projectPath`: the Stop hook never fired and the merge run hung forever.
- Register the presence node for **any** harness (each reports activity through its own hooks); only quiescence re-adoption is Claude-only.
- The registry stores a canonical `projectPath`; lookups canonicalize too, else a path variant hides a live hook from Phase C.

## Completion invariants

- `stopHook.ts` installs **all three** backstops regardless of harness (a mid-run harness switch): Claude Stop hook, Pi completion extension, Codex `.codex/hooks.json` Stop hook (`../codexStopHook.ts`, `always` — scratch is fresh). Unused ones are inert; the prompt still asks for the explicit curl.
- A Claude Stop (`source=claude-stop-hook-*`) never finishes the hook directly — a hook may use subagents, so Stop fires early/repeatedly. `requestPostMergeHookStopComplete` waits for quiescence (no live subagents AND no signal for `PMH_STOP_HOOK_SETTLE_MS`), then finishes once. Otherwise a premature Stop completed the merge run, Phase C saw idle, and the frontend queue dispatched the next workflow's step onto the still-working agent. The explicit curl (`model-explicit-curl`), Pi's `session_shutdown`, Codex's Stop and error-tagged completions finish immediately. Fed by `../agentQuiescence.ts` keyed `pmh:<id>`, updated by `routes/agentActivity.ts`.

## Who waits for a hook

- **The wait is bounded** — nothing observes the hook's pty, so a crashed/killed agent never calls back and an unbounded wait held run.lock forever. `runPostMergeHookGate` passes `POST_MERGE_HOOK_MAX_WAIT_MS` (30 min, same as Phase C); on expiry the registry finishes the hook `errored`, reports `'expired'`, and the gate reclaims the pty via `endPostMergeHook`. A spawn error doesn't block at all.
- `endPostMergeHook(id, status, reason, {killSession?})` is the one teardown from *outside* the completion callback (`/abort`, tab close, expiry): gate cancel, node + quiescence drop, best-effort pty kill — or, with no pty yet, `abortPostMergeHookLaunch` to cancel the queued spawn — finish (unblocks every waiter), scratch cleanup.
- Closing the hook's tab through **either** route (`DELETE /api/terminals/:id`, `DELETE /api/terminal-tabs/:id`) calls `abortPostMergeHookForServerId` to end it `aborted` before the pty dies; a route that skipped it parked the merge run on run.lock for 30 min.
- `/abort` during launch is honoured by the trigger's re-checks after `setupPostMergeHookSession` and after `queuedCreateSession`: a hook no longer `running` gets its late pty killed and `skipped: 'aborted'`, never a `progress` event or node. Aborting also cancels the queued spawn, so the merge run behind it is released at once; that rejection maps to `skipped: 'aborted'` + scratch cleanup.
- **Inside a merge run**, `runPostMergeHook` is awaited **before** `finishRun` (`../mergeRuns/CLAUDE.md`), so `completed` already waits it out. Preserve that ordering.
- **Outside a merge run**, `routes/tasks/hooks/postMergeHookHelper.ts` `awaitPostMergeHookOutsideRun` (resolver `/complete`, `/merged`, `/stash-resolved`) fires only when no merge run is active and is awaited only by that HTTP callback — not by any workflow. Hence the workflow Merge step's **Phase C** (`workflowRuns/controlSteps/merge.ts`), which polls `getActiveHookForProject`. A new hook-firing path must be inside a merge run or visible to `getActiveHookForProject` while it runs — never a fire-and-forget spawn.

## Surviving a backend restart

The hook's agent outlives a backend restart in the detached terminal-server, and `resumeInterruptedMergeRuns` re-runs its merge. `postMergeHookStore` mirrors running hooks to `~/.lattice/per-project/<hash>/post-merge-hooks.json` on record / patch / finish (including a held Stop: `stopReceivedAt` / `stopActiveAt` / `stopBusy`), and boot re-adopts them before listen via `restorePostMergeHook` ([../recovery/oneOffRunResume/CLAUDE.md](../recovery/oneOffRunResume/CLAUDE.md)). A re-adopted hook is visible again, so a resumed merge run's trigger reports `already-running` and awaits it, Phase C waits, and `POST /api/merge-runs` 409s — without the mirror it fired a second hook and the orphan's `/complete` 404'd.

## An owed hook survives a restart (`owed.ts`)

Both firing paths are in-memory decisions made after the merge, so a backend killed between a task landing in QA and the hook firing silently skipped it. Hence:

- `worktree/finalize.ts` records a durable debt (`per-project/<hash>/post-merge-hook-owed.json`, only when a hook is configured) the moment a task lands in QA. The trigger settles it once it has decided (started / aborted / not configured); a spawn error keeps it.
- `already-running` keeps it too (that hook may predate these merges, or be a dead record restored as running for its lost-grace window): the gate waits it out and, if still owed, fires a fresh hook (at most 3 rounds). **Except** when the running hook started at or after the marker's `since` (rewritten on every merge): it IS the hook for those merges, so the trigger settles the debt — else a backend dying between spawn and clear yields a second hook.
- Every path that could fire the hook honours the marker: merge-run teardown (`merged.length > 0 || owed`; a cancelled/halted run clears it instead — no hook on cancel), the workflow Merge step's Phase C (`fireOwedPostMergeHook` before waiting, raced against the workflow's cancel/error so a cancel frees its `workflow-merge:*` run.lock at once; `runPostMergeHookGate`'s `shouldStop` then stops further rounds), and boot step 5a (`recovery/owedPostMergeHooks.ts`, which defers to any active merge/workflow run or held/stale-resumable run.lock).

Tests: named after the module — grep `postMergeHook` in `backend/src/__tests__/`.
