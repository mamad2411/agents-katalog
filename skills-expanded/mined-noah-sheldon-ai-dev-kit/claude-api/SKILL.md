---
name: claude-api
description: Claude API usage — messages API, system prompts, tool use/function calling, extended thinking, prompt caching, token counting, streaming, image understanding, structured output, rate limits, fallback strategies, cost optimization.
origin: AI Dev Kit
---

# Claude API

Comprehensive guide to using the Claude (Anthropic) Messages API effectively, covering
tool use, extended thinking, caching, streaming, structured output, rate limits,
and cost optimization patterns.

## When to Use

- Building applications that call Claude (Opus, Sonnet, Haiku) via the Messages API.
- Implementing tool use (function calling) with Claude's native tool execution.
- Using extended thinking for complex reasoning tasks.
- Optimizing prompt caching for reduced latency and cost.
- Streaming responses for real-time UX or processing large outputs.
- Handling rate limits, errors, and implementing fallback strategies.

## Core Concepts

### 1. Messages API Basics

```python
import anthropic

client = anthropic.Anthropic(api_key="sk-ant-...")

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    system="You are a helpful coding assistant.",
    messages=[
        {"role": "user", "content": "Explain the strategy pattern in Python."}
    ],
)

print(response.content[0].text)
print(f"Tokens: {response.usage.input_tokens} in, {response.usage.output_tokens} out")
```

**Async usage:**

```python
import asyncio
import anthropic

async def main():
    async with anthropic.AsyncAnthropic() as client:
        response = await client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=[{"role": "user", "content": "Write a Python quicksort."}],
        )
        print(response.content[0].text)

asyncio.run(main())
```

### 2. System Prompts

System prompts set behavior, tone, and constraints for the entire conversation:

```python
SYSTEM_PROMPT = """\
You are an expert Python engineer. Follow these rules:

1. Always use type hints.
2. Prefer composition over inheritance.
3. Include docstrings for all public functions and classes.
4. When writing tests, use pytest with fixtures.
5. If unsure about an API, say so explicitly.

Respond in markdown. Include code examples for every substantive claim."""

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    system=SYSTEM_PROMPT,
    messages=[{"role": "user", "content": "How do I implement a retry decorator?"}],
)
```

**Multi-part system prompts** (combining text and images):

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Describe this architecture diagram."},
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": base64_encoded_image_data,
                },
            },
        ],
    }],
)
```

### 3. Tool Use / Function Calling

Claude natively supports tool calling with structured output:

```python
tools = [
    {
        "name": "search_codebase",
        "description": "Search the codebase for a pattern or symbol.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query"},
                "glob": {"type": "string", "description": "File glob pattern, e.g., '*.py'"},
            },
            "required": ["query"],
        },
    },
    {
        "name": "read_file",
        "description": "Read the contents of a file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Absolute path to the file"},
                "lines": {"type": "array", "items": {"type": "integer"}, "description": "Specific line numbers"},
            },
            "required": ["file_path"],
        },
    },
]

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    tools=tools,
    messages=[{"role": "user", "content": "Find the auth middleware and read it."}],
)

# Process tool calls
for content_block in response.content:
    if content_block.type == "tool_use":
        tool_name = content_block.name
        tool_input = content_block.input
        # Execute the tool and send results back
```

**Tool loop pattern:**

```python
def run_tool_loop(client, messages, tools, max_turns=10):
    """Run a tool-calling conversation loop."""
    for _ in range(max_turns):
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            tools=tools,
            messages=messages,
        )

        messages.append({"role": "assistant", "content": response.content})

        # Check if Claude wants to use a tool
        tool_calls = [c for c in response.content if c.type == "tool_use"]
        if not tool_calls:
            break  # No more tool calls, conversation is done

        # Execute tools and append results
        for tool_call in tool_calls:
            result = execute_tool(tool_call.name, tool_call.input)
            messages.append({
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": tool_call.id,
                    "content": str(result),
                }],
            })

    return messages
