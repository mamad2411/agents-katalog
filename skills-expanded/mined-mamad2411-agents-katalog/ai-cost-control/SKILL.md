---
name: ai-cost-control
description: Prevent LLM cost explosion — token budgets, rate limits, cost monitoring, model selection
triggers: [cost, expensive, budget, token limit, LLM costs, spending, expensive AI call, API costs]
---

# SKILL: AI Cost Control

## The Problem
An unbounded LLM call costs $0 to $100+ depending on context and output.
Without guardrails, a single feature can cost thousands per month.

## Hard Rules (never break these)

```python
# RULE 1: Every LLM call has max_tokens set
# ❌ WRONG — unbounded cost
response = await client.messages.create(
    model="claude-sonnet-4-5",
    messages=[{"role": "user", "content": long_prompt}]
)

# ✅ CORRECT — cost bounded
response = await client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,  # ← maximum output
    messages=[...]
)

# RULE 2: Rate limit AI endpoints (prevent repeated calls)
# Use slowapi or similar
@app.post("/api/v1/ai/generate")
@limiter.limit("20/minute")  # max 20 calls/min per user
async def generate(request: Request, ...):
    ...

# RULE 3: Use cheapest model that works
# Costs (approximate, check current pricing):
#   Haiku: $0.80 per 1M input tokens (30% of Sonnet)
#   Sonnet: $3 per 1M input tokens (20% of Opus)
#   Opus: $15 per 1M input tokens (most expensive)
# Route: use Haiku for simple tasks, Sonnet for complex

async def route_to_model(complexity: str) -> str:
    if complexity == "simple":
        return "claude-haiku-4-5"  # 70% cheaper
    elif complexity == "complex":
        return "claude-sonnet-4-5"
    else:
        return "claude-opus-4-6"    # only for critical work

# RULE 4: Streaming > full response (cap output cost)
async for event in client.messages.stream(...):
    if event.type == "content_block_delta":
        chunk = event.delta.text
        yield chunk
# Stop streaming if user closes connection (saves money)
```

## Cost Estimation Before Building

Before implementing an AI feature, estimate the cost:

```
Monthly cost = (Daily calls × Token average × Price per token) × 30

Example: Chat feature
Daily calls: 1000 users × 1 call/day = 1000 calls/day
Input tokens per call: 2000 (user message + context)
Output tokens per call: 500 (AI response)
Model: Claude Sonnet ($3/1M input, $9/1M output)

Monthly cost = (1000 × (2000 input + 500 output)) × 30 × price_per_token
            = (1000 × 2500) × 30 × ((3 + 2.7) / 1M)
            = 75M tokens × $0.0000057 = $427/month
```

If cost is > $10k/month: reconsider the feature or add aggressive caching.

## Cost Monitoring

```python
# Log every LLM call with cost
import logging
from datetime import datetime

logger = logging.getLogger("costs")

async def log_llm_call(
    model: str,
    input_tokens: int,
    output_tokens: int,
    user_id: str
):
    cost = calculate_cost(model, input_tokens, output_tokens)
    logger.info(f"cost_event", extra={
        "timestamp": datetime.utcnow().isoformat(),
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost_usd": cost,
        "user_id": user_id,
    })

# Query costs by user (identify power users)
SELECT user_id, SUM(cost_usd) as monthly_cost
FROM cost_logs
WHERE date >= date_trunc('month', NOW())
GROUP BY user_id
ORDER BY monthly_cost DESC;
```

## Caching Strategy (prevent repeated expensive calls)

```python
# Cache LLM responses for identical inputs
from functools import lru_cache
import hashlib

@lru_cache(maxsize=10000)
async def cached_ai_call(prompt_hash: str, model: str):
    """Only call LLM if cache miss — saves 95% of calls"""
    prompt = get_original_prompt(prompt_hash)
    response = await client.messages.create(
        model=model,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

async def generate(prompt: str, model: str):
    prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()
    return await cached_ai_call(prompt_hash, model)

# Cache hit rate monitoring
cache_hits = 0
cache_misses = 0
# After N calls: if hit_rate < 20%, caching not helping for this feature
```

## Token Budget Allocation

```
Example budget for $5000/month spend:
  Chat features: 40% ($2000) = ~333M tokens
  Code generation: 30% ($1500) = ~250M tokens
  Data analysis: 20% ($1000) = ~167M tokens
  Admin/moderation: 10% ($500) = ~83M tokens

Monitor weekly: are we on track? Trending over/under?
Alert if: any category exceeds 120% of monthly budget
```

## Shutdown Mechanisms (prevent runaway costs)

```python
class CostGuard:
    def __init__(self, daily_limit_usd: float = 100):
        self.daily_limit = daily_limit_usd
        self.today_spent = 0
    
    async def check_before_call(self, estimated_cost: float):
        if self.today_spent + estimated_cost > self.daily_limit:
            raise Exception(
                f"Daily spend limit reached. "
                f"Current: ${self.today_spent:.2f}, "
                f"Limit: ${self.daily_limit:.2f}"
            )
    
    async def log_call(self, actual_cost: float):
        self.today_spent += actual_cost
        if self.today_spent > self.daily_limit:
            # Send emergency alert
            await notify_team(f"Cost limit exceeded: ${self.today_spent}")

guard = CostGuard(daily_limit_usd=100)

@app.post("/api/v1/ai/generate")
async def generate(...):
    estimated_cost = 0.02  # estimate before calling
    await guard.check_before_call(estimated_cost)
    
    response = await client.messages.create(...)
    actual_cost = calculate_cost(response.usage)
    await guard.log_call(actual_cost)
    
    return response
```

## Monthly Cost Review

Every month, analyze:
```sql
-- Top spending categories
SELECT feature, SUM(cost_usd) as spend
FROM cost_logs
WHERE date >= date_trunc('month', NOW())
GROUP BY feature ORDER BY spend DESC;

-- Most expensive users
SELECT user_id, COUNT(*) as calls, SUM(cost_usd) as spend
FROM cost_logs GROUP BY user_id ORDER BY spend DESC LIMIT 20;

-- Cost per user (unit economics)
SELECT SUM(cost_usd) / COUNT(DISTINCT user_id) as cost_per_user
FROM cost_logs;

-- Token efficiency by model
SELECT model, AVG(output_tokens) as avg_output, AVG(cost_usd) as avg_cost
FROM cost_logs GROUP BY model;
```

## Quality checks
- [ ] Every LLM call has max_tokens set
- [ ] Rate limiting on all AI endpoints (no more than 20/min per user)
- [ ] Model selection by task complexity (Haiku for simple, Sonnet for complex)
- [ ] Cost monitoring in place (logging every call)
- [ ] Caching strategy for repeated prompts
- [ ] Daily/monthly cost alerts configured
- [ ] Cost budget defined and tracked
