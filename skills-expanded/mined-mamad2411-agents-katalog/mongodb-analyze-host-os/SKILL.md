---
name: mongodb-analyze-host-os
description: Analyze Linux host configuration for self-managed MongoDB, including memory, swap, Transparent Huge Pages, ulimits, CPU, NUMA considerations, filesystem, disk latency, and kernel/runtime settings. Use for host-level performance or configuration problems.
---

# Analyze Host OS

1. Resolve host OS/version, MongoDB version, CPU, RAM, storage, filesystem, and virtualization.
2. Compare host settings with recommendations appropriate to the deployed MongoDB version.
3. Inspect memory pressure, swap, THP state, file/process limits, CPU saturation, and disk latency.
4. Correlate host pressure with MongoDB cache, connections, and latency.
5. Do not blindly apply historical tuning guidance across MongoDB versions.
6. Do not change kernel/host settings without explicit authorization.

## Output
- Host Profile
- OS Configuration Findings
- Resource Pressure
- MongoDB Correlation
- Recommended Action
