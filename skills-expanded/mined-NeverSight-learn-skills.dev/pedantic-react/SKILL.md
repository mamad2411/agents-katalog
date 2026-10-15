---
name: pedantic-react
description: Opinionated React and TypeScript conventions for JSX, hooks, routing, shared state, and query wiring. Use for style cleanups, refactors, review feedback, or code generation.
---

# Pedantic React

Opinionated house style for React + TypeScript frontends.

## TypeScript

- Prefer explicit types at all boundaries (props, return types, API responses).
- Use `import type` for type-only imports.
- Type component props explicitly with `interface`. Use `PropsWithChildren` when children are accepted.
- Wrap component prop inputs in `Readonly<...>`.
- Prefer `unknown` over `any`; narrow with type guards.
- Avoid non-null assertions (`!`); prefer optional chaining and explicit guards.

## Imports

- Prefer a `@/` alias for imports from `src/`.
- Group imports: external libraries → internal modules → types. Separate groups with a blank line.
- All imports at the top of the file, never inline or inside try blocks.
- Prefer named exports for components and hooks. Avoid default exports; reserve them only for entrypoints, reducers, or interop files that require them.

## JSX

- Prefer rendering variables over inline conditions. Derive named booleans before the return:
  `const showBanner = isLoaded && hasError && !isDismissed` then `showBanner ? <Banner /> : null`.
- For a collection of flags, prefer `[a, b, c].every(Boolean)` or `[a, b, c].some(Boolean)` over chaining `&&` or `||`.
- Never use nested ternaries. Use `if` statements or rendering variables for anything beyond a single obvious ternary.
- Prefer `condition ? <Thing /> : null` over `condition && <Thing />`.
- Remove all instances of `{' '}` or `{" "}`, use layout gap, margin, or padding instead.
- Prefer destructuring to prop drilling. Stop drilling beyond two levels; lift state or use shared state instead.
- Prefer composition and small focused helpers over large boolean-heavy JSX branches.
- Keep JSX return values small; extract sub-trees into named components when a render block grows unwieldy.
- Prefer named handler functions over inlined arrow functions. Extract to a handler when the body reaches 3+ lines or is async:
  `const handleSubmit = async () => { ... }` rather than `onClick={async () => { ... }}`.
- For fire-and-forget async handlers, use `void` to avoid blocking: `void handleSubmit()`.

## Components and hooks

- Prefer named `export function` declarations.
- Destructure props in the function signature or immediately at the top of the function body. Do not thread `props.foo` chains.
- Prefer full variable names over abbreviations.
- Avoid comments that merely restate the code.
- Co-locate a custom hook with the component that owns it unless it is reused.
- Before creating a new component, enumerate what exists and confirm nothing covers the use case.
- Prefer existing page, hook, query, type, and layout patterns over new abstractions.

## `useEffect`, the last resort

`useEffect` is almost never the right tool. Work through this list first:

| Problem | Prefer instead |
|---|---|
| Derived value from state or props | Compute inline during render; `useMemo` if expensive |
| Fetching data | TanStack Query |
| Resetting state when a prop changes | `key` prop to remount, or compute during render |
| Syncing with an external store | `useSyncExternalStore` |
| DOM measurements before paint | `useLayoutEffect` |
| Triggering animations | `useLayoutEffect` or a dedicated animation hook |

`useEffect` is appropriate only for genuine external side effects with cleanup, event listeners, WebSocket connections, third-party library setup, or browser APIs that have no React abstraction. If there is no cleanup and no external system, it is almost certainly the wrong choice.

Never use `useEffect` to sync one piece of state into another, that is always a sign the state model needs restructuring.

## State and data ownership

- Prefer local state first.
- Lift state only when two or more components genuinely share it.
- Prefer Redux (or equivalent global store) for shared non-serializable state or when an existing slice already owns that UI state. Do not duplicate it in local state.
- Use TanStack Query for all server state. Keep `queryOptions(...)` factories in a dedicated `query/` directory. Do not put fetch results in Redux.
- Keep server state separate from UI state, do not mix fetch results into UI slices.
- Keep HTTP access in a dedicated `api/` layer. Components should not call `fetch` directly.
- Keep contract types in `src/types/`. Do not invent frontend-only API contracts, align with the actual producer.
- Prefer optimistic UI updates for mutations that are unlikely to fail. Roll back on error using the query client's `onMutate` / `onError` pattern.

## Routing

- Validate search params explicitly at the route level.
- Derive loader dependencies from search/route state rather than component effects.
- Preload with route loaders when route state is required before render.
- Preserve route and layout structure unless the task intentionally changes it.

## Error and loading states

- Always handle loading, error, and empty states explicitly, avoid silent no-ops.
- Prefer graceful missing-data behavior over throwing or crashing.
- Surface errors at the boundary closest to the user action.

## Review checklist

- JSX conditionals written as ternaries returning `null` instead of `&&`?
- No nested ternaries, replaced with rendering variables or `if` statements?
- Multi-flag conditions use `[].every(Boolean)` / `[].some(Boolean)` where readable?
- No stray `{' '}` or `{" "}` spacer nodes?
- Props destructured at the boundary? No drilling beyond two levels?
- Async handlers named and invoked with `void` where fire-and-forget?
- Inline arrow functions 3+ lines extracted to named handlers?
- Could any `useEffect` be replaced with derived state, `useMemo`, `useLayoutEffect`, `useSyncExternalStore`, or TanStack Query?
- Server state owned by TanStack Query, not local state or Redux?
- Mutations use optimistic updates where failure is unlikely?
- Shared state stays local unless a global store was actually warranted?
- Imports use `@/` and `import type` where appropriate?
- Loading, error, and empty states all handled?
- No frontend-only API contracts invented, types align with the actual producer?
- Change preserves the app's routing and data-loading model?
- Before creating a component, was the existing component inventory checked?
