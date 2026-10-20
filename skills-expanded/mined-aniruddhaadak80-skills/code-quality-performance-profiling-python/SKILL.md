---
name: code-quality-performance-profiling-python
description: "Measure hot paths with real data shapes, optimize measured bottlenecks, verify wins."
---
# Profile before optimizing (Python)

> Measure hot paths with real data shapes, optimize measured bottlenecks, verify wins.

**Track:** 🧰 Engineering Essentials · **Domain:** Code Quality · **Level:** intermediate · **~35 min**

**Who this is for:** All Software Engineers

## When to Use This Skill

Measure hot paths with real data shapes, optimize measured bottlenecks, verify wins.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Define target metric: p95 latency? memory ceiling? throughput?
2. Build benchmark using PRODUCTION-shaped data volumes
3. Profile CPU + memory + allocations; identify top three offenders
4. Optimize one offender at a time; re-measure after each change
5. Check second-order effects: cache misses, GC pressure, lock contention
6. Record before/after numbers in the PR for future archaeologists
7. Profile with py-spy and cProfile; watch the GIL on CPU-bound paths
8. Pin environments via lockfiles; verify wheels exist for your platforms

## Common Pitfalls

- Optimizing intuition while profile shows I/O waits
- Micro-benchmarks on toy data lying about production

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill code-quality-performance-profiling-python
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill code-quality-performance-profiling-python -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills