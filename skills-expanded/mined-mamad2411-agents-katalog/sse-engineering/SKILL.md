---
name: sse-engineering
description: Implement Server-Sent Events. Use when streaming one-way updates
  from server to client.
metadata:
  tags: sse, engineering
---

# SSE Engineering

## Use this skill when
- Streaming events to the browser
- Reconnecting and resuming streams
- Choosing SSE over WebSockets/APIs

## Do not use this skill when
- Bidirectional requirements (use websocket-engineering)
- Low-latency client→server messaging

## Instructions
1. Use SSE for one-way server→client streams (news, progress, AI).
2. Handle auto-reconnect and Last-Event-ID resumption.
3. Add keepalive/comment lines and heartbeat events.
4. Sanitize event fields; JSON-encode data.
5. Scope streams to user and session.
6. Care with proxies buffering; set flush policy.

## Checklist
- Resume support via Last-Event-ID
- Heartbeats keep the stream alive
- Auth on the stream

## Output Format
- Stream events | resumption | buffering notes

## Common Mistakes
- SSE for chat-style bidirectional needs
- Dropping messages without resume
- Buffered streams appearing dead
