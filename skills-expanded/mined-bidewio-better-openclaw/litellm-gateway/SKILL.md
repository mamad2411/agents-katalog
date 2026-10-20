---
name: litellm-gateway
description: "Route LLM requests through a unified gateway supporting 100+ providers via LiteLLM at {{LITELLM_HOST}}:{{LITELLM_PORT}}."
metadata:
  openclaw:
    emoji: "🔀"
---

# LiteLLM Gateway

LiteLLM proxy is available at `http://{{LITELLM_HOST}}:{{LITELLM_PORT}}` within the Docker network, providing an OpenAI-compatible API for 100+ LLM providers.

## Chat Completion

```bash
curl -X POST "http://{{LITELLM_HOST}}:{{LITELLM_PORT}}/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $LITELLM_API_KEY" \
  -d '{"model": "gpt-4", "messages": [{"role": "user", "content": "Hello!"}]}'
```

## List Available Models

```bash
curl "http://{{LITELLM_HOST}}:{{LITELLM_PORT}}/v1/models" \
  -H "Authorization: Bearer $LITELLM_API_KEY"
```

## Tips for AI Agents

- LiteLLM provides a unified OpenAI-compatible interface for all providers.
- Use model aliases to switch providers without changing application code.
- Supports load balancing, fallbacks, and spend tracking.
