---
name: kimi-to-fireworks
description: Use when migrating Kimi (Moonshot) API workflows to Fireworks AI. Covers base URL changes, model mapping, JSON mode compatibility, and context window differences.
---

# Migrate Kimi (Moonshot) to Fireworks

You are helping a developer migrate code that calls the Kimi/Moonshot API to use Fireworks AI instead. Kimi uses an OpenAI-compatible API format, so migration is straightforward.

## Detection Signals

Look for these patterns in the codebase:
- Base URL containing `api.moonshot.cn` or `moonshot`
- Model strings starting with `moonshot-v1` (e.g., `moonshot-v1-8k`, `moonshot-v1-32k`)
- Environment variable references to `KIMI_API_KEY` or `MOONSHOT_API_KEY`
- `openai.OpenAI(base_url="https://api.moonshot.cn/v1")`

## Step 1: Change Base URL and API Key

```python
# Before (Kimi/Moonshot)
client = OpenAI(
    api_key=os.environ["KIMI_API_KEY"],
    base_url="https://api.moonshot.cn/v1",
)

# After (Fireworks)
client = OpenAI(
    api_key=os.environ["FIREWORKS_API_KEY"],
    base_url="https://api.fireworks.ai/inference/v1",
)
```

Both Kimi and Fireworks use the OpenAI SDK — only the URL and key change.

## Step 2: Change Model Identifier

| Kimi Model | Fireworks Equivalent | Notes |
|---|---|---|
| moonshot-v1-8k | `accounts/fireworks/models/kimi-k2p6` | Same model family, Fireworks infra |
| moonshot-v1-32k | `accounts/fireworks/models/kimi-k2p6` | K2.6 supports long context natively |
| moonshot-v1-128k | `accounts/fireworks/models/kimi-k2p6` | K2.6 handles extended context |

**Why Kimi on Fireworks?** Same model quality with Fireworks' optimized inference (lower latency, better scaling, unified billing).

## Step 3: Feature Compatibility

### JSON Mode / Structured Output
- `response_format: { "type": "json_object" }` works identically
- **Known difference**: Some models may return extra fields or different value ranges
- **Best practice**: Include exact JSON schema with field types and allowed values in system prompt

### System Prompts
- System messages work identically
- Classification and extraction prompts transfer directly

### Context Window
- Kimi's moonshot-v1 models have fixed windows (8k, 32k, 128k)
- Fireworks Kimi K2.6 supports flexible context — no need to pick a variant

## Validation Checklist

After migration, verify:
- [ ] JSON output parses without error
- [ ] All expected fields are present
- [ ] Field values match expected types and ranges (e.g., confidence is 0-1, not 0-100)
- [ ] No extra unexpected fields that break downstream parsing
- [ ] System prompt instructions followed consistently
- [ ] Multi-turn conversation context works
