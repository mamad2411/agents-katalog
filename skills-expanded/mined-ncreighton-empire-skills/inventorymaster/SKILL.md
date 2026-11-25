---
name: inventorymaster
description: "Track and manage e-commerce inventory in real-time with automated low-stock alerts and multi-platform integration. Use when the user needs inventory tracking, stock replenishment automation, or warehouse management across Shopify, WooCommerce, and Amazon."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["SHOPIFY_API_KEY", "SHOPIFY_API_PASSWORD", "WOOCOMMERCE_API_KEY", "WOOCOMMERCE_API_SECRET", "AMAZON_AWS_ACCESS_KEY", "AMAZON_AWS_SECRET_KEY", "SLACK_WEBHOOK_URL"],
        "bins": ["curl", "jq"]
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "📦"
    }
  }
---

## Overview

**InventoryMaster** is a production-ready inventory management skill that connects your e-commerce operations to a unified control center. Real-time stock tracking, automated replenishment alerts, and multi-platform synchronization eliminate manual inventory work and prevent stockouts.

### Why This Matters
- **Prevent Lost Sales**: Automated low-stock alerts trigger before inventory runs out
- **Reduce Manual Work**: Sync inventory across Shopify, WooCommerce, Amazon, and custom APIs automatically
- **Multi-Channel Confidence**: Single source of truth for inventory across all sales channels
- **Smart Replenishment**: AI-powered suggestions based on velocity, seasonality, and supplier lead times
- **Slack Integration**: Real-time notifications keep your team informed without context-switching

### Supported Integrations
- **Shopify** (REST API v2024-01)
- **WooCommerce** (REST API v3)
- **Amazon Seller Central** (MWS / SP-API)
- **Google Sheets** (real-time sync)
- **Slack** (alerts & reports)
- **Custom APIs** (webhook-based)

---

## Quick Start

Try these example prompts immediately:

### Example 1: Check Current Inventory Levels
```
Check inventory levels for all products in my Shopify store, 
highlight any items below 10 units, and show me which SKUs 
are at critical stock.
```

### Example 2: Set Up Low-Stock Alerts
```
Configure automatic alerts when any product drops below 
20 units. Send notifications to my Slack channel #inventory 
and email me at operations@mystore.com
```

### Example 3: Sync Multi-Channel Inventory
```
Sync inventory between my Shopify store, WooCommerce site, 
and Amazon seller account. Use Shopify as the source of truth 
and update the other platforms every 15 minutes.
```

### Example 4: Generate Replenishment Report
```
Analyze sales velocity for the last 90 days and recommend 
reorder quantities for my top 50 SKUs. Factor in 14-day 
supplier lead time and include safety stock calculations.
```

### Example 5: Create Inventory Dashboard
```
Build a Google Sheets dashboard showing real-time inventory 
levels, stock turnover rate, and low-stock alerts across all 
my sales channels. Update it every hour.
```

---

## Capabilities

### 1. Real-Time Inventory Tracking
- **Live Stock Sync**: Fetch current inventory from Shopify, WooCommerce, Amazon, or custom APIs
- **Multi-Location Support**: Track stock across warehouses, fulfillment centers, and retail locations
- **Historical Trending**: View inventory changes over time with 90-day historical data
- **SKU Management**: Organize products by SKU, barcode, or custom identifiers

**Usage Example:**
```
Show me inventory for SKU ABC-123 across all locations, 
including on-hand, reserved, and available-to-sell quantities.
```

### 2. Automated Low-Stock Alerts
- **Customizable Thresholds**: Set minimum stock levels per product or category
- **Smart Notifications**: Slack, email, SMS, or webhook alerts when thresholds are breached
- **Alert Escalation**: Notify managers if low-stock items aren't replenished within 24 hours
- **Bulk Configuration**: Apply alert rules to hundreds of products at once

**Usage Example:**
```
Set up alerts for all products in the "Electronics" category 
with min stock 25 units. If stock stays below threshold for 
>48 hours, escalate to my warehouse manager.
```

### 3. Intelligent Replenishment Recommendations
- **Velocity Analysis**: Calculate daily/weekly sales rates from historical data
- **Lead Time Factoring**: Account for supplier delivery times (configurable per vendor)
- **Safety Stock**: Recommend buffer stock based on demand variability
- **Seasonal Adjustment**: Detect seasonal trends and adjust recommendations
- **Cost Optimization**: Balance holding costs vs. stockout risk

**Usage Example:**
```
Recommend reorder quantities for my top 30 products based on 
last 60 days of sales. Use 21-day lead time for my primary 
supplier and include 2-week safety stock buffer.
```

### 4. Multi-Channel Synchronization
- **Bidirectional Sync**: Update inventory across all platforms simultaneously
- **Conflict Resolution**: Choose primary source of truth (Shopify, WooCommerce, etc.)
- **Scheduled Syncs**: Run syncs every 5, 15, 30 minutes or on-demand
- **Sync Logs**: Full audit trail of all inventory changes and sync operations
- **Error Handling**: Automatic retry with exponential backoff on API failures

