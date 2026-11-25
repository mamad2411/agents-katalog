---
name: kanban-governance-starter
description: Use when routing Hermes governance audit findings into Kanban cards with risk classification, specialist assignment, reviewer gates, verification evidence, and clean closure.
version: 1.0.0
author: Hermes Governance Starter
license: MIT
metadata:
  hermes:
    tags: [kanban, governance, remediation, review]
    related_skills: [memory-governance-starter, skill-governance-starter]
    lifecycle: starter
    risk_level: workflow_side_effect_gated
    approval_required_for: [destructive_cleanup, credential_changes, external_side_effects]
---

# Kanban Governance Starter

## Overview

Use this skill when an audit finding needs durable remediation rather than a one-off chat response.

Kanban keeps governance work trackable: inspect, classify, fix, review, verify, close.

## When to Use

- Audit findings require multiple steps.
- A reviewer should approve the fix.
- Work should survive session restarts.
- Evidence needs to be attached to the final state.

## Card Shape

```text
Finding -> Risk -> Target -> Proposed fix -> Review requirement -> Verification command -> Evidence
```

## Common Pitfalls

1. Letting cron detect issues but never creating remediation work.
2. Closing a card without rerunning the relevant audit.
3. Making the same agent both author and reviewer for risky changes.
4. Creating noisy cards for harmless advisory findings.

## Verification Checklist

- [ ] Finding is linked to a report.
- [ ] Risk tier is explicit.
- [ ] Owner/profile is assigned.
- [ ] Reviewer gate exists when needed.
- [ ] Verification output is attached before close.
