---
name: streaming-architecture
version: 1.0.0
min_mindforge_version: 10.0.9
status: stable
triggers: streaming architecture, server sent events, chunked transfer, real-time pipeline, stream processing, backpressure stream, event stream, streaming response, stream consumer, data stream design, stream partitioning, stream windowing
---

# Skill — Streaming Architecture

## When this skill activates
Any task involving real-time data streaming, SSE, chunked transfer encoding,
stream processing pipelines, backpressure, partitioning, or windowing strategies.

## Mandatory actions when this skill is active

### Before writing any code
1. Choose transport (SSE vs WebSocket vs long-polling) using the decision matrix.
2. Define stream data format (NDJSON, chunked binary, protobuf frames).
3. Identify backpressure requirements and partition strategy.

### During implementation
- Implement backpressure handling at every pipeline stage.
- Use chunked transfer encoding for HTTP streaming responses.
- Apply appropriate windowing strategy for aggregation needs.
- Partition by key for ordering, round-robin for throughput.

### After implementation
- Load test under sustained high-throughput conditions.
- Verify consumer groups scale horizontally without message loss.
- Document partition strategy and windowing semantics.

## Transport Decision Matrix

| Transport | Direction | Use For | Limitation |
|-----------|-----------|---------|------------|
| SSE | Server→Client | Notifications, feeds, progress, logs | Text-only, unidirectional |
| WebSocket | Bidirectional | Chat, collaboration, gaming | Proxy complexity, reconnection logic |
| Long-Polling | Client→Server→Client | Legacy envs, infrequent updates | High latency, resource overhead |

- SSE: auto-reconnect via Last-Event-ID, works through load balancers.
- WebSocket: lower per-message overhead after handshake, requires connection management.
- Long-Polling: universally compatible, highest resource cost at scale.

## Streaming Response Patterns

- **Chunked Transfer**: `Transfer-Encoding: chunked` — each chunk is a parseable unit.
- **NDJSON**: one JSON object per `\n`-separated line, parse incrementally.
- Use NDJSON for LLM token streaming, batch results, log streams.

## Stream Processing Windows

- **Tumbling**: fixed-size, non-overlapping. Use for per-minute aggregations.
- **Sliding**: fixed-size, overlapping by step. Use for moving averages.
- **Session**: dynamic size, closes after inactivity gap. Use for user sessions.

## Backpressure Strategies

- **Buffer and Batch**: bounded buffer, process in batches at threshold or timer.
- **Drop Oldest** (lossy): discard stale messages when buffer full. Never for transactions.
- **Signal Producer** (reactive): consumer signals demand, producer throttles emission.

## Partition Strategies

- **Key-Based**: same key → same partition. Guarantees per-key ordering. Risk: hot partitions.
- **Round-Robin**: even distribution, max throughput, no ordering guarantees.

## Consumer Groups
- Multiple consumers share partitions (one partition per consumer max).
- Scale up to partition count (more consumers = idle).
- Rebalancing on consumer join/leave. Track offsets for resume-from-failure.

## Self-check before task completion

- [ ] Is the transport correct for the use case (SSE/WebSocket/long-polling)?
- [ ] Is backpressure handled at every pipeline stage?
- [ ] Are streaming responses chunked with parseable units?
- [ ] Is windowing strategy appropriate for aggregation needs?
- [ ] Are partitions designed for the right ordering vs throughput trade-off?
- [ ] Can consumers scale horizontally without message loss?
- [ ] Is reconnection logic implemented for client-side streams?
