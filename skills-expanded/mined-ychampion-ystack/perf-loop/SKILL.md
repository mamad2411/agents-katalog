---
name: perf-loop
description: >-
  Make code faster by measurement, not by guess: set a target, build a repeatable benchmark, profile to
  find where time or memory really goes, change one thing at a time, keep a table of numbers, and keep
  only changes that beat the noise. Use for "make this faster", "why is this slow", "optimize",
  "reduce memory", "speed up the build/tests/query", or a performance regression.
---

# Perf loop

Most guesses about where time goes are wrong. Measure, change one thing, measure again, keep the
numbers.

## When it applies

- Something is too slow or too memory-hungry and there is a number that would count as fixed.
- A regression: it got slower between two versions (for that, bisect it with the benchmark as the
  test; see step 2).

Skip it for code that runs once and already finishes in a time nobody minds.

## Procedure

### 1. Set the target

Write what is measured and what counts as done: "p95 of `GET /search` under 200 ms on the fixture
data", "build under 60 s", "peak memory under 1 GB". No target, no stopping point.

### 2. Build the benchmark

One command that runs the slow path on realistic input and prints the number. Make it repeatable:
same data, warm-up runs discarded, other load off the machine, at least 5 runs. Record the median and
the spread. The spread is the noise: a later change must beat it to count.

For a regression, the benchmark plus a threshold is a pass/fail command, so `git bisect run` can find
the commit.

### 3. Profile before changing anything

Use a real profiler for the stack (a CPU or sampling profiler, a flame graph, the database's query
plan via `EXPLAIN ANALYZE`, a heap snapshot, the build tool's timing report). Write down the top 3
hot spots with their share of the total. Optimizing something that takes 2% can save at most 2%.

### 4. Change one thing

Pick the biggest hot spot. Typical wins, in rough order of payoff: do less work (cache, skip, batch,
remove an N+1 query, add an index), a better algorithm or data structure, less allocation or copying,
then parallelism. Make one change.

### 5. Measure and record

Run the benchmark and the tests. Add a row:

```
| # | Change                         | Median  | Spread | vs base | Tests | Kept |
| 0 | baseline                       | 840 ms  | ±30    | -       | pass  | -    |
| 1 | index on orders.user_id        | 310 ms  | ±12    | -63%    | pass  | yes  |
| 2 | memoize price lookup           | 305 ms  | ±15    | -1%     | pass  | no (noise) |
```

Keep a change only if it beats the noise and the tests pass. Revert the rest; they are complexity
with no payoff.

### 6. Repeat or stop

Re-profile after each kept change: the hot spots move. Stop at the target, or when the top hot spot
is something you can't change (network, disk, an external service), and say so.

## Rules

- No optimization without a number before and after.
- One change per measurement.
- Correctness first: tests pass on every kept row.
- Report the table, the target, and whether it was met.
