---
description: React hooks correctness and performance practices (cleanup, memoization, code splitting).
globs: "app/**/*.tsx, components/**/*.tsx, hooks/**/*.ts"
alwaysApply: false
---

## React hooks best practices (critical)
- Never call hooks conditionally; hooks must be top-level and stable order.
- All early returns must happen after hooks are declared.
- Use `useCallback` for functions used inside effects and include proper dependencies.
- Always clean up event listeners/observers/timeouts/intervals in `useEffect` cleanup.

## Performance optimization
- Minimize bundle size using code splitting and `next/dynamic` for non-critical UI.
- Avoid unnecessary re-renders (memoize expensive computations; keep props stable).
- Use proper caching strategies (React Query keys must be centralized).
