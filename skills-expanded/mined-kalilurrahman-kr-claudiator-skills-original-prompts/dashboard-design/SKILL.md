---
name: dashboard-design
description: Design analytics dashboards with Tableau, PowerBI, Looker, Metabase. Outputs metric definitions, visualizations, filters, and user flows.
argument-hint: [metrics, audience, update frequency]
allowed-tools: Read, Write, Bash
---

# Dashboard Design

Design effective analytics dashboards for business users. Not chart dumps — purposeful metrics, clear visualizations, and actionable insights.

## Process

1. **Define audience.** Executives, analysts, operations, customers.
2. **Identify metrics.** Key KPIs, supporting metrics, drill-down dimensions.
3. **Choose layout.** Overview → Details, metric cards → charts → tables.
4. **Select visualizations.** Bar charts, line charts, heatmaps based on data type.
5. **Add interactivity.** Filters, drill-through, time period selectors.
6. **Optimize performance.** Pre-aggregation, caching, incremental refresh.
7. **Test with users.** Validate metrics match business questions.

## Output Format

### Dashboard: [Business Function]

**Tool:** Looker  
**Metrics:** 12 KPIs, 8 supporting metrics  
**Update Frequency:** Hourly (incremental)  
**Users:** 50 (sales team)  
**Performance:** < 3 second load time

---

## Dashboard Hierarchy

```
Level 1: Executive Summary
├─ 4-6 key metrics (revenue, users, conversion)
├─ Trend indicators (▲12% vs last month)
└─ High-level charts (sparklines, trend lines)

Level 2: Department View
├─ Metric breakdowns (by region, product, team)
├─ Comparison charts (actual vs target)
└─ Filters (date range, segment)

Level 3: Operational Detail
├─ Detailed tables (transactions, users)
├─ Drill-through to individual records
└─ Export capabilities
```

---

## Metric Card Design

### Good Metric Card
```
┌─────────────────────────┐
│ Monthly Revenue         │
│                         │
│ $1.2M  ▲ 12.5%         │
│        vs last month    │
│                         │
│ [Sparkline trend]       │
│                         │
│ Target: $1.1M ✅        │
└─────────────────────────┘

Elements:
- Clear label
- Big number
- Trend indicator (▲▼)
- Context (vs comparison)
- Mini visualization
- Target/benchmark
```

### Bad Metric Card
```
┌─────────────────────────┐
│ Rev                     │
│ 1234567.89             │
│ +0.125                 │
└─────────────────────────┘

Problems:
- Unclear abbreviation
- No formatting ($1.2M)
- Confusing percentage (0.125 = 12.5%?)
- No context
```

---

## Chart Selection

### Time Series → Line Chart
```
Use for: Trends over time
Example: Daily active users, revenue by month

When to use:
- Continuous data
- Show changes over time
- Compare multiple series
```

### Comparison → Bar Chart
```
Use for: Comparing categories
Example: Revenue by product, sales by region

When to use:
- Categorical data
- Ranking (top 10)
- Part-to-whole (stacked bars)
```

### Distribution → Histogram
```
Use for: Frequency distribution
Example: Order value distribution, user age ranges

When to use:
- Show data spread
- Identify outliers
- Normal vs skewed
```

### Correlation → Scatter Plot
```
Use for: Relationship between variables
Example: Marketing spend vs revenue, price vs conversion

When to use:
- Two continuous variables
- Identify clusters
- Show outliers
```

### Part-to-Whole → Pie Chart (Use Sparingly!)
```
Use for: Proportion of total (max 5 slices)
Example: Market share, traffic sources

Better alternative: Bar chart (easier to compare)
```

### Geographic → Map
```
Use for: Location-based data
Example: Sales by state, user density

When to use:
- Spatial patterns
- Regional comparison
```

---

## Dashboard Layouts

### Executive Dashboard
```
┌────────────────────────────────────────────┐
│ Revenue         Users        Conversion    │
│ $1.2M ▲12%     50K ▲8%      2.5% ▼3%      │
│ [spark][spark][spark]                      │
└────────────────────────────────────────────┘

┌──────────────────┐ ┌──────────────────────┐
│ Revenue Trend    │ │ User Growth          │
│ [Line chart]     │ │ [Area chart]         │
└──────────────────┘ └──────────────────────┘

┌────────────────────────────────────────────┐
│ Top Products (Revenue)                     │
│ [Horizontal bar chart]                     │
└────────────────────────────────────────────┘
```

