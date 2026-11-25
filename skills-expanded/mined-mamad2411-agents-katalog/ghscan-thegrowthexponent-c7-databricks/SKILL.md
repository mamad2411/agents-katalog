---
title: "Analytics & Dashboards Skills"
description: "Business intelligence, dashboards, and data governance with system tables on Databricks"
category: "analytics"
tags:
  [
    "analytics",
    "dashboards",
    "bi",
    "genie",
    "system-tables",
    "unity-catalog",
    "governance",
    "monitoring",
    "cost-analysis",
  ]
priority: "high"
skills_count: 2
last_updated: 2026-02-27
version: "1.0.0"
status: "partial"
---

# Analytics & Dashboards Skills

This directory contains skills and patterns for analytics, dashboards, and data governance on Databricks.

## 📚 Skills Overview

### High Priority Skills

#### 1. Databricks AI/BI Dashboards

**Status**: ❌ Not yet documented
**Priority**: HIGH
**Description**: Create intelligent, AI-powered dashboards for business intelligence and analytics

**Key Topics**:

- Dashboard creation and design
- AI-powered insights generation
- Natural language queries in dashboards
- Genie integration for self-service analytics
- Interactive visualizations
- Dashboard sharing and permissions
- Scheduled dashboard refresh
- Dashboard performance optimization

**Use Cases**:

- Executive dashboards
- Operational reporting
- Self-service analytics for business users
- Real-time monitoring dashboards
- KPI tracking and alerting
- Department-specific analytics

**Prerequisites**:

- SQL Warehouse access
- Unity Catalog enabled
- Data tables prepared
- Basic SQL knowledge

**Related Documentation**:

- [SQL Examples](../../examples/sql.md)
- [Unity Catalog API](../../api/unity-catalog.md)
- [Query and Visualize Data](../../getting-started/query-visualize-data.md)

---

#### 2. Unity Catalog System Tables

**Status**: ⚠️ Partially documented
**Priority**: MEDIUM
**Description**: Leverage system tables for usage monitoring, audit, and governance

**Key Topics**:

- System table schema and structure
- Usage monitoring and analysis
- Audit log querying
- Billing and cost analysis
- Query performance analysis
- Access pattern tracking
- Data lineage exploration
- Compliance reporting

**Use Cases**:

- Cost attribution and chargeback
- Security audit and compliance
- Query performance optimization
- User activity monitoring
- Data usage analytics
- Capacity planning

**Prerequisites**:

- Unity Catalog metastore admin access
- SQL Warehouse configured
- Understanding of Unity Catalog concepts

**Enhancement Needed**:

- Add dedicated system tables guide
- Document common analysis queries
- Include cost monitoring examples
- Show lineage tracking patterns

**Related Documentation**:

- [Unity Catalog API](../../api/unity-catalog.md) ⚠️ Basic coverage only
- [SQL Examples](../../examples/sql.md)
- [Security Best Practices](../../best-practices/security.md)

---

## 🎯 Quick Start Examples

### Example 1: Create AI/BI Dashboard

```sql
-- Create a simple sales dashboard
-- This dashboard will use Genie for natural language queries

-- 1. Key Metrics Tile
SELECT
  COUNT(DISTINCT order_id) as total_orders,
  SUM(revenue) as total_revenue,
  AVG(revenue) as avg_order_value,
  COUNT(DISTINCT customer_id) as unique_customers
FROM main.sales.orders
WHERE order_date >= CURRENT_DATE - INTERVAL 30 DAYS;

-- 2. Revenue Trend (Line Chart)
SELECT
  DATE_TRUNC('day', order_date) as date,
  SUM(revenue) as daily_revenue,
  COUNT(order_id) as order_count
FROM main.sales.orders
WHERE order_date >= CURRENT_DATE - INTERVAL 90 DAYS
GROUP BY DATE_TRUNC('day', order_date)
ORDER BY date;

-- 3. Top Products (Bar Chart)
SELECT
  product_name,
  SUM(quantity) as units_sold,
  SUM(revenue) as total_revenue
FROM main.sales.order_items oi
JOIN main.sales.products p ON oi.product_id = p.product_id
WHERE order_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY product_name
ORDER BY total_revenue DESC
LIMIT 10;

-- 4. Regional Performance (Map)
SELECT
  region,
  country,
  SUM(revenue) as revenue,
  COUNT(DISTINCT customer_id) as customers
FROM main.sales.orders
WHERE order_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY region, country;

-- 5. Customer Segments (Pie Chart)
SELECT
  customer_segment,
  COUNT(DISTINCT customer_id) as customer_count,
  SUM(revenue) as segment_revenue
FROM main.sales.orders
WHERE order_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY customer_segment;
```

