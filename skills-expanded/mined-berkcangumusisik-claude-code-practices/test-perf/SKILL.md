---
name: test-perf
description: Writes performance/benchmark tests for a function or endpoint
argument-hint: <file-path-or-function>
user-invocable: true
allowed-tools: Read Glob Edit Bash
effort: medium
---

## Generate Performance Tests

Target: **$ARGUMENTS**

1. Read the target file and understand what to benchmark.

2. Detect available tools:
```bash
cat package.json | grep -E "vitest|jest|benchmark|autocannon|k6"
```

3. Write benchmarks that measure:
   - Execution time under normal load
   - Memory allocation
   - Degradation under large inputs (10x, 100x, 1000x)
   - Comparison: current implementation vs a naive baseline

4. For HTTP endpoints: generate a load test script (autocannon or k6).

5. Add a performance budget comment:
```js
// Expected: < 10ms for typical input
// Regression threshold: fail if > 50ms
```

6. Place benchmark file in `bench/` or `__benchmarks__/` following project conventions.
