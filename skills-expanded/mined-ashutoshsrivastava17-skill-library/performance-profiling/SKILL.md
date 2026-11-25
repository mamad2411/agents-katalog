---
name: performance-profiling
description: >
  Analyze application performance bottlenecks — CPU, memory, I/O, query time,
  rendering. Produce optimization recommendations with expected impact.
  TRIGGER when: user says /performance-profiling, "profile performance", "why is it slow",
  "find bottlenecks", "optimize performance", or "performance analysis".
argument-hint: "[service, endpoint, or operation to profile]"
user-invocable: true
---

# Performance Profiling

You are a performance engineer analyzing application bottlenecks. Identify root causes, quantify impact, and recommend targeted optimizations.

## Process

### Step 1: Define the Problem

| Parameter | Description |
|-----------|-------------|
| Symptom | What is slow? (endpoint, page load, background job, query) |
| Magnitude | How slow? (current latency vs target) |
| When | Always, under load, intermittent, after a deploy? |
| Who notices | Users, monitoring, internal team |
| SLO impact | Is this breaching or approaching an SLO? |

### Step 2: Profiling Strategy

| Layer | Tool | What to Measure |
|-------|------|----------------|
| **Application** | Profiler (pprof, py-spy, async-profiler, Chrome DevTools) | CPU time, memory allocation, function call frequency |
| **Database** | Query analyzer (EXPLAIN, pg_stat, slow query log) | Query plans, full scans, lock contention, N+1 patterns |
| **Network** | APM traces, tcpdump, curl timing | Latency between services, DNS, TLS handshake, payload size |
| **Infrastructure** | Metrics (CPU, memory, disk I/O, network) | Resource saturation, throttling, swap usage |
| **Frontend** | Lighthouse, WebPageTest, browser DevTools | LCP, FID, CLS, bundle size, render blocking resources |

### Step 3: Root Cause Analysis

| Bottleneck Type | Indicators | Common Causes |
|----------------|-----------|--------------|
| **CPU-bound** | High CPU %, slow with no I/O waits | Inefficient algorithm, excessive serialization, regex backtracking |
| **Memory-bound** | High memory, GC pauses, OOM | Memory leaks, unbounded caches, large object graphs |
| **I/O-bound** | Low CPU, high wait times | Slow queries, network latency, disk reads, missing indexes |
| **Concurrency** | Intermittent slowness under load | Lock contention, thread pool exhaustion, connection pool limits |
| **Frontend** | High LCP, layout shifts | Large bundles, render-blocking resources, unoptimized images |

### Step 4: Optimization Recommendations

| # | Bottleneck | Current | Target | Optimization | Effort | Expected Impact |
|---|-----------|---------|--------|-------------|--------|----------------|
| 1 | [Issue] | [Current metric] | [Target] | [Specific fix] | Low/Med/High | [Expected improvement] |

## Output Format

```markdown
## Performance Profile: [Component]

### Problem Statement
[What is slow and how slow]

### Profiling Results
[Key findings from each layer profiled]

### Root Causes (Ranked by Impact)
1. [Primary bottleneck] — [evidence and data]
2. [Secondary bottleneck] — [evidence and data]

### Optimization Plan
| # | Fix | Expected Improvement | Effort | Priority |

### Verification Plan
[How to confirm optimizations worked — benchmarks, monitoring]
```

## Quality Checklist

- [ ] Problem is quantified with current and target metrics
- [ ] Profiling covers application, database, and infrastructure layers
- [ ] Root causes are backed by profiling data, not guesses
- [ ] Optimizations are ranked by impact-to-effort ratio
- [ ] Verification plan defines how to measure improvement

## Edge Cases

- **Intermittent performance issues**: Profile under load; check for GC pauses, lock contention, or noisy neighbors
- **Slow only in production**: Compare prod config, data volume, and infrastructure vs. dev environment
- **Frontend performance**: Separate server response time from client rendering issues
- **Database performance**: Always start with EXPLAIN — most backend slowness is query-related
