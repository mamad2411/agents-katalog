---
name: websocket-design
description: Design WebSocket architecture for real-time communication. Outputs connection management, message protocols, scaling, and fallback strategies.
argument-hint: [use case, concurrency, message frequency]
allowed-tools: Read, Write, Bash
---

# WebSocket Architecture

Design production WebSocket system for real-time bidirectional communication. Not basic Socket.IO — connection lifecycle, message protocols, horizontal scaling, reconnection, and HTTP fallback.

## Process

1. **Define use cases.** Chat, live updates, collaborative editing, gaming.
2. **Choose protocol.** Native WebSocket, Socket.IO (easier), GraphQL subscriptions.
3. **Design messages.** JSON protocol with types, authentication, routing.
4. **Handle connections.** Lifecycle (connect, disconnect, ping/pong), authentication.
5. **Scale horizontally.** Redis pub/sub for multi-server, sticky sessions.
6. **Add reliability.** Reconnection, message queuing, delivery guarantees.
7. **Monitor.** Active connections, message rate, latency.

## Output Format

### WebSocket System: [Application Name]

**Use Case:** Real-time chat + notifications  
**Protocol:** Socket.IO  
**Peak Connections:** 100k concurrent  
**Scaling:** Redis adapter (multi-server)  
**Fallback:** Long polling (legacy browsers)

---

## Protocol Comparison

| Feature | Native WebSocket | Socket.IO | GraphQL Subscriptions |
|---------|------------------|-----------|----------------------|
| Browser support | Modern only | All browsers | Modern only |
| Reconnection | Manual | Automatic | Automatic |
| Fallback | None | Long polling | Server-sent events |
| Rooms/namespaces | Manual | Built-in | Topic-based |
| Complexity | Low | Medium | High |

**Recommendation:** Socket.IO for reliability, native WebSocket for simplicity

---

## Basic WebSocket (Node.js)

```javascript
import { WebSocketServer } from 'ws';

const wss = new WebSocketServer({ port: 8080 });

// Connection tracking
const clients = new Map();

wss.on('connection', (ws, req) => {
  const clientId = generateId();
  clients.set(clientId, { ws, userId: null });
  
  console.log(`Client connected: ${clientId}`);
  
  // Handle messages
  ws.on('message', (data) => {
    try {
      const message = JSON.parse(data);
      handleMessage(clientId, message);
    } catch (err) {
      ws.send(JSON.stringify({ error: 'Invalid JSON' }));
    }
  });
  
  // Handle disconnect
  ws.on('close', () => {
    console.log(`Client disconnected: ${clientId}`);
    clients.delete(clientId);
  });
  
  // Keep-alive ping
  const interval = setInterval(() => {
    if (ws.readyState === ws.OPEN) {
      ws.ping();
    }
  }, 30000);
  
  ws.on('close', () => clearInterval(interval));
});

function handleMessage(clientId, message) {
  const client = clients.get(clientId);
  
  switch (message.type) {
    case 'auth':
      // Authenticate user
      const user = verifyToken(message.token);
      if (user) {
        client.userId = user.id;
        client.ws.send(JSON.stringify({
          type: 'auth_success',
          user: { id: user.id, name: user.name }
        }));
      }
      break;
      
    case 'message':
      // Broadcast to all clients
      broadcast(message.content, clientId);
      break;
  }
}

function broadcast(message, senderId) {
  const packet = JSON.stringify({
    type: 'message',
    content: message,
    senderId,
    timestamp: Date.now()
  });
  
  for (const [id, client] of clients) {
    if (client.ws.readyState === client.ws.OPEN) {
      client.ws.send(packet);
    }
  }
}
```

---

## Socket.IO (Production-Ready)

