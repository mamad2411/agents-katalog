---
name: inventorygenie
description: "Automate inventory forecasting, supplier integration, and stock analytics for retail operations. Use when the user needs demand prediction, automated reordering, inventory optimization, or multi-location stock management."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["SHOPIFY_API_KEY","SHOPIFY_API_PASSWORD","STRIPE_API_KEY","FORECAST_MODEL_TYPE"],"bins":["python3","curl"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"📦"}}
---

# InventoryGenie — AI-Powered Inventory Management for Retailers

## Overview

InventoryGenie is a production-ready inventory management system designed specifically for retail operations. It combines machine learning-powered demand forecasting, automated supplier integration, and real-time analytics to eliminate stockouts, reduce overstock, and optimize cash flow.

**Why This Matters:**
- **Reduce Carrying Costs**: Predict demand 30+ days ahead to avoid excess inventory
- **Prevent Stockouts**: Automated reordering keeps popular items in stock
- **Multi-Channel Sync**: Integrates with Shopify, WooCommerce, Square, and custom APIs
- **Real-Time Visibility**: Dashboard shows stock levels, turnover rates, and supplier performance across all locations
- **Supplier Automation**: Auto-generates POs, tracks delivery times, and flags slow vendors

**Key Integrations:**
- Shopify (inventory sync, order data)
- WooCommerce (product catalog, sales history)
- Slack (low-stock alerts, reorder notifications)
- Google Sheets (custom reporting, stakeholder dashboards)
- Stripe (sales velocity correlation)
- QuickBooks (cost accounting)

---

## Quick Start

Try these prompts immediately to see InventoryGenie in action:

### Example 1: Demand Forecast Report
```
Generate a 60-day demand forecast for my top 20 SKUs. 
Include seasonality adjustments, confidence intervals, and recommended reorder quantities.
Use the past 18 months of sales data from Shopify.
```

**What you'll get:** CSV with SKU, predicted demand, safety stock, reorder point, and optimal order quantity.

### Example 2: Automated Low-Stock Alert
```
Set up automated alerts for any product that falls below 30% of average weekly sales.
When triggered, create a Slack message to #inventory-team and auto-generate a draft PO to our main supplier.
```

**What you'll get:** Real-time monitoring + Slack notifications + supplier PO drafts ready for approval.

### Example 3: Supplier Performance Dashboard
```
Analyze supplier performance for the last 90 days.
Show on-time delivery rate, average lead time, cost per unit trend, and quality issues.
Recommend which suppliers to prioritize based on reliability.
```

**What you'll get:** Ranked supplier scorecard with actionable recommendations.

### Example 4: Multi-Location Inventory Optimization
```
I have 5 retail locations. Show me which products are overstock in one location 
but understocked in another. Suggest transfers to minimize safety stock across the network.
```

**What you'll get:** Transfer recommendations with cost savings estimates.

---

## Capabilities

### 1. AI-Powered Demand Forecasting
- **Models Supported**: Prophet (seasonal), ARIMA, XGBoost, Linear Regression
- **Data Sources**: Shopify, WooCommerce, custom CSV uploads
- **Forecast Horizon**: 7 to 180 days ahead
- **Accuracy Metrics**: MAPE, RMSE, confidence intervals (80%, 95%, 99%)
- **Seasonal Adjustments**: Auto-detects holidays, promotions, and cyclical patterns
- **Multi-Variable Support**: Correlates with weather, marketing spend, competitor activity

**Usage Example:**
```
Forecast demand for "Winter Boots" using Prophet model.
Include promotional impact from our Black Friday campaign.
Show 95% confidence interval for safety stock calculation.
```

### 2. Automated Supplier Integration
- **Supported Suppliers**: Shopify, custom APIs, EDI files, email-based ordering
- **PO Generation**: Auto-creates purchase orders with optimal quantities
- **Lead Time Tracking**: Monitors supplier delivery performance
- **Cost Optimization**: Suggests bulk order discounts and consolidation opportunities
- **Compliance**: Validates MOQ (minimum order quantity), packaging, incoterms

**Usage Example:**
```
Connect to our supplier API (endpoint: api.supplier.com/v2/orders).
When reorder point is triggered, auto-generate a PO for 2 weeks' worth of inventory.
Set lead time buffer to 5 days and include 10% safety stock.
```

### 3. Real-Time Analytics & Reporting
- **Dashboard Metrics**: Stock turnover, carrying cost, stockout frequency, supplier KPIs
- **Custom Reports**: Export to Google Sheets, PDF, or Slack
- **Alerts & Thresholds**: Configurable triggers for low stock, overstock, slow movers
- **Inventory Aging**: Identifies obsolete stock for clearance
- **ABC Analysis**: Categorizes SKUs by sales velocity and profitability

**Usage Example:**
```
Create a daily Slack report showing:
- Top 10 fast-movers (risk of stockout)
- Top 10 slow-movers (excess inventory)
- Suppliers with delayed shipments
- Forecast accuracy vs. actual sales
```

