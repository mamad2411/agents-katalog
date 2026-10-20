---
name: msk-analyze-producer
description: Analyze producers writing to Amazon MSK including batching, compression, acknowledgments, idempotence, partitioning, retries, IAM/TLS configuration, and broker correlation. Use for producer latency, errors, throughput, or uneven partition traffic.
---

# Analyze Producer

1. Identify producer application, Kafka client, topic, partition strategy, authentication, and workload.
2. Inspect batch, linger, compression, acknowledgments, retries, and idempotence settings.
3. Correlate send errors with MSK broker/capacity/network metrics.
4. Identify low-cardinality partition keys or explicit partition routing that creates skew.
5. Route generic Kafka client semantics to relevant `kafka-*` skills.
6. Never expose credentials.

## Output
- Producer Configuration
- Throughput/Latency Findings
- Partitioning
- MSK Correlation
- Recommended Action
