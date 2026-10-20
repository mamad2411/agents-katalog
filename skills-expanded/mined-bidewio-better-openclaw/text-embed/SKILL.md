---
name: text-embed
description: "Generate text embeddings using Ollama at {{OLLAMA_HOST}}:{{OLLAMA_PORT}}."
metadata:
  openclaw:
    emoji: "🧬"
---

# Text Embed

Use Ollama at `http://{{OLLAMA_HOST}}:{{OLLAMA_PORT}}` for text embedding generation.

## Generate Embeddings

```bash
curl -X POST "http://{{OLLAMA_HOST}}:{{OLLAMA_PORT}}/api/embed" \
  -H "Content-Type: application/json" \
  -d '{"model": "nomic-embed-text", "input": "The quick brown fox jumps over the lazy dog"}'
```

## Tips for AI Agents

- Use `nomic-embed-text` or `mxbai-embed-large` for high-quality embeddings.
- Store embeddings in Qdrant, ChromaDB, or Weaviate for similarity search.
- Batch multiple texts in a single request for efficiency.
- Embedding dimensions vary by model — ensure consistency in your vector store.
