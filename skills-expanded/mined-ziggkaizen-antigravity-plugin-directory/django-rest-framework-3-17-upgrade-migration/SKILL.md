---
name: django-rest-framework-3-17-upgrade-migration
description: Plans and verifies upgrades to Django REST Framework 3.17.x, checking Python/Django compatibility, removed coreapi support, schema-generation changes, dependency pins, and API regressions.
license: MIT
compatibility: Requires a Django project being upgraded to or maintained on Django REST Framework 3.17.x.
---

# Django REST Framework 3.17 Upgrade and Migration

Use this skill when upgrading a project to DRF 3.17.x or validating compatibility within the 3.17.x release line.

## DRF 3.17.x Compatibility Focus

- Python 3.10+.
- Django 4.2, 5.0, 5.1, 5.2, or 6.0.
- Python 3.9 is not supported.
- Deprecated `coreapi` support is removed.
- Prefer third-party OpenAPI tooling for new schema/documentation work.
- Validate optional packages such as `django-filter`, object-permission packages, OpenAPI generators, auth packages, and API clients independently.

## Helper Scripts

This skill includes:

- `scripts/drf-compat-check.py`

Run it with `--help` before using it. The script performs static compatibility checks and does not modify files.

## Workflow References

- [drf-3-17-upgrade-workflow](workflows/drf-3-17-upgrade-workflow.md): Use for planning and verifying a DRF 3.17 upgrade.

## Resource References

- [compatibility-matrix](resources/compatibility-matrix.md): Use as a version and migration checklist.
