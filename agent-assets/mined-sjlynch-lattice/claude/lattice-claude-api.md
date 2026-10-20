# frontend/src/api

Every backend HTTP/WS binding, grouped by domain; `import { ... } from '../api'`
resolves to `index.ts` (some modules export only a subset there, and `ws.ts` /
`opengrepReview.ts` are imported by path). Not here: pty create/DELETE side
effects (`../terminal/terminalApi.ts`) and React state (feature hooks).

## Modules

- `types/` (+ `types.ts` compatibility shim) — payload types by domain. See `types/CLAUDE.md`.
- `http.ts` — `asJson<T>` → status-bearing `HttpError` (`.status`, `.code`, `.detail`); `postJson` / `patchJson` / `deleteJson`.
- `retry.ts` — `retryTransient`, `mayHaveBeenApplied`, backoff constants.
- `ws.ts` — facade re-exporting the three WS modules below; domain files import WS from here.
- `wsTransport.ts` — `subscribeWs`: one socket's reconnect (250 ms → 5 s cap) and stability timer (`WS_STABLE_MS`).
- `wsSharedChannels.ts` — `subscribeWsShared`: ref-counted one-socket-per-path channels with a replay cache for late joiners.
- `wsConnectionHealth.ts` — `isBackendConnectionDown` / `subscribeBackendConnection` behind the navbar's `BackendConnectionIndicator`.
- `tasks.ts` — task CRUD, `runTask` / `resumeTask` / `cancelQueuedRun` / `mergeTask` / `abortTaskMerge`, `subscribeTasks` (`/ws/tasks`: board snapshots, `task-spawned`, `task-spawn-failed`, `task-activity`, `agent-activity`), `subscribeAgentSessions`.
- `mergeRuns.ts` — start / active / cancel / subscribe for "merge all".
- `workflows.ts` — workflow CRUD, `fetchSourceAreas` / `resolveSourceAreas` / `fetchSourceTree` for split previews, `startWorkflow`, `fetchWorkflowRun` (`null` on 404), `subscribeWorkflows` / `subscribeWorkflowRuns`.
- `pushRuns.ts` / `qaRuns.ts` / `postMergeHooks.ts` — one-off run lifecycles (start, status poll, forget/abort, subscribe).
- `projectInit.ts` — Git Setup: `previewProjectInit` (re-POSTed debounced while the `.gitignore` is edited) and `initProjectGit`.
- `scan.ts` — folder browsing, source scan, git history, `subscribeGitBranch` (`/ws/git-branch`), `subscribeGitStatus` (`/ws/git-status` signature; the timeline dedupes `fetchGitHistory` on `GitHistoryResult.signature`).
- `health.ts` — `subscribeHealth` (`/ws/health`, one `HealthUpdate` per save / tree change).
- `settings.ts` — per-project `UserSettings` (`fetchUserSettings`, `fetchUserSettingsStrict`, `patchUserSettings`), `subscribeHarnesses`, `getPiModels` / `probePiEndpoint`, `ensureProjectInstrumentation`, `fetchProjectEnv`, `fetchInstructionTemplates`, `fetchHarnessSystemPrompts`.
- `globalSettings.ts` — machine-global settings (`maxConcurrentAgents`, MCP defs, `piModelMenu`, `piProviders`, `opengrep.packs`).
- `mcp.ts` — MCP catalog, redacted secrets, env presence, validation, other-tool import.
- `opengrep.ts` — engine status / install / rule packs / scans (Settings → Tools) and the Security chip's graph scan (`runOpengrepGraphScan`, `waitForOpengrepGraphScan`, `fetchOpengrepGraphResult`, `cancelOpengrepGraphScan`, `subscribeOpengrepStatus`).
- `opengrepReview.ts` — security review sessions, local triage/history, shared suppression tasks; reads accept abort signals.
- `terminals.ts` — `subscribeTerminalActivity` (`/ws/terminal-activity`, per-tab spinner) and `fetchTerminalServerStatus` (navbar `TerminalServerChip`).
- `terminalTabs.ts` — the durable terminal-tab registry: `fetchTerminalTabs`, `restoreTerminalTabs` (`retry` also retries failed relaunches), label/order PATCHes, `closeTerminalTab`, `subscribeTerminalTabs`. Consumed by `../TerminalsContext.tsx` and `../terminal/terminalRegistrySync.ts`.

## Invariants

Wire types and task runs:

- `types/*` re-export the backend's own wire types from
  `backend/src/shared/wireTypes.ts` — never redeclare a type the backend
  declares in a node-free module (hand mirrors drift). What is still local and
  why: `types/CLAUDE.md`.
- `runTask` / `resumeTask` return `{accepted, queued}`: `accepted` means
  admitted to the spawn queue, not started. The pty arrives later via the
  `/ws/tasks` `task-spawned` event (`subscribeTasks` `onSpawned`); never re-POST
  to "make it start" and never read the response as "the worktree exists".
- Every by-id call (`updateTask`, `deleteTask`, `runTask`, `resumeTask`,
  `cancelQueuedRun`, `mergeTask`, `abortTaskMerge`; `updateWorkflow`,
  `deleteWorkflow`, `cancelWorkflowRun`) takes the ACTIVE board's project and
  sends it as `?project=` (`taskByIdUrl` / `withProjectParam`): the backend's id
  lookup is global, so the pin is what 404s another board's id. Pass
  `activeFolder`, never the task's own `projectPath` (makes the check vacuous).