### Example 2: Query System Tables for Usage Monitoring

```sql
-- Monitor workspace usage patterns

-- 1. Query execution statistics
SELECT
  DATE(statement_execution_start_timestamp) as date,
  user_name,
  COUNT(*) as query_count,
  SUM(execution_duration_ms) / 1000 / 60 as total_minutes,
  AVG(execution_duration_ms) / 1000 as avg_seconds,
  SUM(read_bytes) / 1024 / 1024 / 1024 as total_gb_read
FROM system.query.history
WHERE statement_execution_start_timestamp >= CURRENT_DATE - INTERVAL 7 DAYS
  AND statement_type = 'SELECT'
GROUP BY DATE(statement_execution_start_timestamp), user_name
ORDER BY date DESC, query_count DESC;

-- 2. Most expensive queries
SELECT
  statement_id,
  user_name,
  warehouse_name,
  statement_text,
  execution_duration_ms / 1000 as duration_seconds,
  read_bytes / 1024 / 1024 / 1024 as gb_read,
  rows_produced,
  error_message
FROM system.query.history
WHERE statement_execution_start_timestamp >= CURRENT_DATE - INTERVAL 1 DAYS
  AND execution_duration_ms > 60000  -- More than 1 minute
ORDER BY execution_duration_ms DESC
LIMIT 20;

-- 3. Table access patterns
SELECT
  table_catalog,
  table_schema,
  table_name,
  COUNT(DISTINCT statement_id) as query_count,
  COUNT(DISTINCT user_name) as unique_users,
  SUM(rows_read) as total_rows_read,
  MAX(statement_execution_start_timestamp) as last_accessed
FROM system.access.table_lineage
WHERE event_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY table_catalog, table_schema, table_name
ORDER BY query_count DESC
LIMIT 50;
```

### Example 3: Cost Analysis with System Tables

```sql
-- Analyze compute costs and usage

-- 1. Warehouse cost breakdown by user
SELECT
  warehouse_name,
  user_name,
  COUNT(*) as query_count,
  SUM(execution_duration_ms) / 1000 / 3600 as total_compute_hours,
  -- Estimate cost (adjust rate for your pricing)
  SUM(execution_duration_ms) / 1000 / 3600 * 0.22 as estimated_cost_usd
FROM system.query.history
WHERE statement_execution_start_timestamp >= CURRENT_DATE - INTERVAL 30 DAYS
  AND warehouse_name IS NOT NULL
GROUP BY warehouse_name, user_name
ORDER BY estimated_cost_usd DESC;

-- 2. Daily cost trends
SELECT
  DATE(statement_execution_start_timestamp) as date,
  warehouse_name,
  COUNT(DISTINCT user_name) as active_users,
  COUNT(*) as total_queries,
  SUM(execution_duration_ms) / 1000 / 3600 as compute_hours,
  SUM(execution_duration_ms) / 1000 / 3600 * 0.22 as estimated_cost_usd
FROM system.query.history
WHERE statement_execution_start_timestamp >= CURRENT_DATE - INTERVAL 90 DAYS
GROUP BY DATE(statement_execution_start_timestamp), warehouse_name
ORDER BY date DESC, compute_hours DESC;

-- 3. Cluster usage and costs
SELECT
  cluster_name,
  workspace_name,
  DATE(usage_start_time) as date,
  SUM(usage_quantity) as dbu_consumed,
  -- Estimate cost (adjust DBU price for your pricing)
  SUM(usage_quantity) * 0.15 as estimated_cost_usd
FROM system.billing.usage
WHERE usage_date >= CURRENT_DATE - INTERVAL 30 DAYS
  AND sku_name LIKE '%All-Purpose%'
GROUP BY cluster_name, workspace_name, DATE(usage_start_time)
ORDER BY estimated_cost_usd DESC;
```

### Example 4: Audit and Compliance Queries

