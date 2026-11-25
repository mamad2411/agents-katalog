---
name: logistics-review
description: >
  Review logistics operations including route optimization, carrier performance, cost benchmarking,
  lead time analysis, and last-mile delivery assessment.
  TRIGGER when: user says /logistics-review, "review logistics", "shipping analysis", "freight audit", "carrier review", "transportation analysis".
argument-hint: "[lane/region] [carrier] [time-period]"
user-invocable: true
---

# Logistics Review

Evaluate and improve logistics operations across the transportation network to reduce cost, improve service reliability, and increase visibility.

---

## Input Gathering

| Input                      | Description                                                  | Required |
|----------------------------|--------------------------------------------------------------|----------|
| Shipment data              | Origin, destination, weight, mode, carrier, cost, dates      | Yes      |
| Carrier contracts          | Rate cards, accessorial schedules, SLA commitments           | Yes      |
| Time period                | Review window (recommend minimum 6 months)                   | Yes      |
| Delivery performance data  | Promised vs. actual delivery dates, damage/claim records      | Yes      |
| Network map                | Warehouse/DC locations, customer density, lane volumes        | No       |
| Benchmark data             | Industry rates, peer comparisons, market indices              | No       |
| Customer requirements      | Delivery windows, special handling, compliance mandates       | No       |

---

## Step-by-Step Process

### Step 1 — Shipment Profile Analysis

Build a complete picture of the logistics operation:

| Dimension            | Analysis                                              |
|----------------------|-------------------------------------------------------|
| Mode split           | % of spend and volume by TL, LTL, parcel, air, ocean |
| Lane concentration   | Top 20 lanes by volume and spend; Pareto analysis     |
| Shipment density     | Average weight, cube utilization, pieces per shipment  |
| Temporal patterns    | Day-of-week, monthly, seasonal volume fluctuations     |
| Geographic coverage  | Heat map of origin-destination pairs, delivery zones   |

Flag anomalies: shipments below minimum weight, excessive accessorials, split shipments that could consolidate.

### Step 2 — Carrier Performance Scorecard

Score each carrier on a weighted composite:

| KPI                        | Weight | Measurement                               | Target        |
|----------------------------|--------|-------------------------------------------|---------------|
| On-time delivery (OTD)     | 30%    | Delivered within promised window           | > 95%         |
| Damage / claims rate       | 15%    | Claims filed per 1,000 shipments           | < 2           |
| Invoice accuracy           | 15%    | % of invoices matching contracted rates    | > 98%         |
| Tender acceptance rate     | 15%    | % of loads accepted on first tender        | > 90%         |
| Transit time consistency   | 15%    | Std deviation of transit days per lane      | Low variance  |
| Responsiveness             | 10%    | Time to resolve exceptions and inquiries    | < 4 hours     |

Produce a quarterly ranking and identify carriers eligible for volume increase or reduction.

### Step 3 — Cost Benchmarking and Spend Analysis

Analyze logistics spend against benchmarks:

- **Cost per unit shipped** (by mode and lane).
- **Cost as % of revenue** — compare to industry median (typically 4-8% for manufacturing, 8-15% for e-commerce).
- **Accessorial spend breakdown** — fuel surcharge, detention, liftgate, residential, redelivery.
- **Rate trend analysis** — contracted rates vs. spot market over the review period.
- **Spend leakage** — shipments moving outside contracted rates, unauthorized carriers, off-contract accessorials.

Build a savings waterfall identifying each opportunity by category and estimated annual value.

### Step 4 — Lead Time Analysis

Map end-to-end lead times for key lanes:

| Lead Time Component      | Measurement                      | Optimization Lever            |
|--------------------------|----------------------------------|-------------------------------|
| Order processing         | Order placed to ship-ready       | Automation, cut-off times     |
| Warehouse dwell          | Ship-ready to carrier pickup     | Pickup scheduling, dock slots |
| Transit time             | Pickup to destination arrival    | Mode selection, routing       |
| Customs / clearance      | Border arrival to release        | Pre-clearance, broker perf    |
| Last-mile delivery       | Hub arrival to customer receipt  | Network design, carrier mix   |
| **Total order-to-delivery** | **Sum of above**              | **Process redesign**          |

