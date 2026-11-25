---
name: extract-hook
description: Moves stateful logic out of a React component into a custom hook, keeps behavior identical and adds tests for the hook.
disable-model-invocation: true
---

Extract a custom hook from the component: $ARGUMENTS

1. Read the component. Group the `useState`, `useReducer`, `useEffect`, `useMemo` and `useCallback` calls by purpose. Pick the group that has no JSX dependency, or the one named in the arguments.
2. Name the hook `use` plus what it manages (`useDebouncedSearch`, not `useLogic`). Place it next to the component or in the project's hooks folder, following existing files.
3. Move the code unchanged first. Return only what the component needs, as an object for more than two values. Pass inputs as parameters; do not read from outer scope.
4. Preserve effect cleanup and dependency arrays exactly. Run the exhaustive-deps lint rule and fix real warnings.
5. Write tests with `renderHook` (Testing Library) covering the initial state, one update and cleanup on unmount.

Run the component's existing tests, the new hook tests and the type check. Report the hook's signature and any behavior you suspect was already buggy but left alone.
