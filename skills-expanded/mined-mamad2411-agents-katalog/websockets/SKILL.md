---
name: "websockets"
description: "- Building real-time bidirectional features (chat, live dashboards, notifications, multiplayer)"
---

# WebSockets and Socket.io

## When to activate
- Building real-time bidirectional features (chat, live dashboards, notifications, multiplayer)
- Setting up Socket.io server with authentication middleware
- Managing rooms and namespaces for channel-based messaging
- Scaling Socket.io horizontally with a Redis adapter
- Implementing client-side reconnection logic
- Transmitting binary data over WebSocket

## When NOT to use
- One-directional streaming from server to client only — use Server-Sent Events (SSE) instead
- Simple request/response patterns where HTTP polling is acceptable and latency is not critical
- When the transport layer is already handled by a managed service (Pusher, Ably, etc.) and you only need the client SDK

## Instructions

### Socket.io Server Setup with Auth Middleware

```typescript
// server/socket.ts
import { Server, Socket } from "socket.io";
import { createServer } from "http";
import { verify } from "jsonwebtoken";

const httpServer = createServer(app);

const io = new Server(httpServer, {
  cors: {
    origin: process.env.CLIENT_URL ?? "http://localhost:3000",
    methods: ["GET", "POST"],
    credentials: true,
  },
  pingTimeout: 20000,
  pingInterval: 25000,
  transports: ["websocket", "polling"],   // websocket first, polling fallback
});

// Authentication middleware — runs before the connection event
io.use(async (socket, next) => {
  try {
    const token =
      socket.handshake.auth.token ??
      socket.handshake.headers.authorization?.replace("Bearer ", "");

    if (!token) return next(new Error("Authentication required"));

    const payload = verify(token, process.env.JWT_SECRET!) as { userId: string; role: string };
    socket.data.userId = payload.userId;
    socket.data.role   = payload.role;
    next();
  } catch {
    next(new Error("Invalid token"));
  }
});

io.on("connection", (socket: Socket) => {
  const { userId, role } = socket.data;
  console.log(`[socket] connected: ${socket.id} user=${userId}`);

  socket.on("disconnect", (reason) => {
    console.log(`[socket] disconnected: ${socket.id} reason=${reason}`);
  });

  registerChatHandlers(io, socket);
  registerPresenceHandlers(io, socket);
});

export { io, httpServer };
```

### Room Management — Join, Leave, Broadcast

Rooms are server-side namespaces. A socket can be in multiple rooms. Rooms do not persist — they are created on first join and destroyed when empty.

```typescript
// handlers/chat.ts
export function registerChatHandlers(io: Server, socket: Socket) {
  // Join a room
  socket.on("chat:join", async (roomId: string) => {
    await socket.join(roomId);

    // Notify others in the room
    socket.to(roomId).emit("chat:user_joined", {
      userId: socket.data.userId,
      roomId,
    });

    // Acknowledge to sender
    socket.emit("chat:joined", { roomId, success: true });
  });

  // Send a message to a room
  socket.on("chat:message", async (payload: { roomId: string; text: string }) => {
    const { roomId, text } = payload;

    // Guard: socket must be in the room
    if (!socket.rooms.has(roomId)) {
      socket.emit("chat:error", { message: "Not in this room" });
      return;
    }

    const message = await saveMessage({ userId: socket.data.userId, roomId, text });

    // Broadcast to all sockets in the room INCLUDING sender
    io.to(roomId).emit("chat:message", message);

    // OR exclude sender:
    // socket.to(roomId).emit("chat:message", message);
  });

  // Leave a room
  socket.on("chat:leave", (roomId: string) => {
    socket.leave(roomId);
    socket.to(roomId).emit("chat:user_left", { userId: socket.data.userId });
  });

  // On disconnect, Socket.io auto-removes from all rooms
  socket.on("disconnecting", () => {
    for (const room of socket.rooms) {
      if (room !== socket.id) {
        socket.to(room).emit("chat:user_left", { userId: socket.data.userId });
      }
    }
  });
}
```

Broadcast targets:

```typescript
io.emit("event", data);                  // all connected sockets
io.to("room-id").emit("event", data);    // all sockets in a room
socket.to("room-id").emit("event", data); // room members excluding sender
socket.broadcast.emit("event", data);    // all sockets except sender
socket.emit("event", data);              // sender only
io.except("room-id").emit("event", data); // all except those in room
```

### Redis Adapter for Horizontal Scaling

Without Redis, events emitted on one server process are not received by sockets connected to another process.

```bash
npm install @socket.io/redis-adapter ioredis
```

```typescript
// server/socket.ts
import { createAdapter } from "@socket.io/redis-adapter";
import { createClient } from "ioredis";

const pubClient = createClient({ host: process.env.REDIS_HOST, port: 6379 });
const subClient = pubClient.duplicate();

await Promise.all([pubClient.connect(), subClient.connect()]);

io.adapter(createAdapter(pubClient, subClient));

// After adding the adapter, io.to("room").emit() works across all server instances
```

With the Redis adapter, Socket.io serializes events through Redis pub/sub. All server instances share room membership. For room state lookups across instances use `io.in("room").fetchSockets()` (async).

