---
name: kos-daily-maintenance-sweep
description: Run the daily maintenance sweep (health, security audit, progress, TODO/FIXME scan, stale issues) and create issues ONLY where findings exist — the maintenance workflow's no-spam discipline.
user-invocable: true
when_to_use: "When the maintenance workflow runs its twice-daily sweep, or when tuning what it reports."
category: utilities
argument-hint: "[category or 'all']"
keywords: [maintenance, health, security, audit, todo, fixme, stale, sweep, daily]
related: [kos-gh-automation-tooling, kos-zai-run-failure-prevention, kos-claude-turn-budget, kos-runner-disk-hygiene]
metadata:
  author: kos-workflow-improvement
  attribution: distilled from maintenance.yml prompt (/gsd:health && /gsd:stats + 5-category sweep) + 30/30 success runs
  license: repo
  version: "1.0"
---

# Idea

`maintenance` runs twice daily: `/gsd:health` + `/gsd:stats`, then a 5-category sweep (health, security `npm audit`, progress, TODO/FIXME in recent commits, stale issues >90d), creating a GitHub issue **only** for categories with findings. It is reliably green (30/30) because it is read-mostly and creates issues conservatively. The skill preserves that: sweep, dedupe against existing issues, and never spam (no issue when a category is clean; no duplicate of an open issue).

## When to invoke this skill directly

- You are running the daily maintenance sweep.
- You are deciding which findings become issues.

## References

- `maintenance.yml` prompt (the 5 categories + create-issue rules).
- `ck:security-scan` / `npm audit`, `/gsd:health`, `/gsd:stats`, `/gsd:progress`, `/gsd:inbox`.
- `ensure-workflow-labels` (labels: `maintenance`, `security`, `ci-failure`).
- `report-failure` (only if the sweep itself fails).

## Communication Style

Per category: findings count → issue created / skipped (clean) / skipped (duplicate). End with totals.

## Core Principles

YAGNI / KISS / DRY. Issue only if findings exist AND no open duplicate. Critical security → also comment on open PRs. Clean category = no issue (success, not failure).

## The 5 categories

1. **Planning health** — `/gsd:health` problems.
2. **Security** — `npm audit` HIGH/CRITICAL.
3. **Progress** — `/gsd:progress` stale/blocked phases.
4. **TODO/FIXME** — in commits from the last 12h.
5. **Stale issues** — open >90 days.

## Your Approach

1. Run each category's check.
2. For findings: search for an open issue covering it before creating a new one.
3. Create with the right label (`security`/`maintenance`) only if findings + no duplicate.
4. Critical security → comment on open PRs too.
5. Clean category → skip (no issue).

## Failure modes to avoid

- **Issue spam** → creating an issue every run for the same standing finding (dedupe first).
- **Clean-category "failure"** → no findings is a clean success; do not force an issue.
- **Missing critical escalation** → HIGH/CRITICAL security must reach PRs, not just an issue.
- **Disk** → self-hosted runner; ensure-disk-space before `npm audit` install.

## Process Flow (Authoritative)

1. run 5 checks.
2. dedupe against open issues.
3. create labeled issues only for real, non-duplicate findings.
4. escalate critical security to PR comments.
5. report totals; clean = success.

## Output Format

```text
SWEEP: health=h security=s progress=p todo=t stale=u
ISSUES: created=a skipped-clean=b skipped-dup=c
ESCALATION: pr-comments=<n|none>
```

## Critical Constraints

- Never create a duplicate of an open issue — search first.
- Never create an issue for a clean category.
- HIGH/CRITICAL security findings must also be commented on open PRs.
- Ensure disk space before the install/audit step.
