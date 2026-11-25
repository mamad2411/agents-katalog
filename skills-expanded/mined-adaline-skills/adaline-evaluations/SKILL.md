---
name: adaline-evaluations
description: "Run and manage evaluations in Adaline to test prompt quality at scale. Use when creating evaluation runs, polling status, analyzing results, or cancelling runs."
---

# Adaline Evaluations

## Concepts

Evaluations run a prompt against a dataset and score each row with one evaluator. They are asynchronous: create a run, poll its status, then read paginated results.

Key terms:
- **Evaluation** — one run, identified by `runId`
- **Evaluator** — the scoring configuration, identified by `evaluatorId`
- **Dataset** — rows that provide prompt inputs and optional expected values
- **Grade** — `pass`, `fail`, or `unknown`
- **Metrics** — aggregate pass/fail/unknown counts, cost, latency, and token count

## Status Lifecycle

```
queued -> running -> completed
                  -> failed
                  -> cancelling -> cancelled
```

## Configuration

Set these environment variables when credentials are available:
- `ADALINE_API_KEY` — workspace API key from Admin > API Keys
- `ADALINE_PROMPT_ID` — prompt to evaluate
- `ADALINE_EVALUATOR_ID` — evaluator to run
- `ADALINE_DATASET_ID` — optional dataset override

Base URL: `https://api.adaline.ai/v2`

## Quick Triage

| Symptom | First Fix |
|---|---|
| Create body rejected | Use singular `evaluatorId`, not the old plural evaluator field |
| Follow-up GET returns 404 | Use response `runId` as the `{evaluationId}` path parameter |
| Results missing row data | Add `expand=row` on the results endpoint |
| Pagination skips results | Use `pagination.nextCursor`, not page numbers |
| Python example returns coroutine | Await SDK methods inside an asyncio event loop |

## Running an Evaluation

### Step 1 — Create run

```bash
curl -X POST "https://api.adaline.ai/v2/prompts/$ADALINE_PROMPT_ID/evaluations" \
  -H "Authorization: Bearer $ADALINE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "evaluatorId": "evaluator_abc123",
    "datasetId": "dataset_abc123"
  }'
```

The response returns `runId`. Use that value as `evaluationId` in status/results/cancel calls.

### Step 2 — Poll status

```bash
curl "https://api.adaline.ai/v2/prompts/$ADALINE_PROMPT_ID/evaluations/$RUN_ID" \
  -H "Authorization: Bearer $ADALINE_API_KEY"
```

### Step 3 — Fetch results

```bash
curl "https://api.adaline.ai/v2/prompts/$ADALINE_PROMPT_ID/evaluations/$RUN_ID/results?grade=fail&expand=row&limit=50" \
  -H "Authorization: Bearer $ADALINE_API_KEY"
```

### Step 4 — Cancel if needed

```bash
curl -X POST "https://api.adaline.ai/v2/prompts/$ADALINE_PROMPT_ID/evaluations/$RUN_ID/cancel" \
  -H "Authorization: Bearer $ADALINE_API_KEY"
```

## SDK Usage

```typescript
const run = await adaline.prompts.evaluations.create({
  promptId,
  evaluation: { evaluatorId, datasetId },
});

const status = await adaline.prompts.evaluations.get({
  promptId,
  evaluationId: run.runId,
});

const results = await adaline.prompts.evaluations.results.list({
  promptId,
  evaluationId: run.runId,
  grade: 'fail',
  expand: 'row',
});
```

```python
run = await adaline.prompts.evaluations.create(
    prompt_id=prompt_id,
    evaluation=CreateEvaluationRequest(evaluator_id=evaluator_id, dataset_id=dataset_id),
)

status = await adaline.prompts.evaluations.get(
    prompt_id=prompt_id,
    evaluation_id=run.run_id,
)

results = await adaline.prompts.evaluations.results.list(
    prompt_id=prompt_id,
    evaluation_id=run.run_id,
    grade="fail",
    expand="row",
)
```

## Best Practices

1. Use one evaluator per run; create multiple runs when you need multiple evaluators.
2. Persist `runId` in CI or job metadata so later steps can poll and fetch results.
3. Poll status with backoff; do not tight-loop.
4. Gate deploy/promotion on terminal status and acceptable metrics.
5. Inspect failing rows with `grade=fail&expand=row`.

## References

See references/api.md for request/response schemas and curl examples.
