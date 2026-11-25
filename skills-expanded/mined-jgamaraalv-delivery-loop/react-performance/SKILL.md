---
name: react-performance
description: React performance: unnecessary re-renders, memoization (React.memo/useMemo/useCallback), React Compiler, Context, concurrent features, code splitting, and Core Web Vitals.
---

## Performance Debugging Workflow

Always follow this order — measure before optimizing:

1. **Reproduce** — Document exact steps, browser, device, network conditions
2. **Measure** — Profile with React DevTools Profiler + Chrome Performance tab. Never measure development builds.
3. **Identify** — Form a specific hypothesis about the cause
4. **Fix** — Apply the minimal fix needed
5. **Verify** — Measure improvement under same conditions

**Rule #1**: Do NOT measure the development build. For production profiling, alias:

- `react-dom$` → `react-dom/profiling`
- `scheduler/tracing` → `scheduler/tracing-profiling`

**Rule #2**: Simulate real user conditions (slow CPU, throttled network).

## Why Components Re-render

Components re-render for exactly three reasons:

1. **Its state changed**
2. **Its parent rendered** (unless wrapped in `React.memo`)
3. **A consumed Context value changed**

Renders are either **necessary** or **unnecessary**. Any single unnecessary render is rarely a problem — it's the accumulation over time.

## State Architecture (Fix Before Memoizing)

Before reaching for memoization, fix your state architecture. These are free performance wins:

### Colocate State

Move state to the closest component that needs it. State at the root re-renders the entire tree.

```tsx
// BAD: searchQuery in App re-renders Header, Cart, Footer
function App() {
  const [searchQuery, setSearchQuery] = useState("");
  return (
    <>
      <Header />
      <SearchBar query={searchQuery} onChange={setSearchQuery} />
      <Cart />
    </>
  );
}

// GOOD: searchQuery lives in SearchSection
function App() {
  return (
    <>
      <Header />
      <SearchSection />
      <Cart />
    </>
  );
}
function SearchSection() {
  const [searchQuery, setSearchQuery] = useState("");
  return <SearchBar query={searchQuery} onChange={setSearchQuery} />;
}
```

### Derive, Don't Store

If a value can be computed from existing state/props, compute it — don't store it.

```tsx
// BAD: synchronized state
const [items, setItems] = useState<Item[]>([]);
const [filteredItems, setFilteredItems] = useState<Item[]>([]);
// Must keep in sync — bugs + extra renders

// GOOD: derived value
const [items, setItems] = useState<Item[]>([]);
const filteredItems = items.filter((i) => i.active); // or useMemo if expensive
```

### Lift State Intelligently

Only lift state to the lowest common ancestor that needs it — no higher.

## Memoization Decision Guide

Three memoization tools, each with specific use cases:

| Tool          | What it caches          | Use when                                                                                   |
| ------------- | ----------------------- | ------------------------------------------------------------------------------------------ |
| `React.memo`  | Component render output | Profiler shows component re-renders due to parent, not its own props/state                 |
| `useMemo`     | Computation result      | Expensive calculation runs on every render, OR referential stability for memoized children |
| `useCallback` | Function identity       | Function passed as prop to `React.memo`-wrapped child, OR used in dependency arrays        |

**Key rule**: `useMemo`/`useCallback` are pointless without `React.memo` on the receiving child (or a dependency array consumer).

### When NOT to Memoize

- Simple/cheap components that render fast
- Props that change on almost every render anyway
- Components without memoized children receiving the value
- Simple calculations (the comparison overhead exceeds computation cost)

## React Compiler

The React Compiler is a Babel plugin that automatically applies memoization at build time. It analyzes your code and inserts `useMemo`/`useCallback` where safe.

**Prerequisites**: Code must follow the Rules of React — components must be pure, props/state immutable, no side effects in render.

### What the Compiler Handles

- Stabilizing callback identities (replaces manual `useCallback`)
- Memoizing derived values (replaces manual `useMemo`)
- Memoizing JSX output (replaces many `React.memo` wrappers)

### What You Still Need Manually

