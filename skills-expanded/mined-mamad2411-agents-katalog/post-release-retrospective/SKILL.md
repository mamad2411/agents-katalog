---
name: post-release-retrospective
description: Use after a production promotion to capture release outcomes, lessons, stabilisation findings, and follow-up actions in a durable artifact.
---

# Post-Release Retrospective

## Specialization

Produce a structured retrospective artifact after a production promotion: what was released, how the release executed against plan, what went well, what did not, stabilisation observations, and a prioritised follow-up action list.

This skill closes the release feedback loop. It does not replay root-cause analysis for incidents (that belongs to `support-triage` and `defect-debugger`) — it captures the release-level story and turns observations into durable learning.

## Trigger Conditions

- A production promotion has completed and the team needs to close the release formally.
- Stabilisation monitoring has ended and findings need to be captured before the next delivery cycle begins.
- Release variance (schedule, scope, incidents) was high enough that a structured capture is warranted.
- A release review is needed before the next initiative plan is approved, and the review should reference prior release history.

## Inputs

- Release ID or version identifier.
- Release plan or release notes document (pre-promotion scope).
- Actual scope delivered: included, deferred, and descoped items.
- Incident or defect log from the promotion window and early-life period.
- Approval and sign-off record from `release-readiness`.
- Originating plan or workstream ID for traceability.

## Required Outputs

| Output | Description |
|---|---|
| Release outcome summary | What was released vs. planned: scope included, deferred, descoped. Timeline variance (if applicable). |
| Execution assessment | How the release executed against the plan: gate pass/fail counts, incident count by severity, rollback triggered (Y/N). |
| What went well | Named observations about practices, sequencing, or tooling that reduced release risk or improved execution quality. |
| What to improve | Named observations about gaps, surprises, or failures with severity and a recommended change. |
| Stabilisation findings | Observations from the early-life period: production signals, unexpected behaviour, or monitoring gaps surfaced. |
| Follow-up action list | Prioritised actions arising from the retrospective. Each with: description, owner, priority (Critical / High / Medium), and target date. |

## Workflow

1. Confirm the release ID and link to the originating plan or workstream ID.
2. Compare planned scope vs. delivered scope: list included, deferred, and descoped items with reasons.
3. Assess execution: count gate outcomes, incidents, and note whether rollback was triggered.
4. Run the retrospective: collect observations under What went well and What to improve. Source observations from the release team, on-call record, and monitoring dashboards.
5. Capture stabilisation findings: review the early-life period (minimum 24–72 hours or as defined by SLA) for unexpected signals.
6. Prioritise follow-up actions: convert the What to improve and stabilisation findings into an action list with named owners.
7. Record the artifact with release ID and plan or workstream ID for future reference.

## Timing Guidance

- Conduct within 5 business days of the end of the defined early-life support window.
- Do not defer retrospectives until the next release — findings lose fidelity rapidly.
- If an incident required root-cause analysis, include a reference to the incident record rather than re-analysing inline.

## Done Criteria

- Release outcome summary covers planned vs. delivered scope.
- Execution assessment includes gate outcomes and incident count.
- At least one observation in What went well and one in What to improve (or an explicit statement that none were identified).
- Stabilisation findings present (may note "none observed" if the period was clean).
- Follow-up action list with at least one owner-assigned item per High or Critical finding.
- Release ID and originating plan ID recorded on the artifact.

## Guardrails

- Do not conflate retrospective observations with root-cause analysis — reference incident records, do not duplicate them.
- Do not defer a retrospective indefinitely because the team is busy — a lightweight capture is better than none.
- Follow-up actions must have named owners; anonymous actions are not actionable.

## References

- Related skills: `release-readiness`, `support-triage`, `acceptance-governance`, `delivery-status-grid`
