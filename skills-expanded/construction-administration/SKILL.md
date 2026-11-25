---
name: construction-administration
description: "Support architectural construction-phase administration: RFIs, submittals/shop drawings, site observations, architect instructions, change tracking, payment-support records, punch/defects lists and as-built coordination. Use during tender clarification, construction, commissioning and closeout."
---

# Construction Administration

Maintain a factual project record and route contractual/legal determinations to the responsible professional.

## Preflight

- Contract/delivery context, issued drawing/spec revision, RFI/submittal/change logs, meeting/site records and defined architect authority.
- Response deadlines, responsible parties and whether the item affects cost/time/design/safety.

Keep verified facts, project assumptions, design options, and unresolved questions visibly separate. If a required input is absent, record it as `UNKNOWN` rather than inventing it.

## Workflow

1. Classify incoming item, link it to contract/issued information and identify affected disciplines/drawings/specs.
2. Draft concise response or review comments that answer only within the architect's authority; distinguish clarification from design change.
3. Track status, responsible party, dates, superseded information and downstream drawing/model/spec updates.
4. For site observations/punch lists, record location, evidence, required action and verification status without asserting unseen conditions.

## Deliverables

- RFI response draft
- Submittal/shop-drawing review comments
- Change/decision log
- Site observation or punch-list record
- Closeout/as-built action list

## Verification

- Every response references the correct current issue/revision and does not conflict with prior decisions.
- Changes propagate to affected documentation and responsibility/status remain visible.

For file/model changes, compare the result against a pre-change baseline and report changed items, skipped items, failures, and checks actually run.

## Professional boundaries

- Do not give legal advice, certify payment, accept nonconforming work, direct contractor means/methods, or make safety determinations outside the user's authority.
- Urgent life-safety/site hazards must be escalated to responsible professionals.

If a live CAD/BIM/GIS/analysis tool or MCP integration is available, inspect the current document/model and tool version before write operations. Prefer read-only inspection, dry runs, bounded samples, new output paths, and native undo/transaction mechanisms. Never claim a model or drawing was changed unless the tool confirms it.

If the native application is unavailable, produce a reproducible plan, script, structured data, SVG/DXF artifact, or exact in-application procedure instead of pretending to have operated the software.
