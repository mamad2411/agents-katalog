---
name: langflow-build
description: Visual AI workflow builder powered by Langflow
version: 1.0.0
tags: [ai, workflow, langchain, low-code]
---

# Langflow – Visual AI Workflow Builder

Langflow provides a drag-and-drop interface for building LangChain-based
AI agents, RAG flows, and multi-step LLM pipelines.

- **GitHub**: github.com/langflow-ai/langflow (140 000+ ⭐)
- **License**: MIT
- **Security**: Backed by Datastax. Active CVE response. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{LANGFLOW_URL}}` | Base URL of the Langflow instance |
| `{{LANGFLOW_API_KEY}}` | API key for authentication |

## Usage Examples

### Run a flow

```bash
curl -s -X POST "{{LANGFLOW_URL}}/api/v1/run/<flow_id>" \
  -H "x-api-key: {{LANGFLOW_API_KEY}}" \
  -H "Content-Type: application/json" \
  -d '{"input_value": "What is RAG?", "output_type": "chat"}'
```

### List available flows

```bash
curl -s "{{LANGFLOW_URL}}/api/v1/flows" \
  -H "x-api-key: {{LANGFLOW_API_KEY}}"
```

## AI Agent Tips

- Build complex LLM chains visually, then expose them as API endpoints.
- Supports LangChain components: agents, tools, memory, retrievers.
- Export flows as JSON for version control.
- Integrates with Ollama, OpenAI, and other model providers.
