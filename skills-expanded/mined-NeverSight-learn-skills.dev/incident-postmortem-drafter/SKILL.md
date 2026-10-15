---
name: incident-postmortem-drafter
description: Vendor-neutral skill to draft a blameless incident postmortem from structured incident inputs (timeline, impact, contributing factors) and produce an actionable report.
---

## When to invoke
- You have an outage/incident timeline and need a consistent postmortem draft.
- You want to standardize incident write-ups across teams.

## Inputs needed
- Incident metadata: title, date/time, duration, severity.
- Impact summary: customer impact, internal impact, key metrics.
- Timeline of events (timestamp + event).
- Contributing factors (optional) and what went well/poorly.
- Action items (optional; can be generated placeholders).

## Workflow
1. Validate required fields and normalize timestamps.
2. Derive key milestones (start, detection, mitigation, resolution).
3. Summarize impact and customer communication.
4. Generate a blameless narrative: what happened and why (avoid personal attribution).
5. Produce corrective and preventive actions (CPAs) with owners and due dates if provided; otherwise create placeholders.

## Output format
Markdown report with:
- Summary
- Customer impact
- Timeline
- Root cause / contributing factors (blameless)
- Detection and response analysis
- What went well / what didn’t
- Action items (table)
- Follow-ups and references

## Guardrails
- Do not assign blame to individuals; focus on systems and process.
- If inputs are missing, call them out explicitly rather than inventing facts.
- Keep timestamps and units consistent.

## Reference code
- `postmortem_drafter.py` reads a JSON incident file and writes a Markdown postmortem.
