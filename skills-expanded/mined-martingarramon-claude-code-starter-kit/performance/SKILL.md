# Performance — Profiling and Optimization

## When to Use
- Application is slow, memory-hungry, or unresponsive under load
- After generating large codebases with Claude — AI code often has optimization gaps
- Before scaling to production
- When profiling reveals unclear bottlenecks

## Core Principle
Measure first, then optimize targeted bottlenecks. Use Claude to interpret profiling data, diagnose root causes, and suggest data-driven improvements. Never optimize without evidence.

## Process
1. **Profile baseline** — Run profilers (cProfile, Chrome DevTools, Go pprof, etc.). Have Claude interpret results and highlight hot spots.
2. **Identify bottlenecks** — Decompose by type: CPU, memory, I/O, network, database. Use Claude for hypothesis generation.
3. **Apply targeted fixes** — Implement caching, algorithmic improvements, query optimization. Have Claude generate code variants.
4. **Benchmark changes** — Re-profile and compare. Iterate until goals are met.
5. **Document tradeoffs** — Note any impacts on readability, memory, or maintainability.

## Output Format
- Profiling summary (key metrics before/after)
- Optimization changes (code diffs with explanations)
- Tradeoff analysis
- Future recommendations

## Rules
- Always measure before AND after. No gut-feel optimization.
- 80/20 rule: fix the top 20% causing 80% of issues.
- Validate with real benchmarks, not Claude's estimates.
- Consider the full stack (code, DB, network, infrastructure).
- Readability matters — don't sacrifice clarity for 5% gains.

## Anti-Patterns
- Premature optimization (wasting time on non-issues)
- Optimizing without profiling data (solving the wrong problem)
- Making code unreadable for marginal gains
- Ignoring scalability (works at 100 users, dies at 10K)
- Benchmarking in unrealistic environments
