---
name: langfuse-tracing
description: Instrument LLM apps with Langfuse tracing using the OpenTelemetry-based Python and JS/TS SDKs, including decorators, spans, generations, trace attributes, and framework integrations. Use when adding or debugging Langfuse instrumentation.
---

# Langfuse Tracing

Current SDKs are OpenTelemetry-based (Python SDK v4, JS/TS SDK v5). Install:
`pip install langfuse` / `npm install @langfuse/tracing @langfuse/otel`.
Auth via env vars (see the `langfuse-setup` skill): `LANGFUSE_PUBLIC_KEY`,
`LANGFUSE_SECRET_KEY`, `LANGFUSE_BASE_URL`.

## Python: decorator first

```python
from langfuse import observe

@observe()
def process(data, parameter):
    return {"processed": data}

@observe(name="llm-call", as_type="generation")
async def call_llm(prompt_text):
    return "response"
```

Options: `name`, `as_type`, `capture_input=False`, `capture_output=False`.
IO capture can also be toggled globally via
`LANGFUSE_OBSERVE_DECORATOR_IO_CAPTURE_ENABLED`.

## Python: context managers for explicit control

```python
from langfuse import get_client, propagate_attributes

langfuse = get_client()  # singleton, reads env vars

with langfuse.start_as_current_observation(
    as_type="span", name="user-request", input={"query": "..."}
) as root:
    with propagate_attributes(user_id="user_123", session_id="sess_abc"):
        with langfuse.start_as_current_observation(
            as_type="generation", name="answer", model="gpt-4o"
        ) as gen:
            gen.update(output=text, usage_details={"input": 12, "output": 88})
```

- `as_type`: `"span"` (default), `"generation"` (LLM calls, takes `model`),
  `"tool"` (tool or function calls).
- Child observations nested in the `with` block inherit the parent automatically.
- Update without a direct reference: `langfuse.update_current_span(metadata={...})`
  or `langfuse.update_current_generation(output=..., usage_details={...})`.

## Trace attributes

`propagate_attributes(...)` sets attributes inherited by all nested
observations: `user_id`, `session_id`, `metadata`, `version`, `environment`,
`trace_name`. Pass `as_baggage=True` to propagate across HTTP calls for
distributed tracing.

## Integrations (Python)

- OpenAI drop-in: `from langfuse.openai import openai`, then use the client as
  usual; calls become generations automatically.
- LangChain: pass the Langfuse callback handler
  (`from langfuse.langchain import CallbackHandler`) into `invoke`/`stream`.
- Any OpenTelemetry instrumentation (OpenLLMetry, OpenInference) exports into
  the same trace tree because the SDK is a standard OTel setup.

## JS/TS (SDK v5)

Packages: `@langfuse/tracing` (spans), `@langfuse/otel`
(`LangfuseSpanProcessor` for export), `@langfuse/openai` (auto-trace the
OpenAI SDK), `@langfuse/langchain`. Register the processor on a `NodeSDK`,
then wrap work with `startActiveObservation(...)`. Call `await sdk.shutdown()`
before short-lived processes exit.

## Lifecycle

Events are buffered and sent in the background. In scripts, serverless
functions, and workers call `langfuse.flush()` (or `langfuse.shutdown()` to
also stop background threads) before exit, otherwise traces are lost.

## Debugging

- No traces: check keys and `LANGFUSE_BASE_URL` region, then confirm `flush()`.
- Broken nesting: ensure children are created inside the parent context block.
- Exact parameter shapes: https://langfuse.com/docs (or the bundled Langfuse
  Docs MCP server) is authoritative; SDK surfaces evolve quickly.
