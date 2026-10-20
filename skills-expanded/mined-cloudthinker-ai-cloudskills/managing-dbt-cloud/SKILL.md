---
name: managing-dbt-cloud
description: |
  Use when working with Dbt Cloud — dbt Cloud management — monitor projects,
  environments, job runs, model status, and data freshness. Use when reviewing
  job run health, debugging failed models, inspecting run artifacts, or auditing
  project configuration.
connection_type: dbt-cloud
preload: false
---

# Managing dbt Cloud

Manage and monitor dbt Cloud — projects, environments, jobs, run history, and model artifacts.

## Discovery Phase

```bash
#!/bin/bash

DBT_API="https://cloud.getdbt.com/api/v2"
AUTH="Authorization: Token $DBT_CLOUD_API_TOKEN"

echo "=== Account Info ==="
curl -s -H "$AUTH" "$DBT_API/accounts/$DBT_CLOUD_ACCOUNT_ID/" \
  | jq '.data | {name: .name, id: .id, plan: .plan, run_slots: .run_slots}'

echo ""
echo "=== Projects ==="
curl -s -H "$AUTH" "$DBT_API/accounts/$DBT_CLOUD_ACCOUNT_ID/projects/" \
  | jq -r '.data[] | [.id, .name, .connection.type, .repository.remote_url] | @tsv' | column -t | head -10

echo ""
echo "=== Environments ==="
curl -s -H "$AUTH" "$DBT_API/accounts/$DBT_CLOUD_ACCOUNT_ID/environments/" \
  | jq -r '.data[] | [.id, .name, .type, .dbt_version, .project_id] | @tsv' | column -t | head -10

echo ""
echo "=== Jobs ==="
curl -s -H "$AUTH" "$DBT_API/accounts/$DBT_CLOUD_ACCOUNT_ID/jobs/" \
  | jq -r '.data[] | [.id, .name, .project_id, .state, .schedule.cron] | @tsv' | column -t | head -15
```

## Analysis Phase

```bash
#!/bin/bash

DBT_API="https://cloud.getdbt.com/api/v2"
AUTH="Authorization: Token $DBT_CLOUD_API_TOKEN"
ACCT="accounts/$DBT_CLOUD_ACCOUNT_ID"

echo "=== Recent Runs ==="
curl -s -H "$AUTH" "$DBT_API/$ACCT/runs/?limit=15&order_by=-created_at" \
  | jq -r '.data[] | [.id, .job.name, .status_humanized, .duration_humanized, .created_at] | @tsv' | column -t

echo ""
echo "=== Failed Runs ==="
curl -s -H "$AUTH" "$DBT_API/$ACCT/runs/?limit=10&status=20" \
  | jq -r '.data[] | [.id, .job.name, .created_at, .status_message[:60]] | @tsv' | column -t

echo ""
echo "=== Run Artifacts (latest) ==="
LATEST_RUN=$(curl -s -H "$AUTH" "$DBT_API/$ACCT/runs/?limit=1&status=10&order_by=-finished_at" | jq -r '.data[0].id')
if [ "$LATEST_RUN" != "null" ]; then
  echo "Run ID: $LATEST_RUN"
  curl -s -H "$AUTH" "$DBT_API/$ACCT/runs/$LATEST_RUN/artifacts/" \
    | jq -r '.data[]' | head -10

  echo ""
  echo "=== Run Results Summary ==="
  curl -s -H "$AUTH" "$DBT_API/$ACCT/runs/$LATEST_RUN/artifacts/run_results.json" \
    | jq '{elapsed_time: .elapsed_time, results: [.results[] | {model: .unique_id, status: .status, execution_time: .execution_time}] | sort_by(-.execution_time)[:10]}'
fi

echo ""
echo "=== Model Freshness ==="
curl -s -H "$AUTH" "$DBT_API/$ACCT/runs/$LATEST_RUN/artifacts/sources.json" 2>/dev/null \
  | jq -r '.results[] | [.unique_id, .status, .max_loaded_at, .criteria.warn_after.count // "N/A"] | @tsv' | column -t | head -10
```

## Output Format

```
ACCOUNT
Name:       <account-name>
Plan:       <plan>
Run Slots:  <n>

JOBS
ID       Name             Project  State    Cron
<id>     <job-name>       <proj>   active   <cron>

RECENT RUNS
ID       Job              Status      Duration     Created
<id>     <job-name>       Success     <duration>   <timestamp>

FAILED RUNS
ID       Job              Created         Error
<id>     <job-name>       <timestamp>     <message>

MODEL PERFORMANCE (latest run)
Model              Status    Execution Time
<model-name>       pass      <seconds>s
```

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

