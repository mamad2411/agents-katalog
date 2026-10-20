---
name: msk-analyze-flink
description: Analyze Amazon Managed Service for Apache Flink integrations with Amazon MSK, including source/sink configuration, checkpoints, state, parallelism, backpressure, offsets, lag, and runtime failures. Use for stateful AWS stream-processing pipelines.
---

# Analyze Managed Flink Integration

1. Identify MSK sources/sinks, Flink application, parallelism, checkpoints/savepoints, and processing semantics.
2. Inspect input/output rates, backpressure, checkpoint health, state growth, and failures.
3. Compare Kafka partitions with Flink parallelism.
4. Correlate MSK lag/capacity with Flink processing evidence.
5. Distinguish source, Flink runtime/state, and sink failures.
6. Do not reset state or offsets without explicit authorization.

## Output
- Streaming Topology
- Checkpoint/State Findings
- Parallelism/Backpressure
- Failure Layer
- Recommended Action
