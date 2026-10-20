---
name: mongodb-analyze-storage
description: Analyze self-managed MongoDB storage layout, filesystem, volumes, IOPS/latency, capacity, journal/data placement, RAID or cloud-disk characteristics, and disk saturation. Use for storage bottlenecks or capacity planning.
---

# Analyze Storage

1. Identify volume/filesystem topology, capacity, latency, throughput, and durability characteristics.
2. Inspect disk queue/latency and correlate with MongoDB checkpoints, journaling, reads, and writes.
3. Evaluate filesystem and storage layout against the deployed MongoDB version and workload.
4. Detect capacity exhaustion or noisy-neighbor/storage-throttling behavior.
5. Avoid generic RAID/read-ahead prescriptions without platform evidence.
6. Do not resize/reformat production storage without explicit authorization.

## Output
- Storage Topology
- Capacity/Latency
- MongoDB I/O Correlation
- Bottleneck/Risk
- Recommended Action