```sql
-- Security and compliance monitoring

-- 1. Track access to sensitive tables
SELECT
  event_time,
  user_identity.email as user_email,
  request_params.full_name_arg as table_name,
  action_name,
  request_params,
  response.status_code
FROM system.access.audit
WHERE action_name IN ('getTable', 'readTable', 'listTables')
  AND request_params.full_name_arg LIKE '%sensitive%'
  AND event_date >= CURRENT_DATE - INTERVAL 7 DAYS
ORDER BY event_time DESC;

-- 2. Permission changes audit
SELECT
  event_time,
  user_identity.email as changed_by,
  action_name,
  request_params.securable_type as object_type,
  request_params.securable_full_name as object_name,
  request_params.principal as granted_to,
  request_params.changes as permission_changes
FROM system.access.audit
WHERE action_name IN ('updatePermissions', 'createGrant', 'revokeGrant')
  AND event_date >= CURRENT_DATE - INTERVAL 30 DAYS
ORDER BY event_time DESC;

-- 3. Failed access attempts
SELECT
  event_time,
  user_identity.email as user_email,
  action_name,
  request_params.full_name_arg as resource,
  response.status_code,
  response.error_message
FROM system.access.audit
WHERE response.status_code >= 400
  AND event_date >= CURRENT_DATE - INTERVAL 7 DAYS
ORDER BY event_time DESC
LIMIT 100;

-- 4. Data export tracking
SELECT
  event_time,
  user_identity.email as user_email,
  action_name,
  request_params.path as export_path,
  request_params.format as export_format,
  response.result.bytes_exported
FROM system.access.audit
WHERE action_name IN ('export', 'download', 'dbfsWrite')
  AND event_date >= CURRENT_DATE - INTERVAL 30 DAYS
ORDER BY event_time DESC;
```

### Example 5: Data Lineage Analysis

```sql
-- Understand data lineage and dependencies

-- 1. Find downstream dependencies of a table
WITH RECURSIVE lineage AS (
  -- Base case: direct dependencies
  SELECT
    source_table_full_name,
    target_table_full_name,
    1 as depth
  FROM system.access.table_lineage
  WHERE source_table_full_name = 'main.bronze.raw_events'
    AND event_date >= CURRENT_DATE - INTERVAL 30 DAYS

  UNION ALL

  -- Recursive case: indirect dependencies
  SELECT
    tl.source_table_full_name,
    tl.target_table_full_name,
    l.depth + 1
  FROM system.access.table_lineage tl
  INNER JOIN lineage l ON tl.source_table_full_name = l.target_table_full_name
  WHERE l.depth < 5  -- Limit recursion depth
    AND tl.event_date >= CURRENT_DATE - INTERVAL 30 DAYS
)
SELECT DISTINCT
  target_table_full_name as downstream_table,
  MAX(depth) as dependency_depth
FROM lineage
GROUP BY target_table_full_name
ORDER BY dependency_depth, target_table_full_name;

-- 2. Find upstream sources for a table
SELECT DISTINCT
  source_table_full_name as upstream_table,
  COUNT(DISTINCT statement_id) as usage_count,
  MAX(event_time) as last_used
FROM system.access.table_lineage
WHERE target_table_full_name = 'main.gold.customer_analytics'
  AND event_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY source_table_full_name
ORDER BY usage_count DESC;

-- 3. Column-level lineage
SELECT
  source_table_full_name,
  source_column_name,
  target_table_full_name,
  target_column_name,
  COUNT(DISTINCT statement_id) as transformation_count
FROM system.access.column_lineage
WHERE target_table_full_name = 'main.gold.customer_analytics'
  AND event_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY
  source_table_full_name,
  source_column_name,
  target_table_full_name,
  target_column_name
ORDER BY source_table_full_name, source_column_name;
```

### Example 6: Performance Monitoring Dashboard

