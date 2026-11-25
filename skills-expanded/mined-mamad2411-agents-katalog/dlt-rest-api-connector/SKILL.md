---
name: dlt-rest-api-connector
description: >
  Build dlt REST API pipelines to ADLS Gen2 and OneLake. Use when configuring
  RESTAPIConfig, handling pagination, or setting schema contracts for REST
  sources. Also use when landing REST API data into Fabric lakehouses or
  debugging schema evolution.
tools: Read, Write, Edit, Glob, Grep, Bash
type: source
domain: dlt REST API ingestion
version: 1.0.0
---

# dlt REST API Connector — Practitioner Patterns

Hard-to-find patterns for building dlt REST API pipelines that land data in ADLS Gen2 and Microsoft Fabric lakehouses. Focuses on what Context7 and official docs don't cover well: pagination decision framework, schema contract gotchas, OneLake URL construction, and the `_dlt_load_id` bridge to downstream dbt models.

## Quick Reference

The patterns most likely to prevent mistakes:

### RESTAPIConfig structure

```python
from dlt.sources.rest_api import RESTAPIConfig

config: RESTAPIConfig = {
    "client": {
        "base_url": "https://api.example.com/v1/",
        "auth": {
            "type": "bearer",
            "token": dlt.secrets["api_token"],
        },
        "paginator": {
            "type": "json_link",
            "next_url_path": "paging.next",
        },
    },
    "resource_defaults": {
        "primary_key": "id",
        "write_disposition": "merge",
    },
    "resources": [
        "simple_endpoint",          # string shorthand — name = path = table
        {
            "name": "detailed_endpoint",
            "endpoint": {
                "path": "items",
                "params": {
                    "status": "active",
                },
                "data_selector": "data.items",  # extract from nested response
            },
        },
    ],
}
```

Key structural rules:
- `params` goes **inside** `endpoint`, not at the resource level (common mistake — resource-level `params` is silently ignored)
- `data_selector` uses dot notation for nested JSON (`"data.items"`, not `["data"]["items"]`)
- `resource_defaults` applies to all resources — override per-resource by repeating the key
- String resources use the string as path, name, AND table name simultaneously

### Pagination decision framework

| API behavior | Paginator type | Config key |
|---|---|---|
| Response body has a URL to the next page | `json_link` | `next_url_path` — dot-path to the URL field |
| Response headers have a `Link` header | `header_link` | (none — auto-detects `rel="next"`) |
| API uses `page=1, page=2, ...` | `page_number` | `page_param`, `total_path` or `maximum_page` |
| API uses cursor tokens | `cursor` | `cursor_path`, `cursor_param` |
| API uses `offset=0, offset=100, ...` | `offset` | `limit`, `offset`, `offset_param`, `limit_param` |

**Start with `auto`** — dlt detects pagination from standard patterns. Only configure explicitly when auto-detection fails (returns only the first page of results).

### Write disposition by use case

| Scenario | Disposition | Why |
|---|---|---|
| Append-only event stream (logs, events, webhooks) | `append` | No updates — each record is immutable |
| Entity with `updated_at` (customers, orders) | `merge` | Records change — deduplicate by `primary_key` |
| Reference/lookup data (countries, config) | `replace` | Small table, full refresh is simpler than tracking changes |
| First-time ingestion / backfill | `replace` then switch to `merge` | Avoid merge overhead on initial bulk load |

### Schema contracts — dev vs prod

| Setting | Behavior on new column | Behavior on type change | Use when |
|---|---|---|---|
| `evolve` | Column added automatically | Type widened | Dev, exploration, initial build |
| `freeze` | **Pipeline fails** | **Pipeline fails** | Prod — catches unexpected API changes before they corrupt data |
| `discard_value` | Column dropped, row loaded | Value nulled, row loaded | Prod — tolerant mode, logs discarded fields |
| `discard_row` | Entire row dropped | Entire row dropped | Prod — strict mode, quarantine bad records |

**Default pattern**: `evolve` in dev, `freeze` in prod. Set via `schema_contract`:

