---
name: performance-profiling
description: Finds and fixes backend and application performance problems by measuring first - define the target metric, reproduce under realistic load, profile CPU, memory, I/O and locks, fix the biggest bottleneck, re-measure, and add a regression guard. Use when code or a service is slow, p95 or p99 latency is high, CPU or memory usage is too high, throughput is too low, startup is slow, or the user asks to optimize, profile or benchmark. Not for page-load tuning (use web-performance) or tuning a single SQL query (use sql-optimization).
license: MIT
---

# Performance Profiling

Never optimize what you have not measured. Profile, fix the largest bottleneck, measure again under the same conditions. A change without a before/after number is a guess.

## When to use

- A request, job, function or command is slower than it should be.
- Tail latency (p95/p99) is high or spiky, even if the average looks fine.
- CPU, memory, GC time, or cloud cost is too high.
- Throughput tops out before hardware does.
- The user asks to "make it faster", profile, or benchmark something.

Not for: browser page-load and rendering (web-performance), a single slow SQL query (sql-optimization), or capacity planning without a concrete bottleneck.

## Workflow

1. **State the problem as a number.** Metric, current value, target, conditions. Example: "p99 of `POST /orders` is 1.8 s at 300 req/s on staging; target under 400 ms." If the user gives no target, propose one and confirm it.
2. **Pick the right metric** (table below). Use percentiles, never the mean, for latency.
3. **Reproduce in a production-like setup.** Release/optimized build, realistic data volume and shape, same config and dependency versions, no debugger attached, JIT warmed up. Record a baseline over several runs and note the spread.
4. **Find what bounds you** before opening a profiler: CPU, memory/GC, I/O, locks, or a downstream dependency. Use traces or APM first if they exist: is the time even spent in this process?
5. **Profile with the right tool** for the bound and the stack. See [references/profilers.md](references/profilers.md). Prefer low-overhead sampling profilers.
6. **Form one hypothesis and make one change.** Fix the widest bar in the profile first. Leave code that takes 1% of time alone.
7. **Re-measure under identical conditions.** Compare distributions (several runs), not single numbers. Confirm the profile changed the way you expected.
8. **Check correctness.** Tests pass; output is identical; no new race conditions or stale-cache bugs.
9. **Add a regression guard** (benchmark in CI, load test, or alert) so the win stays.
10. **Report** a before/after table, what changed, why it helped, and any trade-offs (memory for speed, staleness for speed, complexity).

## Choose the metric

| Goal | Measure | Notes |
|---|---|---|
| User-facing latency | p50, p95, p99 (and max) per endpoint | Mean hides tail problems. |
| Throughput | Requests or items per second at a fixed latency SLO and error rate | Throughput without a latency bound is meaningless. |
| Memory | RSS, live heap after GC, allocation rate, GC pause time | Steady growth over hours suggests a leak. |
| Startup | Time to ready / first successful request | Measure cold and warm separately. |
| Batch / CLI | Wall-clock time and cost per item | Use `hyperfine` for command-line comparisons. |
| Cost | CPU-seconds or dollars per request | Useful when latency is already fine. |

## Find the bound

| Symptom | Likely bound | Next step |
|---|---|---|
| CPU near 100% of available cores; latency grows with load | CPU | CPU sampling profiler, flame graph |
| CPU low but latency high | Waiting: I/O, locks, downstream calls, pool exhaustion | Traces, wall-clock/off-CPU profile, thread dump, pool metrics |
| Memory grows steadily and never drops | Leak or unbounded cache/queue | Compare two heap snapshots taken minutes apart |
| High GC time, frequent pauses | Allocation pressure | Allocation profiler |
| Periodic latency spikes | GC pauses, scheduled jobs, cache expiry stampede, noisy neighbour | Correlate spike times with GC logs, cron, cache TTLs |
| Only p99 is bad | Contention, GC, cold caches, retries, one slow dependency | Look at slowest traces, not averages |
| Node.js latency rises for all requests at once | Event-loop blocking | Event-loop delay metric, CPU profile |
| .NET or Java requests queue while CPU is low | Thread pool starvation from blocking calls in async code | Thread-pool queue length, thread dump |

## Reading a flame graph

- Width is the share of samples (time). The x-axis is not time order.
- The y-axis is stack depth; the top edge is where the CPU actually was.
- Look for wide plateaus near the top: that is self time worth optimizing.
- A CPU profile only shows on-CPU time. If the process waits (I/O, locks), use a wall-clock or off-CPU mode, or traces.
- Compare a before and after flame graph of the same workload to confirm the fix.

## Common wins (check in this order)

