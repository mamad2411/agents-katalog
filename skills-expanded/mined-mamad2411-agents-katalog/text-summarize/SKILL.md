---
name: text-summarize
description: "Summarize text using local LLM via Ollama at {{OLLAMA_HOST}}:{{OLLAMA_PORT}}."
metadata:
  openclaw:
    emoji: "📋"
---

# Text Summarize

Use Ollama at `http://{{OLLAMA_HOST}}:{{OLLAMA_PORT}}` for text summarization.

## Summarize Text

```bash
curl -X POST "http://{{OLLAMA_HOST}}:{{OLLAMA_PORT}}/api/generate" \
  -H "Content-Type: application/json" \
  -d '{"model": "llama3.2", "prompt": "Summarize the following text in 3 bullet points:\n\n<paste text here>", "stream": false}'
```

## Tips for AI Agents

- Adjust the prompt to control summary length and style.
- For long documents, summarize in chunks and then summarize the summaries.
- Use smaller models (llama3.2:1b) for faster processing of simple content.