### Operational Dashboard
```
┌────────────────────────────────────────────┐
│ Filters: [Date Range] [Region] [Product]  │
└────────────────────────────────────────────┘

┌──────────────────┐ ┌──────────────────────┐
│ Daily Orders     │ │ Order Status         │
│ [Line chart]     │ │ [Stacked bar]        │
└──────────────────┘ └──────────────────────┘

┌────────────────────────────────────────────┐
│ Recent Orders (Details)                    │
│ ID | Customer | Amount | Status | Date     │
│ [Sortable table with pagination]           │
└────────────────────────────────────────────┘
```

---

## Looker/LookML Example

```lookml
# Revenue dashboard view
view: revenue_metrics {
  derived_table: {
    sql:
      SELECT
        DATE_TRUNC('day', order_date) AS date,
        SUM(order_amount) AS revenue,
        COUNT(DISTINCT order_id) AS orders,
        COUNT(DISTINCT customer_id) AS customers,
        SUM(order_amount) / COUNT(DISTINCT order_id) AS avg_order_value
      FROM orders
      WHERE order_date >= CURRENT_DATE - INTERVAL '90 days'
      GROUP BY 1
    ;;
  }
  
  dimension_group: date {
    type: time
    timeframes: [date, week, month]
    sql: ${TABLE}.date ;;
  }
  
  measure: total_revenue {
    type: sum
    sql: ${TABLE}.revenue ;;
    value_format_name: usd_0
  }
  
  measure: avg_daily_revenue {
    type: average
    sql: ${TABLE}.revenue ;;
    value_format_name: usd_0
  }
}

# Dashboard
dashboard: revenue_overview {
  title: "Revenue Overview"
  
  elements: [
    {
      title: "Total Revenue (Last 30 Days)"
      type: single_value
      query: {
        model: analytics
        explore: revenue_metrics
        measures: [total_revenue]
        filters: {
          date: "30 days"
        }
      }
    },
    {
      title: "Revenue Trend"
      type: line
      query: {
        model: analytics
        explore: revenue_metrics
        dimensions: [date]
        measures: [total_revenue]
        filters: {
          date: "90 days"
        }
      }
    }
  ]
}
```

---

## Metabase SQL Dashboard

```sql
-- Metric: Monthly Recurring Revenue
SELECT
  DATE_TRUNC('month', subscription_start) AS month,
  SUM(monthly_price) AS mrr,
  COUNT(DISTINCT user_id) AS subscribers
FROM subscriptions
WHERE status = 'active'
  AND subscription_start >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '12 months')
GROUP BY 1
ORDER BY 1 DESC

-- Metric: Churn Rate
SELECT
  DATE_TRUNC('month', cancelled_date) AS month,
  COUNT(*) AS churned_customers,
  ROUND(
    COUNT(*)::NUMERIC / 
    LAG(COUNT(*)) OVER (ORDER BY DATE_TRUNC('month', cancelled_date)) * 100,
    2
  ) AS churn_rate_pct
FROM subscriptions
WHERE status = 'cancelled'
  AND cancelled_date >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '12 months')
GROUP BY 1
ORDER BY 1 DESC
```

---

## Interactive Filters

### Date Range Selector
```sql
-- Parameterized query in Metabase
SELECT
  product_name,
  SUM(revenue) AS total_revenue
FROM sales
WHERE sale_date BETWEEN {{start_date}} AND {{end_date}}
GROUP BY product_name
ORDER BY total_revenue DESC
LIMIT 10

-- Parameters:
-- start_date: Date field
-- end_date: Date field
```

### Multi-Select Filter
```sql
-- Filter by multiple regions
SELECT
  region,
  product_category,
  SUM(revenue) AS revenue
FROM sales
WHERE region IN ({{regions}})
  AND sale_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY region, product_category

-- Parameter:
-- regions: Field filter on sales.region (multi-select)
```

---

## Performance Optimization

