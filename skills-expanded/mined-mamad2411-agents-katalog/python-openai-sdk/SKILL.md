---
name: python-openai-sdk
description: Use when calling OpenAI from Python — sync/async, streaming, structured outputs (responses API + json_schema), tool use, cost guardrails, retry/timeout.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: domain
  languages: [python]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-18"
  related: [python-essentials, python-django, python-fastapi, python-pydantic-v2, security, observability-essentials]
---

# Python OpenAI SDK

**Iron Law: every call sets a timeout, a `max_tokens` (or `max_output_tokens`), and a retry budget. Validate the model's output against a schema — never act on free-text directly. For TypeScript/Node use the `openai` npm SDK; the patterns rhyme but the ergonomics differ — this skill is Python-only.**

**Versions:** `openai` Python SDK `1.55+` · Pydantic `2.9+` · tiktoken `0.8+` — _The Responses API (`client.responses._`) is the supported path going forward; Chat Completions still works for now but new features land on Responses first. `client.responses.parse(...)` returns typed Pydantic instances and is the cleanest structured-outputs ergonomic.\*

## Client init

```python
from openai import OpenAI, AsyncOpenAI

client = OpenAI(
    # api_key=... defaults to env var OPENAI_API_KEY
    organization=os.getenv("OPENAI_ORG"),                # optional
    project=os.getenv("OPENAI_PROJECT"),                 # optional, scopes billing
    base_url=os.getenv("OPENAI_BASE_URL"),               # set for Azure / LiteLLM / vLLM proxy
    timeout=httpx.Timeout(60.0, connect=5.0),            # split connect vs read
    max_retries=2,                                        # SDK retries 5xx + 429 with backoff
)

aclient = AsyncOpenAI(timeout=60.0, max_retries=2)        # use in FastAPI / async workers
```

**One client per process**, reused — the SDK keeps an httpx connection pool. **Never** instantiate per-request; you'll exhaust local ports under load.

**Azure OpenAI / proxy**: set `base_url` to the Azure endpoint (`https://<resource>.openai.azure.com/openai/v1/`) plus `api_version` via `default_query={"api-version": "..."}`, or use `AzureOpenAI`. For LiteLLM/vLLM/local models: same OpenAI client, just point `base_url` at the proxy.

## Sync vs async

| Workload                                        | Pick                                                      |
| ----------------------------------------------- | --------------------------------------------------------- |
| Django request handler (sync view)              | `OpenAI` — wrap with `sync_to_async` if mixing into async |
| FastAPI / async DRF / Strawberry async          | `AsyncOpenAI` — `await client.responses.create(...)`      |
| Background batch worker over thousands of items | `AsyncOpenAI` + `asyncio.Semaphore` for concurrency cap   |
| Streaming to the browser (SSE)                  | async — `async for event in stream:`                      |

```python
import asyncio
sem = asyncio.Semaphore(8)         # cap to ≤ rate-limit headroom

async def summarize(text: str) -> str:
    async with sem:
        r = await aclient.responses.create(
            model="gpt-4.1-mini", input=text, max_output_tokens=300,
        )
        return r.output_text
```

## Streaming

```python
stream = client.responses.create(model="gpt-4.1", input=prompt, stream=True)
for event in stream:
    if event.type == "response.output_text.delta":
        sys.stdout.write(event.delta); sys.stdout.flush()
    elif event.type == "response.completed":
        usage = event.response.usage        # token counts available at the end
```

Async streaming is the same shape with `async for`. Always handle `response.error` events; the stream can fail mid-flight after partial output.

## Structured outputs — the only safe way to act on a model's reply

```python
from pydantic import BaseModel, Field
from typing import Literal

class Triage(BaseModel):
    severity: Literal["low", "medium", "high"]
    summary: str = Field(max_length=280)
    next_action: Literal["close", "escalate", "respond"]

# Responses API — typed, validated, retries on schema mismatch internally
resp = client.responses.parse(
    model="gpt-4.1-mini",
    input=[{"role": "user", "content": ticket_text}],
    text_format=Triage,
    max_output_tokens=500,
)
triage: Triage = resp.output_parsed          # guaranteed shape, or a refusal
```

For the Chat Completions API the equivalent is `response_format={"type": "json_schema", "json_schema": {"name": "triage", "schema": Triage.model_json_schema(), "strict": True}}` — `strict: True` is the load-bearing flag; without it the model can drift from the schema.

**Refusals are real**: `resp.output_parsed` can be `None` if the model refused. Branch on it:

```python
if resp.output_parsed is None:
    log.warning("model refused", extra={"refusal": resp.output[0].content[0].refusal})
    raise ValueError("refused")
```

See `Skill(devkit:python-pydantic-v2)` for schema design — keep models flat, use `Literal` for enums, avoid `Union` over more than 3 types (constrained decoding struggles).

## Tool / function calling

