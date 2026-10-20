---
name: msk-analyze-connect
description: Analyze Amazon MSK Connect connectors, custom plugins, worker configurations, capacity/autoscaling, source/sink behavior, errors, IAM, networking, and downstream systems. Use for managed Kafka Connect pipelines on AWS.
---

# Analyze MSK Connect

1. Identify connector, source/sink, plugin, worker configuration, MSK cluster, and target system.
2. Inspect connector state, task failures, throughput, worker capacity, autoscaling, and error handling.
3. Verify IAM and network access to MSK and external systems.
4. Correlate connector errors with source/sink and cluster evidence.
5. Check plugin/version changes before blaming the broker.
6. Do not restart or update production connectors without explicit authorization.

## Output
- Connector Topology
- Task/Capacity Findings
- IAM/Network Findings
- Source/Sink Correlation
- Recommended Action
