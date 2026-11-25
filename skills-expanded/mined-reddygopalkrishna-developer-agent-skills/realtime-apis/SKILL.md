---
name: realtime-apis
description: Designs and scales realtime features with polling, long polling, Server-Sent Events, WebSockets or webhooks, covering auth at connect time, heartbeats, reconnect and resume, ordering, backpressure, fan-out across instances, and deploys. Use when building live updates, chat, notifications, dashboards, collaborative editing or streaming responses, choosing between SSE and WebSockets, or debugging dropped connections, missed messages or connection limits. Not for request/response API design (use api-design).
license: MIT
---

# Realtime APIs

Connections drop: networks change, proxies time out, servers redeploy. Design so a client can reconnect and catch up without losing or duplicating messages, and so one server can be replaced without a reconnect storm. Choose the simplest transport that meets the latency and direction you actually need.

## When to use

- Live updates (notifications, feeds, dashboards, job progress, order status).
- Chat, presence, multiplayer or collaborative editing.
- Streaming long responses to a browser (including LLM token streams).
- Choosing between polling, SSE, WebSockets and webhooks.
- Debugging dropped connections, missing or duplicated messages, or servers hitting connection limits.

Not for: REST/HTTP API design (see **api-design**); message brokers between backend services (see **event-driven-architecture**).

## Choose the transport

| Need | Use | Why |
| --- | --- | --- |
| Updates every 30 s+ are fine | **Polling** (with `ETag` / `If-None-Match`) | Simplest; works through every proxy and cache |
| Server-to-browser only, near real time | **Server-Sent Events** | Plain HTTP, built-in reconnect and resume |
| Two-way, low latency, frequent client messages | **WebSockets** | Full duplex over one connection |
| Server-to-server notifications | **Webhooks** | No open connection; see api-design for signing and retries |
| Legacy clients or proxies that break streaming | **Long polling** | Fallback only |

Default: SSE for server push to browsers, WebSockets only when the client must send frequent messages over the same channel. Each step up adds operational cost.

## Workflow

1. **Write down the requirements**: direction, latency target, messages per second per client, number of concurrent connections, whether missed messages must be recovered.
2. **Pick the transport** from the table.
3. **Design the message envelope**: every message has a `type`, a unique, increasing `id` per stream, and a timestamp. Version the schema. Read [references/protocol-details.md](references/protocol-details.md) for an envelope, close codes and reconnect code.
4. **Authenticate at connect time and authorize every subscription** (rules below).
5. **Add heartbeats, reconnect with backoff and jitter, and resume from the last message ID.**
6. **Handle backpressure** for slow clients.
7. **Plan scaling and deploys**: fan-out across instances, idle timeouts, connection limits, draining.
8. **Add metrics** (list below) and load-test with the target number of connections before launch.

## Server-Sent Events

- Response: `Content-Type: text/event-stream`, kept open; each event is `id:`, `event:`, `data:` lines followed by a blank line.
- The browser `EventSource` reconnects automatically and sends the last received `id` in the `Last-Event-ID` header. The server must replay events after that ID from a buffer or log.
- The server can set the reconnect delay with a `retry:` field (milliseconds).
- `EventSource` can't set custom headers (only `withCredentials` for cookies). Use cookie auth, or a fetch-based SSE client if you need an `Authorization` header.
- Send a comment line (`: ping`) every 15-30 s so proxies don't close an idle stream.
- Disable response buffering in proxies (for example nginx `proxy_buffering off;` or the `X-Accel-Buffering: no` response header) and in compression middleware, or events arrive in bursts.
- Over HTTP/1.1, browsers limit concurrent connections per origin (commonly 6), and each SSE stream uses one. Serve over HTTP/2 or share one stream across tabs.

## WebSockets

**Auth at the handshake:**

- The browser `WebSocket` API can't set custom headers. Options:
  - **Cookie session**: the cookie is sent with the handshake. You **must** check the `Origin` header against an allowlist, or any site can open an authenticated socket for your users (Cross-Site WebSocket Hijacking).
  - **Short-lived ticket**: the client gets a single-use token from an authenticated HTTP endpoint and passes it in the URL query. Expire it within seconds and keep it out of access logs.
