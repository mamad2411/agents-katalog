---
name: performance-optimization
description: >-
  Measure-first performance optimization that targets Core Web Vitals,
  runtime efficiency, and scalability. Covers profiling workflows, bundle
  analysis, lazy loading, caching strategies, database query optimization,
  and anti-pattern detection. Every optimization is driven by data, not
  instinct.
---

# Performance Optimization

## Overview

Performance is a feature with measurable SLAs. The web has established three
core metrics that correlate directly with user satisfaction and business
outcomes — **LCP** (loading), **FID** (interactivity), **CLS** (visual
stability) — and any application with server-side or client-side runtime
has analogous internal metrics: p50/p95/p99 latency, throughput, memory
footprint, and GC pressure.

The cardinal rule of optimization: **measure first**. Without a baseline,
you cannot know whether your change improved, hurt, or left performance
unchanged. Most hunches about performance bottlenecks are wrong. Profile
before you act.

**Core Web Vitals targets:**
| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP (Largest Contentful Paint) | ≤2.5s | 2.5s–4.0s | >4.0s |
| FID (First Input Delay) | ≤100ms | 100ms–300ms | >300ms |
| CLS (Cumulative Layout Shift) | ≤0.1 | 0.1–0.25 | >0.25 |
| INP (Interaction to Next Paint) | ≤200ms | 200ms–500ms | >500ms |
| TTFB (Time to First Byte) | ≤800ms | 800ms–1800ms | >1800ms |

## When to Use

- Core Web Vitals are in the "Needs Improvement" or "Poor" range
- Page load time exceeds 3 seconds for any critical page
- Database query latency exceeds 100ms p50 or 500ms p99
- API response time exceeds 200ms p50 or 1000ms p99
- Bundle size exceeds 250KB (gzipped) for initial load
- Memory usage grows monotonically (leak suspected)
- CPU profiling reveals functions consuming >5% of total time
- Render pipeline takes >16ms per frame (60fps target missed)
- Lighthouse or PageSpeed Insights score drops below 90
- User-reported slowness, spinner fatigue, or janky scrolling

## Process

### Step 1: Establish Baseline Measurements

Never optimize without a baseline. You need a number before and a number after.

**Measurement sources:**

| Source | What It Measures | When to Use |
|--------|-----------------|-------------|
| **Lighthouse / PageSpeed Insights** | Core Web Vitals, best-practice audits | CI gate, pre-deploy check |
| **Web Vitals library** (web-vitals) | Real-user monitoring (RUM) | Production monitoring |
| **Chrome DevTools Performance tab** | JS profiling, rendering, layout, paint | Local debugging |
| **Chrome DevTools Network tab** | Waterfall, blocking, caching, compression | Local debugging |
| **Bundle analysis** (webpack-bundle-analyzer, vite-bundle-visualizer) | Module sizes, duplication | Build pipeline |
| **Server-side profiling** (flamegraphs, async-profiler, py-spy) | Server CPU, allocation, blocking | Backend debug |
| **APM tools** (Datadog, New Relic, Grafana) | Request latency, throughput, error rate | Production |
| **Database query profiling** (EXPLAIN ANALYZE, pg_stat_statements, slow query log) | Query plans, index usage, seq scans | Backend debug |

**Exit criteria:** A documented baseline: LCP, FID, CLS, bundle size gzipped,
p50/p99 API latency, and database slow-query count. Attach a Lighthouse report
screenshot or JSON export.

### Step 2: Identify the Bottleneck

Use the measurement data to find the single largest contributor to the
performance problem. The Pareto principle applies: 20% of the code causes
80% of the slowdown.

**Common bottleneck categories (in order of impact):**

1. **Network:** Large bundles, unoptimized images, lacking compression,
   too many requests, no CDN, no HTTP/2 or HTTP/3. Fix: compress, code-split,
   lazy-load, serve from CDN, preconnect to origins.
