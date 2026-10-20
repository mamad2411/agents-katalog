---
name: eventhub-analyze-stream-analytics
description: Analyze Azure Stream Analytics integrations with Azure Event Hubs, including input configuration, partitions, event time, watermark/late arrival behavior, windows, joins, output errors, and streaming lag. Use for real-time analytics pipeline failures or incorrect results.
---

# Analyze Stream Analytics

1. Identify Event Hubs input, Stream Analytics job, query/window logic, and outputs.
2. Inspect input deserialization, event-time fields, late/out-of-order handling, watermark behavior, and partitioning.
3. Evaluate window/join semantics against expected business behavior.
4. Correlate input lag and Event Hubs metrics with job processing health.
5. Distinguish source issues from query logic and output sink failures.
6. Do not change production queries unless explicitly authorized.

## Output
- Pipeline Topology
- Event-Time/Window Findings
- Input/Output Evidence
- Failure or Correctness Layer
- Recommended Action
