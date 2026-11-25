---
name: graphql-query
description: "Query GraphQL APIs using curl."
metadata:
  openclaw:
    emoji: "◼️"
---

# GraphQL Query

Execute GraphQL queries against APIs.

## Query

```bash
curl -X POST "https://api.example.com/graphql" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"query": "{ users { id name email } }"}'
```

## Mutation

```bash
curl -X POST "https://api.example.com/graphql" \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { createUser(name: \"Alice\") { id name } }"}'
```

## Tips for AI Agents

- Use variables to parameterize queries: `{"query": "...", "variables": {...}}`.
- Use introspection to discover schemas: `{ __schema { types { name } } }`.
- GraphQL returns HTTP 200 even for errors — check the `errors` field.
