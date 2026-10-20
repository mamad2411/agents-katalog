---
name: code-performance
description: Profile and optimize application code with measured before/after numbers and a perf report. Use when the user has slow code, asks to optimize code, fix performance, a memory leak or high CPU, or speed up an API, job or UI.
---

# Code Performance (application code, not DB internals)

Make code measurably faster or leaner without changing behaviour: goal → baseline → hotspot → biggest fix first → re-measure → guard.

## Inputs
- Code (files, snippet, repo path), plus any evidence: profiler output, flame graph, traces, APM screenshots, load-test results, GC/heap stats, Lighthouse report
- The symptom: "endpoint p95 is 2 s", "job takes 3 h", "pod OOM", "CPU 90 %", "page INP 600 ms"
- Constraints: SLA, hardware, data volume, what must not change (API contract, output format)

No numbers given: say so, run `scripts/perf_smells.py` for candidates, and give the exact commands to measure the baseline. Label every unmeasured claim **Estimate**.

## Defaults (state them in one line)
| Setting | Default if not stated | Ask only if |
|---|---|---|
| Goal metric | Backend: p95 latency at stated load; batch: wall time; UI: LCP / INP / bundle KB | Several metrics conflict (latency vs memory) |
| Environment | Release build, production-like data volume, warm run | User only has Debug / tiny data: warn it misleads |
| Stack / version | Detected from files; else .NET 8, Java 21 + Boot 3, Python 3.12, React 18/19, Angular 17+ | Version changes the fix (e.g. virtual threads, zoneless) |
| Scope | The slow path the user names + its callees | "Whole app": ask for the top 1-3 slow operations |
| Change size | Smallest change that removes the hotspot | Fix needs an API or schema change |

## Which reference to read
| Code / symptom | Read |
|---|---|
| C#, ASP.NET Core, EF Core, BenchmarkDotNet, dotnet-counters/trace | `references/dotnet-perf.md` |
| Java, Spring Boot, JPA/Hibernate, JFR, JMH, GC, virtual threads, HikariCP | `references/java-perf.md` |
| Python, FastAPI/Django, pandas/NumPy, asyncio, cProfile/py-spy | `references/python-perf.md` |
| React, Angular, Core Web Vitals, bundle size | `references/frontend-perf.md` |
| Any stack: loops with I/O, N+1, O(n²), caching, logging, pagination | `references/common-antipatterns.md` (always skim) |
| Slow SQL statement, execution plan, index, locking | Hand off to **sql-performance-tuning** (send captured SQL + timings) |

## Steps
1. **Define the goal.** One metric, target and load (e.g. "p95 ≤ 300 ms at 200 RPS"). Fill section 1 of `templates/perf-report-template.md`.
2. **Baseline.** Use the stack's profiler/benchmark from the reference file. Record numbers, environment and method. If the user can't run it now, give the exact commands and mark numbers TBD.
3. **Scan for candidates.** `python3 scripts/perf_smells.py src/ --min MED` (heuristic; output is `file:line SEV rule`). Candidates are not findings until the profile or code reading confirms them.
4. **Find the hotspot.** Rank by measured share of the goal metric (CPU %, wall time, allocations, query count). Classify: algorithmic (Big-O), I/O pattern (N+1, chatty, sequential awaits), concurrency (sync-over-async, blocking, locks), memory (allocations, leaks, unbounded caches), rendering (re-renders, bundle, long tasks), or DB-side (hand off).
5. **Fix the biggest cost first.** Prefer algorithmic and I/O-pattern fixes over micro-optimizations. State Big-O before → after. Keep public behaviour, ordering, error handling and transactions identical.
6. **Prove behaviour unchanged.** Existing tests must pass; add a characterization test if coverage is missing.
7. **Re-measure** with the same method and environment. Report Delta % = (after − before) / before × 100. Drop changes that don't move the goal metric.
8. **Guard it.** Add a benchmark (BenchmarkDotNet, JMH, pytest-benchmark), a query-count test, or a CI budget (Lighthouse CI, Angular budgets, size-limit).
9. **Report** with the template; run the self-check.

## Rules
- Never optimize without evidence: a profile, trace, benchmark, or a proven Big-O problem. No evidence → **Estimate** label + measurement plan.
- Measure before and after in the same environment, build (Release) and data volume; use p95/p99, not averages alone.
- Behaviour stays identical: same outputs, ordering, errors, side effects; tests must pass.
- Algorithmic wins (O(n²) → O(n), N+1 → 1 query, sequential → bounded parallel) before micro-optimizations.
- Don't trade readability for speed without a measured win on the goal metric (≥ ~5 % or an SLA breach fixed).
- Bound everything you add: caches (size + TTL), parallelism (max degree), batches (chunk size), pools.
- `memo`/`useMemo`/`Span`/`ArrayPool`/compiled queries only where the profiler shows the cost.
- DB plan, index, statistics or locking issues → sql-performance-tuning; pure readability → refactoring; PR verdict → code-review.
- Never invent measurements; show units and how each number was obtained.

## Self-check
- [ ] Goal metric, target and load stated
- [ ] Baseline has numbers + method (or is marked TBD with exact commands)
- [ ] Each hotspot cites file:line/function and its measured share
- [ ] Big-O before → after given for algorithmic changes
- [ ] Fixes ordered by impact; no unmeasured micro-optimizations
- [ ] Behaviour unchanged; tests named
- [ ] After numbers use the same method; Delta % computed correctly
- [ ] Benchmark/guard added; caches/parallelism bounded
- [ ] DB-side issues handed off; scanner output treated as candidates, not facts

## Output
1. **Assumptions** line (stack, environment, goal).
2. Report per `templates/perf-report-template.md`: Goal, Baseline, Hotspots table, Changes, After, Delta %, Risks, Benchmark added.
3. **Code** for each change (file path heading, before → after), plus the benchmark/test code.
4. **Needs input / next steps**: numbers to capture, handoffs.

## Files
| Path | Purpose |
|---|---|
| `scripts/perf_smells.py` | Stdlib heuristic scanner (.cs .java .py .ts .tsx .js); exit 1 if any HIGH |
| `templates/samples/bad_perf.cs`, `templates/samples/BadPerf.java`, `templates/samples/bad_perf.py`, `templates/samples/bad_perf.ts` | Deliberately bad samples: each must trigger HIGH findings |
| `templates/samples/clean_perf.cs`, `templates/samples/clean_perf.py` | Clean samples: must report 0 HIGH / 0 MED |
| `evals/test-cases.md` | Trigger and quality test cases; rerun after every edit |

Scanner false positives: `.Contains` on a set, `.Result` on a non-Task type, `in` on a set/str. False negatives: lazy-loading N+1, calls hidden in helpers. Always confirm.
