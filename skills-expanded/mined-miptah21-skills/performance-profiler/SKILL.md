---
name: performance-profiler
description: Performance bottleneck analysis and optimization. Use when apps are slow, P99 latency exceeds SLA, memory leaks suspected, bundle size increased, or preparing for traffic spikes. Covers Node.js, Python, and Go.
---

# Performance Profiler

**Category:** Performance Engineering

## Overview

Systematic performance profiling for web applications. Identifies CPU, memory, and I/O bottlenecks; analyzes bundle sizes; optimizes database queries; detects memory leaks; and runs load tests. Always measures before and after.

## When to Use

- App is slow and you don't know where the bottleneck is
- P99 latency exceeds SLA
- Memory usage grows over time (suspected leak)
- Bundle size increased after adding dependencies
- Preparing for a traffic spike
- Database queries taking >100ms

## Golden Rule: Measure First

```
Wrong: "I think the N+1 query is slow, let me fix it"
Right: Profile → confirm bottleneck → fix → measure again → verify improvement
```

**Always establish baseline BEFORE any optimization.**

## Quick Win Checklist

```
Database
□ Missing indexes on WHERE/ORDER BY columns
□ N+1 queries (check query count per request)
□ Loading all columns when only 2-3 needed (SELECT *)
□ No LIMIT on unbounded queries
□ Missing connection pool

Node.js
□ Sync I/O (fs.readFileSync) in hot path
□ JSON.parse/stringify of large objects in hot loop
□ Missing caching for expensive computations
□ No compression (gzip/brotli) on responses
□ Dependencies loaded in request handler (move to module level)

Bundle
□ Moment.js → dayjs/date-fns
□ Lodash (full) → lodash/function imports
□ Static imports of heavy components → dynamic imports
□ Images not optimized / not using next/image
□ No code splitting on routes

API
□ No pagination on list endpoints
□ No response caching (Cache-Control headers)
□ Serial awaits that could be parallel (Promise.all)
□ Fetching related data in a loop instead of JOIN
```

## Profiling Recipes

### Node.js CPU Profiling

```bash
# Generate CPU profile
node --prof app.js
# Process the log
node --prof-process isolate-*.log > profile.txt

# Using clinic.js
bunx clinic doctor -- node app.js
bunx clinic flame -- node app.js
```

### Node.js Memory Profiling

```bash
# Heap snapshot
node --inspect app.js
# Connect Chrome DevTools → Memory tab → Take snapshot

# Track heap growth
node --max-old-space-size=512 --trace-gc app.js
```

### Bundle Analysis

```bash
# Next.js
ANALYZE=true next build

# Webpack
bunx webpack-bundle-analyzer stats.json

# Package size check
bunx bundlephobia-cli <package-name>
```

### Database Query Analysis

```sql
-- PostgreSQL
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- Check slow queries
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 20;
```

### Load Testing with k6

```javascript
// load-test.js
import http from 'k6/http'
import { check, sleep } from 'k6'

export const options = {
  stages: [
    { duration: '30s', target: 20 },   // Ramp up
    { duration: '1m', target: 20 },    // Sustain
    { duration: '10s', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<200'], // 95% under 200ms
  },
}

export default function () {
  const res = http.get('http://localhost:3000/api/health')
  check(res, { 'status 200': (r) => r.status === 200 })
  sleep(1)
}
```

```bash
k6 run load-test.js
```

## Before/After Template

```markdown
## Performance Optimization: [What You Fixed]

### Problem
[1-2 sentences: what was slow, how observed]

### Root Cause
[What the profiler revealed]

### Baseline (Before)
| Metric | Value |
|--------|-------|
| P50 latency | 480ms |
| P95 latency | 1,240ms |
| P99 latency | 3,100ms |
| RPS @ 50 VUs | 42 |
| Error rate | 0.8% |

### Fix Applied
[What changed]

### After
| Metric | Before | After | Delta |
|--------|--------|-------|-------|
| P50 | 480ms | 48ms | -90% |
| P95 | 1,240ms | 120ms | -90% |
| P99 | 3,100ms | 280ms | -91% |
| RPS | 42 | 380 | +804% |
```

## Common Pitfalls

- **Optimizing without measuring** — you'll optimize the wrong thing
- **Testing with dev data** — profile against production-like volumes
- **Ignoring P99** — P50 can look fine while P99 is catastrophic
- **Premature optimization** — fix correctness first
- **Not re-measuring** — always verify the fix actually helped
