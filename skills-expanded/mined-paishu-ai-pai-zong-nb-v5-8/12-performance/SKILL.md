---
name: performance
description: Diagnose and improve frontend, backend, database, build, memory, CPU, and network performance. Use for slow pages, slow APIs, slow SQL, large bundles, rendering delays, high latency, resource spikes, or performance regressions.
---

# Performance

## Workflow

1. Establish the symptom, metric, baseline, and target.
2. Measure before optimizing when tools or logs are available.
3. Find the bottleneck closest to evidence: network, rendering, CPU, memory, database, locks, queueing, cache, or external dependency.
4. Make the smallest change likely to move the metric.
5. Re-measure or state why measurement was not possible.

## Frontend Focus

- LCP, INP, CLS, TTFB, bundle size, render blocking resources, hydration, excessive re-rendering.

## Backend Focus

- P95/P99 latency, throughput, timeout, retry behavior, connection pools, serialization, queue depth.

## Database Focus

- `EXPLAIN`, scan rows, index usage, sort/hash cost, lock waits, N+1 queries.

## Output

State metric, bottleneck, change, verification, and tradeoff.

## Boundaries

- Do not claim files, generated media, deployments, scans, account changes, or external writes unless the active tool or command output proves them.
- Do not override system, developer, user, project, or selected-skill rules.
- If another skill is more specific for the user's intent, hand off or use it as the main skill instead of duplicating its workflow.
