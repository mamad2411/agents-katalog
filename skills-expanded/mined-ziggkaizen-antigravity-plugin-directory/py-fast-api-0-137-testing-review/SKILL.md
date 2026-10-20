---
name: py-fast-api-0-137-testing-review
description: Writes, repairs, and reviews FastAPI 0.137.x tests and quality checks. Use when changing endpoint behavior, dependency overrides, TestClient tests, route registration, or API security behavior.
license: MIT
---

# FastAPI 0.137.x Testing and Review Skill

Use this skill when testing or reviewing FastAPI `0.137.x` application changes.

## When to Use

- Adding tests for new or changed routes.
- Reviewing route behavior, request validation, or response models.
- Repairing broken tests after dependency or router changes.
- Checking auth, authorization, or OpenAPI behavior.
- Running local quality checks before final review.

## How to Work

1. Read `resources/testing-checklist.md`.
2. Inspect existing test conventions before adding new patterns.
3. Prefer focused tests for route behavior and dependency boundaries.
4. Use dependency overrides for external services and reset overrides after tests.
5. Cover success, validation failure, auth failure, and domain failure paths.
6. Run scripts with `--help` before using them:
   - `scripts/fastapi-quality-check.sh --help`
7. Do not run migrations, seed production data, call live external services, or install dependencies unless the user explicitly approves.

## Workflow

Use `workflows/test-and-review-workflow.md` for multi-step testing or review tasks.
