---
name: repo-release-readiness
description: Reviews release readiness evidence, validation gaps, artifact readiness, changelog alignment, version changes, and rollback readiness. Use before claiming a change is ready to merge, release, publish, or deploy.
---

# Repo Release Readiness

Use this skill before declaring a repository change ready for release, deployment, merge, or publish.

## When to Use This Skill

Use this skill for:

- release readiness checks
- merge readiness summaries
- pre-release review
- artifact readiness
- publish readiness
- version bump review
- release-note evidence
- validation gap analysis

## Required Review Areas

1. Scope of release.
2. User-visible changes.
3. Risky internal changes.
4. Test/build/static-analysis evidence.
5. CI evidence if available.
6. Migration/deployment/rollback notes.
7. Version, changelog, release-note, and artifact alignment.
8. Known gaps and manual checks.

## Workflows

Use:

- `workflows/release-readiness-review-workflow.md`
- `workflows/release-evidence-review-workflow.md`

## Resources

Use:

- `resources/release-readiness-checklist.md`

## Scripts

This skill owns:

```text
scripts/release-evidence-scan.py
```

Run with `--help` before manual use.
