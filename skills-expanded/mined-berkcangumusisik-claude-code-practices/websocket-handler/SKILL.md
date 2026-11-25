---
name: websocket-handler
description: Implements WebSocket handlers with rooms, authentication, and reconnection logic
argument-hint: <feature-description>
user-invocable: true
allowed-tools: Read Glob Edit
effort: medium
---

## WebSocket Implementation

Feature: **$ARGUMENTS**

1. Detect WebSocket library:
```bash
cat package.json | grep -E '"socket.io"|"ws"|"@fastify/websocket"|"hono.*ws"|"partykit"'
```

2. Generate server-side handler:
```ts
// Socket.io example
io.on('connection', (socket) => {
  // Auth check
  const userId = socket.handshake.auth.token
  if (!isValidToken(userId)) {
    socket.disconnect()
    return
  }

  // Room management
  socket.join(`user:${userId}`)

  socket.on('message', async (data) => {
    // Validate input
    // Handle event
    // Broadcast to relevant room
    io.to(`room:${data.roomId}`).emit('message', response)
  })

  socket.on('disconnect', () => {
    // Cleanup
  })
})
```

3. Generate client-side hook with:
   - Automatic reconnection with exponential backoff
   - Connection state management
   - Cleanup on unmount
   - TypeScript event typing

4. Add error handling for:
   - Auth failures
   - Network drops
   - Server restarts

5. Include a message type registry to keep events typed end-to-end.
