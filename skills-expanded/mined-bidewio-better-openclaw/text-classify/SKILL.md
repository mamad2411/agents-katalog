---
name: text-classify
description: "Classify and analyze sentiment of text using local LLM via Ollama at {{OLLAMA_HOST}}:{{OLLAMA_PORT}}."
metadata:
  openclaw:
    emoji: "🏷️"
---

# Text Classify

Use Ollama at `http://{{OLLAMA_HOST}}:{{OLLAMA_PORT}}` for text classification.

## Classify Text

```bash
curl -X POST "http://{{OLLAMA_HOST}}:{{OLLAMA_PORT}}/api/generate" \
  -H "Content-Type: application/json" \
  -d '{"model": "llama3.2", "prompt": "Classify the sentiment of this text as positive, negative, or neutral. Respond with only the label.\n\nText: I love this product!", "stream": false}'
```

## Tips for AI Agents

- Define categories explicitly in the prompt for consistent classification.
- Use structured output (JSON) for programmatic parsing of results.
- For batch classification, process items sequentially to maintain accuracy.
