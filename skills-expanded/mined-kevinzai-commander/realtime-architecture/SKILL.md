---
name: realtime-architecture
description: "Real-time application architecture — WebSocket, SSE, pub/sub, presence, and collaborative editing patterns"
version: 1.0.0
category: architecture
---

# Real-Time Architecture

Patterns for building real-time features: live updates, presence, collaboration, and streaming.

## Technology Selection

| Use Case | Technology | When To Use |
|----------|-----------|-------------|
| Bidirectional messaging | WebSocket | Chat, gaming, collaborative editing |
| Server push (one-way) | Server-Sent Events (SSE) | Notifications, live feeds, dashboards |
| Scalable pub/sub | Redis Pub/Sub | Multi-server broadcasting |
| Database-driven realtime | Supabase Realtime / Firebase | CRUD-triggered updates |
| Request-response streaming | HTTP Streaming | AI responses, large data transfers |

## Patterns

### 1. WebSocket Server (Hono + Bun)

```typescript
import { Hono } from 'hono';
import { createBunWebSocket } from 'hono/bun';

const { upgradeWebSocket, websocket } = createBunWebSocket();
const app = new Hono();

const rooms = new Map<string, Set<WebSocket>>();

app.get('/ws/:room', upgradeWebSocket((c) => ({
  onOpen(event, ws) {
    const room = c.req.param('room');
    if (!rooms.has(room)) rooms.set(room, new Set());
    rooms.get(room)!.add(ws.raw!);
  },
  onMessage(event, ws) {
    const room = c.req.param('room');
    const peers = rooms.get(room);
    if (!peers) return;
    // Broadcast to all peers except sender
    for (const peer of peers) {
      if (peer !== ws.raw && peer.readyState === 1) {
        peer.send(String(event.data));
      }
    }
  },
  onClose(event, ws) {
    for (const [, peers] of rooms) {
      peers.delete(ws.raw!);
    }
  },
})));

export default { port: 3001, fetch: app.fetch, websocket };
```

### 2. Server-Sent Events (Next.js Route Handler)

```typescript
// app/api/events/route.ts
export async function GET() {
  const encoder = new TextEncoder();
  const stream = new ReadableStream({
    start(controller) {
      const send = (data: unknown) => {
        controller.enqueue(
          encoder.encode(`data: ${JSON.stringify(data)}\n\n`)
        );
      };

      // Subscribe to events
      const unsubscribe = eventBus.subscribe('updates', send);

      // Heartbeat every 30s to keep connection alive
      const heartbeat = setInterval(() => {
        controller.enqueue(encoder.encode(': heartbeat\n\n'));
      }, 30_000);

      // Cleanup
      return () => {
        unsubscribe();
        clearInterval(heartbeat);
      };
    },
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      Connection: 'keep-alive',
    },
  });
}
```

### 3. Presence System

```typescript
interface UserPresence {
  userId: string;
  status: 'online' | 'away' | 'offline';
  lastSeen: number;
  cursor?: { x: number; y: number };
}

class PresenceManager {
  private presence = new Map<string, UserPresence>();
  private readonly TIMEOUT_MS = 30_000;

  join(userId: string) {
    this.presence.set(userId, {
      userId, status: 'online', lastSeen: Date.now(),
    });
    this.broadcast({ type: 'presence:join', userId });
  }

  heartbeat(userId: string, cursor?: { x: number; y: number }) {
    const user = this.presence.get(userId);
    if (user) {
      user.lastSeen = Date.now();
      user.status = 'online';
      user.cursor = cursor;
    }
  }

  getOnlineUsers(): UserPresence[] {
    const now = Date.now();
    for (const [id, user] of this.presence) {
      if (now - user.lastSeen > this.TIMEOUT_MS) {
        user.status = 'offline';
        this.presence.delete(id);
        this.broadcast({ type: 'presence:leave', userId: id });
      }
    }
    return [...this.presence.values()];
  }
}
```

### 4. Connection Management (Client)

```typescript
function createReconnectingWebSocket(url: string) {
  let ws: WebSocket;
  let retries = 0;
  const maxRetries = 10;
  const listeners = new Set<(data: unknown) => void>();

  function connect() {
    ws = new WebSocket(url);

    ws.onopen = () => {
      retries = 0; // Reset on successful connection
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      for (const listener of listeners) listener(data);
    };

    ws.onclose = () => {
      if (retries < maxRetries) {
        const delay = Math.min(1000 * Math.pow(2, retries), 30_000);
        retries++;
        setTimeout(connect, delay);
      }
    };
  }

  connect();

  return {
    send: (data: unknown) => ws.send(JSON.stringify(data)),
    subscribe: (fn: (data: unknown) => void) => {
      listeners.add(fn);
      return () => listeners.delete(fn);
    },
    close: () => ws.close(),
  };
}
```

### 5. Redis Pub/Sub (Multi-Server)

```typescript
import { createClient } from 'redis';

const publisher = createClient({ url: process.env.REDIS_URL });
const subscriber = publisher.duplicate();

await Promise.all([publisher.connect(), subscriber.connect()]);

// Publish from any server
async function broadcastToChannel(channel: string, message: unknown) {
  await publisher.publish(channel, JSON.stringify(message));
}

// Subscribe on each server, forward to local WebSocket clients
await subscriber.subscribe('chat:*', (message, channel) => {
  const roomId = channel.split(':')[1];
  const localClients = rooms.get(roomId);
  if (localClients) {
    for (const client of localClients) {
      client.send(message);
    }
  }
});
```

## Architecture Decision Guide

1. **Single server, <1000 connections** → WebSocket directly (no Redis needed)
2. **Multiple servers** → WebSocket + Redis Pub/Sub for cross-server messaging
3. **Server-to-client only** → SSE (simpler than WebSocket)
4. **Database-driven updates** → Supabase Realtime or Postgres LISTEN/NOTIFY
5. **AI streaming responses** → SSE or HTTP streaming
6. **Collaborative editing** → WebSocket + CRDT library (Yjs, Automerge)

## Checklist

- [ ] Connection protocol selected (WebSocket / SSE / both)
- [ ] Reconnection with exponential backoff implemented
- [ ] Heartbeat mechanism for stale connection detection
- [ ] Room/channel management for scoped broadcasting
- [ ] Presence system if showing online users
- [ ] Redis Pub/Sub if multi-server deployment
- [ ] Rate limiting on incoming WebSocket messages
- [ ] Authentication on connection upgrade (verify JWT/session)
- [ ] Graceful shutdown (drain connections before restart)
