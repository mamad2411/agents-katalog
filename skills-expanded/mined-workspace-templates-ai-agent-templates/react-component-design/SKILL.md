---
name: react-component-design
description: Designs and reviews React components for clean state, correct effects, composition and complete loading, empty and error states, in TypeScript.
---

# React component design

Write function components in TypeScript. Keep them small and boring.

## Steps

1. Define the job in one sentence. If it needs "and", split it into two components.
2. Type the props: required props first, no `any`, a discriminated union instead of several booleans (`status: 'idle' | 'loading' | 'error'`). Accept `children` or a slot prop instead of adding a prop per variation.
3. Place state at the lowest component that needs it. Do not store anything you can compute from props or other state; compute it during render (`useMemo` only after you measured).
4. Treat `useEffect` as a last resort. Never use it to transform data, reset state from props (use a `key`) or respond to a click (use the handler). Use it for subscriptions and syncing with outside systems, always with a cleanup and a complete dependency list. Fetch with the project's data library, not a bare effect.
5. Cover every data state: loading (skeleton or spinner), empty (a message and next action), error (readable text and retry), and success. Write them before the happy path.
6. Lists need stable `key` values from the data, never the index when order can change.
7. Prefer composition: pass components or render props instead of a config object that grows.
8. Make it accessible: native elements, labels, focus.

## Rules

- No prop drilling past two levels: use composition or context.
- Do not mutate props or state.

## Report

The component code, the states it handles, and anything you left to the caller.
