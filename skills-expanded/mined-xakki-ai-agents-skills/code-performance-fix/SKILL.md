---
name: code-performance-fix
description: 'Measure and improve performance (web vitals, benchmarks, data access) using representative workloads and raw-sample evidence. Use for slow pages, benchmark comparisons or index proposals. RU: производительность, оптимизация скорости, бенчмарк.'
disable-model-invocation: true
---

# Performance optimization and benchmarks

Establish the user-visible goal, baseline, affected paths, workload and constraints before choosing an optimization. Use representative field data when available and controlled synthetic measurements for reproducible diagnosis; report missing samples and measurement limits rather than treating proxy metrics as proof of user experience.

For web experiences evaluate the relevant current Core Web Vitals (LCP, INP, CLS), network and server latency, payloads and runtime work; confirm current definitions and thresholds from the authoritative tool documentation. Measure the actual bottleneck before choosing rendering, caching, code-splitting, asset, database or infrastructure changes; server rendering, preloading, a CSS naming convention or a service worker is not a universal win. Preserve correctness, accessibility, security and behavior; when caching or data partitioning changes, verify freshness, invalidation and authorization boundaries.

## Benchmarks that inform a decision

Define the question, units, conditions, acceptance criteria, sampling plan, execution budget and permitted resource effects before running, and verify the trials compare the intended builds, workloads, inputs, configuration and constraints. A benchmark runner's availability does not authorize production tests, service changes or broad cleanup. Retain raw per-trial observations and command outcomes; verify schema, units, valid sample counts, failures and substitutions; recompute aggregates from raw values with a stated rounding policy; distinguish mean from worst observed value; instrument readiness, latency or shutdown directly, because one favorable metric cannot establish an unrelated criterion. Compare the same workload and environment before and after, and report method, sample size, provenance, conditions, results, limitations and unmeasured criteria, keeping measurements separate from interpretation. Preserve failures from noisy or incomplete runs instead of treating an exit-zero wrapper or a subset as acceptance. Deploy, change infrastructure, run expensive load tests or clean up only within the authorized scope.

For data-access changes or index proposals use [data-access performance](references/data-access-performance.md).
