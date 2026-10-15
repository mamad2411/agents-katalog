---
name: incident-postmortem-qa-checklist
description: Vendor-neutral skill to turn an incident timeline into a postmortem QA checklist and identify missing or weak evidence.
---

## When to invoke
- After an outage or incident, to ensure the postmortem is complete and actionable.
- During incident review, to highlight gaps in timeline, detection, impact, and follow-ups.

## Inputs needed
- Incident timeline as JSON events with timestamps and short descriptions.
- Optional metadata: service name, severity, start/end time, customer impact.

## Workflow
1. Validate timeline ordering and detect gaps (large time jumps, missing end time).
2. Classify events into phases: detection, triage, mitigation, recovery, follow-up.
3. Generate a checklist covering:
   - Impact statement and affected users
   - Detection signals and alerting
   - Root cause evidence and contributing factors
   - What worked / what didn’t
   - Action items with owners and due dates
4. Flag common quality issues:
   - No customer impact quantification
   - No clear trigger/root cause evidence
   - Action items missing owner or due date

## Output format
- JSON report:
  - `checks[]` list (id, status, rationale)
  - `timeline_analysis` (ordering, gaps)
  - `missing_evidence[]`

## Guardrails
- Do not invent incident facts; only infer checklist gaps from provided inputs.
- If timeline is too sparse, default to “needs more detail” statuses.

## Reference code
- `incident_postmortem_qa_checklist.py` reads timeline JSON and outputs checklist JSON.