**Usage Example:**
```
Make Shopify my inventory source of truth. Every 10 minutes, 
sync Shopify stock levels to WooCommerce and Amazon. Log all 
changes and alert me if any sync fails.
```

### 5. Advanced Reporting & Analytics
- **Inventory Turnover**: Calculate COGS, turnover ratio, and aging analysis
- **Stock Level Reports**: Overstocked vs. understocked items with financial impact
- **Channel Performance**: See which sales channels drive fastest inventory velocity
- **Forecasting**: Predict future stock levels based on trend analysis
- **Custom Dashboards**: Export to Google Sheets, Excel, or Tableau

**Usage Example:**
```
Create a report showing my slowest-moving 20 items (stock age 
>90 days) with potential markdowns to clear inventory. Include 
financial impact of holding costs.
```

### 6. Supplier & Vendor Integration
- **Purchase Order Generation**: Auto-create POs when stock falls below reorder point
- **Supplier Lead Times**: Manage different lead times per vendor
- **Cost Tracking**: Monitor unit costs and flag price increases
- **Delivery Tracking**: Integration with common shipping providers

---

## Configuration

### Required Environment Variables

```bash
# Shopify Integration
export SHOPIFY_API_KEY="your_shopify_api_key"
export SHOPIFY_API_PASSWORD="your_shopify_api_password"
export SHOPIFY_STORE_URL="mystore.myshopify.com"

# WooCommerce Integration
export WOOCOMMERCE_API_KEY="ck_live_xxxxx"
export WOOCOMMERCE_API_SECRET="cs_live_xxxxx"
export WOOCOMMERCE_STORE_URL="https://mystore.com"

# Amazon Seller Central
export AMAZON_AWS_ACCESS_KEY="AKIAIOSFODNN7EXAMPLE"
export AMAZON_AWS_SECRET_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
export AMAZON_SELLER_ID="A1234567890ABC"

# Notifications
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
export ALERT_EMAIL="operations@mystore.com"

# Optional: Custom API Endpoint
export CUSTOM_INVENTORY_API="https://api.mywarehouse.com/inventory"
export CUSTOM_API_KEY="your_custom_api_key"
```

### Setup Instructions

1. **Authenticate Integrations**
   - Shopify: Generate API credentials in Admin > Apps & Integrations > Develop Apps
   - WooCommerce: Create API keys in Settings > Advanced > REST API
   - Amazon: Use AWS IAM to create access keys for SP-API
   - Slack: Create incoming webhook in your Slack workspace

2. **Configure Alert Rules**
   ```
   Set default low-stock threshold: 20 units
   Alert recipients: #inventory Slack channel
   Sync frequency: Every 15 minutes
   Primary source: Shopify
   ```

3. **Validate Connections**
   ```
   Test Shopify connection
   Test WooCommerce connection
   Test Amazon SP-API authentication
   ```

---

## Example Outputs

### Inventory Status Report
```
INVENTORY SNAPSHOT - 2024-01-15 14:32 UTC

Product: Wireless Headphones (SKU: WH-001)
├─ Shopify: 47 units (Available: 45, Reserved: 2)
├─ WooCommerce: 23 units
├─ Amazon FBA: 156 units
├─ Warehouse: 89 units
└─ Total: 315 units

⚠️  LOW STOCK ALERTS (3 items)
├─ USB-C Cables (SKU: USB-C-10): 8 units (threshold: 20)
├─ Phone Cases Red (SKU: CASE-RED): 4 units (threshold: 15)
└─ Screen Protectors (SKU: PROT-001): 12 units (threshold: 25)

📊 REPLENISHMENT RECOMMENDATIONS
├─ USB-C Cables: Order 200 units (velocity: 15/day, lead time: 14 days)
├─ Phone Cases Red: Order 150 units (velocity: 8/day, lead time: 21 days)
└─ Screen Protectors: Order 300 units (velocity: 12/day, lead time: 7 days)
```

### Sync Log
```
SYNC OPERATION - 2024-01-15 14:15 UTC

Source: Shopify
├─ Fetched 342 products in 2.3s
├─ Detected 12 inventory changes

Target: WooCommerce
├─ Updated 12 products in 1.8s
├─ Status: ✓ SUCCESS

Target: Amazon SP-API
├─ Updated 11 products in 3.2s
├─ 1 product skipped (FBA managed)
├─ Status: ✓ SUCCESS

Overall Status: ✓ COMPLETED
Duration: 7.3 seconds
Next sync: 2024-01-15 14:30 UTC
```

---

## Tips & Best Practices

### 1. Optimize Sync Frequency
- **High-velocity stores** (100+ daily orders): Sync every 5-10 minutes
- **Medium stores** (20-100 orders/day): Sync every 15 minutes
- **Low-velocity stores** (<20 orders/day): Sync every 30-60 minutes
- **Cost consideration**: Fewer syncs = lower API costs, but higher stockout risk

