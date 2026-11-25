---
name: governance-delivery
description: Use when a delivery initiative spans multiple disciplines or teams and needs dependency mapping, milestone tracking, RAID log management, and delivery coordination.
---

# Delivery Governance

## Specialization

Produce and maintain the delivery coordination artifacts for a multi-discipline initiative: a RAID log, a dependency map, a milestone list, and a status update template.

This skill is the primary owner of Project Management lane work. It does not make product scope decisions — it tracks the delivery structure that enables those decisions to land on time.

## Trigger Conditions

- A delivery initiative spans more than one discipline or team and dependencies must be mapped.
- A milestone or sprint plan exists but RAID management is absent or informal.
- A delivery review is needed and status must be reported in a structured, consistent format.
- Escalation paths for blockers are undefined or unowned.

## Inputs

- Initiative name and originating plan or workstream ID.
- Participating disciplines and named owners per discipline.
- Known milestones, target dates, and success criteria.
- Known dependencies, risks, assumptions, and issues (seed list — may be empty).

## Required Outputs

| Output | Description |
|---|---|
| RAID log | Risks, Assumptions, Issues, Dependencies — each item has: ID, category, description, owner, status, and target resolution date. |
| Dependency map | Table of cross-discipline dependencies: producing discipline, consuming discipline, artifact or decision required, and current status. |
| Milestone list | Named milestones with target dates, owners, entry criteria, and exit criteria. |
| Status update template | Reusable template for delivery reporting: milestone status, new blockers, resolved items, and next checkpoint. |

## Workflow

1. Confirm initiative scope and link to originating plan or workstream ID.
2. Seed the RAID log: extract known risks, assumptions, issues, and dependencies from inputs. Assign owners and initial status.
3. Build the dependency map: for each discipline pair, identify artifacts or decisions that must transfer and their current readiness.
4. Define milestones: confirm named checkpoints with target dates and entry/exit criteria for each.
5. Validate ownership: every RAID item and every milestone must have a named owner.
6. Produce the status update template: structure it for the reporting cadence used by the initiative.
7. Schedule the next RAID review: identify the trigger (date or event) that prompts the next update.

## RAID Item Classifications

| Category | Examples |
|---|---|
| Risk | Schedule risk, capability gap, dependency delay, scope ambiguity. |
| Assumption | Assumed availability, assumed environment readiness, assumed scope boundary. |
| Issue | Active blocker, defect with delivery impact, failed dependency. |
| Dependency | Cross-discipline artifact, external decision, environment or tooling readiness. |

## Done Criteria

- RAID log is populated with at least the seed items, each with a named owner and status.
- Dependency map covers all identified cross-discipline handoffs.
- Milestone list has target dates, owners, and entry/exit criteria.
- Status update template is present and structured for the reporting cadence.

## References

- Related skills: `delivery-status-grid`, `writing-plans`, `analysis-execution`