```sql
-- Query performance metrics for dashboard

-- 1. Query performance over time
SELECT
  DATE_TRUNC('hour', statement_execution_start_timestamp) as hour,
  COUNT(*) as query_count,
  AVG(execution_duration_ms) / 1000 as avg_duration_seconds,
  PERCENTILE(execution_duration_ms / 1000, 0.50) as p50_seconds,
  PERCENTILE(execution_duration_ms / 1000, 0.95) as p95_seconds,
  PERCENTILE(execution_duration_ms / 1000, 0.99) as p99_seconds
FROM system.query.history
WHERE statement_execution_start_timestamp >= CURRENT_TIMESTAMP - INTERVAL 24 HOURS
GROUP BY DATE_TRUNC('hour', statement_execution_start_timestamp)
ORDER BY hour DESC;

-- 2. Warehouse performance comparison
SELECT
  warehouse_name,
  COUNT(*) as total_queries,
  AVG(execution_duration_ms) / 1000 as avg_duration_seconds,
  SUM(CASE WHEN error_message IS NOT NULL THEN 1 ELSE 0 END) as failed_queries,
  AVG(rows_produced) as avg_rows_produced,
  AVG(read_bytes) / 1024 / 1024 as avg_mb_read
FROM system.query.history
WHERE statement_execution_start_timestamp >= CURRENT_DATE - INTERVAL 7 DAYS
GROUP BY warehouse_name
ORDER BY total_queries DESC;

-- 3. Slow query patterns
SELECT
  REGEXP_EXTRACT(statement_text, '^(SELECT|INSERT|UPDATE|DELETE|MERGE|CREATE)', 1) as query_type,
  CASE
    WHEN statement_text LIKE '%JOIN%JOIN%JOIN%' THEN 'Multiple JOINs'
    WHEN statement_text LIKE '%DISTINCT%' THEN 'DISTINCT'
    WHEN statement_text LIKE '%GROUP BY%' THEN 'Aggregation'
    WHEN statement_text LIKE '%ORDER BY%' THEN 'Sorting'
    ELSE 'Other'
  END as query_pattern,
  COUNT(*) as occurrence_count,
  AVG(execution_duration_ms) / 1000 as avg_duration_seconds,
  AVG(read_bytes) / 1024 / 1024 / 1024 as avg_gb_read
FROM system.query.history
WHERE statement_execution_start_timestamp >= CURRENT_DATE - INTERVAL 7 DAYS
  AND execution_duration_ms > 30000  -- Queries over 30 seconds
GROUP BY
  REGEXP_EXTRACT(statement_text, '^(SELECT|INSERT|UPDATE|DELETE|MERGE|CREATE)', 1),
  CASE
    WHEN statement_text LIKE '%JOIN%JOIN%JOIN%' THEN 'Multiple JOINs'
    WHEN statement_text LIKE '%DISTINCT%' THEN 'DISTINCT'
    WHEN statement_text LIKE '%GROUP BY%' THEN 'Aggregation'
    WHEN statement_text LIKE '%ORDER BY%' THEN 'Sorting'
    ELSE 'Other'
  END
ORDER BY avg_duration_seconds DESC;
```

---

## 🔧 Common Patterns

### Pattern 1: Real-Time Dashboard with Auto-Refresh

```sql
-- Create a live monitoring dashboard
-- Set refresh interval to 1 minute in dashboard settings

-- Active users in last 5 minutes
SELECT
  COUNT(DISTINCT user_name) as active_users,
  COUNT(*) as queries_running,
  SUM(execution_duration_ms) / 1000 / 60 as total_compute_minutes
FROM system.query.history
WHERE statement_execution_start_timestamp >= CURRENT_TIMESTAMP - INTERVAL 5 MINUTES;

-- Currently running queries
SELECT
  statement_id,
  user_name,
  warehouse_name,
  statement_execution_start_timestamp,
  TIMESTAMPDIFF(SECOND, statement_execution_start_timestamp, CURRENT_TIMESTAMP) as running_seconds,
  LEFT(statement_text, 100) as query_preview
FROM system.query.history
WHERE state = 'RUNNING'
ORDER BY statement_execution_start_timestamp;
```

### Pattern 2: Executive Summary Dashboard

```sql
-- High-level KPIs for executives

-- 1. Platform adoption metrics
SELECT
  'Total Users' as metric,
  COUNT(DISTINCT user_name) as value,
  NULL as trend
FROM system.query.history
WHERE statement_execution_start_timestamp >= CURRENT_DATE - INTERVAL 30 DAYS

UNION ALL

SELECT
  'Active Workspaces' as metric,
  COUNT(DISTINCT workspace_id) as value,
  NULL as trend
FROM system.billing.usage
WHERE usage_date >= CURRENT_DATE - INTERVAL 30 DAYS

UNION ALL

SELECT
  'Tables Created' as metric,
  COUNT(DISTINCT table_full_name) as value,
  NULL as trend
FROM system.access.table_lineage
WHERE event_date >= CURRENT_DATE - INTERVAL 30 DAYS;

-- 2. Cost trends
SELECT
  DATE_TRUNC('month', usage_date) as month,
  SUM(usage_quantity * list_price) as total_cost
FROM system.billing.usage
WHERE usage_date >= CURRENT_DATE - INTERVAL 12 MONTHS
GROUP BY DATE_TRUNC('month', usage_date)
ORDER BY month;
```

### Pattern 3: Data Quality Dashboard

