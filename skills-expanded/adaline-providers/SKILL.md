---
name: adaline-providers
description: "List configured AI providers and models in Adaline. Use when discovering available LLM providers, filtering models, or checking provider configuration."
---

# Adaline Providers

## Concepts

Providers are configured LLM connections in an Adaline workspace. Models are provider-specific model records available to prompts and deployments.

Key terms:
- **Provider** — configured connection to a model provider
- **providerId** — provider record ID used to filter models
- **provider** — provider identifier such as `openai`, `anthropic`, or `google`
- **Model** — model record with `model` name and `enabled` flag

## Configuration

Set `ADALINE_API_KEY`. Base URL: `https://api.adaline.ai/v2`.

## Quick Triage

| Symptom | First Fix |
|---|---|
| Provider name missing | Read `provider`, not legacy `name` |
| Model name missing | Read `model`, not legacy `name` |
| Need provider models inline | Call `GET /providers/{providerId}?includeModels=true` |
| Model unavailable | Filter to `enabled: true` |

## REST API

```bash
curl "https://api.adaline.ai/v2/providers" \
  -H "Authorization: Bearer $ADALINE_API_KEY"

curl "https://api.adaline.ai/v2/providers/provider_abc123?includeModels=true" \
  -H "Authorization: Bearer $ADALINE_API_KEY"

curl "https://api.adaline.ai/v2/models?providerId=provider_abc123" \
  -H "Authorization: Bearer $ADALINE_API_KEY"
```

## SDK Usage

```typescript
const providers = await adaline.providers.list();
const provider = await adaline.providers.get({ providerId, includeModels: true });
const models = await adaline.models.list({ providerId });
```

```python
providers = await adaline.providers.list()
provider = await adaline.providers.get(provider_id=provider_id, include_models=True)
models = await adaline.models.list(provider_id=provider_id)
```

## Best Practices

1. Discover provider IDs at startup instead of hardcoding them.
2. Filter models by `providerId` when building prompt/model selectors.
3. Use `modelSettings` only as capability metadata; pass actual runtime values in prompt/deployment config `settings`.
4. Cache provider/model lists briefly; they change less often than prompt traffic.

## References

See references/api.md for schemas and examples.
