# Lattice

Personal coding orchestrator: runs parallel Claude Code / Codex / Pi agents in
git-worktree branches and shows a project's source tree as a 3D force-directed
DAG.

## How these docs work

- An auto-loaded `CLAUDE.md` — this one in every session (every Lattice-spawned
  task agent included), a folder's whenever you read a file under it — holds
  only rules for everything beneath it, plus pointers. Budgets:
  `backend/src/__tests__/docBudget.test.ts`.
- On demand: a `MAP.md` beside a `CLAUDE.md` says which module owns what
  (`backend/src/MAP.md`, `frontend/src/MAP.md`, `frontend/src/components/MAP.md`);
  `docs/ARCHITECTURE.md` covers on-disk state (`~/.lattice/` layout, crash
  logs), the task pipeline, merge runs, worktree paths, the dev loop and E2E
  isolation; `docs/RECIPES.md` lists the touch points of common changes (a
  setting, route, WS event, wire type, MCP tool, …); `docs/MANUAL_TESTING.md`
  seeds tasks / conflict scenarios against a live instance.
- Before changing a subsystem, read the `CLAUDE.md` beside its code. New rules
  go in the owning folder's `CLAUDE.md`, navigation in its `MAP.md` — not here.

## Layout

- `backend/` — Express server (`:5184`) + detached PTY executor (`:5185`);
  `frontend/` — Vite + React + TS + xterm + 3d-force-graph (`:5183`). Ports are
  +10 from Vite's defaults to dodge other local dev servers.
- `scripts/` — `npm run dev` orchestration (`scripts/CLAUDE.md`); `e2e/` —
  Playwright specs (`e2e/CLAUDE.md`).
- State lives in `~/.lattice/` (tasks, worktrees, snapshots, run locks, logs)
  and gitignored `<project>/.lattice/` scratch (`LATTICE_HOME` relocates the
  former for a second instance). Derive every path through
  `backend/src/projectPath.ts`; never recompute a project hash or derive a
  second store from a new path spelling (`backend/src/PROJECT_IDENTITY.md`).
- Something died? Check `~/.lattice/logs/` first (`docs/ARCHITECTURE.md` →
  "Crash forensics").

## Dev server: hands off

**Do not start, stop, or restart the dev server yourself** (`npm run dev`). The
user runs it in their own terminal and watches its output; restarting it from
an agent steals their console, drops their HMR/WS connections and hides errors
they were debugging. Validate with the commands below; the user reloads when
ready.

## Type-check & test (from the repo root)

- `npm run typecheck` — both packages (per package: `cd backend && npx tsc --noEmit`,
  `cd frontend && npx tsc -b`).
- `npm test` — both packages' unit tests; prints failures + a one-line summary only.
- `npm run test:file -- <path>` — one test file in either package, with the
  right preloads (HOME isolation).
- `npm run test:e2e` — Playwright against an isolated backend/vite/terminal-server
  (`:5384`/`:5383`/`:5385`, temp HOME), never the live instance; needs a current
  `backend/dist` (`e2e/CLAUDE.md`).

## Git discipline

**Stay on the `main` branch unless otherwise specified.** Do work, commit, and
push on `main` by default; only switch to (or create) another branch when the
user explicitly asks for it, and switch back to `main` when that work is done.

**Exception — Lattice-spawned agents.** A task agent working in a
`~/.lattice/worktrees/…` checkout commits on its own `lattice/<slug>-<id>`
branch and never checks out, merges into, or pushes `main` — Lattice merges it.
Nor does it start the backend / `npm run dev` there. A merge-resolver or
workflow-step agent follows its brief (`MERGE_INSTRUCTIONS.md`,
`WORKFLOW_STEP.md`, …) over this section.

## `.git`-deletion defences

Every past `.git` loss was a recursive delete reaching it (`fs.rm`, or a lost
`git stash --include-untracked`). So worktrees and scratch live outside the
project tree, all project-repo git goes through the `projectGit()` whitelist,
nothing runs a recursive `fs.rm` inside a project, and snapshots are copies,
never `git stash`. Read the full layered list in `backend/src/worktree/CLAUDE.md`
before touching merge, cleanup or scratch code.

## Conventions

One line each; the named doc owns the detail.

