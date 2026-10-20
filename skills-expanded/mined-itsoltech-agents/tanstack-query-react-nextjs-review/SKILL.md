---
name: tanstack-query-react-nextjs-review
description: "Review React/Next TanStack Query changes to keys, hydration, mutations, cache scope, or behavior tests."
---

# TanStack Query React Next.js Review

Review React 19 and Next.js TanStack Query changes for stable keys, correct query functions, generated API usage, SSR/hydration safety, mutation side effects, cache invalidation, optimistic rollback, auth/tenant cache safety, errors, performance, and tests.

## Trigger boundary

Use this skill when a React/Next.js TanStack Query diff changes query keys/options, generated API usage, SSR/hydration, mutations/invalidation, optimistic updates, auth/tenant cache scope, performance, or tests. Detect repo-pinned React/Next/TanStack versions before judging patterns.

Do not load it for a small local rename, comment, formatting change, or mechanical edit outside query/server-state behavior; follow the repository's established convention directly.

## Process

1. Inspect the diff, surrounding query factories, generated API client, QueryClient provider, auth/session flow, route/server component boundary, tests, and CI config before applying checklist items.
2. Use `itsol-current-tech-context` for findings that depend on TanStack Query, React, Next.js, Hey API, or testing package versions.
3. Build a coverage map: ownership, QueryClient, query keys/options, API client/errors, SSR/hydration, mutations, invalidation, optimistic updates, realtime, auth/logout/tenant, security, performance, tests, and CI.
4. Lead with concrete findings by severity, with file reference, affected behavior, and required fix or verification.
5. Treat missing query-key scope, missing invalidation, stale auth cache, and unsafe hydration as correctness or security risks, not style issues.

## Coordination

Use with `react-nextjs-review`, `react-nextjs-api-cache-forms`, `react-nextjs-app-router-rendering`, `react-nextjs-quality-security`, `hey-api-openapi-review`, and `security-frontend-browser-review`.

## Focused References

- [01-review-scope-blockers-findings.md](./references/01-review-scope-blockers-findings.md) - Review Scope Blockers And Findings
- [02-queryclient-keys-api-errors.md](./references/02-queryclient-keys-api-errors.md) - QueryClient Keys API And Errors
- [03-ssr-mutations-auth-tests.md](./references/03-ssr-mutations-auth-tests.md) - SSR Mutations Auth And Tests