2. **Rendering:** Layout thrash, forced reflows, large DOM size, complex CSS,
   unoptimized animations. Fix: batch DOM writes, use `transform` and `opacity`
   for animations, virtualize long lists, avoid expensive selectors.
3. **JavaScript:** Long tasks (>50ms blocking main thread), excessive GC,
   unoptimized loops, memory leaks. Fix: code-split, defer non-critical JS,
   use Web Workers for pure computation, debounce event handlers.
4. **Database:** N+1 queries, missing indexes, full table scans, lock
   contention, oversized result sets. Fix: eager load, add indexes, paginate,
   cache frequent queries, read replicas.
5. **Server:** CPU-bound handlers, synchronous I/O in async context, slow
   serialization, connection pool exhaustion. Fix: profile with flamegraphs,
   offload CPU work, add caching, tune pool sizes, increase replicas.

**Exit criteria:** A single bottleneck category identified with supporting
evidence from baseline measurements.

### Step 3: Apply Targeted Optimization

Choose the optimization technique that directly addresses the identified
bottleneck. Apply one change at a time and re-measure.

**Optimization catalog:**

| Bottleneck | Technique | Expected Impact |
|------------|-----------|-----------------|
| Large JS bundle | Code splitting (dynamic imports), tree shaking, remove dead code | 20-50% bundle reduction |
| Large images | WebP/AVIF, responsive images (srcset), lazy loading (loading=lazy) | 50-80% image bytes reduction |
| Uncompressed assets | Brotli or Gzip compression | 60-80% text asset reduction |
| Too many requests | Bundling, HTTP/2 multiplexing, preconnect | Consolidated connections |
| Slow LCP | Preload hero image, optimize TTFB, reduce render-blocking resources | Sub-second LCP improvement |
| Layout shift | Explicit dimensions on images/embeds, avoid late-injecting content above fold | CLS near zero |
| Long tasks | Defer non-critical JS, break up tasks with yield/requestIdleCallback | Improved FID/TBT |
| N+1 queries | Eager loading (SELECT .. IN), GraphQL dataloader, batch endpoints | 10-100x query reduction |
| Missing indexes | CREATE INDEX, composite indexes for WHERE+ORDER+JOIN | 10-1000x query speedup |
| Repeated I/O | In-memory cache (Redis, Memcached), HTTP caching (Cache-Control, ETag) | 10-100x latency reduction |
| Expensive computation | Memoization, Web Workers (client), job queue (server) | Offloaded blocking |
| Unoptimized fonts | font-display: swap, subset fonts, preload font-face | Eliminate invisible text |

**Anti-pattern detection:**

| Anti-pattern | Signs | Fix |
|-------------|-------|-----|
| **Golden hammer** | Using the same technique for every problem | Match the technique to the measured bottleneck |
| **Premature optimization** | Optimizing code that accounts for <1% of total runtime | Profile first; optimize the hot paths |
| **Caching everything** | Stale data, invalidation bugs, memory exhaustion | Cache the hot data; cache with TTL; measure hit rate |
| **Over-abstraction** | Factory factories, proxy proxies, decorator stacks | Measure cost of abstraction layers; flatten where possible |
| **Sync in async loop** | `await` inside `for` with independent iterations | `Promise.all()` for independent work |
| **Render-on-every-change** | State change re-renders entire component tree | Memoize, use subscriptions, virtual diff |

**Exit criteria:** One optimization applied, one metric changed, before/after
measurement documented.

### Step 4: Re-Measure & Validate

Apply the same measurement tools from Step 1 to the optimized version.

**Validation checklist:**
- [ ] Target metric improved (LCP, FID, CLS, or the internal equivalent)
- [ ] No other metric regressed by more than 5%
- [ ] All existing tests pass
- [ ] Visual output is identical (no broken layouts, no missing content)
- [ ] The optimization does not degrade the user experience on slower
      devices or networks
- [ ] The optimization is resilient to cache misses (cold-load performance
      is also acceptable)

