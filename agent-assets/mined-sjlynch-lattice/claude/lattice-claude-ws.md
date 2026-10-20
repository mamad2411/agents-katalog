# backend/src/ws

WebSocket endpoints all use `WebSocketServer({ noServer: true })` and are dispatched by the single `upgrade` listener in `wsServer.ts`. Do not add per-path `{ server, path }` WSS instances; the first listener to reject an upgrade can break the matching endpoint.

- `wsServer.ts` — public `attachWebSockets(server)` entry point and pathname route table. Nothing in the `upgrade` listener may throw: it runs outside any request handler, so a throw is an uncaughtException and processGuards exits the backend. `req.url` can be an absolute-form target Node's parser accepts but `new URL` rejects (`GET http://[`), so the pathname goes through `upgradePathname` (null → socket destroyed), and `parseProject` guards the same parse.
- `projectEndpoint.ts` — public factories (`buildProjectWss`, `buildProjectSnapshotWss`), `parseProject`, `projectFromRunEvent`, and re-exports of `sendJson` and the contracts. Owns the serializer and per-WSS `WeakMap`: the same broadcast object is serialized once across clients; never move that cache into a connection. `subscribe` runs once per connection, so a listener that wraps the store's event must hand every connection the SAME wrapper (memoize it on the source object, as `buildProjectSnapshotWss` and `endpoints/tasks.ts` do) — a fresh `{ ...wrapper }` per connection silently misses the cache and re-stringifies a multi-MB board once per open tab.
- `projectConnection.ts` — `handleProjectConnection` owns each validated project's socket, subscription, initial-load settlement, and FIFO event draining; `sendJson` sends single-recipient payloads.
- `projectEndpointContracts.ts` — shared options/event types and limits, with no dependency on the factory or connection helper.
- `endpoints/` — endpoint-specific initial payloads/subscriptions for terminal,
  terminal-tabs (the durable tab registry: `hello` snapshot + live
  upsert/ended/removed/restored events, see `terminalRegistry/`),
  tasks, agent-sessions, merge-runs, post-merge-hooks, workflows,
  workflow-runs, health, git-branch (navbar branch chip, `.git/HEAD` watcher),
  git-status (timeline-scrubber live refresh, `.git`-metadata + working-tree
  watcher), and harness availability.

Project connection invariants:

- Subscribe before loading `initial`; filter by project before buffering. During the load, full snapshot events invalidate it (at most `MAX_INITIAL_SNAPSHOT_LOADS` = 3 loads, then send the latest load); deltas/transients drain in FIFO order after it. No `initial` means immediate forwarding. Mixing snapshots and deltas of the same state would need extra care: reloads can overtake buffered deltas.
- Initial-load failure closes by default. With `initialError: 'ignore'`, use the last successful load, or otherwise the latest snapshot event from the failed load, then drain buffered events. Keep attachment/load await points and send ordering unchanged.
- Idempotent cleanup on close or overflow clears buffered events, the fallback snapshot, and budget bookkeeping before unsubscribing; a late subscription result is immediately unsubscribed. Events and initial completions are fenced against closed/non-OPEN sockets. Routine socket errors are ignored so they cannot crash the backend.
- Handshake buffering retains at most `PROJECT_WS_MAX_PENDING_EVENTS` (4096) events and `PROJECT_WS_MAX_PENDING_BYTES` (16 MB of serialized UTF-8 payloads), including the latest fallback snapshot. Snapshot replacement/reload releases that snapshot's budget. Measurement uses the shared per-WSS serializer/cache. Overflow logs once, cleans up immediately, and terminates for a fresh snapshot on reconnect.
- `forward` also guards slow clients: `bufferedAmount > PROJECT_WS_HIGH_WATER_BYTES` (16 MB), after the OPEN check and before serialization/send, terminates and logs once using the same cleanup. Initial `sendJson` bypasses this send-buffer guard; fallback snapshots and buffered events use it.

Contract coverage in `../__tests__/`: `projectEndpointSnapshotRace.test.ts`, `projectWsSlowClient.test.ts`, `projectWsHandshakeBuffer.test.ts`, `projectWsSerializeOnce.test.ts`, `wsConnectionErrorHandler.test.ts`, `relativeProjectRefused.test.ts`, and `wsMalformedUpgradeUrl.test.ts`. Keep their assertions and the existing `projectEndpoint.ts` import surface stable.
