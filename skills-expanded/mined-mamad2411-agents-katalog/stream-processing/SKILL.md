---
name: stream-processing
version: 1.0.0
min_mindforge_version: 10.6.0
status: stable
triggers: stream processing architecture, event streaming pattern, windowing strategy stream, exactly-once stream processing, stream state management, Kafka streaming, Flink processing, stream join pattern, late event handling, stream aggregation, watermark strategy, event time processing
compose: streaming-architecture
---

# Skill — Stream Processing

## When this skill activates
This skill activates when designing real-time data pipelines, implementing event streaming architectures, or building low-latency aggregation systems. Use when data must be processed continuously as it arrives rather than in batch intervals.

## Mandatory actions when this skill is active

### Before writing any code
1. Define processing semantics requirements: at-most-once (fast, lossy), at-least-once (duplicates possible), exactly-once (consistency critical)
2. Select windowing strategy based on use case: tumbling (fixed non-overlapping), sliding (overlapping intervals), session (activity-based gaps)
3. Design watermark strategy for handling late events: fixed delay, percentile-based, or custom heuristic with acceptable lateness window
4. Establish state management approach: in-memory (fast but limited), RocksDB (scalable), remote store (shared state) with checkpointing frequency

### During implementation
- Implement event time processing using timestamps from event payload rather than processing time to handle out-of-order events correctly
- Configure watermarks with balance between latency and completeness: too aggressive drops late events, too conservative increases latency
- Design stateful operations with appropriate state backend and checkpointing: every 5-60 seconds based on throughput and failure recovery requirements
- Build stream joins with care for state size: time-bounded joins, interval joins, or temporal table joins to prevent unbounded state growth
- Implement exactly-once semantics using transactional producers, idempotent consumers, and two-phase commit when required
- Handle late events with configurable strategy: drop and log, emit to side output, update previous window results with allowed lateness
- Design backpressure handling: flow control to slow down producers, buffer sizing, and scaling policies for consumer parallelism

### After implementation
- Monitor stream processing lag metrics: consumer group lag, watermark delay, late events dropped, and checkpoint duration
- Build observability dashboards: throughput (events/sec), latency percentiles (p50/p95/p99), error rates, and state size growth
- Create alerting on critical conditions: lag exceeding SLA, checkpoint failures, repeated consumer rebalancing, state size approaching limits
- Document failure recovery procedures: checkpoint restoration, consumer group reset, and data replay strategies

## Self-check before task completion
- [ ] Processing semantics (at-least-once or exactly-once) verified with end-to-end tests including failure injection
- [ ] Watermark strategy handles late events appropriately with acceptable data loss or latency trade-off documented
- [ ] State management configured with checkpointing and tested with recovery from checkpoint after failure
- [ ] Stream joins bounded in time with monitoring for state size growth and cleanup of expired state
- [ ] Backpressure scenarios tested with producer slowdown and consumer scaling validated under load