### 4. Multi-Location Management
- **Network Optimization**: Minimizes total safety stock across locations
- **Transfer Recommendations**: Suggests inventory redistribution
- **Centralized Visibility**: Single dashboard for all warehouses and retail stores
- **Demand Pooling**: Shares stock buffers across locations to reduce redundancy

**Usage Example:**
```
Analyze inventory across 5 locations. 
Show me products that are overstock in Location A but understocked in Location B.
Calculate transfer costs and recommend optimal moves.
```

### 5. Inventory Aging & Obsolescence Detection
- **Days on Hand (DOH)**: Tracks how long inventory sits
- **Turnover Velocity**: Identifies slow-moving SKUs
- **Markdown Recommendations**: Suggests clearance pricing for stale stock
- **Write-off Analysis**: Flags items for potential loss

---

## Configuration

### Required Environment Variables

```bash
# Shopify Integration
export SHOPIFY_API_KEY="your_shopify_api_key"
export SHOPIFY_API_PASSWORD="your_shopify_password"
export SHOPIFY_STORE_URL="your-store.myshopify.com"

# Forecasting
export FORECAST_MODEL_TYPE="prophet"  # Options: prophet, arima, xgboost, linear
export FORECAST_HORIZON_DAYS="60"
export CONFIDENCE_INTERVAL="95"

# Supplier Integration
export SUPPLIER_API_ENDPOINT="https://api.supplier.com/v2"
export SUPPLIER_API_KEY="your_supplier_key"

# Alerts & Notifications
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
export LOW_STOCK_THRESHOLD_PERCENT="30"  # Trigger alert at 30% of avg weekly sales

# Database
export INVENTORY_DB_HOST="localhost"
export INVENTORY_DB_PORT="5432"
export INVENTORY_DB_NAME="inventory_prod"
```

### Setup Instructions

1. **Connect Data Source**
   ```bash
   # For Shopify
   inventorygenie connect shopify --api-key $SHOPIFY_API_KEY --password $SHOPIFY_API_PASSWORD
   
   # For WooCommerce
   inventorygenie connect woocommerce --url https://yourstore.com --api-key $WC_KEY
   ```

2. **Configure Forecasting**
   ```bash
   inventorygenie config forecast \
     --model prophet \
     --horizon 60 \
     --confidence 95 \
     --seasonality auto
   ```

3. **Set Up Alerts**
   ```bash
   inventorygenie alert add \
     --name "low_stock" \
     --condition "stock < (avg_weekly_sales * 0.3)" \
     --action "slack" \
     --webhook $SLACK_WEBHOOK_URL
   ```

4. **Enable Supplier Automation**
   ```bash
   inventorygenie supplier connect \
     --name "primary_supplier" \
     --endpoint $SUPPLIER_API_ENDPOINT \
     --auto-reorder true \
     --lead-time 5
   ```

---

## Example Outputs

### Demand Forecast Report
```
SKU,Product Name,Avg Weekly Sales,Forecast 30d,Forecast 60d,Safety Stock,Reorder Point,Recommended Order Qty
SKU-001,Wireless Headphones,145,4350,8700,290,435,1450
SKU-002,USB-C Cable,312,9360,18720,625,936,3120
SKU-003,Phone Case,87,2610,5220,174,261,870
```

### Low-Stock Alert (Slack Format)
```
🚨 LOW STOCK ALERT
Product: Wireless Headphones (SKU-001)
Current Stock: 125 units
Reorder Point: 435 units
Forecast Lead Time: 5 days
Recommended Order: 1,450 units
Estimated Cost: $14,500
Action: Auto-PO sent to Primary Supplier ✓
```

### Supplier Performance Scorecard
```
Supplier Name: Primary Supplier
On-Time Delivery Rate: 94.2% ✓
Avg Lead Time: 4.8 days (target: 5)
Cost per Unit Trend: -2.3% (improving) ✓
Quality Issues: 2 in 90 days (0.8%) ✓
Overall Score: A+ (Recommended for priority)
```

### Multi-Location Optimization
```
Transfer Recommendation:
FROM: Location A (Overstock)
TO: Location B (Understock)
Product: Winter Boots (SKU-042)
Quantity: 45 units
Current Stock Location A: 180 units (45 days supply)
Current Stock Location B: 8 units (2 days supply)
Transfer Cost: $180
Savings: $1,200 (avoided safety stock)
```

---

## Tips & Best Practices

### 1. Optimize Forecast Accuracy
- **Feed Historical Data**: Provide at least 12 months of sales history for best results
- **Exclude Anomalies**: Remove one-time bulk orders or promotional spikes from training data
- **Update Seasonality**: Adjust seasonal factors quarterly as your business evolves
- **Monitor MAPE**: Aim for <15% mean absolute percentage error; if higher, review data quality

### 2. Supplier Relationship Management
- **Lead Time Buffer**: Add 20-30% buffer to supplier lead times for safety
- **Diversify Suppliers**: Use secondary suppliers for critical SKUs to avoid single-point failures
- **Track Performance**: Review supplier scorecards monthly; switch if on-time delivery drops below 90%
- **Negotiate Bulk Discounts**: Use forecast data to negotiate better pricing for predictable volumes

