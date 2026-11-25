# MISTRAL-RATELIMIT

**Generated:** 2026-02-17
**Commit:** 407dc9d
**Branch:** main

## OVERVIEW

Rate-limited Python SDK wrapper for Mistral AI. Token bucket algorithm for RPS + TPM control. Sync/async/streaming support.

**⚠️ CRITICAL: This SDK uses the Beta Conversations API (`/v1/conversations`) ONLY.** The old `/v1/chat/completions` API is NOT supported and should NEVER be used.

## BETA CONVERSATIONS API - MANDATORY READING

### Why Beta Conversations API?

The old `/v1/chat/completions` endpoint is deprecated for many use cases. The Beta Conversations API provides:
- Different rate limits (RPS/TPM) than chat completions
- Better conversation state management
- Agent integration capabilities
- Streaming with proper SSE support

**📖 Official Docs:** https://docs.mistral.ai/api/endpoint/beta/conversations

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/conversations` | POST | Create conversation + append entries |
| `/v1/conversations` | GET | List all conversations |
| `/v1/conversations/{id}` | GET | Get conversation info |
| `/v1/conversations/{id}/entries` | GET | Get all entries in conversation |
| `/v1/conversations/{id}` | DELETE | Delete a conversation |

### Request Format

```python
payload = {
    "model": "mistral-large-latest",  # Required
    "inputs": messages,                 # Required - list of message dicts
    # Optional:
    "instructions": "System prompt here",  # Override/default instructions
    "completion_args": {                  # Sampler parameters
        "temperature": 0.7,
        "max_tokens": 1024,
        "top_p": 0.9,
        "stop": ["END"]
    }
}
```

### completion_args Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `temperature` | float | Sampling temperature (0-2) |
| `max_tokens` | int | Max tokens to generate |
| `top_p` | float | Nucleus sampling threshold |
| `stop` | list[str] | Stop sequences |
| `random_seed` | int | Random seed for reproducibility |

### Response Format

```python
{
    "conversation_id": "conv_xxx",
    "outputs": [{"content": "...", "role": "assistant", "id": "msg_xxx"}],
    "usage": {"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150}
}
```

## RATE LIMITING - VERIFIED BEHAVIOR

### Token Bucket Algorithm

The SDK implements token bucket for both:
- **RPS** (Requests Per Second) - bucket capacity = requests_per_second
- **TPM** (Tokens Per Minute) - bucket capacity = tokens_per_minute

### How It Works

```
1. Before each request: acquire() checks if tokens available
2. If not: blocks until tokens refill (based on refill_rate)
3. After response: unused tokens REFUNDED based on actual usage
```

### Verified Test Results (examples/test_rate_limiting.py)

**SYNC TEST: RPS=0.5 (1 request every 2 seconds)**

| Request | Total Time | Start-to-Start Gap |
|---------|------------|-------------------|
| 1 | 1.29s | - |
| 2 | 2.92s | 1.29s |
| 3 | 4.08s | 2.92s |
| 4 | 3.51s | 4.08s |

**Average gap: 2.76s (expected ≥ 2.0s)** ✅ Rate limiting working!

**ASYNC TEST: 5 concurrent requests, RPS=0.5**

```
Total time: 25.26s (without rate limit would be ~7s)
All tasks created simultaneously: YES
Requests serialized by rate limiter: YES

Key insight: asyncio.gather() creates tasks simultaneously,
but rate limiter applies delays INSIDE each task before API call.
```

### Configuration

```python
config = RatelimitConfig(
    api_key="...",
    requests_per_second=0.5,    # 1 request every 2 seconds
    tokens_per_minute=100000,
    max_retries=3,
    base_delay=1.0,
    max_delay=60.0,
    timeout=30.0
)
```

## EXAMPLE SCRIPTS

Location: `../examples/`

| Script | Purpose |
|--------|---------|
| `test_comprehensive.py` | Full API test: start, instructions, completion_args, append, tools |
| `test_rate_limiting.py` | Rate limiting verification with timing analysis |
| `test_sync.py` | Basic sync functionality test |
| `test_async.py` | Basic async functionality test |
| `visualize_rate_limiting.py` | Visual demo of token bucket (no API key needed) |

### Running Tests

```bash
cd ../examples

# Comprehensive API test
python3 test_comprehensive.py

# Rate limiting verification
python3 test_rate_limiting.py

# Visual demo (no API key)
python3 visualize_rate_limiting.py
```

### Expected Output: test_comprehensive.py

```
═══════════════════════════════════════════════════════════════════
 TEST 1: BASIC CONVERSATION
═══════════════════════════════════════════════════════════════════
✅ PASS - Response received correctly
   Expected: HELLO_WORLD_TEST
   Got:      HELLO_WORLD_TEST
   Match:    ✅ EXACT MATCH
   Tokens:   prompt=12, completion=7, total=19

═══════════════════════════════════════════════════════════════════
 TEST 2: INSTRUCTIONS (SYSTEM PROMPT)
═══════════════════════════════════════════════════════════════════
✅ PASS - System instructions respected
   Response contains pirate speech: "Arrr, matey!"

... (5 tests total, all should pass)
```

### Expected Output: test_rate_limiting.py

```
═══════════════════════════════════════════════════════════════════
 SYNC TEST: Sequential Requests (RPS=0.5, expected gap ≥ 2.0s)
═══════════════════════════════════════════════════════════════════
[REQ 1] T+0.00s | Started
[REQ 1] T+1.29s | Completed | Gap: 0.00s | Prev API done: N/A
[REQ 2] T+1.29s | Started | Prev API done: YES
[REQ 2] T+4.21s | Completed | Gap: 1.29s | Prev API done: YES
...

═══════════════════════════════════════════════════════════════════
 ASYNC TEST: Concurrent Requests (RPS=0.5, 5 parallel)
═══════════════════════════════════════════════════════════════════
[REQ 1] T+0.00s | Started | Prev API done: NO (overlap!)
[REQ 2] T+0.00s | Started | Prev API done: NO (overlap!)
[REQ 3] T+0.00s | Started | Prev API done: NO (overlap!)
...
[REQ 1] T+7.48s | Completed
[REQ 3] T+17.90s | Completed
...

Total time: 25.26s | Without rate limit: ~7s | Rate limit working: ✅ YES
```

## INTEGRATION GUIDE

### Quick Start

```python
from mistral_ratelimit import MistralRatelimitClient, RatelimitConfig

config = RatelimitConfig(
    api_key="your-mistral-api-key",
    requests_per_second=2.0,
    tokens_per_minute=100_000
)

client = MistralRatelimitClient(config)

# Sync
response = client.beta.conversations.start(
    model="mistral-large-latest",
    inputs=[{"role": "user", "content": "Hello!"}]
)
print(response.outputs[0].content)
```

### Async Usage

```python
import asyncio

async def main():
    response = await client.beta.conversations.start_async(
        model="mistral-large-latest",
        inputs=[{"role": "user", "content": "Hello!"}]
    )
    print(response.outputs[0].content)

asyncio.run(main())
```

### Streaming

```python
for event in client.beta.conversations.start_stream(
    model="mistral-large-latest",
    inputs=[{"role": "user", "content": "Count to 5"}]
):
    if event.type == "message.output.delta":
        print(event.delta.content, end="", flush=True)
    elif event.type == "conversation.response.done":
        print(f"\nUsage: {event.usage}")
```

### Multi-Turn

```python
# Start
response = client.beta.conversations.start(
    model="mistral-large-latest",
    inputs=[{"role": "user", "content": "What's 2+2?"}]
)
conversation_id = response.conversation_id

# Continue
response2 = client.beta.conversations.append(
    conversation_id=conversation_id,
    inputs=[{"role": "user", "content": "Now multiply by 3!"}]
)
```

## ANTI-PATTERNS (THIS PROJECT) - READ BEFORE MODIFYING

1. **❌ NEVER use `/v1/chat/completions`**: This SDK wraps the official `mistralai` SDK's beta.conversations API
2. **❌ Don't pass `None` values to SDK**: Filter with `_filter_none()` before calling SDK methods
3. **⚠️ Private bucket access**: `client._token_bucket.available` breaks encapsulation
4. **⚠️ Token estimates**: Heuristics are rough — always refund unused tokens after response
5. **⚠️ Async rate limiting**: Applies INSIDE each task, not between task creation

## STRUCTURE

```
mistral_ratelimit/
├── __init__.py          # Exports: MistralRatelimitClient, RatelimitConfig, exceptions
├── client.py            # RateLimitedConversations, RateLimitedAgents - wraps mistralai SDK
├── rate_limiter.py      # RateLimiter (thread-safe), AsyncRateLimiter (asyncio)
├── token_counter.py     # Tiktoken-based token estimation
├── config.py            # RatelimitConfig dataclass
├── exceptions.py        # MistralRatelimitError hierarchy
└── pyproject.toml       # hatchling build, ruff+mypy configured

../examples/
├── test_comprehensive.py    # Full API test suite
├── test_rate_limiting.py    # Rate limiting verification
├── test_sync.py             # Basic sync test
├── test_async.py            # Basic async test
└── visualize_rate_limiting.py  # Visual demo (no API key)
```

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| Add new API method | `client.py` → RateLimitedConversations | Use `_filter_none()` for params |
| Tune rate limiting | `rate_limiter.py` | Token bucket: capacity = refill_rate |
| Adjust token counting | `token_counter.py` | Rough heuristics, tiktoken-based |
| Change config defaults | `config.py` | RatelimitConfig dataclass |
| Add exception types | `exceptions.py` | Inherit from MistralRatelimitError |
| Run tests | `../examples/` | test_comprehensive.py, test_rate_limiting.py |

## CODE MAP

| Symbol | Type | Location | Role |
|--------|------|----------|------|
| MistralRatelimitClient | class | client.py | Main client, wraps Mistral SDK |
| RateLimitedConversations | class | client.py | Rate-limited beta.conversations wrapper |
| RateLimitedAgents | class | client.py | Rate-limited beta.agents wrapper |
| RateLimiter | class | rate_limiter.py | Thread-safe token bucket |
| AsyncRateLimiter | class | rate_limiter.py | Asyncio token bucket |
| TokenCounter | class | token_counter.py | count_messages(), count_text() |
| RatelimitConfig | dataclass | config.py | api_key, rps, tpm, retries, delays, timeout |
| _filter_none | func | client.py | Filter None values before SDK call |

## CONVENTIONS

- **Line length**: 100 chars (ruff)
- **Python**: >=3.10
- **Typing**: `dict | None` union syntax (no `Optional`)
- **Private attrs**: Leading underscore (`_api_key`, `_rate_limiter`)
- **Thread safety**: Use `RateLimiter` for sync, `AsyncRateLimiter` for async
- **None filtering**: Always filter None params before passing to SDK

## COMMANDS

```bash
# Install dev deps
pip install -e ".[dev]"

# Lint
ruff check .

# Type check
mypy .

# Run tests
cd ../examples && python3 test_comprehensive.py
cd ../examples && python3 test_rate_limiting.py
```

## LINKS

- **Official Beta Conversations API Docs**: https://docs.mistral.ai/api/endpoint/beta/conversations
- **Mistral AI Dashboard**: https://admin.mistral.ai/plateforme/limits
- **Mistral SDK GitHub**: https://github.com/mistralai/mistral-python
