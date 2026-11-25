---
name: graphql-schema
description: Generates or reviews a GraphQL schema with types, queries, mutations, and resolvers
argument-hint: <entity-or-review>
user-invocable: true
allowed-tools: Read Glob Edit Grep
effort: medium
---

## GraphQL Schema

Target: **$ARGUMENTS**

1. Detect GraphQL setup:
```bash
cat package.json | grep -E '"graphql"|"apollo-server"|"pothos"|"nexus"|"typegraphql"|"@graphql-yoga"'
ls src/graphql/ src/schema/ 2>/dev/null | head -10
```

2. If reviewing existing schema:
   - N+1 problem: resolvers fetching data per parent field
   - Missing `DataLoader` for batched queries
   - Over-exposed fields (internal IDs, timestamps that shouldn't be public)
   - Missing pagination (connections pattern)
   - Mutations not returning the updated entity

3. If generating new schema for `$ARGUMENTS`:

```graphql
type $ARGUMENTS {
  id: ID!
  # ... fields
  createdAt: DateTime!
  updatedAt: DateTime!
}

type Query {
  $ARGUMENTS(id: ID!): $ARGUMENTS
  ${ARGUMENTS}s(first: Int, after: String, filter: ${ARGUMENTS}Filter): ${ARGUMENTS}Connection!
}

type Mutation {
  create$ARGUMENTS(input: Create${ARGUMENTS}Input!): ${ARGUMENTS}MutationResult!
  update$ARGUMENTS(id: ID!, input: Update${ARGUMENTS}Input!): ${ARGUMENTS}MutationResult!
  delete$ARGUMENTS(id: ID!): Boolean!
}
```

4. Generate resolver stubs and DataLoader for the entity.

5. Add input validation and proper error types.