Identify the longest and most variable components; quantify the opportunity from reducing each by 10-25%.

### Step 5 — Last-Mile Delivery Assessment

Evaluate last-mile performance specifically:

- **Cost per delivery** by zone, package size, and delivery type (standard, express, same-day).
- **First-attempt delivery success rate** — target > 92%.
- **Customer satisfaction scores** tied to delivery experience.
- **Returns logistics cost** — reverse logistics as % of forward cost.
- **Alternative delivery model evaluation** — gig economy, locker networks, micro-fulfillment, crowd-shipping.

### Step 6 — Recommendations and Action Plan

Prioritize opportunities using an impact-effort matrix:

| Priority | Initiative                       | Annual Savings | Effort | Timeline     |
|----------|----------------------------------|----------------|--------|--------------|
| 1        | Quick wins (rate corrections)    | $...           | Low    | 0-30 days    |
| 2        | Carrier mix optimization         | $...           | Medium | 30-90 days   |
| 3        | Mode shift opportunities         | $...           | Medium | 60-120 days  |
| 4        | Network redesign                 | $...           | High   | 6-12 months  |

---

## Output Format

```
## Logistics Review — [Scope/Region] — [Period]

### Executive Summary
- Total logistics spend reviewed: [$X]
- Shipments analyzed: [count]
- Identified savings opportunities: [$Y] ([%] of spend)
- Service level: [current OTD%] -> [projected OTD%]

### Shipment Profile
| Mode   | Shipments | Spend     | Avg Cost/Shipment | Volume Trend |
|--------|-----------|-----------|-------------------|--------------|
| TL     | ...       | ...       | ...               | ...          |
| LTL    | ...       | ...       | ...               | ...          |
| Parcel | ...       | ...       | ...               | ...          |

### Carrier Scorecard
| Carrier | OTD   | Damage Rate | Invoice Accuracy | Tender Accept | Composite Score |
|---------|-------|-------------|------------------|---------------|-----------------|
| ...     | ...   | ...         | ...              | ...           | ...             |

### Cost Benchmarking
- Cost per unit shipped: [$X] vs. benchmark [$Y]
- Accessorial spend: [%] of total (target: < 15%)
- Savings waterfall: [chart or table]

### Lead Time Breakdown
| Component         | Current (days) | Target (days) | Gap   |
|-------------------|----------------|---------------|-------|
| Order processing  | ...            | ...           | ...   |
| Transit           | ...            | ...           | ...   |
| Last mile         | ...            | ...           | ...   |

### Recommendations (Prioritized)
1. [Initiative — savings — timeline]
2. ...
```

---

## Quality Checklist

- [ ] Shipment data validated for completeness (no missing lanes, costs, or dates)
- [ ] Carrier scorecard uses weighted composite, not a single metric
- [ ] Cost benchmarks sourced from current market data or industry reports
- [ ] Accessorial charges broken out and anomalies flagged
- [ ] Lead time analysis covers end-to-end, not just transit
- [ ] Last-mile assessment includes customer experience metrics
- [ ] Savings estimates are conservative and assumption-documented
- [ ] Recommendations prioritized by impact and feasibility
- [ ] Quick wins separated from structural changes
- [ ] Stakeholder review scheduled for findings presentation

---

## Edge Cases

- **Multi-modal shipments (e.g., ocean + truck)**: Analyze each leg separately; attribute cost and transit time per segment; watch for dwell time at transshipment points.
- **Cross-border / international lanes**: Include customs brokerage, duties, and compliance costs; factor in trade agreement impacts and tariff changes.
- **Peak season vs. off-peak distortion**: Normalize metrics by season; benchmark peak performance separately; evaluate surge capacity strategy.
- **Small parcel high-volume shippers**: Focus on zone skipping, regional carrier diversification, and dimensional weight optimization.
- **Dedicated fleet vs. common carrier**: Run total cost of ownership comparison including fixed fleet costs, empty miles, and driver utilization.
- **Fragile or hazardous goods**: Assess specialized carrier performance separately; include regulatory compliance cost in benchmarking.
