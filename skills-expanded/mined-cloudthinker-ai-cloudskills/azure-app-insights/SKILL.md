---
name: azure-app-insights
description: |
  Use when working with Azure App Insights — application Insights request
  performance, dependency tracking, availability tests, smart detection, and
  failure analysis via Azure CLI and Log Analytics queries.
connection_type: azure
preload: false
---

# Application Insights Skill

Manage and analyze Application Insights using `az monitor app-insights` commands.

## Discovery-First Rule

**ALWAYS discover before acting.** Never assume Application Insights resource names, instrumentation keys, or connection strings.

```bash
# Discover Application Insights resources
az monitor app-insights component show --output json \
  --query "[].{name:name, rg:resourceGroup, appId:appId, instrumentationKey:instrumentationKey, ingestionMode:ingestionMode, retentionDays:retentionInDays, kind:kind}"
```

## Parallel Execution Requirement

**ALL independent operations MUST run in parallel using background jobs (&) and wait.**

```bash
for ai in $(echo "$components" | jq -c '.[]'); do
  {
    name=$(echo "$ai" | jq -r '.name')
    rg=$(echo "$ai" | jq -r '.rg')
    az monitor app-insights component show --app "$name" --resource-group "$rg" --output json
  } &
done
wait
```

## Helper Functions

```bash
# Run App Insights query
query_app_insights() {
  local app="$1" query="$2" timespan="${3:-PT1H}"
  az monitor app-insights query --app "$app" --analytics-query "$query" --offset "$timespan" --output json
}

# Get request performance
get_request_perf() {
  local app="$1" timespan="${2:-PT1H}"
  query_app_insights "$app" "requests | where timestamp > ago(1h) | summarize totalCount=count(), failedCount=countif(success==false), avgDuration=avg(duration), p95Duration=percentile(duration,95), p99Duration=percentile(duration,99) by bin(timestamp, 5m) | sort by timestamp desc" "$timespan"
}

# Get dependency performance
get_dependency_perf() {
  local app="$1"
  query_app_insights "$app" "dependencies | where timestamp > ago(1h) | summarize totalCount=count(), failedCount=countif(success==false), avgDuration=avg(duration) by target, type | sort by totalCount desc | take 20"
}

# Get exception summary
get_exceptions() {
  local app="$1"
  query_app_insights "$app" "exceptions | where timestamp > ago(1h) | summarize count() by type, outerMessage | sort by count_ desc | take 20"
}
```

## Common Operations

### 1. Application Health Overview

```bash
app_id=$(az monitor app-insights component show --app "$APP" --resource-group "$RG" --query "appId" -o tsv)

# Request rate and failure rate
query_app_insights "$app_id" "
  requests
  | where timestamp > ago(1h)
  | summarize
      TotalRequests=count(),
      FailedRequests=countif(success==false),
      FailureRate=round(100.0*countif(success==false)/count(), 2),
      AvgDuration=round(avg(duration), 2),
      P95=round(percentile(duration, 95), 2)
  by bin(timestamp, 5m)
  | sort by timestamp desc"
```

### 2. Dependency Tracking

```bash
# Slowest dependencies
query_app_insights "$app_id" "
  dependencies
  | where timestamp > ago(1h)
  | summarize
      calls=count(),
      failures=countif(success==false),
      avgMs=round(avg(duration), 2),
      p95Ms=round(percentile(duration, 95), 2)
  by target, type, name
  | sort by avgMs desc
  | take 15"

# Failed dependency calls
query_app_insights "$app_id" "
  dependencies
  | where timestamp > ago(1h) and success == false
  | summarize count() by target, type, resultCode
  | sort by count_ desc"
```

### 3. Availability Test Results

```bash
# List availability tests
az monitor app-insights web-test list --resource-group "$RG" --output json \
  --query "[].{name:name, enabled:enabled, kind:kind, frequency:frequency, timeout:timeout, locations:locations[].Id}"

# Check availability results
query_app_insights "$app_id" "
  availabilityResults
  | where timestamp > ago(24h)
  | summarize
      successRate=round(100.0*countif(success==1)/count(), 2),
      avgDuration=round(avg(duration), 2),
      totalTests=count()
  by name
  | sort by successRate asc"
```

### 4. Smart Detection and Anomalies

```bash
# Check smart detection alerts
az monitor app-insights component show --app "$APP" --resource-group "$RG" --output json \
  --query "{smartDetection:smartDetection}"

# Query for anomalies in failure rate
query_app_insights "$app_id" "
  requests
  | where timestamp > ago(24h)
  | summarize failRate=round(100.0*countif(success==false)/count(), 2), total=count() by bin(timestamp, 1h)
  | sort by timestamp desc"
```

### 5. End-to-End Transaction Diagnostics

```bash
# Trace a specific operation
query_app_insights "$app_id" "
  union requests, dependencies, exceptions, traces
  | where operation_Id == '$OPERATION_ID'
  | sort by timestamp asc
  | project timestamp, itemType, name, duration, success, resultCode, message, type"

# Slowest operations
query_app_insights "$app_id" "
  requests
  | where timestamp > ago(1h)
  | summarize avgDuration=avg(duration), p95=percentile(duration, 95), count=count() by name
  | where count > 10
  | sort by p95 desc
  | take 10"
```

## Output Format

Present results as a structured report:
```
Azure App Insights Report
═════════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

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

## Common Pitfalls

1. **Sampling**: Application Insights may sample data at high volumes. Check `itemCount` field to see if counts are projected, not exact.
2. **Ingestion delay**: Data can take 2-5 minutes to appear. Do not query for the last few minutes expecting real-time results.
3. **Workspace-based vs classic**: Workspace-based App Insights stores data in Log Analytics. Use `az monitor log-analytics query` for cross-resource queries.
4. **Duration units**: `duration` in KQL is in milliseconds for requests/dependencies. Do not confuse with seconds.
5. **Connection string vs instrumentation key**: Instrumentation keys are deprecated for new resources. Use connection strings for SDK configuration checks.
