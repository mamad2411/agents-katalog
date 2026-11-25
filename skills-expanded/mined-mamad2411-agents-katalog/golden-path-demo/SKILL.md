---
name: golden-path-demo
description: "Generate a customer-specific Golden Path to Enterprise AI demo. Creates tables, synthetic data, Genify metadata, metric views, and two Genie Spaces (before/after comparison) — all customized for a customer's industry and data domain. Outputs a Google Doc demo walkthrough with links to all assets. Supports gaming, retail, media, telecom, healthcare, financial, and custom verticals."
user-invocable: true
model: sonnet
---

# Golden Path Demo Generator

Generates a complete, customer-specific Golden Path to Enterprise AI demo. Asks a few questions, then builds everything: schemas, tables, synthetic data, Genify metadata comments, metric views, two Genie Spaces (before/after comparison), and a Google Doc demo walkthrough.

**Pre-built verticals** are available in `resources/verticals/` with ready-to-run SQL, Python notebooks, and demo scripts for gaming, retail, RMG, and indie gaming. Custom verticals are generated on-the-fly for any industry.

**Leverages existing skills:**
- `/databricks-data-generation` — for synthetic data (dbldatagen patterns)
- `/databricks-query` — for SQL execution via warehouse
- `/google-docs` — for demo walkthrough document generation
- `/databricks-authentication` — for workspace auth

**Announce at start:** "Let's build your Golden Path demo. I need a few inputs, then I'll generate everything."

---

## Configuration

All workspace-specific values are parameterized. Resolve them dynamically at runtime — do NOT hardcode.

| Variable | How to resolve | Fallback |
|----------|---------------|----------|
| `${DATABRICKS_PROFILE}` | Check `~/.databrickscfg` for available profiles. Ask user which profile to use if multiple exist. | `DEFAULT` |
| `${WAREHOUSE_ID}` | Run `databricks warehouses list --profile ${DATABRICKS_PROFILE} --output json` and let user pick, or use warehouse from `/databricks-warehouse-selector` | _(must resolve — no fallback)_ |
| `${CATALOG}` | Ask user or detect from `databricks catalogs list --profile ${DATABRICKS_PROFILE}` | _(must resolve — no fallback)_ |
| `${WORKSPACE_URL}` | Extract from `~/.databrickscfg` profile `host` value | _(must resolve — no fallback)_ |
| `${SFDC_TARGET_ORG}` | Run `sf org list --json` and pick the default or ask user | _(optional — skip SFDC if unavailable)_ |

**Override via `~/.vibe/profile.yaml`** (if present):
```yaml
golden-path-demo:
  databricks_profile: fe-vm-cmegdemos
  warehouse_id: 9cd919d96b11bf1c
  catalog: cmegdemos_catalog
  sfdc_target_org: user@databricks.com
```

If `~/.vibe/profile.yaml` contains a `golden-path-demo` section, use those values without prompting.

---

## Step 0 — Authenticate

Run these checks in parallel. Do NOT block on SFDC — it's optional context.

**A. Databricks CLI** — verify profile exists:
```bash
databricks workspace list /Workspace/Shared/ --profile ${DATABRICKS_PROFILE} 2>&1 | head -3
```
If this fails, the user needs the profile in `~/.databrickscfg`. Tell them to run `/databricks-authentication`.

**B. Google** — warm auth for the doc at the end:
```bash
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py token 2>/dev/null | head -1
```
If empty, tell user to run `/google-auth`.

**C. Salesforce** (optional) — check for UCO context:
```bash
sf org display 2>&1 | grep -i "connected"
```
If not connected, skip SFDC lookup — proceed with user-provided context only.

---

## Step 1 — Gather Inputs

Ask the user ONE question block. Use the AskUserQuestion tool with these questions:

**Question 1:** "Which customer is this demo for?"
- Options: let them type (Other)

**Question 2:** "Which industry template?"
- Options: Gaming, Retail, Media, Healthcare, Financial, Telecom, Custom

**Question 3:** "What's the 'money question' — the simple metric everyone answers differently?"
- Show defaults per industry (see below) — let them pick or customize

### Industry Defaults

