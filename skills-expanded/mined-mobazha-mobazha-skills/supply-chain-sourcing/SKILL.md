---
name: supply-chain-sourcing
description: Connect a print-on-demand supplier, import products, set up automation rules, and monitor alerts. Use when the user wants to sell print-on-demand or dropshipping products.
---

# Supply Chain Sourcing

Connect your Mobazha store to a print-on-demand (POD) or dropshipping supplier, import products, configure pricing, and set up automatic inventory monitoring.

## Prerequisites

- A Mobazha store (SaaS, VPS Standalone, or Local)
- A supplier account (Printful and Printify are supported)

## 1. Connect a Supplier

### Via the Admin Dashboard

1. Go to **Admin → Settings → Integrations**
2. Find the supplier (e.g., Printful) and click **Connect**
3. Enter your API key (get it from your supplier dashboard)
4. The connection status turns green once verified

### Via the API

```bash
curl -X POST <your-store>/v1/fulfillment/printful/connect \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"credentials":{"apiKey":"<your-printful-api-key>"}}'
```

Replace `<your-store>` with your store URL:
- **SaaS**: `https://app.mobazha.org`
- **VPS Standalone**: `https://your-domain.com`
- **Local**: `http://localhost:15104`

## 2. Browse & Import Products

### Print-on-Demand (POD) Workflow

POD products require custom designs. The recommended flow:

1. **Design on supplier dashboard** — create products with your artwork on Printful
2. **Import via My Designs** — go to **Admin → Sourcing → My Designs**, find your design, and click **Import**
3. **Set pricing** — choose a retail markup (recommended 40-60% for apparel, 50-100% for accessories)
4. **Publish** — the product is live in your store

### Import via API

```bash
# List your designs from the supplier
curl <your-store>/v1/fulfillment/printful/store-products \
  -H "Authorization: Bearer <token>"

# Import a specific design
curl -X POST <your-store>/v1/fulfillment/printful/import \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "syncProductId": "<sync-product-id>",
    "retailMarkup": 50,
    "title": "My Custom T-Shirt"
  }'
```

### Via MCP

If connected via MCP, the AI agent can browse your supplier catalog and import products conversationally.

## 3. Manage Imported Products

Go to **Admin → Sourcing → Imported Products** to see all synced products with their status:

- **Synced** — product data is up to date with the supplier
- **Pending** — sync in progress
- **Error** — sync failed; check the error details

Click **Re-sync** on any product to pull the latest data from the supplier.

## 4. Monitor Alerts

The system automatically monitors your supplier for inventory and pricing changes. Go to **Admin → Sourcing → Alerts & Rules** to view:

### Alert Types

| Type | Description |
|------|-------------|
| **Out of Stock** | A supplier item is no longer available |
| **Back in Stock** | A previously unavailable item is available again |
| **Price Change** | Supplier cost has changed |
| **Rule Action** | An automation rule was triggered |

### Severity Levels

- **Critical** — requires immediate action (e.g., item sold out)
- **Warning** — should review soon (e.g., price increased)
- **Info** — informational (e.g., item back in stock)

Dismiss alerts once reviewed. Dismissed alerts are hidden by default but can be shown with the toggle.

## 5. Configure Automation Rules

Set up rules to automatically respond to supplier changes. Go to **Admin → Sourcing → Alerts & Rules** and click **Add Rule**.

### Available Triggers

| Trigger | Description |
|---------|-------------|
| Supplier item goes out of stock | Fires when stock drops to zero |
| Supplier cost increases | Fires when cost exceeds the threshold |
| Supplier cost decreases | Fires when cost drops below the threshold |

### Available Actions

| Action | Description |
|--------|-------------|
| Hide listing from store | Removes the listing from your storefront |
| Show listing in store | Makes a hidden listing visible again |
| Pause listing | Marks the listing as paused |
| Notify me only | Creates an alert without changing the listing |

### Example: Auto-hide Out-of-Stock Items

```bash
curl -X POST <your-store>/v1/fulfillment/rules \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "trigger": "out_of_stock",
    "action": "hide_listing",
    "enabled": true
  }'
```

### Example: Alert on Price Increase > 10%

```bash
curl -X POST <your-store>/v1/fulfillment/rules \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "trigger": "price_increase",
    "action": "notify_only",
    "threshold": 10,
    "enabled": true
  }'
```

## 6. Order Fulfillment

When a buyer purchases a sourced product:

1. The order is automatically sent to the supplier for fulfillment
2. A **margin gate** checks that the supplier cost hasn't exceeded your retail price
3. The supplier prints/ships the product directly to the buyer
4. Tracking information is automatically synced to the order

Check fulfillment status in **Admin → Orders → Order Details** under the Fulfillment section.

### Fulfillment Statuses

| Status | Meaning |
|--------|---------|
| Pending | Order sent to supplier, awaiting processing |
| In Process | Supplier is producing the item |
| Shipped | Item shipped, tracking available |
| Delivered | Delivery confirmed |
| Failed | Fulfillment failed (check reason) |

### Failure Reasons

If fulfillment fails, the failure reason helps diagnose the issue:

- **Margin protection failed** — supplier cost exceeds your retail price. Adjust pricing.
- **Validation failed** — order data rejected by supplier. Check product configuration.
- **Retryable error** — temporary issue; automatic retry is scheduled.
- **Manual action required** — needs operator review.

## 7. API Reference

| Method | Path | Description |
|--------|------|-------------|
| GET | `/v1/fulfillment/providers` | List connected providers |
| POST | `/v1/fulfillment/<provider>/connect` | Connect a provider |
| DELETE | `/v1/fulfillment/<provider>/disconnect` | Disconnect a provider |
| GET | `/v1/fulfillment/<provider>/catalog` | Browse product catalog |
| GET | `/v1/fulfillment/<provider>/store-products` | List your designs |
| POST | `/v1/fulfillment/<provider>/import` | Import a product |
| GET | `/v1/fulfillment/<provider>/synced-products` | List imported products |
| POST | `/v1/fulfillment/products/<slug>/sync` | Re-sync a product |
| GET | `/v1/fulfillment/orders/<orderID>/status` | Check fulfillment status |
| GET | `/v1/fulfillment/alerts` | List alerts |
| DELETE | `/v1/fulfillment/alerts/<alertID>` | Dismiss an alert |
| GET | `/v1/fulfillment/rules` | List automation rules |
| POST | `/v1/fulfillment/rules` | Create a rule |
| DELETE | `/v1/fulfillment/rules/<ruleID>` | Delete a rule |
