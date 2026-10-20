---
name: llm-diagnostics
description: "LLM-powered Databricks diagnostics — job failure analysis, cost attribution, query performance, and job health assessment. Requires a Model Serving endpoint."
---

# LLM-Powered Diagnostics

Use LLM analysis to diagnose Databricks operational issues. This skill leverages a Databricks Model Serving endpoint to provide intelligent analysis of job failures, cost patterns, query performance, and overall job health.

## Prerequisites

- A Databricks Model Serving endpoint configured for chat completions
- Supported models: databricks-meta-llama-3-1-70b-instruct, databricks-claude-sonnet-4, or any chat-completion-compatible endpoint
- Set the endpoint: `export DATABRICKS_LLM_ENDPOINT="your-endpoint-name"`

## Available MCP Tools

### diagnose_job_failure
Analyze a job failure error message and provide root cause, fix steps, and prevention strategies.

**When to use:** After a job fails, pass the error text and any relevant context.

**Example:**
```
diagnose_job_failure(
    error_text="SparkException: Job aborted due to stage failure...",
    context="ETL job processing 500GB of parquet files, running on i3.xlarge cluster"
)
```

### analyze_job_health
Assess the overall health of a job based on run history, duration trends, and failure rates.

**When to use:** During weekly reviews or when investigating intermittent issues.

**Example:**
```
analyze_job_health(
    health_report="Last 30 runs: 25 success, 5 failed. Avg duration: 45min (was 30min last month). Failures all OOM.",
    context="Daily ETL job, cluster autoscales 2-8 nodes"
)
```

### analyze_costs
Analyze cost attribution data and suggest optimization opportunities.

**When to use:** During cost reviews or when spend exceeds expectations.

**Example:**
```
analyze_costs(
    cost_report="Top 5 jobs by DBU: Job A: 500 DBU/day, Job B: 300 DBU/day...",
    context="Account target is 20% cost reduction this quarter"
)
```

### analyze_query_performance
Analyze slow query statistics and suggest performance improvements.

**When to use:** When queries are running slowly or during performance tuning sessions.

**Example:**
```
analyze_query_performance(
    query_stats="Query duration: 45min. Scanned 2TB. Shuffle write: 500GB. Spill: 200GB.",
    context="SQL warehouse Medium size, query runs hourly"
)
```

## Common Workflows

### Post-Failure Investigation
1. Capture the full error text from the job run
2. Gather context (cluster config, data volumes, recent changes)
3. `diagnose_job_failure(error_text, context)` -- get root cause analysis
4. Apply recommended fixes
5. Monitor next runs

### Weekly Health Review
1. Build health report from run history (success rate, duration trend, failure patterns)
2. `analyze_job_health(health_report, context)` -- get health assessment
3. Prioritize issues by risk level
4. Create action items for high-risk findings

### Cost Optimization Sprint
1. Pull cost report by job/workspace/SKU
2. `analyze_costs(cost_report, context)` -- get optimization recommendations
3. Identify quick wins vs structural changes
4. Implement and track savings

### Query Tuning Session
1. Capture query stats from Query History or EXPLAIN output
2. `analyze_query_performance(query_stats, context)` -- get tuning advice
3. Apply SQL-level optimizations first
4. Consider warehouse sizing changes if needed

## Reference Files

- [diagnostic-patterns.md](diagnostic-patterns.md) -- Detailed diagnostic prompt patterns and tips
