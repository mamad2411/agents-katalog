---
name: openai-to-fireworks
description: Use when migrating OpenAI GPT workflows to Fireworks AI open models. Covers base URL changes, model mapping, tool calling, JSON mode, streaming compatibility, and known behavioral differences.
---

# Migrate OpenAI to Fireworks

You are helping a developer migrate code that calls the OpenAI API to use Fireworks AI instead.

## Detection Signals

Look for these patterns in the codebase:
- `import openai` or `from openai import OpenAI`
- Base URL containing `api.openai.com` (or no base URL, which defaults to OpenAI)
- Model strings starting with `gpt-` (e.g., `gpt-4o`, `gpt-4o-mini`, `gpt-3.5-turbo`)
- `tool_choice`, `tools`, `response_format` parameters
- `openai.OpenAI()` constructor with no `base_url` argument

## Step 1: Change Base URL and API Key

```python
# Before
client = openai.OpenAI()

# After
import os
client = openai.OpenAI(
    base_url="https://api.fireworks.ai/inference/v1",
    api_key=os.environ["FIREWORKS_API_KEY"],
)
```

The OpenAI Python SDK works directly with Fireworks — no new SDK needed.

## Step 2: Change Model Identifier

| OpenAI Model | Fireworks Equivalent | Notes |
|---|---|---|
| gpt-4o, gpt-5 | `accounts/fireworks/models/kimi-k2p6` | Best general replacement for agentic + tool use |
| gpt-4o, gpt-5 | `accounts/fireworks/models/deepseek-v3p2` | Strong alternative, especially for code |
| gpt-4o-mini | `accounts/fireworks/models/qwen3-14b` | Good balance of speed and capability |
| gpt-3.5-turbo | `accounts/fireworks/models/qwen3-8b` | Fast, good for classification and simple tasks |

## Step 3: Feature Compatibility

### Tool Calling
- Fireworks supports OpenAI-compatible tool calling on most large models
- `tool_choice: "auto"` works as expected
- `tool_choice: "required"` works on most models
- Tool call arguments are returned as JSON strings (same as OpenAI)
- **Known difference**: Some models may add extra parameters not in the schema. Add explicit constraints in the system prompt if this occurs.

### JSON Mode / Structured Output
- `response_format: { "type": "json_object" }` is supported
- `response_format: { "type": "json_schema", "json_schema": {...} }` supported on select models
- **Best practice**: Repeat the expected JSON schema in the system prompt for reliable adherence

### Streaming
- SSE streaming is fully compatible with OpenAI's format
- `stream: true` works identically
- Fireworks returns usage stats in both streaming and non-streaming responses

### System Prompts
- System messages work identically
- Multi-turn conversations supported
- No changes needed for message format

## Step 4: Error Handling

| OpenAI Error | Fireworks Equivalent | Action |
|---|---|---|
| `RateLimitError` | Same HTTP 429 | Same retry logic works |
| `APIError` | Same HTTP 5xx | Same retry logic works |
| Model not found | HTTP 404 | Check model ID format: `accounts/fireworks/models/MODEL_NAME` |

## Validation Checklist

After migration, verify:
- [ ] Tool calls parse without error
- [ ] Tool call function names match expected values
- [ ] Tool call arguments contain required fields
- [ ] JSON output matches expected schema
- [ ] System prompt behavior is preserved
- [ ] Multi-turn conversation context works
- [ ] Streaming chunks arrive in expected format
- [ ] Error handling covers Fireworks error codes