```javascript
import { Server } from 'socket.io';
import { createAdapter } from '@socket.io/redis-adapter';
import { createClient } from 'redis';

const io = new Server(3000, {
  cors: { origin: '*' }
});

// Redis adapter for multi-server scaling
const pubClient = createClient({ url: 'redis://localhost:6379' });
const subClient = pubClient.duplicate();

Promise.all([pubClient.connect(), subClient.connect()]).then(() => {
  io.adapter(createAdapter(pubClient, subClient));
});

// Authentication middleware
io.use((socket, next) => {
  const token = socket.handshake.auth.token;
  try {
    const user = verifyJWT(token);
    socket.userId = user.id;
    socket.username = user.name;
    next();
  } catch (err) {
    next(new Error('Authentication failed'));
  }
});

// Connection handler
io.on('connection', (socket) => {
  console.log(`User connected: ${socket.userId}`);
  
  // Join user-specific room
  socket.join(`user:${socket.userId}`);
  
  // Handle chat messages
  socket.on('chat:send', async (data) => {
    const message = {
      id: generateId(),
      content: data.content,
      userId: socket.userId,
      username: socket.username,
      timestamp: Date.now()
    };
    
    // Save to DB
    await db.message.create({ data: message });
    
    // Broadcast to room
    io.to(data.roomId).emit('chat:message', message);
  });
  
  // Join/leave rooms
  socket.on('room:join', (roomId) => {
    socket.join(roomId);
    socket.emit('room:joined', { roomId });
  });
  
  socket.on('room:leave', (roomId) => {
    socket.leave(roomId);
  });
  
  // Typing indicator
  socket.on('typing:start', (roomId) => {
    socket.to(roomId).emit('typing:user', {
      userId: socket.userId,
      username: socket.username
    });
  });
  
  // Disconnect handler
  socket.on('disconnect', (reason) => {
    console.log(`User disconnected: ${socket.userId}, reason: ${reason}`);
  });
});

// Server-to-client events
setInterval(() => {
  // Send live stats to all clients
  io.emit('stats:update', {
    activeUsers: io.sockets.sockets.size,
    timestamp: Date.now()
  });
}, 10000);
```

---

## Message Protocol

```typescript
// Client → Server
interface ClientMessage {
  type: 'auth' | 'subscribe' | 'unsubscribe' | 'message' | 'ping';
  payload: any;
  id?: string;  // For request/response correlation
}

// Server → Client
interface ServerMessage {
  type: 'auth_success' | 'auth_error' | 'message' | 'error' | 'pong';
  payload: any;
  id?: string;  // Correlates with request
}

// Example messages
const authMessage: ClientMessage = {
  type: 'auth',
  payload: { token: 'jwt_token_here' }
};

const subscribeMessage: ClientMessage = {
  type: 'subscribe',
  payload: { channel: 'room:123' }
};

const chatMessage: ClientMessage = {
  type: 'message',
  payload: {
    channel: 'room:123',
    content: 'Hello world'
  }
};

// Server responses
const authSuccess: ServerMessage = {
  type: 'auth_success',
  payload: { userId: '456', username: 'alice' }
};

const incomingMessage: ServerMessage = {
  type: 'message',
  payload: {
    channel: 'room:123',
    content: 'Hello world',
    userId: '456',
    timestamp: 1640000000
  }
};
```

---

## Client Implementation

```javascript
// React hook
import { useEffect, useState } from 'react';
import { io } from 'socket.io-client';

function useChatSocket(roomId, token) {
  const [socket, setSocket] = useState(null);
  const [messages, setMessages] = useState([]);
  const [connected, setConnected] = useState(false);
  
  useEffect(() => {
    // Connect with auth
    const newSocket = io('https://api.example.com', {
      auth: { token },
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: 5
    });
    
    // Connection events
    newSocket.on('connect', () => {
      console.log('Connected');
      setConnected(true);
      newSocket.emit('room:join', roomId);
    });
    
    newSocket.on('disconnect', (reason) => {
      console.log('Disconnected:', reason);
      setConnected(false);
    });
    
    newSocket.on('connect_error', (err) => {
      console.error('Connection error:', err);
    });
    
    // Message events
    newSocket.on('chat:message', (message) => {
      setMessages(prev => [...prev, message]);
    });
    
    setSocket(newSocket);
    
    return () => {
      newSocket.close();
    };
  }, [roomId, token]);
  
  const sendMessage = (content) => {
    if (socket?.connected) {
      socket.emit('chat:send', { content, roomId });
    }
  };
  
  return { messages, sendMessage, connected };
}

// Usage
function ChatRoom({ roomId, token }) {
  const { messages, sendMessage, connected } = useChatSocket(roomId, token);
  
  return (
    <div>
      <div>Status: {connected ? 'Connected' : 'Disconnected'}</div>
      <div>
        {messages.map(msg => (
          <div key={msg.id}>{msg.username}: {msg.content}</div>
        ))}
      </div>
      <input onKeyPress={e => {
        if (e.key === 'Enter') {
          sendMessage(e.target.value);
          e.target.value = '';
        }
      }} />
    </div>
  );
}
```

