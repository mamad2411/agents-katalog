---
name: websocket-essentials
description: Use when designing real-time WebSocket systems — framing, scaling with pub-sub, reconnection with backoff, heartbeats.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: protocol
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [rest-essentials, graphql-essentials, observability-essentials]
---

# WebSocket Essentials

**Iron Law: assume disconnection. Heartbeats, reconnect with backoff, idempotent message handling.**

## When WebSocket beats alternatives

| Need                                   | Pick                                                                   |
| -------------------------------------- | ---------------------------------------------------------------------- |
| Server-pushed events, no client→server | **SSE** (Server-Sent Events) — simpler, auto-reconnect, runs over HTTP |
| Periodic poll, low-frequency           | **HTTP polling** — caches, observable, stateless                       |
| Bidirectional, sub-second, binary      | **WebSocket**                                                          |
| Bidirectional, multiplexed streams     | **WebTransport** (where supported) or HTTP/3                           |
| Mobile with flaky network              | SSE + polling fallback often beats raw WS                              |

WS shines when you genuinely need full-duplex, sub-second, persistent. Otherwise SSE or long-poll is cheaper.

## Framing — text vs binary

| Frame                              | Use                                                       |
| ---------------------------------- | --------------------------------------------------------- |
| **Text (JSON)**                    | chat, presence, control plane, anything humans read       |
| **Binary (CBOR/MsgPack/Protobuf)** | game state, IoT telemetry, audio, anything size-sensitive |

Pick one per channel and stay there — mixing forces clients to sniff every frame. For a binary protocol, version the schema in the first byte or use a length-prefixed envelope:

```
[1B version][4B type][4B length][payload bytes]
```

Define an explicit message envelope even in JSON; raw payloads with no `type` field become unmaintainable fast:

```json
{ "type": "order.updated", "id": "msg_01HZ...", "ts": 1747503600, "data": { ... } }
```

`id` enables dedup on reconnect. `ts` lets clients ignore stale state.

## Heartbeats

The network will lie. A TCP connection can be silently dead for minutes. WS protocol-level ping/pong (RFC 6455) detects this; **application-level heartbeats are still needed** because intermediaries (LBs, mobile NAT) may pass pings while dropping data.

```
client → ping every 25s
server expects ping within 35s; closes if missing
server → pong on every ping
client expects pong within 10s; reconnects if missing
```

Most LBs idle out connections at 60–120s. Heartbeats <30s keep them alive and prove liveness both ways.

## Reconnection — backoff with jitter

```typescript
let delay = 500,
  ws: WebSocket;
const MAX = 30_000;

function open() {
  ws = new WebSocket(url);
  // Cold-connect: no prior session → reset backoff as soon as server greets us.
  // Resume: send the last-seen id and wait for the server's resume.ack before
  // resetting — a fast-closing server otherwise creates a reconnect storm.
  ws.onopen = () => {
    if (lastSeenId) sendResume(lastSeenId);
    else delay = 500;
  };
  ws.addEventListener("message", function firstAck(ev) {
    const m = JSON.parse(ev.data);
    if (m.type === "resume.ack" || m.type === "connected") {
      delay = 500;
      ws.removeEventListener("message", firstAck);
    }
  });
  ws.onclose = reconnect;
}

function reconnect() {
  setTimeout(open, delay + Math.random() * delay); // full jitter
  delay = Math.min(delay * 2, MAX);
}
```

- Exponential backoff: 500ms → 1s → 2s → … → 30s cap.
- **Jitter is mandatory.** Without it, after a server bounce 10k clients reconnect in lockstep and DDoS you.
- Reset backoff AFTER the first server-acknowledged message, not on `onopen` — a server that closes immediately on accept creates a reconnect storm if the timer resets on every open.
- Stop reconnecting on auth-error close codes (4000–4999 are application-defined; convention is `4001` for "unauthorized"). Looping burns battery.

## Resume tokens (don't replay from scratch)

```
client connects with header: Last-Event-Id: msg_01HZ...
server replays missed messages since that ID, then resumes
```

