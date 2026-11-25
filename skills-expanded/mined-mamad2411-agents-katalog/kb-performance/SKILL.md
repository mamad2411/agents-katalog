---
name: kb-performance
last-verified: 2026-04-23
description: Portable performance optimization discipline for Next.js + React + Drizzle + Vercel projects. Invoke when there is a measurable target (LCP/INP/CLS over budget, bundle >200KB, slow dashboard, long-list jank, memory growth) — enforces measure-first rule, 4-step BASELINE→IDENTIFY→FIX→VALIDATE workflow, and stack-tuned playbooks. For slowness that is actually a bug → `kb-debug`.
---

# kb-performance — Performance Optimization

> Stack: Next.js 16+ App Router, React 19, Drizzle + Neon Postgres, Vercel hosting. Tools shipped: `pnpm analyze` (bundle), Lighthouse, DevTools Performance/Memory, `pnpm db:query` for SQL `EXPLAIN ANALYZE`.
>
> **Pair:** [`kb-debug`](../kb-debug/SKILL.md) — when the slowness is a bug, not a measurable optimization opportunity.
> **Cross-refs:** [`kb-ui`](../kb-ui/SKILL.md) for Suspense/Skeleton streaming patterns; [`kb-dataviz`](../kb-dataviz/SKILL.md) for chart-specific perf.

> **Registry anchors** — hooks, action wrappers y helpers shipped por el kit viven indexados en [`project/reference/HOOKS.md`](../../../project/reference/HOOKS.md) (autogen — SSOT de import paths + firmas). Ejemplos de librerías externas (SWR, Recharts) o custom hooks de apps derivadas son **ilustrativos** y no forman parte del kit. Esta skill enseña la **disciplina** (measure first, dedupe, cache, boundaries); los nombres exactos de APIs se leen del registry o de la doc oficial de la lib.
>
> Source material absorbed (2026-04-22): 57 Vercel Engineering rules from legacy `nextjs-react-expert` — condensed into stack-tuned prose below.

---

## 1. Philosophy — measure first

> Users don't care about benchmarks. They care about feeling fast. Profile before optimizing; never optimize from intuition.

| Rule                                 | Why it matters                                                                  |
| ------------------------------------ | ------------------------------------------------------------------------------- |
| **Measure before changing anything** | Without a baseline, you can't prove improvement. "Felt faster" is not a metric. |
| **Fix the biggest bottleneck first** | Micro-optimizations on fast code don't move user-perceived perf.                |
| **Target user-perceived metrics**    | LCP/INP/CLS are proxies for "feels fast", not synthetic benchmarks.             |
| **Stop when good enough**            | Perf tuning has diminishing returns. Hit the target, move on.                   |
| **Do not pre-optimize**              | YAGNI applies; optimize once a real user or a real profile complains.           |

---

## 2. Core Web Vitals — the acceptance bar (2026)

| Metric  | Good    | Needs work  | Poor    | What it measures                         |
| ------- | ------- | ----------- | ------- | ---------------------------------------- |
| **LCP** | < 2.5s  | 2.5 – 4s    | > 4.0s  | Time to largest content paint            |
| **INP** | < 200ms | 200 – 500ms | > 500ms | Worst-case interaction responsiveness    |
| **CLS** | < 0.1   | 0.1 – 0.25  | > 0.25  | Cumulative visual shift during page life |

**Where to measure:**

| Stage        | Tool                                                  |
| ------------ | ----------------------------------------------------- |
| Local dev    | Chrome DevTools → Lighthouse (mobile + throttled CPU) |
| PR / preview | Lighthouse CI against the Vercel preview URL          |
| Production   | Vercel Web Analytics (RUM) — real users, real devices |

Synthetic (Lighthouse) ≠ field (RUM). Use RUM to decide what to fix; use Lighthouse to verify before ship.

---

## 3. The 4-step workflow

```
1. BASELINE   → capture numbers (LCP/INP/CLS + bundle size + SQL timings)
2. IDENTIFY   → find the biggest contributor — do not guess
3. FIX        → one targeted change; keep everything else constant
4. VALIDATE   → re-measure; if the gap moved, commit; if not, revert
```

