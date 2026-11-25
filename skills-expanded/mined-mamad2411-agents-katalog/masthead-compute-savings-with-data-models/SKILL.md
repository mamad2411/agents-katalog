---
name: masthead-compute-savings-with-data-models
description: Optimize BigQuery compute costs by assigning data models (Dataform, dbt, Airflow) to slot reservations or on-demand compute based on Masthead recommendations.
compatibility: Requires gcloud CLI, bq command-line tool. Must have read-only permissions to run BigQuery jobs, access data, and view reservations.
---

# Optimize Orchestration Compute (BigQuery Reservations)

## Purpose

Automatically assign data models from data orchestration to BigQuery slot reservations based on compute complexity and cost optimization strategy. Routes high-compute workloads to on-demand capacities while using reservations pricing for high-traffic jobs.

## When to Use

- Assigning new models/actions to appropriate compute tiers (reserved vs on-demand)
- Rebalancing reservation assignments based on priority changes
- Optimizing costs by moving low-priority workloads to on-demand
- Ensuring critical pipelines get guaranteed compute resources

## Implementation Steps

### Step 1: Source Configuration

Extract and apply recommendations from Masthead insights automatically.

1. Ask user for the BigQuery dataset where Masthead insights are stored. This dataset must contain an `insights` table with the same schema as `masthead-prod.YOUR_DATASET.insights`. If the user does not have access, direct them to [request access](https://docs.mastheadata.com/api#get-access-to-bigquery-resources).

   Once provided, **immediately persist it** by appending to the project-level agent instructions file (e.g. `.github/copilot-instructions.md`, or `AGENTS.md` — whichever already exists in the project root, or creating if none exist):

   ```
   <!-- masthead -->
   MASTHEAD_DATASET=YOUR_DATASET
   <!-- /masthead -->
   ```

   On subsequent runs, read this value from the instructions file instead of prompting the user again.

2. Identify which orchestration technology is in use by querying available recommendations:

```bash
bq query --project_id=YOUR_PROJECT --use_legacy_sql=false --format=csv \
"SELECT subtype, COUNT(*) AS recommendation_count
FROM \`masthead-prod.YOUR_DATASET.insights\`
WHERE category = 'Cost'
  AND type = 'Compute costs'
GROUP BY subtype"
```

If compute model recommendations are not present or all rows share the same technology, infer from the user's project structure (presence of `dbt_project.yml` → dbt, `definitions/` folder → Dataform, Airflow DAG files → Airflow). Confirm the detected tool with the user before proceeding.

3. Pull recommendations from `masthead-prod.YOUR_DATASET.insights`:

   Replace the `subtype` value with the one detected in step 2 (e.g. `'Re-assign reservation for Dataform models'`, `'Re-assign reservation for dbt models'`, or `'Re-assign reservation for Airflow DAGs'`).

```bash
bq query --project_id=YOUR_PROJECT --use_legacy_sql=false --format=csv \
"SELECT
  JSON_VALUE(m, '$.model_id') AS action_name,
  JSON_VALUE(op, '$.recommended_compute_model') AS recommended_model,
  -- CAST(JSON_VALUE(overview, '$.cost_30d') AS FLOAT64) AS cost_30d,
  last_updated_time
FROM \`masthead-prod.YOUR_DATASET.insights\`,
  UNNEST(JSON_QUERY_ARRAY(operations)) AS op,
  UNNEST(JSON_QUERY_ARRAY(op, '$.models')) AS m
WHERE category = 'Cost'
  AND type = 'Compute costs'
  AND subtype = 'Re-assign reservation for Dataform models'
--ORDER BY cost_30d DESC
" > compute_assignment_candidates.csv
```

5. Resolve reservation targets using `recommended_model` values and reservation edition metadata:

- Verify reservation editions using `INFORMATION_SCHEMA.RESERVATIONS`:

```bash
bq query --project_id=YOUR_PROJECT --location=US --use_legacy_sql=false --format=csv \
"SELECT
  reservation_name,
  project_id,
  edition,
  slot_capacity
FROM RESERVATION_ADMIN_PROJECT.\`region-us\`.INFORMATION_SCHEMA.RESERVATIONS
ORDER BY project_id, reservation_name"
```

- Map `recommended_model = 'ON-DEMAND'` to the config entry where `reservation = 'none'`.
- For all other values (for example `ENTERPRISE`), choose a reservation whose **edition** matches `recommended_model`.
- If exactly one matching reservation exists, assign automatically.
- If multiple matching reservations exist, ask the user which reservation tag to use.
- If no matching reservation exists, ask the user to pick a fallback reservation or create a new matching reservation first.
- Ensure an on-demand bucket exists. If missing, create one:

```javascript
{
  tag: 'on_demand',
  reservation: 'none',
  actions: []
}
```

6. Convert recommendations into assignment lists automatically:

```bash
bq query --project_id=YOUR_PROJECT --use_legacy_sql=false --format=csv \
"SELECT
  JSON_VALUE(m, '$.model_id') AS action_name,
  JSON_VALUE(op, '$.recommended_compute_model') AS recommended_model
FROM \`masthead-prod.YOUR_DATASET.insights\`,
  UNNEST(JSON_QUERY_ARRAY(operations)) AS op,
  UNNEST(JSON_QUERY_ARRAY(op, '$.models')) AS m
WHERE category = 'Cost'
  AND type = 'Compute costs'
  AND subtype = 'Re-assign reservation for Dataform models'
ORDER BY CAST(JSON_VALUE(overview, '$.cost_30d') AS FLOAT64) DESC" > compute_assignment_final.csv
```

7. Apply all recommendations based on the detected orchestration tool:

#### Dataform

- Open `definitions/_reservations.js`.
- The `action_name` values in the CSV map directly to Dataform action IDs (e.g. `project.dataset.table`) as used in the `actions` arrays of `_reservations.js`.
- Replace `on_demand` `actions` with all rows where `recommended_model = 'ON-DEMAND'`.
- Replace reserved reservation `actions` with all rows where `recommended_model != 'ON-DEMAND'`.
- Remove duplicates; keep only actions present in this repo's Dataform graph.
- Verify: `dataform compile` and check for duplicate assignments.
- See package reference: [`@masthead-data/dataform-package`](https://github.com/masthead-data/dataform-package)

#### dbt

- Follow the reservation assignment workflow from [`masthead-data/dbt-reservations`](https://github.com/masthead-data/dbt-reservations).
- Map recommendations to the appropriate dbt model tags or selector targets.
- Update the relevant `dbt_project.yml` or profile configuration per the repo's instructions.

#### Airflow

- Follow the reservation assignment workflow from [`masthead-data/airflow-reservations`](https://github.com/masthead-data/airflow-reservations).
- Map recommendations to DAG or task-level BigQuery reservation labels.
- Update the relevant operator configuration per the repo's instructions.

### Step 2: Verify Changes

After applying, confirm assignments are non-overlapping and align with the recommendation output. For Dataform:

```bash
# Check syntax
dataform compile

# Validate no duplicate assignments
grep -r "\.actions" definitions/_reservations.js
```

For dbt and Airflow, follow the verification steps in their respective repositories.

## Decision Criteria

| Factor           | Reserved Slots     | On-Demand             |
| ---------------- | ------------------ | --------------------- |
| **Priority**     | High, SLA-bound    | Low, flexible         |
| **Frequency**    | Regular, scheduled | Ad-hoc, occasional    |
| **Cost Pattern** | Predictable usage  | Variable, sporadic    |
| **Impact**       | Critical pipelines | Experimental, samples |

## Key Notes

- Each action should appear in only ONE reservation config
- File starts with `_` to ensure it runs first in Dataform queue
- Changes take effect on next Dataform workflow run
- Package automatically handles global assignment (no per-file edits needed)
- Default mode is full auto-apply of recommendations; rely on PR review for validation
- The only interactive checkpoint is reservation selection when more than one reservation matches the recommended edition

## Package References

- **Dataform**: [`@masthead-data/dataform-package`](https://github.com/masthead-data/dataform-package)
- **dbt**: [`masthead-data/dbt-reservations`](https://github.com/masthead-data/dbt-reservations)
- **Airflow**: [`masthead-data/airflow-reservations`](https://github.com/masthead-data/airflow-reservations)