```

### 4. Extended Thinking

Extended thinking enables deeper reasoning for complex tasks:

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=16000,  # Higher for thinking
    thinking={
        "type": "enabled",
        "budget_tokens": 10000,  # Tokens allocated to thinking
    },
    messages=[{
        "role": "user",
        "content": "Refactor this entire module to use hexagonal architecture. Explain your reasoning.",
    }],
)

# Thinking blocks are in the response but not returned to the user
for block in response.content:
    if block.type == "thinking":
        print("Internal reasoning (not shown to user):", block.thinking)
    elif block.type == "text":
        print("Final answer:", block.text)
```

**When to use extended thinking:**
- Complex refactoring or system design
- Multi-step reasoning (math, logic puzzles)
- Code review with deep architectural analysis
- Planning tasks with multiple constraints

**When NOT to use it:**
- Simple Q&A, summarization, or extraction
- Cost-sensitive high-volume workloads
- Latency-sensitive real-time applications

### 5. Prompt Caching

Anthropic supports prefix caching for repeated system prompts:

```python
# This system prompt will be cached after the first call
# Subsequent calls with the same prefix save time and cost

SYSTEM = "You are a senior Python developer. Always use type hints, follow PEP 8, ..."

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    system=SYSTEM,
    messages=[
        {"role": "user", "content": question_1},
        {"role": "assistant", "content": answer_1},
        {"role": "user", "content": question_2},
    ],
    # Cache the system prompt and first 2 messages
    extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"},
)
```

**Cache-friendly patterns:**
- Keep system prompts stable across calls
- Put variable content at the end of messages, not the beginning
- Batch similar requests together

### 6. Token Counting and Cost Estimation

```python
# Response includes usage data
response = client.messages.create(...)

input_tokens = response.usage.input_tokens
output_tokens = response.usage.output_tokens
cache_read_tokens = getattr(response.usage, "cache_read_input_tokens", 0)
cache_creation_tokens = getattr(response.usage, "cache_creation_input_tokens", 0)

# Pricing (check anthropic.com/pricing for current rates)
# Sonnet 4: $3/M input, $15/M output
# Cache read: $0.30/M, Cache creation: $3.75/M

def estimate_cost(
    input_tokens: int,
    output_tokens: int,
    cache_read: int = 0,
    cache_creation: int = 0,
    model: str = "sonnet",
) -> float:
    prices = {
        "sonnet": {"input": 3.0, "output": 15.0, "cache_read": 0.30, "cache_create": 3.75},
        "haiku": {"input": 0.80, "output": 4.0, "cache_read": 0.08, "cache_create": 1.0},
        "opus": {"input": 15.0, "output": 75.0, "cache_read": 1.50, "cache_create": 18.75},
    }
    p = prices[model]
    return (
        (input_tokens - cache_read - cache_creation) * p["input"] / 1_000_000
        + cache_read * p["cache_read"] / 1_000_000
        + cache_creation * p["cache_create"] / 1_000_000
        + output_tokens * p["output"] / 1_000_000
    )
```

### 7. Streaming Responses

```python
response_stream = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    messages=[{"role": "user", "content": "Write a long essay about Python metaclasses."}],
    stream=True,
)

full_text = ""
for event in response_stream:
    if event.type == "content_block_delta":
        delta = event.delta.text
        full_text += delta
        print(delta, end="", flush=True)
    elif event.type == "message_delta":
        # Final usage stats available here
        pass

print(f"\n\nTotal: {len(full_text)} characters")
```

### 8. Structured Output with JSON Mode

```python
import json

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=2048,
    messages=[{
        "role": "user",
        "content": """Extract all function names, their signatures, and docstrings
from this code. Return as JSON with this schema:
{
  "functions": [
    {"name": "...", "signature": "...", "docstring": "..."}
  ]
}
Only output valid JSON, no markdown fences, no explanation.""",
    }],
)

data = json.loads(response.content[0].text)
```

