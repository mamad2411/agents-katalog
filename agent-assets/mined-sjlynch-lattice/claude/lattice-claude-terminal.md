# backend/src/terminal

The detached terminal-server's PTY-session core: spawn, attach, kill,
scrollback and output facts for every node-pty process. `../terminal.ts` is the
facade. Not here: the executor's HTTP/WS/guard shell (`../terminalServer/`),
the backend's client + spawn chokepoint (`../terminalServerClient/`), durable
tabs (`../terminalRegistry/`), the frontend's xterm state (`frontend/src/terminal/`).

## Map

- `sessionTypes.ts` — `Session` + opts. Record facts here; activity thresholds /
  harness classification stay in `../terminalActivity.ts`.
- `sessionStore.ts` — the single source of truth (`Map<id, Session>`) +
  `terminal.*` gauges; `listSessions` is also the wire format the backend reads.
- `createSession.ts` — spawn orchestrator (cap → launch context → `pty.spawn` →
  `addSession` → events + banner + `lowerAgentPriority` + initial command);
  `precreateSession` returns a `serverId` before any WS attaches.
- `launchContext.ts` — `buildSessionLaunchContext`: shell (`resolveDefaultShell`:
  `opts.shell` → `LATTICE_DEFAULT_SHELL` → cmd.exe / `$SHELL`), cwd, size, env,
  then the per-harness command rewriters.
- `envSetup.ts` — `applyClaudeOverheadEnv` (defaults only, never overriding a
  user value) + `scrubInheritedNpmEnv`.
- `windowsPath.ts` — `applyFreshWindowsPath` (registry PATH, cached 30 s, so
  tools installed after boot are visible) + `applyPtyPathPrepend`
  (`LATTICE_PTY_PATH_PREPEND`, first on PATH; `scripts/soak/` uses it).
- `codexTrust.ts` — Codex per-launch `--config` injection: trust, managed MCP,
  system prompt (own `LATTICE_CODEX_SYS_<i>` env series); `shellEnvRef`,
  `tomlString` (re-exported by `../mcp/codexServerConfig.ts`).
- `claudeSystemPrompt.ts` — Claude `--(append-)system-prompt-file` override.
- `sessionLifecycle.ts` — `wireSessionPtyEvents` (exit → `deleteSession` +
  conout Worker release), banner, `scheduleInitialCommand`.
- `attach.ts` — `attachTerminal`: subscribe **on hold**, `attached`, replay,
  flush held frames.
- `broadcast.ts` — subscriber fan-out + hold queue; `SUBSCRIBER_HIGH_WATER_BYTES`
  (8 MB) is shared with `../terminalWsRelay.ts`.
- `kill.ts` — `killSession` (+ a deferred `ensureClaudeConfigValid`: a
  force-killed Claude can truncate `~/.claude.json`), `killSessionsByCwd`
  (worktree teardown), `cwdIsAtOrUnder`.
- `conoutWorker.ts` — node-pty conout Worker tracking/release (below).
- `outputFacts.ts` — `TerminalOutputFacts`: constant-memory escape parser →
  `lastTextOutputAt` + OSC 0/2 `terminalTitle` (≤ 128 units, else unknown).
  Dependency-free: `../terminalActivityRelay.ts` reuses it for old executors.
- `ptyDimension.ts` — dependency-free `isPtyDimension` (≤ 32767, ConPTY's
  limit) so `routes/terminals.ts` can share it without loading node-pty.
- `scrollbackStore.ts` — per-session append log under
  `~/.lattice/terminal-scrollback`, degrading to a bounded in-memory tail.
- `scrollbackLogFile.ts` — `trimToLineStart` (replay never starts mid-escape),
  `readTail` / `readTailAsync`.
- `scrollbackCleanup.ts` — boot wipe of orphaned scrollback logs.

## Invariants

**Executor process**

- Every module the executor loads must be in `../terminalFingerprint.ts`
  `FINGERPRINT_FILES`, else an edit leaves a stale executor serving old code.
  Never import `../latticeApiDocs.ts` (changes with every API edit, so the
  executor would go stale constantly — use `latticeApiDocs/docPath.ts`) or
  `../memDiag/browser.ts` (backend-only). `terminalFingerprint.test.ts` pins both.
- This process hosts every pty — never block its loop: the registry PATH read
  stays off the spawn path (a sync `reg.exe` gave empty panes); compaction and
  attach replay stay async (sync multi-MB reads froze every pty and timed out
  the health probe).
- A subscriber past `SUBSCRIBER_HIGH_WATER_BYTES` of `bufferedAmount` is
  `terminate()`d, never buffered further (one stalled tab must not grow this
  heap; it reconnects and replays). Held frames obey the same bound.
- Sizes go through `isPtyDimension`, here and in the upgrade handler
  (`../terminalServer/websocket.ts`), which refuses — never throws on — a
  target `new URL()` rejects (a throw exits the executor).

**Live ptys**

- Never kill a live pty to upgrade an indicator or a launch default; defaults,
  trust and prompt overrides apply on launch/relaunch only.
- Kill via `killSession` (the `killing` guard + process-tree kill), never a
  bare `pty.kill()`.
- An unknown attach id gets `session_lost`, never a silent respawn (reconnect
  loop). A client disconnect drops only the subscriber; the pty lives.
- `launchContext` refuses a cwd that doesn't exist (a doomed spawn feeds a
  reconnect loop).
- `cwdIsAtOrUnder` is separator-agnostic and case-folds only on win32 — the
  same comparison as `../mergeRuns/waiterLiveness.ts` and
  `../recovery/liveSessions.ts`. Keep them in lockstep, or a pty reported alive
  under a worktree escapes its teardown kill and keeps its file locks.
