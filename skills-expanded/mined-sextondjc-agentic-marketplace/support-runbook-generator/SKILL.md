---
name: support-runbook-generator
description: Use when producing support runbooks, escalation guides, and handoff packets for operational teams with consistent structure and actionable resolution steps.
---

# Support Runbook Generator

## Specialization

Produce support runbooks, escalation guides, and handoff packets from failure mode analysis, alert definitions, and system knowledge. Each runbook is structured so that a support engineer can triage, diagnose, and resolve — or escalate — without requiring additional context from the development team.

This skill complements `operability-design`: operability-design defines what must exist; this skill produces the runbook documents themselves. It does not implement monitoring infrastructure or alerting pipelines — it authors the human-readable operational procedures that those signals trigger.

## Trigger Conditions

- A feature or system is approaching release and runbooks do not exist or are too abstract to act on.
- Operability design has produced a failure mode list and alert matrix that need to be turned into runbooks.
- An on-call team is receiving a support handoff and needs structured, executable procedures.
- Existing runbooks are outdated, too high-level, or missing diagnosis and escalation steps.
- A post-release retrospective identified runbook gaps that blocked incident resolution.

## Inputs

- Failure mode list or operability requirements from `operability-design` (preferred) or direct system description.
- Alert matrix: alert names, trigger conditions, severities, and expected response owners.
- System architecture overview: key components, dependencies, and known fragility points.
- Escalation path: on-call team, engineering contacts, and escalation criteria.
- Originating plan or workstream ID for traceability.

## Required Outputs

| Output | Description |
|---|---|
| Runbook set | One runbook per significant failure mode or alert condition. Each runbook follows the standard template below. |
| Escalation guide | Standalone guide defining escalation criteria, the escalation chain by severity, and required information before escalation. |
| Runbook index | A single-page index listing all runbooks with their trigger alert or failure mode, severity, and a link or file reference. |
| Handoff packet summary | Condensed system overview, failure mode summary, runbook index, and primary contact list for support team onboarding. |

## Runbook Template

Each runbook must include:

| Section | Content |
|---|---|
| Title | Alert name or failure mode name. |
| Trigger | What event or alert fires this runbook. |
| Severity | Critical / High / Medium / Low. |
| Symptoms | What the support engineer observes: alert text, user impact description, log patterns. |
| Immediate actions | Steps to take in the first 5 minutes to stop the bleeding or prevent escalation. |
| Diagnosis steps | Ordered steps to identify root cause: what to check, what commands to run, what to look for. |
| Resolution steps | Actions to resolve the issue. Distinguish: self-service (L1), engineering-required (L2), vendor-required (L3). |
| Escalation criteria | When to stop attempting resolution and escalate. Who to contact. What information to include. |
| Recovery verification | How to confirm the issue is resolved. What signals to check. |
| Related runbooks | Cross-references to runbooks for related failure modes. |

## Workflow

1. Collect the failure mode list and alert matrix. If neither exists, derive failure modes from the system description.
2. Prioritise failure modes by severity and frequency. Start runbook authoring with Critical and High severity modes.
3. For each failure mode, draft the runbook following the standard template.
4. Draft the escalation guide: define L1/L2/L3 boundaries, escalation triggers, and required information.
5. Build the runbook index.
6. Assemble the handoff packet summary.
7. Review each runbook: verify that Immediate actions are doable without engineering access and that Diagnosis steps are specific enough to be followed under incident stress.
8. Record the originating plan or workstream ID on the output artifacts.

## Done Criteria

- At least one runbook per Critical or High severity failure mode.
- Every runbook follows the standard template with all sections populated.
- Escalation guide defines L1/L2/L3 boundaries and escalation contacts.
- Runbook index is present.
- Handoff packet summary is present.
- Originating plan or workstream ID on the output.

## Guardrails

- Do not write runbooks at a level of abstraction that requires the reader to consult the development team to execute the steps.
- Do not reference environment access or credentials inline — reference a separate secrets or access procedure.
- Immediate actions must be executable within 5 minutes without deep system knowledge; if they require deep expertise, move those steps to Diagnosis.

## References

- Related skills: `operability-design`, `support-triage`, `release-readiness`, `post-release-retrospective`

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