**For guaranteed schema compliance, add a validation step:**

```python
from pydantic import BaseModel, Field


class FunctionInfo(BaseModel):
    name: str
    signature: str
    docstring: str = ""


class CodeAnalysis(BaseModel):
    functions: list[FunctionInfo] = Field(default_factory=list)


# Validate the LLM output
data = json.loads(response.content[0].text)
validated = CodeAnalysis.model_validate(data)
```

### 9. Rate Limits and Fallback Strategies

**Rate limits by tier:**
- Free tier: ~50 RPM (requests per minute)
- Paid tier: ~1000+ RPM depending on model
- Token-per-minute limits also apply

**Retry with exponential backoff:**

```python
import time
from anthropic import RateLimitError, APITimeoutError


def call_with_retry(client, **kwargs, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.messages.create(**kwargs)
        except (RateLimitError, APITimeoutError) as e:
            if attempt == max_retries - 1:
                raise
            wait_time = (2 ** attempt) + (0.1 * attempt)  # Jitter
            time.sleep(wait_time)
        except Exception:
            raise  # Non-retryable errors bubble up immediately
```

**Model fallback:**

```python
FALLBACK_MODELS = [
    "claude-sonnet-4-20250514",   # Primary
    "claude-haiku-20241022",      # Faster, cheaper fallback
]


def call_with_model_fallback(**kwargs):
    for model in FALLBACK_MODELS:
        try:
            return client.messages.create(model=model, **kwargs)
        except Exception:
            continue
    raise RuntimeError("All model attempts failed")
```

### 10. Cost Optimization

| Strategy | Savings | When to Apply |
|---|---|---|
| **Use Haiku for simple tasks** | 70-80% vs Sonnet | Extraction, classification, summarization |
| **Prompt caching** | 90% on cached input | Repeated system prompts across sessions |
| **Reduce max_tokens** | Proportional | Set tight limits based on expected output |
| **Batch similar requests** | Cache efficiency | Process in groups with same system prompt |
| **Extended thinking only when needed** | Avoid waste | Simple tasks don't benefit from thinking |
| **Truncate long inputs** | Direct savings | Remove irrelevant context before sending |

## Anti-Patterns

- **Sending entire codebase as context** — Use retrieval or search to send only relevant chunks
- **No retry logic** — Rate limits are hit; always implement exponential backoff
- **Unlimited max_tokens** — Set conservative limits; LLMs can burn through tokens quickly
- **Ignoring usage data** — Always log input/output/cache tokens for cost tracking
- **Tool calls without validation** — Validate tool inputs before executing them
- **Not handling tool errors** — Tool failures should feed back into the conversation loop
- **Hardcoded API keys** — Use environment variables or secret managers

## Best Practices

1. **Start with Sonnet** — best quality/cost ratio for most tasks; fall back to Haiku for volume.
2. **Use extended thinking for complex reasoning** — refactoring, planning, multi-step analysis.
3. **Cache system prompts** — keep them stable and put variable content at the end.
4. **Stream for long outputs** — better UX and memory efficiency.
5. **Validate structured output** with Pydantic/Zod — never trust raw JSON from LLMs.
6. **Implement retry with backoff** — handle rate limits and timeouts gracefully.
7. **Track token usage per call** — log input, output, cache_read, cache_creation tokens.
8. **Set tight max_tokens** — estimate expected output length and add 20% headroom.
9. **Use tool loops for multi-step tasks** — let Claude decide which tools to call and when.
10. **Fallback models** — have a secondary model ready for when the primary is unavailable.

## Related Skills

- `prompt-optimizer` — Prompt compression, few-shot selection, and evaluation
- `token-budget-advisor` — Context window allocation and cost estimation
- `openai-api` — Parallel knowledge for OpenAI API patterns
- `iterative-retrieval` — Progressive context loading before LLM calls
- `agentic-engineering` — Agent orchestration that uses Claude as the reasoning engine