| Industry | Tables | Money Question | Poison Data |
|----------|--------|---------------|-------------|
| Gaming | players, player_sessions, transactions, match_history | "How many active players do we have?" | internal + bot accounts inflate counts |
| Media & Entertainment | subscribers, streams, content, engagement | "How many active subscribers watched this week?" | trial + comp accounts inflate MAU |
| Retail & E-Commerce | customers, orders, products, order_items | "What's our return rate?" | employee + internal orders skew metrics |
| Telecom | subscribers, usage, tickets, plans | "What's our churn rate?" | internal + test accounts skew base |
| Financial Services | accounts, transactions, risk_scores, loans | "What's our default rate?" | internal test accounts inflate base |
| Healthcare & Life Sci | patients, encounters, providers, claims | "What's our average length of stay?" | observation encounters skew LOS |

### Derive variables:
- `CUSTOMER` — customer name (e.g., "Comcast")
- `INDUSTRY` — selected template
- `SCHEMA_PREFIX` — lowercase sanitized customer name: `echo "CUSTOMER" | tr '[:upper:]' '[:lower:]' | tr -cd 'a-z0-9_'` (e.g., `comcast`)
- `MONEY_QUESTION` — selected or default
- `TABLES` — 4 table names from industry template
- `POISON_DATA` — the "gotcha" data pattern (internal accounts, bot accounts, etc.)

### Optional SFDC lookup (if authenticated):
```bash
sf data query --query "SELECT Name, Stages__c FROM UseCase__c WHERE Account__r.Name LIKE '%CUSTOMER%' AND Stages__c IN ('U3','U4','U5','U6') ORDER BY Stages__c" --target-org ${SFDC_TARGET_ORG} 2>&1 | grep -v "Warning"
```
If UCOs found, include them in the demo doc. If not, skip — don't block.

### Confirm before proceeding:
```
Golden Path demo for [CUSTOMER] ([INDUSTRY]):

  Workspace profile: [${DATABRICKS_PROFILE}]
  Catalog: [${CATALOG}]
  Schema prefix: [SCHEMA_PREFIX]
  Tables: [table1, table2, table3, table4]
  Money question: "[MONEY_QUESTION]"
  Poison data: [POISON_DATA]
  Total rows: ~[N]K across 4 tables

Type "go" to generate or adjust anything.
```

Wait for user confirmation.

---

## Step 2 — Create Schemas

Create both schemas via SQL API:
```bash
# Run both in parallel
databricks api post /api/2.0/sql/statements --profile ${DATABRICKS_PROFILE} --json '{
  "warehouse_id": "${WAREHOUSE_ID}",
  "statement": "CREATE SCHEMA IF NOT EXISTS ${CATALOG}.{SCHEMA_PREFIX}_raw",
  "wait_timeout": "30s"
}'

databricks api post /api/2.0/sql/statements --profile ${DATABRICKS_PROFILE} --json '{
  "warehouse_id": "${WAREHOUSE_ID}",
  "statement": "CREATE SCHEMA IF NOT EXISTS ${CATALOG}.{SCHEMA_PREFIX}_enriched",
  "wait_timeout": "30s"
}'
```

**Error handling:** If either returns an error (permission denied, catalog not found), stop and tell the user which catalog/profile to fix.

---

## Step 3 — Generate Data

Write a dbldatagen notebook to `/tmp/golden-path-demo/{SCHEMA_PREFIX}_generate_data.py`.

### dbldatagen patterns (MUST follow):
- `expr="uuid()"` for ID columns
- `expr="concat('Name_', cast(id as string))"` for display names — `id` is the ONLY column you can reference in `expr`
- `values=[...]` with `weights=[...]` for ALL categorical columns (do NOT use `expr` to reference other columns)
- `begin="2025-12-01"` and `end="2026-03-05"` for date ranges (last 90 days)
- `minValue=...` and `maxValue=...` for numeric columns
- **NEVER** use `template` with `baseValue` — it does not exist in dbldatagen
- **NEVER** reference other column names in `expr` — only `id` and Spark SQL functions work in `expr`
- Notebook cells separated by `# COMMAND ----------`

