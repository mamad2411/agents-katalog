---
name: ws-rpc-heartbeat-event-buffer
description: WebSocket RPC server with per-client heartbeat (ping/pong + missed-count kill) and a ring buffer of recent events per client so a brief disconnect + reconnect can replay pushes instead of dropping them.
category: build
version: 1.0.0
version_origin: extracted
tags: [websocket, rpc, heartbeat, resumption, event-buffer]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/lukilabs/craft-agents-oss.git
source_ref: main
source_commit: 61f7d48a5b4fd0a8094f002c9e3aea5f3824dcfb
source_project: craft-agents-oss
source_path: packages/server-core/src/transport/server.ts
imported_at: 2026-04-18T00:00:00Z
---

# WebSocket RPC heartbeat + event buffer

## When to use
- RPC server using WebSockets and pushing events to subscribed clients.
- Clients run on flaky networks (mobile, VPN, corporate proxy) where 5-30s disconnects are common.
- You don't want to rebuild full state on every reconnect, but also don't want to lose server-pushed events during the gap.

## How it works
1. Each `ClientConnection` tracks: `id`, `ws`, `missedPongs`, `alive`, `eventBuffer[]` (ring), `lastAckedSeq`, `lastSentSeq`.
2. **Heartbeat loop** every `HEARTBEAT_INTERVAL_MS`:
   - If client didn't answer the previous ping, increment `missedPongs`.
   - If `missedPongs >= HEARTBEAT_MAX_MISSED` (e.g. 3), terminate the socket.
   - Otherwise `ws.ping()` (native control frame, not app-level).
   - On `'pong'`, reset `missedPongs` and set `alive = true`.
3. **Event push**: assign monotonic per-client `seq`, serialize the envelope ONCE as a string (`BufferedEvent.data`), push `{ seq, data, timestamp }` into the ring.
4. Ring caps at `EVENT_BUFFER_MAX_SIZE` events or `EVENT_BUFFER_TTL_MS` ms - drop from the head.
5. Client piggybacks `ack: <lastSeen>` on normal invokes. Server trims the ring at `lastAckedSeq`.
6. **Reconnect**: client hello includes `{ clientId, lastSeenSeq }`. If server still has that client in `DISCONNECTED_CLIENT_TTL_MS`, replay every buffered event with `seq > lastSeenSeq` before accepting new work.
7. After TTL, disconnected client state is GC'd and the reconnect is treated as a fresh session.

## Example
```ts
interface ClientConnection {
  id: string; ws: WebSocket;
  missedPongs: number; alive: boolean;
  eventBuffer: { seq: number; data: string; timestamp: number }[];
  lastAckedSeq: number; lastSentSeq: number;
}

setInterval(() => {
  for (const c of clients.values()) {
    if (!c.alive) { c.missedPongs++; if (c.missedPongs >= 3) c.ws.terminate(); continue; }
    c.alive = false; c.ws.ping();
  }
}, HEARTBEAT_INTERVAL_MS);

function pushEvent(client: ClientConnection, envelope: object) {
  const seq = ++client.lastSentSeq;
  const data = JSON.stringify({ ...envelope, seq });
  client.eventBuffer.push({ seq, data, timestamp: Date.now() });
  while (client.eventBuffer.length > EVENT_BUFFER_MAX_SIZE ||
         (client.eventBuffer.length && client.eventBuffer[0].timestamp < Date.now() - EVENT_BUFFER_TTL_MS)) {
    client.eventBuffer.shift();
  }
  if (client.ws.readyState === 1 /* OPEN */) client.ws.send(data);
}
```

## Gotchas
- Serialize once per event, not per client - share the string across all subscribers.
- Use WebSocket's native ping/pong frames, not an app-level `{type:"ping"}` message - native is handled by the OS and survives CPU stalls.
- Clients must ALSO reset their own timeout on receiving server frames, not just on pongs - otherwise idle busy servers look dead.
- `DISCONNECTED_CLIENT_TTL_MS` should be long enough for a phone to come out of suspend (60-120s). Too short = lost events.
- Always bound the ring buffer by BOTH size and TTL. TTL alone can grow unboundedly during bursty pushes.