```python
tools = [{
    "type": "function",
    "name": "lookup_order",
    "description": "Look up an order by SKU and return status + ship date.",
    "parameters": {
        "type": "object",
        "properties": {"sku": {"type": "string"}},
        "required": ["sku"], "additionalProperties": False,
    },
    "strict": True,                          # constrained decoding — guarantees valid args
}]

resp = client.responses.create(
    model="gpt-4.1", input=user_msg, tools=tools, max_output_tokens=400,
)
for item in resp.output:
    if item.type == "function_call":
        args = json.loads(item.arguments)
        result = lookup_order(**args)        # YOU run the tool; the model doesn't
        # Send result back in a follow-up turn with previous_response_id=resp.id
        follow = client.responses.create(
            model="gpt-4.1",
            previous_response_id=resp.id,
            input=[{"type": "function_call_output", "call_id": item.call_id, "output": json.dumps(result)}],
        )
```

**Tool calls are the model asking you to run code; you decide if and how.** Treat tool args as untrusted input: validate, authorize, rate-limit. Never let the model invoke shell commands, raw SQL, file deletes, or money-moving APIs without an additional human gate.

## Cost guardrails

| Knob                                                  | Effect                                                                                                              |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `max_output_tokens` (Responses) / `max_tokens` (Chat) | Hard cap — model can't run away                                                                                     |
| Pick the smallest model that works                    | `gpt-4.1-mini` ≈ 1/5 the cost of `gpt-4.1` on most tasks                                                            |
| Prompt caching (automatic on prefixes ≥ 1024 tokens)  | Repeated system prompts are billed at ~10–50% rate; structure prompts with stable prefix first, variable input last |
| Batch API (`/v1/batches`)                             | 50% off for jobs you can wait up to 24h on — perfect for nightly re-classify of historical data                     |
| `tiktoken` to pre-count                               | Estimate cost before sending; reject inputs over your budget                                                        |
| Set per-project spend limits in the OpenAI dashboard  | Hard ceiling — failed payments beat a runaway loop                                                                  |
| Log `response.usage` to your metrics                  | `input_tokens`, `output_tokens`, `cached_input_tokens` — you can't optimize what you don't measure                  |

```python
import tiktoken
enc = tiktoken.encoding_for_model("gpt-4.1")
n_tokens = len(enc.encode(prompt))
if n_tokens > 30_000:
    raise ValueError(f"prompt too large: {n_tokens} tokens")
```

## Retry, timeout, error handling

| Exception                       | Mean                                                                                            |
| ------------------------------- | ----------------------------------------------------------------------------------------------- |
| `RateLimitError` (429)          | SDK retries with backoff automatically when `max_retries > 0`                                   |
| `APITimeoutError`               | Your `timeout` fired — increase or split the request                                            |
| `APIConnectionError`            | Network — SDK retries idempotent reads; safe to retry creates too (server dedup not guaranteed) |
| `BadRequestError` (400)         | Schema/param issue — don't retry; fix the call                                                  |
| `AuthenticationError` (401)     | Key bad or revoked — don't retry; alert                                                         |
| `PermissionDeniedError` (403)   | Org/project doesn't have access to that model                                                   |
| `InternalServerError` (500/503) | SDK retries; if persistent, fall back to a smaller/older model                                  |

**Use the SDK's `max_retries`**, don't reinvent. For request-level idempotency (e.g., to prevent double-charging on a retry), pass `extra_headers={"Idempotency-Key": uuid.uuid4().hex}` — supported by the Responses API.

## Anti-patterns

- Feeding model output into a Python `eval` or dynamic code path — RCE risk; use structured outputs
- Constructing SQL from the model's free-text — see `Skill(devkit:security)` injection; parameterize
- Logging full prompts + completions at INFO — PII leak; redact or sample at DEBUG only
- Sending raw user input directly as the system prompt — prompt injection; isolate user content in a clearly delimited block, never the system role
- Calling `client.chat.completions.create` for new code — use Responses API
- No `max_output_tokens` — model writes an essay, bill arrives
- Per-request `OpenAI()` instantiation — connection-pool churn
- Streaming without handling mid-stream errors — silent half-responses to users
- Trusting tool-call args as authorized — re-check authorization on every call, not just the first turn
- Disabling TLS verification on a corporate proxy to "make it work" — fix the cert; never turn off verification

## Red flags

| Thought                                   | Reality                                                                   |
| ----------------------------------------- | ------------------------------------------------------------------------- |
| "I'll parse the JSON the model wrote"     | It will hallucinate fields. Use `responses.parse(text_format=Model)`.     |
| "We don't need a timeout, OpenAI is fast" | Until it isn't. 5 min hangs cost real money in worker queues.             |
| "I'll retry on every error"               | 400s never succeed; you'll loop forever. Retry only transient classes.    |
| "GPT-4.1 for everything"                  | Try `4.1-mini` first; you'll be surprised how often it wins on cost-perf. |
| "Tool calls = secure"                     | The model picks WHICH tool to call; YOU re-authorize every invocation.    |
| "Prompt injection won't happen to us"     | It will. Treat user-supplied text as data, not instructions.              |

## Hand-off

For broader Python rules: `Skill(devkit:python-essentials)`. For schema design with Pydantic (structured outputs lean on this): `Skill(devkit:python-pydantic-v2)`. For Django/DRF integration: `Skill(devkit:python-django)`. For async FastAPI usage: `Skill(devkit:python-fastapi)`. For prompt-injection mitigation and secret handling: `Skill(devkit:security)`. For tracing/cost metrics on LLM calls: `Skill(devkit:observability-essentials)`.
