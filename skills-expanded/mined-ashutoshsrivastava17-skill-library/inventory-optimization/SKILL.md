---
name: inventory-optimization
description: >
  Optimize inventory levels through safety stock calculation, reorder points, ABC/XYZ classification,
  carrying cost analysis, and stockout risk assessment.
  TRIGGER when: user says /inventory-optimization, "optimize inventory", "safety stock", "reorder point", "inventory analysis", "stock levels".
argument-hint: "[product/SKU-group] [warehouse-or-location] [service-level-target]"
user-invocable: true
---

# Inventory Optimization

Right-size inventory across the network to maximize service levels while minimizing carrying costs, obsolescence risk, and working capital consumption.

---

## Input Gathering

| Input                        | Description                                                 | Required |
|------------------------------|-------------------------------------------------------------|----------|
| SKU master data              | Product list with unit cost, lead time, shelf life           | Yes      |
| Demand history               | Minimum 12 months of consumption or sales data               | Yes      |
| Current stock positions      | On-hand, in-transit, on-order by location                    | Yes      |
| Target service level         | Fill rate or cycle service level (e.g., 95%, 98%)            | Yes      |
| Lead time data               | Supplier lead times with variability                         | Yes      |
| Cost parameters              | Holding cost %, ordering cost per PO, stockout penalty cost  | No       |
| Storage constraints          | Warehouse capacity, shelf life limits, lot-size restrictions | No       |

---

## Step-by-Step Process

### Step 1 — ABC/XYZ Classification

Segment the portfolio on two dimensions:

**ABC (Value)** — based on annual revenue or cost of goods sold:

| Class | Share of Revenue | Typical SKU % | Management Approach       |
|-------|-----------------|---------------|---------------------------|
| A     | ~80%            | ~20%          | Tight control, frequent review |
| B     | ~15%            | ~30%          | Moderate control, periodic review |
| C     | ~5%             | ~50%          | Simple rules, exception-based |

**XYZ (Variability)** — based on coefficient of variation (CV) of demand:

| Class | CV Range   | Demand Pattern  | Forecast Reliability |
|-------|-----------|-----------------|----------------------|
| X     | 0 - 0.5   | Stable          | High                 |
| Y     | 0.5 - 1.0 | Variable        | Medium               |
| Z     | > 1.0     | Erratic         | Low                  |

Create a 3x3 matrix (AX, AY, AZ, BX, BY, BZ, CX, CY, CZ) and assign inventory policies per cell.

### Step 2 — Safety Stock Calculation

Calculate safety stock using the appropriate method for each segment:

| Segment | Method | Formula |
|---------|--------|---------|
| AX, BX  | Statistical | SS = Z x sqrt(LT x sigma_d^2 + d_avg^2 x sigma_LT^2) |
| AY, BY  | Statistical + buffer | SS = Z x sigma_demand_during_LT x (1 + buffer%) |
| AZ, BZ  | Simulation / min-max | Run Monte Carlo on demand and lead time distributions |
| CX      | Fixed weeks of supply | SS = avg_weekly_demand x weeks_target |
| CY, CZ  | Min-max with high max | Set min = max observed demand during LT x 1.2 |

Where:
- Z = service level Z-score (e.g., 1.65 for 95%, 2.05 for 98%)
- LT = average lead time
- sigma_d = standard deviation of demand
- sigma_LT = standard deviation of lead time

### Step 3 — Reorder Point and Order Quantity

- **Reorder Point (ROP)** = Average demand during lead time + Safety stock.
- **Economic Order Quantity (EOQ)** = sqrt(2 x D x S / H), where D = annual demand, S = ordering cost, H = holding cost per unit.
- Apply practical constraints: minimum order quantity (MOQ), pack sizes, container utilization, shelf-life limits.
- For expensive A-items, consider lot-for-lot ordering to minimize holding cost.

### Step 4 — Carrying Cost Analysis

Build a full cost-to-carry model:

