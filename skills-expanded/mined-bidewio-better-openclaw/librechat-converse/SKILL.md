---
name: librechat-converse
description: "Multi-model AI conversations using LibreChat at {{LIBRECHAT_HOST}}:{{LIBRECHAT_PORT}}."
metadata:
  openclaw:
    emoji: "🗣️"
---

# LibreChat Converse

LibreChat is available at `http://{{LIBRECHAT_HOST}}:{{LIBRECHAT_PORT}}` within the Docker network.

## Send a Message

```bash
curl -X POST "http://{{LIBRECHAT_HOST}}:{{LIBRECHAT_PORT}}/api/ask/openAI" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $LIBRECHAT_TOKEN" \
  -d '{"text": "Hello!", "model": "gpt-4"}'
```

## Tips for AI Agents

- Supports OpenAI, Anthropic, Google, and self-hosted models simultaneously.
- Conversations persist across sessions with search functionality.
- Plugin system extends capabilities with web browsing, code execution, etc.
