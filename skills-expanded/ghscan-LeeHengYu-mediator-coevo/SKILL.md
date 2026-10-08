---
name: inventory-manager
description: Optimizes inventory levels, predicts demand, and manages stock across warehouses. Use when analyzing inventory, planning reorders, or optimizing supply chain.
---

# Inventory Management System

## Overview

This skill provides systematic approaches to inventory optimization, demand forecasting, and supply chain management for e-commerce and retail businesses.

## Key Metrics

### Stock Level Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Days of Supply | Current Inventory / Daily Sales Rate | 14-45 days |
| Stock Turn | COGS / Average Inventory | 4-12x annually |
| Fill Rate | Orders Fulfilled / Total Orders | > 95% |
| Stockout Rate | Stockout Days / Total Days | < 2% |

**Calculations:**
```
Days of Supply = Current Inventory Units / Average Daily Sales
Stock Turn = Annual COGS / Average Inventory Value
Fill Rate = (Orders Shipped Complete) / (Total Orders) × 100
Stockout Rate = (Days with Zero Stock) / (Total Days) × 100
```

### Reorder Calculations

**Reorder Point Formula:**
```
Reorder Point = (Lead Time × Daily Sales) + Safety Stock

Example:
- Lead time: 14 days
- Daily sales: 50 units
- Safety stock: 200 units
- Reorder Point = (14 × 50) + 200 = 900 units
```

**Safety Stock Formula:**
```
Safety Stock = Z × σd × √L

Where:
Z = Service level factor (1.65 for 95%, 2.33 for 99%)
σd = Standard deviation of daily demand
L = Lead time in days
```

**Economic Order Quantity (EOQ):**
```
EOQ = √[(2 × D × S) / H]

Where:
D = Annual demand
S = Order cost per order
H = Holding cost per unit per year
```

## Alert Thresholds

| Status | Days of Supply | Action Required |
|--------|----------------|-----------------|
| Critical | < 7 days | Immediate reorder, expedite |
| Low | 7-14 days | Place reorder now |
| Normal | 14-45 days | Monitor, scheduled reorder |
| Excess | > 45 days | Evaluate markdown/transfer |
| Dead Stock | > 90 days, zero sales | Liquidate or dispose |

## Inventory Actions

### Low Stock Response

**Immediate Actions:**
1. Check supplier lead times and capacity
2. Evaluate expedited shipping costs vs. stockout cost
3. Identify substitute products to recommend
4. Update availability display on storefront
5. Pause marketing campaigns driving demand

**Reorder Decision Matrix:**
| Scenario | Standard Order | Expedited Order |
|----------|---------------|-----------------|
| Lead time < stockout | Yes | No |
| Lead time > stockout | No | Evaluate cost |
| High margin product | Consider | Yes |
| Low margin product | Yes | No |

### Excess Stock Response

**Evaluation Steps:**
1. Analyze why stock became excess
   - Demand drop
   - Forecast error
   - Cancelled orders
   - Seasonal mismatch

2. Markdown Strategy:
```
Markdown % = (Holding Cost × Projected Days) / Unit Cost

If Markdown % > 30%: Consider liquidation
If Markdown % 10-30%: Promotional pricing
If Markdown % < 10%: Price optimization
```

3. Alternative Actions:
   - Warehouse transfer to higher-demand location
   - Bundle with fast-moving items
   - B2B wholesale channel
   - Donation (tax benefit calculation)

### Dead Stock Management

```
Dead Stock Cost = Units × (Holding Cost + Opportunity Cost)
Liquidation Value = Units × (Salvage Price - Liquidation Cost)

Decision: Liquidate if Liquidation Value > 0 or Dead Stock Cost/month > Liquidation Cost
```

## Demand Forecasting

### Methods

| Method | Best For | Accuracy |
|--------|----------|----------|
| Moving Average | Stable demand | Medium |
| Exponential Smoothing | Trending demand | Medium-High |
| ARIMA | Seasonal patterns | High |
| ML/AI | Complex patterns | Highest |

### Simple Forecasting Formula

```
Forecast = (α × Recent Sales) + ((1-α) × Previous Forecast)

Where α = 0.2 to 0.5 (smoothing factor)
Higher α = More responsive to recent changes
```

### Seasonality Adjustment

```
Seasonal Index = Period Sales / Average Period Sales

Adjusted Forecast = Base Forecast × Seasonal Index

Example (Q4 Holiday Season):
- Base forecast: 1,000 units
- Q4 Index: 1.8
- Adjusted forecast: 1,800 units
```

## Multi-Warehouse Management

### Allocation Strategy

| Factor | Weight | Consideration |
|--------|--------|---------------|
| Regional demand | 40% | Historical sales by region |
| Lead time to customers | 25% | Shipping speed goals |
| Warehouse capacity | 20% | Available space |
| Cost | 15% | Storage and shipping costs |

### Transfer Decision

```
Transfer if:
1. Source warehouse: Days of Supply > 60
2. Destination warehouse: Days of Supply < 14
3. Transfer cost < (Stockout cost × Stockout probability)
```

## Reporting Templates

### Daily Inventory Report

| SKU | Current Stock | Days Supply | Status | Action |
|-----|---------------|-------------|--------|--------|
| | | | | |

### Weekly Performance Report

| Metric | This Week | Last Week | Trend |
|--------|-----------|-----------|-------|
| Fill Rate | | | |
| Stockout % | | | |
| Avg Days Supply | | | |
| Inventory Value | | | |
| Stock Turn (Ann.) | | | |

### Monthly Analysis

- Top 10 fast-moving SKUs
- Top 10 slow-moving SKUs
- Forecast vs. actual variance analysis
- Supplier performance scorecard
- Dead stock report
- Inventory valuation changes

## Integration Points

- **ERP:** Real-time stock levels
- **POS:** Sales velocity data
- **WMS:** Warehouse capacity
- **TMS:** Lead time updates
- **Supplier Portal:** Order status
- **E-commerce Platform:** Availability sync