If the metric did not improve, the hypothesis was wrong. Revert the change
and return to Step 2. Optimization attempts that do not improve the target
metric are noise.

**Exit criteria:** A documented before/after comparison showing measurable
improvement. The improvement crosses at least one threshold boundary (e.g.,
"Needs Improvement" → "Good") or exceeds a defined SLA.

### Step 5: Install Monitoring & Regression Guards

Performance is a feature that must be maintained. Without regression guards,
optimizations degrade over every deploy cycle.

**Guard types:**
- **Lighthouse CI:** Fail the build if LCP, FID, CLS, or TBT regress beyond
  a configured threshold.
- **Bundle size budgets:** Warn at 200KB, fail at 300KB (gzipped, initial).
  Use `webpack-assets-size-limits` or `size-limit`.
- **APM alerts:** Notify when p95 latency exceeds baseline by 20%.
- **Database query timeout:** Set `statement_timeout` in PostgreSQL,
  `max_execution_time` in MySQL.
- **Real-user monitoring:** Web Vitals dashboard with weekly trend alerts.
- **Performance budgets in PR templates:** "Did this change add a new
  dependency? Increase bundle size? Add a database query? If so, what is the
  performance justification?"
- **Perf Champions:** Designate team members who review all changes with
  performance implications.

---

## Anti-Rationalization Table

| Excuse | Rebuttal |
|--------|----------|
| "The page loads fine on my machine." | Your machine has a high-end CPU, plentiful RAM, and a fast network. The median user's device is a 3-year-old phone on 4G. Measure on the median device. |
| "We should optimize this now to be safe." | "Just-in-case" optimization adds complexity and rarely targets the actual bottleneck. Measure first, optimize the real bottleneck, re-measure. |
| "The database is slow, but we can't change the schema right now." | Then add an index. Add a cache. Add a read replica. There is always something you can do without schema changes. Do that now. |
| "Code splitting is too complex for this project." | Code splitting is a one-line change in modern frameworks (`dynamic import()`). The complexity argument is outdated — modern bundlers handle it automatically. |
| "Our users won't notice a 200ms difference." | 200ms exceeds user perception thresholds. Amazon reports 1% revenue drop per 100ms of latency. Google reports 0.2% search abandonment per 100ms. Users notice. |
| "We'll optimize in the next sprint." | Performance debt compounds. Every sprint adds queries, bundles grow, and slowdowns accumulate. Sprint-specific performance budget enforcement prevents this. |
| "The framework handles performance automatically." | Frameworks provide reasonable defaults, but they cannot eliminate N+1 queries, redundant re-renders, or oversized images. Framework performance requires active stewardship. |

## Red Flags

- Optimization committed without baseline measurement
- "Performance improvement" with no measurable metric change
- Bundle size growing every sprint with no budget cap
- Database queries without `EXPLAIN` review
- Images served at 4000px width when displayed at 200px
- No cache headers on API responses
- `will-change` applied to too many elements (memory over-commit)
- No performance monitoring in production
- Performance regressions discovered by users, not by monitoring
- "Let's throw more servers at it" solution instead of profiling

## Verification

1. Run Lighthouse/PageSpeed on the critical pages. All Core Web Vitals in the
   "Good" range?
2. Check bundle size (gzipped). Under 250KB for initial load?
3. Check the performance budget. Does the build fail if exceeded?
4. Run database slow-query log for 24 hours. Zero queries exceeding 500ms?
5. Check APM p95 latency. Under 500ms for API endpoints?
6. Verify cache headers: `Cache-Control`, `ETag`, CDN integration present?
7. Check image sizes: are responsive images (`srcset`, `<picture>`) used?
8. Verify code splitting: does each page route load only its own JS chunk?
9. Check for render-blocking resources: have all non-critical CSS/JS been
   deferred or made async?
10. Test on a throttled connection (Slow 3G) and a mid-range device (Moto G4
    or equivalent). Is the experience acceptable?
