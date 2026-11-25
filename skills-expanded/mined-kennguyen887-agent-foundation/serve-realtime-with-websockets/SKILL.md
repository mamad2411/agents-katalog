---
name: serve-realtime-with-websockets
description: Use when pushing realtime updates to connected clients over WebSockets (a socket.io / WS gateway) — authenticating the socket at the handshake (once, not per message), joining sockets to rooms for targeted broadcast, scaling across instances with a Redis pub/sub adapter (+ sticky sessions), bridging domain events to room emits, and connection-lifecycle hygiene (reconnect, listener cleanup). NestJS/socket.io reference, framework-flexible.
metadata:
  author: Ken Nguyễn <ntnpro@gmail.com>
---

# Serve realtime with WebSockets

Pushing live updates to connected clients (call signalling, notifications, presence, live status) over a
**WebSocket gateway**. Examples NestJS + socket.io, neutral domain. principle → **▸ Example** →
**▸ Other stacks**. Unlike the rest of the backend (request/RPC/queue), a WebSocket holds a **long-lived,
stateful connection** — which changes how you auth, target, and scale. Cross-service events that *feed*
the broadcasts are `integrate-internal-services`.

## Core principle
**Authenticate once at the handshake, target with rooms, and scale with a shared pub/sub adapter.** A
connection is long-lived and pinned to one instance, so: verify identity when it opens (not per
message), broadcast to **rooms** (never a blind global emit), and put a **Redis adapter** between
instances or a multi-pod deploy only reaches the clients on one pod. Keep business logic out of the
gateway — it's a transport.

## 1. The gateway + connection lifecycle
A gateway declares the server, lifecycle hooks, and message handlers:
```ts
@WebSocketGateway({ cors: { origin: corsOrigins } })
export class EventsGateway implements OnGatewayInit, OnGatewayConnection, OnGatewayDisconnect {
  @WebSocketServer() server!: Server;

  handleConnection(socket: Socket) {
    if (!socket.handshake.auth.userId) { socket.emit('error', 'unauthenticated'); socket.disconnect(); return; }  // reject unauth
  }
  handleDisconnect(socket: Socket) { socket.removeAllListeners(); }   // cleanup — avoid listener leaks
  @SubscribeMessage('ping') ping(@MessageBody() d: unknown) { this.server.emit('pong', d); }
}
```
Cap listeners (`server.setMaxListeners(n)` from config) — a busy gateway otherwise trips the
max-listeners warning and leaks.

## 2. Authenticate at the handshake (once), attach identity, join rooms
Use **connection middleware** — verify the token from the handshake **once**, attach the resolved
identity to the socket, and join its rooms there. Per-message auth is wasteful and error-prone.
```ts
server.use(async (socket, next) => {
  const token = socket.handshake.auth.token ?? socket.handshake.query.token;
  const claims = token && await this.auth.verify(token);     // delegate to your auth/IdP (integrate-identity-providers)
  if (!claims) return next(new Error('unauthorized'));        // reject the connection
  socket.handshake.auth = { userId: claims.sub, tenantId: claims.orgId, role: claims.role };  // trusted identity
  socket.join(`tenant:${claims.orgId}`);                      // §3 rooms
  socket.join('everyone');
  next();
});
```

## 3. Rooms for targeted broadcast (not blind global emits)
Join each socket to rooms keyed by **tenant / user / entity** (a prefix convention), then emit to the
**room** — so only the right clients get it, and tenants stay isolated.
```ts
// a user can be in several rooms: tenant:<org>, user:<id>, room:<appointmentId>
this.server.to(`tenant:${orgId}`).emit('order.updated', payload);   // just this tenant
this.server.to(`user:${userId}`).emit('notification', payload);     // just this user
```
Reserve `server.emit(...)` (everyone) for true broadcasts; default to a room.

