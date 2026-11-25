---
name: domino-trace-setup
description: Set up GenAI tracing for an LLM or agent application in Domino by checking the Domino SDK and MLflow requirements (the DSE needs nothing installed), then adding a tracing_setup.py helper, span evaluators, a config.yaml, and @add_tracing / DominoAgentContext wiring. Use when the user asks to add tracing, observability, or evaluation to an agent or LLM app running on Domino.
compatibility: Domino 6.3 and Domino Cloud (agents SDK needs Domino 6.2+ and MLflow 3.2+; the DSE ships MLflow 3.3.2). Runs inside a Domino Workspace or Job, where MLFLOW_TRACKING_URI and DOMINO_API_HOST are set.
---

# Set Up Domino GenAI Tracing

Applies to Domino 6.3 and Domino Cloud.

Instrument an agent or LLM application so its calls, spans, and evaluator scores show up in
Domino's Experiment Manager. For traditional ML tracking, use the `domino-experiment-setup`
skill instead. For evaluator patterns, multi-agent examples and the full context-manager
reference, use the `domino-genai-tracing` skill.

## Inputs

1. **LLM framework**: `openai` (default), `anthropic`, or `langchain`. Detect from the code if possible.
2. **Agent name**: name for the traced entry-point function (letters, digits, `_` and `-` only).
3. **Evaluator**: whether to add quality scoring, and whether to use an LLM-as-judge.
4. **Aggregated metrics**: which evaluator metrics to summarize per run, and with which statistic.

Model access is not an input. Tracing instruments whichever client the agent already uses (a
provider SDK, a Domino-hosted endpoint, or LLM Gateway 2.0 where it is installed: `domino-llm-access`,
`domino-llm-gateway`); do not change it. Pass that client to `create_llm_judge_evaluator(client=...)`
so the judge shares it; through the gateway, model names are aliases.

## Steps

1. **Check requirements.** In the Domino Standard Environment install nothing: it ships the
   agents code (`dominodatalab` 2.2.0) and MLflow 3.3.2; one harmless
   `Failed to end span ... '_metrics'` warning per trace is expected. Do not add the `agents`
   extra there (it downgrades MLflow sub-packages to 3.2.0). Needs `dominodatalab` 2.1.0+ and
   MLflow 3.2+:

   ```bash
   python -c "import importlib.metadata as m; print({p: m.version(p) for p in ('dominodatalab', 'mlflow', 'opentelemetry-sdk')})"
   ```

   Outside the DSE, add to the Dockerfile instructions (or `requirements.txt`), at or below the
   DSE versions:

   ```dockerfile
   RUN pip install "dominodatalab[data]==2.2.0" mlflow==3.3.2 "opentelemetry-sdk<=1.44.0" "opentelemetry-api<=1.44.0"
   ```

2. **Copy helpers** from this skill's `assets/` folder next to the agent's entry point:
   - `assets/tracing_setup.py`: `setup_tracing(framework)`, `create_evaluator()`,
     `create_llm_judge_evaluator()`, `get_aggregation_metrics()`, plus `input_text()` and
     `output_text()` for reading a span.
   - `assets/config.yaml`: agent configuration logged as run parameters through
     `agent_config_path`. Replace the model names with the ones the user actually calls; keep
     `models.judge` equal to the judge model the evaluator uses.
3. **Instrument the agent.** Decorate the entry point with `@add_tracing` and run the evaluation
   loop inside `DominoAgentContext`, as below. Keep the user's existing logic unchanged.
4. **Explain how to view traces** (see "Viewing traces").

## Example traced agent

```python
import mlflow
from domino.agents.tracing import add_tracing
from domino.agents.logging import DominoAgentContext
from openai import OpenAI

mlflow.openai.autolog()
client = OpenAI()     # the agent's existing client; a gateway or Domino-hosted-endpoint client traces the same way

def quality_evaluator(span):
    """Span evaluator: span.inputs is a dict of the call's arguments, span.outputs its return value."""
    output = span.outputs or {}
    scores = {"response_length": len(output.get("response", ""))}
    if isinstance(output.get("confidence"), (int, float)):   # report it only when the agent set it
        scores["confidence"] = float(output["confidence"])
    return scores

@add_tracing(name="my_agent", span_type="AGENT", evaluator=quality_evaluator)
def my_agent(query: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-6.1-sol",          # example model name; use one your provider serves
        messages=[{"role": "user", "content": query}],
    )
    return {"response": response.choices[0].message.content, "confidence": 0.9, "model": "gpt-6.1-sol"}

if __name__ == "__main__":
    aggregated_metrics = [("response_length", "mean"), ("confidence", "mean"), ("confidence", "min")]
    mlflow.set_experiment("my-agent-eval")        # creates the experiment if it does not exist

    with DominoAgentContext(
        agent_config_path="config.yaml",
        custom_summary_metrics=aggregated_metrics,
    ) as run:                                      # run is the mlflow ActiveRun
        for query in ["What is machine learning?", "Explain neural networks"]:
            result = my_agent(query)
            print(f"Q: {query}\nA: {result['response'][:100]}...\n")
        print(f"Run ID: {run.info.run_id}")
```

Two facts the example depends on; the rest of the SDK reference is in the `domino-genai-tracing` skill ([ADD-TRACING-DECORATOR.md](../domino-genai-tracing/ADD-TRACING-DECORATOR.md), [DOMINO-RUN.md](../domino-genai-tracing/DOMINO-RUN.md), [EVALUATORS.md](../domino-genai-tracing/EVALUATORS.md)):

- An evaluator that raises records nothing (the SDK logs the error), so never return a made-up default score, and omit a metric whose input is missing. Results are tags on the shared trace, so give each decorated function's metrics distinct names.
- `DominoAgentContext` takes `experiment_name`, `run_id`, `agent_config_path` and `custom_summary_metrics` only (no `run_name`); `experiment_name` must already exist, so call `mlflow.set_experiment(name)` first and omit it. At exit it logs one `<statistic>_<metric>` run metric per `custom_summary_metrics` pair.

## Framework autologging

| Framework | Setup |
|---|---|
| OpenAI | `mlflow.openai.autolog()` then `OpenAI()` |
| Anthropic | `mlflow.anthropic.autolog()` then `Anthropic()` (may need manual spans for some calls) |
| LangChain | `mlflow.langchain.autolog()` then e.g. `ChatOpenAI(model="gpt-6.1-sol")` |

`@add_tracing(autolog_frameworks=["openai"])` does the same lazily on the first traced call.

## Viewing traces

1. Go to **Experiments** in the Domino project.
2. Open the experiment the run logged to and select the run (an agent version).
3. Open the **Traces** tab: one trace per call of the decorated function, with the span tree
   (agent, tools, LLM calls), token usage, latency and evaluator scores. Aggregated metrics are
   on the run.

Run the evaluation script as a Domino Job rather than from the Workspace when the run should be
deployable as an agent: only Job-originated runs keep the code commit and config lineage.

Docs: https://docs.domino.ai/cloud/platform-capabilities/features/agents/develop (6.3: replace `cloud` with `6.3`).
