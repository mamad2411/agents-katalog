---
name: llamaindex-query
description: Build data-connected LLM applications with LlamaIndex
version: 1.0.0
tags: [ai, rag, llm, data, indexing]
---

# LlamaIndex – Data Framework for LLMs

LlamaIndex simplifies building RAG pipelines by managing data ingestion,
indexing, and LLM integration for question-answering over your data.

- **GitHub**: github.com/run-llama/llama_index (40 000+ ⭐)
- **License**: MIT
- **Security**: Well-maintained, active community. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{LLAMAINDEX_URL}}` | Base URL of a LlamaIndex-powered API |

## Usage Examples

### Query an index

```bash
curl -s -X POST "{{LLAMAINDEX_URL}}/api/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Summarise the quarterly report"}'
```

## AI Agent Tips

- Supports 100+ data connectors via LlamaHub (PDF, Notion, Slack, DBs, etc.).
- Modular: swap embedding models, vector stores, and LLM providers.
- Sub-question engine decomposes complex queries automatically.
- Scalable for processing large document collections.
