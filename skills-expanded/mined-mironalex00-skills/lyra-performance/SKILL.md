---
name: lyra-performance
description: Measurement-first performance optimization across frontend and backend. Use when code touches render paths, API endpoints, database queries, bundle size, or caching.
compatibility: No tools required. Measurement tools (Lighthouse, web-vitals, Chrome DevTools, APM, EXPLAIN ANALYZE, bundlesize, lhci) named but invoked by the user.
---

# lyra-performance

## What it does

A measurement-first performance skill for the full stack — React/Next.js render and Core Web Vitals on the frontend, API latency and DB queries on the backend. Every optimization is a hypothesis until a benchmark proves it; changes that don't measure up get reverted. 
Fourteen rules cover N+1 elimination, indexing, pagination, caching, code splitting, lazy loading, memoization, and image optimization, each with a bad/good pair. Pairs with `lyra-analyze-codebase` for systematic bottleneck discovery and `lyra-database` for deep query work.

## The profiling loop

```
measure     → establish a baseline with real numbers (synthetic + RUM)
identify    → find the actual bottleneck, not the assumed one
hypothesize → "fixing X will move Y from A to B" — falsifiable
fix         → address the specific bottleneck only
re-measure  → confirm the gain; revert if the number didn't move
guard       → add a test or monitor so it stays fixed
```

Skip step 1 and you're guessing. Skip step 5 and you don't know if you helped or hurt.

## The rules

### 1. Optimize from a benchmark, not a hunch

If you can't state the current number and the target, you're gambling. Hypotheses come from profile data, never intuition — the bottleneck sets the max gain (Amdahl), so anything else is wasted effort.

```
// bad:  "I think this loop is slow, let me rewrite it with a Set."
// good: "p95 is 340ms (target <200ms); getUserPermissions takes 280ms. Hypothesis: an index on permissions.user_id drops it below 50ms."
```

### 2. Re-measure, then guard the gain

Every fix is a hypothesis tested against before/after numbers; if the number didn't move, revert — complexity without gain is a regression. Add a budget check or regression test so the win survives next quarter.

```bash
npx bundlesize --config bundlesize.config.json   # bundle guard
npx lhci autorun                                  # Lighthouse CI
```

### 3. Measure synthetic AND real users

Synthetic (Lighthouse, DevTools) gives reproducible isolation; RUM (web-vitals, CrUX, APM) gives real-user truth. A fix that passes synthetic but misses RUM didn't improve the user's experience — "it's fast on my machine" is a confession that you measured the wrong device.

```ts
import { onLCP, onINP, onCLS } from "web-vitals";
onLCP(console.log);
onINP(console.log);
onCLS(console.log);
```

### 4. Follow the symptom-to-cause tree

Don't guess what's slow — walk the symptom to the cause.

```
What is slow?
├── First page load → bundle size, TTFB waterfall, render-blocking CSS/JS
├── Interaction sluggish → main-thread long tasks (>50ms), layout thrash
├── Navigation slow → API times, fetch waterfalls, N+1 client fetches
└── Backend / API
    ├── One endpoint → queries, indexes
    ├── All endpoints → pool, CPU, memory
    └── Intermittent → lock contention, GC, external deps
```

### 5. Eliminate N+1 queries

One query inside a loop is the most common backend performance bug, and it scales with record count. Batch with a join or a single `WHERE IN`.

```ts
// bad — one query per task for the owner
for (const t of await db.tasks.findMany())
  t.owner = await db.users.findUnique({ where: { id: t.ownerId } });
// good — single query with a join
const tasks = await db.tasks.findMany({ include: { owner: true } });
```

### 6. Index for your query patterns

Every `WHERE`, `JOIN`, and `ORDER BY` column needs an index; verify with `EXPLAIN ANALYZE`. An index that exists but isn't used is dead weight that slows every write.

```sql
-- bad — full table scan
SELECT * FROM orders WHERE user_id = ? AND status = 'shipped';
-- good — compound index matches the query; EXPLAIN ANALYZE shows "Index Scan"
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
```

### 7. Paginate every list endpoint

An unbounded `findMany()` is a data-volume bomb — one user with 100K records takes down the endpoint. Always `take` with a stable `orderBy`.

```ts
// bad — fetches all records
const allTasks = await db.tasks.findMany();
// good — paginated with a limit and stable order
const tasks = await db.tasks.findMany({
  take: 20,
  skip: (page - 1) * 20,
  orderBy: { createdAt: "desc" },
});
```

