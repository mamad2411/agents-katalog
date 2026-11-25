---
name: performance-profiling
description: "Finds why code is slow by measuring first: sets a baseline, profiles the hot path, changes one thing and verifies the gain with repeatable numbers."
---

# Performance profiling

No change without a measurement before it and after it.

## Steps

1. Define the metric and target: wall time of one command, p95 latency, memory, queries per request. Write the exact command that produces it.
2. Build a repeatable benchmark: fixed input, warm-up run, at least 5 runs, report median and spread. Run it on an idle machine and with a production-like build (no debug mode).
3. Record the baseline and commit it to your notes.
4. Profile, do not guess. Use the language's tool: `node --cpu-prof` or `clinic`, `py-spy record` or `cProfile`, `go tool pprof`, `perf`, browser Performance panel, database `EXPLAIN ANALYZE`, request tracing. Find the top frames by self time and total time.
5. Name the hot path in one sentence with its share ("62% of time is JSON parsing inside loadConfig, called 4,000 times"). Ignore anything under 5%.
6. Pick the cheapest fix for the biggest share, in this order: do less work (cache, batch, skip), use a better algorithm or data structure, avoid repeated I/O, then micro-optimize. Change one thing.
7. Re-run the benchmark. Keep the change only if the gain exceeds the run-to-run spread. Check correctness with the test suite.
8. Repeat from step 4 until the target is met or the remaining gains are small.

## Rules

- Never trade correctness, readability or safety for a gain under 10% unless asked.
- Do not profile in a debug build.

## Report

Baseline, target, a table of changes with the measured gain of each, final numbers, and what remains.
