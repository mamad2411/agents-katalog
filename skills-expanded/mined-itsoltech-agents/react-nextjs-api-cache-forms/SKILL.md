---
name: react-nextjs-api-cache-forms
description: "Implement React/Next API state and forms with TanStack Query, Hey API, and validation."
---

# React Next.js API Cache Forms

Implement, debug, or review React 19 and Next.js data flows with explicit ownership between OpenAPI-generated clients, API wrappers, Next.js server cache, TanStack Query client cache, mutations, forms, validation, and error mapping.

## Process

1. Inspect API contract source, generated client, query key factory, API wrapper, auth model, form library, cache policy, and tests before editing.
2. Use `itsol-current-tech-context` for TanStack Query, Hey API, Next.js data/cache, or form-library behavior.
3. Decide which layer owns each data category: Server Component/Next cache, Client Component/TanStack Query, form draft, URL state, realtime updates, or public runtime config.
4. Prefer generated Hey API code for OpenAPI-covered endpoints; handwritten wrappers should add auth, base URL, error mapping, telemetry, retry, or runtime config behavior.
5. Verify cache keys, invalidation, rollback, field errors, double submit, logout cleanup, and SSR/hydration privacy when relevant.

## Coordination

Use with `react-nextjs-implementation`, `react-nextjs-app-router-rendering`, `hey-api-openapi-codegen`, `hey-api-openapi-review`, `react-nextjs-quality-security`, and `security-api-input-review`.

## Focused References

- [01-data-cache-and-hydration.md](./references/01-data-cache-and-hydration.md) - Data Cache And Hydration
- [02-api-client-and-openapi.md](./references/02-api-client-and-openapi.md) - API Client And OpenAPI
- [03-forms-and-state-boundaries.md](./references/03-forms-and-state-boundaries.md) - Forms And State Boundaries
