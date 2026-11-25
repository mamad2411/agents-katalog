---
name: dev-server-start
description: Start one workspace member's dev server in the background and wait for ready — package manager and port from project config; reuses a running server.
kind: skill
pack: frontend
allowed-tools: [Read, Grep, Glob, Bash]
---

# dev-server-start

## Premise

Existing project conventions are the truth. Read `package.json`, the lockfile, and the framework config before guessing — never invent a start command. Mirror the script the project already ships with (`dev`, `start`, `serve`); if none exists, halt rather than fabricate one. Idempotency is non-negotiable: a re-run in the same session must detect an already-running server, not spawn a duplicate.

Refuse to start a server when `package.json` is absent at the chosen project root — and **choose that root deliberately**, because in a workspace the nearest `package.json` above `$PWD` belongs to the workspace, whose `dev` script starts N servers rather than one.

Boilerplate for "I need the app running locally before I can verify it." Used as a prerequisite by `verify-with-playwright`, `a11y-scan`, `visual-check`, `ssr-audit`, and any task that ends with "open the page and check."

## When to run

- Before invoking the Playwright MCP server's `navigate` tool against `http://localhost:<port>`.
- Before running an e2e test that hits `localhost`.
- Before a manual visual check — agent or human.

## When NOT to run

- The user already has the dev server running in another terminal — `lsof -iTCP:<port> -sTCP:LISTEN` should detect it; this skill is a no-op then.
- Static-only checks (lint, type-check, bundle analysis) — no server needed.
- Production / staging URL targets — point Playwright there directly.

## Inputs

- Working directory of the project (defaults to `$PWD`).
- Optional `app_target` — the workspace member to start (`apps/web`, or its package name). Required, or the run halts, when the workspace holds more than one app member. Ignored in a single-package repo.
- Optional `port_override` (numeric) — when the project's default port is taken or a separate instance is needed (e.g., E2E parallel runs).

## Procedure

### Step 0 — Resolve PROJECT_ROOT (runs before everything)

The hard rule below requires a verified `package.json` at `PROJECT_ROOT`. Nothing *chooses* that root unless this step does, and in a workspace the obvious choice is the wrong one.

1. **Is this a workspace?** Walk up from `$PWD` to the outermost directory holding a `package.json`. It is a workspace root when any of these sits beside it: `pnpm-workspace.yaml`, a `workspaces` key in that `package.json` (npm / yarn / bun), `turbo.json`, `nx.json`, `lerna.json`, `rush.json`.
   **Not a workspace** → `PROJECT_ROOT` is that directory; go to Step 1.

2. **Does the root `dev` script fan out?** Read `scripts.dev` there. `turbo run dev`, `nx run-many`, `pnpm -r dev`, `npm run dev --workspaces`, `lerna run dev`, `concurrently ...` each start **several** servers. That is the whole failure this step exists for: Step 2's single-port precedence picks one default, Step 5 declares ready on whichever app bound it first, and `verify-with-playwright`, `a11y-scan`, `visual-check` and `ssr-audit` then all run against the wrong app with no error raised anywhere. A silently wrong URL is worse than a halt, because the four downstream skills report clean results about a page nobody asked for.

3. **Enumerate the app members.** Resolve the workspace globs — `pnpm-workspace.yaml` `packages:`, the `workspaces` array, or `apps/*` / `packages/*` — then keep only the members that are *apps*: a member with its own `scripts.dev` **and** a framework config beside it (`vite.config`, `next.config`, `nuxt.config`, `angular.json`, `svelte.config`, `astro.config`). A member with a `dev` script but no framework config (a watch-mode library build, an API server in a fullstack repo) is not an app for this skill's purpose — name it in the candidate list, do not silently drop it, and let the caller pick if that is what they meant.

4. **Choose, and never guess:**
   - `app_target` given → that member.
   - Exactly one app member → take it and say so: `root: apps/web (sole app member)`.
   - More than one app member and no `app_target` → **HALT `workspace-target-ambiguous`**, printing one line per candidate: `<dir> — <dev script> — <framework> — <configured port>`. Do not run the fan-out script; do not take the alphabetically-first member.

