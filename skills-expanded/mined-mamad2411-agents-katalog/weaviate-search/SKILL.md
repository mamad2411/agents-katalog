---
name: weaviate-search
description: "Perform hybrid vector and keyword search using Weaviate at {{WEAVIATE_HOST}}:{{WEAVIATE_PORT}}."
metadata:
  openclaw:
    emoji: "🔮"
---

# Weaviate Search

Weaviate is available at `http://{{WEAVIATE_HOST}}:{{WEAVIATE_PORT}}` within the Docker network.

## Create a Class

```bash
curl -X POST "http://{{WEAVIATE_HOST}}:{{WEAVIATE_PORT}}/v1/schema" \
  -H "Content-Type: application/json" \
  -d '{"class": "Document", "vectorizer": "none", "properties": [{"name": "content", "dataType": ["text"]}]}'
```

## Add Objects

```bash
curl -X POST "http://{{WEAVIATE_HOST}}:{{WEAVIATE_PORT}}/v1/objects" \
  -H "Content-Type: application/json" \
  -d '{"class": "Document", "properties": {"content": "Hello world"}, "vector": [0.1, 0.2, 0.3]}'
```

## Search

```bash
curl -X POST "http://{{WEAVIATE_HOST}}:{{WEAVIATE_PORT}}/v1/graphql" \
  -H "Content-Type: application/json" \
  -d '{"query": "{Get {Document(nearVector: {vector: [0.1, 0.2, 0.3]}, limit: 5) {content}}}"}'
```

## Tips for AI Agents

- Weaviate supports hybrid search combining vector and BM25 keyword search.
- Use GraphQL for complex queries with filters and aggregations.
- Multi-tenancy enables isolated datasets per tenant.
