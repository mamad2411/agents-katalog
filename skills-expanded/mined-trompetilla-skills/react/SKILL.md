---
name: React
description: Build fast, accessible React apps with hooks, state, and component patterns.
metadata: {"clawdbot":{"emoji":"⚛️","requires":{"bins":["node"]},"os":["linux","darwin","win32"]}}
---

# React Production Rules

## Common Mistakes
- `{count && <Component />}` renders "0" when count is 0 — always use `{count > 0 && <Component />}` for numeric conditions
- Never mutate state directly (`array.push()` then `setState(array)`) — React won't detect the change. Always spread: `setState([...array, item])`
- Keys generated during render (`key={Math.random()}`) destroy and recreate components every render — generate stable IDs when data is created
- Uninitialized controlled inputs (`useState()` without default) flip between controlled/uncontrolled — always initialize with empty string or appropriate default

## Hooks Traps
- `useEffect` callback cannot be async directly — define async function inside the effect and call it
- Missing cleanup in effects causes memory leaks — return cleanup function for subscriptions, intervals, and event listeners
- Dependencies array with objects/arrays triggers on every render (new reference each time) — memoize with `useMemo` or extract primitive values
- `useState` setter with same reference won't trigger re-render — for objects/arrays, always create new reference

## Performance
- Sequential awaits create waterfalls — use `Promise.all([fetchA(), fetchB()])` for independent requests
- Barrel imports (`import { X } from '@/components'`) pull entire module — use direct path imports for tree-shaking
- Expensive computations in render body recalculate every render — wrap in `useMemo` with proper dependencies
- Use `startTransition` for non-urgent UI updates (filtering, sorting large lists) — keeps input responsive while heavy renders process in background
- Use `useRef` instead of `useState` for values that don't need to trigger re-renders (timers, previous values, DOM measurements)

## State Architecture
- Colocate state as close as possible to where it's used — lifting state too high causes unnecessary re-renders in the entire subtree
- Derive values from existing state instead of syncing with useEffect — computed values don't need their own state
- When multiple state updates happen together, use `useReducer` — prevents impossible state combinations that separate `useState` calls allow
- URL search params are state too — use them for filter/sort/pagination state so users can share and bookmark

## Forms (React 19+)
- Prefer form actions over useEffect for mutations — actions handle pending states, errors, and optimistic updates built-in
- Use `useActionState` for form submission status — replaces manual loading/error state management
- `useOptimistic` updates UI immediately before server confirms — revert automatically on error

## Common Mistakes
- Fetching data in useEffect without abort controller — race conditions when component remounts or deps change fast
- Returning objects from custom hooks without memoizing — consumers re-render on every call even if data hasn't changed
- Using index as key in lists that reorder, filter, or insert — causes subtle bugs where component state gets attached to wrong items
