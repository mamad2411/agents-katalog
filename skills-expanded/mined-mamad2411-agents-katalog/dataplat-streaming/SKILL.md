---
name: dataplat-streaming
description: Streaming / event-data specialist. Owns Kafka / Kinesis / Pulsar / PubSub topology, schema evolution, exactly-once semantics, stream processing (Flink / Spark / ksqlDB), and stream-to-warehouse landing. Auto-invoked when designing or debugging streaming pipelines, schemas, or stream-processing jobs.
---

# Data Platform Streaming

Streams are batch jobs you can't reach back into: a bad schema, key, or
delivery guarantee is replayed at full volume before anyone notices. Schema
evolution, delivery semantics, and back-pressure are the difference between a
real-time pipeline and a real-time outage.

## When to reach for this

- Designing topics, partitions, retention, or compaction on Kafka / Kinesis / Pulsar / PubSub
- Choosing or enforcing delivery semantics (at-least-once vs exactly-once)
- Writing or debugging Flink / Spark Structured Streaming / ksqlDB jobs, watermarks, or state
- Landing streams into the warehouse (CDC, change feeds, sink connectors)

## Principles

1. **Schema registry from day one.** Avro/Protobuf with `BACKWARD`
   compatibility enforced at publish time — consumers upgrade first, producers
   can then add optional fields and drop fields safely. Raw JSON topics are
   schema drift waiting to happen.
2. **Partition key with intent.** The key determines ordering (per-partition
   only) and co-partitioning for joins. Keys must be high-cardinality and
   evenly distributed; changing the partition count rehashes keys and breaks
   per-key ordering, so over-provision partitions up front.
3. **Exactly-once is configuration *and* code.** On Kafka:
   `enable.idempotence=true` on producers, transactions for read-process-write,
   `isolation.level=read_committed` on consumers — and a transactional or
   idempotent sink. Miss any one and the guarantee is gone.
4. **At-least-once + idempotent sink is the pragmatic default.** Effectively-once
   via upsert/merge keyed on a stable event ID is simpler and cheaper than full
   transactional exactly-once; reserve the latter for ledger-grade streams.
5. **Every windowed job declares a late-data policy.** Watermark delay, allowed
   lateness, and what happens to later-than-allowed events (drop, side output,
   reconciliation batch) are written down, not discovered.
6. **Design for slow consumers, not just spikes.** Back-pressure is normal
   operation: monitor consumer lag with alerts, bound state with TTLs, and size
   retention so the slowest consumer can recover from an outage without data loss.

## Delivery-semantics decision table

| Need | Choose | Enforced by |
|---|---|---|
| Metrics / analytics events | at-least-once + dedupe in warehouse | stable event ID, merge on load |
| Materialized views / upserts | effectively-once | idempotent sink keyed on entity ID |
| Read-process-write between topics | exactly-once | Kafka transactions + `read_committed` |
| Money movement / ledger | exactly-once + reconciliation | transactions and an independent batch audit |
| Fire-and-forget telemetry, loss OK | at-most-once | acks=0/1, no retries — be explicit it's lossy |

## Topic design checklist

- [ ] Key chosen for join/ordering needs; cardinality checked for hot partitions
- [ ] Partition count sized for target consumer parallelism (consumers ≤ partitions)
- [ ] Replication factor ≥ 3 with `min.insync.replicas=2` and producer `acks=all` for durable topics
- [ ] Retention sized to worst-case consumer recovery time; compaction only for changelog/keyed-state topics
- [ ] Schema registered with compatibility mode recorded; evolution workflow documented
- [ ] Consumer lag alerting wired before go-live
- [ ] DLQ or side-output path for poison messages

## Pitfalls

- Committing offsets before processing completes — accidental at-most-once,
  data lost on crash
- "Exactly-once" claimed because the framework checkpoint is on, while the sink
  is a plain append (duplicates on recovery)
- Low-cardinality partition keys (country, status) creating hot partitions that
  cap throughput
- Unbounded keyed state in stream joins/aggregations without TTL — the job dies
  weeks later on state size
- One poison message stalling a partition because there's no DLQ path
- Timestamps taken from broker ingestion time instead of event time, skewing
  every window

---
*Related: `dataplat-etl` (batch ingestion and the landing zone),
`dataplat-quality` (contracts on landed tables, schema-change blast radius),
`dataplat-feature-store` (streams feeding online features) · domain agent:
`dataplat-architect` (batch vs streaming topology) · output/ADR format:
`playbook-conventions`*
