---
name: repo-postmortem-and-runbook-writing
description: Writes and reviews blameless postmortems, incident timelines, operational runbooks, rollback procedures, verification steps, and follow-up action items. Use after incidents or when documenting operational procedures and recovery paths.
---

# Repository Postmortem and Runbook Writing

Use this skill to document incidents and operational procedures clearly and safely.

## When to Use This Skill

Use this skill for:

- postmortems
- incident summaries
- incident timelines
- runbooks
- rollback procedures
- operational checklists
- on-call handoff notes
- remediation action tracking
- release or deployment recovery docs

## Writing Process

1. Use evidence and timestamps.
2. Keep analysis blameless.
3. Separate customer impact, technical cause, contributing factors, and detection gaps.
4. Document what worked and what did not.
5. Create specific, owned, testable follow-up actions.
6. Ensure runbooks are executable, safe, and reversible.
7. Include verification and rollback steps.
8. Avoid exposing secrets, customer data, internal incident details, or private links beyond the intended audience.

## Workflows

Use:

```text
workflows/postmortem-writing-workflow.md
workflows/runbook-review-workflow.md
```

## Scripts

This skill owns:

```text
scripts/runbook-link-scan.py
```

Run the script with `--help` before manual use.
