# One-off run resume (push / QA / post-merge hook)

Boot step 3a of the [parent recovery guide](../CLAUDE.md): re-adopts push runs,
QA e2e runs and post-merge hooks whose agent survived a backend restart in the
detached terminal-server. The public facade is
[../oneOffRunResume.ts](../oneOffRunResume.ts) (exports, the pure
`classifyOneOffRunResume` policy, the typed boot sweep); internal modules never
import it.

## Map

- `contracts.ts` — shared types and timing constants (`LOST_SETTLE_GRACE_MS`
  90 s, `ONE_OFF_WATCH_INTERVAL_MS` 30 s, `READOPTED_HOOK_MIN_WAIT_MS` 5 min).
- `adapters.ts` — per-kind push / QA / post-merge behaviour (load, restore,
  re-adopt bookkeeping, settle-as-lost) and the re-adopted hook's wait.
- `watch.ts` — the liveness-watch singleton: registry, timer, tick,
  reset/debug helpers. It stores bound run operations, not the facade.

## Invariants

- Runs **before listen**: each registry mirrors its RUNNING records to
  `~/.lattice/per-project/<hash>/{push-runs,qa-runs,post-merge-hooks}.json`
  (`homeScratch/persistence.ts`), and the first callback (or the callback
  outbox's replay) must find its record — an unknown id 404s `/done` /
  `/verdict` / `/complete`, idles the terminal forever, drops a QA pass's
  qa → done, and lets a resumed merge run fire a second post-merge hook (or
  Phase C read "idle" beside the orphan).
- Runs before the boot scratch sweeps (3b), which keep only live-pty dirs.
- One terminal-server probe per sweep. A pty found at the record's scratch cwd,
  **or an unprobeable server** (`null`: can't tell ≠ gone), means **re-adopt**:
  restore the record and re-register the presence node.
- A re-adopted post-merge hook also gets back its one-running-per-project state
  (a resumed merge run / Phase C await it instead of starting a second),
  `markAgentReadopted` for a Claude hook (its live-subagent tracking died with
  the old process), a Stop the old process was holding (`stopReceivedAt`)
  re-armed (no second Stop is coming from the idle agent), and the merge's
  bounded wait re-armed for at least `READOPTED_HOOK_MIN_WAIT_MS`.
- A pty that is gone is still restored, then settled **lost** only after
  `LOST_SETTLE_GRACE_MS` unless its callback lands first — the outbox replays a
  Stop that fired while the backend was down; settling at once records "lost"
  for a run that finished. Lost means:
  - push → `lost` + done; never attachable by a re-dispatched workflow Push
    step, which fails rather than reporting success;
  - QA → any verdict already reported is applied as `/done` would (a
    confident PASS still promotes), then done;
  - post-merge hook → finished `errored` (waiters released).
- The liveness watch (every 30 s, unref'd, stops when empty, skips a pass on an
  unprobeable server) applies the same settlement to a re-adopted run whose pty
  dies later without calling back — the restarted process's stand-in for the
  old process's waiters.

Related: [../../homeScratch/CLAUDE.md](../../homeScratch/CLAUDE.md) (mirrors,
scratch contract), [../../postMergeHooks/CLAUDE.md](../../postMergeHooks/CLAUDE.md).
