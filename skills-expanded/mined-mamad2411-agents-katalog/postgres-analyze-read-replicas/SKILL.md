---
name: postgres-analyze-read-replicas
description: Analyze Azure PostgreSQL Flexible Server read replicas, replication lag, read scaling, replica topology, application routing, cascading behavior where supported, and promotion considerations. Use for read-scaling or replica incidents.
---

# Analyze Read Replicas

1. Map primary and replicas, regions, compute/storage, and application read routing.
2. Inspect replication lag and workload on each replica.
3. Evaluate read-after-write consistency requirements before routing reads to replicas.
4. Correlate lag with write rate, query workload, network, and resource pressure.
5. Verify current platform support before recommending cascading or promotion patterns.
6. Do not promote or reconfigure production replicas without explicit authorization.

## Output
- Replica Topology
- Lag/Capacity Findings
- Consistency Impact
- Routing Findings
- Recommended Action
