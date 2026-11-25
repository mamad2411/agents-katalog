---
name: react-best-practices
description: React/Next.js best-practices reviewer for TSX/JSX. Triggers when writing or reviewing React components to check structure, hooks, accessibility, performance, and TypeScript patterns.
---

# Vercel React Best Practices

Comprehensive performance optimization guide for React and Next.js applications, maintained by Vercel. Contains 64 rules across 8 categories, prioritized by impact to guide automated refactoring and code generation.

## Rule Categories by Priority

| Priority | Category                  | Impact      | Prefix       | Reference                              |
| -------- | ------------------------- | ----------- | ------------ | -------------------------------------- |
| 1        | Eliminating Waterfalls    | CRITICAL    | `async-`     | `references/eliminating-waterfalls.md` |
| 2        | Bundle Size Optimization  | CRITICAL    | `bundle-`    | `references/bundle-size.md`            |
| 3        | Server-Side Performance   | HIGH        | `server-`    | `references/server-performance.md`     |
| 4        | Client-Side Data Fetching | MEDIUM-HIGH | `client-`    | `references/client-data-fetching.md`   |
| 5        | Re-render Optimization    | MEDIUM      | `rerender-`  | `references/rerender-optimization.md`  |
| 6        | Rendering Performance     | MEDIUM      | `rendering-` | `references/rendering-performance.md`  |
| 7        | JavaScript Performance    | LOW-MEDIUM  | `js-`        | `references/javascript-performance.md` |
| 8        | Advanced Patterns         | LOW         | `advanced-`  | `references/advanced-patterns.md`      |

## References

Each file is loaded on demand — read one only when the task needs that depth (progressive disclosure).

- `references/eliminating-waterfalls.md` — parallelize independent async work (`Promise.all`, `better-all`), defer await into the branch that needs it, stream with Suspense, and start promises early in API routes/Server Actions · read when touching async data flow, `await` chains, API routes, or Server Actions.
- `references/bundle-size.md` — import directly (no barrel files), `next/dynamic` for heavy components, defer third-party scripts past hydration, load modules conditionally, and preload on user intent · read when reducing bundle size, code-splitting, or adding third-party/analytics scripts.
- `references/server-performance.md` — authenticate server actions, dedupe with `React.cache()`/LRU, hoist static I/O, parallelize fetches, minimize RSC prop serialization, and use `after()` for non-blocking work · read when writing Server Components, Server Actions, or RSC data fetching.
- `references/client-data-fetching.md` — SWR request deduplication, shared/passive global event listeners, and versioned, minimal localStorage · read when fetching on the client, attaching window/document listeners, or persisting to storage.
- `references/rerender-optimization.md` — subscribe narrowly (defer reads, derived booleans), derive state during render not effects, functional/lazy `useState`, `React.memo` correctly, split hooks, transitions/`useDeferredValue`, and refs for transient values · read when diagnosing or preventing unnecessary re-renders and effect churn.
- `references/rendering-performance.md` — hoist static JSX, `content-visibility`/`Activity` for offscreen work, animate wrappers not SVGs, SVG precision, explicit conditional rendering, hydration without flicker, and resource/script hints · read when optimizing render cost, hydration flicker, SVG/animation, or `<script>`/preload tags.
- `references/javascript-performance.md` — index maps and Set/Map O(1) lookups, cached property/function/storage reads, single-pass iteration (`flatMap`, combined loops), early exits, hoisted RegExp, loop-based min/max, and `toSorted` · read when optimizing hot loops or data-structure-heavy JS.
- `references/advanced-patterns.md` — store event handlers in refs, initialize once per app load, and `useLatest`/`useEffectEvent` for stable callback refs · read when stabilizing callback identity or guarding one-time initialization.
