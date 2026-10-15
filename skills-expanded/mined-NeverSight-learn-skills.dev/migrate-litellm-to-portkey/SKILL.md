---
name: migrate-litellm-to-portkey
description: Migrate Python applications from LiteLLM to Portkey AI Gateway. Covers litellm.completion, Router, Proxy, fallbacks, caching, retries, callbacks, embeddings, and image generation. Use when the user wants to replace LiteLLM with Portkey or switch from LiteLLM to Portkey.
license: Apache-2.0
compatibility: Requires Python 3.8+. Replaces litellm with portkey-ai package.
metadata:
  author: portkey-ai
  version: "1.0.0"
  docs: https://docs.portkey.ai
---

# Migrate from LiteLLM to Portkey

Step-by-step guide for migrating Python applications from LiteLLM to the Portkey AI Gateway SDK. Portkey uses an OpenAI-compatible client interface, so most code changes are structural (client instantiation and config) rather than call-signature changes.

**Additional References:**
- [Detailed Migration Patterns](references/MIGRATION_PATTERNS.md) - Every LiteLLM pattern with before/after code
- [Proxy & Config Migration](references/LITELLM_PROXY_MIGRATION.md) - LiteLLM Proxy → Portkey gateway migration

---

## Pre-Migration Checklist

1. **Get a Portkey API key** at [app.portkey.ai/api-keys](https://app.portkey.ai/api-keys)
2. **Set up AI Providers** in the [Model Catalog](https://app.portkey.ai) — connect your LLM providers (OpenAI, Anthropic, Azure, Bedrock, etc.) and note each provider's slug (e.g., `openai-prod`, `anthropic-main`)
3. **Swap the package**:
   ```bash
   pip uninstall litellm
   pip install portkey-ai
   ```
4. **Set environment variables**:
   ```bash
   export PORTKEY_API_KEY="your-portkey-api-key"
   # Provider keys are now stored securely in the Model Catalog
   # You no longer need OPENAI_API_KEY, ANTHROPIC_API_KEY, etc. in your env
   ```
5. **(Optional) Verify connectivity** with the Portkey CLI:
   ```bash
   npx portkey verify
   ```

---

## Quick Migration Map

| LiteLLM | Portkey |
|---------|---------|
| `from litellm import completion` | `from portkey_ai import Portkey` |
| `completion(model="openai/gpt-4o", ...)` | `client.chat.completions.create(model="@openai-prod/gpt-4o", ...)` |
| `litellm.acompletion(...)` | `await async_client.chat.completions.create(...)` |
| `litellm.embedding(...)` | `client.embeddings.create(...)` |
| `litellm.image_generation(...)` | `client.images.generate(...)` |
| `Router(model_list=[...])` | `Portkey(config={"strategy": ..., "targets": [...]})` |
| `completion(..., fallbacks=[...])` | `Portkey(config={"strategy": {"mode": "fallback"}, ...})` |
| `completion(..., num_retries=3)` | `Portkey(config={"retry": {"attempts": 3, ...}})` |
| `litellm.cache = Cache(...)` | `Portkey(config={"cache": {"mode": "semantic", ...}})` |
| `litellm.success_callback = [...]` | Built-in dashboard + `trace_id` / `metadata` |
| `completion(..., timeout=30)` | `Portkey(..., request_timeout=30)` |
| `completion(..., metadata={...})` | `Portkey(..., metadata={...})` |
| `"openai/gpt-4o"` (provider/model) | `"@openai-prod/gpt-4o"` (@provider-slug/model) |

---

## Core Migrations

### 1. Basic Completion

**LiteLLM:**
```python
from litellm import completion
import os

os.environ["OPENAI_API_KEY"] = "sk-..."

response = completion(
    model="openai/gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

**Portkey:**
```python
import os
from portkey_ai import Portkey

client = Portkey(
    api_key=os.environ["PORTKEY_API_KEY"]
)

response = client.chat.completions.create(
    model="@openai-prod/gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

Key differences:
- Stateless function → stateful client object
- Model format changes from `"openai/gpt-4o"` to `"@provider-slug/gpt-4o"` where the provider slug comes from your Model Catalog
- Provider API keys no longer needed in env — credentials are stored in the Model Catalog

### 2. Streaming

**LiteLLM:**
```python
for chunk in completion(
    model="openai/gpt-4o",
    messages=[{"role": "user", "content": "Write a poem"}],
    stream=True,
):
    print(chunk.choices[0].delta.content or "", end="")
```

**Portkey:**
```python
stream = client.chat.completions.create(
    model="@openai-prod/gpt-4o",
    messages=[{"role": "user", "content": "Write a poem"}],
    stream=True
)
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### 3. Async

**LiteLLM:**
```python
import litellm
response = await litellm.acompletion(
    model="openai/gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

**Portkey:**
```python
from portkey_ai import AsyncPortkey

client = AsyncPortkey(
    api_key=os.environ["PORTKEY_API_KEY"]
)
response = await client.chat.completions.create(
    model="@openai-prod/gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### 4. Fallbacks

**LiteLLM:**
```python
response = completion(
    model="openai/gpt-4o",
    messages=messages,
    fallbacks=["anthropic/claude-3-5-sonnet-20241022"]
)
```

**Portkey:**
```python
client = Portkey(
    api_key=os.environ["PORTKEY_API_KEY"],
    config={
        "strategy": {"mode": "fallback"},
        "targets": [
            {
                "override_params": {"model": "@openai-prod/gpt-4o"}
            },
            {
                "override_params": {"model": "@anthropic-main/claude-3-5-sonnet-20241022"}
            }
        ]
    }
)
response = client.chat.completions.create(messages=messages)
```

### 5. Load Balancing (Router)

**LiteLLM:**
```python
from litellm import Router

model_list = [
    {
        "model_name": "gpt-3.5-turbo",
        "litellm_params": {
            "model": "azure/chatgpt-v-2",
            "api_key": os.getenv("AZURE_API_KEY"),
            "api_base": os.getenv("AZURE_API_BASE"),
            "rpm": 900
        }
    },
    {
        "model_name": "gpt-3.5-turbo",
        "litellm_params": {
            "model": "openai/gpt-3.5-turbo",
            "api_key": os.getenv("OPENAI_API_KEY"),
            "rpm": 100
        }
    }
]

router = Router(model_list=model_list, routing_strategy="simple-shuffle")
response = await router.acompletion(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

**Portkey:**
```python
client = Portkey(
    api_key=os.environ["PORTKEY_API_KEY"],
    config={
        "strategy": {"mode": "loadbalance"},
        "targets": [
            {
                "override_params": {"model": "@azure-prod/gpt-3.5-turbo"},
                "weight": 0.9
            },
            {
                "override_params": {"model": "@openai-prod/gpt-3.5-turbo"},
                "weight": 0.1
            }
        ]
    }
)
response = client.chat.completions.create(
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### 6. Retries

**LiteLLM:**
```python
response = completion(
    model="openai/gpt-4o",
    messages=messages,
    num_retries=3
)
```

**Portkey:**
```python
client = Portkey(
    api_key=os.environ["PORTKEY_API_KEY"],
    config={
        "retry": {"attempts": 3, "on_status_codes": [429, 500, 502, 503, 504]}
    }
)
response = client.chat.completions.create(
    model="@openai-prod/gpt-4o",
    messages=messages
)
```

### 7. Caching

**LiteLLM:**
```python
import litellm
from litellm.caching.caching import Cache

litellm.cache = Cache(type="redis", host="localhost", port=6379)

response = completion(model="openai/gpt-4o", messages=messages, caching=True)
```

**Portkey:** (no infrastructure to manage — caching is built-in)
```python
client = Portkey(
    api_key=os.environ["PORTKEY_API_KEY"],
    config={
        "cache": {"mode": "semantic", "max_age": 3600}
    }
)
response = client.chat.completions.create(
    model="@openai-prod/gpt-4o",
    messages=messages
)
```

### 8. Observability

**LiteLLM:**
```python
import litellm
litellm.success_callback = ["langfuse"]
litellm.failure_callback = ["langfuse"]
```

**Portkey:** (built-in — every request is logged automatically)
```python
client = Portkey(
    api_key=os.environ["PORTKEY_API_KEY"],
    trace_id="session-123",
    metadata={
        "user_id": "user-456",
        "environment": "production"
    }
)
```

View logs, traces, costs, and latency at [app.portkey.ai](https://app.portkey.ai). No third-party callback integration needed.

---

## Model Naming

LiteLLM uses `provider/model` format. Portkey uses `@provider-slug/model` where the provider slug comes from your Model Catalog:

| LiteLLM Model String | Portkey Model String |
|----------------------|---------------------|
| `"openai/gpt-4o"` | `"@openai-prod/gpt-4o"` |
| `"anthropic/claude-3-5-sonnet-20241022"` | `"@anthropic-main/claude-3-5-sonnet-20241022"` |
| `"azure/gpt-4"` | `"@azure-us-east/gpt-4"` |
| `"bedrock/anthropic.claude-3-sonnet..."` | `"@bedrock-main/anthropic.claude-3-sonnet..."` |
| `"vertex_ai/gemini-1.5-pro"` | `"@vertex-prod/gemini-1.5-pro"` |

The `@slug` prefix maps to an AI Provider in your Model Catalog. You control which models are available under each provider.

---

## Error Handling

**LiteLLM:**
```python
import litellm
try:
    response = completion(model="openai/gpt-4o", messages=messages)
except litellm.AuthenticationError:
    print("Bad API key")
except litellm.RateLimitError:
    print("Rate limited")
```

**Portkey:**
```python
try:
    response = client.chat.completions.create(
        model="@openai-prod/gpt-4o", messages=messages
    )
except Exception as e:
    status = getattr(e, 'status_code', None)
    if status == 401:
        print("Bad API key")
    elif status == 429:
        print("Rate limited")
```

---

## AI Coding Agent Migrations

### Claude Code

If Claude Code is routed through a LiteLLM Proxy (via `ANTHROPIC_BASE_URL`), the fastest migration is:

```bash
npx portkey setup
```

This replaces the LiteLLM Proxy env vars (`ANTHROPIC_BASE_URL`, `ANTHROPIC_API_KEY`) with Portkey equivalents. See [Proxy Migration — Claude Code section](references/LITELLM_PROXY_MIGRATION.md#claude-code-litellm-proxy--portkey) for manual setup, Bedrock/Vertex model mappings, and Config-based routing.

### OpenAI Codex CLI

If Codex CLI is routed through a LiteLLM Proxy (via `openai_base_url` or `OPENAI_BASE_URL`), update `~/.codex/config.json` to point at Portkey with a `portkey` provider and `model: "@provider-slug/model"` format. See [Proxy Migration — Codex section](references/LITELLM_PROXY_MIGRATION.md#openai-codex-cli-litellm-proxy--portkey) for step-by-step setup.

---

## Zero-Change Path: Keep LiteLLM, Route Through Portkey

If you want Portkey's observability and reliability without rewriting any code, you can keep using `litellm.completion()` and just point it at Portkey's gateway:

```python
from litellm import completion

response = completion(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}],
    api_base="https://api.portkey.ai/v1",
    api_key=os.environ["PORTKEY_API_KEY"],
    extra_headers={"x-portkey-provider": "@openai-prod"}
)
```

This gives you Portkey logging, caching, and guardrails immediately — then you can migrate call-by-call to the Portkey SDK at your own pace.

---

## OpenAI Client Approach (Minimal Changes)

If your codebase uses the OpenAI SDK to talk to LiteLLM's proxy, you can switch to Portkey by only changing `base_url` and adding headers — no import changes required:

```python
import openai
from portkey_ai import PORTKEY_GATEWAY_URL, createHeaders

client = openai.OpenAI(
    api_key="not-used",
    base_url=PORTKEY_GATEWAY_URL,  # https://api.portkey.ai/v1
    default_headers=createHeaders(
        api_key="your-portkey-api-key"
    )
)

response = client.chat.completions.create(
    model="@openai-prod/gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

This also works in **TypeScript/JavaScript**:

```typescript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "https://api.portkey.ai/v1",
  apiKey: process.env.PORTKEY_API_KEY,
  defaultHeaders: { "x-portkey-provider": "@openai-prod" }
});

const response = await client.chat.completions.create({
  model: "gpt-4o",
  messages: [{ role: "user", content: "Hello!" }]
});
```

### Quick Verification with cURL

Before changing any code, test the gateway connection:

```bash
curl -s https://api.portkey.ai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "x-portkey-api-key: $PORTKEY_API_KEY" \
  -H "x-portkey-provider: @openai-prod" \
  -d '{
    "model": "gpt-4o",
    "max_tokens": 5,
    "messages": [{"role": "user", "content": "Say ok"}]
  }'
```

### Routing via Headers

Portkey supports two routing modes, set via headers:

| Header | Use Case |
|--------|----------|
| `x-portkey-provider: @slug` | Route to a specific AI Provider from your Model Catalog |
| `x-portkey-config: pc-config-xxx` | Use a Config (with fallbacks, caching, etc.) from the dashboard |

With the `@provider-slug/model` format in the `model` parameter, you typically don't need to set these headers explicitly.

---

## Migration Workflow

1. **Verify** — Test connectivity before touching code:
   ```bash
   npx portkey verify
   ```
2. **Audit** — Grep your codebase for LiteLLM usage:
   ```bash
   grep -rn "from litellm\|import litellm\|litellm\." --include="*.py"
   ```
3. **Quick win** — Point existing LiteLLM calls at Portkey with `api_base` (see [Zero-Change Path](#zero-change-path-keep-litellm-route-through-portkey))
4. **Map** — For each usage, find the Portkey equivalent using the table above or [MIGRATION_PATTERNS.md](references/MIGRATION_PATTERNS.md)
5. **Replace** — Swap imports, instantiate a Portkey client, and update call sites
6. **Configure** — Move routing/fallback/cache logic from code into Portkey `config` dicts (or dashboard [Config IDs](https://app.portkey.ai/configs))
7. **Test** — Run your test suite; response formats are identical (OpenAI-compatible)
8. **Clean up** — Remove `litellm` from requirements, remove provider API key env vars

---

## Resources

- **Portkey Docs**: [docs.portkey.ai](https://docs.portkey.ai)
- **Dashboard**: [app.portkey.ai](https://app.portkey.ai)
- **Python SDK**: [github.com/portkey-ai/portkey-python-sdk](https://github.com/portkey-ai/portkey-python-sdk)
- **Discord**: [portkey.ai/discord](https://portkey.ai/discord)
