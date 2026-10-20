---
name: mongodb-analyze-connections
description: Analyze MongoDB connection usage, driver pools, connection limits, authentication overhead, network churn, timeouts, and application pool behavior. Use for connection storms, pool exhaustion, or intermittent connectivity.
---

# Analyze Connections

1. Identify application instances, drivers, pool configuration, and MongoDB endpoints.
2. Inspect current/available connections and connection creation/churn.
3. Correlate connection spikes with deployments, autoscaling, failovers, and authentication.
4. Distinguish server connection limits from application pool starvation or leaks.
5. Check load balancer/router behavior where applicable.
6. Route driver-specific issues to application skills when appropriate.

## Output
- Connection Topology
- Pool/Server Evidence
- Churn/Timeout Findings
- Failure Layer
- Recommended Action
