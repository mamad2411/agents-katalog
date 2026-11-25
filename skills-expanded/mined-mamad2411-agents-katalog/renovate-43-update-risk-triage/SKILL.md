---
name: renovate-43-update-risk-triage
description: Categorizes Renovate 43 dependency updates by risk, detects critical dependency categories, reviews lockfile risk, and prepares major-upgrade plans. Use when reviewing Renovate PRs, major updates, lockfile-only updates, framework updates, auth/crypto/database/infra changes, or packageRules that affect update grouping and automerge.
license: MIT
compatibility: Requires git for diff-based helper scripts. Does not require network access.
---

# Renovate 43 Update Risk Triage

Use this skill to classify dependency update risk and choose review, grouping, automerge, and testing requirements.

## Workflows

- `workflows/renovate-43-update-risk-triage-workflow.md`
- `workflows/renovate-43-major-upgrade-plan-workflow.md`
- `workflows/renovate-43-lockfile-review-workflow.md`

## Resources

- `resources/renovate-43-update-risk-matrix.md`
- `resources/renovate-43-critical-dependency-heuristics.md`

## Scripts

Run scripts with `--help` before using them.

```bash
python3 scripts/renovate-risk-detector.py --help
python3 scripts/lockfile-risk-check.py --help
```

## Decision Rules

- Prioritize security updates, but do not skip critical dependency review.
- Do not automerge critical dependency categories.
- Do not group security updates with routine maintenance.
- Do not group major updates with minor, patch, or digest updates.
- Review lockfile diffs for unexpected source, integrity, registry, or transitive dependency changes.
