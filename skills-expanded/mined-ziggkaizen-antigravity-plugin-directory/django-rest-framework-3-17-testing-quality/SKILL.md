---
name: django-rest-framework-3-17-testing-quality
description: Designs, repairs, and runs tests and quality checks for Django REST Framework 3.17.x APIs. Use when adding API tests, debugging failing API tests, or verifying DRF changes before merge.
license: MIT
compatibility: Requires a Django project using Django REST Framework 3.17.x and Python 3.10+.
---

# Django REST Framework 3.17 Testing Quality

Use this skill for DRF API test design, test repair, verification, and quality review.

## Testing Focus

Cover serializer validation and representation, endpoint success and failure responses, authentication and permission behavior, object-level and tenant/user scoping, pagination, ordering, filtering, throttling where relevant, custom actions, and list/retrieve performance regressions.

## Helper Scripts

This skill includes:

- `scripts/drf-verify.sh`

Run scripts with `--help` before using them. The verification script is safe by default and does not run the full test suite unless `DRF_VERIFY_RUN_TESTS=1` is set.

## Workflow References

- [api-test-repair-workflow](workflows/api-test-repair-workflow.md): Use when writing or repairing DRF endpoint tests.

## Resource References

- [testing-checklist](resources/testing-checklist.md): Use as a coverage checklist.
- [api-test-example](examples/api-test-example.md): Use as a compact test style reference.