| Symptom                 | First diagnostic                                                                                                     |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------- |
| LCP > 2.5s              | Lighthouse → "Opportunities" → focus on LCP element                                                                  |
| INP > 200ms             | DevTools Performance → record interaction → look for long tasks (>50ms)                                              |
| CLS > 0.1               | Lighthouse → "Avoid large layout shifts" — images without dimensions, late-loading fonts/ads                         |
| Main bundle > 200KB     | `pnpm analyze` → open the report → find the largest module                                                           |
| Slow server response    | Vercel function logs or `EXPLAIN ANALYZE` via `pnpm db:query`                                                        |
| Jank during scroll      | DevTools Performance → flame chart → long paint/layout frames                                                        |
| Memory growth over time | DevTools Memory → 2 heap snapshots → compare retained objects                                                        |
| List of 1000+ rows lags | DevTools Performance → check recalc-style/layout cost per row; consider virtualization or `content-visibility: auto` |

---

## 4. Stack-specific playbooks

### 4.1 Eliminate waterfalls

Sequential `await` is the single biggest LCP killer. Each await = full network latency added in series.

**Rule — `Promise.all` for independent operations:**

```tsx
// ❌ 3 round-trips in series
const user = await getUser();
const projects = await getProjects(user.id);
const tasks = await getTasks(user.id);

// ✅ max(RTT), not sum(RTT). Start early, await at the join
const userPromise = getUser();
const [user, projects, tasks] = await Promise.all([
  userPromise,
  userPromise.then((u) => getProjects(u.id)),
  userPromise.then((u) => getTasks(u.id)),
]);
```

**Rule — promise-first pattern for API routes / Server Actions:**

```tsx
// ✅ auth + config kick off immediately; data awaits only after session is known
export async function GET() {
  const sessionPromise = auth();
  const configPromise = fetchConfig();
  const session = await sessionPromise;
  const [config, data] = await Promise.all([configPromise, fetchData(session.user.id)]);
  return Response.json({ data, config });
}
```

**Rule — defer `await` until needed:** early-return paths must not pay for data they never use.

```tsx
// ❌ fetches permissions even for 404
async function updateResource(id: string, userId: string) {
  const permissions = await fetchPermissions(userId);
  const resource = await getResource(id);
  if (!resource) return { error: 'Not found' };
  // ...
}

// ✅ fetch only on the branches that need it
async function updateResource(id: string, userId: string) {
  const resource = await getResource(id);
  if (!resource) return { error: 'Not found' };
  const permissions = await fetchPermissions(userId);
  // ...
}
```

**Rule — strategic Suspense boundaries:** don't block the layout on data. Wrap the async leaf in `<Suspense>` and render the frame immediately.

```tsx
// ❌ wrapper blocked by data fetching
async function Page() {
  const data = await fetchData();
  return (
    <Layout>
      <DataDisplay data={data} />
    </Layout>
  );
}

// ✅ layout streams instantly; only DataDisplay waits
function Page() {
  return (
    <Layout>
      <Suspense fallback={<Skeleton />}>
        <DataDisplay />
      </Suspense>
    </Layout>
  );
}
async function DataDisplay() {
  const data = await fetchData();
  return <div>{data.content}</div>;
}
```

Share one promise across siblings with `use()` if both need the same data. Don't suspense critical above-the-fold content (layout shift risk); do suspense secondary sections. Skeletons must mirror real layout to avoid CLS — see [`kb-ui §6`](../kb-ui/SKILL.md).

**Rule — parallel fetching via RSC composition:** Server Components execute sequentially within a tree. Restructure so each async component fetches its own data rather than a parent awaiting everything first.

```tsx
// ❌ Sidebar's fetch waits for Header's fetch to complete
async function Page() {
  const header = await fetchHeader();
  return (
    <div>
      <Header data={header} />
      <Sidebar />
    </div>
  );
}

// ✅ Header + Sidebar both await, React schedules them in parallel
function Page() {
  return (
    <div>
      <Header />
      <Sidebar />
    </div>
  );
}
async function Header() {
  const data = await fetchHeader();
  return <div>{data}</div>;
}
async function Sidebar() {
  const items = await fetchSidebarItems();
  return <nav>{items.map(renderItem)}</nav>;
}
```

---

### 4.2 Bundle discipline

```bash
pnpm analyze
# Target: main client bundle < 200KB gzipped. Watch the server bundle too.
```

