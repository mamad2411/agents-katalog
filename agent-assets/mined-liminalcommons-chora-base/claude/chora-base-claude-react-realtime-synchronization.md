# SAP-037: Real-Time Data Synchronization - Claude Agent Guide

**SAP ID**: SAP-037
**Version**: 1.0.0
**Status**: pilot
**For**: Claude Code, Claude Desktop, Claude API
**Last Updated**: 2025-11-09

---

## 📖 Quick Reference

**New to SAP-037?** → Read **[README.md](README.md)** first (10-min read)

The README provides:
- 🚀 **Quick Start** - 40-minute setup with 4 real-time providers (Socket.IO, SSE, Pusher, Ably)
- 📚 **Time Savings** - 80% WebSocket setup time reduction (40 min vs 5-7 hours manual), 90.5% savings with production-ready patterns
- 🎯 **Provider Decision Matrix** - Cost, performance, scalability comparison for choosing the right solution
- 🔧 **TanStack Query Integration** - Real-time invalidation, optimistic updates, offline handling
- 📊 **Conflict Resolution** - LWW, OT, CRDTs patterns for handling concurrent updates
- 🔗 **Integration** - Works with SAP-020 (Foundation), SAP-023 (State), SAP-034 (Database)

This CLAUDE.md provides: Claude Code-specific workflows for real-time synchronization implementation.

---

## Quick Reference for Claude

### What This SAP Provides

SAP-037 enables **real-time data synchronization** in React applications with four battle-tested providers:

1. **Socket.IO** - Bidirectional, self-hosted, 60k GitHub stars
2. **SSE** - Native EventSource API, unidirectional, simple
3. **Pusher** - Managed service, 100 connections free, 6ms latency
4. **Ably** - Enterprise-grade, 6M messages/month free, 99.999% SLA

**Time savings**: 90.5% (5-7h → 40min)

---

### When to Use This SAP

**Use SAP-037 when user requests**:
- "Add real-time updates to my app"
- "Implement live notifications"
- "Build a chat feature"
- "Add collaborative editing (Google Docs style)"
- "Show online users / presence tracking"
- "Implement WebSocket / Server-Sent Events"

**Don't use SAP-037 when**:
- User wants polling (use setInterval instead)
- User wants long polling (deprecated, recommend WebSockets)
- User wants HTTP/2 Server Push (deprecated, recommend SSE)

---

## Progressive Context Loading Strategy

Claude should load context progressively to optimize token usage:

### Phase 1: Orientation (0-10k tokens)

**Goal**: Understand requirements and recommend provider

**Read**:
1. This file (CLAUDE.md) for overview
2. AGENTS.md for provider decision tree

**Ask user**:
- "Do you need bidirectional communication (client ↔ server) or just server → client?"
- "Do you prefer self-hosted or managed service?"
- "What's your expected scale (concurrent users)?"

**Output**: Provider recommendation based on decision tree

**Time**: 2-3 minutes

---

### Phase 2: Implementation (10-50k tokens)

**Goal**: Setup chosen provider and integrate with app

**Read**:
1. `adoption-blueprint.md` - Step-by-step setup for chosen provider
2. `protocol-spec.md` (relevant sections) - Code examples and API reference

**Generate**:
- Provider setup code (Socket.IO context, SSE hook, etc.)
- TanStack Query integration
- Reconnection logic
- Basic testing instructions

**Time**: 15-20 minutes

---

### Phase 3: Advanced Patterns (50-100k tokens)

**Goal**: Implement presence tracking, offline queue, conflict resolution

**Read**:
1. `protocol-spec.md` (How-To Guides section) - Advanced patterns
2. `AGENTS.md` (Integration section) - Cross-SAP patterns

**Generate**:
- Presence tracking hook
- Offline queue with localStorage
- Conflict resolution (LWW, OT, or CRDTs)
- Integration with SAP-023 (State), SAP-034 (Database), SAP-036 (Error Handling)

