---
name: react-hook-authoring
description: Use when writing, reviewing, or designing custom React hooks for component libraries. Covers memoization decisions, consumer DX, controlled/uncontrolled patterns, and function stability. Prevents overengineering — start simple, add complexity only when profiler demands it. This skill should be used when building hooks that other developers will consume.
metadata:
  author: b4r7x
  version: "1.0.0"
---

# React Hook Authoring

Principles for building custom hooks in React 19 component libraries. Optimized for consumer DX — developers using the hooks should not need to think about memoization.

## Core Principle

**Start without memoization. Add it only when the profiler shows a problem.**

The default hook returns plain functions recreated each render. This is correct, simple, and sufficient for the vast majority of cases. Stability is the consumer's responsibility where needed (e.g. `useMemo` on context value).

## Decision Tree

```
Writing a custom hook that returns functions?
│
├─ Default: no useCallback, no useRef, no useMemo
│  (Approach A — see references/approaches.md)
│
├─ Does setValue go into a context with many consumers
│  AND profiler shows unnecessary re-renders?
│  └─ Yes → useLayoutEffect + useRef + useCallback([])
│     (Approach B — see references/approaches.md)
│     Requires "use client"
│
├─ Does the hook accept a callback from the consumer?
│  (e.g. onChange, onSuccess, onError)
│  └─ NEVER require the consumer to useCallback
│     Store it in a ref internally if needed for stability
│
├─ Does the hook use useSyncExternalStore?
│  └─ subscribe must be stable → useCallback (React requires this)
│
└─ Is the hook for a context provider?
   └─ useMemo on the context value object is justified
      Functions in the value should be stable IF many consumers exist
```

## Antipatterns

### 1. Premature useCallback

```ts
// ❌ useCallback with unstable dep — achieves nothing
const setValue = useCallback((next: T) => {
  onChange?.(next); // onChange is new every parent render
}, [onChange]); // setValue changes every render anyway

// ✅ No useCallback — same behavior, less complexity
const setValue = (next: T) => {
  onChange?.(next);
};
```

The `useCallback` cascade breaks when any dep is unstable. One unstable dep (like an unmemoized `onChange` from a parent) makes the entire chain useless.

### 2. Side effect in state updater

```ts
// ❌ Strict Mode calls the updater 2x — onChange fires twice
setInternal((prev) => {
  const resolved = updater(prev);
  onChange?.(resolved); // BUG: side effect in pure function
  return resolved;
});

// ✅ onChange after setInternal, not inside
const resolved = updater(current);
setInternal(resolved);
onChange?.(resolved);
```

State updater functions must be pure. React may call them multiple times in Strict Mode and Concurrent Mode.

### 3. Ref-during-render (without useLayoutEffect)

```ts
// ❌ React docs warn: "Do not write ref.current during rendering"
const ref = useRef(onChange);
ref.current = onChange; // tearing risk in Concurrent Mode

// ✅ Safe — updates after commit
const ref = useRef(onChange);
useLayoutEffect(() => {
  ref.current = onChange;
});
```

Libraries do ref-during-render because `useLayoutEffect` causes SSR warnings. With `"use client"`, use `useLayoutEffect` — it's safe and React-compliant.

### 4. Forcing consumer to memoize

```ts
// ❌ Bad DX — consumer must useCallback or hook breaks
function useMyHook(onSuccess: () => void) {
  useEffect(() => {
    fetchData().then(onSuccess);
  }, [onSuccess]); // re-fetches when parent re-renders
}

// ✅ Good DX — consumer passes plain function
function useMyHook(onSuccess: () => void) {
  const ref = useRef(onSuccess);
  useLayoutEffect(() => { ref.current = onSuccess; });

  useEffect(() => {
    fetchData().then(() => ref.current());
  }, []); // stable — never re-fetches
}
```

### 5. Overengineering controlled/uncontrolled

```ts
// ❌ Two separate hooks, useReducer, Zustand-like store, useEventCallback wrapper
// All of these add complexity without solving a real problem

// ✅ Mantine-style — 15 lines, covers 95% of use cases
const [internal, setInternal] = useState(defaultValue);
const controlled = value !== undefined;
const current = controlled ? value! : internal;

const setValue = (next: T) => {
  if (!controlled) setInternal(next);
  onChange?.(next);
};
```

## When useMemo IS Justified

- **Context value object** — prevents all consumers from re-rendering on unrelated parent changes
- **Heavy computation** — filter/sort of large arrays with measurable cost (profile first)
- **Object/array in useEffect deps** — when the reference must be stable to prevent effect re-runs

## When useMemo is NOT Justified

- Primitives (string, number, boolean) — compared by value, not reference
- Objects that are only read during render and not passed as deps
- "Just in case" / preventive memoization

## Reference Material

For detailed patterns from top libraries (react-hook-form, TanStack, ahooks, SWR, Mantine), read `references/library-patterns.md`.

For full Approach A vs B code with decision rules, read `references/approaches.md`.
