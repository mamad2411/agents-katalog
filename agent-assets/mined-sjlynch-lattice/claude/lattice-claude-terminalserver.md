# backend/src/terminalServer

The **detached terminal-server** that runs as its own process on `:5185`,
separate from the main backend (`:5184`). PTY sessions — and the Claude/Pi/codex
agents inside them — live here so a main-server restart (`tsc -w`, a dev
restart, a crash) never kills a running agent. The main server reconnects on its
next boot.

`terminal-server.ts` (one level up) is the detached **entry point**; this folder
holds its pieces. The agent-facing PTY machinery itself lives in `../terminal/`
(re-exported via `../terminal.ts`); this folder is just the process's HTTP/WS/
lifecycle shell.

## The boundary

The terminal-server is a **dumb executor**. It never resolves spawn policy
(MCP servers, trust, memory opt-out) — the main backend does that and ships the
result as DATA in the `POST /sessions` body, which `createSessionHandler.ts`
applies verbatim microseconds before `pty.spawn` (`applyClaudeProjectConfig`).
Keeping resolution out of this long-lived process is deliberate: a spawn-policy
change is then a backend-only edit that never forces an agent-killing respawn of
this server.

The two sides of the wire:

- **Client side (main backend):** `../terminalServerClient.ts` (a barrel over
  `../terminalServerClient/`) is the HTTP client — `proxyCreateSession`,
  `proxyListSessions`/`Count`/`…OrNull`, `proxyKillSession[sByCwd]`,
  `proxyShutdown`. `../terminalServerLifecycle.ts` owns spawn/respawn/health
  (`BASE`, `ensureTerminalServer`) and the fingerprint check. Each ConPTY spawn
  blocks this process's event loop (~150 ms), so a spawn burst can miss the
  500 ms health probe: `ensureTerminalServer` re-probes a timeout for up to
  10 s rather than failing the spawn (it failed every restored Claude tab).
  `../terminalServerStatus.ts` reports it read-only (`GET
  /api/terminal-server/status` → `current`/`stale`/`absent`/`unavailable` +
  the session count a `stale` update is waiting on) for the navbar's
  "Terminal server update pending" chip — a deferred update is otherwise only
  one console line, and with the user's terminals open it can last forever.
- **Server side (this folder):** the routes that serve those calls.

Anything new this process loads at runtime must be added to
`../terminalFingerprint.ts`'s `FINGERPRINT_FILES`, so a byte change makes an older
executor distinguishable. `../terminalProtocol.ts` defines wire compatibility;
only incompatible wire changes bump its protocol version. A compatible older
executor is reused while it has live or starting sessions. Upgrade uses the
authenticated, instance-pinned `POST /shutdown-if-idle` and only replaces an
empty executor. Fingerprint-only legacy servers are retained until the user's
next normal shutdown/restart because they cannot atomically prove idle and
close admission. Unknown/unhealthy listeners are never force-killed.

## Layout

- `processGuards.ts` — `installTerminalProcessGuards()`: swallow node-pty's known
  Windows cleanup throw; every other uncaught exception/rejection is logged and
  then fails fast (exit 1) rather than leaving this detached process running in
  an undefined state (the main backend respawns it on demand). Installed first,
  before any PTY can throw asynchronously. Fail-fast contract regression-covered
  by `../__tests__/processGuards.test.ts`.
- `routes.ts` — `registerTerminalRoutes(app, { fingerprint, shutdown, authToken,
  admission?, instanceId?, sessionCount?, sessionHandler?,
  onAuthenticatedRequest? })` (the optional ones default to a fresh admission
  gate, a random instance id, the live session count, and
  `createSessionHandler()`; `sessionHandler` is a test seam;
  `onAuthenticatedRequest` fires on each token-authenticated request —
  `terminal-server.ts` stamps the last-backend-contact time `parentWatch` relies
  on): the JSON HTTP surface — `GET /health` (fingerprint, protocol, instance
  ID and capabilities), protected
  `GET /sessions`, `POST /sessions`, `DELETE /sessions/by-cwd` (**must** precede
  `/:id` — Express matches in registration order), `DELETE /sessions/:id`, and
  `POST /shutdown` (explicit user shutdown), `POST /shutdown-if-idle` (upgrade).
  Protected routes reject disallowed browser `Origin`s and
  require the shared terminal-server token header. The token must ride in a
  **custom** header (`x-lattice-terminal-token`), constant-time-compared via
  `tokenMatches` — a custom header is the invariant that keeps a browser
  form-POST (can't set custom headers) or a cross-site fetch (can't read the
  response) from driving PTY create/shutdown against the loopback port. A
  catch-all 404 + error middleware force a **JSON-only** body so the client's
  `await res.json()` never explodes on stray HTML.