| Cost Component          | Typical Range | Calculation Basis         |
|-------------------------|---------------|---------------------------|
| Capital / opportunity   | 8-15%         | WACC x average inventory value |
| Warehousing             | 2-5%          | Space, labor, utilities    |
| Insurance               | 0.5-1%        | Insured value              |
| Obsolescence / shrinkage| 2-10%         | Historical write-off rate  |
| **Total carrying cost** | **15-30%**    | Sum of above               |

Compare current vs. proposed inventory investment and quantify savings.

### Step 5 — Stockout Risk Assessment

For each SKU-location, calculate:

- **Probability of stockout per cycle** = 1 - Service Level achieved.
- **Expected stockout units** = integral of demand distribution beyond ROP during lead time.
- **Revenue at risk** = Expected stockout units x unit price x (1 - substitution rate).
- **Customer impact score** = Revenue at risk x customer criticality weight.

Rank SKUs by customer impact score and flag the top decile for immediate action.

### Step 6 — Policy Recommendations and Monitoring

- Set inventory policies (ROP, safety stock, review period) per ABC/XYZ segment.
- Define exception triggers: days of supply < threshold, excess > X weeks, slow-moving flag.
- Create a dashboard cadence: A-items reviewed weekly, B-items biweekly, C-items monthly.
- Establish an obsolescence review quarterly for items with < 60 days shelf life remaining or > 12 months of supply.

---

## Output Format

```
## Inventory Optimization Report — [Scope] — [Date]

### Executive Summary
- Total SKUs analyzed: [count]
- Current inventory value: [$X]
- Recommended inventory value: [$Y]
- Projected savings: [$Z] ([%] reduction)
- Service level impact: [current] -> [projected]

### ABC/XYZ Classification Summary
| Segment | SKU Count | Inventory Value | Revenue Share | Recommended Policy |
|---------|-----------|-----------------|---------------|--------------------|
| AX      | ...       | ...             | ...           | ...                |
| AY      | ...       | ...             | ...           | ...                |
| ...     | ...       | ...             | ...           | ...                |

### Safety Stock and Reorder Points (Top SKUs)
| SKU | Current SS | Proposed SS | ROP | EOQ | Days of Supply |
|-----|-----------|-------------|-----|-----|----------------|
| ... | ...       | ...         | ... | ... | ...            |

### Stockout Risk Register
| SKU | Stockout Probability | Revenue at Risk | Impact Score | Action |
|-----|----------------------|-----------------|--------------|--------|
| ... | ...                  | ...             | ...          | ...    |

### Recommendations
1. [Specific, actionable recommendations]
2. ...

### Implementation Roadmap
- [Week 1-2]: ...
- [Week 3-4]: ...
```

---

## Quality Checklist

- [ ] Demand data covers at least 12 months and is cleansed of stockout periods
- [ ] ABC/XYZ classification completed and validated with stakeholders
- [ ] Safety stock method appropriate for each segment's demand pattern
- [ ] Lead time variability captured (not just averages)
- [ ] Carrying cost rate reflects actual company cost structure
- [ ] Stockout cost includes both direct and downstream impact
- [ ] MOQ, lot size, and shelf-life constraints applied to order quantities
- [ ] Exception triggers defined for proactive monitoring
- [ ] Recommendations quantified with expected financial impact
- [ ] Review cadence established per segment

---

## Edge Cases

- **New SKU with no demand history**: Use analogous product demand profile; set conservative safety stock at 1.5x expected lead time demand until 3 months of actuals accumulate.
- **Highly seasonal products**: Calculate safety stock using within-season variability only; pre-build inventory using seasonal index.
- **Perishable goods with short shelf life**: Add shelf-life constraint to EOQ; reduce max stock to shelf-life minus lead time; implement FEFO (First Expired, First Out).
- **Long and variable lead times (e.g., overseas sourcing)**: Use lead-time demand distribution from simulation; consider dual sourcing to reduce effective variability.
- **Vendor-managed inventory (VMI)**: Shift analysis to consumption-based replenishment; share demand signals directly with supplier.
- **Promotional spikes**: Separate base and promotional demand; plan promotional inventory as a one-time forward buy outside the standard safety stock framework.
