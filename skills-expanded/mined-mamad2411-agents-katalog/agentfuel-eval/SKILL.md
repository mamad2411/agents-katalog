---
name: agentfuel-eval
description: Evaluates LLM-based data analysis agents on their ability to execute domain-specific time-series queries, particularly focusing on stateful logic, temporal dependencies, and incident pattern detection. It probes whether agents can correctly interpret schemas, track state across sequential events, and identify anomalous behavior without relying on predefined time windows. Use when the user wants to benchmark on AgentFuel Benchmark, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2603.12483
  bibtex_key: maddi2026agentfuel
  confidence: high
---

# agentfuel-eval

> Generating Expressive and Customizable Evals for Timeseries Data Analysis Agents with AgentFuel — Maddi et al. (2026) (arXiv:2603.12483, 2026)

## What this evaluates

Evaluates LLM-based data analysis agents on their ability to execute domain-specific time-series queries, particularly focusing on stateful logic, temporal dependencies, and incident pattern detection. It probes whether agents can correctly interpret schemas, track state across sequential events, and identify anomalous behavior without relying on predefined time windows.

## Datasets

- **AgentFuel Benchmark** — total 79500; splits: e-commerce (6000), iot (50000), telecom (23500)

## Metrics

- `accuracy` **(primary)** — range: [0, 1]
  - Proportion of queries where the agent's response (natural language, table, or chart) contains or allows derivation of the expected answer. Responses are manually classified as correct, incorrect, or runtime error.
- `pass@2` — range: [0, 1]
  - Probability that an agent produces at least one correct answer across two independent trials for the same query.
- `self-consistency` — range: [0, 1]
  - Ratio of the count of the majority response category (correct/incorrect/error) to the total number of trials for a given query.

## Input / output format

**Input**: Dataset schema, data previews, and natural language queries (stateless, stateful, or incident-specific) provided in a one-shot setting.

**Output**: Natural language responses, tables, charts, or code artifacts.

## Scoring recipe

```python
# Manual classification per trial
labels = []
for trial in trials:
    if expected_in_response(response) or expected_derivable_from_artifact(response):
        labels.append("correct")
    else:
        labels.append("incorrect") # includes runtime errors
accuracy = labels.count("correct") / len(labels)
pass_at_2 = 1 if labels[:2].count("correct") > 0 else 0
self_consistency = max(labels.count(c) for c in ["correct", "incorrect"]) / len(labels)
```

## Common pitfalls

- Agents frequently fail on stateful queries by not tracking state across events (e.g., failing to update view counts while a cart is full).
- For incident-specific queries, agents assume fixed or global time windows instead of detecting anomalies by comparing entities against their own historical behavior.
- Schema confusion causes agents to select wrong tables or infer incorrect time intervals, leading to false column-not-found errors.

## Evidence (verbatim from paper)

> We report three metrics: accuracy, pass@2, and self-consistency. An agent response is accurate if its natural language response contains the expected answer, or if the expected answer can be derived from the artifacts. An agent response is considered inaccurate if it returns an incorrect answer or raises an error. Self-consistency is computed as the ratio of the majority category label count to the number of trials.

## Citation

```bibtex
@misc{maddi2026agentfuel,
  title={Generating Expressive and Customizable Evals for Timeseries Data Analysis Agents with AgentFuel},
  author={Maddi et al. (2026)},
  year={2026},
  note={arXiv:2603.12483}
}
```

- arXiv: 2603.12483