**Time**: 30-60 minutes (depending on complexity)

---

## Provider Decision Framework for Claude

### Decision Tree Prompt

When user requests real-time features, use this prompt:

```
I'll help you add real-time synchronization. First, let me ask a few questions:

1. **Communication pattern**: Do you need bidirectional (client ↔ server, like chat)
   or unidirectional (server → client, like notifications)?

2. **Hosting preference**: Would you prefer to self-host (more control, lower cost at scale)
   or use a managed service (easier setup, auto-scaling)?

3. **Scale**: How many concurrent users do you expect? (<100, 100-1k, 1k-10k, >10k)

Based on your answers, I'll recommend the best provider:
- **SSE**: Unidirectional, simple, native browser API
- **Socket.IO**: Bidirectional, self-hosted, full control
- **Pusher**: Bidirectional, managed, 100 free connections
- **Ably**: Bidirectional, managed, enterprise-grade
```

---

### Recommendation Matrix

| User Requirements | Recommended Provider | Rationale |
|-------------------|---------------------|-----------|
| Unidirectional + any scale | **SSE** | Simplest, native API, no library needed |
| Bidirectional + self-host + <10k users | **Socket.IO** | Full control, cheaper at scale |
| Bidirectional + managed + tight budget | **Pusher** | 100 free connections, easy setup |
| Bidirectional + managed + enterprise | **Ably** | 99.999% SLA, global edge |

---

## Code Generation Patterns for Claude

### Pattern 1: Socket.IO Setup

**User request**: "Setup Socket.IO for real-time updates"

**Claude generates**:

1. **Install dependencies**:
```bash
npm install socket.io-client
```

2. **Create Socket context** (`lib/socket.tsx`):
```typescript
'use client';

import { createContext, useContext, useEffect, useState } from 'react';
import { io, Socket } from 'socket.io-client';

const SocketContext = createContext<Socket | null>(null);

export function SocketProvider({ children }: { children: React.ReactNode }) {
  const [socket, setSocket] = useState<Socket | null>(null);

  useEffect(() => {
    const socketInstance = io(process.env.NEXT_PUBLIC_SOCKET_URL || 'http://localhost:3000', {
      autoConnect: true,
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionAttempts: 5,
    });

    socketInstance.on('connect', () => {
      console.log('Socket.IO connected:', socketInstance.id);
    });

    setSocket(socketInstance);

    return () => {
      socketInstance.disconnect();
    };
  }, []);

  return (
    <SocketContext.Provider value={socket}>
      {children}
    </SocketContext.Provider>
  );
}

export function useSocket() {
  const socket = useContext(SocketContext);
  if (!socket) throw new Error('useSocket must be used within SocketProvider');
  return socket;
}
```

3. **Wrap app** (`app/layout.tsx`):
```typescript
import { SocketProvider } from '@/lib/socket';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <SocketProvider>
          {children}
        </SocketProvider>
      </body>
    </html>
  );
}
```

4. **Use in component**:
```typescript
'use client';

import { useEffect } from 'react';
import { useSocket } from '@/lib/socket';
import { useQueryClient } from '@tanstack/react-query';

export default function TodoList() {
  const socket = useSocket();
  const queryClient = useQueryClient();

  useEffect(() => {
    socket.on('todo:created', () => {
      queryClient.invalidateQueries(['todos']);
    });

    return () => {
      socket.off('todo:created');
    };
  }, [socket, queryClient]);

  return <div>...</div>;
}
```

**Explain to user**:
- "I've set up Socket.IO with auto-reconnection and TanStack Query integration"
- "Open two browser windows to test real-time sync"
- "Next steps: Set up server-side Socket.IO (see protocol-spec.md for examples)"

---

### Pattern 2: SSE Setup

**User request**: "Add live notifications using Server-Sent Events"

**Claude generates**:

1. **Create SSE hook** (`lib/useSSE.ts`):
```typescript
import { useEffect, useState } from 'react';

export function useSSE<T>(url: string, eventName: string) {
  const [data, setData] = useState<T | null>(null);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const eventSource = new EventSource(url);

    eventSource.onopen = () => setIsConnected(true);

    eventSource.addEventListener(eventName, (event) => {
      setData(JSON.parse(event.data));
    });

    eventSource.onerror = () => {
      setIsConnected(false);
      eventSource.close();
    };

    return () => eventSource.close();
  }, [url, eventName]);

  return { data, isConnected };
}
```

2. **Create API route** (`app/api/notifications/route.ts`):
```typescript
export async function GET(req: Request) {
  const encoder = new TextEncoder();

  const stream = new ReadableStream({
    start(controller) {
      controller.enqueue(
        encoder.encode(`event: connected\ndata: {}\n\n`)
      );

      const interval = setInterval(() => {
        const notification = { id: Date.now(), message: 'New notification' };
        controller.enqueue(
          encoder.encode(`event: notification\ndata: ${JSON.stringify(notification)}\n\n`)
        );
      }, 5000);

      req.signal.addEventListener('abort', () => {
        clearInterval(interval);
        controller.close();
      });
    },
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    },
  });
}
```

3. **Use in component**:
```typescript
'use client';

import { useEffect } from 'react';
import { useSSE } from '@/lib/useSSE';
import { useQueryClient } from '@tanstack/react-query';

export default function Notifications() {
  const queryClient = useQueryClient();
  const { data: newNotification, isConnected } = useSSE('/api/notifications', 'notification');

  useEffect(() => {
    if (newNotification) {
      queryClient.invalidateQueries(['notifications']);
    }
  }, [newNotification, queryClient]);

  return (
    <div>
      <div>Status: {isConnected ? 'Connected' : 'Disconnected'}</div>
      {/* Notification list */}
    </div>
  );
}
```

**Explain to user**:
- "I've set up Server-Sent Events using the native EventSource API (no library needed)"
- "This is perfect for one-way notifications (server → client)"
- "For bidirectional chat, use Socket.IO or Pusher instead"

---

### Pattern 3: TanStack Query Real-Time Invalidation

**User request**: "Invalidate TanStack Query cache on real-time events"

**Claude generates**:

```typescript
import { useEffect } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { useSocket } from './useSocket';

export function useRealtimeInvalidation(
  queryKey: string[],
  events: string[]
) {
  const queryClient = useQueryClient();
  const socket = useSocket();

  useEffect(() => {
    const handler = () => {
      queryClient.invalidateQueries(queryKey);
    };

    events.forEach(event => {
      socket.on(event, handler);
    });

    return () => {
      events.forEach(event => {
        socket.off(event, handler);
      });
    };
  }, [socket, queryClient, queryKey, events]);
}

// Usage
function TodoList() {
  const { data: todos } = useQuery(['todos'], fetchTodos);

  useRealtimeInvalidation(['todos'], [
    'todo:created',
    'todo:updated',
    'todo:deleted',
  ]);

  return <div>{todos.map(renderTodo)}</div>;
}
```

**Explain to user**:
- "This hook automatically invalidates TanStack Query cache when real-time events arrive"
- "No manual cache updates needed—Query will refetch automatically"
- "For optimistic updates, see protocol-spec.md How-To section"

---

### Pattern 4: Optimistic Updates with Real-Time Sync

**User request**: "Add optimistic updates that sync with real-time events"

**Claude generates**:

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';