| Anti-pattern                                                     | Fix                                                                                                                          |
| ---------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Barrel import from huge lib (`import { X } from 'lucide-react'`) | Import deep: `import X from 'lucide-react/dist/esm/icons/x'`. Barrels can re-export 10k modules and add 200–800ms cold start |
| Whole icon pack imported                                         | Same rule — only the icons you use                                                                                           |
| Heavy editor/chart library on every page                         | `dynamic(() => import('./HeavyEditor'), { ssr: false })`                                                                     |
| Analytics/logging in root layout                                 | `dynamic(() => import('@vercel/analytics/react').then(m => m.Analytics), { ssr: false })` — load after hydration             |
| Duplicate dep versions in lockfile                               | `pnpm dedupe`                                                                                                                |
| Dead code dragged in by re-exports                               | `pnpm knip`                                                                                                                  |

**Ergonomic barrel workaround — `optimizePackageImports`:**

```js
// next.config.js
module.exports = {
  experimental: {
    optimizePackageImports: ['lucide-react', '@mui/material', 'date-fns'],
  },
};
// Then `import { X } from 'lucide-react'` is auto-transformed to deep imports at build time.
```

**Rule on barrel files (`index.ts` re-exports):** fine for `@/components/ui` primitives (stable surface). Avoid in `app/` route code — tree-shaking across barrels is fragile unless the lib is listed in `optimizePackageImports`.

**Rule — conditional module loading:** lazy-import big data/modules only when the feature activates, and guard with `typeof window !== 'undefined'` so nothing bundles into the server chunk.

```tsx
useEffect(() => {
  if (enabled && !frames && typeof window !== 'undefined') {
    import('./animation-frames.js').then((mod) => setFrames(mod.frames));
  }
}, [enabled]);
```

**Rule — preload on user intent:** warm heavy bundles on hover/focus or when a flag enables a feature, so the click is instant.

```tsx
<button
  onMouseEnter={() => {
    if (typeof window !== 'undefined') void import('./monaco-editor');
  }}
  onFocus={() => {
    if (typeof window !== 'undefined') void import('./monaco-editor');
  }}
  onClick={open}
>
  Open Editor
</button>
```

---

### 4.3 React 19 cost model + RSC boundary

| Pattern                                    | Cost                                                                            |
| ------------------------------------------ | ------------------------------------------------------------------------------- |
| Server Component                           | Zero client JS for the render itself                                            |
| `'use client'` at the page root            | Ships the entire tree to the client — expensive                                 |
| `'use client'` at the leaf (button, input) | Ships only the leaf — cheap                                                     |
| `cache()` around a function                | Dedupes within a request (per-render memo)                                      |
| `unstable_cache()`                         | Dedupes across requests with a TTL/tag                                          |
| `fetch(url, { cache: 'force-cache' })`     | HTTP-level caching, route-segment aware                                         |
| `after(() => ...)`                         | Runs AFTER the response is sent — logging, analytics, audit, cache invalidation |
| `useMemo` / `useCallback`                  | Only if profiled — keep the source stable or they're useless                    |
| `React.memo` on a component                | Only if parent re-renders frequently AND child render cost is non-trivial       |

```tsx
// Per-request dedup — multiple callers in the same request get the same Promise
import { cache } from 'react';
export const getUser = cache(async (id: string) => db.select()...);
```

**Default:** every component is Server. Add `'use client'` only when a leaf needs `useState`/`useEffect`/event handlers/browser APIs (see [`kb-ui §1`](../kb-ui/SKILL.md)).

**`cache()` argument rule — primitives over objects.** `cache()` uses `Object.is`, so inline objects create new refs and always miss the cache:

```tsx
// ❌ Always cache miss — each call creates a new object
const getUser = cache(async (p: { id: number }) => db.user.findUnique({ where: { id: p.id } }));
getUser({ id: 1 });
getUser({ id: 1 });

// ✅ Primitive args use value equality
const getUser = cache(async (id: number) => db.user.findUnique({ where: { id } }));
getUser(1);
getUser(1); // cache hit
```

Next.js auto-dedupes `fetch()` with the same URL + options within a request — you don't need `cache()` for fetch. Use `cache()` for DB queries (Drizzle/Prisma), auth checks, file I/O.

**Minimize RSC serialization.** Every prop you pass across the Server→Client boundary is serialized into the HTML + RSC payload. Only pass fields the client actually uses.

```tsx
// ❌ serializes all 50 fields of user
async function Page() {
  const user = await fetchUser();
  return <Profile user={user} />;
}

// ✅ serializes only what Profile needs
async function Page() {
  const user = await fetchUser();
  return <Profile name={user.name} avatar={user.avatar} />;
}
```

**Don't duplicate data at the boundary.** RSC→client dedupes by reference, not value. Transformations (`.toSorted()`, `.filter()`, `.map()`, `{...obj}`) create new refs and double the payload. Do transforms in the client, not the server:

