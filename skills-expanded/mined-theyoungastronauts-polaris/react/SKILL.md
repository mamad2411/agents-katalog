---
name: react
description: "React and Next.js performance best-practices reference — 57 rules across 8 categories, prioritized by impact."
disable-model-invocation: true
---

# Vercel React Best Practices

> Adapted from [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)

Comprehensive performance optimization guide for React and Next.js applications, maintained by Vercel. 57 rules across 8 categories, prioritized by impact.

## When to Apply

- Writing new React components or Next.js pages
- Implementing data fetching (client or server-side)
- Reviewing code for performance issues
- Refactoring existing React/Next.js code
- Optimizing bundle size or load times

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|---|---|---|---|
| 1 | Eliminating Waterfalls | CRITICAL | `async-` |
| 2 | Bundle Size Optimization | CRITICAL | `bundle-` |
| 3 | Server-Side Performance | HIGH | `server-` |
| 4 | Client-Side Data Fetching | MEDIUM-HIGH | `client-` |
| 5 | Re-render Optimization | MEDIUM | `rerender-` |
| 6 | Rendering Performance | MEDIUM | `rendering-` |
| 7 | JavaScript Performance | LOW-MEDIUM | `js-` |
| 8 | Advanced Patterns | LOW | `advanced-` |

## 1. Eliminating Waterfalls (CRITICAL)

- **async-defer-await**: Move `await` into branches where actually used
- **async-parallel**: Use `Promise.all()` for independent operations
- **async-dependencies**: Use `better-all` for partial dependencies
- **async-api-routes**: Start promises early, await late in API routes
- **async-suspense-boundaries**: Use Suspense to stream content

**Key pattern:** If two fetches don't depend on each other, run them in parallel:
```tsx
// BAD: Sequential
const user = await getUser(id)
const posts = await getPosts(id)

// GOOD: Parallel
const [user, posts] = await Promise.all([getUser(id), getPosts(id)])
```

## 2. Bundle Size Optimization (CRITICAL)

- **bundle-barrel-imports**: Import directly, avoid barrel files (`import { X } from './X'` not `from './index'`)
- **bundle-dynamic-imports**: Use `next/dynamic` for heavy components
- **bundle-defer-third-party**: Load analytics/logging after hydration
- **bundle-conditional**: Load modules only when feature is activated
- **bundle-preload**: Preload on hover/focus for perceived speed

## 3. Server-Side Performance (HIGH)

- **server-auth-actions**: Authenticate server actions like API routes
- **server-cache-react**: Use `React.cache()` for per-request deduplication
- **server-cache-lru**: Use LRU cache for cross-request caching
- **server-dedup-props**: Avoid duplicate serialization in RSC props
- **server-serialization**: Minimize data passed to client components
- **server-parallel-fetching**: Restructure components to parallelize fetches
- **server-after-nonblocking**: Use `after()` for non-blocking operations

**Key pattern:** Only send what the client needs:
```tsx
// BAD: Passing entire object
<ClientComponent data={fullUserObject} />

// GOOD: Pick only needed fields
<ClientComponent name={user.name} avatar={user.avatar} />
```

## 4. Client-Side Data Fetching (MEDIUM-HIGH)

- **client-swr-dedup**: Use SWR for automatic request deduplication
- **client-event-listeners**: Deduplicate global event listeners
- **client-passive-event-listeners**: Use passive listeners for scroll
- **client-localstorage-schema**: Version and minimize localStorage data

## 5. Re-render Optimization (MEDIUM)

- **rerender-defer-reads**: Don't subscribe to state only used in callbacks
- **rerender-memo**: Extract expensive work into memoized components
- **rerender-memo-with-default-value**: Hoist default non-primitive props
- **rerender-dependencies**: Use primitive dependencies in effects
- **rerender-derived-state**: Subscribe to derived booleans, not raw values
- **rerender-derived-state-no-effect**: Derive state during render, not effects
- **rerender-functional-setstate**: Use functional `setState` for stable callbacks
- **rerender-lazy-state-init**: Pass function to `useState` for expensive values
- **rerender-simple-expression-in-memo**: Avoid memo for simple primitives
- **rerender-move-effect-to-event**: Put interaction logic in event handlers
- **rerender-transitions**: Use `startTransition` for non-urgent updates
- **rerender-use-ref-transient-values**: Use refs for transient frequent values

**Key pattern:** Derive state during render, not in effects:
```tsx
// BAD: Effect to derive state
const [items, setItems] = useState([])
const [filteredItems, setFilteredItems] = useState([])
useEffect(() => { setFilteredItems(items.filter(i => i.active)) }, [items])

// GOOD: Derive during render
const [items, setItems] = useState([])
const filteredItems = items.filter(i => i.active)
```

## 6. Rendering Performance (MEDIUM)

- **rendering-content-visibility**: Use `content-visibility` for long lists
- **rendering-hoist-jsx**: Extract static JSX outside components
- **rendering-hydration-no-flicker**: Use inline script for client-only data
- **rendering-activity**: Use Activity component for show/hide
- **rendering-conditional-render**: Use ternary, not `&&` for conditionals
- **rendering-usetransition-loading**: Prefer `useTransition` for loading state

## 7. JavaScript Performance (LOW-MEDIUM)

- **js-batch-dom-css**: Group CSS changes via classes or `cssText`
- **js-index-maps**: Build `Map` for repeated lookups
- **js-combine-iterations**: Combine multiple `filter/map` into one loop
- **js-set-map-lookups**: Use `Set/Map` for O(1) lookups
- **js-early-exit**: Return early from functions
- **js-tosorted-immutable**: Use `toSorted()` for immutability

## 8. Advanced Patterns (LOW)

- **advanced-event-handler-refs**: Store event handlers in refs
- **advanced-init-once**: Initialize app once per app load
- **advanced-use-latest**: `useLatest` for stable callback refs

## Reference

For full rule explanations with detailed code examples, install the original skill:
```
npx skills add https://github.com/vercel-labs/agent-skills --skill vercel-react-best-practices
```
Individual rule files are available at `rules/<rule-name>.md` in the original repo.
