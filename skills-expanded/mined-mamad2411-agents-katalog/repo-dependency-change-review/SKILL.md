---
name: repo-dependency-change-review
description: Reviews dependency additions, removals, upgrades, downgrades, package-manager commands, manifest edits, and lockfile impact. Use when dependency graphs, package manifests, package managers, lockfiles, package scripts, or supply-chain risk are involved.
---

# Repository Dependency Change Review

Use this skill when a task changes or reviews dependencies.

## When to Use This Skill

Use this skill for:

- adding or removing dependencies
- upgrading or downgrading dependencies
- running package-manager commands
- reviewing dependency bot PRs
- editing manifests or package-manager config
- reviewing lockfile changes
- evaluating package-source changes
- deciding whether an audit fix is safe

## Review Process

1. Identify the package manager and ecosystem.
2. Identify manifest and lockfile files.
3. Determine whether the change is direct, transitive, runtime, build-time, test-only, or development-only.
4. Check whether lifecycle scripts may run.
5. Check whether the change broadens version ranges or rewrites transitive dependencies.
6. Classify risk using `resources/dependency-risk-matrix.md`.
7. Prefer minimal scoped changes.
8. Plan validation and rollback.
9. Ask for approval before broad or high-risk operations.

## Workflows

Use `workflows/dependency-change-review-workflow.md` for dependency adds, removals, upgrades, downgrades, and dependency PR review.

## Scripts

This skill owns:

```text
scripts/dependency-command-guard.py
scripts/dependency-risk-scan.py
```

Run scripts with `--help` before manual use.
