---
name: ecommerce_inventory_tracker
description: Track and manage e-commerce inventory levels. Set up low stock alerts, forecast demand, manage reorder points, and prevent stockouts across multiple platforms.
---

# E-Commerce Inventory Tracker

Monitor and manage inventory across multiple sales channels.

## When to Use

Use this skill when the user wants to:
- Track inventory levels across platforms
- Set up low stock alerts
- Forecast reorder timing
- Manage multi-channel inventory
- Prevent stockouts and overstocking
- Analyze inventory turnover

## Supported Platforms

- Shopify, WooCommerce, Amazon Seller Central
- Etsy, eBay, Walmart Marketplace
- Manual CSV/spreadsheet import
- Inventory management systems (Cin7, TradeGecko, DEAR)

## Key Inventory Metrics

### Essential KPIs

| Metric | Formula | Target |
|--------|--------|--------|
| Stock Turnover | COGS / Average Inventory | 6-12x per year |
| Days of Inventory | 365 / Turnover | 30-60 days |
| Stockout Rate | Stockouts / Total Orders | <2% |
| Carrying Cost | Inventory Value × 20-30% | Minimize |
| Reorder Point | (Lead Time × Daily Sales) + Safety Stock | Calculate |

### Safety Stock Calculation

```
Safety Stock = Z × σ × √(Lead Time)

Where:
- Z = Service factor (1.65 for 95% service level)
- σ = Standard deviation of daily demand
- Lead Time = Days from order to receipt
```

## Workflow

### Step 1: Inventory Audit

Gather current stock levels:

```markdown
## Inventory Snapshot

| SKU | Product | Current Stock | Location | Status |
|-----|---------|--------------|----------|--------|
| SKU-001 | Product Name | 150 | Warehouse A | OK |
| SKU-002 | Product Name | 5 | Warehouse A | ⚠️ LOW |
| SKU-003 | Product Name | 0 | Warehouse B | ❌ OUT |
```

### Step 2: Set Reorder Parameters

For each product, define:
- **Reorder Point**: When to place new order
- **Reorder Quantity**: How much to order
- **Lead Time**: Days from order to receipt
- **Safety Stock**: Buffer for unexpected demand

### Step 3: Alert Configuration

```markdown
## Alert Thresholds

| Alert Level | Trigger | Action |
|-------------|---------|--------|
| 🔴 Critical | ≤5 units | Immediate reorder |
| 🟡 Warning | ≤20 units | Review and plan reorder |
| 🟢 Normal | >20 units | Monitor |
```

### Step 4: Demand Forecasting

```
Weekly Forecast Formula:
Expected Weekly Sales = (Last 4 weeks sales) / 4 × Seasonality Factor

Seasonality Factors:
- Peak season: 1.3-1.5x
- Normal: 1.0x
- Off-peak: 0.7-0.8x
```

## Inventory Status Reports

### Daily Stock Report

```markdown
## 📦 Daily Inventory Report - [DATE]

### Critical Alerts
| SKU | Product | Stock | Days Left | Action |
|-----|---------|-------|-----------|--------|
| SKU-123 | Widget A | 3 | 0.5 days | REORDER NOW |
| SKU-456 | Widget B | 8 | 2 days | Review reorder |

### Healthy Stock
| SKU | Product | Stock | Days Left |
|-----|---------|-------|-----------|
| SKU-789 | Gadget X | 250 | 45 days |
| SKU-012 | Gadget Y | 180 | 30 days |

### Out of Stock
- SKU-999 - Super Gadget (2 pending orders)
```

### Weekly Reorder Plan

```markdown
## 📋 Weekly Reorder Plan - Week of [DATE]

### Orders to Place Today
| Supplier | SKU | Qty | Cost | Lead Time |
|----------|-----|-----|------|-----------|
| Supplier A | SKU-123 | 500 | $2,500 | 7 days |
| Supplier B | SKU-456 | 200 | $1,800 | 14 days |

### Orders to Monitor
| SKU | ETA | Status |
|-----|-----|--------|
| SKU-789 | Mar 30 | In Transit |
| SKU-012 | Apr 2 | Processing |
```

## Best Practices

1. **ABC Analysis**: Prioritize A items (80% revenue, 20% SKUs)
2. **Lead Time Buffer**: Always add 2-3 days buffer to lead times
3. **Seasonal Planning**: Adjust forecasts for holidays and events
4. **Multi-Channel Sync**: Real-time inventory across all platforms
5. **Dead Stock Identification**: Flag items with <90 days sales history
6. **Regular Audits**: Monthly cycle counts vs. annual full inventory

## Inventory Management Formulas

### Economic Order Quantity (EOQ)
```
EOQ = √(2 × D × S / H)

Where:
- D = Annual demand
- S = Ordering cost per order
- H = Annual holding cost per unit
```

### Days of Inventory
```
Days of Inventory = (Current Stock / Average Daily Sales)

Interpretation:
- <30 days: Potential stockout risk
- 30-60 days: Healthy range
- >60 days: Overstocking risk
```

## Example Prompts

- "Create a low stock alert system for my Shopify store"
- "Calculate reorder points for my top 20 SKUs"
- "Forecast demand for Q4 holiday season"
- "Identify slow-moving inventory and suggest clearance strategies"
- "Build a weekly inventory reconciliation report"