- Re-check authorization for every channel or room the client subscribes to, not only at connect.
- When the session expires or is revoked, close the connection (close code 1008, policy violation).

**Liveness:**

- Servers should send protocol ping frames and close connections that don't answer with a pong.
- Browser JavaScript can't send protocol pings. If the client needs to detect a dead connection, add an application-level heartbeat message.

**Limits:**

- Set a maximum message size and a per-connection message rate; close abusers.
- Validate every inbound message against a schema, just like an HTTP request body.

## Reconnect and resume

- Reconnect with exponential backoff, full jitter and a cap (for example start at 1 s, cap at 30 s). Without jitter, every client reconnects at the same moment after an outage.
- On reconnect, the client sends the last message ID it processed. The server replays newer messages from a bounded buffer (in memory, Redis Streams, or a log), or tells the client to refetch full state if the gap is too old.
- Make client handlers idempotent: drop messages whose ID was already applied.
- Order is only guaranteed within one connection. If order matters across reconnects, rely on message IDs or sequence numbers, not arrival order.

## Backpressure and slow consumers

- Each connection gets a bounded send queue. When it is full, either drop non-essential messages (for example older presence updates), coalesce (send only the latest state), or disconnect the client so it reconnects and resyncs.
- Never let one slow client grow server memory without bound.
- In the browser, `WebSocket.bufferedAmount` shows unsent bytes; stop sending when it keeps growing.

## Scaling connections

| Concern | What to do |
| --- | --- |
| Messages must reach clients on other instances | Fan out through a pub/sub layer (Redis pub/sub or Streams, NATS, Kafka, a cloud pub/sub service). Each instance subscribes to the channels its clients use |
| Sticky sessions | Needed only if a protocol keeps state across HTTP requests (for example long-polling fallbacks). Pure WebSocket and SSE connections stay on one instance anyway |
| Load balancer and proxy idle timeouts | Many default to about 60 s. Send heartbeats more often than the shortest timeout on the path |
| Per-instance limits | Raise file descriptor limits (`ulimit -n`), budget memory per connection, and watch ephemeral port limits on proxies |
| Autoscaling | Scale on connection count and memory, not only CPU |

## Deploys and draining

1. Stop routing new connections to the old instance (mark it not-ready).
2. Tell connected clients to reconnect elsewhere: WebSocket close code 1001 (going away) or 1012 (service restart), or end the SSE stream.
3. Spread the reconnects: clients use jittered backoff, or the server closes connections in batches over the drain window.
4. Make the termination grace period longer than the drain window (see **kubernetes-deployments**).

## Observability

Track per instance and in total:

- Open connections, connects and disconnects per minute, and close codes.
- Reconnect rate (a spike usually means a proxy timeout or a deploy problem).
- Messages sent and received per second; send queue depth; dropped messages.
- Delivery lag: time from event creation to send.
- Auth failures at handshake.

## Anti-patterns

- **WebSockets for one-way updates** that SSE or polling would handle.
- **Checking auth only at connect** and never again for subscriptions or expiry.
- **Cookie-authenticated WebSockets without an Origin check.**
- **No message IDs**, so reconnecting clients silently miss events.
- **Fixed reconnect delay with no jitter**, causing a reconnect storm after each deploy.
- **Unbounded per-connection buffers.**
- **In-memory fan-out only**, which breaks as soon as there are two instances.

## Done when

- The transport choice is written down with its reason.
- Clients survive a server restart and a network drop without losing or duplicating messages (tested by killing an instance during a load test).
- Handshake auth, per-subscription authz and Origin checks are in place.
- Heartbeats are shorter than every idle timeout on the path.
- Fan-out works across at least two instances.
- Connection, reconnect, queue and lag metrics are on a dashboard.

## References

- [references/protocol-details.md](references/protocol-details.md): read when writing the message envelope, close-code handling or client reconnect logic.