- **`React.memo`**: Impure components, 3rd-party library components, explicit render boundaries
- **`useMemo`**: Truly **expensive computations** the compiler can't prove safe, custom equality logic
- **`useCallback`**: **Complex** closure semantics, library APIs requiring stable function identities

## Context API Performance

Context is a broadcast mechanism — every consumer re-renders when the value changes. The fix is splitting.

### The Two-Context Pattern

Separate state from dispatch/actions into two contexts so components that only dispatch never re-render when state changes (full Provider example in `references/context-optimization.md`).

### Split by Domain

Never create a "mega context" with unrelated state. Split into `ThemeContext`, `AuthContext`, `UIContext`, etc.

## Concurrent Features

### useTransition vs useDeferredValue

|          | `useTransition`              | `useDeferredValue`                      |
| -------- | ---------------------------- | --------------------------------------- |
| Wraps    | The action (setState call)   | The value (result)                      |
| Use when | You control the state update | You don't control the update            |
| Provides | `isPending` boolean          | Compare current vs deferred value       |
| Effect   | Marks update as low-priority | Value lags behind during urgent updates |

Neither makes anything faster — they make the UI feel faster by prioritizing urgent updates (typing) over expensive work (filtering). Code examples for both, plus Suspense and data-fetching patterns, live in `references/concurrent-features.md`.

## Bundle Performance

### Code Splitting Checklist

1. **Route-based splitting** — `lazy()` + `Suspense` for each route
2. **Heavy component splitting** — Lazy-load modals, charts, editors
3. **Conditional feature splitting** — Admin panels, premium features
4. **Bundle analysis** — Use `webpack-bundle-analyzer` or `source-map-explorer`
5. **Tree shaking** — Use named exports, check `sideEffects` in package.json

## Core Web Vitals Quick Reference

| Metric                              | Target  | React Optimization                                                      |
| ----------------------------------- | ------- | ----------------------------------------------------------------------- |
| **LCP** (Largest Contentful Paint)  | < 2.5s  | SSR/SSG, preload critical assets, optimize images                       |
| **INP** (Interaction to Next Paint) | < 200ms | Break long tasks, memoize, debounce/throttle, Web Workers               |
| **CLS** (Cumulative Layout Shift)   | < 0.1   | Set image dimensions, reserve space for async content, skeleton loaders |

## React Fiber — How Rendering Works

React Fiber is a cooperatively-scheduled rendering engine using a linked-list tree structure.

- **Two trees**: Current (what DOM reflects) and Work-in-Progress (draft being prepared)
- **Yielding**: React yields to browser every ~5ms, allowing paint/input handling
- **Lanes**: Priority system using bitmasks — `SyncLane` > `InputContinuousLane` > `DefaultLane` > `TransitionLane` > `IdleLane`
- **Commits are never interrupted** — once render phase completes, DOM updates happen synchronously

Understanding this helps explain why `useTransition` works: it assigns updates to lower-priority lanes.

## References

Each file is loaded on demand — read one only when the task needs that depth (progressive disclosure).

- `references/profiling-and-debugging.md` — the systematic measure-before-optimize workflow, the React DevTools Profiler, the Chrome Performance tab, and production-profiling build setup · read when measuring, reproducing, or diagnosing a slowdown before touching code.
- `references/memoization-patterns.md` — `React.memo`, `useMemo`, and `useCallback` in depth with custom comparators and the dependency-array rules · read when applying memoization or deciding which of the three to reach for.
- `references/react-compiler.md` — React Compiler setup, how it auto-memoizes, migration steps, and what still needs manual memoization · read when adopting/migrating to the React Compiler or auditing what it can't cover.
- `references/context-optimization.md` — the two-context (state/dispatch) Provider pattern, the mega-context anti-pattern, and domain splitting · read when a Context value re-renders too many consumers.
- `references/concurrent-features.md` — `useTransition`, `useDeferredValue`, and Suspense with full code and data-fetching patterns · read when making expensive updates non-blocking or wiring Suspense.
- `references/bundle-and-loading.md` — code splitting, `lazy()`/`Suspense` route and component splitting, lazy-loading patterns, tree shaking, and bundle analysis · read when reducing bundle size or implementing lazy loading.