## 4. Scale across instances with a Redis pub/sub adapter (the #1 gotcha)
A socket lives on **one** instance. With >1 instance, `server.to(room).emit()` only reaches clients on
**that** instance unless a **pub/sub adapter** relays emits to the others. Wire a Redis adapter; also
require **sticky sessions** at the LB (the HTTP upgrade + polling fallback must return to the same pod).
```ts
export class SocketAdapter extends IoAdapter {                 // custom adapter
  private ctor!: ReturnType<typeof createAdapter>;
  async connectToRedis() {
    const pub = createClient({ /* host/port/tls from config */ }); const sub = pub.duplicate();
    await Promise.all([pub.connect(), sub.connect()]);
    this.ctor = createAdapter(pub, sub);                       // @socket.io/redis-adapter
  }
  createIOServer(port: number, opts?: ServerOptions) {
    const server = super.createIOServer(port, opts); server.adapter(this.ctor); return server;
  }
}
```
**Without this, realtime "works in dev, drops half the messages in prod"** (one pod locally, many pods deployed).

## 5. Bridge domain events → room emits (gateway is a transport, not a brain)
The gateway shouldn't contain business logic. A use-case emits a domain event; an event handler (or the
service) calls the gateway to **broadcast to the relevant room**. Same events that drive the rest of the
system drive realtime.
```ts
@EventsHandler(OrderStatusChangedEvent)
class PushOrderStatus { handle(e) { this.gateway.toRoom(`tenant:${e.orgId}`, 'order.updated', map(e)); } }
```
(Inbound cross-service triggers arrive via SQS/RPC — `integrate-internal-services` — then fan out to sockets.)

## 6. Reconnection & client contract
Clients drop and reconnect constantly (network, sleep). On reconnect the client **re-sends its token and
re-joins** (your middleware re-runs, so rooms are restored). Emit **typed, mapped payloads** (a subset,
like outbound events in `write-service-code` §6), version event names, and don't assume delivery —
critical state must also be fetchable via a normal request.
▸ *Other stacks:* `ws`/Socket.IO (Node), **Phoenix Channels** (Elixir), **ActionCable** (Rails),
**SignalR** (.NET), Centrifugo. The three invariants are universal: **auth at connect, rooms/channels
for targeting, a shared backplane (Redis/NATS) + sticky sessions to scale**.

## Verification
- **Auth at handshake, not per-message:** open a socket with **no** `auth.token` → server emits `error` and disconnects (client `connected === false`); a valid token stays connected. `grep -rn "verify\|introspect" src --include='*gateway*'` finds the check in a `server.use(...)` middleware, **not** inside any `@SubscribeMessage` handler.
- **Rooms, not global:** `grep -rn "server\.emit(" src` returns only deliberate broadcasts (≈0); targeted sends go through `.to(room).emit(...)`. Connected as tenant B, emit to tenant A's room → B receives nothing.
- **Cross-instance backplane:** run **2** instances, one client on each, join both to a room, emit once → **both** receive it. `redis-cli PUBSUB CHANNELS "*socket.io*"` is non-empty while clients are connected; the LB/ingress has session affinity (sticky) on.
- **Transport-only gateway:** `grep -rn "Repository\|DataSource" src --include='*gateway*'` → empty (no DB in the gateway); emits originate from `@EventsHandler` classes.
- **Lifecycle hygiene:** `grep -n "removeAllListeners\|setMaxListeners" src` hits `handleDisconnect` + bootstrap; drop a client's network then restore → it reconnects, the middleware re-runs, and a re-emit to its room reaches it.

## Related
- `integrate-internal-services` — the SQS/RPC events that feed the broadcasts (use-case → event → gateway emit).
- `integrate-identity-providers` — verifying the handshake token; `write-service-code` §6 (mapped-subset payloads), §7 (logging).
- `background-jobs-and-caching` — the Redis you already run also backs the socket adapter · `containerize-and-ship-a-service` (sticky-session ingress).
