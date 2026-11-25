---
name: cost-planning-value-engineering
description: Support architectural cost planning, quantity-based option comparison, value engineering and life-cycle tradeoff analysis using traceable quantities and cost sources. Use for early cost plans, option deltas, budget reconciliation, VE workshops and scope prioritization.
---

# Cost Planning & Value Engineering

Provide transparent estimates and option logic; keep professional quantity surveying/cost certification outside the skill.

## Preflight

- Area/quantity basis, design stage, location/currency/base date, procurement assumptions, inflation/escalation basis, allowances and exclusions.
- Latest cost plan or benchmark sources and defined client budget.

Keep verified facts, project assumptions, design options, and unresolved questions visibly separate. If a required input is absent, record it as `UNKNOWN` rather than inventing it.

## Workflow

1. Freeze a quantity/area baseline and map cost drivers to systems/elements rather than arbitrary percentages.
2. Use sourced unit rates/ranges and state base date, currency, taxes/fees, contingency and escalation treatment.
3. Compare options by cost delta plus performance/design/program consequences; avoid cost-only optimization.
4. Track accepted/rejected VE items, design impacts and required drawing/spec changes.

## Deliverables

- Cost-plan assumptions sheet
- Element/option cost matrix
- VE register with consequences
- Budget reconciliation and unknowns

## Verification

- Quantities reconcile with area/quantity audits and cost sources are dated/location-specific.
- Ranges and uncertainty widen appropriately for earlier stages.

For file/model changes, compare the result against a pre-change baseline and report changed items, skipped items, failures, and checks actually run.

## Professional boundaries

- Do not present estimates as tenders, final accounts or professional QS certification.
- Do not invent current market rates or contractor pricing.

If a live CAD/BIM/GIS/analysis tool or MCP integration is available, inspect the current document/model and tool version before write operations. Prefer read-only inspection, dry runs, bounded samples, new output paths, and native undo/transaction mechanisms. Never claim a model or drawing was changed unless the tool confirms it.

If the native application is unavailable, produce a reproducible plan, script, structured data, SVG/DXF artifact, or exact in-application procedure instead of pretending to have operated the software.
