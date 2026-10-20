# Orchestrator helpers

Helpers for `../orchestrate.mjs`, the `npm run dev` boot sequence (backend,
wait for `/api/health`, then vite). The user-facing dev-console contract and
dependency handling are in [../CLAUDE.md](../CLAUDE.md); the backend's own
runner is `backend/scripts/dev.mjs` (`backend/scripts/CLAUDE.md`).

## Map

- `children.mjs` — `startChild` / `killTree`: child spawn and shutdown.
- `health.mjs` — `/api/health` polling.
- `logFilter.mjs` — `prefixLines` (`[backend]` / `[frontend]`, called on each
  child's stdout/stderr) + Vite proxy `ECONNREFUSED` suppression.
- `config.mjs` — shared constants and colors.
- `devControl.mjs` — dev-console commands + the orchestrator ↔ dev-runner
  control protocol (`RESTART_EXIT_CODE`, `SOFT_STOP_TIMEOUT_MS`, control
  lines); unit-tested in `backend/src/__tests__/devControl.test.ts`.
- `consoleSink.mjs` — how the orchestrator writes to the console.
- `devLog.mjs` — crash bookkeeping into `~/.lattice/logs/dev-runner.log`.

## Invariants

- **Preserve the visible console contract**: `[backend]` / `[frontend]`
  prefixes and colors, Vite proxy-error suppression, Windows `taskkill /T`
  process-tree shutdown.
- **Console commands are lines, not raw keypresses**: raw mode clears the
  console's `ENABLE_PROCESSED_INPUT` on Windows (a per-console setting), so
  Ctrl+C would stop reaching `dev.mjs` / `dist/index.js` as the console break
  their full-stop path depends on. Commands are read only from a real console
  (`process.stdin.isTTY`); `LATTICE_DEV_CONSOLE_STDIN=1` opts a piped stdin in
  for a test driver (an isolated stack on alternate `PORT` / `TERMINAL_PORT` /
  `LATTICE_FRONTEND_PORT` / `LATTICE_BACKEND_PORT` and its own
  `HOME`/`USERPROFILE`; the health URL follows `PORT`).
- **The orchestrator is the console's ONLY reader.** The backend child's stdin
  is a **control pipe** (`stdin: 'pipe'` + `LATTICE_DEV_CONTROL=stdin`, which
  `dev.mjs` deletes from its env on read so it never reaches agent ptys)
  carrying `soft-stop` / `deps-recheck` lines. Vite gets a pipe that is never
  written (dropping its own h/r/o/q shortcuts — two readers split the
  console's lines unpredictably). Never `'ignore'` vite's stdin: vite closes
  its server when stdin ENDS, and an ignored stdin ends at once.
- **A soft stop must not take the agents with it**: `dev.mjs` kills
  `dist/index.js` with a plain `kill()` (not a tree kill), and the
  orchestrator waits for `dev.mjs` to exit on its own (`SOFT_STOP_TIMEOUT_MS`,
  30 s) instead of `taskkill /T`-ing a tree that still contains the detached
  terminal-server (a `detached` child keeps its parent pid). Only a runner
  that ignores the request for 30 s is tree-killed.
- **The soft stop drains the backend first**, like every automatic restart:
  `backend/scripts/dev/devShutdown.mjs` calls the restart-drain `prepare`
  (`backend/scripts/dev/restartHandshake.mjs`, fail-open) so debounced task /
  run-mirror writes flush and an in-flight transition lands. Its budget
  (`SOFT_STOP_PREPARE_TIMEOUT_MS`, 15 s) must stay below
  `SOFT_STOP_TIMEOUT_MS`; a Ctrl+C during the drain cuts it short
  (`devShutdown.test.ts`).
- **A full stop must not depend on a child's `'exit'`**: each child is a
  `cmd.exe` running npm.cmd, which after Ctrl+C prompts
  `Terminate batch job (Y/N)?` on its stdin (our pipe) and never exits. So
  `killTree` ends the child's stdin (EOF ends the prompt), runs `taskkill`
  `detached` (a repeated Ctrl+C otherwise kills it mid-walk), and the signal
  path exits after `FULL_STOP_EXIT_MS` regardless — else orphaned
  orchestrators keep reading the console and answer the next `npm run dev`
  with "unknown command". `KILL_GRACE_MS` must exceed `dev.mjs`'s
  terminal-server `/shutdown` cap, or `/F` lands mid-request and orphans the
  terminal-server with every pty.
- **On Windows `startChild` hands the shell ONE constant command string**
  (`npm run dev`), never args + `shell: true` (Node's DEP0190 warning at every
  boot); args are validated as bare script names before joining. Same rule
  as `../preflight.mjs` and `backend/scripts/dev/deps.mjs`. Children get their
  own `cwd`, never `npm --prefix` (see `../CLAUDE.md`).
- **All console output goes through `consoleSink.mjs`**: `process.stdout.write`
  blocks the event loop (Node forces blocking TTY writes), Windows pauses a
  console while a text selection is open, and this process is the only reader
  of the children's pipes — one stray click froze the backend solid. Writes
  use async `fs.write()` with a bounded queue. A short write's tail and an
  `EAGAIN`-refused chunk go back to the FRONT of the queue (EAGAIN retried
  after 25 ms) — never the back (splits a line) and never dropped
  (`devConsoleSinkWriteErrors.test.ts`). The backend's copy:
  `backend/src/consoleSink.ts`.
- **Raw bytes need a UTF-8 console**: `fs.write` skips libuv's UTF-8 → UTF-16
  conversion, so Windows decodes the bytes with the console code page (437 on
  a US install → every `·`/`—`/`➜` was mojibake). `useUtf8ConsoleCodePage()`
  (here) switches the console to 65001 for the life of `../devLoop.mjs` (and a
  standalone `backend/scripts/dev.mjs`) and restores the user's page on exit;
  `../orchestrate.mjs` calls it too (a no-op under a current devLoop) so a soft
  restart applies it. A caller that finds 65001 already set restores nothing.
  Its `chcp` must share the console — never `windowsHide` (that child gets a
  hidden console of its own and the switch lands there).
- **`devLog.mjs` exists because deaths go unrecorded otherwise**: it keeps
  each child's output tail in memory and appends it to `dev-runner.log` on an
  abnormal exit — a `taskkill`, OS OOM-kill, native fault or vite crash
  leaves no crash file. Pass `recordExit` a decoded `detail`, or a Windows
  fault reads as a bare `code=3221225477`. This orchestrator only sees its two
  children (`dev.mjs`, vite), never `dist/index.js`; that supervisor is
  `backend/scripts/dev/backendLifecycle.mjs` (plus `compilerLifecycle.mjs`),
  which import `recordExit` from here — keep them in step.
