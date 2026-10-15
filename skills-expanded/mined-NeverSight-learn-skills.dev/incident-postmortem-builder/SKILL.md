---
name: incident-postmortem-builder
description: Use after a production incident to build a blameless postmortem. Pulls timeline from PagerDuty/Slack/observability, computes MTTD/MTTR, drafts impact, root cause, contributing factors, and action items.
---

# Incident Postmortem Builder

## When to invoke
- "Write the postmortem for INC-1234."
- "Draft a blameless postmortem from this Slack timeline."
- "Compute MTTD/MTTR for the May 3 outage."

## Inputs needed
1. **Incident ID / title**
2. **Timeline source** — Slack export, PagerDuty incident, or a CSV (timestamp,event,actor)
3. **Impact data** — affected services, % users, revenue impact (if known)
4. **Detected at / mitigated at / resolved at**

## Workflow
1. **Build timeline** — normalize timestamps, attach actors and sources.
2. **Compute metrics** — TTD, TTM, TTR, customer-minutes lost.
3. **Five-whys + contributing factors** — guided prompts; never blame people.
4. **Action items** — each must have owner, due date, type (prevent / detect / mitigate).
5. **Render** — Markdown postmortem ready for the doc.

## Output format
Standard SRE postmortem: Summary, Impact, Timeline, Detection, Response, Root cause, Contributing factors, What went well, What went wrong, Action items.

## Guardrails
- Blameless language — describe systems and decisions, never individuals.
- Every action item MUST have owner + due date + type.
- TTR/TTM/TTD must be computed from timestamps, never approximated.

## Reference code
`build.py` ingests a timeline CSV (or Slack export JSON) and renders the postmortem.
