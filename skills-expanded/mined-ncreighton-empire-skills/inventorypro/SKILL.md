---
name: inventorypro
description: "Automate inventory tracking, order fulfillment, and shipping across e-commerce platforms. Use when the user needs real-time stock management, multi-channel order processing, or automated fulfillment workflows."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["SHOPIFY_API_KEY", "SHOPIFY_API_SECRET", "STRIPE_API_KEY", "SHIPSTATION_API_KEY", "SLACK_WEBHOOK_URL"],
        "bins": ["curl", "jq"]
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "📦"
    }
  }
---

# InventoryPro: Intelligent Inventory Management & Order Fulfillment Automation

## Overview

InventoryPro is an AI-powered inventory management and order fulfillment automation skill designed for e-commerce businesses. It eliminates manual inventory tracking, automates order processing across multiple sales channels, and provides real-time visibility into stock levels and fulfillment status.

**Why InventoryPro Matters:**
- **Reduce Manual Work**: Automate 80%+ of inventory updates and order processing tasks
- **Multi-Channel Integration**: Seamlessly sync inventory across Shopify, WooCommerce, Amazon, and custom platforms
- **Real-Time Visibility**: Track stock levels, order status, and shipping in one unified dashboard
- **Prevent Stockouts**: Intelligent low-stock alerts and automated reorder triggers
- **Shipping Automation**: Integrate with ShipStation, EasyPost, and major carriers (FedEx, UPS, USPS)
- **Slack Integration**: Receive order alerts, inventory warnings, and fulfillment updates in real-time

**Perfect for:**
- E-commerce store owners managing 100+ SKUs
- Dropshippers coordinating multiple suppliers
- Subscription box businesses with recurring orders
- Multi-channel sellers (Amazon, eBay, Shopify, WooCommerce)
- Fulfillment centers automating order workflows

---

## Quick Start

Try these example prompts immediately:

### Example 1: Sync Inventory Across Platforms
```
Sync my current Shopify inventory with WooCommerce and Amazon. 
Show me any discrepancies and update all platforms to match 
the Shopify master inventory count.
```

### Example 2: Process Pending Orders
```
Process all pending orders from the last 24 hours. 
Check inventory availability, create shipping labels via ShipStation, 
and send Slack notifications to the fulfillment team.
```

### Example 3: Low Stock Alert & Reorder
```
Scan inventory for items below 15 units. 
Generate a purchase order for my supplier and alert me via Slack 
if any top-selling products are at critical levels.
```

### Example 4: Order Status Report
```
Generate a fulfillment report for orders placed in the last 7 days. 
Show me order status, tracking numbers, and estimated delivery dates. 
Highlight any delayed shipments.
```

### Example 5: Inventory Forecast
```
Analyze my sales data from the last 90 days and forecast 
inventory needs for the next 30 days. Flag items that may 
run out based on current sales velocity.
```

---

## Capabilities

### 1. **Automated Inventory Tracking**
- Real-time stock level synchronization across all connected platforms
- Automatic inventory adjustments based on sales, returns, and manual corrections
- Historical inventory tracking with audit logs
- Batch inventory imports from CSV/Excel files
- Barcode scanning integration for physical inventory counts

**Usage Example:**
```
Update inventory: Product SKU-12345 sold 5 units on Shopify. 
Deduct from master inventory, sync to Amazon and WooCommerce, 
and trigger reorder if stock falls below 20.
```

### 2. **Multi-Channel Order Processing**
- Unified order queue from Shopify, WooCommerce, Amazon, eBay, and custom APIs
- Automatic order validation and fraud detection
- Intelligent order routing (local warehouse vs. dropshipper vs. marketplace fulfillment)
- Order status synchronization back to all sales channels
- Batch order processing for high-volume days

**Usage Example:**
```
Pull all orders from the past 2 hours across all channels. 
Validate payment status, check inventory, and route orders to 
the appropriate fulfillment location.
```

### 3. **Shipping & Fulfillment Automation**
- Integration with ShipStation, EasyPost, and carrier APIs
- Automatic shipping label generation and rate shopping
- Multi-carrier selection based on cost, speed, and destination
- Tracking number capture and customer notification
- Return label generation and reverse logistics tracking

**Usage Example:**
```
For all orders ready to ship, compare FedEx, UPS, and USPS rates. 
Select the cheapest option, generate labels, and email tracking 
numbers to customers.
```

### 4. **Intelligent Alerts & Notifications**
- Slack integration for real-time order and inventory alerts
- Email notifications for critical events (low stock, failed orders, shipping delays)
- Customizable alert thresholds and escalation rules
- SMS alerts for high-priority issues
- Daily/weekly digest reports

**Usage Example:**
```
Set up a Slack alert: notify #inventory-team when any product 
drops below 10 units, and escalate to #management if it's a 
top-selling item.
```

