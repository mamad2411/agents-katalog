---
name: performance-profiling
description: Diagnose a measured performance problem in application code, database queries, or web runtime. Use when latency, throughput, CPU, memory, or query cost is the task.
---

# Performance profiling

Define the workload and record a baseline metric before optimizing. Use the project's available profiler, trace, query plan, or benchmark to find the actual bottleneck. Keep the test conditions stable and distinguish cold start from steady state.

Change the bottleneck with the least complexity that meets the target. Measure again under comparable conditions and report the before and after values, method, and limits. Check correctness and relevant regressions. Avoid performance claims based only on intuition or code appearance.
