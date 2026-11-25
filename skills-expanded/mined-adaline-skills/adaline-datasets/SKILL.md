---
name: adaline-datasets
description: "Create and manage evaluation datasets in Adaline. Use when building test cases, adding dataset columns/rows, importing data, or triggering dynamic columns."
---

# Adaline Datasets

## Concepts

Datasets are structured test cases for evaluations. Rows supply prompt inputs and optional expected values. Columns define the cell modality or dynamic generation source.

Key terms:
- **Dataset** — table of evaluation cases in a project
- **Column** — named field; types are `static`, `prompt`, or `api`
- **Row** — one test case; values are keyed by column ID or column name
- **Dynamic column** — `prompt` or `api` column whose values are generated on demand

## Configuration

Set these environment variables when credentials are available:
- `ADALINE_API_KEY` — workspace API key from Admin > API Keys
- `ADALINE_PROJECT_ID` — project ID

Base URL: `https://api.adaline.ai/v2`

## Key Rule: Use Current Batch Shapes

Column creation takes `{ "columns": [...] }`. Row creation takes `{ "rows": [...] }`. Do not send a single bare column object to `/columns`.

## Quick Triage

| Symptom | First Fix |
|---|---|
| Column add fails | Wrap columns in `{ "columns": [...] }` |
| Row values not applied | Use `valuesBy=columnName` when keys are names |
| Dynamic fetch ignored rows | Use `datasetRowIds`; the shorter legacy row-id key is not accepted |
| Pagination missing rows | Use `pagination.nextCursor` |
| Python snippets return coroutine | Await SDK methods |

## Creating a Dataset

```bash
curl -X POST "https://api.adaline.ai/v2/datasets" \
  -H "Authorization: Bearer $ADALINE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "projectId": "project_abc123",
    "title": "Support eval set",
    "icon": { "type": "emoji", "value": "📚" },
    "description": "Support questions and expected answers"
  }'
```

## Adding Columns

```bash
curl -X POST "https://api.adaline.ai/v2/datasets/dataset_abc123/columns" \
  -H "Authorization: Bearer $ADALINE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "columns": [
      { "name": "question", "type": "static" },
      { "name": "expected_answer", "type": "static" },
      {
        "name": "draft_answer",
        "type": "prompt",
        "settings": { "promptId": "prompt_abc123" }
      }
    ]
  }'
```

API dynamic column:

```json
{
  "name": "retrieved_context",
  "type": "api",
  "settings": {
    "method": "POST",
    "url": "https://example.com/retrieve",
    "headers": { "Authorization": "Bearer token" },
    "bodyTemplate": "{ \"query\": \"{{question}}\" }"
  }
}
```

## Adding Rows

```bash
curl -X POST "https://api.adaline.ai/v2/datasets/dataset_abc123/rows?valuesBy=columnName" \
  -H "Authorization: Bearer $ADALINE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "rows": [
      {
        "values": {
          "question": { "value": "How do I reset my password?" },
          "expected_answer": { "value": "Send the reset link." }
        }
      }
    ]
  }'
```

## Dynamic Columns

```bash
curl -X POST "https://api.adaline.ai/v2/datasets/dataset_abc123/dynamic-columns/fetch" \
  -H "Authorization: Bearer $ADALINE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "columnIds": ["column_abc123"],
    "datasetRowIds": ["row_abc123"],
    "runMode": "all"
  }'
```

`runMode` can be `all`, `failed`, or `first`.

## SDK Usage

```typescript
await adaline.datasets.list({ projectId, limit: 20 });
await adaline.datasets.create({ dataset });
await adaline.datasets.columns.create({ datasetId, columns });
await adaline.datasets.rows.create({ datasetId, valuesBy: 'columnName', rows });
await adaline.datasets.columns.fetchDynamic({ datasetId, query });
```

```python
await adaline.datasets.list(project_id=project_id, limit=20)
await adaline.datasets.create(dataset=dataset)
await adaline.datasets.columns.create(dataset_id=dataset_id, columns=columns)
await adaline.datasets.rows.create(dataset_id=dataset_id, values_by="columnName", rows=rows)
await adaline.datasets.columns.fetch_dynamic(dataset_id=dataset_id, query=query)
```

## Best Practices

1. Prefer `valuesBy=columnName` for authoring fixtures; use column IDs for immutable machine integrations.
2. Batch rows and columns when possible.
3. Add static input columns first, then rows, then dynamic columns.
4. Use `datasetRowIds` to rerun dynamic generation for a focused subset.
5. Keep dataset column names aligned with prompt variables where rows feed prompt evaluations.

## References

See references/api.md for the full REST contract.
