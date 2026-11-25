---
name: braintrust-logging
description: Instrument production AI code with Braintrust logging, including traces, spans, wrapped LLM clients, and online scoring. Use when capturing production requests or closing the loop between logs and evals.
---

# Braintrust Logging

Production requests are captured as traces made of spans. Logs and evals share
the same data structures, so any interesting log can become a test case.
Auth: `BRAINTRUST_API_KEY` env var (keys start with `sk-`).

## Initialize and wrap

```typescript
import { initLogger, wrapOpenAI, wrapTraced } from "braintrust";
import OpenAI from "openai";

const logger = initLogger({ projectName: "My Project" });
const client = wrapOpenAI(new OpenAI());   // auto-logs every LLM call

const answerQuestion = wrapTraced(async function answerQuestion(q: string) {
  const res = await client.chat.completions.create({
    model: "gpt-5-mini",
    messages: [{ role: "user", content: q }],
  });
  return res.choices[0].message.content;
});
```

```python
from braintrust import init_logger, traced, wrap_openai
from openai import OpenAI

logger = init_logger(project="My Project")
client = wrap_openai(OpenAI())

@traced
def answer_question(q: str) -> str:
    res = client.chat.completions.create(
        model="gpt-5-mini", messages=[{"role": "user", "content": q}]
    )
    return res.choices[0].message.content
```

Wrapped clients log input, output, token counts, latency, cost, and model
config per call. Prefer auto-instrumentation (wrapped clients and supported
framework integrations) over hand-built spans; add manual spans only around
your own business logic.

## Manual spans and fields

Inside traced code, attach fields to the current span: `input`, `output`,
`expected`, `metadata`, `tags`, and `scores`. Typical pattern: log the user
id and feature flags as metadata at the root span, then log a score when
feedback arrives (thumbs up = 1, thumbs down = 0) against the original span
so quality is measurable per request. Span types include `llm`, `tool`,
`function`, `task`, `score`, `eval`, `classifier`.

Logs are buffered and flushed in the background; in serverless handlers flush
before returning.

## Online scoring

Online scoring runs scorers (autoevals or custom, see `braintrust-evals`)
automatically on a sample of incoming production logs, configured per project
in the UI: choose scorers, sampling rate, and which spans they apply to. This
gives continuous quality metrics without shipping judge code in your app.

## Working the logs

- The Logs page is a searchable trace table: filter point-and-click, or query
  with SQL/BTQL; save custom views.
- Topics auto-clusters logs into facets (task, sentiment, issues) to surface
  silent failures and blind spots.
- Dashboards aggregate request counts, latency, token usage, cost, and scores
  over time.
- One-click: add any log row to a dataset to grow your eval suite; this
  production-to-eval loop is the core Braintrust workflow.
- The bundled Braintrust MCP server exposes BTQL queries, experiment
  summaries, and permalinks, so you can triage logs directly from Caeros.
