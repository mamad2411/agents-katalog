---
name: eventhub-analyze-throughput
description: Analyze Azure Event Hubs throughput and capacity including throughput units, processing units or capacity units as applicable, auto-inflate, ingress/egress, throttling, quota pressure, and workload bursts. Use for throttling, capacity incidents, or stream scaling analysis.
---

# Analyze Throughput

1. Resolve namespace tier and the capacity model used by that tier.
2. Inspect ingress, egress, request/throttling signals, partition load, and workload peaks.
3. Determine whether pressure is:
   - capacity-related
   - partition-skew related
   - producer burst related
   - consumer/backlog related
4. Inspect auto-inflate or equivalent capacity settings when applicable.
5. Compare capacity with sustained and burst workload needs.
6. Do not change capacity unless explicitly authorized.

## Output
- Capacity Model
- Throughput Evidence
- Throttling/Quota Findings
- Capacity vs Distribution Assessment
- Recommended Action
