---
name: anythingllm-workspace
description: "Manage document workspaces and chat with documents using AnythingLLM at {{ANYTHINGLLM_HOST}}:{{ANYTHINGLLM_PORT}}."
metadata:
  openclaw:
    emoji: "📄"
---

# AnythingLLM Workspace

AnythingLLM is available at `http://{{ANYTHINGLLM_HOST}}:{{ANYTHINGLLM_PORT}}` within the Docker network.

## Chat with a Workspace

```bash
curl -X POST "http://{{ANYTHINGLLM_HOST}}:{{ANYTHINGLLM_PORT}}/api/v1/workspace/{slug}/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ANYTHINGLLM_API_KEY" \
  -d '{"message": "Summarize the uploaded documents"}'
```

## Upload a Document

```bash
curl -X POST "http://{{ANYTHINGLLM_HOST}}:{{ANYTHINGLLM_PORT}}/api/v1/document/upload" \
  -H "Authorization: Bearer $ANYTHINGLLM_API_KEY" \
  -F "file=@/data/input/document.pdf"
```

## Tips for AI Agents

- Each workspace has isolated document context for focused conversations.
- Supports PDF, TXT, DOCX, and web page ingestion.
- Works with Ollama, OpenAI, and other LLM providers.
