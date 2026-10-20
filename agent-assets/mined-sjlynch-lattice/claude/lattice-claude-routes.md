# backend/src/routes

One Express `Router` per domain, each built by a `buildXRouter(...)` factory
and mounted by `server/app.ts` `mountRouteFactories` (read the order there).
Every route, one row each: [ROUTES.md](./ROUTES.md). Business logic lives in
the domain module each router wraps, not here.

## Route map

- `restartDrain.ts` — the dev runner's restart handshake
  (`/api/internal/restart-drain/{prepare,cancel,lock-holders}`: refuses any
  `Origin`, requires `x-lattice-terminal-token`) and
  `buildRestartDrainAdmissionGate`, which 503s (`backend-restarting`,
  `Retry-After`) new top-level starts during a drain. **Must stay mounted
  FIRST** so the gate runs before the routes it guards. See
  `../restartDrain/CLAUDE.md`.
- `buildCallbackOutboxAck` (`../callbackOutbox/ack.ts`, middleware, mounted
  right after restartDrain) — for a POST matching `CALLBACK_PATH_RE`
  (`../callbackOutbox/drain.ts`) it unlinks that callback's durable outbox
  entry once the response is final (anything but 5xx / 408 / 429), because
  the hook that sent it may be killed by the cleanup the callback triggers.
  Replays (`OUTBOX_REPLAY_HEADER`) are skipped; the drain removes those
  itself. See `../callbackOutbox/CLAUDE.md`.
- `health.ts` — composes `health/`: `liveness.ts`, `scan.ts` (scan +
  agent-facing dead-code summary), `gitInfo.ts` (`/api/git-history`,
  `/api/git-branch`), `browse.ts` (folder picker). `scan.ts` shares scans
  across subscribers and detects a disconnect via the unfinished
  *response's* `close` — never the request's, which a fully consumed GET can
  emit while its response still waits.
  `scan.ts` also serves `/api/source-areas`, its `/resolve` preview and
  `/api/source-tree`, using `sourceAreasCollect.ts` for weighted, generated-free
  source and package roots; shared logic lives in `shared/sourceAreas.ts`.
- `debug.ts` — `/api/debug/*` memory diagnostics, mounted right after health
  (`../memDiag/CLAUDE.md`).
- `search.ts` — `/api/search` file-content grep (rg fast path, JS fallback).
- `settings.ts` — per-project settings, env notes, instruction templates, Codex models, Pi
  models/endpoint probe; see [settings/CLAUDE.md](settings/CLAUDE.md).
- `globalSettings.ts` — `/api/global-settings`; a PATCH applies the spawn
  `softCap` live and reconciles Pi providers when they change.
- `mcp.ts` — MCP catalog, secrets, env presence, validation, config import.
- `opengrep.ts` — Opengrep (SAST), thin over `../opengrep/` (see its
  CLAUDE.md): status, the user-clicked engine / rule-pack install (202 + poll
  `/status`), the agent-facing scan / stored scans / cancel, and `/ignore`.
  Errors map to codes (409 `busy` / `not-installed` / `no-rules` / …, 400
  `bad-target` for a target outside the project; full list in ROUTES.md).
  Pack install/remove also answer 409 `busy`
  while ANY project's scan runs — a pack swap under a reading engine is a
  half-swapped tree (or a Windows EBUSY).
- `opengrepReview.ts` (mounted by `opengrep.ts`) — triage history /
  disposition, shared-ignore (creates a reviewed source-suppression task) and
  interactive security reviews (`/reviews`, `/reviews/:id/{done,cancel}`:
  `done` marks the turn waiting without closing the conversation). No report
  storage or apply endpoint — the harness waits for the user's choice before
  creating the agreed Open tasks. Writes require an existing project
  directory; `done` takes the project in its query.
- `projectInit.ts` — `POST /api/project-init/preview` (re-POSTed as the user
  edits the `.gitignore`) and `POST /api/project-init`. Thin: validation plus
  the `ProjectInitError.code` → 409/422/500/503 mapping; work in
  `../projectInit/`.
- `terminals.ts` — terminal list + spawn-queue snapshot (debug),
  `DELETE /api/terminals/:id`, and `POST /api/terminals`: pre-creates a pty
  via `proxyCreateSession` and returns its `serverId`, so a sidebar harness
  terminal goes through the spawn chokepoint (`resolveHarnessSpawnBody`) and
  gets its Codex/Pi MCP config — a serverless `/ws/terminal` connect would
  bypass it.
- `terminalTabs.ts` — the durable tab registry's surface
  (`../terminalRegistry/`), all `?project=`-scoped. `DELETE …/:id` order:
  persist the close intent, abort a post-merge hook owning the pty, kill the
  pty, then remove the record; an uncertain kill keeps ownership and returns
  a retryable 503 (same abort as `DELETE /api/terminals/:id`).
- `tasks.ts` — the task API; see [tasks/CLAUDE.md](tasks/CLAUDE.md). Its
  list / summary / search reads are the agent-facing progressive-disclosure
  surface (active-lane + compact + newest-100 defaults, self-pricing
  envelopes, 256 KB ceiling → 413).
- `agentActivity.ts` — `/api/agent-activity/:token` for Lattice-spawned
  non-worktree sessions (push / workflow / post-merge) → graph beams.
