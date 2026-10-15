---
name: websocket-real-time
description: "Implement WebSocket communication for real-time bidirectional client-server communication."
---

# WebSocket Real-Time Communication

## Overview
WebSockets provide persistent bidirectional communication between clients and servers. This skill should be invoked when building real-time applications like chat, live dashboards, or collaborative tools.

## Core Principles
- **Persistent Connection**: Single connection for bidirectional communication
- **Message Protocol**: Define message format for your application
- **Connection Lifecycle**: Handle connect, disconnect, error events
- **Reconnection**: Implement automatic reconnection

## Preparation Checklist
- [ ] Choose WebSocket library (ws, Socket.io)
- [ ] Design message protocol
- [ ] Plan connection handling
- [ ] Design for scaling

## Step-by-Step Process
1. **Server**: Set up WebSocket server
2. **Upgrade**: Handle HTTP to WebSocket upgrade
3. **Message**: Implement send/receive logic
4. **Lifecycle**: Handle connect/disconnect
5. **Reconnect**: Add reconnection logic
6. **Scale**: Plan for horizontal scaling

## Do's and Don'ts
- ✅ **Do** use secure WebSocket (wss://)
- ✅ **Do** implement heartbeat/ping-pong
- ✅ **Do** handle reconnection
- ❌ **Don't** send sensitive data unencrypted
- ❌ **Don't** skip error handling
- ❌ **Don't** ignore scaling challenges

## Anti-Patterns
- **No Heartbeat**: Not detecting dead connections
- **No Reconnection**: Not handling dropped connections
- **Large Messages**: Sending too much data
- **No Error Handling**: Ignoring errors