export function useOptimisticTodo() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (newTodo: { text: string }) => {
      return fetch('/api/todos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newTodo),
      }).then(res => res.json());
    },
    onMutate: async (newTodo) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries(['todos']);

      // Snapshot previous value
      const previousTodos = queryClient.getQueryData(['todos']);

      // Optimistically update (instant UI)
      queryClient.setQueryData(['todos'], (old: any[]) => [
        ...old,
        { id: 'temp-' + Date.now(), text: newTodo.text, completed: false },
      ]);

      return { previousTodos };
    },
    onError: (err, newTodo, context) => {
      // Rollback on error
      queryClient.setQueryData(['todos'], context?.previousTodos);
    },
    onSettled: () => {
      // Refetch to ensure server state
      queryClient.invalidateQueries(['todos']);
    },
  });
}

// Usage
function TodoList() {
  const createTodo = useOptimisticTodo();

  return (
    <button onClick={() => createTodo.mutate({ text: 'New todo' })}>
      Add Todo (Instant UI)
    </button>
  );
}
```

**Explain to user**:
- "Optimistic updates make UI feel instant (no waiting for server)"
- "Real-time events reconcile state across all clients"
- "Errors are handled gracefully (rollback optimistic update)"

---

## Workflow Templates for Claude

### Workflow 1: New Real-Time Project (40 min)

**User**: "I want to add real-time features to my React app"

**Claude**:

1. **Ask clarifying questions** (5 min):
   ```
   To recommend the best real-time provider, I need to know:

   1. Do you need bidirectional (client ↔ server) or unidirectional (server → client)?
   2. Self-hosted or managed service?
   3. Expected scale (concurrent users)?
   ```

2. **Recommend provider** (5 min):
   - Based on answers, use decision tree
   - Explain rationale (cost, performance, ease of use)

3. **Setup provider** (15-20 min):
   - Follow `adoption-blueprint.md` for chosen provider
   - Generate provider context/hook
   - Wrap app with provider
   - Create example component

4. **Add TanStack Query integration** (10 min):
   - Generate `useRealtimeInvalidation` hook
   - Show optimistic update example
   - Explain server-side event broadcasting

5. **Testing** (5 min):
   - Open two browser windows
   - Test real-time sync
   - Verify reconnection (kill server, restart)

**Expected time**: 40 minutes
**Output**: Working real-time features with provider setup, TanStack Query integration, and testing

---

### Workflow 2: Add Presence Tracking (30 min)

**User**: "Show online users in my collaborative app"

**Claude**:

1. **Check provider** (2 min):
   - Verify bidirectional provider (Socket.IO, Pusher, or Ably)
   - If SSE, recommend upgrading to Socket.IO or Pusher

2. **Generate presence hook** (15 min):
   ```typescript
   export function usePresence(socket: Socket, roomId: string) {
     const [users, setUsers] = useState<User[]>([]);

     useEffect(() => {
       socket.emit('presence:join', { roomId, user: getCurrentUser() });

       socket.on('presence:update', setUsers);
       socket.on('presence:user-joined', (user) => {
         setUsers(prev => [...prev, user]);
       });
       socket.on('presence:user-left', (userId) => {
         setUsers(prev => prev.filter(u => u.id !== userId));
       });

       return () => {
         socket.emit('presence:leave', roomId);
         socket.off('presence:update');
       };
     }, [socket, roomId]);

     return users;
   }
   ```

3. **Add UI** (10 min):
   ```typescript
   function CollaborativeEditor() {
     const socket = useSocket();
     const users = usePresence(socket, 'room123');

     return (
       <div>
         <div>Online: {users.filter(u => u.status === 'online').length}</div>
         {users.map(user => (
           <div key={user.id}>{user.name} ({user.status})</div>
         ))}
       </div>
     );
   }
   ```

4. **Server-side logic** (5 min):
   - Show server event handlers (`presence:join`, `presence:leave`)
   - Explain broadcasting to room

**Expected time**: 30 minutes
**Output**: Working presence tracking with online users list

---

### Workflow 3: Add Offline Queue (20 min)

**User**: "Queue mutations during offline, sync on reconnect"

**Claude**:

1. **Generate offline queue hook** (15 min):
   ```typescript
   export function useOfflineQueue(socket: Socket) {
     const [queue, setQueue] = useState<Mutation[]>(() => {
       const saved = localStorage.getItem('offline-queue');
       return saved ? JSON.parse(saved) : [];
     });

     const [isOnline, setIsOnline] = useState(socket.connected);

     useEffect(() => {
       socket.on('connect', () => setIsOnline(true));
       socket.on('disconnect', () => setIsOnline(false));

       return () => {
         socket.off('connect');
         socket.off('disconnect');
       };
     }, [socket]);

     const queueMutation = useCallback((mutation) => {
       if (isOnline) {
         socket.emit('mutation', mutation);
       } else {
         setQueue(q => {
           const newQueue = [...q, mutation];
           localStorage.setItem('offline-queue', JSON.stringify(newQueue));
           return newQueue;
         });
       }
     }, [isOnline, socket]);

     useEffect(() => {
       if (isOnline && queue.length > 0) {
         queue.forEach(mutation => socket.emit('mutation', mutation));
         setQueue([]);
         localStorage.removeItem('offline-queue');
       }
     }, [isOnline, queue, socket]);

     return { queueMutation, pendingCount: queue.length, isOnline };
   }
   ```

2. **Add UI indicator** (5 min):
   ```typescript
   const { queueMutation, pendingCount, isOnline } = useOfflineQueue(socket);

   return (
     <div>
       {!isOnline && (
         <div className="bg-yellow-100 p-2">
           Offline ({pendingCount} pending changes)
         </div>
       )}
     </div>
   );
   ```

**Expected time**: 20 minutes
**Output**: Offline queue with localStorage persistence and sync on reconnect

---

### Workflow 4: Debug Real-Time Issues (15-30 min)

**User**: "My WebSocket connections keep dropping"

**Claude**:

1. **Add connection logging** (5 min):
   ```typescript
   socket.on('connect', () => console.log('Connected:', socket.id));
   socket.on('disconnect', (reason) => console.log('Disconnected:', reason));
   socket.on('connect_error', (err) => console.error('Connection error:', err));
   ```

2. **Check common issues** (5-10 min):
   - CORS errors → verify server CORS config
   - Auth failures → check JWT token in `socket.handshake.auth`
   - No auto-reconnect → verify `reconnection: true` in Socket.IO config
   - Load balancer issues → enable sticky sessions

3. **Add reconnection indicator** (5 min):
   ```typescript
   const [isConnected, setIsConnected] = useState(socket.connected);

   useEffect(() => {
     socket.on('connect', () => setIsConnected(true));
     socket.on('disconnect', () => setIsConnected(false));

     return () => {
       socket.off('connect');
       socket.off('disconnect');
     };
   }, [socket]);

   return (
     <div>
       {!isConnected && (
         <div className="bg-yellow-500 text-white p-2">Reconnecting...</div>
       )}
     </div>
   );
   ```

4. **Test fixes** (5-10 min):
   - Kill server → verify auto-reconnect
   - Disable network → verify offline queue
   - Re-enable → verify sync

**Expected time**: 15-30 minutes
**Output**: Debugged connection issues with logging and reconnection indicator

---

## Integration Guidance for Claude

### SAP-023: State Management

**When user has Zustand/Jotai**, integrate real-time updates:

```typescript
import { create } from 'zustand';