```sql
-- Monitor data quality metrics

-- 1. Table freshness
SELECT
  table_catalog,
  table_schema,
  table_name,
  MAX(event_time) as last_updated,
  TIMESTAMPDIFF(HOUR, MAX(event_time), CURRENT_TIMESTAMP) as hours_since_update
FROM system.access.table_lineage
WHERE event_date >= CURRENT_DATE - INTERVAL 7 DAYS
  AND table_catalog = 'main'
  AND table_schema IN ('silver', 'gold')
GROUP BY table_catalog, table_schema, table_name
HAVING hours_since_update > 24  -- Tables not updated in 24 hours
ORDER BY hours_since_update DESC;

-- 2. Failed pipeline runs
SELECT
  DATE(event_time) as date,
  request_params.job_name as job_name,
  COUNT(*) as failure_count,
  COLLECT_SET(response.error_message) as error_messages
FROM system.access.audit
WHERE action_name = 'runFailed'
  AND event_date >= CURRENT_DATE - INTERVAL 7 DAYS
GROUP BY DATE(event_time), request_params.job_name
ORDER BY date DESC, failure_count DESC;
```

### Pattern 4: Genie Space Integration

```python
# Python code to interact with Genie programmatically
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.dashboards import GenieSpace

w = WorkspaceClient()

# Create a Genie Space
genie_space = w.genie.create(
    display_name="Sales Analytics Genie",
    description="Natural language interface for sales data",
    warehouse_id="abc123",
    tables=[
        "main.sales.orders",
        "main.sales.customers",
        "main.sales.products"
    ],
    instructions="Focus on revenue, customer segments, and product performance. "
                "Always filter to the last 90 days unless specified otherwise."
)

print(f"Created Genie Space: {genie_space.id}")

# Ask a question
response = w.genie.ask_question(
    space_id=genie_space.id,
    question="What are our top 5 products by revenue this month?"
)

print(f"SQL Generated: {response.sql}")
print(f"Results: {response.results}")
```

---

## 📊 Best Practices

### Dashboard Design

1. **User-Focused Design**
   - Identify your audience (executives, analysts, operations)
   - Prioritize key metrics above the fold
   - Use clear, descriptive titles and labels
   - Provide context with comparison periods

2. **Performance Optimization**
   - Pre-aggregate data where possible
   - Use materialized views for complex calculations
   - Set appropriate refresh intervals
   - Limit result set sizes with filters
   - Cache frequently accessed queries

3. **Visual Best Practices**
   - Choose appropriate chart types
   - Use consistent color schemes
   - Avoid chart junk and clutter
   - Make dashboards mobile-friendly
   - Add interactive filters

### System Tables Usage

1. **Query Optimization**
   - Always filter by date partitions
   - Use specific columns instead of SELECT \*
   - Leverage predicate pushdown
   - Sample large result sets when exploring

2. **Access Control**
   - Limit access to audit tables
   - Use views to expose filtered data
   - Document sensitive data handling
   - Implement row-level security where needed

3. **Monitoring Strategy**
   - Set up alerts for anomalies
   - Track trends over time
   - Create baseline metrics
   - Schedule regular reports

### Cost Management

1. **Resource Optimization**
   - Right-size SQL Warehouses
   - Use serverless warehouses for variable workloads
   - Enable auto-scaling and auto-suspend
   - Monitor query efficiency

2. **Chargeback & Attribution**
   - Tag resources by team/project
   - Track usage by user and department
   - Create cost allocation reports
   - Identify optimization opportunities

3. **Budget Alerts**
   - Set spending thresholds
   - Monitor daily cost trends
   - Alert on unusual usage patterns
   - Review top cost drivers weekly

---

## 🚀 Getting Started Checklist

### For AI/BI Dashboards

- [ ] Enable Databricks SQL in workspace
- [ ] Create or select SQL Warehouse
- [ ] Prepare source tables in Unity Catalog
- [ ] Create first dashboard with basic queries
- [ ] Add visualizations (charts, tables, counters)
- [ ] Configure dashboard refresh schedule
- [ ] Set up dashboard permissions
- [ ] Create Genie Space for natural language queries
- [ ] Test with business users
- [ ] Gather feedback and iterate

### For System Tables Analysis

- [ ] Verify Unity Catalog metastore access
- [ ] Locate system catalog in SQL editor
- [ ] Explore available system schemas (access, billing, query)
- [ ] Create queries for key metrics
- [ ] Build monitoring dashboard
- [ ] Set up alerts for anomalies
- [ ] Document query patterns
- [ ] Share with stakeholders

