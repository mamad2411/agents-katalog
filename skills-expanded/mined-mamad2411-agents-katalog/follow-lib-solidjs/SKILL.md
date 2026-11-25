---
name: follow-lib-solidjs
description: Develop Solid.js applications with fine-grained reactivity and performance optimization
argument-hint: "[task]"
related:
  - follow-create-web
  - follow-lang-typescript
  - follow-tool-vite
  - follow-create-plugins
  - follow-tool-vitest

---

## Goal

Develop Solid.js applications with fine-grained reactivity, the render-once mental model, and performance optimization

## Scope

For Solid.js projects that aren't SolidStart (client-side only or integrated with other frameworks)

- Latest: `solid-js@1.9.15` (stable), `2.0.0-rc.8` (next — release candidate), `1.10.0-beta.0` (beta) (verified 2026-09-18)

## Execute

### Workflows

> Goal: dispatch to the workflow matching the task

| Topic | Workflow |
|-------|----------|
| `setup`, `install`, `scaffold` | `workflows/setup-solid/SKILL.md` — vite-plugin-solid, JSX config, render root |
| `component`, `props`, `control-flow` | `workflows/build-components/SKILL.md` — render-once, `splitProps`, `<For>`/`<Show>`/`<Switch>` |
| `signal`, `store`, `memo`, `state` | `workflows/manage-state/SKILL.md` — `createSignal`, `createStore`, `createMemo`, `batch` |
| `async`, `resource`, `suspense`, `fetch` | `workflows/handle-async/SKILL.md` — `createResource`, `Suspense`, `useTransition`, `lazy` |
| `test`, `testing-library` | `workflows/test-solid/SKILL.md` — vitest, `@solidjs/testing-library`, `createRoot` |
| `migrate`, `2.0`, `upgrade` | `workflows/migrate-solid-2/SKILL.md` — Solid 1.x → 2.0 incremental migration |

### 1. Setup And Components

> Goal: component structure correct per the Solid.js mental model

1. Check `package.json` for `solid-js` and `babel-preset-solid`; if missing → install with `bun add solid-js` and `bun add -D babel-preset-solid`
2. Use functional components that run once (render-once); use `.tsx` for every component
3. Type with `Component<P>`, `VoidComponent<P>`, `ParentComponent<P>`, `FlowComponent<P, C>`
4. Never destructure props — use `mergeProps` to combine default props and `splitProps` when passing specific props, to preserve the getter chain

### 2. Reactivity And State

> Goal: use reactive primitives and state management correctly

1. Use `createSignal` for state management — set via function: `setCount(c => c + 1)`
2. Use `createMemo` only for expensive computations — simple derived values should be plain functions (Solid re-evaluates within the reactive scope)
3. Use `createEffect` for side effects only (DOM manipulation, third-party libraries) — never for syncing derived state
4. Use `createStore` for nested reactive state via Proxies — use `createMutable` for interop with external libraries (with caution)
5. Use `batch` to group multiple state updates, `untrack` to prevent dependencies, the `on` helper to manually specify effect dependencies
6. Use the Context API for global state — avoid deep nesting unless necessary

### 3. Control Flow And Async

> Goal: use control flow components and async patterns correctly

1. Use `<For>` for lists tracked by reference (keyed list), `<Index>` for lists with stable indices but changing values
2. Use `<Show>` for conditional rendering with the callback form for type narrowing, `<Switch>`/`<Match>` for complex conditions, `<Dynamic>` for dynamic component rendering
3. Avoid calling `map` and `filter` directly on reactive arrays
4. Use `createResource` for async data fetching (not `createEffect` to fetch) — use the `refetch` and `mutate` actions for cache control
5. Use `Suspense` for async data loading boundaries, `ErrorBoundary` for error handling
6. Use `createDeferred` to defer non-critical updates, `lazy` for code splitting and async component loading

### 4. Optimize Performance

> Goal: improve performance with Solid.js patterns

1. Use fine-grained updates (no Virtual DOM) — avoid reactive reads at the component top level except in JSX, `createMemo`, or `createEffect`
2. Use `<For>` and `<Index>` for efficient list rendering
3. Use `untrack` when you don't want to create dependencies
4. Use SSR and hydration for initial load performance if needed

### 5. Testing

> Goal: test Solid.js applications correctly

1. Use `@solidjs/testing-library` for component testing with auto cleanup
2. Use `@testing-library/user-event` to simulate user interactions, `@testing-library/jest-dom` for custom matchers
3. Use Vitest for unit testing — use `renderHook` to test primitives without rendering a component
4. Use `testEffect` for testing async effects — test reactive behavior with `createRoot` and `dispose`

## Rules

### 1. Render-Once Mental Model

- Components are functions that run once to set up the view
- Never destructure props — use `mergeProps` and `splitProps` to preserve the getter chain
- Use `.tsx` for every component
- Avoid re-running the component when state changes

### 2. Reactivity Rules

- Use `createEffect` for side effects only, not to sync derived state — use a function or `createMemo` instead
- Use `createMemo` only for expensive computations — for simple ones use a plain function
- Use `createResource` for async data fetching, not `createEffect`
- Use `batch` for grouped updates, the `on` helper to manually specify dependencies

### 3. Solid 2.0 Migration Notes

Prepare for Solid 2.0 (`2.0.0-rc.8` — release candidate, GA near):

- `Suspense` → `Loading`, `ErrorBoundary` → `Errored`
- `createResource` → async `createMemo` + `Loading` boundary
- `<Index>` is removed — use `<For keyed={false}>` instead
- `SuspenseList` → `Reveal` with the `order` prop (`sequential`, `together`) and `collapsed`
- `batch` → default microtask batching, use `flush()` instead
- `onMount` → `onSettled` (supports a cleanup return), `mergeProps`/`splitProps` → `merge`/`omit`, `unwrap` → `snapshot`
- `createMemo` changes signature: the second arg is options, not an initial value
- `onError` is deprecated → use `catchError` instead
- New: `action()`, `createOptimisticStore`, `isPending()`, `latest()`, `refresh()`, `deep()`
- rc.8 fixes SSR XSS: strings yielded through flow-control memos (`<Show>`/`<For>`/`<Switch>` fallbacks) are now escaped on the server — if using a 2.0 RC with SSR, pin `>=2.0.0-rc.8`

### 4. Related Workflows

- Do `/follow-solid-framework` for TanStack Start + SolidJS applications
- Do `/follow-lang-typescript` for TypeScript best practices
- Do `/follow-tool-vitest` for testing configuration

- Use /follow-tool-vite if needed
- Use /follow-create-vite-plugin if needed (lib solidjs)
- Use /follow-create-plugins if needed
- See best-practices/ for recommended patterns and pitfalls


## Expected Outcome

- Solid.js components developed per the render-once mental model
- Reactivity system used correctly (no derived state in effects)
- Performance optimization via fine-grained updates
- Control flow and async patterns used appropriately
- Complete testing setup with `@solidjs/testing-library`
- Prepared for the Solid 2.0 migration
