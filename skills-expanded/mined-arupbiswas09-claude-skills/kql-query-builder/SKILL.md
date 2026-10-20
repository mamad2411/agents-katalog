---
name: kql-query-builder
description: Write, explain, and optimise Kusto Query Language (KQL) queries for Azure Log Analytics, Application Insights, and Azure Monitor.
---

# KQL Query Builder

Write, explain, and optimise Kusto Query Language (KQL) queries for Azure Log Analytics, Application Insights, and Azure Monitor.

## Trigger

Use this skill when the user asks to:
- Write or generate a KQL query
- Debug or fix a failing/slow KQL query
- Explain what a KQL query does
- Optimise query performance
- Find logs, traces, exceptions, metrics, or alerts in Azure
- Query specific tables: `AzureDiagnostics`, `AppRequests`, `AppExceptions`, `Heartbeat`, `ContainerLog`, `SecurityEvent`, `AuditLogs`, `SigninLogs`, `Perf`, `Usage`, etc.

## Instructions

### Before writing a query

Ask (or infer from context) the following if not already provided:

1. **Target service** — Log Analytics workspace, Application Insights, or Azure Monitor Metrics?
2. **Time range** — default to `last 24h` (`ago(24h)`) if unspecified
3. **What to find** — errors, latency, a specific operation, a resource, a user, a correlation ID?
4. **Output shape** — raw rows, aggregated counts, a time-series chart, a top-N list?

### Query construction rules

Always follow this order of operators for readability and performance:

```
TableName
| where  (filter first — reduces row count early)
| where  (additional filters on the same pass when possible)
| extend (computed columns)
| summarize (aggregations)
| order by / top
| project (select only needed columns — always last)
```

**Performance rules (apply to every query):**
- Put the most selective `where` clause first
- Prefer `has` over `contains` for string matching (uses the index)
- Prefer `==` over `=~` when case sensitivity is acceptable
- Avoid `*` in `project` — name columns explicitly
- Use `materialize()` when the same subquery is referenced more than once
- For large tables, always filter on `TimeGenerated` before any other column
- Prefer `summarize ... by bin(TimeGenerated, 5m)` over looping client-side

**Correctness rules:**
- Wrap column names with spaces in `['Column Name']`
- Use `isnotempty()` not `!= ""`
- Use `toint()`, `toreal()`, `todatetime()` for explicit casts rather than implicit coercion
- In Application Insights queries use `union isfuzzy=true` when spanning multiple resources
- Use `let` statements to define reusable sub-expressions and make intent clear

### Output format

Return:
1. The query in a fenced KQL code block
2. A brief explanation (one sentence per operator) so the user can adapt it
3. Any caveats (permissions needed, table retention limits, sampling effects in Application Insights, etc.)

When the user wants a **parameterised** query, use `let` variables at the top:

```kql
let _timeRange = 24h;
let _resourceGroup = "my-rg";
// ... rest of query
```

### Common patterns

**Error rate over time**
```kql
AppRequests
| where TimeGenerated > ago(1h)
| summarize
    Total = count(),
    Errors = countif(Success == false)
    by bin(TimeGenerated, 5m)
| extend ErrorRate = round(100.0 * Errors / Total, 2)
| order by TimeGenerated asc
```

**Slowest operations (p95 latency)**
```kql
AppRequests
| where TimeGenerated > ago(24h)
| summarize
    p50 = percentile(DurationMs, 50),
    p95 = percentile(DurationMs, 95),
    p99 = percentile(DurationMs, 99),
    RequestCount = count()
    by Name
| order by p95 desc
| take 20
```

**Exception details with correlation**
```kql
AppExceptions
| where TimeGenerated > ago(6h)
| where OuterType has "ArgumentNullException" or SeverityLevel >= 3
| project TimeGenerated, OperationId, OuterType, OuterMessage, Assembly, FileName, LineNumber
| order by TimeGenerated desc
```

**Kubernetes pod restarts (Container Insights)**
```kql
KubePodInventory
| where TimeGenerated > ago(1h)
| where RestartCount > 0
| summarize MaxRestarts = max(RestartCount) by Name, Namespace, bin(TimeGenerated, 5m)
| order by MaxRestarts desc
```

**Azure AD sign-in failures**
```kql
SigninLogs
| where TimeGenerated > ago(24h)
| where ResultType != "0"
| summarize FailureCount = count() by UserPrincipalName, ResultDescription, AppDisplayName
| order by FailureCount desc
| take 50
```

**Resource health events**
```kql
AzureActivity
| where TimeGenerated > ago(7d)
| where ActivityStatusValue in ("Failed", "Critical")
| project TimeGenerated, OperationNameValue, ResourceGroup, ResourceId, Caller, ActivityStatusValue, Properties
| order by TimeGenerated desc
```

**Alert rule — threshold over 5-minute window**
```kql
Perf
| where TimeGenerated > ago(5m)
| where ObjectName == "Processor" and CounterName == "% Processor Time"
| where InstanceName == "_Total"
| summarize AvgCPU = avg(CounterValue) by Computer
| where AvgCPU > 85
```

### Explaining an existing query

When the user pastes a query and asks what it does:
1. Identify the source table and the data domain
2. Walk through each operator in order, one sentence each
3. State what the final output shape is (columns, sort order, row limit)
4. Flag any performance or correctness concerns

### Debugging a query

When the user reports an error or unexpected results:
1. Check operator order (filter → aggregate → project)
2. Verify column name casing (KQL column names are case-sensitive)
3. Check time range — `ago()` is relative to query execution time
4. Check for implicit type mismatches (string vs. int comparisons)
5. Suggest `take 10` on intermediate steps to inspect intermediate rows
6. For "no results": relax filters one by one to find where data disappears

## References

- [KQL quick reference](./references/kql-cheatsheet.md)
- [Common Log Analytics tables](./references/log-analytics-tables.md)
- [Query performance patterns](./references/performance-patterns.md)
- Official docs: https://learn.microsoft.com/en-us/azure/data-explorer/kusto/query/
