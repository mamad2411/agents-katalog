---
name: github-actions-ci-reliability
description: Improves GitHub Actions CI reliability, matrix design, dependency caching, artifact use, concurrency, test separation, retry strategy, and failure diagnosis.
---


# GitHub Actions CI Reliability

Use this skill when CI is flaky, slow, hard to debug, or incorrectly scoped.

## Review Focus

- trigger scope
- matrix shape and fail-fast behavior
- dependency caching
- setup actions
- test grouping
- timeout behavior
- concurrency
- artifacts and logs
- failure summaries
- duplication across workflows

## Workflow

Use `workflows/ci-reliability-review-workflow.md`.

## Resources

- `resources/ci-reliability-checklist.md`

## Scripts

This skill owns:

```text
scripts/summarize-github-actions-workflows.py
```

Run the script with `--help` before use.