### Critical data design rules:
Each industry template MUST include "poison" dimension values that inflate metrics when not filtered:
- **Gaming:** `account_type` with values `["standard", "premium", "trial", "internal", "bot"]` — internal + bot must be excluded
- **Retail:** `customer_type` with values `["retail", "wholesale", "employee", "internal", "test"]` — employee + internal must be excluded
- **Media:** `account_type` with values `["paid", "trial", "comp", "internal", "test"]` — trial + comp + internal must be excluded
- **Healthcare:** `encounter_type` with values `["inpatient", "outpatient", "observation", "er", "telehealth"]` — observation must be excluded from LOS
- **Financial:** `account_type` with values `["retail", "commercial", "internal", "test"]` — internal + test must be excluded
- **Telecom:** `account_type` with values `["residential", "business", "internal", "test"]` — internal + test must be excluded

This is what makes the BEFORE/AFTER comparison work — without the filter, Genie includes garbage data.

### Upload and run:
```bash
databricks workspace import --file /tmp/golden-path-demo/{SCHEMA_PREFIX}_generate_data.py \
  --format SOURCE --language PYTHON --overwrite \
  /Workspace/Shared/golden-path-demo/{SCHEMA_PREFIX}_generate_data --profile ${DATABRICKS_PROFILE}

# Create and trigger job
JOB_ID=$(databricks api post /api/2.1/jobs/create --profile ${DATABRICKS_PROFILE} --json '{
  "name": "Golden Path - {CUSTOMER} Data Gen",
  "tasks": [{"task_key": "gen", "notebook_task": {"notebook_path": "/Workspace/Shared/golden-path-demo/{SCHEMA_PREFIX}_generate_data", "source": "WORKSPACE"}, "environment_key": "default"}],
  "environments": [{"environment_key": "default", "spec": {"client": "2", "dependencies": ["dbldatagen"]}}]
}' 2>&1 | python3 -c "import sys,json; print(json.load(sys.stdin).get('job_id'))")

RUN_ID=$(databricks api post /api/2.1/jobs/run-now --profile ${DATABRICKS_PROFILE} --json "{\"job_id\": $JOB_ID}" 2>&1 | python3 -c "import sys,json; print(json.load(sys.stdin).get('run_id'))")
```

### Poll for completion:
```bash
for i in $(seq 1 30); do
  sleep 15
  STATE=$(databricks api get /api/2.1/jobs/runs/get --profile ${DATABRICKS_PROFILE} --json "{\"run_id\": $RUN_ID}" 2>&1 | python3 -c "import sys,json; s=json.load(sys.stdin).get('state',{}); print(f\"{s.get('life_cycle_state')}|{s.get('result_state','pending')}\")")
  echo "  [$i] $STATE"
  if echo "$STATE" | grep -q "TERMINATED"; then break; fi
done
```

**Error handling:**
- `TERMINATED|FAILED` — fetch run output with `databricks api get /api/2.1/jobs/runs/get-output` and show the error to the user
- `ModuleNotFoundError: dbldatagen` — missing `"dependencies": ["dbldatagen"]` in environment spec
- `DataGenError: invalid column option baseValue` — used `template` instead of `expr`
- `UNRESOLVED_COLUMN` in `expr=` — you can't reference other column names in `expr`. Use `values=[]` for all categoricals, `expr="concat('Prefix_', cast(id as string))"` for names, `expr="uuid()"` for IDs. Only `id` is available in expressions.

---

## Step 4 — Enrich Tables + Genify Metadata

**IMPORTANT: This is a two-phase process. CTAS must complete before COMMENT statements.**

### Phase 1: CTAS enriched tables from raw
Run one CTAS per table via SQL API. Run all 4 in parallel:
```bash
for TABLE in {table1} {table2} {table3} {table4}; do
  databricks api post /api/2.0/sql/statements --profile ${DATABRICKS_PROFILE} --json "{
    \"warehouse_id\": \"${WAREHOUSE_ID}\",
    \"statement\": \"CREATE OR REPLACE TABLE ${CATALOG}.{SCHEMA_PREFIX}_enriched.${TABLE} AS SELECT * FROM ${CATALOG}.{SCHEMA_PREFIX}_raw.${TABLE}\",
    \"wait_timeout\": \"30s\"
  }"
done
```

