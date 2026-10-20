---
name: repo-lockfile-review
description: Reviews lockfile changes for reproducibility, unexpected transitive churn, registry/source drift, integrity changes, package-manager mismatch, and rollback safety. Use when lockfiles are generated, modified, deleted, or included in dependency changes.
---

# Repository Lockfile Review

Use this skill whenever lockfiles change.

## When to Use This Skill

Use this skill for lockfiles such as `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `bun.lockb`, `poetry.lock`, `uv.lock`, `Pipfile.lock`, `Cargo.lock`, `go.sum`, `Gemfile.lock`, and `composer.lock`.

## Review Process

1. Identify which lockfiles changed.
2. Confirm matching manifest changes.
3. Check whether lockfile churn is expected.
4. Review package source/registry/integrity changes where visible.
5. Check package-manager version drift.
6. Avoid accepting lockfile-only changes without explanation.
7. Recommend targeted regeneration only when necessary.

## Workflow

Use `workflows/lockfile-review-workflow.md`.

## Scripts

This skill owns `scripts/lockfile-change-summary.py`.
