---
name: supply-chain-optimizer
description: "Optimize supply chains automatically using demand forecasting, inventory analysis, and cost reduction algorithms. Use when the user needs demand planning, inventory optimization, supplier coordination, or cost reduction across warehouses and distribution networks."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["ERP_API_KEY", "SUPPLY_CHAIN_DB_URL", "ANALYTICS_ENGINE"],
        "bins": ["python3", "jq"]
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "📦"
    }
  }
---

# Supply Chain Optimizer

## Overview

The Supply Chain Optimizer skill automates end-to-end supply chain management by analyzing demand patterns, inventory levels, and supplier performance data to generate actionable optimization recommendations. This skill integrates with enterprise ERP systems (SAP, Oracle NetSuite, Microsoft Dynamics), supply chain platforms (Kinaxis, Blue Yonder), and data warehouses to deliver real-time insights that reduce costs, minimize stockouts, and improve fulfillment velocity.

**Why it matters:** Supply chain inefficiencies cost enterprises 5-15% of annual revenue through excess inventory, expedited shipping, and missed sales. Manual optimization processes are slow and reactive. This skill enables data-driven, proactive supply chain management at scale.

**Key integrations:**
- **ERP Systems:** SAP, Oracle NetSuite, Microsoft Dynamics 365
- **Supply Chain Platforms:** Kinaxis RapidResponse, Blue Yonder, Coupa
- **Data Warehouses:** Snowflake, BigQuery, Redshift
- **Collaboration Tools:** Slack (alerts), Salesforce (demand data), Tableau (reporting)
- **Logistics APIs:** Flexport, Shippo, Descartes

---

## Quick Start

Try these prompts immediately to see the skill in action:

### Example 1: Demand Forecast & Inventory Optimization
```
Analyze our inventory across 12 distribution centers for Q1 2024. 
We have $2.3M tied up in slow-moving SKUs. Forecast demand using 
24 months of historical sales data, identify overstock situations, 
and recommend reallocation to high-demand regions. Include safety 
stock calculations for 98% service level.
```

### Example 2: Supplier Performance & Cost Reduction
```
Evaluate our top 15 suppliers across lead time, quality, and cost metrics. 
Identify opportunities to consolidate orders, negotiate volume discounts, 
and reduce the supplier base by 20%. Flag any single-source dependencies 
and recommend dual-sourcing strategies for critical components.
```

### Example 3: Network Optimization & Fulfillment Planning
```
We operate 8 warehouses with 45% excess capacity. Analyze fulfillment 
costs, shipping distances, and inventory turns. Recommend optimal 
warehouse network configuration, including facility consolidation, 
and estimate annual savings. Include transition timeline and one-time costs.
```

### Example 4: Production Scheduling & Material Requirements
```
Generate a 12-week production schedule based on confirmed orders and 
demand forecast. Calculate material requirements, identify supply 
constraints, flag lead-time risks for long-lead items, and recommend 
procurement actions. Output includes Gantt chart and critical path analysis.
```

---

## Capabilities

### 1. Demand Forecasting & Planning
- **Multi-method forecasting:** Exponential smoothing, ARIMA, Prophet, machine learning ensemble models
- **Seasonality detection:** Automatic identification of seasonal patterns, trends, and anomalies
- **Scenario planning:** Best-case, worst-case, and most-likely demand scenarios
- **Forecast accuracy metrics:** MAPE, RMSE, MAE with confidence intervals
- **Collaborative forecasting:** Incorporates sales team input, marketing campaigns, and external factors (weather, economic indicators)
- **Output:** Demand forecasts by SKU, location, and time period with visualization

### 2. Inventory Optimization
- **ABC/XYZ analysis:** Automatic inventory segmentation by value and variability
- **Safety stock calculation:** Balances service level targets with carrying costs
- **Reorder point & order quantity optimization:** Economic order quantity (EOQ) with constraints
- **Slow-moving SKU detection:** Identifies obsolescence risk and recommends clearance actions
- **Multi-echelon optimization:** Optimizes inventory across tiers (plant → DC → store)
- **Cycle counting recommendations:** Prioritizes high-value and high-variability items
- **Output:** Inventory targets by SKU, reallocation recommendations, carrying cost analysis

### 3. Supplier Management & Procurement
- **Supplier scorecarding:** Evaluates cost, quality, delivery, responsiveness, and innovation
- **Consolidation analysis:** Identifies opportunities to reduce supplier count and increase volume leverage
- **Dual-sourcing recommendations:** Flags single-source risks and suggests alternatives
- **Lead time analysis:** Maps supplier lead times, identifies critical-path items
- **Contract optimization:** Recommends volume tiers, payment terms, and renewal timing
- **Supply risk assessment:** Geopolitical, financial, and operational risk scoring
- **Output:** Supplier rankings, consolidation roadmap, procurement strategy

### 4. Network Optimization
- **Facility location analysis:** Evaluates warehouse, plant, and distribution center network
- **Fulfillment cost modeling:** Calculates inbound, outbound, handling, and storage costs by facility
- **Service level coverage:** Maps coverage by region and identifies gaps
- **Consolidation scenarios:** Analyzes 1-stage, 2-stage, and 3-stage network designs
- **Cross-docking opportunities:** Identifies products suited for bypass/cross-dock operations
- **Output:** Network recommendations, facility utilization, annual cost impact

