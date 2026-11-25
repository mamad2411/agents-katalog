---
name: mongodb-analyze-wiredtiger
description: Analyze MongoDB WiredTiger storage-engine behavior including cache pressure, eviction, checkpoints, tickets/concurrency, compression, dirty data, history store, and disk interaction. Use for memory, eviction, checkpoint, or storage-engine incidents.
---

# Analyze WiredTiger

1. Inspect WiredTiger cache usage, dirty bytes, eviction behavior, checkpoints, and relevant concurrency signals.
2. Correlate cache pressure with host memory and filesystem cache behavior.
3. Inspect storage latency before attributing stalls to WiredTiger.
4. Identify sustained eviction/checkpoint pressure and workload patterns.
5. Avoid arbitrary cache-size or engine tuning without workload evidence.
6. Treat undocumented/internal parameters as high risk.

## Output
- Cache/Eviction State
- Checkpoint Findings
- Memory/Disk Correlation
- Bottleneck Assessment
- Recommended Action