```python
source = rest_api_source(config)
source.schema_contract = {"tables": "evolve", "columns": "freeze", "data_type": "freeze"}
```

The three-level contract (`tables`, `columns`, `data_type`) lets you freeze column schema while still allowing new tables — useful when the API adds new endpoints but existing endpoint schemas should not drift.

### max_table_nesting=0 — preserving JSON in bronze

```python
@dlt.source(max_table_nesting=0)
def my_api_source():
    ...
```

**When to use**: Always in bronze. dlt's default normalizer explodes nested JSON into child tables (one per nested object/array). With `max_table_nesting=0`, nested structures are stored as JSON columns instead.

**Why this matters for Fabric**: JSON columns land as `VARCHAR` in Delta tables. dbt can then use `OPENJSON()` (T-SQL) to extract fields in the silver layer — keeping bronze as a faithful copy of the API response.

**Without it**: dlt creates tables like `orders__line_items`, `orders__line_items__taxes` — hard to reason about, hard to debug, and the child table names don't match the API structure.

### _dlt_load_id bridge to dbt

Every row dlt loads gets a `_dlt_load_id` column — a unique identifier for the load batch. This is the bridge between dlt (bronze) and dbt (silver):

```sql
-- dbt incremental model using _dlt_load_id instead of business timestamps
{% if is_incremental() %}
  where _dlt_load_id > (select max(_dlt_load_id) from {{ this }})
{% endif %}
```

**Why `_dlt_load_id` over `updated_at`**:
- `updated_at` reflects when the event happened — late-arriving data is missed
- `_dlt_load_id` reflects when dlt loaded the row — captures everything from the last load
- No lookback window needed — each load ID is unique and monotonically increasing
- Eliminates the need for deduplication logic on the incremental boundary

**Trade-off**: `_dlt_load_id` ties your dbt model to dlt's loading semantics. If you ever switch ingestion tools, you'll need to change the incremental predicate.

## Anti-patterns

What LLMs consistently get wrong with dlt REST API pipelines:

- **Assuming dlt transforms data** — dlt is EL only. All transformations happen in dbt. Don't ask dlt to rename columns, filter rows, or join datasets.
- **`params` at resource level** — `params` must be inside `endpoint: { params: {...} }`. Resource-level `params` is silently ignored, leading to unfiltered API calls.
- **Hallucinating dlt connectors** — Claude invents `dlt.sources.stripe()` or `dlt.sources.hubspot()`. Check verified sources at `dlt-hub/verified-sources` — many APIs require building a custom REST API config.
- **Display names in OneLake URLs** — OneLake paths require workspace and lakehouse GUIDs, not display names. `abfss://workspace-guid@onelake.dfs.fabric.microsoft.com/lakehouse-guid/Tables/` — not `my-workspace` or `my-lakehouse`.
- **Missing schema contracts in prod** — Running with `evolve` in production means an API schema change silently adds columns or widens types. Use `freeze` or `discard_value` to catch drift.
- **Skipping `max_table_nesting=0`** — Default nesting creates child tables that fragment the API response. Bronze should preserve the original JSON structure.
- **Using `merge` for event streams** — Events are immutable. `merge` adds unnecessary primary key matching overhead. Use `append`.
- **Confusing dlt (dlthub) with Databricks DLT** — Completely different tools. dlt is an open-source Python library; Delta Live Tables is a Databricks feature.

## Reference Files

For deeper guidance on specific patterns:

- **[references/rest-api-patterns.md](references/rest-api-patterns.md)** — RESTAPIConfig structure, pagination types with real examples, auth patterns, data_selector paths, incremental loading, resource dependencies, and response extraction.
- **[references/azure-destination.md](references/azure-destination.md)** — ADLS Gen2 filesystem destination, Delta format configuration, OneLake URL construction with GUIDs, secrets management, lakehouse landing patterns, and the medallion handoff to dbt.
- **[references/evaluations.md](references/evaluations.md)** — Evaluation scenarios testing skill effectiveness on REST API config, pagination choice, schema contracts, and ADLS destination setup.