Verify all 4 return `"state": "SUCCEEDED"` before proceeding to Phase 2. If any fail, stop and report the error.

### Phase 2: Apply COMMENT ON TABLE and COMMENT ON COLUMN
Run each comment as a separate SQL API call. Do NOT try to batch them in a single statement.

**Genify comment generation rules:**
- **Table comments** must state: what each row represents, which rows to INCLUDE, which to EXCLUDE, and why
- **Column comments** must state: what the column means, valid values, and HOW TO USE IT in queries (filter guidance)
- **The most important comments** are on the "poison" columns — the ones that encode which rows to exclude
- Example: `"Account classification: residential, business, internal, test. CRITICAL: Always exclude internal and test accounts from all customer-facing metrics. Internal = employee lines. Test = automated QA."`

Generate 1 table comment + all column comments per table. That's typically 4 table comments + 25-35 column comments = 30-40 SQL API calls. Run them sequentially (each is fast).

```bash
# Pattern for each comment:
databricks api post /api/2.0/sql/statements --profile ${DATABRICKS_PROFILE} --json '{
  "warehouse_id": "${WAREHOUSE_ID}",
  "statement": "COMMENT ON TABLE ${CATALOG}.{SCHEMA_PREFIX}_enriched.{table} IS '\''comment text'\''",
  "wait_timeout": "30s"
}'
```

**Tip:** Use a Python script to run all comments to avoid shell quoting issues:
```python
import subprocess, json

PROFILE = "${DATABRICKS_PROFILE}"
WAREHOUSE = "${WAREHOUSE_ID}"

stmts = [
    "COMMENT ON TABLE ... IS '...'",
    "COMMENT ON COLUMN ... IS '...'",
    # ... all comments
]
for stmt in stmts:
    body = json.dumps({"warehouse_id": WAREHOUSE, "statement": stmt, "wait_timeout": "30s"})
    result = subprocess.run(
        ["databricks", "api", "post", "/api/2.0/sql/statements", "--profile", PROFILE, "--json", body],
        capture_output=True, text=True
    )
    resp = json.loads(result.stdout) if result.stdout else {}
    if resp.get("status", {}).get("state") != "SUCCEEDED":
        print(f"FAILED: {stmt[:80]}... -> {resp.get('status', {})}")
```

---

## Step 5 — Create Metric Views

Write a notebook to `/tmp/golden-path-demo/{SCHEMA_PREFIX}_create_metric_views.py` with 3 metric views (one per fact table).

### Metric View Syntax (MUST use exactly this format):
```sql
CREATE OR REPLACE VIEW ${CATALOG}.{SCHEMA_PREFIX}_enriched.mv_{name}
WITH METRICS LANGUAGE YAML AS $$
version: 1.1
comment: "Description of what this metric view measures and what it excludes."

source: ${CATALOG}.{SCHEMA_PREFIX}_enriched.{fact_table}

joins:
  - name: {dim_alias}
    source: ${CATALOG}.{SCHEMA_PREFIX}_enriched.{dim_table}
    "on": source.{fk} = {dim_alias}.{pk}

filter: {dim_alias}.{poison_column} IN ('valid_value_1', 'valid_value_2') AND {additional_filters}

dimensions:
  - name: {date_column}
    expr: {date_column}
    comment: "Description."
  - name: {category_column}
    expr: {expression}
    comment: "Description."

measures:
  - name: {metric_name}
    expr: COUNT(DISTINCT source.{id_column})
    comment: "Description of what this counts and what it excludes."
$$
```