- `fetchTasks` sends `WHOLE_BOARD_QUERY`, opting out of every agent-tuned
  `GET /api/tasks` default — drop one param and the board loses its done lane,
  truncates descriptions, or 413s on a mature project.
- `subscribeTasks`' replay cache holds only the in-progress tasks, delivered as
  `onUpdate(tasks, {partial: true})` — never cache a full-board frame (megabytes
  kept as a second parsed copy). The graph overlay uses partial updates as-is;
  `useTaskList` ignores them (it fetches the board over HTTP).

Errors and retries:

- `HttpError.detail` carries verbatim tool output (git's stderr) and must
  survive, never flattened into `.message` — it's often the only place the fix
  is spelled out (`initProjectGit` 422 renders it; the backend is barred from
  naming those git config keys itself).
- `retryTransient` retries only fetch `TypeError` and 502/503/504, backing off
  1→2→4→8→15 s for up to 3 min; any other status throws at once.
  `mayHaveBeenApplied(err)` flags failures whose request may have landed
  (network error, 504, a 502 that isn't ECONNREFUSED).
- A POST the backend won't dedupe past settlement (task Resume, workflow start,
  single-task merge, push and QA-run starts) passes `retryIf: err => !mayHaveBeenApplied(err)` and
  surfaces an ambiguous acknowledgement instead of replaying — queue dedupe and
  active-run guards expire before transport retries do, so a replay can
  allocate a second agent. Run / merge-all may retry everything and treat a
  later 400/409 after a possibly-applied attempt as their own.
- Strict vs lenient reads: `fetchUserSettings` maps a failure to `{}`; an
  editor that saves a whole sub-object back must load with
  `fetchUserSettingsStrict` (else a mid-restart `{}` becomes the saved state).
  `getPiModels` throws rather than reading as "no models"; `fetchTerminalTabs`
  throws on non-2xx so a restarting backend reads as "unknown", never "no tabs".

WebSocket:

- Every subscriber builds on `subscribeWs` / `subscribeWsShared` from `./ws` —
  don't reinvent reconnect/backoff. Internal imports flow shared channels →
  transport → connection health, never back to the `ws.ts` facade (cycle).
- Transport: backoff resets only after a socket stays open `WS_STABLE_MS`;
  `onDisconnect` fires before a retry is scheduled; close/teardown clear the
  stability timer and teardown cancels pending retries; malformed frames are
  dropped; a throwing handler is logged (`[ws] handler failed`) without closing
  the socket.
- Shared channels: every caller of one path passes the SAME replay policy
  (`shouldReplay`, `replayValue`, `resetReplayOnDisconnect`). Each subscription
  is its own registration (cleanup bound to that channel instance); message,
  disconnect and replay callback failures are isolated per subscriber. A
  throwing `replayValue` projection caches nothing. The last unsubscribe tears
  down the socket and releases the replay cache. Terminal activity opts into
  `resetReplayOnDisconnect` so a lost connection can't replay stale busy ids.
- Connection health is display-only — never gate behaviour on it.
- `subscribeTerminalActivity`'s `busy` list is machine-wide; the consumer
  intersects it with its own project-scoped tabs.

Other boundaries:

- `checkGit().hasGit` is a plain stat of `<path>/.git` (what Push reads) — do
  NOT make it walk up; the additive `git: ProjectGitProbe` walks up (so it can
  report `nested`) and may be absent from an older backend.
- Terminal-tab records are CREATED by the backend at pty creation; the
  frontend only reads, restores and decorates. `closeTerminalTab` is `void`
  with optional `onClosed` / `onError`: 404 = already closed, `{ok:true}`
  confirms; a 503 `terminal-close-unconfirmed` is retryable — close intent is
  not proof the pty is gone, so callers keep the tab until confirmation. Full
  lifecycle: [frontend/src/terminal/CLAUDE.md](../terminal/CLAUDE.md),
  [backend/src/terminalRegistry/CLAUDE.md](../../../backend/src/terminalRegistry/CLAUDE.md).
- Opengrep: no automatic, startup or retried scans — only explicit Security
  chip/panel actions start or cancel one. `runOpengrepGraphScan` POSTs once
  (`async: true, acceptImmediately: true`), publishes the accepted id, then
  polls GET-only (`format=graph`, 1.5 s); after a refresh the overlay
  re-attaches to `status.project.runningScan` through
  `waitForOpengrepGraphScan` (GETs only); cancellation is by exact id and waits
  for backend confirmation.
  `subscribeOpengrepStatus`: the latest-started status request wins and an
  aborted one never publishes. No automatic review or recommendation storage
  in `opengrepReview.ts`.
- Raw MCP secret values never cross this boundary (redacted reads, env presence).

## Adding an endpoint

1. Type goes in the matching `types/<domain>.ts`, re-exported by
   `types/index.ts` — or re-export the backend's own via
   `backend/src/shared/wireTypes.ts` (see `types/CLAUDE.md`).
2. Function goes in the matching domain file: `asJson` for GETs,
   `postJson` / `patchJson` / `deleteJson` for JSON writes. A by-id route takes
   the active project and pins it (`taskByIdUrl` / `withProjectParam`).
3. WS: `subscribeWs(path, cb)`, or `subscribeWsShared` when several features
   watch the same path (same replay policy from every caller).
4. New domain: add a file + `export *` (or named exports) in `index.ts`.