- **UI:** no MUI / CSS-in-JS — hand-written CSS (`frontend/src/styles/`) +
  `lucide-react`; per-extension sprite shape/color only in
  `frontend/src/extensionStyles.ts` (add a language there), task/session colors
  only in `frontend/src/taskColors.ts` (stable `Task.colorIndex` slots).
- **Graph** (`frontend/src/components/forceGraph/CLAUDE.md`): overlays
  `H`/`Z`/`D`/`W`/`Alt`; filter through `nodeVisibility`, never structural
  add/remove; render-on-demand idle reasons; the Security chip scans only on an
  explicit click — never on load, file change or project switch.
- **Agent presence:** every agent (Claude/Codex/Pi; task, workflow or
  user-started) is a graph node with focus beams; every hook body decodes in
  `backend/src/activityHook.ts`; opening a project installs activity hooks
  (`backend/src/projectClaude/CLAUDE.md`). Codex ≥0.157 runs hooks through
  PowerShell 5.1: post with `cmd /c curl … -d@- <url>`, never `--data-binary @-`.
- **MCP** (`backend/src/mcp/CLAUDE.md`): resolved once at the spawn chokepoint
  (`resolveHarnessSpawnBody`); third-party servers off by default; secrets by
  env name only; **never set `defaultEnabled` on a third-party entry**.
- **Opengrep** (`backend/src/opengrep/CLAUDE.md`): downloaded on the user's click
  into `~/.lattice/opengrep/`; **nothing third-party is committed or bundled**
  (keeps Lattice MIT; guard test `opengrepNoVendoredAssets`); agents see
  digests, never raw JSON.
- **Pi** (`backend/src/piModels/CLAUDE.md`, `backend/src/piSubagents/CLAUDE.md`):
  `piModel` (`provider/model`; the model half may contain `/`) is its own field,
  never a composite with `harness`; a model `backend/src/shared/harnesses.ts`
  rejects has its `--model` silently dropped; the user's global Pi config is
  never touched.
- **Terminals** (`backend/src/terminal/CLAUDE.md`, `backend/src/terminalRegistry/CLAUDE.md`,
  `frontend/src/components/sidebar/CLAUDE.md`):
  tabs survive restarts; spawns pre-create the pty and panes lazy-mount; Codex
  trust is a per-launch override, never `~/.codex/config.toml`; **never kill
  live ptys** to upgrade an indicator or default.
- **System prompts** (`backend/src/harnessSystemPrompts/CLAUDE.md`): per-harness
  Append/Replace plus the Lattice preamble naming `.lattice/LATTICE_API.md`
  (< 5 KB, generated from `backend/src/latticeApiDocs/`). Agents find Lattice
  only through the system prompt — never reintroduce `LATTICE_*` pty env vars
  or rely on the terminal banner; neither reaches the agent.
- **Task agents don't run tests, builds or type-checks**
  (`backend/src/taskVerification.ts`; per-project opt-ins `taskAgentTypecheck`
  for scoped type-checks and `taskAgentTests` for targeted test files);
  a workflow's Run tests step verifies merged work once, commits fixes by
  explicit path only and never stops the workflow
  (`backend/src/workflowRuns/testStep/CLAUDE.md`); a confident QA-run PASS
  auto-advances qa → done (`backend/src/qaRuns/CLAUDE.md`).
- **Routes:** every route is a row in `backend/src/routes/ROUTES.md`
  (drift-tested); a relative or drive-relative `project`/`path`/`cwd` is a 400;
  all WS endpoints share one `upgrade` dispatcher (`backend/src/routes/CLAUDE.md`).
- **Runs are re-runnable:** the backend can restart mid merge/workflow/push run
  and boot resumes it, so every run step must be idempotent on half-done work
  (`backend/src/mergeRuns/CLAUDE.md`, `backend/src/recovery/CLAUDE.md`).
- **State:** tasks are an in-memory per-project cache with debounced JSON
  persistence (`backend/src/taskCache/CLAUDE.md`); per-project UI state is
  `localStorage` `lattice.<thing>.<projectPath>` plus
  `<project>/.lattice/userSettings.json` via `/api/settings`.
- **Memory:** `registerMemGauge` beside every long-lived collection, listener
  set or GPU resource (`backend/src/memDiag/CLAUDE.md`).
- **Shared code** both packages need lives once in `backend/src/shared/`
  (relative imports only), never a hand-mirrored copy (`backend/src/shared/CLAUDE.md`).
- Prefer editing existing files; no new abstractions for one-off tweaks.