### For Cost Monitoring

- [ ] Access system.billing.usage table
- [ ] Identify your DBU pricing
- [ ] Create cost analysis queries
- [ ] Build cost dashboard
- [ ] Set up daily cost reports
- [ ] Create budget alerts
- [ ] Implement chargeback process
- [ ] Review optimization opportunities

---

## 🔍 Advanced Topics

### Custom System Table Views

```sql
-- Create reusable views on system tables

-- View: Daily cost by team
CREATE OR REPLACE VIEW main.analytics.daily_costs_by_team AS
SELECT
  DATE(usage_start_time) as date,
  workspace_name,
  COALESCE(tags.team, 'Untagged') as team,
  SUM(usage_quantity) as dbu_consumed,
  SUM(usage_quantity * list_price) as total_cost
FROM system.billing.usage
WHERE usage_date >= CURRENT_DATE - INTERVAL 90 DAYS
GROUP BY
  DATE(usage_start_time),
  workspace_name,
  COALESCE(tags.team, 'Untagged');

-- View: Query performance summary
CREATE OR REPLACE VIEW main.analytics.query_performance_summary AS
SELECT
  warehouse_name,
  user_name,
  DATE(statement_execution_start_timestamp) as date,
  COUNT(*) as query_count,
  AVG(execution_duration_ms) / 1000 as avg_duration_seconds,
  PERCENTILE(execution_duration_ms / 1000, 0.95) as p95_duration_seconds,
  SUM(read_bytes) / 1024 / 1024 / 1024 as total_gb_read
FROM system.query.history
WHERE statement_execution_start_timestamp >= CURRENT_DATE - INTERVAL 90 DAYS
GROUP BY
  warehouse_name,
  user_name,
  DATE(statement_execution_start_timestamp);
```

### Alerting with System Tables

```python
# Create alerts based on system table queries
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

# Create alert for high query failures
alert = w.alerts.create(
    name="High Query Failure Rate",
    options={
        "query_id": "query_id_here",
        "column": "failure_rate",
        "op": "greater than",
        "value": 10
    },
    rearm=3600  # Re-arm after 1 hour
)

# Add notification destination
w.alerts.subscribe(
    alert_id=alert.id,
    destination_type="email",
    destination="team@company.com"
)
```

### Advanced Lineage Tracking

```sql
-- Track full data lineage with transformations

WITH source_to_target AS (
  SELECT
    source_table_full_name,
    target_table_full_name,
    source_column_name,
    target_column_name,
    statement_text,
    user_name,
    event_time
  FROM system.access.column_lineage
  WHERE event_date >= CURRENT_DATE - INTERVAL 7 DAYS
    AND target_table_full_name = 'main.gold.customer_360'
)
SELECT
  source_table_full_name,
  source_column_name,
  target_column_name,
  COUNT(DISTINCT statement_id) as transformation_count,
  COLLECT_SET(user_name) as contributors,
  MAX(event_time) as last_transformation
FROM source_to_target
GROUP BY
  source_table_full_name,
  source_column_name,
  target_column_name
ORDER BY transformation_count DESC;
```

---

## 📖 Additional Resources

### Official Documentation

- [Databricks SQL Dashboards](https://docs.databricks.com/en/dashboards/index.html)
- [AI/BI Dashboards](https://docs.databricks.com/en/dashboards/ai-bi-dashboards.html)
- [Genie Spaces](https://docs.databricks.com/en/genie/index.html)
- [System Tables Reference](https://docs.databricks.com/en/admin/system-tables/index.html)
- [Unity Catalog Audit Logs](https://docs.databricks.com/en/admin/system-tables/audit-logs.html)

### Tutorials

- [Query and Visualize Data](../../getting-started/query-visualize-data.md)
- [SQL Examples](../../examples/sql.md)
- [Create Table Tutorial](../../getting-started/create-table-tutorial.md)

### API References

- [Unity Catalog API](../../api/unity-catalog.md)
- [SQL Warehouse Management](../../api/overview.md)
- [Python SDK](../../sdk/python.md)

---

## 🏷️ Tags

`dashboards` `analytics` `bi` `genie` `system-tables` `monitoring` `cost-analysis` `audit` `compliance` `lineage` `sql` `visualization` `reporting`

---

**Last Updated**: 2026-01-15
**Status**: AI/BI Dashboards need detailed guide - System tables partially covered
**Maintainer**: Context7 Documentation Team