export const useTodoStore = create((set) => ({
  todos: [],
  addTodo: (todo) => set((state) => ({ todos: [...state.todos, todo] })),
}));

// Real-time sync
export function useRealtimeSync() {
  const socket = useSocket();
  const { addTodo } = useTodoStore();

  useEffect(() => {
    socket.on('todo:created', addTodo);
    return () => socket.off('todo:created');
  }, [socket, addTodo]);
}
```

**Explain**: "Real-time events update Zustand store directly—all components re-render automatically"

---

### SAP-034: Database Integration

**When user has Prisma**, broadcast database changes:

```typescript
// Server: Broadcast on create
app.post('/api/todos', async (req, res) => {
  const newTodo = await prisma.todo.create({ data: req.body });
  io.emit('todo:created', newTodo); // Broadcast to all clients
  res.json(newTodo);
});

// Client: Invalidate TanStack Query cache
useEffect(() => {
  socket.on('todo:created', () => {
    queryClient.invalidateQueries(['todos']);
  });
}, [socket, queryClient]);
```

**Explain**: "Database changes trigger real-time events—all clients stay in sync automatically"

---

### SAP-036: Error Handling

**Add reconnection error boundaries**:

```typescript
function RealtimeErrorBoundary({ children }) {
  const socket = useSocket();
  const [hasError, setHasError] = useState(false);

  useEffect(() => {
    socket.on('connect_error', () => setHasError(true));
    socket.on('connect', () => setHasError(false));

    return () => {
      socket.off('connect_error');
      socket.off('connect');
    };
  }, [socket]);

  if (hasError) {
    return <div>Connection lost. Reconnecting...</div>;
  }

  return <>{children}</>;
}
```

**Explain**: "Error boundary shows fallback UI during connection failures—graceful degradation"

---

## Common Pitfalls for Claude

### Pitfall 1: Not Cleaning Up Event Listeners

**Problem**:
```typescript
// ❌ Memory leak (no cleanup)
useEffect(() => {
  socket.on('event', handler);
  // No return statement
}, [socket]);
```

**Fix**:
```typescript
// ✅ Proper cleanup
useEffect(() => {
  socket.on('event', handler);

  return () => {
    socket.off('event', handler);
  };
}, [socket]);
```

**Claude should always generate cleanup** in `useEffect` return statements.

---

### Pitfall 2: Not Waiting for Connection Before Emitting

**Problem**:
```typescript
// ❌ Socket may not be connected yet
socket.emit('join:room', roomId);
```

**Fix**:
```typescript
// ✅ Wait for connection
useEffect(() => {
  socket.on('connect', () => {
    socket.emit('join:room', roomId);
  });
}, [socket, roomId]);
```

**Claude should wrap emits** in `connect` event handler.

---

### Pitfall 3: Recommending Wrong Provider

**Problem**: User asks for "notifications" → Claude recommends Socket.IO (overkill)

**Fix**: Ask "Do you need bidirectional?" → If NO, recommend SSE (simpler)

**Claude should always use decision tree** before recommending provider.

---

### Pitfall 4: Not Explaining Server-Side Setup

**Problem**: Claude only generates client code, user confused about server

**Fix**: Always mention server setup:
- "Next, you'll need to set up Socket.IO on your server (see protocol-spec.md)"
- "For SSE, create an API route that streams events (I'll show you)"

**Claude should provide both client AND server code** (or link to protocol-spec.md).

---

### Pitfall 5: Not Testing Reconnection

**Problem**: User tests once with stable connection, misses reconnection bugs

**Fix**: Always include testing instructions:
- "Test by opening two browser windows"
- "Kill server, restart, verify auto-reconnect"
- "Disable network, verify offline queue"

**Claude should provide testing checklist** in every setup.

---

## Performance Optimization Tips for Claude

### 1. Throttle High-Frequency Events

**When user implements cursor tracking**:

```typescript
import { throttle } from 'lodash';

