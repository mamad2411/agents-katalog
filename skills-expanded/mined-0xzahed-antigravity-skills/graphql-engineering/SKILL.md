---
name: graphql-engineering
description: Engineer GraphQL APIs. Use when building, reviewing, or evolving a
  GraphQL service.
metadata:
  tags: graphql, engineering
---

# GraphQL Engineering

## Use this skill when
- Designing the schema and types
- Implementing resolvers and data loaders
- Handling auth, pagination, and complexity limits
- Optimizing N+1 and caching

## Do not use this skill when
- Non-GraphQL APIs
- Schema-level architecture decisions already made (use graphql-architect)

## Instructions
1. Design the schema from the client needs; keep it a shared contract.
2. Use batching/dataloaders to prevent N+1 queries.
3. Enforce query depth and complexity limits.
4. Handle auth at the field and object level per spec.
5. Implement connections for pagination with stable cursors.
6. Persisted queries for high-traffic, caching-friendly fetches.
7. Add error handling per spec: extensions codes for client errors.
8. Monitor resolver-level performance.

## Checklist
- Every query maps to bounded work
- No N+1 in hot queries

## Output Format
- Schema | resolver map | batching | limits | auth rules

## Common Mistakes
- “Fetch everything” resolvers hitting N+1
- Unbounded nested queries
- Business logic leaking into fields
