---
name: zeromq
description: "Applies when building or reviewing ZeroMQ messaging systems. Covers socket patterns, context management, HWM, polling, and message serialization."
---

# ZeroMQ

## Context and sockets

1. **zmq.Context as long-lived singleton.** One per process. term() at shutdown.
2. **Right pattern.** REQ/REP: sync RPC. PUB/SUB: broadcast. PUSH/PULL: work distribution. DEALER/ROUTER: async routing.
3. **Bind stable node (server), connect transient (workers/clients).**

## Configuration

4. **Set HWM to prevent unbounded memory.** Default 1000. PUB drops, PUSH blocks when reached.
5. **zmq.Poller for multiplexing.** Never busy-loop recv(). Poller = select/epoll.
6. **LINGER on sockets before close.** Default infinite blocks forever. Set 0 or short timeout.

## Messages

7. **Multipart for framing.** Separate identity, headers, body. No custom delimiters.
8. **msgpack or protobuf, not pickle.** JSON for interop, msgpack for speed.

## Pitfalls

9. **REQ/REP lockstep: crash mid-conversation = both stuck.** DEALER/ROUTER for production.
10. **PUB/SUB slow-joiner: subscribers miss initial messages.** Sync pattern or PUSH/PULL.
11. **Never share sockets across threads.** inproc:// with per-thread sockets.
12. **PAIR only for intra-process.** 1-to-1, no reconnect.
13. **TCP_KEEPALIVE for long-lived connections.** Firewalls drop idle silently.
14. **Proxy for load balancing.** ROUTER frontend, DEALER backend.
