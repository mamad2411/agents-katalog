---
tags: [backend, kafka, consumer, tenant, fan, out]
name: kafka-consumer-tenant-fan-out
description: @KafkaListener pattern consuming a topicPattern across tenants, using a record header for tenant identity and routing to per-tenant downstream streams
trigger: A single consumer group needs to consume messages across many per-tenant topics and route by tenant — without hardcoding topic names or restarting on tenant add
category: backend
source_project: lucida-realtime
version: 1.0.0
---

# kafka-consumer-tenant-fan-out

See `content.md`.
