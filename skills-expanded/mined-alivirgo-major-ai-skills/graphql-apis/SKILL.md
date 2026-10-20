---
name: graphql-apis
description: "Design GraphQL schemas and resolvers with authorization checks and N+1 query prevention."
category: development
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["graphql", "api", "schema", "resolvers", "dataloader", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# GraphQL APIs AI Skill Guide

## Overview & Engine Architecture

GraphQL exposes a typed schema (types, queries, mutations, subscriptions) where clients ask for exact fields. Servers resolve fields via resolvers; naive per-field DB access causes N+1 queries. Agents design schemas for product use cases, enforce authz at resolver/field level, batch loads (DataLoader), and treat persisted/allowlisted operations as a production hardening option.

```
Client query
    |
 GraphQL runtime (parse/validate/execute)
    |
 resolvers (+ DataLoader)
    |
 services / DB
```

## When to use this skill

- Designing or evolving GraphQL schemas
- Implementing resolvers without N+1 pathologies
- Adding authn/authz around sensitive fields
- Pairing GraphQL with Express, FastAPI, or Spring hosts

## Operational directives

1. Schema-first (or code-first with schema as contract) - clients depend on stable types.
2. Never trust client-provided IDs without authz checks in resolvers.
3. Batch and cache per-request DB lookups (DataLoader or equivalent).
4. Prefer pagination (`connection` / cursor) for lists that can grow.
5. Limit query depth/complexity in public APIs; disable introspection in prod if policy requires.

## Schema + resolver sketch

```graphql
type Item {
  id: ID!
  sku: String!
  qty: Int!
}

type Query {
  item(id: ID!): Item
  items(first: Int = 20): [Item!]!
}

type Mutation {
  createItem(sku: String!, qty: Int!): Item!
}
```

```ts
// Pseudocode resolver map
const resolvers = {
  Query: {
    item: (_: unknown, { id }: { id: string }, ctx: Ctx) => ctx.items.byId(id),
    items: (_: unknown, { first }: { first: number }, ctx: Ctx) =>
      ctx.items.list(Math.min(first, 100)),
  },
  Mutation: {
    createItem: async (_: unknown, args: { sku: string; qty: number }, ctx: Ctx) => {
      ctx.requireUser();
      return ctx.items.create(args);
    },
  },
};
```

## Commands

```bash
# Depends on stack - examples:
npm run codegen          # GraphQL Code Generator
npx rover graph check    # schema checks when using Apollo tooling
```

## Common pitfalls

| Pitfall | Why it hurts | Fix |
| --- | --- | --- |
| N+1 field resolvers | Latency explosion | DataLoader / joins |
| Auth only at gateway | Field leaks | Per-field/resolver checks |
| Unlimited list fields | DoS / huge payloads | Pagination + limits |
| Breaking field removals | Client outages | Deprecate first |

## Best practices

- Version via additive evolution; use `@deprecated` before removal.
- Colocate input validation with mutation args.
- Emit operation names in logs for supportability.
- Test resolvers with representative query documents, not only unit mocks.

## Limitations

- File uploads and subscriptions need transport-specific setup.
- Federated graphs add ownership and composition complexity.
- Caching differs from REST - think about persisted queries and CDN carefully.

## Related skills

- `@express` / `@fastapi` / `@spring-boot` - HTTP hosts
- `@prisma` - typed DB access behind resolvers
- `@playwright` - end-to-end against GraphQL-backed UIs