Additional considerations:
- Use a sticky session load balancer (e.g., NGINX `ip_hash`, AWS ALB `stickiness`) when `polling` is enabled — polling requires all requests from a client to hit the same server during the handshake phase
- If using WebSocket transport only (`transports: ["websocket"]`), sticky sessions are not required

### Client Reconnection with Exponential Backoff

Socket.io client handles reconnection automatically. Configure it explicitly:

```typescript
// client/socket.ts
import { io, Socket } from "socket.io-client";

let socket: Socket;

export function createSocket(token: string): Socket {
  socket = io(process.env.NEXT_PUBLIC_API_URL!, {
    auth: { token },
    transports: ["websocket"],
    reconnection: true,
    reconnectionAttempts: 10,
    reconnectionDelay: 1000,          // initial delay ms
    reconnectionDelayMax: 30000,      // cap at 30s
    randomizationFactor: 0.5,         // jitter ±50%
    timeout: 10000,
  });

  socket.on("connect", () => {
    console.log("[socket] connected:", socket.id);
    // Re-join rooms after reconnect
    rejoinRooms();
  });

  socket.on("connect_error", (err) => {
    if (err.message === "Invalid token") {
      socket.disconnect();
      redirectToLogin();
    }
    console.error("[socket] connect error:", err.message);
  });

  socket.on("disconnect", (reason) => {
    console.warn("[socket] disconnected:", reason);
    if (reason === "io server disconnect") {
      // Server forcibly disconnected — manual reconnect
      socket.connect();
    }
    // Other reasons: client will auto-reconnect
  });

  return socket;
}
```

Re-join rooms after reconnect since room membership is stored in memory per server process:

```typescript
function rejoinRooms() {
  const rooms = getRoomStateFromLocalStorage();
  rooms.forEach((roomId) => socket.emit("chat:join", roomId));
}
```

### Event Naming Conventions

Consistent event naming prevents conflicts and aids debugging. Use `namespace:action` format:

```
chat:message
chat:join
chat:leave
chat:typing_start
chat:typing_stop
presence:online
presence:offline
notification:new
room:created
room:deleted
error                 # reserved by Socket.io — use sparingly
```

Avoid generic names like `data`, `update`, `event`. Always use lowercase and underscores within the action segment.

Define event types in a shared module:

```typescript
// shared/socket-events.ts
export interface ServerToClientEvents {
  "chat:message": (msg: ChatMessage) => void;
  "chat:user_joined": (info: { userId: string; roomId: string }) => void;
  "presence:online": (userId: string) => void;
  "notification:new": (notif: Notification) => void;
}

export interface ClientToServerEvents {
  "chat:join": (roomId: string, callback: (success: boolean) => void) => void;
  "chat:message": (payload: { roomId: string; text: string }) => void;
  "chat:leave": (roomId: string) => void;
}

// Typed server
const io = new Server<ClientToServerEvents, ServerToClientEvents>(httpServer);

// Typed client
const socket: Socket<ServerToClientEvents, ClientToServerEvents> = io("...");
```

### Binary Data over WebSocket

Socket.io supports sending binary data (Buffer, ArrayBuffer, Blob, TypedArray) natively:

```typescript
// Server — send a file buffer
socket.on("file:request", async (fileId: string) => {
  const buffer: Buffer = await readFile(fileId);
  socket.emit("file:data", { id: fileId, buffer });
});

// Client — receive and use binary
socket.on("file:data", ({ id, buffer }: { id: string; buffer: ArrayBuffer }) => {
  const blob = new Blob([buffer]);
  const url  = URL.createObjectURL(blob);
  downloadLink.href = url;
});

// Client — send binary (e.g., audio chunk)
navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
  const recorder = new MediaRecorder(stream);
  recorder.ondataavailable = (e) => {
    if (e.data.size > 0) socket.emit("audio:chunk", e.data);
  };
  recorder.start(100);  // 100ms chunks
});
```

For large file transfers, chunk the data manually and reassemble on the receiver. Do not send files larger than a few MB as single events — it saturates the event loop.

## Example

A real-time presence and messaging system:

```typescript
// server — presence handler
export function registerPresenceHandlers(io: Server, socket: Socket) {
  socket.on("presence:ping", (roomId: string) => {
    socket.to(roomId).emit("presence:online", socket.data.userId);
  });

  socket.on("disconnecting", () => {
    for (const room of socket.rooms) {
      if (room !== socket.id) {
        io.to(room).emit("presence:offline", socket.data.userId);
      }
    }
  });
}

// client React hook
function useSocket(roomId: string) {
  const [online, setOnline] = useState<string[]>([]);
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  useEffect(() => {
    socket.emit("chat:join", roomId);
    socket.emit("presence:ping", roomId);

    socket.on("chat:message", (msg) => setMessages((prev) => [...prev, msg]));
    socket.on("presence:online",  (id) => setOnline((prev) => [...new Set([...prev, id])]));
    socket.on("presence:offline", (id) => setOnline((prev) => prev.filter((u) => u !== id)));

    return () => {
      socket.emit("chat:leave", roomId);
      socket.off("chat:message");
      socket.off("presence:online");
      socket.off("presence:offline");
    };
  }, [roomId]);

  const send = (text: string) => socket.emit("chat:message", { roomId, text });

  return { online, messages, send };
}
```

---
