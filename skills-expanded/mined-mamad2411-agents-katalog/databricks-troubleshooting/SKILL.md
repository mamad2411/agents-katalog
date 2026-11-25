---
name: databricks-troubleshooting
description: Systematic troubleshooting guide for common Databricks issues and errors
user-invocable: true
---

# Databricks Troubleshooting Workflow

This skill provides a systematic approach to diagnosing and resolving common Databricks issues. It covers clusters, jobs, SQL warehouses, authentication, networking, Unity Catalog, and model serving.

**Related skills:**
- `/performance-tuning` — for slow queries, spill/skew, cost optimization
- `/support-escalation` — for issues that require engineering involvement
- `/jira-actions` — for ES ticket creation

## Prerequisites

- Authenticated to the target Databricks workspace (`/databricks-authentication`)
- Access to cluster/job logs or the error message text
- Databricks CLI installed (`databricks --version`)

## Step 1: Gather Information

Before diagnosing, collect context. Run these commands to understand the environment:

```bash
# Workspace info
databricks current-user me --output json | jq '{user: .userName, workspace: .displayName}'

# Cluster runtime version (if cluster-related)
databricks clusters get <CLUSTER_ID> --output json | jq '{state: .state, spark_version: .spark_version, node_type: .node_type_id, autoscale: .autoscale, num_workers: .num_workers}'

# Recent job runs (if job-related)
databricks jobs list-runs --job-id <JOB_ID> --limit 5 --output json | jq '.runs[] | {run_id: .run_id, state: .state.result_state, start_time: .start_time, end_time: .end_time}'
```

**Ask the user for:**
1. The exact error message or screenshot
2. When it started happening (first occurrence, frequency)
3. What changed recently (new code, config change, runtime upgrade, permissions change)
4. Whether it's reproducible or intermittent

## Step 2: Identify Error Category

Classify the issue into one of these categories based on the error message or symptoms:

