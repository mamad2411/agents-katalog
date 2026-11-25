---
name: domino-genai-tracing
description: Trace and evaluate GenAI applications (LLM calls, agents, RAG pipelines, multi-step AI systems) in Domino with the Domino agents SDK, using the @add_tracing decorator, span and trace evaluators, DominoAgentContext / DominoRun evaluation runs with aggregated metrics, manual MLflow spans, and post-hoc or production scoring with search_traces, search_agent_traces and log_evaluation. Captures inputs, outputs, token usage, latency, tool calls and errors per span. Use when building or debugging agents and LLM apps on Domino, adding evaluators or LLM-as-judge scoring, comparing agent versions in Experiment Manager, or scoring the production traces of a deployed agent.
compatibility: Domino 6.3 and Domino Cloud (agents SDK needs Domino 6.2+ and MLflow 3.2+; the DSE ships MLflow 3.3.2). Runs inside Domino executions, where MLFLOW_TRACKING_URI and DOMINO_API_HOST are set.
---

# Domino GenAI Tracing

Applies to Domino 6.3 and Domino Cloud.

Tracing records every call an agentic system makes (LLM calls, tool invocations, retrieval, nested agents) as a trace of spans with evaluator scores attached, so agent versions can be compared in Experiment Manager and production agents monitored. Works on the DSE as shipped; install nothing there.

## Two modes

| Mode | Where traces appear | What the code does |
|------|---------------------|--------------------|
| **Development / evaluation**: a script run in a Workspace or, for a deployable agent version, as a Domino Job | **Experiments** > experiment > run (agent version) > **Traces** tab | Wrap the evaluation loop in `DominoAgentContext` (or `DominoRun`); evaluators passed to `@add_tracing` run after every call and the run logs aggregated metrics at exit |
| **Deployed agent**: a Domino App whose request handler is decorated | The agent's details page: **Performance**, **Usage**, **Monitoring** tabs | `@add_tracing` alone. When Domino sets `DOMINO_AGENT_IS_PROD=true` and `DOMINO_APP_ID`, the SDK routes traces to the experiment `agent_experiment_<app id>` and **skips inline evaluators**; score production traces out of band ([EVALUATORS.md](./EVALUATORS.md)) |

Do not call `mlflow.set_experiment()` or wrap requests in `DominoAgentContext` / `DominoRun` inside a deployed agent; the SDK manages that experiment.

## What gets captured

- The decorated function's arguments (`span.inputs`, a dict by parameter name) and return value (`span.outputs`).
- Child spans: every autologged LLM call (model, messages, token usage, latency) and every manual `mlflow.start_span` / `@mlflow.trace` span, such as tool calls.
- Errors: an exception inside the function ends the span with the error and propagates.
- Evaluator results, stored as trace tags: numeric values as metrics, strings as labels.

The SDK does not compute cost; derive it from the LLM-span token counts.

## Core components

1. **`@add_tracing(name, autolog_frameworks=[], evaluator=None, trace_evaluator=None, eagerly_evaluate_streamed_results=True, span_type="UNKNOWN", attributes=None)`** from `domino.agents.tracing`: starts a span (a new trace, or a child span if a trace is active), records inputs and outputs, runs the evaluators. Place it directly on the function. [ADD-TRACING-DECORATOR.md](./ADD-TRACING-DECORATOR.md)
2. **Evaluators**: `evaluator(span)` gets the finished `mlflow.entities.Span`; `trace_evaluator(trace)` gets the whole `mlflow.entities.Trace` when this call started the trace. Both return `{name: number | str}`. [EVALUATORS.md](./EVALUATORS.md)
3. **`DominoAgentContext` / `DominoRun(experiment_name=None, run_id=None, agent_config_path=None, custom_summary_metrics=None)`** from `domino.agents.logging`: starts an MLflow run, logs the agent config YAML as parameters, and at exit logs `<statistic>_<metric>` aggregates (for example `mean_relevancy`) over the run's evaluated traces. No `run_name` parameter; the run id is `run.info.run_id`. [DOMINO-RUN.md](./DOMINO-RUN.md)
4. **Manual spans**: `mlflow.start_span(name=..., span_type=...)` or `@mlflow.trace(span_type=...)` for tool calls and non-framework LLM calls.
5. **Post-hoc scoring**: `search_traces(run_id=...)` and `search_agent_traces(agent_id=..., agent_version=...)` from `domino.agents.tracing`, `log_evaluation(trace_id, name, value)` from `domino.agents.logging`.