Server keeps a per-session buffer (redis stream, ring buffer) of recent messages. Without resume, every reconnect = full state rehydrate = bad UX + thundering herd.

For idempotent processing, the **client** dedups by message `id`: if a server replays a message the client already applied, the local op is a no-op.

## Scaling

```
              ┌──── WS instance A (sticky) ─── client a, b
LB (sticky) ──┤
              └──── WS instance B (sticky) ─── client c, d
                                ↕
                       Redis/Dragonfly pub-sub
```

| Concern                                  | Pattern                                                             |
| ---------------------------------------- | ------------------------------------------------------------------- |
| Routing reconnects to right instance     | **sticky sessions** (cookie or IP-hash on LB)                       |
| Broadcasting to all of a user's tabs     | pub-sub on `user:{id}` channel                                      |
| Broadcasting to a room                   | pub-sub on `room:{id}` channel                                      |
| Avoiding fan-out to 10k subscribers      | filter at publisher (sender knows room membership)                  |
| Connection count > 1 instance can handle | horizontal — instances stateless except for their owned connections |
| Cross-DC                                 | pub-sub backbone (NATS, Kafka) between regions                      |

**Sticky sessions are non-negotiable for resume.** Without them, a reconnect to instance B has no buffer for the session that was on A.

Dragonfly / Redis pub-sub is good enough up to ~100k connections per cluster. Past that, look at NATS or Kafka with consumer groups.

## Backpressure

If client is slow and server is fast, the per-connection send buffer grows unbounded → OOM.

```typescript
if (ws.bufferedAmount > 1_000_000) {
  // drop low-priority frames OR close the connection
  ws.close(1008, "backpressure");
}
```

Drop, coalesce, or close. Never let the buffer grow to infinity.

## Auth

| Mechanism                                                       | Verdict                                                                                                                                                                                                                                                                         |
| --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Subprotocol header** (`Sec-WebSocket-Protocol: bearer.{jwt}`) | Works in browsers (no custom headers on `new WebSocket()`). Header appears in devtools + some proxy logs — protect via TLS only.                                                                                                                                                |
| Cookie + same-origin + server-side **`Origin` allowlist**       | Standard, easiest. Without the `Origin` check it's CSWSH (cross-site WS hijack): any page can `new WebSocket("wss://your-api")` and the browser sends the cookie. CSRF tokens don't help WS. Defense in depth: also reject `Sec-Fetch-Site: cross-site` on the upgrade request. |
| `?token=...` query                                              | Leaks in access logs, `Referer`, browser history, CDN caches. **Don't.**                                                                                                                                                                                                        |
| First message handshake                                         | Adds a round-trip; needed if URL is fully public.                                                                                                                                                                                                                               |

Always require `wss://` (not `ws://`). Re-validate auth on resume; token may have expired during the gap.

## Anti-patterns

- Assuming the connection is stable — no heartbeat, no reconnect logic
- No jitter on reconnect → thundering herd takes down the server you just brought back
- Infinite reconnect loop on auth failure → battery drain, log flood
- Resume by replaying from `msg_0` every time → quadratic load
- No sticky sessions + expecting resume to work
- Unbounded send buffers → OOM kills the process
- Token in query string → leaks into every proxy log
- One global pub-sub channel → fan-out to all instances even when only one cares
- Mixing text and binary frames on the same channel
- No message ID → client can't dedup replays

## Red flags

| Thought                         | Reality                                                             |
| ------------------------------- | ------------------------------------------------------------------- |
| "Browsers handle reconnect"     | They emit `close`. You build the rest.                              |
| "We don't need sticky sessions" | Then your resume tokens are decorative.                             |
| "10k connections, no problem"   | Each is a file descriptor, a goroutine/task, a TCP buffer. Measure. |
| "We'll add heartbeats later"    | LB silently kills idle connections; users blame the app.            |

## Hand-off

For request/response APIs: `Skill(rest-essentials)`. For GraphQL subscriptions sitting on WS: `Skill(graphql-essentials)`. For correlation IDs and trace propagation through WS messages: `Skill(observability-essentials)`.
