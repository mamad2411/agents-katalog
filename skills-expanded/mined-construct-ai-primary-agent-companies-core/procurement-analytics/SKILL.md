---
title: Procurement Analytics
description: Generate spend analytics, procurement KPIs, cost variance reports, and supplier quality trending with data aggregation and visualization patterns
version: 1.0
frequency_percent: 60.0
success_rate_percent: 91.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/procurement-analytics
gigabrain_tags: disciplines, 01900_procurement, spend-analytics, procurement-kpis, cost-variance, supplier-quality, predictive-analytics
openstinger_context: procurement-dashboard, data-analysis, procurement-performance
last_updated: 2026-03-31
related_docs:
  - docs_construct_ai/disciplines/01900_procurement/agent-data/domain-knowledge/1900_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/01900_procurement/agent-data/prompts/01900_AI-NATIVE-PROCUREMENT-OPERATIONS-PROMPT.md
  - docs_construct_ai/disciplines/01900_procurement/agent-data/domain-knowledge/1900_GLOSSARY.MD
  - docs_construct_ai/disciplines/01900_procurement/workflow_docs/1900_PROCUREMENT_COMPREHENSIVE_WORKFLOW.MD
related_skills:
  - pre-task-assessment-readiness
  - workflow-implementation
  - procurement-data-extraction
  - supplier-evaluation
---

# Procurement Analytics

## Overview

