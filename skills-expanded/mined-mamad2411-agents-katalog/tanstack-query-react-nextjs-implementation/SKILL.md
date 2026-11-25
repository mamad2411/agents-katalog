---
name: tanstack-query-react-nextjs-implementation
description: "Implement React/Next TanStack Query changes to keys, cache, mutations, API integration, or hydration."
---

# TanStack Query React Next.js Implementation

Model React 19 and Next.js client-side server state explicitly with stable query keys, generated API contracts, safe cache invalidation, SSR-aware hydration, typed errors, and tested mutation behavior.

## Trigger boundary

Use this skill when a React/Next.js TanStack Query change alters query ownership, keys/options, generated API integration, cache invalidation, mutations, auth/tenant isolation, or SSR/hydration behavior. Detect repo-pinned React/Next/TanStack versions before choosing patterns.

Do not load it for a small local rename, comment, formatting change, or mechanical edit outside query/server-state behavior; follow the repository's established convention directly.

## Process

1. Inspect repo conventions, `.itsol.md`, React/Next/TanStack versions, generated OpenAPI client, auth model, query provider, tests, and CI before editing.
2. Use `itsol-current-tech-context` for TanStack Query, React, Next.js, Hey API, testing, or package-version decisions.
3. Decide whether TanStack Query owns the data. Use it for interactive client-side server state, not local UI state, form draft state, or static server-only data.
4. Prefer generated Hey API query keys/options when available; otherwise create domain query key and query options factories.
5. Implement the smallest coherent data flow with explicit loading, empty, error, stale/refetching, pending mutation, and auth/tenant behavior.
6. Verify success, error, invalidation, cache cleanup, and SSR/hydration behavior with tests or documented replacement verification.

## Coordination

Use with `react-nextjs-api-cache-forms`, `react-nextjs-app-router-rendering`, `react-nextjs-quality-security`, `hey-api-openapi-codegen`, `hey-api-openapi-review`, and `security-frontend-browser-review`.

## Focused References

- [01-model-setup-and-api-client.md](./references/01-model-setup-and-api-client.md) - Model Setup And API Client
- [02-query-keys-fetching-and-ssr.md](./references/02-query-keys-fetching-and-ssr.md) - Query Keys Fetching And SSR
- [03-mutations-optimism-and-realtime.md](./references/03-mutations-optimism-and-realtime.md) - Mutations Optimism And Realtime
- [04-auth-errors-tests.md](./references/04-auth-errors-tests.md) - Auth Errors And Tests