```tsx
// ❌ sends the array twice (new ref from toSorted)
<ClientList items={items} itemsSorted={items.toSorted()} />

// ✅ send once, sort in the client
<ClientList items={items} />;
// 'use client'
const sorted = useMemo(() => [...items].sort(), [items]);
```

**`after()` for non-blocking side effects.** Logging, analytics, audit entries, cache invalidation — don't make the response wait.

```tsx
import { after } from 'next/server';

export async function POST(request: Request) {
  await updateDatabase(request);
  after(async () => {
    logUserAction({ userAgent: (await headers()).get('user-agent') });
  });
  return Response.json({ status: 'ok' });
}
```

Runs even on failure/redirect. Works in Server Actions, Route Handlers, and Server Components.

**Cross-request LRU on Fluid Compute.** `cache()` only dedupes within a single request. For data shared across sequential requests (user clicks A, then B, both hitting the same lookup), use an LRU. On Vercel Fluid Compute, instances are reused and the cache persists across requests without Redis:

```ts-example
import { LRUCache } from 'lru-cache';
const cache = new LRUCache<string, User>({ max: 1000, ttl: 5 * 60 * 1000 });

export async function getUser(id: string) {
  const hit = cache.get(id);
  if (hit) return hit;
  const user = await db.user.findUnique({ where: { id } });
  if (user) cache.set(id, user);
  return user;
}
```

On traditional serverless (cold-start-per-request), LRU won't persist — use Redis or Neon materialized views instead.

**Server Action auth — not a perf rule, but belongs here for completeness.** Server Actions are public endpoints. Always `await auth()` + permission check inside each `'use server'` function, even if middleware guards the page — SK.md §2.3 provides `withAuth()` / `withSelf()` wrappers so this is one line. Don't rely on layout guards.

---

### 4.4 Client-side data + event hygiene

**SWR over raw `useEffect` + `fetch`.** Multiple component instances calling the same endpoint should share one request. SWR dedupes, caches, and revalidates for free:

```ts-example
import useSWR from 'swr';
const { data, error, isLoading } = useSWR('/api/users', fetcher);
// Multiple <UserList> siblings → one network request
```

For writes and config-style immutable reads, use SWR's mutation and immutable variants (see SWR docs — external lib, not kit-shipped).

**Passive touch/wheel listeners** eliminate scroll-blocking. Browsers wait on non-passive listeners to see if `preventDefault()` is called; passive tells them not to bother:

```tsx
useEffect(() => {
  document.addEventListener('wheel', handleWheel, { passive: true });
  document.addEventListener('touchstart', handleTouch, { passive: true });
  return () => {
    /* removeEventListener */
  };
}, []);
```

Only skip passive when you actually need `preventDefault()` (custom swipe gestures, custom zoom).

