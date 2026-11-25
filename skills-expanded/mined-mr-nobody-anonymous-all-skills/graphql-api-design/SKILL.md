---
name: graphql-api-design
description: "Design and evolve GraphQL APIs: schema modelling, nullability, pagination with connections, N+1 avoidance, and safe deprecation."
type: procedural
category: development
domain: development
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: advanced
triggers:
  - graphql schema design
  - graphql n+1 dataloader
  - graphql pagination cursor
  - graphql deprecation strategy
  - graphql mutation design
keywords:
  - graphql
  - schema
  - dataloader
  - pagination
  - deprecation
source: custom
enabled: true
---

# GraphQL API Design

## Purpose

Design and evolve GraphQL APIs: schema modelling, nullability, pagination with connections, N+1 avoidance, and safe deprecation.

## When to Use

- You are defining or changing a GraphQL schema consumed by clients.
- Resolver performance shows N+1 queries or excessive depth.
- A breaking change needs a migration path for existing clients.

## When NOT to Use

- The integration is a simple single-endpoint fetch where REST is sufficient.
- The team has no schema governance and cannot ship deprecations safely.
- You need streaming or file transfer semantics GraphQL handles poorly.

## Capabilities

- Model types around client use cases, with intentional nullability.
- Implement cursor pagination using the connection specification.
- Batch and cache resolver lookups to remove N+1 patterns.
- Deprecate and remove fields with a measured migration window.

## Inputs

- The schema and its consumers (web, mobile, third parties).
- The query patterns you must support and their expected cardinality.
- Current performance data: latency, query depth, resolver counts.

## Workflow

1. List the client use cases and derive types from them, not from database tables.
2. Mark only genuinely optional fields nullable; non-null enables better client code.
3. Add connection-style pagination for any list that can grow.
4. Batch lookups with a per-request loader and cap query depth/complexity.
5. Deprecate with `@deprecated(reason:)`, monitor usage, then remove.

## Tools

- graphql schema linter
- Apollo/urql devtools
- DataLoader

## Examples

- `npx graphql-inspector diff old.graphql new.graphql`
- `npx prettier --check schema.graphql`
- `npm run codegen`

## Safety

- Non-null fields are impossible to relax later without breaking clients.
- Unbounded list fields invite denial-of-service queries; always paginate.
- Never remove a field in the same release you deprecate it.

## Source

All-Skills canonical library (`skills/development/graphql-api-design`). First-party skill, maintained in this repository.

## Notes

- Schema diffing in CI catches accidental breaking changes early.
- Persisted queries reduce both payload size and attack surface.
- Pairs with: `development/api-mock-generator`, `integration/webhook-delivery-design`.
