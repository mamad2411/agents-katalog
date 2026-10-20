---
name: follow-lib-tanstack-pacer
description: Use TanStack Pacer end to end — debounce, throttle, rate limit, queue, batch — hooks and core classes
argument-hint: "[framework] [utility]"
related:
  - follow-lib-tanstack-ecosystem
  - run-test
  - run-typecheck
  - resolve-errors
---

## Goal

Use TanStack Pacer fully — debounce, throttle, rate limit, queue, batch across both React hooks and framework-agnostic core classes

## Scope

Use instead of ad-hoc `setTimeout` utilities — search inputs, scroll/resize, API rate limiting, sequential tasks, batched updates — **0.x**: verify the latest API in the docs before implementing

- part of TanStack ecosystem — selection/dispatch lives in `/follow-lib-tanstack-ecosystem`

## Execute

### 1. Install

> Goal: install the pacer package

```bash
bun add @tanstack/react-pacer   # React hooks; core @tanstack/pacer for non-React/vanilla
```

### 2. Core Utilities

> Goal: pick the tool by semantics

| Tool | Semantics | Use case |
|------|-----------|----------|
| `useDebouncedCallback`/`useDebouncedState` | keeps the last call after `wait` of silence | search input, resize end |
| `useThrottledCallback`/`useThrottledValue` | at most 1 call per `wait` | scroll position, mouse move |
| `useRateLimiter`/`RateLimiter` | hard cap `limit` per `window` | API quota, login attempts |
| `useQueuer`/`Queuer` | sequential/concurrency-limited | upload queue, job processing |
| `useBatcher`/`Batcher` | collapse rapid events into a batch | bulk inserts, analytics flush |

```tsx
const onSearch = useDebouncedCallback((q: string) => api.search(q), { wait: 300 })
const onScroll = useThrottledCallback(() => sync(), { wait: 100 })
const limiter = useRateLimiter(call, { limit: 5, window: 1000 })
```

Core (non-hook): `new Debouncer(fn, { wait })`, `debounce(fn, opts)` from `@tanstack/pacer`

### 3. Options And Control

> Goal: fine-tune behavior

1. `leading`/`trailing` edges — default trailing; `leading: true` = call immediately on the first trigger
2. `enabled` flag — pause/resume conditionally
3. Queuer: `concurrency`, `started` state, `getAllItems()`; Batcher: `maxSize` or `wait` trigger
4. Hooks auto-cancel on unmount; core classes must call `.cancel()` themselves

### 4. Testing Patterns

> Goal: make timing logic testable

1. `vi.useFakeTimers()` + `advanceTimersByTime` — verify `wait`/`window` semantics
2. Test trailing vs leading separately
3. Queue/batch → assert call counts after flush

### 5. Verify

> Goal: prove debounce/throttle/queue/batch behave as configured before finishing

1. `/run-test` with fake timers + `/run-typecheck`
2. Edge behavior (leading/trailing) matches options
3. If it fails → `/resolve-errors` max 3 rounds

## Rules

- Debounce ≠ throttle ≠ rate limit ≠ queue ≠ batch — choose by semantics, not approximation
- Set `wait` to real UX needs: search ~300ms, scroll/resize 50-150ms
- Never debounce actions that need immediate feedback (submit button)
- Test timing with fake timers always — never `await sleep()` for real

## Expected Outcome

- Tools match semantics + timing is correct
- No hand-rolled debounce/throttle left in the codebase
- Timing logic has tests
