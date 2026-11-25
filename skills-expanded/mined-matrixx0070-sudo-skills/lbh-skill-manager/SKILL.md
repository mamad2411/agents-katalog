---
name: lbh-skill-manager
version: 1.0.0
description: Manage the installed set of legal skills — list, inspect status, resolve conflicts, and route to enable/disable/update/uninstall actions.
author: matrixx0070
tags: [legal, management, inventory, status, orchestration]
capabilities: []
---

## When to use

Use this as the control panel for a user's installed legal skills. It gives an at-a-glance inventory — what's installed, which version, enabled or disabled, last reviewed, update available — and routes each item to the right lifecycle action.

**Not for:** discovering new skills (`lbh-registry-browser`), the security gate (`lbh-skills-qa`), or the individual mechanical actions themselves — this skill orchestrates and hands off to `lbh-skill-installer`, `lbh-auto-updater`, `lbh-disable`, and `lbh-uninstall`.

## Method

1. Build the inventory from install records: name, version, enabled state, QA verdict date, source, and any applied conditions.
2. Flag health issues: skills past the staleness threshold, skills with an update available, skills whose last QA is older than a re-review interval (default 12 months).
3. Detect conflicts: two installed skills claiming the same capability + jurisdiction, or overlapping trigger phrases that would fire ambiguously.
4. Recommend one action per flagged item and name the skill that performs it — never perform destructive actions from here.
5. Surface the security posture: count of enabled skills with any elevated condition, so the user sees their exposure.
6. Keep it read-and-route: this skill reports and dispatches; it does not mutate installs directly.

## Example

Inventory shows 6 legal skills. Two both claim `nda-review / US`, a conflict — you recommend disabling the lower-scored one via `lbh-disable`. One is 14 months since QA — you route it to re-review via `lbh-skills-qa`. One has v2.2 available — route to `lbh-auto-updater`. The user gets a single dashboard with three clear next actions.

## Pitfalls

- Silently mutating installs from the manager. Keep it a router; destructive changes go through their dedicated, audited skills.
- Ignoring capability collisions, so two skills fire on the same request and produce contradictory legal output.
- Letting stale QA slide. A skill vetted a year ago against an older registry may now be risky; re-review on interval.
- Reporting enabled-count without exposure. Show which enabled skills carry elevated conditions.

## Output format

```
# Legal Skills Inventory
INSTALLED (<n>):
- <name>@<ver> [enabled|disabled] QA:<date> update:<ver|none> cond:<...>
FLAGS:
- CONFLICT: <a> vs <b> on <capability/jurisdiction> -> lbh-disable
- STALE-QA: <name> (<months>) -> lbh-skills-qa
- UPDATE: <name> <cur>-><new> -> lbh-auto-updater
EXPOSURE: enabled-with-conditions=<n>
```

## Reference

**Skill-vetting checklist (management link):** every installed entry must carry a QA date; entries past the re-review interval are surfaced for re-vetting, not left assumed-safe.

**Security-review gate criteria:** the manager tracks each enabled skill's applied conditions and re-review age; an enabled skill with a lapsed review is treated as a HIGH exposure flag.

**Versioning / rollback:** inventory shows installed vs available versions so updates and rollbacks target explicit coordinates; the manager routes, `lbh-auto-updater` executes with a rollback point.
