---
name: warehouse-operations
description: Warehouse operations — receiving and putaway, slotting, picking and packing workflows, pick-path and layout optimization, throughput and bottleneck analysis, cycle counting and inventory accuracy, labor planning, warehouse KPIs (pick rate, order accuracy, dock-to-stock time). Use for warehouse layout, picking efficiency, fulfillment throughput, or inventory accuracy problems. For carrier selection or shipment exceptions, prefer the logistics skills.
---

# Warehouse Operations (receive → putaway → pick → pack → ship)

## KPIs — define before optimizing

```
pick rate          = lines (or units) picked / labor hour
order accuracy     = orders shipped without error / orders shipped   (target ≥ 99.5% — rule of thumb)
dock-to-stock      = truck arrival → sellable/pickable location      (hours, not days)
inventory accuracy = locations counted correct / locations counted   (by location, not by value)
order cycle time   = order released → shipped
cost per order     = total warehouse labor+space cost / orders shipped
```

Report rates with their denominator (lines vs units vs orders) — mixing denominators between
periods is how "productivity improvements" get invented.

## Slotting and layout

- **Velocity slotting**: A-movers (top ~20% SKUs ≈ 80% of picks) go in the golden zone —
  waist-to-shoulder height, closest to pack-out. Re-slot on a cadence (monthly/seasonal);
  slotting decays as the product mix shifts.
- Store correlated items (frequently co-ordered) near each other; separate look-alike SKUs
  that cause mispicks.
- Replenishment must be a separate flow from picking (different aisles/times); pickers waiting
  on replenishment is a top hidden throughput loss.
- Layout test: walk the actual pick path of the 10 most common order profiles. Travel is
  typically ~50% of pick labor — layout wins come from cutting steps, not from picking faster.

## Picking methodology — match to order profile

| Profile | Method |
|---|---|
| Few large multi-line orders | discrete (one order per trip) |
| Many small orders, few lines each | batch picking (N orders per trip), sort at pack |
| Very high volume, stable zones | zone picking with pass-along or wave consolidation |

Changing the picking method usually beats micro-optimizing the current one — but it changes
pack-out and error modes, so pilot one zone first.

## Receiving and putaway

- Dock-to-stock is a throughput KPI, not an afterthought: unputaway pallets are invisible
  inventory (system says available, pickers can't find it).
- Directed putaway (system assigns location) over memory-based; every exception ("put it
  wherever") becomes a future cycle-count error.

## Inventory accuracy: cycle counting over wall-to-wall

- Count a rotating sample daily (A items more often than C); investigate every discrepancy to
  root cause (receiving error, mispick, unrecorded damage) — the count fixes the number, the
  root cause fixes the process.
- Accuracy measured by location and quantity; value-weighted accuracy hides many small errors
  that each kill a customer order.

## Labor planning

- Forecast volume (orders, lines) per day/shift from sales seasonality; convert with measured
  rates per function (receive, putaway, pick, pack), include indirect time (~15–20%: meetings,
  cleanup, equipment) and absence.
- Cross-train for peak: the flex pool between functions is the cheapest surge capacity.

## Failure modes — what wrong looks like

- Optimizing pick speed while travel dominates: effort where the loss isn't.
- Slotting done once and never refreshed; last year's A-movers occupy the golden zone.
- Batch size raised until pack-out becomes the new bottleneck — throughput unchanged, WIP up.
- Cycle counts that adjust quantities without root-causing discrepancies: accuracy decays back
  within weeks.
- KPI gaming: pick rate up because easy single-line orders were cherry-picked; order cycle
  time for the rest got worse.

## Reviewer checklist

- [ ] Every KPI has an explicit denominator and a measured baseline
- [ ] Bottleneck identified from flow data (receive→ship), not assumed to be picking
- [ ] Layout/slotting recommendation quantifies travel reduction for real order profiles
- [ ] Picking method matches the order profile table; changes piloted, not big-banged
- [ ] Cycle counting includes root-cause investigation, not just quantity adjustment
- [ ] Labor plan includes indirect time and absence; peak plan names the flex source
- [ ] Rule-of-thumb figures (80/20 velocity, 99.5% accuracy) labeled as such

Provenance: standard warehousing practice (velocity slotting, batch/zone picking, cycle
counting); numeric targets are rules of thumb — derived, unverified for any specific operation.
