---
name: adaline-logs
description: "Send traces and spans to Adaline for AI agent observability. Use when instrumenting LLM calls, tools, retrieval, embeddings, guardrails, or custom operations."
---

# Adaline Logs

## Concepts

Adaline Logs captures AI application execution as traces and spans.

Key terms:
- **Trace** — one end-to-end user request, agent run, job, or conversation turn
- **Span** — one operation inside a trace, such as an LLM call or retrieval step
- **referenceId** — caller-supplied ID for stitching traces/spans across services
- **sessionId** — groups related traces, such as a chat thread
- **Content type** — semantic span payload: `Model`, `ModelStream`, `Tool`, `Retrieval`, `Embeddings`, `Function`, `Guardrail`, or `Other`

## Configuration

Set these environment variables when credentials are available:
- `ADALINE_API_KEY` — workspace API key from Admin > API Keys
- `ADALINE_PROJECT_ID` — project ID

Base URL: `https://api.adaline.ai/v2`

## Quick Start

### TypeScript SDK

```typescript
import { Adaline } from '@adaline/client';
import type { LogSpanContent } from '@adaline/api';

const adaline = new Adaline();
const monitor = adaline.initMonitor({ projectId: process.env.ADALINE_PROJECT_ID! });

const trace = monitor.logTrace({ name: 'chat-request', sessionId: 'user_42' });

const span = trace.logSpan({
  name: 'llm-call',
  status: 'unknown',
});

// Run provider call here.

span.update({
  status: 'success',
  content: {
    type: 'Model',
    provider: 'openai',
    model: 'gpt-4o',
    input: JSON.stringify(openaiRequest),
    output: JSON.stringify(openaiResponse),
  } as LogSpanContent,
});
span.end();

trace.update({ status: 'success' });
trace.end();

await monitor.flush();
monitor.stop();
```

### Python SDK

```python
import json
from adaline import Adaline
from adaline_api.models.log_span_content import LogSpanContent
from adaline_api.models.log_span_model_content import LogSpanModelContent

adaline = Adaline()
monitor = adaline.init_monitor(project_id="project_abc123")

trace = monitor.log_trace(name="chat-request", session_id="user_42")
span = trace.log_span(name="llm-call", status="unknown")

# Run provider call here.

span.update({
    "status": "success",
    "content": LogSpanContent(LogSpanModelContent(
        type="Model",
        provider="openai",
        model="gpt-4o",
        input=json.dumps(openai_request),
        output=json.dumps(openai_response),
    )),
})
span.end()

trace.update({"status": "success"})
trace.end()

await monitor.flush()
monitor.stop()
```

### REST API

```bash
curl -X POST "https://api.adaline.ai/v2/logs/trace" \
  -H "Authorization: Bearer $ADALINE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "projectId": "project_abc123",
    "trace": {
      "name": "chat-request",
      "status": "success",
      "referenceId": "request-123",
      "startedAt": 1713657600000,
      "endedAt": 1713657602500
    },
    "spans": [
      {
        "name": "llm-call",
        "status": "success",
        "referenceId": "span-123",
        "startedAt": 1713657600100,
        "endedAt": 1713657602400,
        "content": {
          "type": "Model",
          "provider": "openai",
          "model": "gpt-4o",
          "input": "{\"messages\":[]}",
          "output": "{\"choices\":[]}"
        }
      }
    ]
  }'
```

## Integration Patterns

### Single-service logging

Use the SDK monitor. Create a trace, create spans from that trace, call `end()`, then flush before process exit.

### Nested spans

```typescript
const parent = trace.logSpan({ name: 'agent-loop', referenceId: 'loop-1' });
const child = parent.logSpan({ name: 'tool-call' });
child.end();
parent.end();
```

```python
parent = trace.log_span(name="agent-loop", reference_id="loop-1")
child = parent.log_span(name="tool-call")
child.end()
parent.end()
```

### Distributed tracing

Use REST `POST /logs/span` or raw SDK `logsApi`/`logs_api` with `traceReferenceId` / `trace_reference_id` when a different process needs to attach a span to an existing trace.

### User feedback and trace metadata

Use `PATCH /logs/trace` with `logTrace.attributes` and `logTrace.tags` operation arrays.

## Best Practices

1. Store provider request/response bodies as JSON strings in span `input` and `output`.
2. Use `referenceId` on traces and spans so distributed systems can stitch work together.
3. Use `sessionId` for multi-turn chats or long-running workflows.
4. End spans before ending traces; trace end will also end child spans as a safety net.
5. Await `monitor.flush()` in Python and TypeScript before shutdown/serverless return.
6. In Python, pass generated `LogSpanContent(...)` wrapper objects, not raw dictionaries, for SDK span content.

## References

See references/api.md for REST payloads.
See references/typescript-sdk.md for TypeScript SDK usage.
See references/python-sdk.md for Python SDK usage.
