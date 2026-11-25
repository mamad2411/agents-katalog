---
name: build-realtime-channel
description: Builds realtime push channels over WebSocket/SSE — auth-on-connect, heartbeat/zombie eviction, topic subscribe/publish with per-topic authz and presence, sequence-numbered resume for missed-message recovery, client reconnect with backoff+jitter, and a Redis/NATS pub/sub backplane with send-buffer limits for horizontal scale.
when_to_use: Adding live updates (chat, notifications, live dashboards, collaborative cursors, feeds), choosing WebSocket vs SSE vs long-poll, or fixing a channel that drops messages, leaks connections, thunders on reconnect, or can't scale past one server. Distinct from message-queue-jobs (durable server-to-server work queues) and manage-client-server-state (client cache/refetch, not the transport).
---

## When to Use

Reach for this skill when the request is about **pushing live data to clients over a long-lived connection**:

- "Push notifications / chat messages / order updates to the browser in realtime"
- "Build a live dashboard / activity feed / collaborative cursors that updates without polling"
- "Should this be WebSocket, SSE, or long-poll?"
- "Our socket drops messages after a reconnect" / "clients miss updates while disconnected"
- "Connections leak — server FD count climbs and never drops" / "zombie sockets pile up"
- "On deploy every client reconnects at once and melts the box" (thundering herd)
- "Realtime works on one node but breaks behind a load balancer / can't scale out"

