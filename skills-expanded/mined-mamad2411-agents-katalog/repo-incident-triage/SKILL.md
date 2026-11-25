---
name: repo-incident-triage
description: Guides safe incident investigation, timeline creation, mitigation planning, rollback evaluation, customer-impact analysis, and risky operational command review. Use when responding to alerts, outages, degradations, production failures, emergency rollbacks, or incident follow-up.
---

# Repository Incident Triage

Use this skill during incident investigation, outage response, alert triage, emergency rollback, or production-adjacent mitigation planning.

## When to Use This Skill

Use this skill for:

- active incident response
- alert investigation
- service degradation or outage triage
- emergency rollback planning
- mitigation command review
- incident timelines
- customer-impact analysis
- follow-up action planning

## Triage Process

1. State known symptoms and scope.
2. Confirm environment, service, region, account, tenant, cluster, or deployment target.
3. Build a timeline using `resources/incident-roles-and-timeline.md`.
4. Prefer read-only diagnostics first.
5. Separate hypotheses from evidence.
6. Identify immediate mitigation options and risks.
7. Ask for approval before mutating production-like systems.
8. Verify recovery using user-impact signals.
9. Record follow-up actions and detection gaps.

## Workflow

Use `workflows/incident-triage-workflow.md` for incident investigation and mitigation planning.

## Scripts

This skill owns:

```text
scripts/guard-incident-command.py
```

The root-level `hooks.json` calls this script before `run_command`. Run it with `--help` before manual use.
