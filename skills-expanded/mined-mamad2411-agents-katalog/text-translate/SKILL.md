---
name: text-translate
description: "Translate text between languages using local LLM via Ollama at {{OLLAMA_HOST}}:{{OLLAMA_PORT}}."
metadata:
  openclaw:
    emoji: "🌐"
---

# Text Translate

Use Ollama at `http://{{OLLAMA_HOST}}:{{OLLAMA_PORT}}` for text translation.

## Translate Text

```bash
curl -X POST "http://{{OLLAMA_HOST}}:{{OLLAMA_PORT}}/api/generate" \
  -H "Content-Type: application/json" \
  -d '{"model": "llama3.2", "prompt": "Translate the following English text to French:\n\nHello, how are you?", "stream": false}'
```

## Tips for AI Agents

- Specify source and target languages explicitly in the prompt.
- For technical content, include domain context for better translations.
- Larger models produce more accurate translations for complex text.
