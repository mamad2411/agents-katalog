---
name: handover-fm-postoccupancy
description: Coordinate architectural handover, closeout, asset information, O&M manuals, warranties, training, commissioning records, defects, BIM/COBie-style asset data, facilities-management handoff and post-occupancy evaluation. Use from practical completion through building operation.
---

# Handover, FM & Post-Occupancy

Turn project information into an auditable owner/FM handover and feedback loop.

## Preflight

- Contract closeout requirements, asset information requirements, commissioning plan, O&M/warranty inputs, as-built models/drawings and FM system requirements.
- Outstanding defects, training requirements, seasonal commissioning and post-occupancy goals.

Keep verified facts, project assumptions, design options, and unresolved questions visibly separate. If a required input is absent, record it as `UNKNOWN` rather than inventing it.

## Workflow

1. Build a closeout deliverable matrix with owner, format, responsible party and acceptance status.
2. Reconcile as-built drawings/models, asset tags, spaces/equipment, manuals, warranties and commissioning evidence.
3. Track defects/punch closure and unresolved operational risks; do not mark complete from paperwork alone when physical verification is required.
4. Plan user/FM training, seasonal review and post-occupancy evaluation; feed lessons back into project standards.

## Deliverables

- Handover/closeout matrix
- Asset-information QA report
- Defect/commissioning status
- FM training and post-occupancy plan

## Verification

- Asset IDs, locations and documents cross-reference correctly and required files open in their target systems.
- As-built status is based on verified records, not design intent alone.

For file/model changes, compare the result against a pre-change baseline and report changed items, skipped items, failures, and checks actually run.

## Professional boundaries

- Do not certify commissioning or practical completion outside the user's contractual authority.
- Protect sensitive building/security and occupant data in handover datasets.

If a live CAD/BIM/GIS/analysis tool or MCP integration is available, inspect the current document/model and tool version before write operations. Prefer read-only inspection, dry runs, bounded samples, new output paths, and native undo/transaction mechanisms. Never claim a model or drawing was changed unless the tool confirms it.

If the native application is unavailable, produce a reproducible plan, script, structured data, SVG/DXF artifact, or exact in-application procedure instead of pretending to have operated the software.
