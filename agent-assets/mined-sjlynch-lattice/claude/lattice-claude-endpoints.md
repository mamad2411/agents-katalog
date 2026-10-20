# backend/src/ws/endpoints

Endpoint-specific WebSocket builders. `../wsServer.ts` is the only place that
attaches them to HTTP upgrades.

- Most endpoints are project-scoped and should use `buildProjectWss` or
  `buildProjectSnapshotWss` from `../projectEndpoint.ts`; they require a
  `?project=` query and close on missing/invalid projects.
- Two endpoints sit outside the project helpers. Do not force either through
  them:
  - `/ws/terminal` proxies terminal-server sessions and uses its own query
    (`id`, `cwd`, `cols`, `rows`, `initialCommand`).
  - `/ws/harnesses` (`harnesses.ts`) is a raw `WebSocketServer({noServer:true})`
    with no `?project=`. Harness availability is machine-global, so it pushes
    every detection result to every client.
- Initial snapshots should be small and safe to send once per connection;
  broadcast payloads are serialized once per event by the shared helper.
- **`/ws/tasks` is the standing exception: a known large payload.** On connect
  its `initial` sends the entire, unclipped board via `listTasks(project)`
  (`tasks.ts`), including every done task's description and summary. On the
  Lattice repo that is ~2.3 MB for ~750 tasks. It sends the whole board again
  as `{type:'tasks', tasks}` on every coalesced task mutation (one frame per
  project per event-loop turn, see `ProjectStateManager.notifyProject`), to
  every open tab. `GET /api/tasks` returns a 413 above 256 KB
  (`LIST_RESPONSE_CEILING_BYTES`), but this path has no cap. This matters for
  the browser out-of-memory investigation: each frame is a fresh multi-MB
  string the browser must allocate and `JSON.parse`. **Any change that raises
  task-mutation frequency multiplies that cost per tab.** For example, writing
  a task field on every agent activity event would turn each tool call into a
  whole-board frame. Send such high-rate signals as their own transient event
  type, as `task-activity` / `agent-activity` already are.
- Keep event filtering by canonical project path on the server side so tabs for
  other projects never receive unrelated state. `/ws/terminal-activity` (the
  sidebar tab spinner) is the one deliberate exception: it takes `?project=` to
  scope the CONNECTION like everything else, but its payload is machine-wide.
  Session ids are opaque, the sidebar already scopes its own tab list, and a
  session's `projectPath` can legitimately be a worktree rather than the project
  root — filtering on it would silently drop the task tabs the spinner exists
  for. Don't "fix" it by adding a project filter.
- `/ws/workflow-runs`' `hello` is the client's authoritative active-runs
  snapshot, but after a restart the runs are only back once post-listen
  recovery registers them. Until `isWorkflowRecoveryDone()` it therefore sends
  `{type:'hello', runs, recovering: true}` (merged additively by the client)
  and follows up per connection with an authoritative hello when recovery
  lands. `/ws/tasks` needs no such flag (tasks load from disk on demand);
  `/ws/merge-runs` / `/ws/post-merge-hooks` send `idle` until a resumed run
  re-announces itself, which only blanks a display strip — no client state
  machine reads it as "finished".
- Add a new endpoint by adding a builder here and a route tuple in
  `wsServer.ts`.
