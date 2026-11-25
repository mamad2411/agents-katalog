---
name: react-hook
description: Creates a custom React hook with TypeScript types, tests, and usage example
argument-hint: <hook-name> [description]
user-invocable: true
allowed-tools: Read Glob Edit
effort: low
---

## Generate Custom React Hook

Hook name: **use$1** (auto-prefix `use` if not present)
Description: **$2**

1. Check existing hooks:
```bash
ls src/hooks/ 2>/dev/null | head -10
```
Read 1-2 existing hooks to match style.

2. Generate the hook:
   - Proper TypeScript generics if applicable
   - Return type explicitly typed
   - Cleanup in `useEffect` if subscriptions/listeners involved
   - Error and loading states if async
   - Stable callback references with `useCallback`
   - Memoized values with `useMemo` where appropriate

3. Generate a test using `@testing-library/react-hooks` or `renderHook`.

4. Add a usage example comment at the top:
```ts
/**
 * @example
 * const { data, isLoading } = useMyHook(id)
 */
```

5. Place in `src/hooks/use$1.ts` (or match project convention).