---

## Horizontal Scaling (Redis Adapter)

**Problem:** With multiple servers, Socket.IO clients on different servers can't communicate.

**Solution:** Redis pub/sub to sync messages across servers.

```javascript
// Server 1
io.on('connection', (socket) => {
  socket.on('message', (data) => {
    io.to('room1').emit('message', data);  // Broadcasts via Redis
  });
});

// Server 2 (different process)
// Client receives message even though connected to different server
```

**Redis channels:**
```
socket.io#room1#/  → Messages to room1
socket.io#user:123#/ → Messages to specific user
```

---

## Reconnection Strategy

```javascript
// Client
const socket = io({
  reconnection: true,
  reconnectionAttempts: 5,
  reconnectionDelay: 1000,
  reconnectionDelayMax: 5000,
  timeout: 20000
});

socket.on('connect', () => {
  console.log('Connected');
  
  // Resubscribe to rooms
  socket.emit('room:join', 'room1');
  
  // Request missed messages
  socket.emit('sync:messages', { since: lastMessageTimestamp });
});

socket.on('disconnect', (reason) => {
  if (reason === 'io server disconnect') {
    // Server kicked us, reconnect manually
    socket.connect();
  }
  // Otherwise auto-reconnect happens
});
```

---

## Monitoring

```javascript
import { Counter, Gauge, Histogram } from 'prom-client';

const connectionsGauge = new Gauge({
  name: 'websocket_connections_active',
  help: 'Active WebSocket connections'
});

const messagesCounter = new Counter({
  name: 'websocket_messages_total',
  help: 'Total messages sent',
  labelNames: ['type']
});

const latencyHistogram = new Histogram({
  name: 'websocket_message_latency_seconds',
  help: 'Message latency'
});

io.on('connection', (socket) => {
  connectionsGauge.inc();
  
  socket.on('disconnect', () => {
    connectionsGauge.dec();
  });
  
  socket.on('message', (data) => {
    const start = Date.now();
    messagesCounter.inc({ type: data.type });
    
    // ... handle message ...
    
    latencyHistogram.observe((Date.now() - start) / 1000);
  });
});
```

**Metrics to track:**
- Active connections
- Messages/second
- Message latency (p50, p95, p99)
- Reconnection rate
- Error rate

---

## Security

### Authentication
```javascript
io.use((socket, next) => {
  const token = socket.handshake.auth.token;
  if (!token) {
    return next(new Error('No token'));
  }
  
  jwt.verify(token, SECRET, (err, user) => {
    if (err) return next(new Error('Invalid token'));
    socket.userId = user.id;
    next();
  });
});
```

### Rate Limiting
```javascript
const rateLimits = new Map();

io.on('connection', (socket) => {
  socket.on('message', (data) => {
    const key = socket.userId;
    const now = Date.now();
    const limit = rateLimits.get(key) || { count: 0, resetAt: now + 60000 };
    
    if (now > limit.resetAt) {
      limit.count = 0;
      limit.resetAt = now + 60000;
    }
    
    limit.count++;
    rateLimits.set(key, limit);
    
    if (limit.count > 100) {  // 100 messages per minute
      socket.emit('error', { message: 'Rate limit exceeded' });
      return;
    }
    
    // Process message
  });
});
```

### Input Validation
```javascript
socket.on('message', (data) => {
  if (!data.content || typeof data.content !== 'string') {
    return socket.emit('error', { message: 'Invalid message' });
  }
  
  if (data.content.length > 1000) {
    return socket.emit('error', { message: 'Message too long' });
  }
  
  // Sanitize HTML
  const clean = sanitizeHtml(data.content);
  
  // Process
});
```

## Rules

- Authentication required on connection — verify JWT before allowing communication.
- Redis adapter mandatory for multi-server deployments — enables cross-server messaging.
- Reconnection with exponential backoff — prevents thundering herd on server restart.
- Rate limiting per user/connection — prevents spam and abuse.
- Message size limits (1-10KB) — prevents memory exhaustion.
- Heartbeat/ping-pong every 30s — detects dead connections.
- Room-based broadcasting, not individual sends — scales to thousands of connections.
- Graceful shutdown: disconnect clients with warning — prevents abrupt connection loss.
- Message queuing during reconnect — prevent message loss.
- Monitor active connections, message rate, latency — alert on anomalies.
