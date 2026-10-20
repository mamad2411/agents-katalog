---
name: create-a-runbook
domain: business
locale: [generic]
interface: mixed
difficulty: intermediate
est_time: 30min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Create a runbook that gives an operator repeatable steps for handling a business workflow, support process, or operational incident.

## Preconditions

- The workflow or scenario is known.
- Current owners, systems, permissions, and escalation paths are available.
- You know where runbooks are stored.

## Steps

1. **Open the runbook location.** Create a document in the approved knowledge base, wiki, or shared folder. → *Expect:* a blank runbook draft is available.
2. **Name the scope.** Write the process name, when to use it, and when not to use it. → *Expect:* readers know the runbook's boundary.
3. **List prerequisites.** Add required access, tools, inputs, dashboards, and permissions. → *Expect:* operators can check readiness before starting.
4. **Write ordered steps.** Describe each action, expected observation, and handoff point. → *Expect:* the workflow can be followed without relying on memory.
5. **Add decision points.** Include branches for common conditions, severity levels, or customer states. → *Expect:* operators know how to choose paths.
6. **Add recovery paths.** Document common failures, detection signals, and escalation contacts. → *Expect:* operators can recover or escalate.
7. **Review with an owner.** Ask the process owner or experienced operator to verify the runbook. → *Expect:* obvious gaps are corrected before use.
8. **Publish and link it.** Save the runbook in the official location and link it from relevant tickets, trackers, or dashboards. → *Expect:* the runbook is findable during work.

## Decision points

- If the process is safety-critical or compliance-sensitive → require owner review before publishing.
- If steps differ by tool → use clearly labeled branches instead of mixing instructions.
- If the process is not yet stable → label the runbook draft and add a review date.

## Failure modes & recovery

- **F1 Missing prerequisite:** detect operators cannot start due to access or input gaps → recover by adding prerequisites and request paths.
- **F2 Ambiguous step:** detect different operators interpret a step differently → recover by rewriting with observable expected outcomes.
- **F3 Stale runbook:** detect screenshots, links, or owners are outdated → recover by updating content and last-reviewed metadata.

## Verification

The runbook has scope, prerequisites, ordered steps, decision points, failure recovery, owner review, publish location, and links from relevant work surfaces.

## Variations

- Support runbook: include customer reply templates and escalation rules.
- Project operations runbook: include cadence, tracker views, and reporting responsibilities.
- Incident runbook: include severity, communication channels, and rollback criteria.

## Safety & privacy

Low risk unless the runbook includes credentials, customer data, or incident procedures. Store secrets in approved secret systems, not in the runbook.
