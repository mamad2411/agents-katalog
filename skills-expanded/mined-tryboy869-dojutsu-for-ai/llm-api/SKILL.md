---
name: llm-api
description: "Apply when integrating LLM APIs (OpenAI, Groq, Anthropic, Mistral) into applications. Covers: prompt engineering, streaming, retry logic, cost control, structured outputs, function calling. Trigger for: LLM, GPT, Claude, Groq, AI API, prompt, OpenAI, Anthropic."
---

# LLM API — Production Integration Patterns

## Provider Selection (2025)
| Provider | Best for | Latency | Cost |
|----------|----------|---------|------|
| Groq | Speed-critical, real-time | Ultra-low | Low |
| Anthropic Claude | Complex reasoning, long context | Medium | Medium |
| OpenAI GPT-4o | General purpose, function calling | Medium | Medium |
| Mistral | EU data residency, multilingual | Low | Low |

## Retry with Exponential Backoff (MANDATORY)
```python
import asyncio
from groq import AsyncGroq, RateLimitError, APIError

async def llm_call(messages: list[dict], model: str, max_retries: int = 3) -> str:
    client = AsyncGroq()
    for attempt in range(max_retries):
        try:
            resp = await client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.1,
                max_tokens=4096,
            )
            return resp.choices[0].message.content
        except RateLimitError:
            wait = 2 ** attempt  # 1s, 2s, 4s
            await asyncio.sleep(wait)
        except APIError as e:
            if e.status_code >= 500 and attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)
            else:
                raise
    raise RuntimeError("LLM call failed after retries")
```

## Streaming — For long outputs
```python
async def stream_response(prompt: str):
    async with AsyncGroq() as client:
        stream = await client.chat.completions.create(
            model="moonshotai/kimi-k2-instruct-0905",
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )
        async for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            yield delta  # stream to client via SSE
```

## Structured Output (JSON mode)
```python
from pydantic import BaseModel

class AnalysisResult(BaseModel):
    summary: str
    risks: list[str]
    recommendation: str

async def analyze_structured(task: str) -> AnalysisResult:
    resp = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": task}],
        response_format={"type": "json_object"},
    )
    return AnalysisResult.model_validate_json(resp.choices[0].message.content)
```

## Prompt Engineering Rules
```python
SYSTEM_PROMPT = """You are an expert {role}.
Task: {specific_task}
Output format: {format_spec}
Constraints:
- {constraint_1}
- {constraint_2}
NEVER: {what_to_avoid}"""

# ✅ Structured, explicit, with examples
# ✅ Separate system (role/rules) from user (task)
# ✅ Temperature 0 for deterministic, 0.7 for creative
# ❌ Vague prompts ("do something good")
# ❌ Putting everything in user message
```

## Cost Control
```python
# Estimate before calling
def estimate_cost(prompt: str, model: str) -> float:
    tokens = len(prompt.split()) * 1.3  # rough estimate
    costs = {
        "gpt-4o": 0.0000025,   # per token
        "groq/kimi": 0.0000009,
    }
    return tokens * costs.get(model, 0.000005)

# Cache identical prompts
import hashlib, json
def cache_key(messages: list) -> str:
    return hashlib.sha256(json.dumps(messages, sort_keys=True).encode()).hexdigest()
```

## Forbidden
❌ API keys in code — use environment variables
❌ No retry logic (rate limits happen)
❌ Parsing LLM JSON with `eval()` — use `json.loads()` with try/catch
❌ `max_tokens` not set — LLM can run forever
❌ Logging full prompts in production (may contain PII)
❌ No timeout on API calls
