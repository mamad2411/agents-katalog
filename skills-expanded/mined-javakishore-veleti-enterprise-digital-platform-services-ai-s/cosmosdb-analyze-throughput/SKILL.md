---
name: cosmosdb-analyze-throughput
description: Analyze Azure Cosmos DB Request Unit consumption, provisioned throughput, autoscale, serverless usage, throttling, 429 responses, burst behavior, container/database throughput placement, and capacity. Use for performance, scaling, or RU-related incidents.
---

# Analyze Throughput

1. Resolve throughput mode and where throughput is configured.
2. Inspect RU consumption, normalized RU usage, throttling/429s, partition-level demand, and workload peaks.
3. Determine whether pressure is:
   - query-driven
   - write-driven
   - hot-partition driven
   - under-provisioning
   - burst-related
4. Compare provisioned/autoscale/serverless behavior to workload shape.
5. Separate capacity symptoms from inefficient application operations.
6. Do not change throughput unless explicitly authorized.

## Output
- Throughput Mode
- RU Consumption Evidence
- Throttling Analysis
- Capacity vs Efficiency Assessment
- Recommended Action
