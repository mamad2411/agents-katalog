---
name: adaline-prompts
description: "Create and manage prompts in Adaline via the v2 API or SDK clients. Use when programmatically creating prompts, updating prompt drafts, listing prompts, or reading prompt/playground data."
---

# Adaline Prompts

## Concepts

Prompts are the central artifact in Adaline's Prompt surface. A prompt has metadata, a draft, optional playground data, and deployable snapshots.

Key terms:
- **Prompt** — a named artifact inside a project
- **Draft** — editable prompt config, messages, and tools
- **Config** — provider/model selection plus flexible `settings`
- **Messages** — ordered role messages with structured `content` arrays
- **Tools** — function definitions with optional HTTP request configuration
- **Variables** — derived from `{{variable}}` placeholders and returned on prompt/draft resources

## Configuration

Set these environment variables when credentials are available:
- `ADALINE_API_KEY` — workspace API key from Admin > API Keys
- `ADALINE_PROJECT_ID` — project to create/list prompts in

Base URL: `https://api.adaline.ai/v2`

## Quick Triage

| Symptom | First Fix |
|---|---|
| List returns empty | Include the correct `projectId` query parameter |
| Pagination skips records | Use `pagination.nextCursor`, not legacy page-number pagination |
| Prompt creation fails | Ensure `draft.messages[].content` is an array of content objects |
| Tool schema fails | Use `{ "type": "function", "definition": { ... } }`, not legacy top-level `name`/`parameters` |
| Draft changes not in production | Deploy a prompt snapshot in the Platform UI, then fetch with the deployments skill |

## API Endpoints

```bash
# List prompts
curl "https://api.adaline.ai/v2/prompts?projectId=$ADALINE_PROJECT_ID&limit=20" \
  -H "Authorization: Bearer $ADALINE_API_KEY"

# Create prompt
curl -X POST "https://api.adaline.ai/v2/prompts" \
  -H "Authorization: Bearer $ADALINE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "projectId": "project_abc123",
    "title": "Support triage",
    "icon": { "type": "emoji", "value": "🎧" },
    "draft": {
      "config": {
        "provider": "openai",
        "model": "gpt-4o",
        "settings": { "temperature": 0.3 }
      },
      "messages": [
        {
          "role": "system",
          "content": [
            { "modality": "text", "value": "You are a helpful support assistant." }
          ]
        },
        {
          "role": "user",
          "content": [
            { "modality": "text", "value": "Answer {{question}}" }
          ]
        }
      ],
      "tools": []
    }
  }'
```

## Draft Structure

```json
{
  "config": {
    "provider": "openai",
    "model": "gpt-4o",
    "settings": {
      "temperature": 0.3,
      "maxTokens": 1024
    }
  },
  "messages": [
    {
      "role": "system",
      "content": [
        { "modality": "text", "value": "You are helpful." }
      ]
    }
  ],
  "tools": [
    {
      "type": "function",
      "definition": {
        "name": "lookup_order",
        "description": "Look up an order by ID",
        "parameters": {
          "type": "object",
          "properties": {
            "order_id": { "type": "string" }
          },
          "required": ["order_id"]
        }
      }
    }
  ]
}
```

## Message Content

Prompt message content is structured. Supported `modality` values include `text`, `image`, `pdf`, `tool-call`, `tool-response`, `reasoning`, `search-result`, and `error`.

```json
{
  "role": "user",
  "content": [
    { "modality": "text", "value": "Describe this image." },
    {
      "modality": "image",
      "detail": "auto",
      "value": { "type": "url", "url": "https://example.com/image.png" }
    }
  ]
}
```

## SDK Usage

The current TypeScript and Python SDKs expose prompt namespace clients:

```typescript
await adaline.prompts.list({ projectId, limit: 20 });
await adaline.prompts.create({ prompt });
await adaline.prompts.get({ promptId, expand: 'playground' });
await adaline.prompts.update({ promptId, prompt: { title: 'New title' } });
await adaline.prompts.draft.get({ promptId });
```

```python
await adaline.prompts.list(project_id=project_id, limit=20)
await adaline.prompts.create(prompt=prompt)
await adaline.prompts.get(prompt_id=prompt_id, expand="playground")
await adaline.prompts.update(prompt_id=prompt_id, prompt=patch)
await adaline.prompts.draft.get(prompt_id=prompt_id)
```

## Best Practices

1. Use cursor pagination (`limit` + `cursor`) for list endpoints.
2. Put model parameters inside `config.settings`.
3. Let Adaline derive variables from message placeholders; do not rely on legacy create-body `variables` arrays.
4. Keep prompt creation separate from deployment. Prompt edits change the draft; deployments produce immutable runtime snapshots.

## References

See references/api.md for the full REST contract and examples.
