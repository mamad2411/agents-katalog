---
name: perf-audit
description: Finds performance bottlenecks in code - N+1 queries, unnecessary re-renders, blocking operations
argument-hint: [file-or-directory]
user-invocable: true
allowed-tools: Read Grep Glob
effort: medium
---

## Performance Audit

Target: **$1** (or `src/` if not specified)

### Database / API
- N+1 query patterns (loop with query inside)
- Missing indexes (queries on non-indexed columns)
- Fetching all fields when only a few are needed (`SELECT *`)
- Sequential async calls that could be parallel (`Promise.all`)

### Frontend
- Expensive computations on every render (should use `useMemo`)
- Event listeners added without cleanup
- Large imports not code-split (`import * from`)
- Images without lazy loading or size hints

### General
- Synchronous operations that block the event loop
- Memory leaks (closures holding references)
- Redundant data transformation loops (can be combined)
- Missing caching for expensive operations

---

For each finding:
1. Show the problematic code
2. Explain the performance impact
3. Show the fix
4. Estimate improvement (rough order of magnitude)

Prioritize by impact: fix things that run in hot paths (request handlers, render functions, loops) first.
