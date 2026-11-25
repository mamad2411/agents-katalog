---
name: adaline-evaluators
description: "Create and manage evaluators in Adaline to score prompt outputs. Use when setting up LLM-as-a-judge, JavaScript, text-matcher, cost, latency, or response-length evaluators."
---

# Adaline Evaluators

## Concepts

Evaluators define how Adaline scores prompt outputs. Each evaluator is attached to a prompt and dataset. Evaluation runs use an evaluator to produce per-row grades, scores, reasons, and aggregate metrics.

Key terms:
- **Evaluator** — configured scoring rule attached to a prompt
- **Dataset** — rows used by the evaluator when creating evaluation runs
- **Config** — discriminated object by `type`
- **Status** — `active` or `archived`

## Configuration

Set these environment variables when credentials are available:
- `ADALINE_API_KEY` — workspace API key from Admin > API Keys
- `ADALINE_PROJECT_ID` — project ID
- `ADALINE_PROMPT_ID` — prompt to attach evaluators to
- `ADALINE_DATASET_ID` — dataset for evaluator runs

Base URL: `https://api.adaline.ai/v2`

## Evaluator Types

### LLM-as-a-Judge

```json
{
  "type": "llm-as-a-judge",
  "value": "Pass only if the response answers the question and all factual claims are grounded in the reference answer."
}
```

### JavaScript

```json
{
  "type": "javascript",
  "value": "const parsed = JSON.parse(output); return parsed.answer ? 'pass' : 'fail';"
}
```

### Text Matcher

```json
{
  "type": "text-matcher",
  "value": {
    "operator": "contains-all",
    "value": ["Summary", "Recommendation"]
  }
}
```

Operators: `regex`, `equals`, `starts-with`, `ends-with`, `contains-all`, `contains-any`, `not-contains-any`.

### Cost, Latency, Response Length

These evaluator types use a comparison rule directly as `value`:

```json
{
  "type": "latency",
  "value": {
    "value": 2000,
    "unit": "ms",
    "operator": "less"
  }
}
```

Operators: `less`, `greater`, `equals`.

## Quick Triage

| Symptom | Fix |
|---|---|
| API rejects `group` | Remove it; current config is discriminated by `type` only |
| Text matcher rejected | Use `value.operator` and `value.value`, not `pattern` / `patterns` |
| Cost/latency rejected | Use comparison rule directly as `config.value`, not nested under `threshold` |
| List response lacks config | List returns lightweight summaries; call GET evaluator for full config |
| Evaluation needs multiple evaluators | Create one evaluation run per `evaluatorId` |

## Creating an Evaluator

```bash
curl -X POST "https://api.adaline.ai/v2/prompts/$ADALINE_PROMPT_ID/evaluators" \
  -H "Authorization: Bearer $ADALINE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "projectId": "project_abc123",
    "title": "Factual accuracy",
    "datasetId": "dataset_abc123",
    "config": {
      "type": "llm-as-a-judge",
      "value": "Pass only if the answer is accurate and cites the provided context."
    }
  }'
```

## SDK Usage

```typescript
await adaline.prompts.evaluators.list({ promptId, limit: 20 });
await adaline.prompts.evaluators.create({ promptId, evaluator });
await adaline.prompts.evaluators.get({ promptId, evaluatorId });
await adaline.prompts.evaluators.update({ promptId, evaluatorId, evaluator: { title: 'Updated' } });
await adaline.prompts.evaluators.delete({ promptId, evaluatorId });
```

```python
await adaline.prompts.evaluators.list(prompt_id=prompt_id, limit=20)
await adaline.prompts.evaluators.create(prompt_id=prompt_id, evaluator=evaluator)
await adaline.prompts.evaluators.get(prompt_id=prompt_id, evaluator_id=evaluator_id)
await adaline.prompts.evaluators.update(prompt_id=prompt_id, evaluator_id=evaluator_id, evaluator=patch)
await adaline.prompts.evaluators.delete(prompt_id=prompt_id, evaluator_id=evaluator_id)
```

## Best Practices

1. Use LLM-as-a-judge for qualitative criteria and write explicit pass/fail rubrics.
2. Use JavaScript/Text Matcher for deterministic structural checks.
3. Use cost/latency/response-length evaluators for performance budgets.
4. Keep evaluator titles descriptive because list responses are lightweight.
5. Attach evaluators to stable datasets so runs are comparable over time.

## References

See references/api.md for the full REST contract with all config shapes.
