---
name: react-performance-optimization
description: Finds needless React re-renders with the Profiler and adds memoization only where a measurement shows it pays off.
---

# React performance optimization

Measure, find the cause, make the smallest change, measure again.

## Steps

1. Reproduce the slow interaction and describe it precisely (typing, scroll, route change). Record a Profiler trace for it, or add a temporary `<Profiler onRender>` and log `actualDuration`. Note the baseline in milliseconds and render counts.
2. Identify the top offenders: components rendering most often or taking longest. For each ask why it rendered (state change, parent render, context change, new prop identity). Use "Highlight updates" or `why-did-you-render` if installed.
3. Fix in this order:
   - Move state down to the component that needs it, or lift expensive static children up as `children`.
   - Split a context so consumers of one value do not re-render for another.
   - Stabilize props only where a memoized child receives them: `useCallback` and `useMemo` for functions and objects.
   - Wrap a component in `React.memo` only when the profile shows it re-renders with unchanged props and costs real time.
   - Virtualize long lists (react-window or TanStack Virtual) instead of memoizing rows.
   - Use `useDeferredValue` or `startTransition` for expensive filtering from an input.
   - Split heavy routes with `lazy` and `Suspense`.
4. Never use array index as key for reorderable lists; use stable ids.
5. Re-profile and compare against the baseline.

## Rules

- No optimization without a number before and after.
- Remove any memo or callback wrapper that did not move the number.
- Do not mutate state to avoid renders.

## Report

Baseline versus result, each change with the reason, and the changes you tried and reverted.
