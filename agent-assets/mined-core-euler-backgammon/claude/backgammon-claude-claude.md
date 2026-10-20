# Claude Operating Contract

AI-driven freelance agency. Focus: Telegram bots (aiogram 3.x), Mini Apps, AI systems, docker-compose.

**Workflow**: See `README.md` | **Rules**: See `RULES.md`

## Principles

1. Architecture before implementation (no "vibe coding")
2. Docker is source of truth
3. Simple > clever, explicit > implicit
4. Ask if blocking, document decisions

## AI Integration Pattern

```python
# Versioned prompt
PROMPT_V1 = PromptVersion(version="v1.0", template="...")

# Retry with backoff
for attempt in range(3):
    try:
        response = await client.messages.create(...)
        break
    except RateLimitError:
        await asyncio.sleep(2 ** attempt)
    except Exception:
        return fallback_response()

# Log everything
logger.info("ai_request", model=model, tokens=tokens, cost_usd=cost)
```

## Model Selection

- **Sonnet**: Default (balanced)
- **Opus**: Complex reasoning
- **Haiku**: Fast/cheap tasks