### 5. **Inventory Analytics & Forecasting**
- Sales velocity analysis by product, category, and time period
- Demand forecasting using historical sales data
- Inventory turnover metrics and ABC analysis
- Seasonal trend detection
- Stock-out risk assessment

**Usage Example:**
```
Analyze the last 6 months of sales data. Show me which products 
have the highest turnover, which are slow-movers, and forecast 
demand for the next quarter.
```

### 6. **Supplier & Purchase Order Management**
- Automated PO generation based on reorder points
- Supplier API integration for real-time lead times
- PO tracking and receipt confirmation
- Cost analysis and supplier performance metrics
- Batch order consolidation to reduce shipping costs

**Usage Example:**
```
Create a purchase order for my top 20 low-stock items. 
Consolidate orders to my primary supplier where possible, 
calculate lead times, and set delivery reminders.
```

---

## Configuration

### Required Environment Variables

```bash
# Shopify Integration
export SHOPIFY_API_KEY="your_shopify_api_key"
export SHOPIFY_API_SECRET="your_shopify_api_secret"
export SHOPIFY_STORE_URL="your-store.myshopify.com"

# Payment & Subscription Processing
export STRIPE_API_KEY="sk_live_your_stripe_key"

# Shipping & Fulfillment
export SHIPSTATION_API_KEY="your_shipstation_api_key"
export SHIPSTATION_API_SECRET="your_shipstation_api_secret"

# Notifications
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
export SLACK_CHANNEL="#order-alerts"

# Optional: Additional Platforms
export WOOCOMMERCE_API_KEY="your_woocommerce_key"
export WOOCOMMERCE_API_SECRET="your_woocommerce_secret"
export AMAZON_MWS_KEY="your_amazon_mws_key"
export EASYPOST_API_KEY="your_easypost_key"
```

### Setup Instructions

1. **Connect Your E-commerce Platform:**
   - Shopify: Create a custom app in Admin > Settings > Apps and Integrations
   - WooCommerce: Generate REST API credentials in Settings > Advanced
   - Amazon: Register for Selling Partner API and create IAM credentials

2. **Configure Shipping Integration:**
   - ShipStation: Generate API key in Settings > API Settings
   - EasyPost: Create account and retrieve API keys from Dashboard

3. **Set Up Slack Notifications:**
   - Create incoming webhook in Slack workspace
   - Add webhook URL to environment variables
   - Test with: `curl -X POST -H 'Content-type: application/json' --data '{"text":"Test"}' $SLACK_WEBHOOK_URL`

4. **Configure Reorder Rules:**
   - Define minimum stock levels per product
   - Set reorder quantities and supplier preferences
   - Specify lead times and safety stock buffers

---

## Example Outputs

### Inventory Sync Report
```
✅ INVENTORY SYNCHRONIZATION COMPLETE

Platform Updates:
├─ Shopify: 47 products updated
├─ WooCommerce: 47 products updated
├─ Amazon: 43 products updated (4 skipped - inactive listings)
└─ eBay: 45 products updated

Discrepancies Resolved:
├─ SKU-12345: Shopify (50) → All platforms (50)
├─ SKU-67890: WooCommerce had 5 extra units (corrected)
└─ SKU-11111: Amazon out of sync (updated to 0 - out of stock)

Sync Duration: 2m 34s
Next Sync: In 30 minutes
```

### Order Fulfillment Status
```
📦 ORDER FULFILLMENT REPORT (Last 24 Hours)

Total Orders Processed: 127
├─ Fulfilled & Shipped: 118 (93%)
├─ Pending Fulfillment: 7 (5%)
├─ On Hold (Payment): 2 (2%)
└─ Cancelled: 0 (0%)

Shipping Summary:
├─ FedEx: 52 orders ($847.23)
├─ UPS: 48 orders ($756.18)
├─ USPS: 18 orders ($89.45)
└─ Local Pickup: 0 orders

Delayed Orders (>24 hours):
├─ Order #ORD-9876: Awaiting payment confirmation
└─ Order #ORD-9875: Oversized item - special handling

Avg Processing Time: 4.2 hours
Avg Shipping Cost: $8.94 per order
```

### Low Stock Alert
```
⚠️ LOW INVENTORY ALERT

Critical (0-5 units):
├─ SKU-12345 "Premium Widget" - 3 units remaining
│  └─ Avg Daily Sales: 8 units → REORDER IMMEDIATELY
├─ SKU-54321 "Best Seller" - 2 units remaining
│  └─ Lead Time: 14 days → URGENT

Warning (5-15 units):
├─ SKU-99999 "Summer Collection" - 12 units
│  └─ Suggested PO: 100 units
└─ SKU-88888 "Seasonal Item" - 8 units
   └─ Suggested PO: 50 units

Recommended Actions:
✓ Generate PO for 3 critical items
✓ Notify supplier of urgent need
✓ Consider pre-orders for out-of-stock items
```

