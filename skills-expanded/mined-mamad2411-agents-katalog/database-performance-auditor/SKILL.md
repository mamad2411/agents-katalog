---
name: database-performance-auditor
description: Audit database performance and capacity. Use when a system is slow
  or when planning DB growth.
metadata:
  tags: database, performance, auditor
---

# Database Performance Auditing

## Use this skill when
- Investigating slowness from the DB angle
- Reviewing indexes, queries, and planning
- Capacity and bottleneck analysis

## Do not use this skill when
- Schema design
- Application code profiling beyond queries

## Instructions
1. Pull the slow-query log; explain the costliest.
2. Check index usage, bloat, vacuum/statistics health.
3. Review connection/pool behavior and locks.
4. Quantify: query latency percentiles, throughput, contention.
5. Identify capacity limits: disk, memory, connections.
6. Prioritize fixes by impact/effort.
7. Verify improvements before/after.

## Output Format
- Query | bottleneck | evidence | fix | impact

## Common Mistakes
- Anecdotal “it’s slow” without baselines
- Missing index bloat/stats angles
- Only app-side answers

## References
- `references/audit-checklist.md` – Evidence-gathering steps, plan-reading, quick wins, and baseline template