### 5. Production Scheduling & MRP
- **Master production schedule (MPS):** Balances demand, capacity, and inventory targets
- **Material requirements planning (MRP):** Explodes demand into component requirements
- **Capacity constraint analysis:** Identifies bottlenecks and resource conflicts
- **Lead-time offsetting:** Automatically schedules procurement and production based on lead times
- **Critical path analysis:** Highlights items that constrain overall delivery
- **What-if scenarios:** Models impact of demand changes, supply disruptions, or capacity additions
- **Output:** Production schedule, procurement orders, resource plan, Gantt chart

### 6. Cost Reduction & Performance Analytics
- **Total cost of ownership (TCO):** Calculates landed cost, including freight, duties, and handling
- **Benchmark analysis:** Compares your metrics against industry standards
- **Variance analysis:** Explains cost drivers and identifies improvement opportunities
- **KPI dashboards:** Tracks on-time delivery, inventory turns, days inventory outstanding (DIO), cash-to-cash cycle
- **Trend analysis:** Identifies seasonal patterns and long-term shifts
- **Output:** Cost reduction roadmap, savings estimates, performance dashboards

---

## Configuration

### Environment Variables (Required)

```bash
# ERP System Connection
ERP_API_KEY=your_erp_api_key_here
ERP_ENDPOINT=https://your-erp-system.com/api/v1
ERP_SYSTEM=sap|oracle|dynamics|netSuite  # Specify your ERP

# Supply Chain Database
SUPPLY_CHAIN_DB_URL=postgresql://user:password@host:5432/supply_chain
SUPPLY_CHAIN_DB_TIMEOUT=30  # seconds

# Analytics & Forecasting Engine
ANALYTICS_ENGINE=databricks|snowflake|bigquery
ANALYTICS_API_KEY=your_analytics_key
FORECAST_MODEL=prophet|arima|ensemble  # Default: ensemble

# Slack Integration (Optional - for alerts)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
SLACK_CHANNEL=#supply-chain-alerts

# Salesforce Integration (Optional - for demand data)
SALESFORCE_CLIENT_ID=your_salesforce_client_id
SALESFORCE_CLIENT_SECRET=your_salesforce_secret
```

### Configuration Options

```yaml
# optimization_config.yml
demand_forecasting:
  methods: ["prophet", "arima", "exponential_smoothing"]
  lookback_periods: 24  # months of historical data
  confidence_level: 0.95
  seasonality: true
  external_factors: ["marketing_campaigns", "economic_indicators"]

inventory_optimization:
  service_level_target: 0.98  # 98% fill rate
  carrying_cost_percent: 0.25  # 25% of inventory value annually
  obsolescence_threshold: 12  # months without movement
  abc_thresholds: [0.80, 0.15, 0.05]  # A, B, C percentages

supplier_management:
  evaluation_weights:
    cost: 0.40
    quality: 0.25
    delivery: 0.20
    responsiveness: 0.10
    innovation: 0.05
  consolidation_target: 0.80  # 80% spend with top suppliers
  lead_time_buffer: 1.5  # 1.5x standard deviation

network_optimization:
  facility_types: ["plant", "distribution_center", "warehouse"]
  service_level_by_region: 0.95
  transportation_modes: ["ltl", "truckload", "air", "ocean"]
  optimization_horizon: 12  # months

reporting:
  format: ["pdf", "excel", "json", "tableau"]
  frequency: "weekly"
  recipients: ["supply-chain@company.com"]
  include_scenarios: true
```

### Setup Instructions

1. **Connect your ERP system:**
   ```bash
   claw config set ERP_SYSTEM=sap
   claw config set ERP_API_KEY=<your_key>
   claw test-connection erp
   ```

2. **Configure database access:**
   ```bash
   claw config set SUPPLY_CHAIN_DB_URL=<your_connection_string>
   claw test-connection database
   ```

3. **Set up Slack notifications (optional):**
   ```bash
   claw config set SLACK_WEBHOOK_URL=<your_webhook>
   ```

4. **Validate configuration:**
   ```bash
   claw validate supply-chain-optimizer
   ```

---

## Example Outputs

### Output 1: Demand Forecast Report (JSON)
```json
{
  "forecast_period": "2024-Q1",
  "sku": "SKU-12345",
  "demand_forecast": [
    {
      "week": "2024-01-01",
      "forecast": 1250,
      "lower_bound": 1050,
      "upper_bound": 1450,
      "confidence": 0.95
    },
    {
      "week": "2024-01-08",
      "forecast": 1380,
      "lower_bound": 1120,
      "upper_bound": 1640,
      "confidence": 0.95
    }
  ],
  "forecast_accuracy": {
    "mape": 8.3,
    "rmse": 145,
    "mae": 98
  },
  "seasonality_factors": {
    "jan": 0.95,
    "feb": 0.88,
    "mar": 1.05
  },
  "recommendations": [
    "Increase safety stock by 15% in Q1 due to holiday demand volatility",
    "Coordinate with sales on promotional timing to reduce forecast variance"
  ]
}
```