NOT this skill:
- Durable server-to-server work queues, retries, dead-letter, exactly-once job processing → message-queue-jobs (this skill is at-most/at-least-once *push to clients*, not a job system)
- Native mobile push via APNs/FCM, device-token registration, woken-from-killed delivery → implement-push-notifications (OS push to a closed app; this skill is an open in-app socket/stream)
- Client-side cache, refetch, optimistic UI, query invalidation → manage-client-server-state (that's what the client *does* with pushed data; this is the wire)
- Issuing/validating the token itself, refresh, session rotation → auth-jwt-session (this skill *consumes* a token on connect, it doesn't mint it)
- Capping how many connects/messages a client may send → rate-limiting
- Races inside your fan-out/handler code (shared mutable state, missing await) → async-concurrency-correctness
- Metrics/tracing/log wiring for the channel → observability-instrument

## Steps

1. **Pick the transport by directionality — do not default to WebSocket.** Most "realtime" needs are server→client only.

   | Transport | Use when | Cost / caveat |
   |---|---|---|
   | **SSE** (`text/event-stream`) | Server→client only (feeds, notifications, dashboards, token streaming). **Default for one-way.** | One HTTP/1.1 conn per stream (use HTTP/2 to avoid 6-conn cap); auto-reconnect + `Last-Event-ID` built in; no binary |
   | **WebSocket** | True bidirectional, low-latency, high message rate (chat, presence, games, collaborative editing) | Manual heartbeat/reconnect/resume; no auto-resume; proxies/LBs need explicit `Upgrade` support |
   | **Long-poll** | Fallback only when SSE/WS are blocked (ancient proxy, locked-down corp net) | High overhead, ~1 msg per round trip; keep as graceful degradation, not primary |

   Rule: one-way → **SSE**; bidirectional or >~10 msg/s/client → **WebSocket**; long-poll only as fallback. Don't hand-roll if a maintained lib fits — `Socket.IO` (built-in reconnect+rooms+fallback), `Phoenix Channels` (presence+backpressure+cluster PubSub out of the box), `Centrifugo` (standalone server, history/recovery built in), `SignalR` (.NET). Raw `ws`/SSE only when you need full control and will build lifecycle yourself.

2. **Authenticate on connect — never in the query string.** A token in `?token=...` lands in access logs, proxy logs, and `Referer`. Validate *before* upgrading.
   - **WebSocket:** pass the token via the `Sec-WebSocket-Protocol` subprotocol header, or require an authenticated **cookie** (sent automatically on the upgrade), or accept an unauthenticated socket and require an `auth` frame as the **first message** within a short deadline (≤5s) or close.
   - **SSE:** EventSource can't set headers — use a same-site auth **cookie**, or a short-lived single-use ticket fetched over a normal authed request then passed once.
   - On bad/expired token: WS close code **`4401`** (app range; reserve `4403` for authz failure), SSE respond **`401`** before the stream opens. Re-check token expiry on long-lived sockets; close when it lapses.

   ```js
   // WS upgrade with subprotocol-carried token (client)
   new WebSocket("wss://api.example.com/ws", ["bearer", token]);
   // server: read token from Sec-WebSocket-Protocol, verify, then accept (echo the protocol)
   ```

3. **Run the full connection lifecycle — this is where leaks live.**
   - **Heartbeat:** WS — server sends `ping` every **30s**, expects `pong`; if 2 missed (60s), terminate the socket (a half-open TCP conn looks alive to the OS but is dead). SSE — emit a comment line `:keep-alive\n\n` every 15–30s so proxies don't idle-close. `ws` clients that never `pong` are zombies; an `isAlive` flag flipped false on each ping and reset on pong evicts them.
   - **Zombie eviction:** sweep on an interval; `socket.terminate()` (not `.close()`) anything that failed the heartbeat. Track open connections in a registry so you can count and reap them.
   - **Graceful drain on deploy:** on `SIGTERM`, stop accepting new connections, send a `going_away` app message (so clients reconnect *staggered*, not instantly), then close with code **`1001`** after a grace window. Never `kill -9` a live channel node — every client stampedes back at once.

4. **Model subscriptions as topics with per-topic authz, and add presence.** A connection is not a subscription. Let a client subscribe to named topics/channels (`chat:room:42`, `user:7:notifications`) over one socket.
   - **Authorize every subscribe** against the *current* user — a connection authed as user 7 must not subscribe to `user:9:*`. Check on subscribe, not just on connect; deny with an error frame, don't silently drop.
   - **Namespace topics** so wildcards can't leak (`org:{id}:...`). Reject subscribe to topics the user can't read.
   - **Presence:** maintain a per-topic set of members in the backplane (Redis `SET`/hash keyed by topic, member = `{userId, connId}`); broadcast `join`/`leave` on change. Tie membership to the connection so a dropped socket auto-removes the member (TTL-backed, refreshed by heartbeat — otherwise a crashed client lingers as "online" forever).

5. **Make missed-message recovery explicit with sequence numbers + a resume cursor — decide the delivery guarantee up front.** Default to **at-least-once + client dedup**, not "best effort."
   - Stamp every message per-topic with a monotonic **`seq`** (and an event `id`). Keep a bounded **history buffer** per topic (e.g. last N=1000 or last 5 min) in Redis (`XADD` to a stream, or a capped list).
   - On (re)subscribe the client sends its **last seen `seq`** (`resume_from`); server replays buffered events `> resume_from` then switches to live. SSE gets this for free: the browser auto-sends **`Last-Event-ID`** on reconnect — honor it and replay.
   - If the gap exceeds the buffer, send a **`reset`/snapshot-required** signal so the client refetches full state instead of silently missing data.
   - Guarantee table — pick one and document it:

   | Guarantee | Mechanism | Cost |
   |---|---|---|
   | Best-effort (at-most-once) | Fire-and-forget, no buffer | Drops on any disconnect — only for ephemeral (live cursor pos) |
   | **At-least-once + dedup** | seq + history buffer + resume cursor; client drops `seq ≤ lastSeen` | **Default.** Bounded buffer mem; client must dedup |
   | Exactly-once *delivery* | Don't. Use at-least-once + idempotent client apply | True E2E exactly-once is a distributed-systems tax you don't need |

6. **Reconnect on the client with backoff + jitter, then resubscribe and dedup.** A fixed-delay or zero-delay reconnect loop is how one deploy becomes a self-DDoS.

   ```js
   // exponential backoff, full jitter, cap 30s — applies to WS and SSE-with-manual-reconnect
   let attempt = 0;
   function reconnect() {
     const base = Math.min(30000, 1000 * 2 ** attempt++);
     const delay = Math.random() * base;          // full jitter — spreads the herd
     setTimeout(connect, delay);
   }
   // on open: attempt = 0; resubscribe all topics with resume_from=lastSeq[topic];
   //          drop any replayed event whose seq <= lastSeq[topic] (dedup)
   ```
   Reset the attempt counter on a *successful* open, resubscribe every topic with its own `resume_from`, and dedup replayed events by `seq`. Stop reconnecting on a fatal close code (`4401`/`4403`) — don't hammer a server that rejected your auth.

7. **Scale horizontally with a pub/sub backplane + per-connection backpressure.** A second node means a publish on node A must reach a subscriber on node B.
   - **Stateless + backplane (preferred):** each node holds its own sockets; publishes go to **Redis Pub/Sub**, **Redis Streams**, or **NATS**; every node subscribes and fans out to its local sockets for that topic. No sticky sessions needed for WS (the socket stays pinned to one node by TCP anyway); for SSE/long-poll across nodes you still need either a backplane or sticky routing.
   - **Sticky sessions:** only needed for handshake-split transports (Socket.IO long-poll→WS upgrade must hit the same node) — set LB affinity or force `transports: ['websocket']`. Prefer stateless+backplane over relying on stickiness.
   - **Backpressure / slow-consumer:** a client that reads slower than you write balloons the per-socket send buffer and OOMs the node. Cap it: watch `ws.bufferedAmount` (or your lib's queue depth); if it exceeds a threshold (e.g. 1–4 MB), **drop the slow consumer** (close `1013`/`4408`) rather than buffer unboundedly. For SSE, the same applies to the response stream's write backpressure. One slow consumer must never degrade the rest.

8. **Load + soak test, then observe.** Single-connection tests prove nothing about a channel (see Verify). Wire metrics (open conns, msgs/s, send-buffer high-water, reconnect rate, dropped-slow-consumers) via observability-instrument.

## Common Errors

- **Token in the query string.** `?token=...` leaks into access/proxy logs and `Referer`. Use subprotocol header, auth cookie, or a first-frame `auth` message.
- **No heartbeat → silent half-open sockets.** TCP keepalive defaults to ~2h; a dead peer looks connected for hours. App-level ping/pong (30s) + terminate on miss is mandatory.
- **`.close()` instead of `.terminate()` on a zombie.** `close()` waits for a close handshake the dead peer will never send, so the FD lingers. Terminate failed-heartbeat sockets.
- **Unbounded per-socket send buffer.** One slow/paused client grows `bufferedAmount` until the node OOMs and takes down *every* connection. Cap buffer; drop the slow consumer.
- **No jitter on reconnect.** All clients backoff on the same schedule and reconnect in lockstep after an outage/deploy — synchronized thundering herd. Add full jitter.
- **Instant/zero-delay reconnect loop.** A server that closes on every connect gets hammered thousands of times/sec. Always backoff; stop on fatal auth close codes.
- **Treating a connection as a subscription / authz only on connect.** A long-lived socket can request any topic later; authorize every `subscribe` against the current user, namespace topics, deny cross-tenant.
- **No sequence numbers → "messages disappear" after reconnect.** Without `seq` + history + resume there's no way to recover the gap; clients silently miss data. Stamp seq, buffer, replay from cursor (or `Last-Event-ID`).
- **In-memory subscriptions/presence with >1 node.** A publish on node A never reaches node B's subscribers; presence shows half the users. Use a Redis/NATS backplane; back presence with a TTL'd shared store.
- **Presence that never clears.** Membership tied to a clean disconnect only — a crashed client stays "online" forever. TTL the entry, refresh on heartbeat.
- **No graceful drain on deploy.** Killing a node drops every socket simultaneously and they all reconnect at once. SIGTERM → stop accepts → `going_away` (staggered reconnect) → close `1001`.
- **Relying on sticky sessions to "fix" scale.** Stickiness papers over a missing backplane and breaks the moment a node dies (all its clients fail over to a node that doesn't know their topics). Make nodes stateless + backplane; use stickiness only for handshake-split transports.
- **SSE without keep-alive comments.** Idle proxies/LBs close a quiet `text/event-stream` after their timeout. Emit `:keep-alive` every 15–30s.

## Verify

1. **Auth on connect:** connect with no/expired/forged token → rejected before the stream opens (WS close `4401`, SSE `401`); token never appears in `nginx`/access logs. Cross-tenant `subscribe` → denied with an error frame, not silently dropped.
2. **Heartbeat + zombie eviction:** `tc`/`iptables`-drop a client's traffic (simulate half-open) → server detects via missed pong within ~60s and `terminate()`s it; server open-connection gauge returns to baseline (no FD leak). Re-run 100× in a loop — count must not climb.
3. **Missed-message recovery:** subscribe, record `seq`, kill the client, publish 50 events, reconnect with `resume_from`/`Last-Event-ID` → client receives exactly those 50 in order, zero gaps, zero dupes after dedup. Exceed the buffer → client gets a `reset`/snapshot signal (not a silent gap).
4. **Reconnect storm (thundering herd):** connect 5–10k clients, restart/kill the node → reconnects spread over the backoff window (full-jitter histogram, not a spike); server stays up; all topics resubscribed. With zero jitter this test must visibly fail (then pass after adding jitter).
5. **Horizontal fan-out:** run ≥2 nodes behind an LB; a subscriber on node B receives a message published to node A → proves the backplane works, not just one box. Kill node A mid-stream → its clients fail over to node B and resume from cursor with no lost messages.
6. **Slow-consumer isolation:** one client stops reading (pause the socket) while others stay live → the slow one is dropped (`bufferedAmount` cap hit, close `1013`/`4408`); all other clients keep flowing with no latency spike; node memory stays flat.
7. **Graceful drain:** send the node `SIGTERM` under load → clients get `going_away` then close `1001`, reconnect staggered to another node, miss zero messages (resume covers the gap).
8. **Load/soak:** drive target concurrent connections at peak msg/s with a WS/SSE load tool (`k6` `ws`/SSE, `artillery`, `vegeta` for SSE) for ≥30 min → p99 delivery latency within budget; open-conn count, memory, and send-buffer high-water are flat (no leak/creep).

Done = auth-on-connect (no query-string token), heartbeat-driven zombie eviction with flat FD/conn count under churn, sequence-based resume recovers every missed message with no dupes, reconnect uses backoff+jitter, fan-out works across ≥2 nodes via the backplane, slow consumers are dropped without affecting others, and a ≥30-min soak shows no leak.