const throttledUpdateCursor = throttle((x, y) => {
  socket.emit('presence:cursor', { x, y });
}, 100); // Max 10 updates/sec

<div onMouseMove={(e) => throttledUpdateCursor(e.clientX, e.clientY)} />
```

**Explain**: "Cursor moves 60 times/sec—throttling to 10/sec reduces server load by 83%"

---

### 2. Batch Multiple Updates

**When user has frequent updates**:

```typescript
let pendingUpdates: Update[] = [];
let batchTimeout: NodeJS.Timeout;

socket.on('todo:update', (update) => {
  pendingUpdates.push(update);

  clearTimeout(batchTimeout);
  batchTimeout = setTimeout(() => {
    applyBatchUpdates(pendingUpdates);
    pendingUpdates = [];
  }, 100);
});
```

**Explain**: "Batching 10 updates into 1 reduces re-renders by 90%"

---

### 3. Use Rooms for Scoped Broadcasts

**When user broadcasts to all clients**:

```typescript
// ❌ Broadcasts to ALL clients (wasteful)
io.emit('todo:created', newTodo);

// ✅ Broadcast to room only
io.to(roomId).emit('todo:created', newTodo);
```

**Explain**: "Rooms reduce bandwidth by 10x—only users in same room receive events"

---

## Security Checklist for Claude

When implementing real-time features, Claude should ensure:

- [ ] **Authentication**: JWT tokens in `socket.handshake.auth`
- [ ] **Authorization**: Check user permissions before broadcasting
- [ ] **Rate limiting**: Prevent abuse (token bucket algorithm)
- [ ] **Message validation**: Zod schemas for all events
- [ ] **XSS prevention**: Sanitize user-generated content
- [ ] **CORS configuration**: Restrict origins in production
- [ ] **TLS/SSL**: Use `wss://` and `https://` in production

