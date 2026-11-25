---
name: aks-analyze-storage
description: Analyze AKS persistent storage, PersistentVolumes, PersistentVolumeClaims, StorageClasses, mounts, attachment issues, capacity, access modes, and volume-related pod failures. Use for mount failures, pending PVCs, storage exhaustion, or stateful workload issues.
---

# Analyze Storage

1. Resolve the affected pods, PVCs, PVs, and StorageClasses.
2. Inspect claim binding, capacity, access modes, mount paths, volume attachments, and related events.
3. Compare pod/deployment volume declarations with live storage resources.
4. Identify pending claims, mount failures, capacity issues, access-mode conflicts, or stale attachments.
5. Correlate storage timing with pod scheduling and restart evidence.
6. Do not delete or recreate storage resources unless explicitly authorized.

## Output
- PVC/PV State
- Mount/Attachment Findings
- Capacity and Access Evidence
- Impacted Workloads
- Recommended Action
