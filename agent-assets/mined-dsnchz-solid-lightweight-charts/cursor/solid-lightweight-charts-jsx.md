---
description: 
globs: *.tsx
alwaysApply: false
---

You are an expert in JSX libraries like React and SolidJS and understand the differences between the two.

API differences in React vs Solid

- React has `useState`, Solid has `createSignal`
- React has `useEffect`, Solid has `createEffect`
- React has `useMemo`, Solid has `createMemo`
- React has `useRef`, Solid supports native ref value assignment.
- In React, when using `useState` you get a value/setter tuple. 
- In Solid, when using `createSignal`, you get a getter/setter tuple.
- In React, you iterate through lists in JSX to create elements. In Solid, you can use either `For`, `Index` or `Switch` control flow components.
- In React, you can conditionally show JSX by evaluating a JS expression within JSX. In Solid, you use the `Show` or `Suspense` component.

SolidJS Conventions

- Never destructure props. You must use `splitProps` for that.
- Use `mergeProps` to assign default values for optional props when necessary.
- Avoid direct value assignments derived from prop values inside of a JSX/TSX components. Use getter/accessor functions that return values as those are "read-only" signals.
