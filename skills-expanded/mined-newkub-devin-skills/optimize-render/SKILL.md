---
name: follow-lib-react-optimize render
description: Optimize React renders — memo/useMemo/useCallback, React Compiler, profiling
argument-hint: "[scope]"
related:
  - follow-lib-react
  - follow-tool-react-scan
  - run-bench
  - run-profiler
  - report-before-after
---

## Goal

Cut unnecessary re-renders in a React app — `memo`/`useMemo`/`useCallback` discipline, React Compiler notes, and the profiling workflow

## Scope

Use when optimizing render performance of a React 19 app — covers baseline profiling, memoization discipline, compiler interplay, and verify (must measure before and after)

## Execute

### 1. Baseline And Profile

> Goal: identify the real re-render bottleneck before fixing — never guess

1. Use React DevTools Profiler or `react-scan` (`/follow-tool-react-scan`) — record the components that re-render often/slowly
2. Run `/deep-optimize` — separate the problems: unnecessary re-renders vs expensive render vs state scoped too wide
3. Capture baseline numbers (render count, render duration) for comparison after the fix

### 2. Fix Root Causes First

> Goal: fix structural issues before memoizing

1. Move state down closer to the components that use it (state colocation) — state held too high = the whole tree re-renders
2. Separate frequently changing components from static children — use children props / composition instead of memo
3. Use `useTransition`/`useDeferredValue` for expensive updates that aren't critical
4. Context: split contexts by how often their values change — a changed context value = every consumer re-renders

### 3. Apply Memoization Discipline

> Goal: use `memo`/`useMemo`/`useCallback` only where needed and at the right spots

1. If React Compiler is on (`babel-plugin-react-compiler`) — don't add new manual memoization; the compiler memoizes automatically; check lint with the latest `eslint-plugin-react-hooks`
2. Without the Compiler:
   - `React.memo` only for leaf components whose props are often unchanged and whose render is expensive
   - `useMemo` only for genuinely expensive computation — don't memo everything
   - `useCallback` only when the function is passed to a memoized child or sits in effect deps
3. Memoization doesn't help if props change every render — fix the parent first (stable references; don't create new inline objects/functions every render for memoized children)

### 4. Verify And Compare

> Goal: measure after the fix against the baseline

1. Profile again — render count/duration must decrease vs the baseline, shown with `/report-before-after`
2. Run tests — behavior must be unchanged (optimize ≠ change output)
3. If there's no improvement or a regression → revert that point and report

## Rules

- Always profile first — never add memoization without evidence
- Fix root causes (state placement, composition) before memoizing
- React Compiler + manual memoization don't mix — pick one per component
- No over-memoization — memoizing everything adds memory/complexity with no gain
- Always preserve behavior — `useMemo`/`useCallback` must have no side effects
- Use `/follow-lib-react` for React 19 standards

## Expected Outcome

- Re-render hotspots reduced vs the baseline, with real numbers
- Memoization used only where necessary — no over-memoization
- Behavior unchanged every time; tests pass
