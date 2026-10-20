# Django Base Model

## Summary

**One-sentence:** Produces a Django abstract BaseModel with uid (UUID), created_at, updated_at; integer PK kept for joins; UUID exposed in APIs/URLs.

**One-paragraph:** Produces a Django abstract BaseModel with uid (UUID), created_at, updated_at; integer PK kept for joins; UUID exposed in APIs/URLs. The methodology fires on a named trigger, produces a fixed-shape artifact with evidence anchors and a named owner, and is reviewed against outcomes at a published cadence so it stops being folklore.

**Ефективно для:** команд, що оперують цим артефактом регулярно і потребують детермінованого формату плюс перевірюваного результату.

## Applies If (ALL must hold)

- Project uses Django 5.x (or 4.2 LTS) with Python 3.12+.
- Code in question lives under `apps/<app>/` or `core/` per the django-coding-standards layout.
- A test runner is configured (`pytest + pytest-django`).
- The team has agreed to enforce service-layer logic separation.

## Skip If (ANY kills it)

- Project is not on Django (FastAPI, Flask, or other) — load the framework-specific methodology instead.
- Tiny throwaway tool with no growth horizon — overhead exceeds payoff.
- Codebase has not adopted the apps/core/config layout and refactoring it is out of scope right now.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `pyproject.toml` | TOML | repo root |
| `apps/<app>/` layout | directory tree | repo source |
| Target Django version | string | `pyproject.toml` |
| Existing test runner config | TOML | `pyproject.toml` `[tool.pytest.ini_options]` |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/dev/python-developer/python-typing` | Type-checker baseline for Django code. |
| `free/dev/software-developer/django-coding-standards` | Layout standard that gates placement of files produced here. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules specific to django-base-model | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artifact + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | Recurring antipatterns with reason | ~900 |
| `content/06-decision-tree.xml` | essential | Decision tree from observable inputs to a rule conclusion | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Scaffold model/serializer/view/test from spec | sonnet | Mechanical code generation. |
| Design service-layer boundaries | opus | Needs domain judgement. |
| Audit existing code for layering violations | sonnet | Pattern matching with deterministic output. |

## Templates

| File | Purpose |
|------|---------|
| `templates/base_model.py` | Working Django abstract BaseModel: id (int PK), uid (UUIDField), created_at, updated_at, Meta.abstract = True. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-django-base-model.py` | Validates the output record against `02-output-contract.xml`. | After the methodology runs, before publishing the artifact. |

## Related

- [[django-coding-standards]] — see methodology AGENTS.md for context.
- [[django-models]] — see methodology AGENTS.md for context.
- [[django-pytest]] — see methodology AGENTS.md for context.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` keys off the observable inputs documented in Prerequisites and routes to either "run the methodology" (preconditions hold) or "skip and route elsewhere" (preconditions fail). Use it before invoking the methodology, not after.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/base_model.py`

```python
"""
Django BaseModel scaffold.

Usage: copy to core/models.py, import in every domain model.
UUIDv7 upgrade: pip install uuid-utils, uncomment uuid7 section.
"""
import uuid
from django.db import models
from django.utils import timezone

# --- UUID: default is v4. For high-write tables, upgrade to v7: ---
# import uuid_utils
# def uuid7(): return uuid_utils.uuid7()
# Then set: uid = models.UUIDField(default=uuid7, ...)


class BaseModel(models.Model):
    uid = models.UUIDField(
        default=uuid.uuid4,  # callable — NOT uuid.uuid4()
        editable=False,
        unique=True,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']
        get_latest_by = 'created_at'

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.uid})"


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class SoftDeleteModel(BaseModel):
    """BaseModel + soft delete. Use only for non-PII data."""

    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta(BaseModel.Meta):
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at', 'updated_at'])

    def hard_delete(self, using=None, keep_parents=False):
        super().delete(using=using, keep_parents=keep_parents)

    def restore(self):
        self.deleted_at = None
        self.save(update_fields=['deleted_at', 'updated_at'])

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
```
