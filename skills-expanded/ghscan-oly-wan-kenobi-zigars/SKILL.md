---
name: zigars-performance-regression-investigator
description: Use when investigating Zig performance regressions, benchmark slowdowns, coverage budget drops, profiler captures, flamegraph comparisons, Samply or Tracy artifacts, performance gates, or performance claims that need evidence.
---

# Zigars Performance Regression Investigator

## Purpose

Use this skill when performance evidence must be designed, compared, and reported
without overstating what a benchmark, coverage map, or profiler capture proves.

## Workflow

1. Define the performance question: throughput, latency, allocation behavior,
   binary size, coverage budget, regression threshold, or profiler hypothesis.
2. Record context: command, target, optimize mode, toolchain, machine or CI
   environment, workload, baseline identity, current result identity, and
   threshold.
3. Use zigars performance tools according to the evidence needed:
   `zig_coverage` (mode=map/diff/budget),
   `zig_bench_discover`, `zig_bench_run`, `zig_bench_compare`,
   `zig_bench_regression_gate`, `zig_perf_budget_check`,
   `zig_profile_regression`, and `zig_perf_evidence_pack`.
4. For profiler work, preview or collect `zig_profile_plan`,
   `zig_profile_run`, `zig_flamegraph`, `zig_flamegraph_diff`,
   `zig_samply_record`, `zig_samply_summary`, `zig_tracy_plan`,
   `zig_tracy_capture`, and related artifact tools only within their apply and
   backend constraints.
5. Compare against a baseline before claiming regression or improvement.
6. Preserve artifacts with paths, hashes, skipped validation, backend status, and
   limitations.

## Claim Boundary

- A single benchmark run is weak evidence unless the project policy says
  otherwise.
- Coverage does not prove behavior; benchmark parsing does not prove workload
  representativeness; profiler output does not prove root cause alone.
- Backend unavailability must be reported, not hidden behind fallback claims.

## Finish

Report baseline, current evidence, threshold, regression decision, profiler or
coverage artifacts, skipped checks, and follow-up experiment.
