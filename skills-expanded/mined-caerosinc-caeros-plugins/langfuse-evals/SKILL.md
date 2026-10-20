---
name: langfuse-evals
description: Evaluate LLM apps in Langfuse with scores, LLM-as-a-judge evaluators, datasets, and experiments. Use when setting up online or offline evaluation, scoring traces, or comparing prompt and model variants.
---

# Langfuse Evaluation

Two loops: **online** (score live production traces) and **offline** (run
experiments against datasets before shipping). Both produce scores attached to
traces, observations, or sessions.

## Scores

Data types: `NUMERIC`, `CATEGORICAL`, `BOOLEAN`, `TEXT`.

```python
from langfuse import get_client
langfuse = get_client()

langfuse.create_score(
    name="accuracy",
    value=0.92,                  # float, or string for CATEGORICAL
    trace_id=trace_id,
    observation_id=obs_id,       # optional: score one observation
    session_id=None,             # optional: session-level score
    data_type="NUMERIC",
    comment="grounded in retrieved docs",
    score_id=None,               # idempotency key, pass to update
)
```

In-context shortcuts while instrumented code runs:
`span.score(...)`, `span.score_trace(...)`,
`langfuse.score_current_span(...)`, `langfuse.score_current_trace(...)`.

JS/TS: `langfuse.score.create({traceId, name, value, dataType, ...})`, then
`await langfuse.flush()` in short-lived environments.

REST: `POST /api/public/scores` with Basic auth (public key as username,
secret key as password), same fields.

## LLM-as-a-judge (online)

Configured in the Langfuse UI: pick a managed evaluator template (hallucination,
helpfulness, toxicity, relevance, etc.) or write a custom judge prompt, map
trace fields into the template variables, choose the model, and set sampling
(e.g. 10% of production traces) plus filters. Scores appear on traces
automatically. Start with sampling low: judge calls cost tokens.

## Datasets

A dataset is a reusable set of test cases with `input` and `expected_output`.

```python
langfuse.create_dataset(name="qa-regression")
langfuse.create_dataset_item(
    dataset_name="qa-regression",
    input={"question": "What is Langfuse?"},
    expected_output="An open-source LLM engineering platform",
    metadata={"source": "docs"},
)
```

Seed items from the UI, the SDK, or by converting interesting production
traces into dataset items (one click in the trace view).

## Experiments (offline)

Run your app over a dataset and link each execution to its item, producing a
named dataset run you can compare in the UI:

```python
dataset = langfuse.get_dataset("qa-regression")
for item in dataset.items:
    with item.run(run_name="prompt-v5") as root_span:
        output = my_app(item.input)
        root_span.update_trace(output=output)
        root_span.score_trace(name="exact_match",
                              value=float(output == item.expected_output))
```

Compare runs side by side (scores, latency, cost) to gate prompt or model
changes; combine with prompt labels (see `langfuse-prompts`) for safe rollout.
LLM-as-a-judge evaluators can also be applied to experiment runs.

## Human review

Annotation queues route traces to reviewers who attach scores through the UI;
user feedback from your app lands as scores through the same API. Use human
labels to calibrate and spot-check judge evaluators.

## Practices

- Name scores consistently; dashboards and run comparisons group by name.
- Track a small core set (correctness, groundedness, format validity) rather
  than many one-off metrics.
- Exact current SDK shapes: verify via https://langfuse.com/docs or the
  bundled Langfuse Docs MCP server.
