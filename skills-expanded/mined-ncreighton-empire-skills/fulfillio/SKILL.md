---
name: fulfillio
description: "Automate multi-step e-commerce order fulfillment with intelligent routing, real-time inventory tracking, and shipping integration. Use when the user needs order automation, inventory management, or fulfillment workflows across multiple channels."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["SHOPIFY_API_KEY","SHOPIFY_API_PASSWORD","SHIPSTATION_API_KEY","SHIPSTATION_API_SECRET","WAREHOUSE_DB_CONNECTION"],"bins":["curl","jq"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"📦"}}
---

## Overview

**Fulfillio** is a production-grade order fulfillment automation skill that orchestrates complex e-commerce workflows end-to-end. It eliminates manual fulfillment bottlenecks by automating order routing, real-time inventory synchronization, and shipping carrier integration.

### Why Fulfillio Matters

E-commerce fulfillment involves dozens of manual touchpoints: order verification, inventory allocation, warehouse routing, carrier selection, label generation, and customer notification. Each manual step introduces delays, errors, and lost revenue. Fulfillio automates the entire pipeline, reducing order-to-ship time from hours to minutes while maintaining inventory accuracy across channels.

### Supported Integrations

- **Shopify** — native order sync and inventory management
- **WooCommerce** — WordPress e-commerce integration via REST API
- **ShipStation** — multi-carrier shipping automation
- **EasyPost** — intelligent carrier selection and rate shopping
- **Slack** — real-time fulfillment alerts and order notifications
- **Google Sheets** — inventory reporting and analytics
- **Stripe** — payment verification before fulfillment
- **AWS S3** — label storage and document management

---

## Quick Start

Try these example prompts to see Fulfillio in action:

### Example 1: Automate Order Fulfillment Workflow
```
"Set up an automated order fulfillment workflow that:
- Captures new Shopify orders every 5 minutes
- Verifies inventory availability in real-time
- Routes orders to the nearest warehouse
- Generates shipping labels via ShipStation
- Notifies customer via email with tracking info
- Posts fulfillment status to Slack #orders channel"
```

### Example 2: Sync Inventory Across Channels
```
"Create a real-time inventory sync that:
- Pulls stock levels from warehouse management system
- Updates Shopify, WooCommerce, and Amazon listings
- Prevents overselling across channels
- Flags low-stock items for reordering
- Generates daily inventory report in Google Sheets
- Alerts team when items drop below safety threshold"
```

### Example 3: Smart Carrier Selection
```
"Build a shipping optimization workflow that:
- Compares rates across USPS, UPS, FedEx, DHL
- Selects cheapest carrier meeting delivery SLA
- Applies negotiated discounts automatically
- Generates labels with branded tracking pages
- Stores PDFs in S3 for compliance
- Updates order with chosen carrier and estimated delivery"
```

### Example 4: Handle Returns & Refunds
```
"Automate return processing:
- Capture return requests from Shopify
- Generate prepaid return labels
- Track return shipment status
- Verify item condition upon receipt
- Process refund when item scanned at warehouse
- Update inventory and customer via email"
```

---

## Capabilities

### 1. Intelligent Order Routing
- **Multi-warehouse allocation** — Automatically routes orders to nearest warehouse based on inventory availability and shipping zones
- **Split shipment logic** — Breaks large orders into multiple shipments from different warehouses when inventory is split
- **Priority ordering** — Respects VIP customer status, express shipping requirements, and backorder preferences
- **Geolocation optimization** — Uses ZIP code mapping to minimize shipping distances and costs

**Usage Example:**
```
When order arrives:
1. Query inventory across all warehouses
2. Calculate distance to customer
3. Select warehouse with item + shortest ship time
4. Reserve inventory atomically
5. Create picking ticket with warehouse routing code
```

### 2. Real-Time Inventory Management
- **Bi-directional sync** — Pulls inventory from warehouse management system, pushes to all sales channels
- **Reservation tracking** — Prevents overselling by reserving stock when order is placed
- **Cycle counting** — Validates physical inventory against system records
- **Reorder automation** — Triggers purchase orders when stock falls below configurable thresholds
- **Channel-specific visibility** — Hides out-of-stock items on Shopify/WooCommerce automatically

**Configuration:**
```yaml
inventory_sync:
  frequency: "every 5 minutes"
  channels: ["shopify", "woocommerce", "amazon"]
  safety_stock_threshold: 10
  reorder_point: 25
  auto_purchase_order: true
```

### 3. Shipping Carrier Integration
- **Rate shopping** — Queries multiple carriers (USPS, UPS, FedEx, DHL) in real-time
- **Service level matching** — Selects carrier that meets delivery SLA at lowest cost
- **Negotiated rate application** — Applies volume discounts automatically
- **Label generation** — Creates shipping labels with barcode, tracking, and return address
- **Tracking sync** — Pulls tracking updates and notifies customer automatically
- **Branded tracking pages** — Custom tracking experience with your branding