Generate procurement analytical insights from structured data sources: spend analytics (category, vendor, timeline), KPI dashboards (order cycle time, approval turnaround, supplier performance), cost variance reports (budget vs. actual), supplier quality trending (inspection results, quality scores), and predictive analytics (risk prediction, price forecasting) based data, and supplier quality trending (inspection results, quality scores. Aggregates data from procurement systems (ERP, order management, supplier database) and generates visualizations and reports.

**Announce at start:** "I'm using the procurement-analytics skill to analyze procurement data and generate analytical insights."

## When to Use This Skill

**Trigger Conditions:**
- Generating spend analysis reports (category breakdown, vendor concentration, trend charts)
- Creating procurement KPI dashboards (order cycle time, approval turnaround, supplier performance)
- Producing cost variance reports (budget vs. actual, variance causes)
- Tracking supplier quality trends (inspection results, quality scores over time)
- Building procurement performance reports for management review
- Generating export reports for audit or regulatory compliance

**Prerequisites:**
- Structured procurement data available (orders, approvals, invoices, delivery records)
- Time range defined for analysis
- Dimension of interest identified (category, vendor, project, time period)

## Step-by-Step Procedure

### Step 1: Analytics Type Selection

Select the type of analysis required:

| Analysis Type | Purpose | Key Metrics | Output |
|---------------|---------|-------------|--------|
| **Spend Analytics** | Understand spending patterns, identify savings | Category spend, vendor concentration, trend over time | Category breakdown chart, vendor concentration table |
| **KPI Dashboard** | Monitor procurement performance | Order cycle time, approval turnaround, supplier performance | KPI widgets, trend charts |
| **Cost Variance** | Track budget compliance | Budget vs. actual, variance amount, variance % | Variance report, corrective action log |
| **Supplier Quality** | Monitor supplier performance trends | Inspection pass rate, defect rate, quality score | Quality trend chart, supplier ranking |
| **Predictive Analytics** | Forecast procurement performance | Delivery risk score, price trend forecast | Risk score, forecast chart |
| **Ad-Hoc Report** | Custom analysis for specific need | Dependent on query | Custom report, data table |

### Step 2: Data Source Identification

Identify data sources required for the analysis:

| Data Source | Purpose | Data Available |
|-------------|---------|----------------|
| **Order Management** | Order cycle time, value analysis | Order date, approval date, order value, line items |
| **Approval Logs** | Approval cycle time, escalation rates | Submitted date, approved date, approver, rejection count |
| **Invoice Records** | Spend, cost variance | Invoice amount, PO reference, payment date, variance |
| **Delivery Records** | Delivery reliability, lead time analysis | Expected date, actual date, quantity variance |
| **Inspection Records** | Supplier quality, defect tracking | Pass/fail, defect type, severity, corrective action |
| **Supplier Database** | Vendor concentration, tier performance | Supplier tier, contract value, performance score |

### Step 3: Aggregation Pipeline

Execute data aggregation following the pipeline:

```
DATA EXTRACTION (source systems → structured dataset)
    ↓
FILTERING (time range, categories, vendors, projects)
    ↓
AGGREGATION (sums, averages, rates, trends)
    ↓
CALCULATION (variance, performance, ranking)
    ↓
VISUALIZATION DATA PREPARATION (chart-ready format)
    ↓
OUTPUT (report, dashboard, export)
```

**Aggregation Examples:**

**Spend by Category:**
```sql
SELECT category, SUM(amount) as total_spend, COUNT(*) as order_count
FROM orders
WHERE order_date BETWEEN start AND end
GROUP BY category
ORDER BY total_spend DESC
```

**Supplier Delivery Reliability:**
```sql
SELECT supplier_id, 
       AVG(CASE WHEN delivery_date <= expected_date THEN 1.0 ELSE 0.0 END) as on_time_rate,
       COUNT(*) as total_deliveries
FROM delivery_records
WHERE delivery_date BETWEEN start AND end
GROUP BY supplier_id
```

### Step 4: KPI Calculation

Calculate procurement KPIs using standard definitions:

| KPI | Formula | Target |
|-----|---------|--------|
| **Order Cycle Time** | Average(days from requisition to approved PO) | <5 days (standard), <1 day (emergency) |
| **Approval Turnaround** | Average(days from submission to approval) | <24 hours per level |
| **PO Accuracy Rate** | (POs without revision / total POs) × 100 | >98% |
| **On-Time Delivery** | (On-time deliveries / total deliveries) × 100 | >95% |
| **Budget Compliance** | (Actual spend / Budget) × 100 | 95-105% (variance within tolerance) |
| **Supplier Defect Rate** | (Defective deliveries / total deliveries) × 100 | <2% |
| **Contract Utilization** | (Spend under contract / total spend) × 100 | >85% |

### Step 5: Cost Variance Analysis

Calculate cost variance for orders and projects:

```
Cost Variance = Actual Cost - Budgeted Cost
Variance % = (Actual Cost - Budgeted Cost) / Budgeted Cost × 100
```

**Variance Categories:**
| Variance Range | Classification | Action Required |
|----------------|---------------|-----------------|
| 0-5% | Within tolerance | Monitor, no action |
| 5-10% | Minor variance | Document cause, flag for review |
| 10-20% | Significant variance | Root cause analysis, corrective action |
| >20% | Major variance | Escalate to management, formal review |

### Step 6: Supplier Quality Trending

Track supplier quality performance over time:

**Trend Analysis:**
- Collect inspection results monthly (or per delivery)
- Calculate rolling average (last 12 months or last 20 deliveries)
- Identify trend direction (improving, stable, declining)
- Flag suppliers with declining quality trend

**Quality Score:**
```
Quality Score = (Passing Inspections / Total Inspections) × 100
Severity Weighted = Σ(inspection_result.weight) / Σ(inspection.weight) × 100
```

### Step 7: Predictive Analytics (Future State)

Prepare for predictive analytics when ML models are available:

| Predictive Capability | Data Required | Model | Output |
|----------------------|--------------|-------|--------|
| **Delivery Risk** | Historical delivery data, supplier performance, external factors | Classification model | Risk score (0-100) |
| **Price Forecasting** | Historical price data, commodity indices, market data | Time series model | 3-month price forecast |
| **Supplier Risk** | Financial data, delivery performance, quality data | Scoring model | Supplier risk score |
| **Cycle Time Prediction** | Order complexity, approval history, workload | Regression model | Predicted cycle time |

### Step 8: Report Generation

Generate analytical report in requested format:

| Format | Use Case | Content |
|--------|----------|---------|
| **Dashboard** | Real-time monitoring | KPI widgets, trend charts, alerts |
| **PDF Report** | Management review, archival | Executive summary, detailed charts, recommendations |
| **Excel Export** | Data analysis, pivot tables | Raw data, calculated fields, charts |
| **JSON** | System integration | Structured data, all metrics, time series |

## Success Criteria

- [ ] Analytics type correctly selected per requirements
- [ ] Data sources identified and accessed correctly
- [ ] Aggregation pipeline completes without data errors
- [ ] All KPIs calculated correctly with documented formulas
- [ ] Cost variance analysis identifies significant variances
- [ ] Supplier quality trending includes trend direction
- [ ] Report generated in requested format(s)
- [ ] Data accuracy matches source system values

## Common Pitfalls

1. **Incorrect Time Boundaries** — Always use consistent date ranges across all data sources. Mixing fiscal and calendar periods causes comparison errors.
2. **Double Counting** — When aggregating orders and line items, avoid double counting (e.g., counting order total AND line items). Use consistent grain.
3. **Ignoring Null Values** — Null ≠ 0. Missing data should be flagged as null, not assumed to be zero. This affects averages and trends.
4. **Stale Data** — Always check last data refresh timestamp. Reports based on stale data mislead decision-makers.
5. **No Baseline Comparison** — KPIs without targets or baselines are not actionable. Always include the target or prior period comparison.

## Cross-References

### Related Skills
- `procurement-data-extraction` — Provides structured data for aggregation
- `supplier-evaluation` — Uses quality trending data for supplier scoring
- `procurement-order-management` — Provides order data for cycle time analysis
- `procurement-compliance` — Uses spend data for compliance monitoring

### Related Agents
- `Procurement Analytics Specialist` (DomainForge) — Primary analytics owner, report generation
- `Procurement Strategy Specialist` (DomainForge) — Trend interpretation, recommendations
- `Financial Compliance Specialist` (DomainForge) — Cost variance analysis, budget compliance

## Example Usage

**Scenario:** Generate Q1 2026 spend analysis and KPI dashboard for construction materials

1. **Analytics Type:** Spend analytics + KPI dashboard
2. **Data Sources:** Order records (Q1 2026), approval logs, delivery records, supplier database
3. **Aggregation:** Group orders by category (structural steel, concrete, electrical, mechanical)
4. **KPIs:** Order cycle time (4.2 days avg), approval turnaround (18 hours avg), on-time delivery (93%), budget compliance (102%)
5. **Cost Variance:** Structural steel +8% (above budget due to price increase), concrete -3% (under budget)
6. **Quality Trend:** Steel supplier quality declining (98% → 95% → 92% over 3 months)
7. **Output:** PDF report with executive summary, Excel export with detailed data

## Performance Metrics

**Target Performance:**
- Data accuracy: >99.9% (matching source system aggregations)
- KPI calculation accuracy: 100% (correct formulas applied)
- Report generation time: <30 seconds (dashboard), <5 minutes (full report)
- Data freshness: <1 hour for dashboard, <24 hours for report