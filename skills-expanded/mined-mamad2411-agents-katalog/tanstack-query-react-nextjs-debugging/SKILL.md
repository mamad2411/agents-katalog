---
name: tanstack-query-react-nextjs-debugging
description: "Diagnose React/Next TanStack Query stale data, hydration, invalidation, or cache isolation failures."
---

# TanStack Query React Next.js Debugging

For bugfix authorization and plan prerequisites, defer to `itsol-workflow-mode`; retain evidence, root-cause analysis, proportionate verification, and final review in every mode.

Trace React 19 and Next.js TanStack Query failures from query key to query function, API error mapping, cache state, invalidation, SSR hydration, auth scope, and rendered UI before changing behavior.

## Trigger boundary

Use this skill when React/Next.js TanStack Query behavior diverges across query keys/functions, API errors, cache or invalidation, SSR/hydration, auth/tenant scope, or rendered UI. Detect repo-pinned React/Next/TanStack versions before judging behavior.

Do not load it for a small local edit with a deterministic cause and no query, cache, hydration, auth-scope, reactivity, or rendered-state behavior change; follow the repository's established convention directly.

## Process

1. State expected behavior, actual behavior, affected route/component, user/tenant context, environment, and smallest reproducible symptom.
2. Gather evidence from React Query Devtools, Network tab, browser console, server logs, request ids, package versions, generated API output, tests, and route/server component code.
3. Use `itsol-current-tech-context` when symptoms depend on TanStack Query, React, Next.js, Hey API, or package versions.
4. Classify the failure: key, query function, enabled/dependency, invalidation, mutation, optimistic update, hydration, auth/tenant cache, realtime, persistence, or performance.
5. Fix one root cause and verify with a regression test or documented replacement verification.
6. Use `itsol-bug-debugging`; in `governed`, require an approved Technical Fix Plan before implementation, while autonomous/direct prerequisites come from `itsol-workflow-mode`.

## Coordination

Use with `react-nextjs-debugging`, `react-nextjs-api-cache-forms`, `react-nextjs-app-router-rendering`, `react-nextjs-quality-security`, `hey-api-openapi-contract-debugging`, and `security-frontend-browser-review`.

## Focused References

- [01-evidence-and-failure-classes.md](./references/01-evidence-and-failure-classes.md) - Evidence And Failure Classes
- [02-debugging-questions-and-fix.md](./references/02-debugging-questions-and-fix.md) - Debugging Questions And Fix
