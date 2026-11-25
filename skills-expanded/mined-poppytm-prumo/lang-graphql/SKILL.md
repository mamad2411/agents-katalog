---
name: lang-graphql
description: GraphQL schema-first design, strict nullability, DataLoader batching (zero N+1), query depth/cost limiting, and cursor pagination.
---

# GraphQL Engineering & Safety Contract

## 1. Schema-First Design & Nullability
- Design schemas contract-first with explicit docstrings on all types, fields, and arguments.
- Treat nullability as an error-boundary: fields that can fail independently must be nullable (\`String\`), but IDs and immutable core properties should be non-null (\`ID!\`).
- Mutation payloads must return union types or domain payload objects containing result and user-facing errors.

## 2. N+1 Prevention & DataLoader
- Resolvers that fetch child relations must use \`DataLoader\` batching to collapse multiple single-record queries into batch lookups.
- Never issue unbatched SQL queries inside a field resolver loop.

## 3. Query Cost, Depth & Security
- Configure query depth limiting (e.g. max depth 7) and complexity/cost analysis to prevent recursive DOS attacks.
- Enforce cursor-based pagination (Relay specification: \`edges\`, \`node\`, \`pageInfo\`) on unbounded list fields.
- Disable schema introspection (\`__schema\`) in production environments.\n