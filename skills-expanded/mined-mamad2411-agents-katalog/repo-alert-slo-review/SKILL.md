---
name: repo-alert-slo-review
description: Reviews alerts, monitors, SLOs, paging rules, severity mapping, dashboard links, runbook links, noise risk, and operational gates. Use when creating or changing alerting, service-level objectives, monitoring thresholds, or incident detection behavior.
---

# Repository Alert and SLO Review

Use this skill when creating or reviewing alerts, monitors, SLOs, paging rules, and deployment or release gates.

## When to Use This Skill

Use this skill for:

- new alerts or monitors
- alert threshold changes
- SLO or SLI definitions
- paging, escalation, and notification rules
- dashboard and runbook links
- alert fatigue reduction
- incident severity classification
- deployment gates based on health signals

## Review Process

1. Identify the customer or operational impact represented by the alert.
2. Classify severity using `resources/alert-severity-matrix.md`.
3. Confirm the alert is actionable and owned.
4. Check for runbook, dashboard, query, and service ownership.
5. Review threshold, duration, burn rate, and evaluation window.
6. Check for duplicate or noisy alerts.
7. Verify that silencing, deleting, or weakening an alert has explicit approval and restoration instructions.

## Workflow

Use `workflows/alert-slo-review-workflow.md` for alert and SLO changes.

## Scripts

This skill owns:

```text
scripts/alert-config-scan.py
```

Run the script with `--help` before manual use.
