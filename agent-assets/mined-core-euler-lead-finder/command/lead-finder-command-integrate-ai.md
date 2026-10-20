# /integrate_ai

**Goal**: Add AI functionality with proper versioning, error handling, and observability.

**When**: Adding LLM, RAG, or embedding features.

**Agents**: ai_engineer (implement), tech_lead (approve)

## Process

| Step | Owner | Do | Output |
|------|-------|----|--------|
| Design | AI Eng | Choose model, design prompts, plan retry/fallback, estimate costs | AI architecture |
| Prompts | AI Eng | Create versioned templates, test edge cases, optimize tokens | Versioned prompts |
| Implementation | AI Eng | Retry logic, fallbacks, structured logging, env vars for keys | Working integration |
| Observability | AI Eng | Log: version, model, tokens, cost, latency; test failure modes | Monitored service |
| Review | TL | Validate versioning, error handling, costs | Approval |

## Required Pattern
```python
# Versioned prompt
PROMPT_V1 = PromptVersion(version="v1.0", template="...")

# Retry with backoff
for attempt in range(3):
    try:
        response = await client.create(...)
        break
    except RateLimitError:
        await asyncio.sleep(2 ** attempt)
    except Exception:
        return fallback_response()

# Log everything
logger.info("ai_request", version="v1.0", tokens=n, cost=c, latency_ms=ms)
```

## Gates
- **Blocker**: Prompts not versioned
- **Blocker**: No retry/fallback logic
- **Blocker**: AI requests not logged
- **Blocker**: Costs not documented
- **Blocker**: API keys hardcoded

## Authority
**Tech Lead** approves model choices and cost implications.

**Next**: `/test`
