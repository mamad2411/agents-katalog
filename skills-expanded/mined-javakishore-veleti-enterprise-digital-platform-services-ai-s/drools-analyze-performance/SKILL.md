---
name: drools-analyze-performance
description: Analyze Drools rule-evaluation performance, constraint selectivity, network behavior, activation volume, fact volume, memory usage, session design, and rule hotspots. Use for high CPU, memory growth, slow rule execution, or scalability investigations.
---

# Analyze Performance

1. Establish workload size, fact volume, rule count, session type, and latency target.
2. Identify high-frequency rules, broad joins, Cartesian-like matches, expensive constraints, and excessive activations.
3. Inspect fact churn and repeated updates.
4. Correlate rule execution with CPU, memory, GC, and request latency where telemetry exists.
5. Compare representative workloads rather than optimizing synthetic edge cases alone.
6. Preserve business correctness while reducing evaluation work.

## Output
- Workload Profile
- Rule Hotspots
- Activation/Fact Findings
- Runtime Correlation
- Recommended Optimizations
