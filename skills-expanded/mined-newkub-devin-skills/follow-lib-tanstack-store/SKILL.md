---
name: follow-lib-tanstack-store
description: Use TanStack Store end to end — stores, selectors, derived state, batching, cross-framework
argument-hint: "[framework]"
related:
  - follow-lib-tanstack-ecosystem
  - run-test
  - run-typecheck
  - resolve-errors
---

## Goal

Use TanStack Store fully — a framework-agnostic client state store: stores, fine-grained selectors, `Derived` computed, `batch`, and non-React usage

## Scope

Use for **client state** (UI state, drafts, prefs, ephemeral) — for server state use `follow-query`/`follow-db`; a good Zustand-style store replacement when you're already in the TanStack ecosystem

- part of TanStack ecosystem — selection/dispatch lives in `/follow-lib-tanstack-ecosystem`

## Execute

### 1. Install

> Goal: install the store package and the framework adapter

```bash
bun add @tanstack/react-store   # adapter wraps the @tanstack/store core — solid/vue/svelte/angular available
```

### 2. Create Store

> Goal: typed store + derived state

```ts
import { Store, Derived } from '@tanstack/react-store'

export const appStore = new Store({
  theme: 'dark' as 'dark' | 'light',
  sidebarOpen: false,
  todos: [] as Todo[],
})

// computed — recomputes when deps change
export const openCount = new Derived({
  fn: () => appStore.state.todos.filter((t) => !t.done).length,
  deps: [appStore],
})
openCount.mount()
```

### 3. Read, Write, Batch

> Goal: fine-grained reactivity

```tsx
const theme = useStore(appStore, (s) => s.theme)  // always a selector — re-render only the slice

appStore.setState((s) => ({ ...s, theme: 'light' }))

batch(() => {                          // collapse into one notification
  appStore.setState((s) => ({ ...s, sidebarOpen: true }))
  otherStore.setState((s) => ({ ...s, loaded: true }))
})
```

- Read outside a component: `appStore.state` (sync, non-reactive)
- `store.subscribe` for side-effects outside the framework

### 4. Patterns

> Goal: real-world usage covered

1. **Modular stores**: split stores by domain (`userStore`, `uiStore`) — not one god-store
2. **Action functions**: export an `updateTheme()` helper next to the store instead of scattering `setState` across the codebase
3. **Persist**: subscribe → `localStorage` or pair with a DB `localStorageCollectionOptions`
4. **Outside React**: the core `Store` works in vanilla/node — adapters are only needed when binding to the UI
5. **Testing**: create a fresh store instance per test, or reset via `setState` in `beforeEach`

### 5. Verify

> Goal: prove selector-driven granular re-render works before finishing

1. `/run-typecheck` + `/run-test`
2. Selector granularity — other components don't re-render when an unrelated slice changes
3. If it fails → `/resolve-errors` max 3 rounds

## Rules

- `useStore(store, selector)` — the selector is mandatory, otherwise every change re-renders
- Never mutate `store.state` directly — use `setState` only
- `Derived` must `.mount()`; derived-from-derived works (chain)
- Store = a module singleton export — never create it inside a component
- Never put server state in a Store — `follow-query`; a reactive client DB → `follow-db`

## Expected Outcome

- Client state is reactive, granular re-render via selectors
- Derived/batch used in the right places
- The boundary with Query/DB is clear
