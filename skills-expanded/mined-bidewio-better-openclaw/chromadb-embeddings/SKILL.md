---
name: chromadb-embeddings
description: "Store and query vector embeddings using ChromaDB at {{CHROMADB_HOST}}:{{CHROMADB_PORT}}."
metadata:
  openclaw:
    emoji: "🎨"
---

# ChromaDB Embeddings

ChromaDB is available at `http://{{CHROMADB_HOST}}:{{CHROMADB_PORT}}` within the Docker network.

## Create a Collection

```bash
curl -X POST "http://{{CHROMADB_HOST}}:{{CHROMADB_PORT}}/api/v1/collections" \
  -H "Content-Type: application/json" \
  -d '{"name": "my_collection", "metadata": {"hnsw:space": "cosine"}}'
```

## Add Documents

```bash
curl -X POST "http://{{CHROMADB_HOST}}:{{CHROMADB_PORT}}/api/v1/collections/{collection_id}/add" \
  -H "Content-Type: application/json" \
  -d '{"ids": ["doc1"], "documents": ["Hello world"], "metadatas": [{"source": "test"}]}'
```

## Query Similar Documents

```bash
curl -X POST "http://{{CHROMADB_HOST}}:{{CHROMADB_PORT}}/api/v1/collections/{collection_id}/query" \
  -H "Content-Type: application/json" \
  -d '{"query_texts": ["greeting"], "n_results": 5}'
```

## Tips for AI Agents

- ChromaDB can auto-generate embeddings if configured with an embedding function.
- Use metadata filters to narrow search results.
- Prefer cosine distance for normalized embeddings.
