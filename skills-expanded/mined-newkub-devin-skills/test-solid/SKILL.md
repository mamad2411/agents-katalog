---
name: follow-lib-solidjs-test-solid
description: Test SolidJS — @solidjs/testing-library, vitest config, user-event, assertions on fine-grained DOM
argument-hint: "[scope]"
related:
  - follow-lib-solidjs
  - run-test
  - resolve-errors
  - improve
---

## Goal

Write tests for SolidJS — `@solidjs/testing-library`, vitest browser/jsdom setup, user interactions, async assertions

## Scope

component + signal testing — vitest + `@solidjs/testing-library` + jsdom/happy-dom; e2e → the Playwright skill

## Execute

### 1. Setup

```bash
bun i -D vitest @solidjs/testing-library jsdom @testing-library/jest-dom @testing-library/user-event
```

```ts
// vite.config.ts — test section (vitest reads vite config)
export default defineConfig({
  plugins: [solid()],
  test: { environment: 'jsdom', globals: true },
  resolve: { conditions: ['development', 'browser'] },  // solid ssr/browser conditions
})
```

- `conditions: ['development', 'browser']` — solid must pick the (web) entry in the test env
- jest-dom setup file: `import '@testing-library/jest-dom/vitest'`

### 2. Render And Assert

```tsx
import { render, screen, fireEvent } from '@solidjs/testing-library'

it('increments', () => {
  const { unmount } = render(() => <Counter />)
  fireEvent.click(screen.getByRole('button'))
  expect(screen.getByText('Count: 1')).toBeInTheDocument()
  unmount()
})
```

- `render(() => <Comp />)` — must be a function (render-once semantics)
- `screen` queries — `getByRole`/`getByText`/`findBy*` (async); `container` direct access
- `fireEvent` / `user-event` — interactions; async updates flush automatically (no React-style act())

### 3. Testing Signals And Stores

```ts
import { createRoot } from 'solid-js'

it('signal', () => createRoot(dispose => {
  const [v, setV] = createSignal(0)
  setV(1); expect(v()).toBe(1)
  dispose()
}))
```

- Primitives must live inside `createRoot` or a component — test directly through a root wrapper
- Store tests: assert through proxy reads; async resources: trigger `refetch`/`mutate` then assert state

### 4. Async And Boundaries

- `await screen.findByText(...)` — resources resolving
- Suspense tests: assert fallback → content; `ErrorBoundary` — throw inside a component then assert the fallback
- `vi.useFakeTimers()` — debounce/async timing

## Rules

- `render(() => <X/>)` — the function wrapper is mandatory (not a bare `<X/>`)
- `conditions` in the vite config matters — without it, resolution picks the node/SSR entry → tests break
- There is no `act()` — Solid updates are synchronous; `await` only for async finders/microtasks
- Test primitives through `createRoot` — don't create signals outside a reactive root in tests

## Expected Outcome

- Component tests render + interact + assert through testing-library
- Signals/stores/resources testable via `createRoot` and async finders
