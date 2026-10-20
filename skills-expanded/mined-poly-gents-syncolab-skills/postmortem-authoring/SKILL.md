---
name: postmortem-authoring
description: Authors blameless incident and defect postmortems with timeline, impact, root cause, and corrective actions. Use after incidents or for formal defect write-ups.
---

# Postmortem authoring

## Purpose

Produce a blameless, evidence-based postmortem suitable for stakeholders and future search—grounded in logs, deploys, and metrics, not speculation.

## When to Use

- User asks for incident postmortem, RCA document, or defect write-up.
- After mitigation when timeline and impact need formal capture.
- Publishing to docs/tickets via **google-docs**, **github**, or **jira**.

## When NOT to Use

- Active incident command → **lead-incidents**, **coordinate-incidents** first.
- Threat design review → **threat-modeling**.
- Skill repo authoring → **create-skill** / **publish-skill**.

## Expected Outcome

- Complete postmortem draft with required sections and explicit unknowns.
- Corrective actions with owners and dates when provided.
- UTC timeline aligned to evidence sources.

## Inputs to Gather

- Incident window (UTC), severity, and services affected.
- Alerts, deploys, feature flags, and key log/metric links.
- Customer/revenue/SLO impact estimates.
- Existing tickets or chat threads.

## Workflow

1. Collect evidence (alerts, deploys, dashboards) before drafting narrative.
2. Build UTC timeline with source citations.
3. Draft sections below; mark gaps as unknown.
4. Separate proximate vs contributing causes without blaming individuals.
5. Propose corrective actions (quick wins + systemic); request owners/dates.
6. Review for blameless language and sensitive data redaction.

## Domain guidance

Produce a **blameless** document suitable for stakeholders and future search.

### Sections

1. **Summary** — what broke, for whom, how long.
2. **Timeline** — evidence-based (logs, deploys, alerts), UTC.
3. **Impact** — users, revenue, SLOs, data.
4. **Root cause** — mechanism, not individuals; proximate vs contributing.
5. **Detection** — why it was not caught earlier.
6. **Mitigation** — what stopped the bleeding.
7. **Corrective actions** — owned, dated; quick wins and systemic fixes.

Stay factual; mark unknowns explicitly.

## Tool Availability Rules

| Access | Behavior |
|--------|----------|
| Full tool access | Pull evidence from connected tools; publish doc if asked. |
| Read-only | Draft from user-provided evidence only. |
| No integration | Draft structure; user supplies links and timestamps. |

### Related tool sets

- `jira`
- `github`
- `google-docs`

## Review / Decision / Execution Criteria

- Every timeline entry traceable to a source.
- Corrective actions are SMART where possible.
- No naming individuals as root cause.

## Output Format

Markdown or doc-ready sections per template above, plus optional one-paragraph executive summary.

## Quality Bar

- Suitable for exec + engineering audiences.
- Distinguishes facts, hypotheses, and unknowns.

## Safety and Boundaries

- Redact customer PII and secrets from excerpts.
- Do not fabricate deploy times or metric values.

## Escalation / Dispatch Rules

- SLO policy implications → **error-budget-management**.
- Ongoing reliability work → **monitor-slos**.

## References

- `skills/old_skills.json` (`postmortem-authoring`).
- `skills/skill.instruction.md`, `skills/meta.instructions.md`