### CRITICAL syntax rules:
- `CREATE OR REPLACE VIEW ... WITH METRICS LANGUAGE YAML AS $$ ... $$` — NOT `CREATE METRIC VIEW`
- `"on":` must be quoted in YAML (it's a reserved word)
- Do NOT use `format:` field — it requires complex v1.1 type structure and errors out
- Validation query: `SELECT dim, MEASURE(metric) FROM mv GROUP BY dim LIMIT 5`
- The `filter:` line is WHERE the magic happens — it encodes the business logic that Genie uses
- **Join constraint:** Each join's `"on"` clause can ONLY reference `source.column` and `alias.column`. You CANNOT reference other join aliases (no multi-hop joins like `ord.customer_id = cust.customer_id`). If you need a 3-table join, limit the metric view to 2 tables or restructure so the FK chain goes through `source`.

### Upload and run:
```bash
databricks workspace import --file /tmp/golden-path-demo/{SCHEMA_PREFIX}_create_metric_views.py \
  --format SOURCE --language PYTHON --overwrite \
  /Workspace/Shared/golden-path-demo/{SCHEMA_PREFIX}_create_metric_views --profile ${DATABRICKS_PROFILE}

# Create and run job (no dbldatagen dependency needed)
JOB_ID=$(databricks api post /api/2.1/jobs/create --profile ${DATABRICKS_PROFILE} --json '{
  "name": "Golden Path - {CUSTOMER} Metric Views",
  "tasks": [{"task_key": "mvs", "notebook_task": {"notebook_path": "/Workspace/Shared/golden-path-demo/{SCHEMA_PREFIX}_create_metric_views", "source": "WORKSPACE"}, "environment_key": "default"}],
  "environments": [{"environment_key": "default", "spec": {"client": "2"}}]
}' 2>&1 | python3 -c "import sys,json; print(json.load(sys.stdin).get('job_id'))")

RUN_ID=$(databricks api post /api/2.1/jobs/run-now --profile ${DATABRICKS_PROFILE} --json "{\"job_id\": $JOB_ID}" 2>&1 | python3 -c "import sys,json; print(json.load(sys.stdin).get('run_id'))")

# Poll
for i in $(seq 1 20); do
  sleep 15
  STATE=$(databricks api get /api/2.1/jobs/runs/get --profile ${DATABRICKS_PROFILE} --json "{\"run_id\": $RUN_ID}" 2>&1 | python3 -c "import sys,json; s=json.load(sys.stdin).get('state',{}); print(f\"{s.get('life_cycle_state')}|{s.get('result_state','pending')}\")")
  echo "  [$i] $STATE"
  if echo "$STATE" | grep -q "TERMINATED"; then break; fi
done
```

**Error handling:** If `TERMINATED|FAILED`, fetch run output and show error. Common metric view errors:
- `PARSE_SYNTAX_ERROR` — check YAML indentation and quoting of `"on":`
- `TABLE_OR_VIEW_NOT_FOUND` — CTAS from Step 4 may not have completed

---

## Step 6 — Create Genie Spaces

Create two Genie Spaces via REST API. Run both in parallel.

**Safe resource management:** This step CREATES new Genie Spaces — it does NOT delete or overwrite existing ones. Each run produces new spaces with unique IDs.

### BEFORE (raw, no metadata):
```bash
python3 -c "
import subprocess, json, sys

PROFILE = '${DATABRICKS_PROFILE}'
WAREHOUSE = '${WAREHOUSE_ID}'
CATALOG = '${CATALOG}'
WORKSPACE_URL = '${WORKSPACE_URL}'

tables = sorted(['{table1}', '{table2}', '{table3}', '{table4}'])
serialized = json.dumps({'version': 2, 'data_sources': {'tables': [{'identifier': f'{CATALOG}.{SCHEMA_PREFIX}_raw.{t}'} for t in tables]}})
body = json.dumps({'warehouse_id': WAREHOUSE, 'title': '{CUSTOMER} Analytics (BEFORE - No Golden Path)', 'description': 'Raw data with no Genify metadata or metric views.', 'serialized_space': serialized})
r = subprocess.run(['databricks', 'api', 'post', '/api/2.0/genie/spaces', '--profile', PROFILE, '--json', body], capture_output=True, text=True)
if r.returncode != 0:
    print(f'ERROR creating BEFORE space: {r.stderr}', file=sys.stderr)
    sys.exit(1)
d = json.loads(r.stdout)
sid = d.get('space_id', d.get('id', 'UNKNOWN'))
print(f'BEFORE: {WORKSPACE_URL}/genie/rooms/{sid}')
"
```

### AFTER (enriched + metric views):
```bash
python3 -c "
import subprocess, json, sys

PROFILE = '${DATABRICKS_PROFILE}'
WAREHOUSE = '${WAREHOUSE_ID}'
CATALOG = '${CATALOG}'
WORKSPACE_URL = '${WORKSPACE_URL}'

items = sorted([
    '${CATALOG}.{SCHEMA_PREFIX}_enriched.{table1}',
    '${CATALOG}.{SCHEMA_PREFIX}_enriched.{table2}',
    '${CATALOG}.{SCHEMA_PREFIX}_enriched.{table3}',
    '${CATALOG}.{SCHEMA_PREFIX}_enriched.{table4}',
    '${CATALOG}.{SCHEMA_PREFIX}_enriched.mv_{mv1}',
    '${CATALOG}.{SCHEMA_PREFIX}_enriched.mv_{mv2}',
    '${CATALOG}.{SCHEMA_PREFIX}_enriched.mv_{mv3}',
])
serialized = json.dumps({'version': 2, 'data_sources': {'tables': [{'identifier': t} for t in items]}})
body = json.dumps({'warehouse_id': WAREHOUSE, 'title': '{CUSTOMER} Analytics (AFTER - Golden Path)', 'description': 'Enriched data with Genify metadata and metric views.', 'serialized_space': serialized})
r = subprocess.run(['databricks', 'api', 'post', '/api/2.0/genie/spaces', '--profile', PROFILE, '--json', body], capture_output=True, text=True)
if r.returncode != 0:
    print(f'ERROR creating AFTER space: {r.stderr}', file=sys.stderr)
    sys.exit(1)
d = json.loads(r.stdout)
sid = d.get('space_id', d.get('id', 'UNKNOWN'))
print(f'AFTER: {WORKSPACE_URL}/genie/rooms/{sid}')
"
```

**IMPORTANT:** Tables MUST be sorted alphabetically by `identifier` in the `serialized_space` JSON or the API will reject it.

Capture both URLs.

---

## Step 7 — Generate Demo Walkthrough Google Doc

Write a demo script to `/tmp/golden-path-demo/{SCHEMA_PREFIX}_demo_script.md` following this structure:

```markdown
# Golden Path to Enterprise AI — [CUSTOMER] Demo

## [CUSTOMER] | Databricks Field Engineering

**Workspace:** ${WORKSPACE_URL}
**Catalog:** ${CATALOG}
**Duration:** 25-35 minutes
**Prepared for:** [CUSTOMER] ([INDUSTRY])

---

## Pre-Demo Setup (5 min)

1. Open two browser tabs to the workspace
2. Open both Genie Spaces:
   - BEFORE: [BEFORE_URL]
   - AFTER: [AFTER_URL]
3. Have a SQL editor open for DESCRIBE queries

---

## Act 1: The Problem (5 min)

> "[CUSTOMER] has data in the Lakehouse. Tables exist. But when your VP asks '[MONEY_QUESTION]' — the answer depends on who you ask."

### Show raw tables
DESCRIBE EXTENDED ${CATALOG}.{SCHEMA_PREFIX}_raw.{dim_table};
Point out: No comments. No business context. No way to know which rows to exclude.

### Ask the BEFORE Genie Space: "[MONEY_QUESTION]"
Expected: Wrong answer — includes [POISON_DATA], inflating/deflating the metric.

---

## Act 2: Genify (7 min)

> "Genify makes your data AI-ready."

Show enriched table:
DESCRIBE EXTENDED ${CATALOG}.{SCHEMA_PREFIX}_enriched.{dim_table};

Read the poison column comment aloud — the one with the CRITICAL filter guidance.

---

## Act 3: Metric Views (10 min)

> "Metric views are SQL guardrails for Genie."

Show metric view query:
SELECT {dim}, MEASURE({key_metric}) FROM ${CATALOG}.{SCHEMA_PREFIX}_enriched.mv_{name} GROUP BY {dim} LIMIT 10;

---

## Act 4: The Payoff — Before vs After (8 min)

| Question | BEFORE | AFTER |
|----------|--------|-------|
| "[MONEY_QUESTION]" | Wrong — includes [poison] | Correct — filtered + metric view |
| [Q2] | [wrong] | [correct] |
| [Q3] | [wrong] | [correct] |
| [Q4] | [wrong] | [correct] |
| [Q5] | [wrong] | [correct] |

> "Same data. Same questions. Dramatically better answers. That's the Golden Path."

---

## Act 5: The Framework (5 min)

> "One domain. One data product. 60 days. Then replicate."

---

## Artifacts

| Asset | Location |
|-------|----------|
| Raw tables | ${CATALOG}.{SCHEMA_PREFIX}_raw.* |
| Enriched tables | ${CATALOG}.{SCHEMA_PREFIX}_enriched.* |
| Metric views | ${CATALOG}.{SCHEMA_PREFIX}_enriched.mv_* |
| BEFORE Genie Space | [BEFORE_URL] |
| AFTER Genie Space | [AFTER_URL] |
| Data gen notebook | /Workspace/Shared/golden-path-demo/{SCHEMA_PREFIX}_generate_data |
| Metric views notebook | /Workspace/Shared/golden-path-demo/{SCHEMA_PREFIX}_create_metric_views |

## Audience Guide

| Audience | Duration | Focus |
|----------|----------|-------|
| C-level | 15 min | Acts 1 + 4 only. Wrong answer, right answer, framework. |
| Data Leaders | 25 min | Full demo. Emphasize Genify + metric views. |
| Engineers | 35 min | Full demo + YAML deep dive + column comment patterns. |
| Workshop | 90 min | Full demo + hands-on: build metric views for a second domain. |
```

### Generate 5 comparison questions:
Based on the industry and data model, generate 5 questions where the BEFORE space will give a wrong/misleading answer and the AFTER space will give the correct answer. The first question is always the MONEY_QUESTION. Fill in the expected wrong vs correct behavior for each.

### Convert to Google Doc:
```bash
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-docs/resources/markdown_to_gdocs.py \
  --input /tmp/golden-path-demo/{SCHEMA_PREFIX}_demo_script.md \
  --title "Golden Path Demo — {CUSTOMER}"
```

---

## Step 8 — Deliver

Post the final output:

```
Golden Path demo ready for [CUSTOMER]:

Demo Walkthrough: [Google Doc URL]

Assets on workspace:
  Raw tables:      ${CATALOG}.{SCHEMA_PREFIX}_raw.* (4 tables, ~[N]K rows, 0 comments)
  Enriched tables: ${CATALOG}.{SCHEMA_PREFIX}_enriched.* (4 tables, [N] comments)
  Metric views:    mv_[name1], mv_[name2], mv_[name3]
  BEFORE Genie:    [BEFORE_URL]
  AFTER Genie:     [AFTER_URL]

Demo comparison questions:
  1. "[MONEY_QUESTION]"
  2. [Q2]
  3. [Q3]
  4. [Q4]
  5. [Q5]

The BEFORE space includes [POISON_DATA] and has no business context.
The AFTER space filters correctly via metric views + Genify metadata.

Ready to demo — open both Genie Spaces side by side and fire away.
```

---

## Error Handling

| Failure | How to detect | Recovery |
|---------|--------------|----------|
| Databricks auth expired | Profile check in Step 0 returns auth error | Tell user to run `/databricks-authentication` |
| Google auth expired | Token check returns empty | Tell user to run `/google-auth` |
| Schema creation fails | SQL API returns error state | Check catalog permissions, report error to user |
| Data gen job fails | Poll returns `TERMINATED\|FAILED` | Fetch run output with `jobs/runs/get-output`, show error |
| Metric view syntax error | Job fails with `PARSE_SYNTAX_ERROR` | Check YAML quoting (`"on":`) and indentation |
| Genie Space API error | Python script exits non-zero | Show API error response, check warehouse permissions |
| Google Doc creation fails | `markdown_to_gdocs.py` exits non-zero | Check Google auth, retry `/google-auth` |

**Never silently skip a failed step.** If any step fails, stop and report the error with enough context for the user to fix it.

---

## Technical Reference

### Metric View Syntax (CORRECT — use exactly this)
```sql
CREATE OR REPLACE VIEW catalog.schema.mv_name
WITH METRICS LANGUAGE YAML AS $$
version: 1.1
comment: "Description"
source: catalog.schema.fact_table
joins:
  - name: dim_alias
    source: catalog.schema.dim_table
    "on": source.fk = dim_alias.pk
filter: <business logic filters>
dimensions:
  - name: col
    expr: expression
    comment: "Description"
measures:
  - name: metric
    expr: AGG(column)
    comment: "Description"
$$
```

### Genie Space API
```python
# Tables MUST be sorted alphabetically by identifier
serialized = json.dumps({
    "version": 2,
    "data_sources": {
        "tables": sorted([{"identifier": "..."}, ...], key=lambda x: x["identifier"])
    }
})
# POST /api/2.0/genie/spaces with warehouse_id, title, description, serialized_space
```

### dbldatagen Patterns
- `expr="uuid()"` for IDs
- `expr="concat('Name_', cast(id as string))"` for display names (NOT `template` with `baseValue`)
- `values=[...]` with `weights=[...]` for categoricals
- Run on serverless with `"dependencies": ["dbldatagen"]` in environment spec

### Pre-Built Vertical Resources

> **WARNING:** Resource files in `resources/verticals/` contain hardcoded `cmegdemos_catalog` references from the original development workspace. These MUST be replaced with the user's `${CATALOG}` and `{SCHEMA_PREFIX}` values at runtime before execution. This is accepted tech debt for a pilot/training skill — full parameterization is planned for a future iteration.

This skill includes ready-to-run assets in `resources/verticals/`:

| Vertical | Files | Key Tables |
|----------|-------|------------|
| **gaming** | `01_create_tables.sql`, `02_generate_data.py`, `03_apply_genify.sql`, `04_create_metric_views.py`, `demo_script.md` | players, sessions, transactions, match_history |
| **retail** | `02_generate_data.py`, `04_create_metric_views.py`, `demo_script.md` | customers, orders, products, returns |
| **rmg** | `01_create_tables.sql`, `02_generate_data.py`, `03_apply_genify.sql`, `04_create_metric_views.sql`, `demo_script.md` | patrons, wagers, transactions, sessions |
| **indie** | `01_create_tables.sql`, `02_generate_data.py`, `03_apply_genify.sql`, `04_create_metric_views.py`, `05_create_genie_spaces.py`, `demo_script.md` | players, game_runs, purchases, sessions |

For pre-built verticals, load and execute the numbered files in order. For custom verticals, generate equivalent assets following the patterns in the gaming template.

**Note:** Pre-built resource files may contain hardcoded catalog/schema references from the original workspace. When using them, search-and-replace the catalog and schema values to match `${CATALOG}` and `{SCHEMA_PREFIX}` before executing.

---

## Safe Resource Management

This skill creates the following resources:
- **Schemas**: Uses `CREATE SCHEMA IF NOT EXISTS` — safe, will not overwrite existing schemas
- **Tables**: Uses `CREATE OR REPLACE TABLE` in dedicated `{SCHEMA_PREFIX}_raw` and `{SCHEMA_PREFIX}_enriched` schemas — the schema prefix is customer-specific so collisions with existing tables are unlikely. If the user re-runs for the same customer, tables are replaced (expected behavior for regeneration)
- **Notebooks**: Uploaded with `--overwrite` to `/Workspace/Shared/golden-path-demo/` — only overwrites the skill's own notebooks in its own directory
- **Jobs**: Creates new jobs each run. Does NOT delete existing jobs
- **Genie Spaces**: Creates new spaces each run. Does NOT delete existing spaces

**This skill does NOT delete any pre-existing resources.** Re-runs for the same customer will replace that customer's generated tables and notebooks only.

---

## Pre-Requisites

- Databricks CLI with a configured profile (`/databricks-authentication`)
- Google auth for doc creation (`/google-auth`)
- Salesforce auth optional — for UCO context (`/salesforce-authentication`)

---

## Invocation Examples

```
/golden-path-demo
  Prompts for customer, industry, money question. Generates everything.

/golden-path-demo DraftKings
  Gaming template. Money question: "How many active players?"

/golden-path-demo Comcast
  Telecom template. Money question: "What's our churn rate?"

/golden-path-demo CVS
  Healthcare template. Money question: "What's our average LOS?"

/golden-path-demo Target
  Retail template. Money question: "What's our return rate?"
```