**Supported Carriers:**
- USPS (Priority Mail, Priority Express, Ground Advantage)
- UPS (Ground, 2-Day, Next Day, International)
- FedEx (Ground, 2-Day, Overnight, International)
- DHL Express (International)

### 4. Order Status Management
- **Real-time status updates** — Tracks order through picking → packing → shipping → delivery
- **Customer notifications** — Sends email/SMS at each milestone (order confirmed, shipped, delivered)
- **Slack integration** — Posts fulfillment alerts to team channels
- **Webhook support** — Sends order status events to your systems
- **Exception handling** — Flags unshipped orders, failed deliveries, and exceptions

### 5. Returns & Refunds
- **Automated return label generation** — Customer requests return, prepaid label is emailed instantly
- **Return tracking** — Monitors return shipment status end-to-end
- **Condition verification** — Captures return condition at warehouse (restockable, defective, etc.)
- **Refund processing** — Automatically refunds customer when item is received and verified
- **Restocking** — Returns inventory to available stock automatically

---

## Configuration

### Required Environment Variables

Set these before using Fulfillio:

```bash
# Shopify Configuration
export SHOPIFY_API_KEY="your_api_key"
export SHOPIFY_API_PASSWORD="your_api_password"
export SHOPIFY_STORE_URL="mystore.myshopify.com"

# ShipStation Configuration
export SHIPSTATION_API_KEY="your_api_key"
export SHIPSTATION_API_SECRET="your_api_secret"

# Warehouse Database
export WAREHOUSE_DB_CONNECTION="postgresql://user:pass@host:5432/warehouse_db"

# Optional: EasyPost for advanced rate shopping
export EASYPOST_API_KEY="your_easypost_key"

# Optional: Slack notifications
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

# Optional: AWS S3 for label storage
export AWS_ACCESS_KEY_ID="your_access_key"
export AWS_SECRET_ACCESS_KEY="your_secret_key"
export AWS_S3_BUCKET="fulfillment-labels"
```

### Setup Instructions

1. **Connect to Shopify:**
   - Generate API credentials in Shopify Admin → Apps and integrations → Develop apps
   - Select scopes: `read_orders`, `write_orders`, `read_inventory`, `write_inventory`
   - Add credentials to environment variables above

2. **Connect to ShipStation:**
   - Sign up for ShipStation account
   - Add your carriers (USPS, UPS, FedEx, DHL)
   - Generate API key in Settings → API Settings
   - Add credentials to environment variables

3. **Connect Warehouse Database:**
   - Ensure warehouse system has REST API or direct database access
   - Test connection: `psql $WAREHOUSE_DB_CONNECTION -c "SELECT 1"`
   - Verify inventory tables exist with SKU, quantity, location fields

4. **Optional: Enable Slack Notifications:**
   - Create Slack app in workspace
   - Generate incoming webhook URL
   - Add to SLACK_WEBHOOK_URL environment variable

---

## Example Outputs

### Order Fulfillment Summary
```json
{
  "order_id": "ORD-2024-001847",
  "customer": "jane@example.com",
  "status": "shipped",
  "fulfillment_details": {
    "warehouse": "Chicago Distribution Center",
    "picked_at": "2024-01-15T09:23:00Z",
    "packed_at": "2024-01-15T10:45:00Z",
    "shipped_at": "2024-01-15T14:30:00Z"
  },
  "shipping": {
    "carrier": "UPS",
    "service": "2-Day Air",
    "tracking_number": "1Z999AA10123456784",
    "cost": "$12.50",
    "estimated_delivery": "2024-01-17"
  },
  "items": [
    {
      "sku": "WIDGET-001",
      "name": "Premium Widget",
      "quantity": 2,
      "warehouse_location": "A-12-3"
    }
  ],
  "notifications_sent": [
    "order_confirmed (2024-01-15 08:00)",
    "order_shipped (2024-01-15 14:35)",
    "slack_alert (2024-01-15 14:36)"
  ]
}
```

### Inventory Sync Report
```json
{
  "sync_timestamp": "2024-01-15T15:30:00Z",
  "channels_updated": ["shopify", "woocommerce"],
  "items_synced": 847,
  "changes": {
    "quantity_updated": 312,
    "visibility_changed": 45,
    "new_items": 12,
    "discontinued": 3
  },
  "alerts": [
    "WIDGET-001: Low stock (5 units remaining, reorder threshold is 25)",
    "GADGET-042: Out of stock across all warehouses, hidden from channels"
  ],
  "next_sync": "2024-01-15T15:35:00Z"
}
```

### Shipping Rate Comparison
```json
{
  "order_id": "ORD-2024-001847",
  "destination": "San Francisco, CA 94102",
  "weight": "2.5 lbs",
  "rates_compared": [
    {
      "carrier": "USPS",
      "service": "Priority Mail Express",
      "cost": "$28.95",
      "delivery_days": 1,
      "selected": false
    },
    {
      "carrier": "UPS",
      "service": "2-Day Air",
      "cost": "$12.50",
      "delivery_days": 2,
      "selected": true,
      "reason": "Lowest cost meeting 2-day SLA"
    },
    {
      "carrier": "FedEx",
      "service": "Ground",
      "cost": "$8.75",
      "delivery_days": 5,
      "selected": false
    }
  ],
  "selected_carrier": "UPS",
  "label_generated": true,
  "label_url": "s3://fulfillment-labels/ORD-2024-001847.pdf"
}
```