### Pre-Aggregation
```sql
-- Create materialized view for fast dashboard queries
CREATE MATERIALIZED VIEW daily_revenue_summary AS
SELECT
  DATE(order_date) AS date,
  product_id,
  region,
  SUM(order_amount) AS revenue,
  COUNT(*) AS order_count,
  AVG(order_amount) AS avg_order_value
FROM orders
GROUP BY 1, 2, 3;

-- Refresh nightly
CREATE INDEX ON daily_revenue_summary (date, region);

-- Query uses summary (fast)
SELECT
  region,
  SUM(revenue) AS total_revenue
FROM daily_revenue_summary
WHERE date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY region;
```

### Incremental Refresh
```python
# Update only new data
import pandas as pd
from datetime import datetime, timedelta

def incremental_refresh():
    # Get last refresh timestamp
    last_refresh = get_last_refresh_time()
    
    # Query only new data
    new_data = query_database(f"""
        SELECT * FROM orders
        WHERE updated_at > '{last_refresh}'
    """)
    
    # Append to existing data
    append_to_dashboard_data(new_data)
    
    # Update refresh timestamp
    set_last_refresh_time(datetime.now())
```

---

## Drill-Through & Drill-Down

### Drill-Down (Hierarchy)
```
Revenue by Region
  ↓ (click region)
Revenue by Store
  ↓ (click store)
Revenue by Product
```

### Drill-Through (Related View)
```
Product Revenue Dashboard
  ↓ (click product)
Product Detail Page
  - Stock levels
  - Recent orders
  - Customer reviews
```

**Implementation (Looker):**
```lookml
measure: revenue {
  type: sum
  sql: ${TABLE}.revenue ;;
  
  drill_fields: [
    region,
    store_name,
    product_name,
    revenue
  ]
}
```

---

## Dashboard Refresh Strategies

### Real-Time (< 1 minute)
```
Use for: Live monitoring, alerts
Data source: Streaming (Kafka → Flink → Dashboard)
Cost: High (compute, infrastructure)
```

### Near Real-Time (5-15 minutes)
```
Use for: Operational dashboards
Data source: Micro-batches, CDC
Cost: Medium
```

### Hourly
```
Use for: Business dashboards
Data source: Scheduled ETL
Cost: Low
```

### Daily
```
Use for: Executive reports, historical analysis
Data source: Batch ETL (overnight)
Cost: Very low
```

---

## Accessibility & Mobile

### Color Blindness Safe
```
❌ Red/Green only (8% of men can't distinguish)
✅ Red/Blue, Orange/Blue
✅ Use patterns + colors
✅ Add labels to all chart elements
```

### Mobile-Friendly
```
Desktop layout: 3 columns, detailed charts
Mobile layout: 1 column, simplified charts

Responsive design:
- Stack vertically
- Hide detailed tables (show on tap)
- Larger touch targets
- Horizontal scroll for tables
```

---

## Dashboard Anti-Patterns

### ❌ Chart Junk
```
Problem: 3D pie charts, unnecessary gradients, decorations
Solution: Clean, simple charts with minimal non-data ink
```

### ❌ Too Many Metrics
```
Problem: 50 metrics on one page, cognitive overload
Solution: 5-7 key metrics, drill-down for details
```

### ❌ Misleading Axes
```
Problem: Y-axis doesn't start at 0 (exaggerates change)
Solution: Start at 0 for bar charts, context for line charts
```

### ❌ No Context
```
Problem: "Revenue: $1.2M" - is that good?
Solution: Add comparison (vs last month, vs target)
```

### ❌ Stale Data
```
Problem: "Last updated: 3 days ago"
Solution: Automated refresh, "Updated 5 minutes ago"
```

## Rules

- Start with questions, not charts — "What decisions does this dashboard enable?"
- 5-7 key metrics maximum on summary view — more creates decision paralysis.
- Always show trend direction (▲▼) and comparison — "$1.2M" means nothing without context.
- Use color sparingly and consistently — red = bad, green = good, blue = neutral.
- Pre-aggregate for performance — dashboard queries should return in < 3 seconds.
- Date range filter is mandatory — users need to explore different time periods.
- Export to CSV/Excel enabled — analysts need raw data.
- Mobile-first for executive dashboards — executives view on phones.
- Test with actual users before launch — what makes sense to you may confuse them.
- Document metric definitions — "Revenue" could mean many things, be specific.