### 8. Cache with a TTL and an invalidation strategy

A cache without invalidation is a stale-data bug waiting to ship. Layer caches by scope (browser → CDN → app → DB), each with a TTL matched to how stale the data can get and a signal that invalidates it.

```ts
const CACHE_TTL = 5 * 60 * 1000;
let cached: AppConfig | null = null,
  expiry = 0;
async function getAppConfig(): Promise<AppConfig> {
  if (cached && Date.now() < expiry) return cached;
  cached = await db.config.findFirst();
  expiry = Date.now() + CACHE_TTL;
  return cached;
}
// Invalidate on write: cached = null;
```

### 9. Hit Core Web Vitals thresholds

LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1 — measured in RUM, not synthetic. A synthetic pass doesn't count; if RUM shows a miss, you have a real problem.

### 10. Code-split bundles and lazy-load heavy components

The initial bundle loads on every user, so split by route and defer heavy, rarely-used components behind `lazy()` + `Suspense`.

```tsx
// bad — everything in the initial bundle
import ChartLibrary from "./ChartLibrary";
import SettingsPage from "./pages/Settings";
// good — heavy components deferred; wrap usage in <Suspense fallback={<Spinner/>}>
const SettingsPage = lazy(() => import("./pages/Settings"));
const ChartLibrary = lazy(() => import("./ChartLibrary"));
```

### 11. Memoize only when measurement proves it

`useMemo` and `React.memo` aren't free — they add allocation and comparison overhead. Apply them only when a measurement shows the re-render is expensive and the memo comparison is cheaper; the same logic applies to stable references — a new object on every render defeats `React.memo`, so hoist it out.

```tsx
// bad — memoizing a trivial value; the memo costs more than the compute
const label = useMemo(() => `${count} items`, [count]);
// good — memoizing a genuinely expensive computation
const sorted = useMemo(() => heavySort(items, comparator), [items, comparator]);
```

### 12. Optimize images with dimensions, modern formats, and priority

Images are the largest LCP contributor. Provide dimensions (prevents CLS), modern formats (AVIF/WebP), responsive `srcset`, and `fetchpriority="high"` on the LCP image.

```html
<!-- bad — no dimensions, no format, no priority -->
<img src="/hero.jpg" />
<!-- good — dimensions, responsive, modern format, high priority -->
<img
  src="/hero-800.webp"
  srcset="/hero-400.webp 400w, /hero-800.webp 800w, /hero-1200.webp 1200w"
  sizes="(max-width: 1200px) 100vw, 1200px"
  width="1200"
  height="600"
  fetchpriority="high"
  decoding="async"
  alt="Hero"
/>
```

### 13. Don't optimize what isn't the bottleneck

Optimizing code that isn't the bottleneck adds complexity and slows the next developer — Knuth was right. "We'll optimize later" compounds if it's an N+1 or unbounded query (fix now); it's honest deferral for micro-optimizations. Don't trade readability for a gain that's neither measured nor significant (>10%) — `x >> 1` instead of `x / 2` saves nothing the JIT doesn't already do.

### 14. Compose with lyra-analyze-codebase and lyra-database

This skill fixes known bottlenecks. Use `lyra-analyze-codebase` to scan the repo for anti-patterns (N+1, missing indexes, unbounded queries, large bundles) before you profile, and `lyra-database` for deep query work (EXPLAIN plans, index strategy, denormalization) when the database is the bottleneck.

```
lyra-analyze-codebase → surfaces candidate bottlenecks
lyra-performance      → measures, confirms, fixes the real one
lyra-database         → optimizes the query/index layer
lyra-performance      → re-measures, guards the regression
```

## Performance targets

| Layer    | Metric                          | Target  |
| -------- | ------------------------------- | ------- |
| Frontend | LCP (Largest Contentful Paint)  | ≤ 2.5s  |
| Frontend | INP (Interaction to Next Paint) | ≤ 200ms |
| Frontend | CLS (Cumulative Layout Shift)   | ≤ 0.1   |
| Frontend | FCP (First Contentful Paint)    | ≤ 1.8s  |
| Frontend | Initial JS bundle (gzipped)     | < 200KB |
| Backend  | API p95 latency                 | < 200ms |
| Backend  | DB query p95                    | < 50ms  |
| Backend  | Error rate                      | < 0.1%  |

_Part of the [skill collection](../README.md)._