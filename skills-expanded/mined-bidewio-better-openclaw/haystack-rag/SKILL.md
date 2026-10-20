---
name: haystack-rag
description: Build production-ready RAG pipelines with Haystack
version: 1.0.0
tags: [ai, rag, search, nlp, framework]
---

# Haystack – Production RAG Framework

Haystack is an open-source framework for building production-ready
search and question-answering systems using RAG.

- **GitHub**: github.com/deepset-ai/haystack (20 000+ ⭐)
- **License**: Apache-2.0
- **Security**: Backed by deepset. Enterprise-grade. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{HAYSTACK_URL}}` | Base URL of a Haystack pipeline API |

## Usage Examples

### Query a deployed pipeline

```bash
curl -s -X POST "{{HAYSTACK_URL}}/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is retrieval augmented generation?"}'
```

## AI Agent Tips

- Modular pipeline architecture: swap retrievers, generators, and stores.
- Supports hybrid search (BM25 + dense vector retrieval).
- Built-in evaluation tools for measuring RAG quality.
- Integrates with Elasticsearch, OpenSearch, Qdrant, Weaviate, and more.