---

## Tips & Best Practices

### 1. Optimize Warehouse Routing
- **Map shipping zones to warehouses** — Define which warehouse serves which ZIP codes to minimize distance
- **Balance inventory distribution** — Keep fast-moving items in multiple warehouses to reduce split shipments
- **Monitor warehouse utilization** — Track picking/packing speed by warehouse and rebalance if needed
- **Set up geofencing** — Use latitude/longitude to intelligently route orders to nearest fulfillment center

### 2. Reduce Shipping Costs
- **Enable rate shopping** — Always compare carriers; savings typically 15-25% vs. negotiated rates alone
- **Batch shipments** — Group orders shipping to same ZIP code for potential discounts
- **Negotiate volume discounts** — Use Fulfillio's reporting to show carriers your volume and negotiate better rates
- **Use regional carriers** — USPS often beats UPS/FedEx for light packages; DHL excels for international

### 3. Improve Inventory Accuracy
- **Run cycle counts** — Use Fulfillio's cycle counting to verify physical inventory monthly
- **Set safety stock** — Configure reorder points 20-30% above average demand to prevent stockouts
- **Monitor shrinkage** — Track discrepancies between system and physical counts to identify theft/damage
- **Use SKU-level tracking** — Enable barcode scanning at picking/packing to catch errors early

### 4. Enhance Customer Experience
- **Provide tracking early** — Send tracking info within 1 hour of shipment
- **Use branded tracking pages** — Customize tracking experience with your logo and messaging
- **Offer multiple notification channels** — Email + SMS + Slack for time-sensitive orders
- **Proactive exception handling** — Alert customer immediately if delivery is delayed

### 5. Monitor Performance
- **Track key metrics** — Monitor order-to-ship time, inventory accuracy, carrier performance, customer satisfaction
- **Set up dashboards** — Use Google Sheets integration to visualize fulfillment KPIs daily
- **Review carrier performance** — Rank carriers by cost, speed, and reliability; adjust carrier mix quarterly
- **Analyze return rates** — Identify products with high return rates and investigate root causes

---

## Safety & Guardrails

### What Fulfillio Will NOT Do

- **Override payment verification** — Orders will not be fulfilled until payment is confirmed (Stripe integration required)
- **Ship to high-risk locations** — Automatically blocks shipments to addresses flagged by fraud detection
- **Violate carrier restrictions** — Respects carrier rules (weight limits, hazmat restrictions, prohibited items)
- **Bypass inventory holds** — Will not fulfill orders if inventory is reserved for other orders or on hold
- **Process unverified returns** — Return refunds only process after item is physically received and scanned

### Limitations & Boundaries

1. **Inventory sync delays** — Real-time sync has 5-minute maximum latency; overselling possible if orders placed simultaneously across channels
2. **International shipping complexity** — Customs forms, duties, and international restrictions require manual review for some destinations
3. **Carrier API dependencies** — If carrier APIs are down, label generation may fail; fallback to manual label creation
4. **Data retention** — Order data retained for 90 days; archive older orders to reduce query latency
5. **Rate limits** — Shopify API: 2 requests/second; ShipStation: 5 requests/second; plan batch operations accordingly

### Compliance & Security

- **PCI DSS compliance** — Payment data never stored locally; Stripe handles tokenization
- **Data encryption** — All API credentials encrypted at rest using AES-256
- **Audit logging** — All fulfillment actions logged with timestamp and user for compliance
- **GDPR compliance** — Customer data can be deleted on request; deletion removes from all systems within 24 hours
- **Webhook security** — Validates webhook signatures to prevent spoofed order events

---

## Troubleshooting

### Common Issues & Solutions

#### Issue: "Inventory sync not updating Shopify"
**Diagnosis:**
```bash
# Check API connectivity
curl -X GET https://mystore.myshopify.com/admin/api/2024-01/inventory_levels.json \
  -H "X-Shopify-Access-Token: $SHOPIFY_API_PASSWORD"
```

**Solutions:**
1. Verify `SHOPIFY_API_KEY` and `SHOPIFY_API_PASSWORD` are set correctly
2. Check API scopes include `read_inventory` and `write_inventory`
3. Ensure inventory tracking is enabled in Shopify for the product
4. Check for API rate limiting: `curl -I` response should show `X-Request-Id` header
5. Verify product variant IDs match between Shopify and warehouse system

#### Issue: "ShipStation label generation fails"
**Diagnosis:**
```bash
# Test ShipStation API connectivity
curl -X GET https://ssapi.shipstation.com/accounts/getac