---
name: ragflow-pipeline
description: Deep document understanding RAG engine with RAGFlow
version: 1.0.0
tags: [ai, rag, documents, search]
---

# RAGFlow – Document RAG Engine

RAGFlow is an open-source RAG engine with deep document understanding
for trustworthy question-answering from complex documents.

- **GitHub**: github.com/infiniflow/ragflow (40 000+ ⭐)
- **License**: Apache-2.0
- **Security**: Active development. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{RAGFLOW_URL}}` | Base URL of the RAGFlow instance |
| `{{RAGFLOW_API_KEY}}` | API key |

## Usage Examples

### Query a knowledge base

```bash
curl -s -X POST "{{RAGFLOW_URL}}/api/completion" \
  -H "Authorization: Bearer {{RAGFLOW_API_KEY}}" \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the key findings?", "stream": false}'
```

## AI Agent Tips

- Supports PDF, Word, Excel, PPT, and image documents.
- Deep layout analysis and table extraction for complex documents.
- Chunk-level citations for verifiable answers.
- Visual pipeline builder for custom RAG workflows.
