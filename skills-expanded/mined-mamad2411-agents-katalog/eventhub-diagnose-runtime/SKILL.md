---
name: eventhub-diagnose-runtime
description: Diagnose Azure Event Hubs incidents end-to-end across namespaces, capacity, partitions, producers, consumers, consumer groups, checkpoints, schema, Capture, security, Kafka protocol, geo-replication, and application evidence. Use as the primary Event Hubs incident workflow when the failure domain is unknown.
---

# Diagnose Runtime

1. Read `.digital-platform-ai/eventhub.yaml`, service dependencies, environments, observability metadata, and relevant service instructions.
2. Resolve namespace, event hub, consumer group, environment, producer, and consumer.
3. Gather independent evidence in parallel:
   - namespace/capacity metrics
   - partition distribution
   - producer errors
   - consumer lag/checkpoints
   - application logs/traces
   - schema or authentication errors
4. Build a timeline around the first confirmed abnormal event.
5. Route to focused `eventhub-*` skills as needed.
6. Separate producer, broker/capacity, partition, consumer, schema, networking/security, and downstream failures.
7. Do not mutate production resources unless explicitly authorized.

## Output
- Incident Scope
- Stream Topology
- First Confirmed Failure
- Supporting Evidence
- Failing Layer
- Recommended Action
