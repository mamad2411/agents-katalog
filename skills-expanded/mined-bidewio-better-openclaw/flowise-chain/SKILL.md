---
name: flowise-chain
description: "Build LLM chains and agents visually using Flowise at {{FLOWISE_HOST}}:{{FLOWISE_PORT}}."
metadata:
  openclaw:
    emoji: "🌊"
---

# Flowise Chain Builder

Flowise is available at `http://{{FLOWISE_HOST}}:{{FLOWISE_PORT}}` within the Docker network.

## Run a Prediction

```bash
curl -X POST "http://{{FLOWISE_HOST}}:{{FLOWISE_PORT}}/api/v1/prediction/{chatflow_id}" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is machine learning?"}'
```

## Tips for AI Agents

- Flowise provides a drag-and-drop UI for building LangChain flows.
- Supports custom tools, memory, and document loaders.
- Export flows as JSON for version control and sharing.
