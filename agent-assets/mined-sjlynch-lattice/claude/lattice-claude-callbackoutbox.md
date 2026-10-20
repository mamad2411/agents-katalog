# backend/src/callbackOutbox

Durable delivery for agent **completion callbacks** — the POST a Claude Stop
hook, a Codex `Stop` hook or the Pi `session_shutdown` extension makes to
`/api/tasks/:id/complete`, `/api/workflow-runs/:runId/steps/:n/complete`,
`/api/post-merge-hooks/:id/complete`, `/api/push-runs/:id/done`,
`/api/qa-runs/:id/done`, ….

## Why

Those callbacks used to be one `curl -s -m 5` (Pi: three tries in ~1.2 s).
When Lattice works on its own repo, every merge that touches `backend/src`
restarts the backend; a Stop that fired inside that window was simply gone.
The task sat `in_progress` beside an idle terminal forever (the in-progress
sweep only acts on a DEAD pty, and an interactive Claude stays alive after its
turn), and a re-adopted workflow agent step never advanced. Agent ptys live in
the detached terminal-server and survive the restart — only the one message
that says "I'm done" was lost.

## How

1. **Hook side** — `script.ts` renders `~/.lattice/bin/lattice-callback.cjs`
   (plain CommonJS, no deps; regenerated at boot and on every hook install, so
   it always matches this backend). Claude Stop hooks (`claudeStopHook.ts`)
   and Codex Stop hooks (`codexStopHook.ts`) prefer `node <script> <url>`
   (fallbacks below). The script writes an outbox entry FIRST, then POSTs
   with retries for `CALLBACK_HOOK_BUDGET_MS` (45 s); a definitive answer (2xx,
   or a 4xx other than 408/429) removes the entry. When the budget runs out
   it rewrites its own entry with `holdUntil: now`, handing it to the drain at
   once (the up-front hold is the worst case, ~budget + 25 s, and only matters
   for a hook killed mid-retry). It always exits 0 and
   prints nothing — a Stop hook's output/exit code is interpreted by the
   harness. The Pi extension (`piExtension/template.ts`) writes and clears the
   same entry around its own retry loop.
2. **Backend side** — `drain.ts` `startCallbackOutboxLoop` (started post-listen
   in `server/startup.ts`, at the END of the recovery chain — after the
   workflow / merge-run resumes and owed post-merge hooks — so a replayed push
   `/done` can't beat the Push step's re-dispatch — though never behind an agent
   step's pre-run scan, see `recovery/CLAUDE.md` 4a; then every 10 s) replays each entry by POSTing it back to
   this backend's own origin, so it goes through the same route, validation
   and idempotency guards as a live callback, with one addition: the
   `x-lattice-outbox-created-at` header (`OUTBOX_REPLAY_HEADER`) carrying the
   entry's `createdAt`, i.e. when the Stop fired. 5xx / network → kept with
   exponential backoff (≤ 60 s); definitive → removed.

## Invariants

- **One entry per callback URL** (`paths.ts` `callbackOutboxKey`, sha1[:20]).
  A Claude Stop fires on every turn end, so repeats collapse into the newest
  one. The generated script and the Pi extension compute the same key — keep
  them in step.
- **`holdUntil`**: the drain leaves an entry alone while the hook that wrote
  it may still be retrying, so the two never deliver concurrently.
- **The drain never undoes someone else's write.** Every removal and every
  bookkeeping rewrite first checks the file still holds the entry it read
  (same `createdAt`): a hook writes a newer entry for the same URL on every
  Stop, and a live delivery removes a delivered one. A rewrite writes its temp
  file first and re-checks right before the rename. The ack middleware
  (`ack.ts`) skips replays (they carry the replay header) — the drain removes
  those itself, under that check.
- **Only our own completion callbacks are replayed** (`classifyReplayUrl`:
  same origin, `/api/` path, and `CALLBACK_PATH_RE` — `/complete`, `/done`,
  `/verdict`, `/merged`, `/merge-aborted`, `/stash-resolved`). The outbox is a
  plain directory; its contents are never "POST wherever this says". An entry
  for our origin naming any other route (`/api/merge-runs`,
  `/api/workflows/:id/run`, …) is dropped without a request. An entry for
  another origin is left in place (another Lattice instance sharing this home
  on a different port drains its own) until the age cap drops it.
- **A late replay must not end a turn that started after it.** Nobody can type
  into an agent while the backend is down (the terminal WS is relayed through
  it), but the replay lands after the backend is back — and by then the user
  may have typed a new instruction into the idle agent. So a task `/complete`
  carrying the replay header is refused (`409 stale-replay`, final → dropped)
  when the task's session showed activity after the Stop
  (`replayGuard.ts` `taskSessionActiveSince`): an `/api/tasks/:id/activity`
  hook POST more than 3 s after it, or a line submitted (Enter) into a pty in
  the task's worktree (stamped by `terminalWsRelay.ts`). The new turn ends in
  its own Stop, which delivers a fresh callback. Refusal needs positive
  evidence — an unreachable terminal-server never blocks a replay. The other
  callback endpoints rely on idempotency. Entries older than 24 h
  (`OUTBOX_MAX_AGE_MS`) are dropped.
- **Fallbacks**: the Claude command is `node "<script>" "<url>" || <retrying
  curl>` — the curl only runs when node can't run the script at all. Codex
  0.144.1 on Windows was observed to whitespace-split hook commands and spawn
  argv directly without a shell; 0.157 on Windows ran hooks through PowerShell
  5.1. `script.ts`'s `codexCallbackCommands` retains compatibility with the
  legacy direct-argv path (no quotes or `||`): use the Node outbox script when
  its path is whitespace-free, otherwise use retrying curl. This conservative
  policy does not imply PowerShell cannot quote a path. Windows uses `cmd /c`
  for either command to resolve `node` / `curl.exe`. See
  [`codexStopHook.ts`](../codexStopHook.ts) for the observations and the separate
  activity-hook `-d@-` / bare `@-` PowerShell parsing footgun.
- The model-explicit completion curls in the briefs (`LATTICE_TASK.md`,
  `WORKFLOW_STEP.md`, merge / QA / post-merge / stash templates) carry
  `--retry … --retry-connrefused` for the same reason; they have no outbox.

From `backend/`: build `npm run build`; test `npm test`; type-check
`npx tsc --noEmit`.

Tests: `__tests__/callbackOutbox.test.ts` runs the real generated script and
the real generated Pi extension against a local HTTP server (delivered,
retry-then-keep, backend down → kept → drained, hold released on give-up)
plus the drain's policy (replay header, non-callback routes dropped unsent,
no resurrection / clobbering of a concurrently removed or rewritten entry).
`__tests__/callbackOutboxReplayGuard.test.ts` drives the real `/complete`
handler: a replay after later activity is refused and the task stays
in_progress; without it (or live) the task completes.
