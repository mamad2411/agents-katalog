---
name: eventhub-analyze-producer
description: Analyze Azure Event Hubs producer behavior including batching, partition routing, retries, idempotency expectations, transport, send latency, failures, schema serialization, and SDK configuration. Use for publish failures, uneven partitions, high send latency, or producer integration review.
---

# Analyze Producer

1. Identify producer service, SDK/client, event hub, transport, batching, partition-key strategy, and schema.
2. Inspect send errors, retry behavior, timeout handling, and batch sizing.
3. Correlate producer telemetry with Event Hubs ingress/throttling metrics.
4. Check whether explicit partition IDs or low-cardinality keys create skew.
5. Validate serialization/schema behavior when Schema Registry is used.
6. Do not expose SAS keys, connection strings, tokens, or credentials.

## Output
- Producer Configuration
- Send/Retry Findings
- Partition Routing
- Broker Correlation
- Recommended Changes
