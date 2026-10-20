---
name: py-django-6-quality-checks
description: Runs and interprets Django 6.0 quality gates including system checks, migration checks, tests, deployment checks, and safe command review. Use before handoff, review, or release.
license: MIT
compatibility: Requires Django 6.0 and Python 3.12, 3.13, or 3.14.
---

# py-django-6 Quality Checks

## When to Use

Use this skill when the user asks to:

- Run tests.
- Validate migrations.
- Check deployment readiness.
- Prepare a final answer after code changes.
- Review whether generated changes are safe.
- Investigate failing Django checks.

## Workflow

Use `workflows/test-and-quality-workflow.md`.

## Resources and Scripts

- `resources/quality-gates.md`
- `scripts/django-quality-check.sh`
- `scripts/django-command-safety.py`

Run scripts with `--help` before using them.

## Default Gates

Use the repository’s existing commands first. If none exist, use Django-native gates:

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

For production-facing work:

```bash
python manage.py check --deploy
python manage.py migrate --plan
```

## Interpreting Results

- Fix system check errors before feature handoff.
- Treat migration drift as a blocker for model changes.
- Treat failing tests as blockers unless unrelated and documented.
- Treat deployment check warnings as release risks.
- Do not hide warnings by changing settings without understanding the impact.

## Safety

- Do not run `flush`, `sqlflush`, destructive SQL, broad delete scripts, or production migrations without explicit user approval.
- Do not run long test suites without considering user context and repository norms.
- Prefer targeted test labels while iterating, then broader tests before final handoff.
