# AI Incident Response Playbook

## Summary

**One-sentence:** Operational runbook for AI-system incidents — explicit steps with signals, thresholds, kill-switch and rollback paths, escalation contacts at top, drilled within 90 days.

**One-paragraph:** Generic SRE runbooks miss AI-specific decision points: when to flip a kill-switch on the model, when to fall back to a deterministic rule, when to rollback to a prior bundle, when to throttle. This methodology produces one runbook per AI feature with structured steps (input signal, threshold, action, post-condition, time budget), escalation block at the top, and a drill-completion-date stamp. Output is committed in the ops repo alongside the incident-tracker links.

**Ефективно для:** Команд, які на incident читають runbook і знаходять «check if things look bad» — і потім втрачають 20 хвилин на догадки; методологія примушує писати «error_rate > 2% AND p95 latency > 3s → kill-switch step 5», і одна людина о 3-й ранку це виконує без думання.

## Applies If (ALL must hold)

- AI feature is in production with monitoring (error rate, latency, cost dashboards).
- A kill-switch or rollback mechanism exists in code (no runbook for non-revertible systems).
- On-call rotation exists with at least 2 engineers.
- Owner can schedule a drill within 90 days.
- Incident tracker (Linear / GitHub / PagerDuty) integrates with the runbook.

## Skip If (ANY kills it)

- No production AI traffic (pre-launch).
- No kill-switch / rollback path — runbook would have no actions to take.
- Single-engineer project where escalation block is meaningless.
- One-off batch job with no live users.

## Prerequisites

| Artifact | Format | Source |
|---|---|---|
| Monitoring dashboards | URLs / IDs | Observability |
| Kill-switch endpoint | URL + auth scheme | Platform |
| Rollback bundle spec | from `agent-rollback-button-design` | Platform |
| Escalation contacts | name + handle + on-call shift | HR / on-call schedule |
| Incident tracker integration | issue template | Tools |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/agent-rollback-button-design/AGENTS.md` | Rollback mechanism the playbook calls into. |
| `geek/ai/ai-agents/agent-kill-switch-design/AGENTS.md` | Kill-switch endpoint the playbook references. |
| `geek/ai/ai-agents/ai-incident-postmortem-template/AGENTS.md` | Closes the loop after the incident. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 rules: explicit steps with budgets, signal+threshold branches, drill within 90 days, escalation at top | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the runbook | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns | ~900 |
| `content/04-procedure.xml` | medium | 5-step authoring procedure | ~900 |
| `content/05-examples.xml` | medium | Worked example: runbook for a hallucination incident class | ~1000 |
| `content/06-decision-tree.xml` | essential | Tree: severity? → contained? → kill-switch or rollback? → escalate or close | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract_monitoring_signals` | haiku | Structured pull from dashboards. |
| `author_steps` | sonnet | Per-step composition with thresholds. |
| `validate_runbook` | sonnet | Final composition. |
| `executive_review` | opus | For high-stakes services. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the runbook. |
| `templates/output.example.json` | Filled example. |
| `templates/runbook.md.j2` | Markdown skeleton with escalation header + step table. |
| `templates/runbook.md` | Markdown skeleton with escalation header + step table. Generated from `templates/runbook.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Validate the runbook. | After authoring, before publishing to ops repo. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/ai-agents/`
- peer: [[agent-kill-switch-design]] — kill switch invoked from step in runbook.
- peer: [[agent-rollback-button-design]] — rollback path used when kill-switch is insufficient.
- peer: [[ai-incident-postmortem-template]] — runbook completion triggers postmortem.

## Decision tree

See `content/06-decision-tree.xml`. Asks: (1) what is severity (sev-1/2/3)? (2) is the failure contained (single feature) or systemic? (3) is kill-switch sufficient or do we need rollback to prior bundle? Leaves point to the step path through the runbook.