- node-pty (`useConptyDll`) never stops its per-pty conout Worker (~10 MB RSS,
  invisible to `heapUsed`); `releaseConoutWorker` (from onExit) disposes it.
  Gauge `terminal.conoutWorkers` must equal `terminal.sessions`; re-verify
  both on any node-pty upgrade.
- `deleteSession` is the one deletion point and disposes the scrollback.
- `lowerAgentPriority` drops an **agent** pty's shell
  (`agentHarnessForCommand`) to below-normal *before* the agent command is
  typed, so everything it spawns inherits it (a dozen equal-priority agents
  froze the desktop). User shells / dev servers keep normal;
  `LATTICE_AGENT_PRIORITY=normal` opts out.

**Agent discovery is not this folder's job**

- Plant no `LATTICE_*` env vars in a pty — no harness reads its environment
  into context. Discovery is the system-prompt preamble
  (`../harnessSystemPrompts/latticePreamble.ts`).
- The banner is human-only: appended to SCROLLBACK, never written to the pty.
- `launchContext` only looks up `LATTICE_API.md`; the backend regenerates it
  before requesting a session (`resolveHarnessSpawnBody`; `../terminalWsRelay.ts`
  for a serverless connect).
- The Windows default shell is cmd.exe, where `$VAR` doesn't expand — so the
  generated doc bakes in literal values and the banner names it by absolute path.

**Harness command rewriting**

- Codex trust is per launch (`--config projects={'<cwd>'={trust_level='trusted'}}`,
  merged over the user's `[projects]`); never write `~/.codex/config.toml`.
- The path is an inline-table key inside the VALUE (Codex splits a `-c` KEY on
  every `.`, and worktree paths contain `.lattice`), as a single-quoted literal
  (`tomlString`; cmd's `"%VAR%"` strips inner double quotes).
- Dynamic values (TOML, prompt-file paths) ride in child-env vars referenced
  via `shellEnvRef`, never interpolated into shell source.

**Inherited environment**

- `scrubInheritedNpmEnv` (the backend is an npm run-script; every pty inherits
  its env) strips `npm_config_prefix` & co. (redirected `npm install -g` into
  `<latticeRoot>/backend`) and npm's injected `node_modules/.bin` PATH entries
  (lent every terminal Lattice's `tsc`/`tsx`/`playwright` — a meaningless clean
  type-check). Never a blanket `npm_config_*` scrub (`registry`/`cache`/
  `_authToken` may be the user's); derive the `.bin` set from
  `npm_config_local_prefix`, never a hardcoded layout. Runs before
  `applyFreshWindowsPath` so the registry PATH merges back on top;
  `inheritedNpmEnv.test.ts` fails if dropped or reordered. Root cause:
  `scripts/orchestrate/config.mjs` (cwd, not `npm --prefix`).

**Scrollback**

- During a compaction (temp + rename), flushes hold output in `pending`
  (bounded to the replay window) and land after the rename; `replay` appends
  the held tail. A rename failing on a Windows lock (EPERM/EBUSY, a concurrent
  replay) is retried, then the OLD log is kept (complete, over cap) with a 5 s
  cooldown — never a drop to memory-only, which is reserved for a dead disk.
- `replayAsync` (attach) snapshots flushed length + pending synchronously and
  reads capped at it, so output appended meanwhile arrives only as held live
  frames, never twice; mid-compaction it takes the sync `replay()`.
- Attach always sends a `replayed: true` `data` frame before held live frames,
  even for an empty/failed read: the browser suppresses replies to historical
  terminal queries, so without that boundary a live startup query reads as history.
- `clearTerminalScrollback` is path-guarded to `~/.lattice/terminal-scrollback`.

**Output facts**

- CSI sync/cursor/query frames, OSC titles and DCS/APC/PM payloads are not
  text, even split across chunks (Codex redraws while idle); `lastTextOutputAt`
  0 = no printable output yet. Raw output still reaches scrollback/subscribers
  unchanged, and `lastOutputAt` keeps its raw-byte meaning for liveness consumers.

## Codex launch defaults

Owned by the main backend: `withCodexActivityTitle` (`../codexTerminalActivity.ts`,
injected via `../terminalServerClient/spawnBody.ts` and `../terminalWsRelay.ts`)
adds per-launch `tui.terminal_title=['status']` and
`tui.terminal_resize_reflow_max_rows=500` — idempotent, upgrades a title-only
command on relaunch, later user overrides still win, no user config written.
Keep the cap: with an inherited `WT_SESSION` Codex re-emits up to 9001 rows per
resize (minutes through PTY → relay → xterm); it and the frontend resize
debounce prevent that. Working state follows the status title.

## Scrollback and session caps

`TERMINAL_CONFIG` in `../terminalConfig.ts`: `SCROLLBACK_REPLAY_BYTES` (2 MB,
max a browser gets per (re)attach), `SCROLLBACK_KEEP_BYTES` (4 MB, tail a
compaction keeps), `SCROLLBACK_MAX_DISK_BYTES` (8 MB, triggers compaction),
`SCROLLBACK_FLUSH_BYTES` (64 KB), `MAX_TERMINAL_SESSIONS` (200, runaway
backstop). Every mounted pane receives the replay on each (re)attach, inflated
by JSON-escaping — raising it multiplies browser memory per pane.

## Pointers

- Tests: named after the module — grep `<module>` in `backend/src/__tests__/`
  (`terminalAttach`, `scrollbackStore`, `defaultShell`, `terminalKillByCwd`, …).
- Related: `../terminalServer/CLAUDE.md` (process, stale-executor upgrade
  policy), `../terminalServerClient/CLAUDE.md`, `../terminalRegistry/CLAUDE.md`,
  `../harnessSystemPrompts/CLAUDE.md`, `../memDiag/CLAUDE.md`.
