---
name: ollama-local-llm
description: "Run local LLM inference for chat, text generation, and embeddings via the Ollama server at {{OLLAMA_HOST}}:{{OLLAMA_PORT}}."
metadata:
  openclaw:
    emoji: "🦙"
---

# Ollama Local LLM Skill

Ollama local LLM server is available at `http://{{OLLAMA_HOST}}:{{OLLAMA_PORT}}` within the Docker network.

## Chat Completion

Send a multi-turn conversation and get a response:

```bash
curl -X POST "http://{{OLLAMA_HOST}}:{{OLLAMA_PORT}}/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2",
    "messages": [
      { "role": "system", "content": "You are a helpful coding assistant." },
      { "role": "user", "content": "Write a Python function to reverse a string." }
    ],
    "stream": false
  }'
```

## Text Generation

Generate text from a single prompt:

```bash
curl -X POST "http://{{OLLAMA_HOST}}:{{OLLAMA_PORT}}/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2",
    "prompt": "Explain the concept of recursion in simple terms.",
    "stream": false
  }'
```

## Streaming Responses

For real-time token-by-token output, enable streaming:

```bash
curl -X POST "http://{{OLLAMA_HOST}}:{{OLLAMA_PORT}}/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2",
    "messages": [
      { "role": "user", "content": "Tell me a short story." }
    ],
    "stream": true
  }'
```

## Generating Embeddings

Create vector embeddings for text (useful with Qdrant):

```bash
curl -X POST "http://{{OLLAMA_HOST}}:{{OLLAMA_PORT}}/api/embed" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nomic-embed-text",
    "input": ["This is a sentence to embed.", "Another sentence for comparison."]
  }'
```

## Model Management

```bash
# List available models
curl "http://{{OLLAMA_HOST}}:{{OLLAMA_PORT}}/api/tags"

# Pull a new model
curl -X POST "http://{{OLLAMA_HOST}}:{{OLLAMA_PORT}}/api/pull" \
  -H "Content-Type: application/json" \
  -d '{"name": "llama3.2"}'

# Show model details
curl -X POST "http://{{OLLAMA_HOST}}:{{OLLAMA_PORT}}/api/show" \
  -H "Content-Type: application/json" \
  -d '{"name": "llama3.2"}'

# Delete a model
curl -X DELETE "http://{{OLLAMA_HOST}}:{{OLLAMA_PORT}}/api/delete" \
  -H "Content-Type: application/json" \
  -d '{"name": "old-model"}'
```

## Advanced Generation Options

Fine-tune generation with parameters:

```bash
curl -X POST "http://{{OLLAMA_HOST}}:{{OLLAMA_PORT}}/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2",
    "messages": [
      { "role": "user", "content": "Write a creative poem about the ocean." }
    ],
    "stream": false,
    "options": {
      "temperature": 0.8,
      "top_p": 0.9,
      "top_k": 40,
      "num_predict": 512,
      "seed": 42
    }
  }'
```

## Using a Custom System Prompt

```bash
curl -X POST "http://{{OLLAMA_HOST}}:{{OLLAMA_PORT}}/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2",
    "messages": [
      { "role": "system", "content": "You are an expert data analyst. Respond with structured JSON when possible." },
      { "role": "user", "content": "Analyze this data: [10, 25, 18, 42, 7, 33]" }
    ],
    "stream": false,
    "format": "json"
  }'
```

## Recommended Models

| Model | Use Case | Size |
|-------|----------|------|
| `llama3.2` | General chat and reasoning | 3B |
| `llama3.2:70b` | Complex reasoning tasks | 70B |
| `codellama` | Code generation and review | 7B |
| `nomic-embed-text` | Text embeddings for RAG | 137M |
| `mistral` | Fast general-purpose inference | 7B |
| `phi3` | Compact and efficient reasoning | 3.8B |

## Tips for AI Agents

- Always set `"stream": false` when you need to parse the complete response programmatically.
- Use `format: "json"` when you need structured output that's easy to parse.
- Check available models with `/api/tags` before making inference calls to avoid 404 errors.
- For embedding tasks, use `nomic-embed-text` or similar dedicated embedding models, not chat models.
- Lower `temperature` (0.1-0.3) for factual/deterministic tasks; raise it (0.7-1.0) for creative tasks.
- Set `num_predict` to limit response length and prevent runaway generation.
- Use the embeddings endpoint with Qdrant for building RAG (Retrieval-Augmented Generation) pipelines.
- Check Ollama health at `http://{{OLLAMA_HOST}}:{{OLLAMA_PORT}}/` — it returns "Ollama is running".