5. **What resolves where.** `PROJECT_ROOT` is the chosen **member** directory — the framework config, the port, and the ready-probe all come from there. Two exceptions: the **package manager** is read from the lockfile at the *workspace* root (members do not carry one), and `.claude/dev-server.{pid,log}` stay at the workspace root, suffixed with the member so two members can run at once (`dev-server.web.pid`). Launch through the workspace runner so the member's dependencies resolve — `pnpm --filter <member> dev`, `npm run dev -w <member>`, `yarn workspace <member> dev`, `bun run --filter <member> dev`, or `npx --no turbo run dev --filter=<member>` — never a bare `cd <member> && npm run dev`, which bypasses hoisting in some layouts.

### Step 1 — Detect the runtime + start command

Read `scripts.dev` in the **chosen member's** `package.json` (or `scripts.start` for Next/Nuxt). Detect package manager from the lockfile at the workspace root (single-package repo: the same directory):
- `pnpm-lock.yaml` → `pnpm dev`
- `yarn.lock` → `yarn dev`
- `bun.lock` (text lockfile, the default from Bun 1.2) or `bun.lockb` (binary, older Bun) → `bun dev`
- `package-lock.json` → `npm run dev`

If no `dev` script and no recognizable framework config (`vite.config`, `next.config`, `nuxt.config`, `angular.json`, `svelte.config`), halt with `dev-server-not-applicable`.

### Step 1b — Read the framework's own dev lock/manifest FIRST

Some frameworks now record their running dev server themselves — Next.js 16 added a lockfile mechanism
that prevents a second `next dev` on the same project, and prints where the running one is. **A file the
framework wrote is authoritative for URL and PID; the port-probing heuristic below is the fallback for
frameworks that write nothing.** Check for it before probing, and if it exists, trust it over `lsof`.

Confirm the exact path against the installed version's own docs before relying on it — this skill does
not hardcode a path it has not verified for that version, and a stale guess is worse than the probe.

### Step 2 — Detect the port

Order of precedence:
1. `port_override` input.
2. Explicit port in the chosen member's `vite.config.ts` `server.port` / `next.config.js` / `nuxt.config.ts`, or a `--port` flag inside its own `dev` script.
3. Framework default: Vite → 5173, Next → 3000, Nuxt → 3000, Angular → 4200, SvelteKit → 5173, Remix → 3000. **In a workspace, two members can share one default** — `apps/web` and `apps/admin` both on 3000. Whichever booted first owns the port; the second is not this app, so treat that as the collision path in Step 3, not as `already-running`.
4. Fall back to 3000.

### Step 3 — Idempotency check

```bash
lsof -nP -iTCP:<port> -sTCP:LISTEN 2>/dev/null
```

If a process is already listening on that port AND it's a node/bun process (`lsof` output contains `node` or `bun`), assume it's the dev server — but confirm it is **this member's** server, not a sibling workspace member or another repo squatting on the same default port (probe the body for this app's mount point / title / a route only this member serves before adopting it). In a workspace this check is not optional: the sibling app is a node process serving 200s on the expected port, so an unprobed adoption always succeeds and is always wrong. Probe `http://localhost:<port>` with a 2-second timeout — 200 / 304 / any 4xx other than 404 means it's serving. Return `already-running` with the URL.

If something else is listening (Postgres on 5432, etc.), choose `port_override = port + 1`, retry.

### Step 4 — Launch in background

```bash
mkdir -p "$WS_ROOT/.claude"
LOG="$WS_ROOT/.claude/dev-server${MEMBER:+.$MEMBER}.log"; PIDF="$WS_ROOT/.claude/dev-server${MEMBER:+.$MEMBER}.pid"
( cd "$PROJECT_ROOT" && exec nohup <pkg-manager> dev ) > "$LOG" 2>&1 &
echo $! > "$PIDF"
[ -s "$PIDF" ] && kill -0 "$(cat "$PIDF")" 2>/dev/null || { echo "dev-server-start: no live PID recorded"; exit 1; }
```

`$!` is set only in the shell that ran the `&`. The earlier form, `( cd … && <pm> dev … & )` followed by `echo $! > pid`, backgrounded inside a subshell, so the outer `$!` was empty and every later cleanup killed nothing. Here the subshell itself is backgrounded and `exec` replaces it with the package manager, so `$!` is that process. It is the package manager's PID, not the bundler's: for cleanup, kill it and then whatever still listens on the port (`lsof -t -nP -iTCP:<port> -sTCP:LISTEN`). `kill -0` checks liveness without `ps`, which some sandboxes refuse. `WS_ROOT` is the workspace root (Step 0, item 5) and `MEMBER` the member name, empty in a single-package repo.