- `projectClaude.ts` — project-root instrumentation install/remove plus
  `/api/project-activity/:token`, the activity callback for every
  project-instrumented session (user Claude via `.claude/settings.local.json`,
  user Codex tabs via per-launch hook overrides, the project-root Pi
  extension), keyed by the body's `session_id`.
- `mergeRuns.ts` — merge-all start / active / get / cancel / stash-resolved.
- `postMergeHooks.ts` — active/recent read, completion callback, abort.
- `pushRuns.ts` — `/api/git-check` plus push-run start / status / done /
  forget. `hasGit` keeps its exact `fs.stat(<path>/.git)` semantics (the Push
  button reads it and must not appear for a repo's subdirectories); the Git
  Setup chip's `git: ProjectGitProbe` is additive.
- `qaRuns.ts` — QA e2e run start / status / verdict / done / forget; its
  load-bearing response shapes, duplicate-run guard and tolerant verdict
  parse are in [qaRuns/CLAUDE.md](qaRuns/CLAUDE.md).
- `workflows.ts` — workflow definitions and runs; see
  [workflows/CLAUDE.md](workflows/CLAUDE.md).
- `projectParam.ts` — the project/path readers below.

## The `project` parameter

- **`readProjectParam(req, res, {source?, optional?})` is the ONE way a
  non-task route reads its project** (`?project=` first, then the body; the
  tasks routes' `requireAbsoluteProject` / `validateProjectForCreate` apply
  the same rule). Act on the value it returns (trimmed), never the raw field.
- **A relative or drive-relative value is a 400** naming the likely cause
  (shell-stripped backslashes: `C:developmentproj`). On Windows a
  ROOT-relative value (`\foo`, or MSYS `/c/development/proj`, whose 400
  suggests `C:\development\proj`) is refused too: `path.isAbsolute` accepts
  it but `path.resolve` pins it to the backend's drive — a silently-empty
  board. Every guard (these routes, `ws/projectEndpoint.ts` `parseProject`,
  the task cache's `ensureProjectLoaded`) uses `isRealAbsoluteProjectPath`
  (`../projectPath.ts`), never bare `path.isAbsolute`.
- **Validate before identity resolution**: resolving a rejected value first
  can make it absolute under the backend's cwd/drive, bypass downstream
  guards, and register a phantom project with a junk identity binding.
  (Canonical spelling vs. storage-hash bindings:
  [project identity](../projectIdentity/CLAUDE.md).)
- `POST /api/terminals` applies the rule to `cwd` and `projectPath`; the
  folder browser (`/api/list-dir`, `/api/create-dir`, `../fsbrowse/`) uses
  `isRealAbsoluteProjectPath` + `relativeProjectError`.
- **A route that WRITES under the project folder also requires an existing
  directory** (`requireExistingProjectDir`): `POST /api/project-instrumentation`
  (mkdirs `.claude/`), `PATCH /api/settings`, `POST /api/opengrep/ignore`
  (the settings store mkdirs `.lattice/`) — else a typo'd or deleted project
  is recreated by the next save.
- Read-only graph routes with a default-root fallback (`/api/scan`,
  `/api/search`, `/api/health/dead-code`, `/api/git-history`,
  `/api/git-branch`) use `readPathParam`: absent → default root,
  present-but-relative → the same 400. WS endpoints close the socket
  (`parseProject` yields `''`).
- By-id routes honour an optional `?project=` ownership pin
  (`requireOwnedByRequestedProject`; tasks: `requireTaskInRequestedProject`):
  another board's record is a 404, checked before any side effect.
  Absent/empty → unpinned (Stop hooks and resolver curls send none).
- Pinned by `__tests__/relativeProjectRefused.test.ts`, which drives every
  project-scoped route (and `/ws/tasks`) through the real app.

## Why factories?

Routers need `backendOrigin` (for the curl callbacks baked into hooks and
prompts), computed by `server/config.ts` and threaded through
`mountRouteFactories` — passing it in keeps routers testable, no globals.

## Adding a route

0. Add its row to [ROUTES.md](./ROUTES.md) (drift-tested) and either document
   it for agents (`../latticeApiDocs/*.template.md`) or opt it out in the
   drift test's `UNDOCUMENTED_ROUTES` with a reason.
1. Add a handler to the right module (or create a new `buildXRouter`).
2. Mount it from `server/app.ts` in an order where no parameter route shadows
   a static path.
3. Sync and async handler errors reach the global JSON error middleware in
   `server/app.ts` (`express-async-errors`).
4. A **completion-callback** route (one a Stop hook POSTs through the
   callback outbox) must end in a `CALLBACK_PATH_RE` suffix (`/complete`,
   `/done`, `/verdict`, `/merged`, `/merge-aborted`, `/stash-resolved`), or
   the ack never clears its outbox entry and the drain drops it as "not a
   completion callback route" — a callback lost in a restart is never
   redelivered. New suffix → extend the shared regex in
   `../callbackOutbox/drain.ts`; don't write a second filter.

Commands (from `backend/`): `npm run build`, `npm test`, `npx tsc --noEmit`;
HOME-isolated single-file runs: [the test guide](../__tests__/CLAUDE.md).
