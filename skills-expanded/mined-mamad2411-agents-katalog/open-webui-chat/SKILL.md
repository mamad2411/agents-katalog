---
name: open-webui-chat
description: "Interact with LLMs through Open WebUI's chat interface and API at {{OPEN_WEBUI_HOST}}:{{OPEN_WEBUI_PORT}}."
metadata:
  openclaw:
    emoji: "💬"
---

# Open WebUI Chat

Open WebUI is available at `http://{{OPEN_WEBUI_HOST}}:{{OPEN_WEBUI_PORT}}` within the Docker network.

## Chat via API

```bash
curl -X POST "http://{{OPEN_WEBUI_HOST}}:{{OPEN_WEBUI_PORT}}/api/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPEN_WEBUI_API_KEY" \
  -d '{"model": "llama3.2", "messages": [{"role": "user", "content": "Hello!"}]}'
```

## Tips for AI Agents

- Open WebUI connects to Ollama and other OpenAI-compatible APIs.
- Supports RAG with document uploads for context-aware conversations.
- Web search integration provides real-time information.