- `createSessionHandler.ts` — `POST /sessions` implementation: pre-create a pty;
  applies the backend-resolved Claude config, returns `{ id }`, or
  `503 {code:'CAP'}` at the hard cap.
- `sessionRequests.ts` — shares pending/results by request ID so a lost response
  cannot execute the agent twice. IDs are bound to identical request bytes and
  this executor instance. The registry stores hashes and results, caps at 4096,
  retains completed requests for ten minutes, and refuses request identities
  older than five minutes (so eviction never enables replay). Pending requests
  are never evicted; a full registry refuses new admission.
- `admission.ts` — one synchronous gate shared by HTTP and WS session creation
  and idle shutdown. Async config writes hold admission even after an HTTP
  client disconnects. A successful idle shutdown fences all later new sessions.
- `websocket.ts` — the `/ws/terminal` upgrade handler: parse the query
  (`id`/`cwd`/`cols`/`rows`/`initialCommand`/`projectPath`) and hand the socket to
  `attachTerminal`. Disallowed browser `Origin`s (CSWSH defence — this handler
  runs `initialCommand` on a fresh pty) and non-matching upgrade paths are
  destroyed before the upgrade. A target `new URL()` rejects is refused, never
  thrown on — a throw there exits the executor and every live pty with it.
- `shutdown.ts` — `createTerminalShutdown()` (idempotent: kill every session, wait
  ~500 ms for `taskkill /T` to walk the tree, then `process.exit(0)`) +
  `wireTerminalShutdownSignals` (SIGTERM/SIGINT).
- `parentWatch.ts` — `watchParentProcess(parentPid, tryShutdown)`: poll
  `BACKEND_PARENT_PID` (the long-lived orchestrator's pid, stable across dev
  restarts); once it is gone, ask `tryShutdown` every tick until it agrees.
  `terminal-server.ts` agrees only when no backend has made an authenticated
  request for 60 s (a newer backend adopts an existing server without changing
  `BACKEND_PARENT_PID`) **and** `admission.closeIfIdle(sessionCount())` — so an
  ungracefully-killed orchestrator (crash, `taskkill /F`, closed console) no
  longer takes every running agent down with it five seconds later
  (2026-09-22); the next backend adopts the busy server (a fingerprint
  mismatch is already "update deferred" while sessions are live). An idle
  orphan still exits. A graceful `npm run dev` stop is unchanged: `dev.mjs`
  POSTs `/shutdown`, and terminal-tab restore relaunches the agents into their
  conversations on the next start. The dev console's **soft restart / detach**
  (`r` / `d`, see `scripts/CLAUDE.md`) replaces `dev.mjs` WITHOUT that POST, so
  `BACKEND_PARENT_PID` names a dead runner from then on and only the
  contact/idle rule applies — which is why the watch treats "parent gone" as
  **sticky**: a recycled pid must not read as the parent coming back, or an
  idle, unowned server would never exit (`__tests__/terminalServerParentWatch.test.ts`).

## Why detached / why no `&` kill

Because it's detached + unref'd, this process does **not** see the dev
orchestrator's Ctrl+C — that's exactly what `POST /shutdown` (sent by
`shutdownTerminalServer` in `backend/scripts/dev/backendLifecycle.mjs`, 2.5 s
timeout; the backend's `proxyShutdown` is an unused re-export) and the
`parentWatch` fallback are for. Don't "fix" the detachment; it's what keeps
agents alive across restarts.
