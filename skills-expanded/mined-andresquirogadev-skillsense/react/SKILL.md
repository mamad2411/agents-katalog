# React Skill

You are working in a React codebase. Apply these patterns and conventions.

## Component Design

- Write functional components with named exports. Avoid class components.
- Keep components small and focused: one concern per component.
- Extract reusable logic into custom hooks (`use` prefix, return an object for multiple values).
- Co-locate component state as close as possible to where it is used.

## Hooks

- Follow the Rules of Hooks: only call hooks at the top level, never inside conditions or loops.
- Use `useState` for simple local state; `useReducer` for complex state with multiple sub-values.
- Use `useCallback` to stabilize callbacks passed as props to memoized children.
- Use `useMemo` only when profiling shows an actual performance problem.
- Prefer `useId()` over manual IDs to avoid hydration mismatches.

## State Management

- For global state, prefer React Context + `useReducer` for small apps; use Zustand or Jotai for larger ones.
- Avoid prop drilling more than 2–3 levels deep — reach for Context or a state library.
- Keep server state in a dedicated library (TanStack Query, SWR) rather than manually managing loading/error/data.

## React 19 Features

- Use `useActionState` for form actions and loading states — replaces `useFormState`.
- Use `use(promise)` to read async data from Server Components passed as props.
- Use `useOptimistic` for instant UI feedback on mutations.
- `ref` is now a regular prop; no need for `forwardRef` in React 19.

## Performance

- Wrap expensive pure components with `React.memo`.
- Use `key` on list items; never use array index as key for dynamic lists.
- Use `<Suspense>` for lazy-loaded components and async operations.
- Use `startTransition` to mark non-urgent state updates and keep the UI responsive.

## Patterns to Avoid

- Never mutate state directly — always return a new value.
- Never use `index` as key in a list that can be reordered or filtered.
- Never fetch data inside `useEffect` without cleanup; prefer TanStack Query.
- Never create components inside render — they will remount on every render.