### Output 2: Inventory Optimization Summary (Excel)
```
SKU          | Current Qty | Optimal Qty | Variance | ABC | Action
SKU-12345    | 5,200       | 3,800       | +1,400   | A   | Reduce
SKU-67890    | 450         | 850         | -400     | A   | Increase
SKU-11111    | 120         | 45          | +75      | C   | Clearance
SKU-22222    | 2,100       | 2,100       | 0        | B   | Maintain

Total Carrying Cost Reduction: $285,000 annually
Working Capital Release: $1.2M
Inventory Turns Improvement: 4.2x → 5.1x
```

### Output 3: Supplier Consolidation Roadmap (Tableau Visualization)
```
Current State:
- 47 active suppliers
- Top 10 = 65% of spend
- Average lead time: 35 days
- Quality reject rate: 2.1%

Recommended State (12-month plan):
- 28 active suppliers (-40%)
- Top 10 = 80% of spend (+15%)
- Average lead time: 28 days (-20%)
- Quality reject rate: 1.2% (-43%)

Annual Savings: $1.8M
Transition Risk: LOW (phased approach, dual-sourcing for critical items)
```

### Output 4: Network Optimization Analysis (PDF Report)
```
Current Network: 8 warehouses, 45% excess capacity, $4.2M annual cost
Recommended Network: 6 warehouses, 65% utilization, $3.1M annual cost

Consolidation Timeline:
- Phase 1 (Months 1-3): Dual-run facilities, transfer inventory
- Phase 2 (Months 4-6): Close 2 facilities, optimize routing
- Phase 3 (Months 7-9): Finalize network, stabilize operations

One-Time Costs: $450K (facility closure, equipment relocation)
Annual Savings: $1.1M
ROI: 4.1x in Year 1, ongoing savings thereafter
Service Level Impact: 95% → 96% (improved due to better inventory positioning)
```

---

## Tips & Best Practices

### 1. Data Quality is Critical
- **Garbage in, garbage out:** Ensure your ERP data is clean, consistent, and complete
- **Reconcile inventory regularly:** Monthly physical counts vs. system records
- **Validate demand history:** Remove outliers, adjust for one-time events (promotions, stockouts)
- **Standardize SKU definitions:** Consolidate duplicate SKUs before analysis

### 2. Start with High-Impact Opportunities
- **Pareto principle:** 20% of SKUs typically drive 80% of value; optimize these first
- **Quick wins:** Focus on slow-moving inventory and single-source suppliers (2-4 week payback)
- **Build momentum:** Early successes build stakeholder buy-in for larger network redesigns

### 3. Collaborative Planning
- **Involve sales & marketing:** Their insights on demand drivers improve forecast accuracy
- **Engage procurement:** Supplier relationships and lead times affect optimization feasibility
- **Partner with operations:** Warehouse and production constraints must be incorporated
- **Executive alignment:** Clarify trade-offs (e.g., higher service level vs. lower inventory cost)

### 4. Scenario Planning & Risk Management
- **Run multiple scenarios:** Test impact of demand shocks, supplier failures, capacity constraints
- **Stress-test recommendations:** What if demand drops 20%? What if key supplier fails?
- **Build safety buffers:** Don't optimize to the edge; account for variability and uncertainty
- **Monitor KPIs continuously:** Track forecast accuracy, inventory turns, on-time delivery weekly

### 5. Change Management
- **Communicate early:** Explain "why" behind optimization recommendations
- **Pilot programs:** Test recommendations in one region or product line first
- **Training:** Ensure teams understand new processes and tools
- **Celebrate wins:** Share cost savings and service improvements with stakeholders

### 6. Continuous Improvement
- **Monthly reviews:** Compare actual vs. forecast, identify variance drivers
- **Quarterly optimization:** Re-run analysis as new data arrives
- **Annual strategic review:** Reassess network design, supplier base, demand patterns
- **Benchmark externally:** Compare your metrics against industry peers

---

## Safety & Guardrails

### What This Skill Will NOT Do

- **Replace human judgment:** Recommendations are data-driven inputs; final decisions rest with supply chain leadership
- **Guarantee accuracy:** Forecasts are probabilistic; unexpected events (pandemics, natural disasters, geopolitical shifts) can invalidate models
- **Optimize for a single metric:** Cost reduction recommendations may impact service level or flexibility; trade-offs must be evaluated
- **Handle sensitive supplier negotiations:** This skill provides data; your procurement team conducts actual negotiations
- **Automate procurement orders:** Recommendations require approval before order placement; no autonomous purchasing

### Limitations & Boundaries

- **Data dependencies:** Requires 12+ months of historical data for reliable forecasting; new products with <3 months history use conservative estimates
- **External factor limitations:** Cannot predict unprecedented events (wars, pandemics, regulatory changes); external factor modeling is rule-based, not predictive
- **Supplier risk:** Consolidation recommendations assume supplier viability; geopolitical and