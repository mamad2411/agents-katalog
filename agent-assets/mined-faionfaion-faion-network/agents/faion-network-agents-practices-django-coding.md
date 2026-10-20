# Django Coding Practices

## Summary

**One-sentence:** Produces Django app code that uses fat-model thin-view discipline, custom QuerySet managers, select_related/prefetch_related to kill N+1, atomic transactions on writes, and class-based views/DRF for HTTP boundaries.

**One-paragraph:** Django coding practices distilled into testable rules. Models hold business logic and validation (clean() + custom QuerySet); views stay thin; querysets resolve relations eagerly via select_related (FK) and prefetch_related (M2M); all writes are wrapped in transaction.atomic; signals are limited to cross-app concerns; settings are split env-aware. The artefact is the metadata describing the generated app, validated by the per-rule schema.

**Ефективно для:**

- New Django app/module under an existing project.
- Refactor passes removing N+1 queries surfaced by django-silk.
- Code-review gates checking transaction.atomic on write paths.
- Migrating fat-view code into fat-model + service-layer shape.

## Applies If (ALL must hold)

- Django 4.x or 5.x project using the ORM.
- Code path includes write operations that need atomicity.
- Views touch related models (FK / M2M / reverse relations).
- Project has a tests/ directory wired to pytest-django or unittest.

## Skip If (ANY kills it)

- Non-Django projects (use practices-python-ecosystem).
- Read-only async serverless endpoints with no ORM use.
- Legacy projects that explicitly mandate fat-view style and refuse refactor.
- Pure data-pipeline code without HTTP boundary.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Existing Django project root | directory | filesystem |
| App / module name | string | task brief |
| Domain model spec | model fields + relations | design doc |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[practices-python-ecosystem]] | shared Python tooling: ruff, mypy, pyproject.toml |
| [[testing-django-pytest]] | tests use pytest-django fixtures and factories |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 6-step procedure | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `emit-models` | sonnet | model fields + QuerySet methods + clean() |
| `emit-views` | sonnet | class-based views or DRF viewsets respecting thin-view rule |
| `scan-n-plus-one` | haiku | static check for FK access in template loops + missing select_related |

## Templates

| File | Purpose |
|------|---------|
| `templates/models.py` | Model with custom QuerySet + clean() validation |
| `templates/services.py` | Service function wrapping multi-write flow in transaction.atomic |
| `templates/views.py` | Thin DRF ViewSet using select_related + service call |
| `templates/settings-base.py` | Base settings imported by dev/prod variants |
| `templates/artefact.json` | Sample artefact metadata for validator |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-practices-django-coding.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; agent self-check |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[testing-django-pytest]]
- [[practices-python-ecosystem]]
- [[practices-backend-languages]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, environment context, risk level) to a concrete conclusion, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which rule applies to the current context.