### 30-Day Inventory Forecast
```
📊 DEMAND FORECAST (Next 30 Days)

High Confidence (90%+):
├─ SKU-12345: Projected 240 units (current: 50) → REORDER 200+
├─ SKU-67890: Projected 180 units (current: 120) → REORDER 80+
└─ SKU-11111: Projected 95 units (current: 85) → REORDER 20+

Medium Confidence (70-90%):
├─ SKU-22222: Projected 45 units (current: 30) → Monitor
└─ SKU-33333: Projected 35 units (current: 40) → Adequate

Low Confidence (<70%):
└─ SKU-44444: Projected 15 units (wide variance) → Review

Seasonal Trends:
├─ Summer items trending +35% week-over-week
├─ Winter clearance items trending -20% week-over-week
└─ Holiday prep: Expected 45% spike in 45 days
```

---

## Tips & Best Practices

### 1. **Optimize Reorder Points**
- Use the ABC analysis feature to set different reorder thresholds for high/medium/low movers
- Account for supplier lead times: Reorder Point = (Daily Sales Velocity × Lead Time) + Safety Stock
- Example: If you sell 10/day with 14-day lead time, reorder at 150 units (10 × 14 + 10 safety)

### 2. **Reduce Shipping Costs**
- Enable automatic rate shopping to compare carriers on every order
- Consolidate orders to the same supplier when possible
- Use regional warehouses to reduce shipping distances
- Negotiate volume discounts with primary carriers

### 3. **Prevent Stockouts**
- Set up automated low-stock Slack alerts for your top 50 products
- Use demand forecasting to anticipate seasonal spikes
- Maintain safety stock for slow-moving items with long lead times
- Monitor competitor pricing to detect market shifts

### 4. **Streamline Multi-Channel Operations**
- Sync inventory every 15-30 minutes (not hourly) to minimize overselling
- Use order routing to fulfill from the closest warehouse
- Automate return processing with reverse logistics tracking
- Set up channel-specific fulfillment rules (e.g., Amazon Prime vs. standard)

### 5. **Monitor Key Metrics**
- Track inventory turnover ratio (COGS ÷ Average Inventory Value)
- Monitor order fulfillment time and shipping accuracy rates
- Analyze cost per order (fulfillment + shipping + packaging)
- Review supplier performance (on-time delivery, quality, cost)

### 6. **Integrate with Your Workflow**
- Post daily inventory reports to a dedicated Slack channel
- Set up email digests for executive summaries
- Create custom webhooks to trigger external systems
- Use API to pull data into your BI tool (Tableau, Looker, etc.)

---

## Safety & Guardrails

### What InventoryPro Will NOT Do

- **No Financial Transactions**: This skill does not process payments or refunds. It integrates with Stripe/PayPal but only for order validation.
- **No Unauthorized Access**: Requires valid API credentials for all connected platforms. Will not bypass authentication.
- **No Inventory Manipulation for Fraud**: Cannot be used to artificially inflate/deflate stock for deceptive purposes.
- **No PII Extraction**: Does not extract or store customer personal data beyond what's necessary for order fulfillment.
- **No Automated Pricing Changes**: Cannot unilaterally adjust product prices without explicit user confirmation.
- **No Supplier Fraud**: Will not create unauthorized purchase orders or modify supplier agreements.

### Limitations & Boundaries

1. **API Rate Limits**: Respects platform rate limits (Shopify: 2 requests/sec, Amazon: varies by operation)
2. **Data Sync Delays**: Inventory sync has 5-15 minute latency due to platform processing times
3. **Platform Compatibility**: Only works with platforms that offer public APIs (some legacy systems not supported)
4. **Geographic Restrictions**: Shipping integrations limited to carriers available in your region
5. **Inventory Accuracy**: Dependent on accurate input data; garbage in = garbage out
6. **Concurrent Orders**: Can process up to 1,000 orders per batch; larger volumes may require batching

### Security Best Practices

- Store API keys in environment variables, never hardcode
- Rotate API credentials every 90 days
- Enable IP whitelisting on API keys where available
- Use read-only API scopes for data retrieval operations
- Audit logs track all inventory changes for compliance
- Encrypt sensitive data in transit (HTTPS/TLS 1.2+)

---

## Troubleshooting

### Common Issues & Solutions

**Q: Inventory not syncing between Shopify and WooCommerce**
- A: Check that both API keys are valid and have inventory read/write permissions. Run `curl -H "Authorization: Bearer $SHOPIFY_API_KEY" https://your-store.myshopify.com/admin/api/2024-01/products.json` to test connectivity.

**Q: Orders not appearing in the unified queue**
- A: Verify that all e-commerce platforms are connected and have "Order Read" permissions. Check Slack for sync error notifications. Run manual sync: `inventorypro --sync-orders --force`

**Q: Shipping labels not generating via ShipStation**
- A: Confirm ShipStation API key is correct and account has active carrier accounts. Ensure order addresses are complete and valid. ShipStation requires: street, city, state, ZIP, country.

**Q: Low-