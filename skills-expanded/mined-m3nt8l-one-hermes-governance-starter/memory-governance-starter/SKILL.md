---
name: memory-governance-starter
description: Use when setting up or maintaining generic Hermes memory governance: placement rules, stale-fact audits, wiki hygiene, quiet cron reports, and safe promotion/demotion between memory, docs, skills, and reports.
version: 1.0.0
author: Hermes Governance Starter
license: MIT
metadata:
  hermes:
    tags: [memory, governance, wiki, cron, hygiene]
    related_skills: [skill-governance-starter, kanban-governance-starter]
    lifecycle: starter
    risk_level: file_write_reversible
    approval_required_for: [credential_changes, destructive_cleanup, external_side_effects]
---

# Memory Governance Starter

## Overview

Use this skill to keep Hermes memory small, scoped, current, and source-backed.

Memory governance separates durable knowledge from procedures, temporary reports, and historical conversation logs.

## When to Use

- Auditing active memory for stale or duplicate facts.
- Deciding whether knowledge belongs in memory, wiki/docs, skill, report, or nowhere.
- Creating quiet memory governance cron jobs.
- Reviewing wiki/docs health and unresolved links.

## Placement Rule

```text
Active memory = small stable behavior-shaping facts
Wiki/docs     = long source-backed knowledge
Skills        = reusable procedures
Reports       = temporary evidence
Sessions      = historical conversation recall
Secrets       = never stored
```

## Common Pitfalls

1. Promoting task progress into durable memory.
2. Keeping long procedures in memory instead of skills.
3. Treating retrieved context as permission for high-risk actions.
4. Letting cron reports spam the main chat.
5. Storing credentials in reports or wiki pages.

## Verification Checklist

- [ ] Memory files are compact and scoped.
- [ ] Stale/time-sensitive notes are demoted to reports or docs.
- [ ] Procedures are moved to skills.
- [ ] Wiki links and required indexes are valid.
- [ ] Audit reports are written outside active memory.
