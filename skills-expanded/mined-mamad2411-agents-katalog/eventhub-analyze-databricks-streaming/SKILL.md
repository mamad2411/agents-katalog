---
name: eventhub-analyze-databricks-streaming
description: Analyze Azure Databricks or Spark Structured Streaming integrations with Azure Event Hubs, including Kafka-compatible endpoints, offsets, checkpoints, partition parallelism, lag, throughput, and downstream processing. Use for Databricks/Spark streaming pipeline issues.
---

# Analyze Databricks Streaming

1. Identify Event Hubs source, connection mode, Spark/Databricks job, checkpoint location, partitions, and processing trigger.
2. Inspect input rate, processing rate, batch duration, offsets, lag, and checkpoint behavior.
3. Compare source partitions with Spark parallelism.
4. Correlate Event Hubs throttling or skew with streaming-job backpressure.
5. Distinguish source ingestion issues from Spark processing or downstream sink problems.
6. Do not reset checkpoints or offsets unless explicitly authorized.

## Output
- Streaming Topology
- Offset/Lag Findings
- Parallelism/Backpressure
- Failure Layer
- Recommended Action
