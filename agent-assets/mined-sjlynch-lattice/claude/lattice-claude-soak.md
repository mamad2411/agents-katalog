# Self-hosting soak

Does a workflow survive its backend being hard-killed over and over
mid-flight (what happens when Lattice merges into its own repo and every merge
restarts the backend)? `node scripts/soak/selfHostSoak.mjs [--tasks 8]
[--chaos 10-30] [--down 0-4] [--timeout 25] [--no-chaos] [--keep]`. Fully
isolated from the live instance; no tokens, deterministic. Needs a current
`backend/dist` (keep `npm run dev` running, or build first).

- `selfHostSoak.mjs` is the executable entry point. It owns CLI parsing,
  the dist preflight, settings/task/workflow seeding, chaos scheduling,
  settling, report printing, and teardown order.
- `soakFixture.mjs` exports `createSoakFixture({ here, port, terminalPort })`.
  It creates the temporary root, initial git commit, fake-Claude shim, and
  child environment. The returned paths, env, and project-bound `g` git
  helper are passed explicitly to the runtime and report.
- `soakRuntime.mjs` exports `createSoakRuntime` and `sleep`. Each runtime
  owns its backend handle and generation, start/kill operations, API retries,
  health polling, and terminal-server shutdown. Creation itself starts nothing.
- `soakReport.mjs` exports `collectSoakReport`. Given the fixture, API caller,
  and scenario results, it reads the invariants and returns the report.
  Printing and exit decisions stay in the entry point.
- Importing any of the three helpers performs no filesystem/process work
  and does not execute the scenario.

## Scenario and isolation

CLI defaults: 8 tasks, chaos every 10–30 s, downtime 0–4 s, timeout 25 min,
backend port 5484, terminal port 5485; `--no-chaos` and `--keep` are flags.
The backend uses this checkout's existing `backend/dist/index.js`.
The throwaway project starts on main; even tasks append to `shared.txt` (so
every later merge conflicts and runs the resolver flow), odd tasks to
`own/task-N.txt`. Post-merge hooks are enabled and the workflow is
Start → Merge → Run tests → Push.

All generated state lives under `<os.tmpdir()>/lattice-soak-*`: `project/`,
`home/`, `bin/`, and `tmp/`. Child HOME and USERPROFILE point at `home/`;
TEMP/TMP/TMPDIR point at the sibling `tmp/` so restart recovery keeps the
project (the backend prunes `projects.json` entries under its own temp dir as
test junk). Strip inherited Claude session markers, preserve case-insensitive
PATH-key lookup, and keep both the shim PATH prefix and
`LATTICE_PTY_PATH_PREPEND` (Windows registry PATH otherwise outranks it).
The shim is `claude.cmd` on Windows and an executable `claude` shell script
elsewhere. Diagnostics are `backend-<generation>.log`, `fake-agents.jsonl`,
and `home/.lattice/` (including the callback outbox and terminal token).

## Fake-Claude protocol and report contract

`fakeClaude.mjs` ignores flags, detects resolver/task/test/workflow/session
work from its cwd, applies `SOAK-EDIT: <relpath> :: <line>` idempotently,
union-resolves conflicts, or writes `TEST_SUMMARY.md`. It records JSONL
events via SOAK_LOG, waits SOAK_FAKE_DELAY (1500–8000 ms), runs the installed
Stop hook, then idles until the pty is killed. Keep that protocol unchanged.

The report checks completion, QA/done task status, every expected line,
no shared-file conflict markers, one registered worktree, an empty outbox,
exactly one push, at least one post-merge hook, and no fake-agent failures.
Keys: `ok`, `failures`, `elapsedSec`, `restarts`, `run`, `tasksByStatus`,
`mainCommits`, `sessionsByKind`, `pushSessions`, `hookSessions`, `stopHooks`,
`root`. Preserve diagnostics and assertion order.

Preserve timing: API retries every 500 ms with 15 s requests (60 s budget,
120 s for health/run polling); only HTTP 502/503 trigger status retries.
After chaos, wait 15 s, then poll outbox every 2 s up to 120 s before reporting.
Teardown prints the report, hard-kills only the backend (SIGKILL), attempts
token-authenticated terminal shutdown (5 s), then on success without
`--keep` waits 2 s and removes the fixture. Failures/`--keep` retain it.
Exit codes: 0 pass, 1 invariant failure, 2 missing dist. Do not add recovery
or change process cleanup policy during extraction.