| Category | Common Symptoms | Jump To |
|----------|----------------|---------|
| **Cluster** | Fails to start, terminates unexpectedly, CLOUD_PROVIDER_LAUNCH_FAILURE | [Cluster Issues](#cluster-issues) |
| **Job** | Run fails, timeout, task skipped, dependency error | [Job Failures](#job-failures) |
| **SQL Warehouse** | Query timeout, warehouse won't start, ODBC/JDBC errors | [SQL Warehouse Issues](#sql-warehouse-issues) |
| **Authentication** | 401/403, token expired, SSO loop, SCIM errors | [Authentication Errors](#authentication-errors) |
| **Unity Catalog** | PERMISSION_DENIED, catalog not found, lineage missing | [Unity Catalog Issues](#unity-catalog-issues) |
| **Networking** | Connection timeout, PrivateLink errors, egress blocked | [Networking Issues](#networking-issues) |
| **Model Serving** | Endpoint failed, cold start timeout, OOM | [Model Serving Issues](#model-serving-issues) |
| **Spark/Performance** | OOM, shuffle spill, skew, slow queries | Use `/performance-tuning` instead |

## Cluster Issues

### Cluster Fails to Start

**Diagnostic steps:**

```bash
# Get cluster events (shows why it failed)
databricks clusters events <CLUSTER_ID> --output json | jq '.events[] | select(.type == "TERMINATING" or .type == "NOT_RUNNING") | {type: .type, reason: .details.reason, code: .details.code, timestamp: .timestamp}' | head -20

# Check init script logs (common failure source)
databricks fs ls dbfs:/cluster-logs/<CLUSTER_ID>/init_scripts/ 2>/dev/null
```

**Common causes and fixes:**

| Error | Cause | Fix |
|-------|-------|-----|
| `CLOUD_PROVIDER_LAUNCH_FAILURE` | AWS/Azure/GCP capacity or quota | Try different availability zone, instance type, or request quota increase |
| `INIT_SCRIPT_FAILURE` | Init script error or timeout | Check init script logs at `dbfs:/cluster-logs/<CLUSTER_ID>/init_scripts/`. Scripts must exit 0 within 10 minutes. |
| `DRIVER_UNREACHABLE` | Driver node crashed during startup | Check driver logs. Often caused by OOM from large library installs or init scripts. Increase driver node size. |
| `SPARK_STARTUP_FAILURE` | Spark config error | Review `spark_conf` for invalid settings. Common: wrong `spark.executor.memory` format, invalid Hive metastore URI. |
| `INSTANCE_POOL_CLUSTER_FAILURE` | Pool has no available instances | Check pool min/max idle, or switch to on-demand. |
| `METASTORE_DOWN` | HMS/UC metastore unreachable | Check workspace metastore assignment. For external HMS, verify connectivity and credentials. |

### Cluster Terminates Unexpectedly

```bash
# Check termination reason
databricks clusters get <CLUSTER_ID> --output json | jq '{state: .state, termination_reason: .termination_reason}'
```

| Reason | Fix |
|--------|-----|
| `INACTIVITY` | Increase auto-termination timeout or disable it for long-running workloads |
| `CLOUD_PROVIDER_SHUTDOWN` | Spot/preemptible instance reclaimed. Use on-demand for driver, spot for workers only. |
| `SPARK_ERROR` | OOM or unhandled exception. Check Spark UI > Executors for memory usage. |
| `GLOBAL_INIT_SCRIPT_FAILURE` | Workspace-level init script failed. Check admin console > Compute > Global init scripts. |

### Library Installation Failures

```bash
# Check library status
databricks libraries cluster-status <CLUSTER_ID> --output json | jq '.library_statuses[] | select(.status != "INSTALLED") | {library: .library, status: .status, messages: .messages}'
```

**Common fixes:**
- PyPI timeout: Add `--index-url` to a mirror, or use init script with `pip install --timeout 120`
- Conflicting versions: Use `%pip install` in notebook instead of cluster libraries for isolation
- Maven resolution failure: Verify artifact coordinates and repository URL

## Job Failures

### Diagnostic Steps

```bash
# Get run details with error
databricks jobs get-run <RUN_ID> --output json | jq '{state: .state, tasks: [.tasks[] | {task_key: .task_key, state: .state.result_state, life_cycle_state: .state.life_cycle_state}]}'

# Get task-level output for failed task
databricks jobs get-run-output <RUN_ID> --output json | jq '{error: .error, error_trace: .error_trace}'
```

### Common Job Failures

| Error Pattern | Cause | Fix |
|---------------|-------|-----|
| `LIBRARY_INSTALLATION_ERROR` | Dependency conflict or network issue | Pin library versions. Use `%pip install` in notebook tasks. |
| `RUN_DURATION_EXCEEDED` | Job exceeded timeout | Increase timeout in job settings, or optimize the workload. |
| `MAX_CONCURRENT_RUNS_REACHED` | Too many parallel runs | Increase `max_concurrent_runs` or queue runs. |
| `INTERNAL_ERROR` | Platform-side issue | Retry. If persistent, file ES ticket with run ID. |
| `INVALID_CLUSTER_REQUEST` | Cluster spec invalid (e.g., instance type retired) | Update job cluster spec to use current instance types. |
| Task dependency `EXCLUDED` | Upstream task failed | Fix the upstream task first. Check `depends_on` configuration. |

### Workflow/Orchestration Issues

```bash
# List recent runs to see failure pattern
databricks jobs list-runs --job-id <JOB_ID> --limit 10 --output json | jq '.runs[] | {run_id: .run_id, result: .state.result_state, trigger: .trigger}'
```

- **Cron not triggering:** Verify timezone in schedule. Databricks uses UTC by default. Check `quartz_cron_expression` syntax.
- **Repair runs failing:** Repair only re-runs failed/skipped tasks. If the failure was in a shared cluster setup, the repair may hit the same issue.
- **Task parameters not passing:** Use `{{job.parameters.X}}` syntax. Dynamic values from upstream tasks use `{{tasks.task_key.values.output}}`.

## SQL Warehouse Issues

### Warehouse Won't Start

```bash
# Check warehouse status
databricks warehouses get <WAREHOUSE_ID> --output json | jq '{name: .name, state: .state, num_clusters: .num_clusters, health: .health}'
```

| Issue | Fix |
|-------|-----|
| Stuck in `STARTING` | Check for quota limits. Serverless warehouses may queue during high demand. Wait or try a different size. |
| `STOPPED` and won't start | Check if the user has `CAN_USE` permission on the warehouse. Check if workspace has serverless enabled. |
| Frequent auto-stop | Increase `auto_stop_mins`. For dashboards, set to 10+ minutes. |

### Query Failures

| Error | Fix |
|-------|-----|
| `TEMPORARILY_UNAVAILABLE` | Warehouse is scaling. Retry after a few seconds. For dashboards, increase `min_num_clusters`. |
| `TABLE_OR_VIEW_NOT_FOUND` | Check catalog/schema context. Run `SELECT current_catalog(), current_schema()` to verify. |
| `ODBC/JDBC connection refused` | Verify hostname, HTTP path, and token. For PrivateLink, check DNS resolution. |
| Query timeout | Increase `statement_timeout_seconds` in warehouse config. Default is 2 hours. |

## Authentication Errors

### Token/PAT Issues

| Error | Fix |
|-------|-----|
| `401 Unauthorized` | Token expired or revoked. Generate new PAT: Workspace > User Settings > Developer > Access tokens. |
| `403 Forbidden` | Token valid but user lacks permissions. Check workspace admin console for entitlements. |
| `PERMISSION_DENIED on API call` | User may need specific entitlement (e.g., `workspace-access`, `databricks-sql-access`). |

### SSO/SAML Issues

- **SSO login loop:** Clear browser cookies for the workspace domain. Check IdP SAML assertion for `NameID` format.
- **User provisioned but can't log in:** Verify SCIM sync is active and user is in the correct IdP group.
- **Service principal auth failing:** Verify OAuth secret hasn't expired. For M2M OAuth, check token endpoint URL matches workspace region.

```bash
# Verify current auth method
databricks auth describe --output json | jq '{auth_type: .auth_type, host: .host, user: .username}'

# Test connectivity
databricks current-user me
```

### CLI Authentication

```bash
# If CLI auth fails, re-configure
databricks auth login --host <WORKSPACE_URL>

# For service principals
databricks auth login --host <WORKSPACE_URL> --client-id <SP_CLIENT_ID> --client-secret <SP_SECRET>

# Verify profile
databricks auth profiles
```

## Unity Catalog Issues

### Permission Errors

```bash
# Check grants on an object
databricks unity-catalog effective-permissions get <SECURABLE_TYPE> <FULL_NAME> --output json

# Common securable types: catalog, schema, table, volume, function
```

| Error | Fix |
|-------|-----|
| `PERMISSION_DENIED` on table | Grant `SELECT` on the table, or `USE CATALOG` + `USE SCHEMA` on parent objects. All three levels needed. |
| `CATALOG_NOT_FOUND` | Catalog not assigned to workspace. Admin must bind it via Account Console > Catalog > Workspaces. |
| `SCHEMA_NOT_FOUND` | Check spelling and catalog context. Run `SHOW SCHEMAS IN <catalog>`. |
| Lineage not showing | Lineage requires Unity Catalog-enabled compute. Check cluster has UC access mode (Shared or Single User). |

### Common UC Patterns

```sql
-- Grant read access to a table
GRANT SELECT ON TABLE catalog.schema.table TO `user@example.com`;

-- Grant usage on parent objects (required for access)
GRANT USE CATALOG ON CATALOG catalog TO `user@example.com`;
GRANT USE SCHEMA ON SCHEMA catalog.schema TO `user@example.com`;

-- Check who has access
SHOW GRANTS ON TABLE catalog.schema.table;
```

### External Locations / Storage Credentials

```bash
# List external locations
databricks unity-catalog external-locations list --output json | jq '.[].name'

# Validate access
databricks unity-catalog validate-external-location --name <LOCATION_NAME> --url <CLOUD_PATH> --output json
```

- **`STORAGE_CREDENTIAL_PERMISSION_DENIED`:** The storage credential's IAM role/managed identity doesn't have access to the cloud path. Check IAM policy.
- **`EXTERNAL_LOCATION_NOT_FOUND`:** No external location covers the path. Create one or update the existing location's URL prefix.

## Networking Issues

### PrivateLink / VPC Peering

| Symptom | Diagnostic | Fix |
|---------|-----------|-----|
| Connection timeout to workspace | `nslookup <workspace-url>` — should resolve to private IP | Check DNS configuration. PrivateLink requires private DNS zone. |
| Can't reach external APIs | `curl -v https://api.example.com` from notebook | Check NSG/security group egress rules. Databricks needs outbound HTTPS (443). |
| DBFS mount fails | Check storage endpoint connectivity | For PrivateLink workspaces, ensure storage service endpoint or PrivateLink is configured. |

### Connectivity Testing from Notebook

```python
# Test outbound connectivity from a cluster
import subprocess
result = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "https://api.example.com"], capture_output=True, text=True)
print(f"HTTP status: {result.stdout}")

# Test DNS resolution
result = subprocess.run(["nslookup", "your-workspace.cloud.databricks.com"], capture_output=True, text=True)
print(result.stdout)
```

### Firewall / Proxy Issues

- **Workspace UI loads but clusters fail:** Clusters need outbound access to control plane IPs. Check [Databricks IP ranges](https://docs.databricks.com/en/resources/supported-regions.html).
- **PyPI/Maven install fails:** Proxy may block package registries. Configure `HTTP_PROXY`/`HTTPS_PROXY` in init script or cluster env vars.
- **Metastore connection fails:** For external Hive metastore, verify port 3306 (MySQL) or 5432 (Postgres) is open in security groups.

## Model Serving Issues

### Endpoint Failures

```bash
# Check endpoint status
databricks serving-endpoints get <ENDPOINT_NAME> --output json | jq '{name: .name, state: .state, config: .config.served_entities[0]}'

# Check endpoint logs
databricks serving-endpoints logs <ENDPOINT_NAME> --served-model-name <MODEL_NAME>
```

| Error | Fix |
|-------|-----|
| `ENDPOINT_STATE_CONFIG_UPDATE_FAILED` | Model artifact issue. Check MLflow model registry for the model version. Verify dependencies in `conda.yaml` or `requirements.txt`. |
| Cold start timeout (>120s) | Increase `scale_to_zero_enabled: false` for latency-sensitive endpoints, or increase `workload_size`. |
| `OUT_OF_MEMORY` | Model too large for container. Increase `workload_size` (Small→Medium→Large) or optimize model. |
| `MODEL_LOADING_FAILED` | Missing dependencies or incompatible Python version. Check `python_version` in MLflow model metadata. |
| 429 Too Many Requests | Rate limited. Increase `max_provisioned_throughput` or implement client-side retry with backoff. |

### Foundation Model API Issues

| Error | Fix |
|-------|-----|
| `RESOURCE_DOES_NOT_EXIST` | Model not available in this region. Check [supported models](https://docs.databricks.com/en/machine-learning/model-serving/supported-models.html). |
| Token limit exceeded | Reduce `max_tokens` in request. Check model's context window limit. |
| Slow responses | Use streaming (`stream: true`) for better perceived latency. For batch, use provisioned throughput. |

## Diagnostic Tools

### Cluster Logs

```bash
# Driver logs
databricks fs cat dbfs:/cluster-logs/<CLUSTER_ID>/driver/log4j-active.log | tail -100

# Executor logs (for specific executor)
databricks fs ls dbfs:/cluster-logs/<CLUSTER_ID>/executor/
```

### Spark UI (from notebook)

```python
# Get Spark UI URL
spark.sparkContext.uiWebUrl

# Key tabs to check:
# - Jobs: failed stages, task failures
# - Stages: shuffle read/write, spill
# - Storage: cached RDDs/DataFrames
# - Executors: memory usage, GC time, failed tasks
# - SQL: query plans, scan sizes
```

### System Tables for Historical Analysis

```sql
-- Recent job failures (last 7 days)
SELECT job_id, run_id, result_state, error_message, 
       TIMESTAMPDIFF(MINUTE, start_time, end_time) as duration_min
FROM system.lakeflow.job_run_timeline
WHERE result_state = 'FAILED'
  AND start_time > DATEADD(DAY, -7, CURRENT_TIMESTAMP())
ORDER BY start_time DESC
LIMIT 20;

-- Cluster events
SELECT cluster_id, event_type, event_details, timestamp
FROM system.compute.clusters
WHERE timestamp > DATEADD(DAY, -7, CURRENT_TIMESTAMP())
  AND event_type IN ('TERMINATING', 'NOT_RUNNING', 'INIT_SCRIPTS_FAILED')
ORDER BY timestamp DESC;

-- Warehouse query history (slow or failed)
SELECT statement_id, status, error_message, 
       total_duration_ms, rows_produced
FROM system.query.history
WHERE status = 'FAILED'
  AND start_time > DATEADD(DAY, -1, CURRENT_TIMESTAMP())
ORDER BY start_time DESC
LIMIT 20;
```

### Databricks CLI Diagnostics

```bash
# Workspace connectivity test
databricks current-user me

# List recent cluster events
databricks clusters events <CLUSTER_ID> --order DESC --limit 10

# Check workspace status
databricks workspace get-status /

# API rate limit check (look at response headers)
curl -v -H "Authorization: Bearer $DATABRICKS_TOKEN" "$DATABRICKS_HOST/api/2.0/clusters/list" 2>&1 | grep -i "x-ratelimit"
```

## Step 3: Apply Solutions

After identifying the category and specific error:

1. **Try the fix** from the tables above
2. **Verify** the fix resolved the issue (re-run the failing operation)
3. **If the fix doesn't work**, gather additional diagnostics:
   - Cluster event logs
   - Spark driver/executor logs
   - Network trace (for connectivity issues)
   - Exact API request/response (for auth issues)

## Step 4: Verify and Document

After resolving:

```bash
# Verify the fix (re-run the failing operation)
# For clusters: start the cluster
databricks clusters start <CLUSTER_ID>

# For jobs: trigger a new run
databricks jobs run-now --job-id <JOB_ID>

# For queries: re-execute the failing query
databricks sql execute --warehouse-id <WAREHOUSE_ID> --statement "SELECT 1"
```

**Document the resolution** — update the customer's UCO next steps or ES ticket with:
- Root cause identified
- Fix applied
- Verification result
- Any follow-up actions needed

## Escalation Path

If the issue cannot be resolved with the steps above:

1. **Check known issues:** Search [Databricks Status Page](https://status.databricks.com/) for ongoing incidents
2. **Search internal resources:** Use Glean or Slack `#field-engineering` for similar issues
3. **File an ES ticket:** Use `/jira-actions` to create an Engineering Support ticket with:
   - Workspace URL and ID
   - Cluster/Job/Warehouse ID
   - Exact error message and stack trace
   - Steps to reproduce
   - Diagnostic logs collected above
   - Business impact and urgency
4. **For P1/P2 severity:** Also post in `#support-escalations` Slack channel with the ES ticket number
