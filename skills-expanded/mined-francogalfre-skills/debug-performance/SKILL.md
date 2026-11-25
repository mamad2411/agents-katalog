---
name: debug-performance
description: Diagnoses and fixes performance problems in web apps: slow renders, memory leaks, large bundles, waterfall requests, and poor Core Web Vitals. Use when the user says "my app is slow", "too many re-renders", "memory leak", "LCP is bad", "bundle is too large", "this feels laggy", "optimize this component", or shares performance profiler output or Lighthouse results.
---

# Debug Performance

Diagnoses web application performance problems across four layers: rendering,
network, bundle, and memory. Identifies the root cause, not just symptoms,
and provides concrete fixes with measurable impact.

---

## Required Details

| Detail | Example |
|---|---|
| **Symptom** | "Laggy UI", "slow LCP", "memory grows over time" |
| **Framework** | Next.js / React / vanilla JS |
| **Code or profiler output** | Component, network waterfall, Lighthouse report |
| **Where it's slow** | Initial load / interaction / specific page |

---

## Instructions

### Step 1 — Identify the layer

| Symptom | Likely layer |
|---|---|
| Laggy UI, janky interactions | Rendering — re-renders or layout thrash |
| Slow initial page load | Network waterfall or bundle size |
| Bad LCP / CLS / INP score | Core Web Vitals — specific root causes per metric |
| Memory grows without release | Memory leak |
| Slow after many interactions | Memory leak or accumulating state |
| Slow API responses affecting UI | Network — waterfall or missing cache |

### Step 2 — Diagnose by layer

**Rendering (React)**
```tsx
// Diagnose: add to component to count renders
let renderCount = 0;
console.log('renders:', ++renderCount);

// Fix unnecessary re-renders
// ❌ Object created on every render — breaks memo
<Child config={{ theme: 'dark' }} />

// ✅ Stable reference
const config = useMemo(() => ({ theme: 'dark' }), []);
<Child config={config} />
```

Common causes:
- Props with inline objects/arrays/functions (`onClick={() => ...}`)
- Missing `React.memo` on expensive pure components
- State too high — move state down to the component that needs it
- `useEffect` with missing or wrong dependencies causing loops

**Bundle size**
```ts
// Diagnose: add to next.config.ts
import { BundleAnalyzerPlugin } from 'webpack-bundle-analyzer';

// Fix: dynamic import for heavy components
const HeavyChart = dynamic(() => import('@/components/HeavyChart'), {
  loading: () => <Skeleton />,
  ssr: false,
});

// Fix: import only what you need
// ❌
import _ from 'lodash';
// ✅
import debounce from 'lodash/debounce';
```

**Core Web Vitals**

| Metric | Root cause | Fix |
|---|---|---|
| LCP (slow largest paint) | Unoptimized hero image | `<Image priority />`, preload, WebP/AVIF |
| CLS (layout shift) | Images without dimensions | Always set `width` + `height` on images |
| INP (slow interaction) | Heavy JS on main thread | `startTransition`, `useDeferredValue`, Web Workers |

**Memory leaks**
```ts
// ❌ Event listener never removed
useEffect(() => {
  window.addEventListener('resize', handler);
}, []); // missing cleanup

// ✅ Cleanup on unmount
useEffect(() => {
  window.addEventListener('resize', handler);
  return () => window.removeEventListener('resize', handler);
}, []);
```

Common memory leaks:
- Event listeners without cleanup in `useEffect`
- `setInterval` / `setTimeout` without `clearInterval` / `clearTimeout`
- Subscriptions (WebSocket, RxJS, EventEmitter) not unsubscribed
- Closures holding references to large objects

**Network waterfall**
```ts
// ❌ Sequential fetches — waterfall
const user = await getUser(id);
const posts = await getPosts(user.id); // waits for user first

// ✅ Parallel fetches
const [user, posts] = await Promise.all([
  getUser(id),
  getPosts(id), // both start at the same time
]);
```

### Step 3 — Verify the fix

For each fix, provide a way to confirm it worked:
- Re-renders: React DevTools Profiler → check render count dropped
- Bundle: `next build` output → check chunk sizes
- LCP/CLS/INP: Lighthouse re-run → check score improvement
- Memory: Chrome DevTools Memory tab → heap snapshot before/after

---

## Non-Negotiable Acceptance Criteria

- [ ] Root cause identified — not just the symptom
- [ ] Each fix includes code showing before (❌) and after (✅)
- [ ] Each fix includes how to verify it worked
- [ ] Fixes are ordered by impact — highest impact first
- [ ] If multiple layers are affected, each is addressed separately

---

## Output Format

~~~
## Performance Diagnosis

### Root Cause
[What is actually causing the problem — be specific]

### Layer: [Rendering / Bundle / Network / Memory]

**Problem**
[explanation + problematic code]

**Fix**
[corrected code]

**How to verify**
[tool and what to look for]

[repeat for each layer affected]

### Expected Impact
[rough estimate: "should reduce re-renders by ~80%", "LCP improvement of ~1s"]
~~~