### 2. Set Realistic Alert Thresholds
- **Fast-moving items**: Set threshold to 2-3x daily sales velocity
- **Slow movers**: Set threshold to 1-2x weekly sales velocity
- **Seasonal items**: Increase thresholds 2-4 weeks before peak season
- **Test thresholds**: Start conservative, adjust based on stockout frequency

### 3. Leverage Replenishment Automation
- **Use velocity analysis**: Don't guess—let 60+ days of data drive decisions
- **Account for lead times**: Longer lead times = higher safety stock
- **Review seasonality**: Adjust recommendations 4-6 weeks before seasonal peaks
- **Monitor cost impact**: Balance carrying costs vs. stockout costs

### 4. Master Multi-Channel Inventory
- **Choose ONE source of truth**: Prevents conflicting updates
- **Use channel-specific overrides**: Allow manual adjustments per channel when needed
- **Monitor sync failures**: Set up escalation alerts if syncs fail 2x in a row
- **Archive old data**: Keep 90 days of history for trending, archive older data

### 5. Create Actionable Dashboards
- **Include key metrics**: Stock levels, turnover rate, days inventory outstanding
- **Use color coding**: Green (healthy), yellow (warning), red (critical)
- **Refresh hourly**: Real-time data keeps decisions current
- **Share with team**: Google Sheets dashboards are team-friendly

### 6. Integrate with Your Workflow
- **Slack notifications**: Set up dedicated #inventory channel for alerts
- **Email summaries**: Daily/weekly digests to key stakeholders
- **Mobile alerts**: Critical low-stock alerts via SMS for warehouse staff
- **PO automation**: Auto-generate purchase orders when reorder points hit

---

## Safety & Guardrails

### What This Skill Will NOT Do
- ❌ **Delete or permanently remove inventory**: All changes are logged and reversible
- ❌ **Modify pricing**: This skill manages quantities only, never prices
- ❌ **Access customer data**: Only reads inventory, not customer information
- ❌ **Bypass authentication**: Requires valid API credentials for all integrations
- ❌ **Make financial decisions**: Recommendations are advisory only; humans approve replenishment
- ❌ **Override manual inventory adjustments**: Your manual changes are preserved and logged

### Limitations & Boundaries
- **API Rate Limits**: Respects all platform rate limits; queues requests if needed
- **Data Consistency**: 5-15 minute lag between actual sales and inventory sync (inherent to APIs)
- **Supported Platforms**: Works with Shopify, WooCommerce, Amazon; custom APIs require webhook setup
- **Historical Data**: Retains 90 days of inventory history; older data archived
- **Concurrent Syncs**: Runs one sync at a time; queues additional requests
- **Timezone Handling**: All timestamps in UTC; configure your local timezone for reporting

### Security Best Practices
- **Credential Storage**: Never log or display API keys; use environment variables only
- **Audit Logging**: All inventory changes logged with timestamp, user, and reason
- **Access Control**: Restrict alert notifications to authorized team members
- **IP Whitelisting**: Available for enterprise deployments
- **Encryption**: All API communications use TLS 1.2+

---

## Troubleshooting

### Issue: Sync Failing Between Shopify and WooCommerce

**Symptoms:**
```
Sync error: "WooCommerce API returned 401 Unauthorized"
```

**Solutions:**
1. Verify `WOOCOMMERCE_API_KEY` and `WOOCOMMERCE_API_SECRET` are correct
2. Check that API keys have "Read/Write" permissions for products
3. Ensure WooCommerce store URL matches `WOOCOMMERCE_STORE_URL` env var
4. Test connection manually:
   ```bash
   curl -u $WOOCOMMERCE_API_KEY:$WOOCOMMERCE_API_SECRET \
     https://mystore.com/wp-json/wc/v3/products
   ```

### Issue: Low-Stock Alerts Not Triggering

**Symptoms:**
```
Product at 5 units, threshold is 20, but no Slack notification sent
```

**Solutions:**
1. Verify alert rule is active:
   ```
   Show me all configured alert rules
   ```
2. Check Slack webhook URL is valid:
   ```
   Test Slack webhook connection
   ```
3. Confirm product is included in alert rule scope
4. Check alert logs for errors:
   ```
   Show me alert logs from the last 24 hours
   ```

### Issue: Inventory Numbers Don't Match Across Channels

**Symptoms:**
```
Shopify shows 50 units, WooCommerce shows 45 units
```

**Solutions:**
1. Check last sync time—may be in progress:
   ```
   Show me sync status and last completed sync
   ```
2. Verify primary source of truth is set correctly
3. Check for manual inventory adjustments on either platform
4. Review sync logs for failed updates:
   ```
   Show me sync errors from the last 24 hours
   ```
5. Force immediate resync:
   ```
   Sync inventory now from Shopify to all channels
   ```

### Issue: Amazon SP-API Connection Failing

**Symptoms:**
```
Amazon sync error: "InvalidParameterValue: Invalid MarketplaceId"
```

**Solutions:**
1. Verify `AMAZON_SELLER_ID` is correct (9-digit format)
2. Confirm AWS credentials have SP-API permissions
3. Check