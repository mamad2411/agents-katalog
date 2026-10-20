---
name: server-state-fetching
description: Fetch and cache server data in the frontend. Use when implementing
  data fetching and mutations in web apps.
metadata:
  tags: server, state, fetching
---

# Server State & Data Fetching

## Use this skill when
- Fetching data with loading/error/empty states
- Implementing cache invalidation and refetching
- Handling optimistic updates
- Building pagination and infinite queries

## Do not use this skill when
- State lives entirely client-side
- You are doing SSR/SSG data fetching (use nextjs-development)

## Instructions
1. Use a server-state client (React Query, SWR, TanStack Query).
2. Define stable query keys that uniquely identify the data.
3. Invalidate cache after mutations, or update optimistically.
4. Expose loading, error, empty, and stale states as explicit UI states.
5. Use infinite queries for paginated lists.
6. Prefetch data before navigation for perceived speed.
7. Keep queries co-located with the components that use them.

## Checklist
- Every query has loading and error UI
- Mutations invalidate the correct keys

## Output Format
- Query inventory | keys | invalidation strategy | component mapping

## Common Mistakes
- Fetching in effects and re-implementing caching
- Forgetting to invalidate after mutations
- Silently failing on errors
