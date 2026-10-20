---
name: meilisearch-index
description: "Index and search documents with typo-tolerant full-text search using Meilisearch at {{MEILISEARCH_HOST}}:{{MEILISEARCH_PORT}}."
metadata:
  openclaw:
    emoji: "🔎"
---

# Meilisearch Index

Meilisearch is available at `http://{{MEILISEARCH_HOST}}:{{MEILISEARCH_PORT}}` within the Docker network.

## Add Documents

```bash
curl -X POST "http://{{MEILISEARCH_HOST}}:{{MEILISEARCH_PORT}}/indexes/movies/documents" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MEILISEARCH_API_KEY" \
  -d '[{"id": 1, "title": "Inception", "genre": "sci-fi"}]'
```

## Search

```bash
curl -X POST "http://{{MEILISEARCH_HOST}}:{{MEILISEARCH_PORT}}/indexes/movies/search" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MEILISEARCH_API_KEY" \
  -d '{"q": "incption", "limit": 10}'
```

## Tips for AI Agents

- Meilisearch handles typos gracefully — no need for exact matches.
- Configure searchable and filterable attributes for optimal results.
- Use faceted search for aggregated filtering.