**Deduplicate global listeners across N hook instances.** If a custom keyboard-shortcut or window-resize hook registers one listener per caller, the listener count grows linearly. Share via module-level `Map` + a single subscription primitive (SWR's subscription helper or a hand-rolled store):

```tsx
const keyCallbacks = new Map<string, Set<() => void>>();

function useKeyboardShortcut(key: string, cb: () => void) {
  useEffect(() => {
    const set = keyCallbacks.get(key) ?? new Set();
    set.add(cb);
    keyCallbacks.set(key, set);
    return () => {
      set.delete(cb);
      if (set.size === 0) keyCallbacks.delete(key);
    };
  }, [key, cb]);

  useSWRSubscription('global-keydown', () => {
    const handler = (e: KeyboardEvent) => keyCallbacks.get(e.key)?.forEach((c) => c());
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  });
}
```

**Versioned + minimal `localStorage`.** Always prefix keys with a version, store only the fields the UI needs, wrap every access in `try/catch` (throws in incognito, over quota, or when disabled).

```tsx
const V = 'v2';
function save(k: string, value: unknown) {
  try {
    localStorage.setItem(`${k}:${V}`, JSON.stringify(value));
  } catch {}
}
function load<T>(k: string): T | null {
  try {
    const raw = localStorage.getItem(`${k}:${V}`);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}
```

Never store tokens, PII, or a whole server response object — cherry-pick the 2–3 fields the UI actually reads.

---

### 4.5 Drizzle + Neon profiling

```bash
pnpm db:query "EXPLAIN ANALYZE SELECT * FROM tasks WHERE user_id = 'x' ORDER BY created_at DESC LIMIT 20"
```

| Red flag in EXPLAIN                    | Likely fix                                          |
| -------------------------------------- | --------------------------------------------------- |
| `Seq Scan` on a large table            | Add an index on the `WHERE` column                  |
| `Sort` on large result                 | Add a composite index matching `WHERE` + `ORDER BY` |
| Query time >> network RTT              | SQL problem, not network — fix the plan             |
| Many roundtrips in function logs (N+1) | Batch with `inArray()` or use a single join         |

**Pagination rule:** always `ORDER BY` with a **stable tiebreaker** (usually `id` or a monotonic timestamp). Offset-based pagination drifts if rows are inserted mid-scroll; cursor-based with a tiebreaker is stable.

**Connection pool:** Neon serverless driver is per-request; if you see `too many connections` in Vercel function logs, you're holding a connection across a stream/loop — close deterministically or switch to the pooled endpoint.

---

### 4.6 Re-render hygiene

Re-renders are cheap until they're not. Profile with the React DevTools Profiler before memoizing anything. If your project has React Compiler enabled, most manual memoization becomes unnecessary — but the correctness rules (stale closures, unnecessary state) still apply.

```tsx
// ❌ Stale closure — always reads initial `count`
const handleClick = () => setCount(count + 1);

// ✅ Functional updater — latest value, stable identity, no useCallback needed
const handleClick = () => setCount((prev) => prev + 1);
```

**Derive during render, don't sync in an effect.** If a value can be computed from props/state, compute it — don't store it + mirror with `useEffect`. Effects that only mirror props are dead weight and create extra renders.

```tsx
// ❌
useEffect(() => {
  setFullName(first + ' ' + last);
}, [first, last]);

// ✅
const fullName = first + ' ' + last;
```

**Put interaction side-effects in event handlers, not effects keyed by state.** Submitting, toasting, posting — those are event-triggered, not state-triggered. Modelling them as `state + useEffect` makes the effect re-run on unrelated dep changes and can double-fire.

**Don't wrap primitives in `useMemo`.** If the expression is `a || b` or `arr.length > 0`, `useMemo` costs more than recomputing.

**Stable defaults for memoized-component non-primitive params.** `memo()` compares refs; a default `() => {}` inline creates a new ref every render, breaking memo. Hoist to a module constant (`NOOP`).

**Extract to a memoized component for early returns.** `useMemo` inside a component still pays the dep-compare cost even when the result is discarded. Extracting to `memo(Child)` lets the parent early-return before Child renders.

**Narrow `useEffect` deps to primitives.** `[user]` re-runs on any field change; `[user.id]` re-runs only on identity change. For derived booleans (`width < 768`), compute the boolean outside the effect so the effect depends on the transition, not on every pixel.

**Lazy state init for expensive initial values.** Pass a function to `useState` so `buildSearchIndex(items)` runs only on mount, not every render:

```tsx
// ❌ runs on every render
const [idx] = useState(buildSearchIndex(items));
// ✅ runs only on mount
const [idx] = useState(() => buildSearchIndex(items));
```

**`useRef` for transient values** that change fast but shouldn't trigger re-renders (mouse position, debounce timers, "did-fire" flags). Updating a ref never re-renders.

**`startTransition` for non-urgent updates** (scroll position, search results behind a debounce). Keeps the UI responsive by marking the update as interruptible.

**Subscribe to derived state, not raw continuous values.** `useMediaQuery('(max-width: 767px)')` re-renders only on the breakpoint transition; `useWindowWidth()` re-renders on every pixel change.

**Defer dynamic-state reads to the usage point.** If `searchParams` or `localStorage` is only read inside a handler, don't subscribe at the component level — read from `window.location.search` / `localStorage` inside the handler. Skips N re-renders per route change.

| Symptom                                       | Fix                                                                          |
| --------------------------------------------- | ---------------------------------------------------------------------------- |
| Typing in one input re-renders the whole form | Lift only the changed field; consider RHF (it's uncontrolled by default)     |
| List re-renders all rows on one change        | Stable `key={item.id}` + `React.memo(Row)` (only if Row render is expensive) |
| Every click re-renders a heavy dashboard      | Move state to the leaf; sibling sections stay put                            |
| `useEffect` fires every render                | Fix the dep array — unstable object/function refs are the usual cause        |

---

### 4.7 Rendering performance

| Issue                                                  | Fix                                                                                                                     |
| ------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| Large lists (>100 rows)                                | Virtualize — `@tanstack/react-virtual` or TanStack Table windowing                                                      |
| Long scrollable lists where virtualization is overkill | `content-visibility: auto; contain-intrinsic-size: 0 Xpx` on each row — browser skips layout/paint for off-screen items |
| Images cause CLS                                       | Always set `width`+`height` (or `fill` with a reserved container)                                                       |
| Fonts cause FOIT/FOUT                                  | `next/font` — ships with `font-display: swap` + size-adjust                                                             |
| Layout thrash during scroll                            | Batch DOM reads then writes; avoid reading `offsetWidth` in a loop                                                      |
| Animations jank                                        | Animate `transform`/`opacity` only (GPU); never `top`/`left`/`width`                                                    |
| SVG animation stutters                                 | Wrap the SVG in a `<div>` and animate the wrapper — many browsers skip GPU accel on SVG elements directly               |
| Oversized SVG paths                                    | `npx svgo --precision=1 --multipass icon.svg` — big win on large icons                                                  |
| Static JSX recreated each render                       | Hoist to module scope: `const skeleton = <div class="…" />;` (React Compiler does this automatically)                   |

Respect `prefers-reduced-motion` for any non-essential animation — a11y + perceived perf win.

**Hydration without flicker.** When the first paint depends on `localStorage` / cookies (theme, locale), don't render-then-correct in `useEffect` — emit a synchronous inline script that mutates the DOM before React hydrates:

```tsx
<>
  <div id="theme-wrapper">{children}</div>
  <script
    dangerouslySetInnerHTML={{
      __html: `(function(){try{var t=localStorage.getItem('theme')||'light';var e=document.getElementById('theme-wrapper');if(e)e.className=t;}catch(e){}})();`,
    }}
  />
</>
```

`suppressHydrationWarning` is only for _expected_ mismatches (timestamps, locale formatting, generated IDs). Never use it to hide real hydration bugs.

**`<Activity>` for show/hide state preservation.** When a panel/dropdown is expensive to mount and toggles often, use `<Activity mode={open ? 'visible' : 'hidden'}>` to keep its DOM + state around instead of re-mounting.

**Explicit conditional rendering.** `{count && <Badge n={count} />}` renders the literal `0` when count is 0. Use `{count > 0 ? <Badge n={count} /> : null}` for numeric/string conditions that can be falsy.

**`useTransition` over manual `isLoading`.** Avoids the `setIsLoading(true) → setIsLoading(false)` boilerplate, resets correctly on error, auto-cancels when a newer transition starts:

```tsx
const [isPending, startTransition] = useTransition();
const onSearch = (q: string) => {
  setQuery(q);
  startTransition(async () => setResults(await fetchResults(q)));
};
```

---

### 4.8 Memory leaks

**Browser (long-lived dashboards):**

- `useEffect` with `addEventListener` missing cleanup in the return.
- `setInterval` / `setTimeout` without `clearInterval` at unmount.
- Module-scope `Map`/`Set` caches that never evict.
- React portal removed but ref still held by parent state.

**Server (Node / Server Actions):**

- `setInterval` in a request handler — scoped wrong, never cleared.
- Growing module-scope cache instead of `unstable_cache` with TTL (on Fluid Compute, use LRU with a `max` and `ttl` — §4.3).
- Retained references in closures — watch `cache()` on functions that close over large objects.

```bash
# Browser: Chrome DevTools → Memory → Heap snapshot → interact → snapshot → Comparison view
# Node: node --inspect ; attach DevTools ; 2 snapshots around the workload ; look at 'Retained Size'
```

---

### 4.9 JS hot-path micro-ops

Low-to-medium impact individually; worth applying in event handlers, render loops, or functions that run 100k+ times per session. Skip on cold paths — readable code wins there.

| Pattern                                       | Rule                                                                                    |
| --------------------------------------------- | --------------------------------------------------------------------------------------- |
| Repeated `.includes()` on an array            | Convert to `Set`: `new Set(ids).has(x)` — O(1) vs O(n)                                  |
| Repeated `.find(u => u.id === orderId)`       | Build a `Map` once: `new Map(users.map(u => [u.id, u]))`                                |
| `.sort()` inside a component / on props       | Use `.toSorted()` — `.sort()` mutates, breaks React's immutability                      |
| Sort to find max/min                          | Single loop — `let best = arr[0]; for (...) if (...) best = ...;`                       |
| `RegExp` created inside render                | Hoist to module scope or `useMemo` — watch `/g` `lastIndex` mutation                    |
| Multiple `.filter()` over the same array      | Single `for..of` with multiple pushes                                                   |
| Expensive array equality                      | Length check first, then element-by-element — avoid `sort().join()`                     |
| Deep property lookup inside loop              | Hoist: `const v = obj.a.b.c; for(...) use(v);`                                          |
| Same function called N times with same arg    | Cache in a module-level `Map<input, output>`                                            |
| `localStorage.getItem` called repeatedly      | Wrap in a `Map` cache; invalidate on `storage` + `visibilitychange`                     |
| Long validation loop                          | Early return on the first failure — no need to keep scanning                            |
| Interleaved DOM read+write (layout thrashing) | Batch all writes, then all reads. Prefer toggling a CSS class over `.style.*` in a loop |

---

### 4.10 Advanced patterns

**Init-once, not per-mount.** `useEffect(() => { init(); }, [])` runs on every remount and twice in dev Strict Mode. For app-startup side effects (auth check, SDK init, storage hydration), use a module-level flag:

```tsx
let didInit = false;
function Root() {
  useEffect(() => {
    if (didInit) return;
    didInit = true;
    loadFromStorage();
    checkAuthToken();
  }, []);
  // ...
}
```

**Stable subscriptions with latest-handler access.** When an effect subscribes to an event but depends on a handler that changes often, you don't want to re-subscribe every render. Use `useEffectEvent` (React 19) or a ref:

```tsx
import { useEffectEvent } from 'react';

function useWindowEvent(event: string, handler: (e: Event) => void) {
  const onEvent = useEffectEvent(handler);
  useEffect(() => {
    window.addEventListener(event, onEvent);
    return () => window.removeEventListener(event, onEvent);
  }, [event]);
}
```

Same pattern with a ref if you're on older React: store `handler` in a ref, update it on each render, call `ref.current(e)` inside the listener.

---

### 4.11 Vercel edge vs node runtime

| Need                                                    | Runtime                                      |
| ------------------------------------------------------- | -------------------------------------------- |
| Low-latency read-only handler, small body               | `edge` (auto-geo, faster cold start)         |
| Needs Node built-ins (`fs`, `crypto.randomBytes` large) | `nodejs` (default)                           |
| Uses Drizzle + Neon serverless driver                   | Either — driver supports both                |
| Uses Drizzle + `pg` pooled client                       | `nodejs` only                                |
| Benefits from cross-request LRU                         | `nodejs` on Fluid Compute (reuses instances) |

Edge is not a free speed-up — if your handler does 3 DB roundtrips, edge doesn't help. Fix the waterfalls first.

---

## 5. Quick-win order (highest ROI first)

1. **Eliminate waterfalls** (Server Components + `Promise.all` + RSC composition). Saves hundreds of ms.
2. **Minimize RSC serialization** (pass fields, not whole objects; don't duplicate via `.toSorted()` at the boundary).
3. **Dynamic-import heavy client components** (charts, editors, analytics). Cuts main bundle.
4. **Kill barrel imports** or enable `optimizePackageImports` for large libs.
5. **Add/fix DB indexes** for frequent queries on large tables. Turns seconds into ms.
6. **Add Suspense + skeleton** for slow sections — streams the fast parts early.
7. **Image dimensions + `next/image`** — fixes CLS, lazy-loads off-screen images.
8. **Font preloading with `next/font`** — fixes FOIT/FOUT + CLS.
9. **Virtualize lists >100 rows** or apply `content-visibility: auto` for lighter cases.
10. **Dedupe with `cache()`** in request-scoped data; LRU for cross-request on Fluid Compute.
11. **Fix re-render correctness** (functional `setState`, narrow deps, derive-during-render) — often fixes more than `memo`.
12. **Memoize only after profiling proves a re-render is expensive.**

---

## 6. Commands reference

| Need                              | Command                                                       |
| --------------------------------- | ------------------------------------------------------------- |
| Bundle analysis (client + server) | `pnpm analyze`                                                |
| Lighthouse locally                | Chrome DevTools → Lighthouse → Mobile + Throttled CPU         |
| Profile React re-renders          | React DevTools → Profiler → Record interaction                |
| Heap snapshot (browser)           | Chrome DevTools → Memory → Heap snapshot                      |
| Heap snapshot (node)              | `node --inspect` → chrome://inspect → Memory tab              |
| EXPLAIN a query safely            | `pnpm db:query "EXPLAIN ANALYZE SELECT ..."`                  |
| List tables / describe schema     | `pnpm db:query --tables` / `pnpm db:query --describe <table>` |
| Detect unused exports / deps      | `pnpm knip`                                                   |
| Shrink oversized SVGs             | `npx svgo --precision=1 --multipass <file>`                   |

---

## 7. Anti-patterns

| ❌ Don't                                                   | ✅ Do                                                          |
| ---------------------------------------------------------- | -------------------------------------------------------------- |
| Optimize without a baseline                                | Measure first; keep the before/after numbers                   |
| Chase micro-optimizations on already-fast code             | Fix the biggest bottleneck; stop when target is hit            |
| Sprinkle `useMemo` / `React.memo` everywhere               | Memoize only after profiling proves the re-render is expensive |
| `useMemo` wrapping a primitive expression                  | Just inline the expression                                     |
| Put `'use client'` at the page root                        | Push it to the leaves that need it                             |
| Sequential `await` for independent fetches                 | `Promise.all` or Suspense streaming                            |
| Pass whole server objects to client components             | Pass only the fields the client uses                           |
| Transform data at the RSC boundary (`.toSorted()`, spread) | Transform in the client; keep the server payload small         |
| Sync props into state via `useEffect`                      | Derive during render                                           |
| Side effects in effects instead of handlers                | If an event triggers it, handle it in the event handler        |
| Seq Scan on large tables                                   | Add the index; verify with `EXPLAIN ANALYZE`                   |
| Offset pagination on growing tables                        | Cursor + stable tiebreaker (`id`)                              |
| Forget image dimensions                                    | Always `width`/`height` or `fill` with reserved container      |
| Animate `top` / `left` / `width`                           | Animate `transform` / `opacity` — GPU composited               |
| Animate the SVG element directly                           | Wrap in `<div>` and animate the wrapper                        |
| `{count && <Badge n={count} />}` (renders `0`)             | `{count > 0 ? <Badge n={count} /> : null}`                     |
| Module-scope `Map` cache with no bound                     | `unstable_cache` with TTL/tag, or LRU with `max` + `ttl`       |
| Store whole server response in `localStorage`              | Version the key + cherry-pick only UI-needed fields            |
| `.sort()` on props / state                                 | `.toSorted()` — no mutation                                    |
| Treat Lighthouse score as truth                            | RUM (Vercel Web Analytics) is what real users feel             |

---

## 8. Pre-ship checklist

### Critical (block ship)

- [ ] No sequential `await` for independent data
- [ ] Main client bundle < 200KB gzipped (`pnpm analyze`)
- [ ] LCP < 2.5s on mobile throttled (Lighthouse preview)
- [ ] INP < 200ms on the primary interaction
- [ ] CLS < 0.1 (images sized, fonts preloaded)
- [ ] No barrel imports from large libs (or `optimizePackageImports` configured)

### High priority

- [ ] Server Components used where possible; `'use client'` only at leaves
- [ ] Heavy client components dynamically imported
- [ ] Analytics/logging deferred via `dynamic()` with `ssr: false`
- [ ] DB queries on large tables use indexes (verified with EXPLAIN)
- [ ] Suspense boundaries around slow sections with skeletons mirroring layout
- [ ] RSC props pass only fields the client uses
- [ ] No data duplication at the RSC boundary (`.toSorted()` / spread in server code)
- [ ] `after()` used for logging / analytics / audit in Route Handlers + Server Actions

### Nice to have

- [ ] `prefers-reduced-motion` respected on animations
- [ ] Lists >100 rows virtualized or `content-visibility: auto`
- [ ] `pnpm knip` shows no unused exports/deps
- [ ] `cache()` used for per-request dedup on expensive functions (DB queries, auth)
- [ ] Hot-path window/keyboard event hooks dedupe global listeners
- [ ] `localStorage` access is versioned, minimal, and wrapped in `try/catch`
- [ ] Touch/wheel listeners are `{ passive: true }` unless `preventDefault` is needed
- [ ] App-wide init gated by module-level flag, not `useEffect([])`

---

Cross-reference: [`kb-debug`](../kb-debug/SKILL.md) — when the slowness is a bug not an optimization opportunity. [`kb-ui`](../kb-ui/SKILL.md) — Server/Client boundary and Suspense+Skeleton layout-mirror pattern. [`kb-dataviz`](../kb-dataviz/SKILL.md) — chart-specific perf (Recharts reduced-motion, tooltip anchoring, lib choice).
