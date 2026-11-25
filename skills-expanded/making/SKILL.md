---
name: making
description: Work with manufacturing orders, bills of materials, work orders, and quality checks. Use when the user mentions manufacturing, production, MRP, BOMs, work orders, maken, or productie.
triggers: [manufacturing, production, mrp, bom, stuklijst, work order, werkorder, maken, productie, assembly]
odoo_modules_any: [mrp, quality]
---

# Making

Turn components into finished goods using BOMs and work centers.

## Key models

- `mrp.bom` — bill of materials (kit, normal, or phantom)
- `mrp.bom.line` — component line
- `mrp.production` — manufacturing order (MO)
- `mrp.workorder` — work order (one per operation on a routing)
- `mrp.workcenter` — work station with capacity/cost
- `mrp.routing.workcenter` — operation on a routing
- `quality.check` — QC point tied to MO or picking

## Typical workflows

1. **Define BOM** → `mrp.bom` with `type = normal` (consume & produce) or `phantom` (kit, no MO)
2. **Plan MO** → create `mrp.production`, reserve components, schedule work orders
3. **Explode BOM** → recursive walk of sub-BOMs for material-requirements planning
4. **Execute** → mark components consumed (`_action_done`), record produced qty
5. **Quality** → trigger `quality.check` at operation, receipt, or shipping

## Gotchas

- Phantom BOMs don't create an MO — they just explode the kit into the parent's lines.
- `qty_producing` on the MO drives backflush; partial production is allowed.
- Routings moved into `mrp.bom.operation_ids` in recent versions — check your Odoo version.
- Cost rollup: component `standard_price` + work center cost-per-hour → finished `standard_price` (if FIFO/average enabled).
