---
name: repo-issue-prioritization
description: Classifies issue severity, priority, labels, escalation needs, and release risk. Use when deciding impact, urgency, labels, milestones, release-blocking status, or whether an issue needs escalation.
---

# Repo Issue Prioritization

Use this skill when determining severity, priority, labels, milestones, escalation, or release-blocking status.

## Required Distinction

- Severity is impact.
- Priority is ordering.

## Inputs to Consider

- user or customer impact
- revenue, security, legal, or compliance risk
- production outage or degradation
- data loss or data integrity risk
- affected population
- frequency
- workaround
- release timing
- dependencies
- reversibility

## Workflow

Use `workflows/issue-prioritization-workflow.md`.

## Resources

- `resources/severity-priority-matrix.md`
- `resources/triage-label-taxonomy.md`