## Quick start: evaluation script

```python
import csv
from domino.agents.tracing import add_tracing
from domino.agents.logging import DominoAgentContext
from openai import OpenAI

client = OpenAI()   # OPENAI_API_KEY from a Domino environment variable

def judge(span):
    answer = span.outputs["answer"]
    return {"answer_length": len(answer), "non_empty": 1.0 if answer.strip() else 0.0}

@add_tracing(name="single_question_agent", span_type="AGENT", autolog_frameworks=["openai"], evaluator=judge)
def process_single_question(data_point: dict) -> dict:
    response = client.chat.completions.create(
        model="gpt-6.1-sol", messages=[{"role": "user", "content": data_point["question"]}])  # example model
    return {"answer": response.choices[0].message.content}

if __name__ == "__main__":
    with DominoAgentContext(agent_config_path="ai_system_config.yaml",
                            custom_summary_metrics=[("answer_length", "mean"), ("non_empty", "min")]) as run:
        with open("sample_questions.csv") as f:
            for row in csv.DictReader(f):
                process_single_question(row)        # one trace per row
        print(run.info.run_id)
```

Run it as a Domino Job to create a deployable agent version (the Job ties the run to the commit and config); from a Workspace only to gut-check.

## Quick start: deployed agent

```python
from fastapi import FastAPI
from domino.agents.tracing import add_tracing

app = FastAPI()

@add_tracing(name="chat_turn", span_type="AGENT", autolog_frameworks=["openai"])
async def chat_turn(message: str) -> dict:
    ...                                   # LLM and tool calls; see ADD-TRACING-DECORATOR.md
    return {"response": "..."}

@app.post("/chat")
async def chat(body: dict):
    return await chat_turn(body["message"])   # no DominoAgentContext, no set_experiment
```

## Framework support

`autolog_frameworks` accepts any `mlflow.<name>.autolog()` integration (`openai`, `anthropic`, `langchain`, `pydantic_ai`, `llama_index`, ...); the SDK calls each once, lazily. Anthropic autologging may miss some calls; add manual spans where needed.

## Viewing traces

- Evaluation: **Experiments** > the experiment > the run > **Traces** tab (span tree, inputs, outputs, scores). **Compare** two to four runs' aggregated metrics. Only Job-originated runs offer **Deploy Agent**.
- Deployed agent: the agent's details page > **Performance**, **Usage**, **Monitoring**.

## Reference files

- [TRACING-SETUP.md](./TRACING-SETUP.md): environment (DSE needs nothing; pins for other images), variables, troubleshooting
- [ADD-TRACING-DECORATOR.md](./ADD-TRACING-DECORATOR.md): decorator parameters, manual spans, tool-use agent pattern
- [DOMINO-RUN.md](./DOMINO-RUN.md): `DominoAgentContext` / `DominoRun`, config file, aggregated metrics
- [EVALUATORS.md](./EVALUATORS.md): span, trace, LLM-as-judge, post-hoc and production evaluators
- [MULTI-AGENT-EXAMPLE.md](./MULTI-AGENT-EXAMPLE.md): a deployed tool-use agent and a batch-evaluated multi-agent pipeline

To scaffold tracing into an existing project, use the `domino-trace-setup` skill. For the model client, use LLM Gateway 2.0 where deployed (`domino-llm-gateway`), else `domino-llm-access`; tracing works the same.

## Documentation

- Develop agentic systems: https://docs.domino.ai/cloud/platform-capabilities/features/agents/develop (6.3: replace `cloud` with `6.3`)
- Experiment Manager, deploy, monitor: `.../features/agents/experiment`, `.../agents/deploy`, `.../agents/monitor`
- SDK source: https://github.com/dominodatalab/python-domino/tree/Release-2.2.0/domino/agents