**Example**: Always include auth middleware in server examples:

```typescript
io.use((socket, next) => {
  const token = socket.handshake.auth.token;
  if (!token) return next(new Error('Auth required'));

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET!);
    socket.data.userId = decoded.userId;
    next();
  } catch (err) {
    next(new Error('Invalid token'));
  }
});
```

---

## Documentation Navigation for Claude

### When to Read Each Artifact

| User Request | Artifact to Read | Why |
|--------------|------------------|-----|
| "What is SAP-037?" | AGENTS.md (quick reference) | High-level overview, decision tree |
| "Setup Socket.IO" | adoption-blueprint.md (Option A) | Step-by-step setup, 15 min |
| "How to integrate with TanStack Query?" | protocol-spec.md (How-To section) | Copy-paste patterns |
| "Show me presence tracking example" | protocol-spec.md (How-To section) | Complete code example |
| "Why use Pusher vs Socket.IO?" | capability-charter.md (Solution Design) | Architecture comparison |
| "How much time does this save?" | ledger.md (Time Savings Evidence) | Quantified metrics |

---

### Progressive Reading Strategy

**Small request** (e.g., "Setup Socket.IO"):
- Read: adoption-blueprint.md (Option A only)
- Don't read: protocol-spec.md (too large), capability-charter.md (not needed)

**Medium request** (e.g., "Add real-time + presence"):
- Read: adoption-blueprint.md + protocol-spec.md (How-To section)
- Don't read: capability-charter.md, ledger.md

**Large request** (e.g., "Design real-time architecture"):
- Read: capability-charter.md (Solution Design) + protocol-spec.md (full)
- Skim: ledger.md (cost analysis)

---

## Quick Command Reference

### Installation

```bash
# Socket.IO
npm install socket.io-client

# SSE (native, no install)

# Pusher
npm install pusher-js

# Ably
npm install ably
```

### Testing

```bash
# Run dev server
npm run dev

# Open two browser windows
open http://localhost:3000
open http://localhost:3000

# Kill server (test reconnection)
Ctrl+C

# Restart server
npm run dev
```

---

## Version History

- **1.0.0** (2025-11-09): Initial release
  - Four-provider architecture (Socket.IO, SSE, Pusher, Ably)
  - Progressive context loading strategy
  - Code generation patterns for all providers
  - 4 workflow templates
  - Integration guidance (SAP-023, SAP-034, SAP-036)
  - Common pitfalls and fixes

---

**Status**: Pilot
**For**: Claude Code, Claude Desktop, Claude API
**Estimated Setup Time**: 40 minutes
**Time Savings**: 90.5% (5-7h → 40min)
**Next Review**: After 3 validation projects
