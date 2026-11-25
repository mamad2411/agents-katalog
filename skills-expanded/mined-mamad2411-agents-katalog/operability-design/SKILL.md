---
name: operability-design
description: Use during DESIGN or IMPLEMENTATION when support readiness must be designed in — covers operability requirements, runbook design, observability hook specification, on-call readiness, and support handoff artifacts.
---

# Operability Design

## Specialization

Design and document the operational support layer for a system or feature: operability requirements, a runbook outline, an alert matrix, and a support handoff packet.

This skill ensures supportability is designed in, not bolted on after delivery. It serves Support discipline cells across all phases and the Release readiness gate. It does not implement monitoring infrastructure — it specifies what must exist before support accepts ownership.

## Trigger Conditions

- A feature or system is being designed or built and operational readiness has not been addressed.
- Runbooks do not exist or are too abstract to execute under incident conditions.
- An alerting strategy is undefined or does not map to actionable responses.
- A support handoff is approaching and the receiving team lacks the context to triage independently.
- Release readiness review identifies operability gaps.

## Inputs

- System or feature description: what it does, what can go wrong, and who uses it.
- Existing runbooks or operational docs (if any — empty is valid).
- Current alerting setup or target observability platform.
- Support team context: who will receive the handoff, what is their background, and what escalation path exists.
- Originating plan or workstream ID for traceability.

## Required Outputs

| Output | Description |
|---|---|
| Operability requirements list | Named requirements for observability, alerting, diagnosability, graceful degradation, and support tooling. Each with priority (Must / Should / Could) and owner. |
| Runbook outline | Structured runbook per failure mode: trigger, symptoms, immediate actions, diagnosis steps, resolution steps, and escalation path. |
| Alert matrix | Table of alert conditions: alert name, trigger condition, severity, response owner, and expected action. |
| Support handoff packet | Context document for the receiving support team: system overview, failure modes, runbook index, escalation path, and contact list. |

## Workflow

1. Map failure modes: identify the most probable and most impactful ways the system or feature can fail.
2. Define operability requirements: for each failure mode, specify the observability, alerting, and diagnosability requirements needed to detect and resolve it.
3. Draft runbook outlines: one runbook per significant failure mode. Include trigger, symptoms, actions, diagnosis, resolution, and escalation.
4. Build the alert matrix: for each observability requirement, define the alert condition, severity, and response owner.
5. Identify diagnosability gaps: list any failure modes that cannot currently be diagnosed from available signals.
6. Assemble the support handoff packet: system overview, failure mode summary, runbook index, escalation path, and contacts.
7. Validate completeness: confirm that every Must operability requirement has a corresponding runbook or alert entry.

## Failure Mode Coverage Checklist

- [ ] Service unavailability or health check failure
- [ ] Degraded throughput or elevated error rate
- [ ] Data pipeline or integration failure
- [ ] Authentication or authorisation failure
- [ ] Dependency failure (downstream service, database, queue)
- [ ] Data quality or consistency failure

## Done Criteria

- Operability requirements list is complete with priorities and owners.
- Runbook outline covers all identified Must failure modes.
- Alert matrix maps conditions to owners and actions.
- Support handoff packet is present and contains enough context for an independent triage.

## References

- Related skills: `release-readiness`, `ci-cd-workflows`, `governance-delivery`

## Execution Context

### Input Context

- Request objective and scope boundary.
- Applicable constraints and required outputs.

### Process Context

- Follow this skill's deterministic workflow from intake to closure.
- Record ownership and decisions for required outputs.

### Output Context

- Deliverables with explicit completion status.
- Residual risks and next actions.
## References Assets

- [Reference assets](./references/README.md)
