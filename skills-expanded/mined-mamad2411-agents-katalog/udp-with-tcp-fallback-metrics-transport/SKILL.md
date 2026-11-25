---
name: udp-with-tcp-fallback-metrics-transport
description: Transport telemetry via UDP for low-latency fire-and-forget streams, and fall back to TCP for critical request/response and bulk uploads that require delivery guarantees
category: backend
version: 1.0.0
source_type: extracted-from-git
source_url: https://github.com/kjuhwa/scouter
source_ref: master
source_commit: 126bb19f07d1fe4fe915eb408c381e2c140cc94c
source_project: scouter
version_origin: extracted
tags: [network, udp, tcp, apm, telemetry]
confidence: high
---

# UDP + TCP Hybrid Metrics Transport

Apply when you're building a metric collector or APM agent that must be cheap on the monitored process and reliable for control-plane operations.

## Pattern

1. **UDP lane (default)** — periodic counters, stacks, heartbeats. Packet loss tolerated because next tick retransmits naturally.
2. **TCP lane (critical)** — config fetch, agent registration, XLog profile uploads, anything that must arrive.
3. **Fragmentation aware** — MTU (~1400 B) forces multi-packet framing with sequence IDs when a single record exceeds one datagram. Reassembler keeps a short TTL buffer.
4. **Backpressure** — UDP has none. Cap agent sender rate; drop excess locally rather than flood the network.
5. **Ports** — conventionally split (scouter: 6100 UDP, 6101 TCP). Documented in agent config.

## Evidence

- `scouter.agent.batch/src/main/java/scouter/agent/batch/netio/data/net/UdpAgent.java`
- `scouter.agent.batch/src/main/java/scouter/agent/batch/netio/data/net/TcpAgentReqMgr.java`
- `scouter.document/main/Configuration.md`

## Trade-offs

- UDP minimizes agent CPU / network overhead — critical for production JVMs.
- No native encryption for UDP path; if deploying cross-zone, wrap UDP in WireGuard or similar, or force TCP.
- Not suitable for exactly-once telemetry (billing events, audit logs) — use TCP or a message queue.

## Related knowledge

- `udp-for-throughput-tcp-for-reliability` (decision)
