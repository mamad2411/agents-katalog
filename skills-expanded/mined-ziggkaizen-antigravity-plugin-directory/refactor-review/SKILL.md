---
name: refactor-review
description: Reviews refactors for behavior preservation, API compatibility, hidden coupling, test coverage, rollback safety, and unintended side effects. Use when code is reorganized, renamed, extracted, simplified, or broadly rewritten without intended behavior changes.
---

# Refactor Review

Use this skill when reviewing refactors.

## When to Use This Skill

Use this skill for:

- file moves
- renames
- extraction of functions, classes, modules, or services
- dependency inversion
- architecture cleanup
- broad formatting-adjacent changes
- replacing implementations without intended behavior change
- removing dead code

## Refactor Review Principles

- Behavior preservation is the default expectation.
- Public interfaces must remain compatible unless a breaking change is explicit.
- Tests should prove behavior preservation.
- Large refactors should be split into reviewable steps.
- Formatting-only changes should not hide behavior changes.
- Dead-code removal should be justified by references or usage analysis.

## Workflow

Use `workflows/refactor-risk-review-workflow.md`.

## Resource

Use `resources/refactor-review-checklist.md`.
