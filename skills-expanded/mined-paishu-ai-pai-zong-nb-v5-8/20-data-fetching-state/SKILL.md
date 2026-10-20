---
name: data-fetching-state
description: Design and implement client-side data fetching and server state for API-driven desktop and web apps: caching, invalidation, optimistic updates, polling, subscriptions, pagination, stale data, offline behavior, and request race handling.
---

# Data Fetching State

## Workflow

1. Classify data as server state, client UI state, form draft, or local persisted state.
2. Choose existing project tooling: TanStack Query, SWR, RTK Query, Apollo, custom store, or native async patterns.
3. Define cache keys, invalidation rules, stale time, retry behavior, and background refresh.
4. Handle race conditions, cancellation, duplicated requests, and auth expiry.
5. Decide whether optimistic updates are safe; provide rollback if used.

## Required Checks

- Do not duplicate server state across unrelated stores without a reason.
- Keep loading, refetching, stale, error, and saving states distinct.
- Use cursor pagination when the API supports it for changing datasets.
- Avoid polling when events, webhooks, or push channels already exist and are reliable.
- Make destructive mutations invalidate or update affected queries.

## Output

State state categories, fetch strategy, cache/invalidation behavior, mutation behavior, and tests.