### 3. Inventory Segmentation (ABC Analysis)
- **A Items** (High value, high velocity): Reorder frequently, tight safety stock
- **B Items** (Medium): Standard reorder points
- **C Items** (Low value): Higher safety stock, less frequent reorders
- **Apply Different Policies**: Use tighter forecasts for A items; looser for C items

### 4. Reduce Carrying Costs
- **Target Turnover Ratio**: Aim for 4-8x annual turnover depending on category
- **Quarterly Reviews**: Identify slow movers; mark down or clear stock
- **Just-In-Time for High-Volume**: Reduce safety stock for fast-moving items with reliable suppliers
- **Seasonal Planning**: Build inventory 60 days before peak season; clear 30 days after

### 5. Multi-Location Strategy
- **Centralized Safety Stock**: Keep buffer stock at warehouse; distribute to stores as needed
- **Cross-Location Transfers**: Use forecasts to identify and execute transfers before stockouts
- **Network Demand Pooling**: Reduce total inventory 10-20% by sharing stock across locations

---

## Safety & Guardrails

### What This Skill Will NOT Do

⚠️ **No Financial Decisions Without Review**
- InventoryGenie generates recommendations, not binding decisions
- All POs over $5,000 require manual approval (configurable)
- Does not execute payments or change supplier contracts

⚠️ **No Data Deletion or Modification**
- This skill reads inventory data; it does not delete or permanently modify records
- All changes are logged and auditable
- Forecast adjustments are suggestions only

⚠️ **No Supplier Communication Without Approval**
- Auto-generated POs are drafts; they require human review before sending
- Slack alerts notify your team; they don't commit to orders
- Email to suppliers is always sent by your account (not InventoryGenie's)

⚠️ **Forecast Accuracy Limitations**
- Forecasts assume historical patterns continue
- Cannot predict sudden market disruptions, supply chain crises, or competitive changes
- Accuracy decreases beyond 90 days; use with caution for long-term planning
- Always validate forecasts with domain expertise

⚠️ **Data Privacy & Security**
- Requires read access to your inventory and sales data
- Does not share data with third parties
- Encrypts all API credentials in transit and at rest
- Complies with GDPR, CCPA, and SOC 2 standards

⚠️ **Supplier Integration Limitations**
- Only works with suppliers that provide API access or EDI files
- Email-based ordering requires manual PO entry
- Does not negotiate pricing or enforce contract terms
- Lead time estimates are historical averages; actual times may vary

---

## Troubleshooting

### Common Issues & Solutions

**Q: My forecasts are inaccurate (MAPE > 25%)**

A: Check these items:
1. Is your sales data clean? Remove returns, cancellations, and bulk orders from training data
2. Do you have enough history? Minimum 12 months; ideally 24 months
3. Are you missing seasonality? Adjust seasonal factors for holidays and promotions
4. Is your product new? New SKUs have no history; use similar products as proxy
5. Try a different model: Switch from Prophet to XGBoost if you have >50 SKUs

**Q: Supplier POs aren't being created**

A: Verify:
1. Supplier API credentials are correct: `inventorygenie test supplier --name primary_supplier`
2. Lead time is set: `inventorygenie config supplier --lead-time 5`
3. Reorder point is being triggered: Check current stock vs. calculated reorder point
4. Approval threshold: If PO value > $5,000, it requires manual approval (check email)

**Q: Low-stock alerts aren't firing**

A: Debug:
1. Confirm Slack webhook is valid: `inventorygenie test alert slack`
2. Check threshold: Is current stock actually below 30% of weekly average?
3. Review alert rules: `inventorygenie alert list`
4. Check logs: `inventorygenie logs --filter alert --last 24h`

**Q: Forecast accuracy drops after promotions**

A: This is expected. Solutions:
1. Exclude promotional periods from training data (mark as anomalies)
2. Increase safety stock during promotional windows
3. Use separate forecasts for "baseline" vs. "promotional" demand
4. Update forecasts daily during campaigns to catch real-time trends

**Q: Multi-location transfers are too expensive**

A: Optimize:
1. Batch transfers: Consolidate 5+ SKUs per shipment
2. Adjust transfer cost model: `inventorygenie config transfer --cost-per-unit 2.50`
3. Increase transfer threshold: Only recommend transfers for items with >$1,000 savings
4. Use slower shipping: Trade cost for longer lead time

**Q: API rate limits exceeded**

A: Solutions:
1. Reduce forecast frequency: Change from hourly to daily updates
2. Batch API calls: Consolidate multiple requests into single endpoint call
3. Use webhook polling instead of constant API hits
4. Contact your data source (Shopify, WooCommerce) for higher rate limits

### FAQ

**Q: How often should I update forecasts?**
A: Daily for fast-moving items (turnover > 2x/week), weekly for standard items, monthly for slow movers. More frequent updates = better accuracy but higher compute cost.

**Q: Can I use this with multiple sales channels?**
A: Yes. InventoryGenie aggregates data from Shopify, WooCommerce, Amazon, and custom APIs. It provides unified forecasting across all