### Step 5 — Wait for ready

Poll `http://localhost:<port>` every 500ms. Ready conditions:
- HTTP 200 / 304 / 304-equivalent.
- For SPAs: response body contains the root mount-point (`<div id="app">`, `<div id="__next">`, etc.) — guards against the framework still bundling.

Timeout: 60 seconds. On timeout, print last 30 lines of `.claude/dev-server.log` and halt with `dev-server-timeout`.

### Step 6 — Hand off

Return:
- `url` — `http://localhost:<port>` (or override).
- `pid` — for the caller to kill on cleanup if it owns lifecycle.
- `mode` — `started-fresh` or `already-running` (caller decides whether to kill on exit; never kill an already-running server).

## Output format

```
dev-server-start
  root: apps/web        (workspace: pnpm + turbo; 2 app members, app_target given)
  pkg-mgr: pnpm
  cmd: pnpm dev
  port: 5173
  mode: started-fresh
  pid: 84321
  url: http://localhost:5173
  log: .claude/dev-server.log
  ready-after: 4.2s
```

## Failure modes

- **Port collided with non-dev process** — detected (Postgres, system service); skill auto-bumps and retries on `port + 1`. If still colliding after 3 bumps, halt.
- **Bundler error** — dev server exits in <2s with non-zero code. Skill detects via `kill -0` on the recorded PID + log inspection. Surfaces last 30 log lines + halts.
- **Watcher exhausted** (Linux ENOSPC) — fs.inotify limit hit. Surface the precise error + suggest `sudo sysctl fs.inotify.max_user_watches=524288`.
- **Wrong project root** — `package.json` not found at `$PROJECT_ROOT`. Halt; do not start a server in the wrong dir.
- **Workspace fan-out mistaken for one server** — the root `dev` delegates to `turbo` / `nx` / `pnpm -r`, N servers boot, and the ready probe adopts whichever app won the default port. Prevented by Step 0; if the fan-out already started, kill it and re-run against a single member rather than probing your way out.
- **Sibling member adopted as `already-running`** — two members share a framework default port and the idempotency probe skipped the body check. The run then verifies the wrong app and reports PASS.

## Related

- `verify-with-playwright` — typical caller; consumes the returned URL.
- `a11y-scan`, `visual-check`, `ssr-audit` — also depend on a running server.
- To stop the server: kill the PID recorded in `.claude/dev-server.pid` (if present), then any process still listening on the port (the package manager's child), and clear the file.

## Hard rules

- **Idempotent.** Re-running this skill in a session must never spawn a duplicate server. The port-detection step is non-skippable.
- **Background only.** Never block the agent's main loop on the server's stdout. Tail the log on demand.
- **Never start a server in production / CI mode** — refuse if `NODE_ENV=production` or `CI=true` is set.
- **Project-root verified, and chosen rather than assumed.** Step 0 selects `PROJECT_ROOT`; `package.json` must exist there. No fallback to `cwd`, and no fallback to the workspace root when the target is a member.
- **One member per run.** This skill starts a single dev server. Starting a workspace's whole app set is out of scope — the caller runs it once per member with an explicit `app_target`.

## Halt conditions

- Halt if `package.json` has no `dev` / `start` script and no recognised framework config — do not fabricate a start command.
- Halt if the lockfile + package manager don't match (e.g., `pnpm-lock.yaml` present but `npm` requested). Mirror what the project actually ships with.
- Halt if the port collides with a non-dev process after 3 bumps — stop guessing, surface the conflict.
- Halt if the server exits within 2s of launch — capture the last 30 log lines and refuse to declare success.
- Halt if the PID file is empty or names a dead process after launch — a server nobody can stop is not `started-fresh`.
- Halt `workspace-target-ambiguous` if the repo is a workspace with more than one app member and no `app_target` was given. List the candidates with their dev script, framework and configured port; picking one is the caller's decision, not the run's.
- Halt if the resolved start command is a fan-out runner (`turbo run dev`, `nx run-many`, `pnpm -r dev`, `npm run dev --workspaces`, `concurrently`) — that starts N servers and this skill returns one `url`. Re-resolve to a member first.
