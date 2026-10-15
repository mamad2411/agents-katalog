---
name: incident-status-page-ops-review
description: Design and audit incident status page operations covering component taxonomy, incident declaration, public/private updates, subscriber notifications, templates, severity, SLO impact, customer segmentation, uptime history, maintenance windows, post-incident follow-up, support coordination, and trust-preserving communications. Use when reliability incidents need accurate external communication.
---

# Incident Status Page Ops Review

Use this skill to convert incident status page, public communication, subscriber notification, maintenance, component, and post-incident questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify product components, customer segments, incident severity, detection sources, SLO/customer impact, communication owners, support load, legal/security constraints, and current status page gaps.
2. Read `references/incident-status-page-ops-patterns.md`.
3. Classify communication as investigating, identified, monitoring, resolved, scheduled maintenance, degraded performance, partial outage, security-sensitive, or post-incident follow-up.
4. Define component taxonomy, declaration threshold, update cadence, template, approval path, subscriber channels, support coordination, and history/postmortem linkage.
5. Produce status-page ops plan, state machine, decision table, event schema, communication checklist, and incident drill plan.

## Guardrails

- Do not delay customer-visible incident acknowledgement until the root cause is fully known.
- Do not overstate uptime by hiding degraded components, regional impact, or partial outages.
- Do not publish sensitive security details, customer data, or speculative root cause without approval.
- Do not let support, status page, in-app banners, sales, and account teams send contradictory incident messages.

## Output format

```text
Status-page context:
Audience / source of truth / risk boundary:

Incident communication plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Components, updates, subscribers, and follow-up:
- <trigger> -> <policy, metric, edge case, support note>
```