| Problem | How to spot it | Fix |
|---|---|---|
| N+1 queries | Many near-identical queries per request in logs or a trace waterfall | Batch, join, eager-load, or a data loader |
| Missing index or bad query plan | Slow query log, DB time dominates traces | See sql-optimization |
| Chatty network | Many sequential calls in one trace | Batch requests, run independent calls in parallel, cache |
| Blocking I/O on a hot path | Event-loop lag (Node), thread-pool starvation (.NET/Java), sync calls inside async code | Use async APIs end to end; move CPU work to workers |
| Serialization overhead | JSON encode/decode wide in the profile | Smaller payloads, avoid serializing twice, faster serializer |
| Allocations in hot loops | Allocation profile, high GC time | Preallocate, reuse buffers, avoid boxing and repeated string concatenation |
| Lock contention | Threads blocked, low CPU, wide lock frames in wall-clock profile | Shrink critical sections, shard state, use concurrent data structures |
| Repeated expensive work | Same computation or remote call with same inputs | Memoize or cache with a size bound, TTL and invalidation; prevent stampedes |
| Wrong algorithm or data structure | Nested loops over large inputs, linear lookups in a loop | Hash maps/sets, sorting once, indexing |
| Logging on the hot path | Formatting or I/O of logs visible in the profile | Lower level, check level before formatting, sample |
| Pool sizing | Time spent waiting for a connection or worker | Right-size the pool; never above what the database can serve |
| Regex backtracking | One regex dominates CPU on certain inputs | Anchor and simplify the pattern, or use a linear-time engine |

## Benchmarking properly

- Use a real harness, not a stopwatch loop:

  | Stack | Harness |
  |---|---|
  | Java/Kotlin | JMH |
  | C#/.NET | BenchmarkDotNet (add `[MemoryDiagnoser]` for allocations) |
  | Python | `pyperf`, `pytest-benchmark`, or `python -m timeit` for one-liners |
  | Go | `go test -bench=. -benchmem -count=10`, compare runs with `benchstat` |
  | Rust | `criterion` |
  | JS/TS | `tinybench` or `mitata` |
  | Any CLI | `hyperfine --warmup 3 'old-cmd' 'new-cmd'` |

- Warm up before measuring (JIT, caches, connection pools).
- Run many iterations and several processes; report median and spread. Treat differences inside the noise as no difference.
- Benchmark optimized builds only (`--release`, `-c Release`, production `NODE_ENV`).
- Guard against dead-code elimination and constant folding: consume results (JMH `Blackhole`, return values).
- Use realistic inputs. Sorted, tiny, or always-cached data gives misleading results.
- Keep the machine quiet: no other heavy processes, power plugged in, same hardware for before and after.
- A microbenchmark proves a local speedup; only an end-to-end measurement proves user impact.

## Load testing

- Use a load generator such as k6, wrk2, vegeta, hey or Locust against a staging environment.
- Prefer open-model (fixed arrival rate) load, e.g. k6's `constant-arrival-rate` executor or wrk2's `-R`. Closed-loop tools that wait for each response under-report latency when the system slows down (coordinated omission).
- Ramp up gradually and record where latency or errors break the SLO; that is the real capacity.

## Safety

- Do not run load tests against production or shared environments without explicit confirmation from the user.
- Ask before attaching a profiler to a production process. Prefer low-overhead samplers. Heap dumps can pause the process and contain secrets and personal data: treat dump files as sensitive and never commit or share them.
- Never trade correctness for speed silently (skipping validation, weakening consistency, unbounded caches). Call out every such trade-off.

## Anti-patterns

- **Optimizing by intuition** — the real bottleneck is rarely where you guess. Profile first.
- **Reporting the mean** — averages hide the tail users feel.
- **Benchmarking debug builds or cold JITs** — numbers will not transfer.
- **Changing several things at once** — you cannot tell which change helped or hurt.
- **Micro-optimizing a function that is 1% of the profile** — no visible effect, more complexity.
- **Caching without bounds or invalidation** — trades a latency problem for a memory or correctness problem.
- **Tiny test data** — hides N+1s, missing indexes and O(n²) code.
- **Declaring victory on one run** — noise can exceed the improvement.

## Done when

- [ ] Before and after numbers exist for the target metric under the same conditions, over several runs.
- [ ] The target is met, or the report explains what limits further gains.
- [ ] A new profile shows the bottleneck moved or shrank.
- [ ] Tests pass and behaviour is unchanged.
- [ ] A regression guard (benchmark, load test, or alert) is in place.
- [ ] Trade-offs are written down in the PR or a code comment.

## References

- [references/profilers.md](references/profilers.md) — read when choosing or running a profiler, heap analyzer, tracer or load generator for a specific language or OS.
