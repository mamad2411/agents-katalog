# Django Testing

## Summary

**One-sentence:** Produces a Django test pattern with pytest + model_bakery/factory_boy + APIClient; service-layer tests call real code, mocks live at process boundaries (HTTP, S3, third-party SDKs).

**One-paragraph:** Produces a Django test pattern with pytest + model_bakery/factory_boy + APIClient; service-layer tests call real code, mocks live at process boundaries (HTTP, S3, third-party SDKs). The methodology fires on a named trigger, produces a fixed-shape artifact with evidence anchors and a named owner, and is reviewed against outcomes at a published cadence so it stops being folklore.

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
| `content/01-core-rules.xml` | essential | Testable rules specific to django-testing | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artifact + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | Recurring antipatterns with reason | ~900 |
| `content/04-procedure.xml` | medium | Step-by-step procedure (when complexity >= medium) | ~600 |
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
| `templates/conftest.py` | pytest-django conftest with db, factories, APIClient. |
| `templates/pyproject-pytest.toml` | pyproject.toml [tool.pytest.ini_options] section preset for Django. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-django-testing.py` | Validates the output record against `02-output-contract.xml`. | After the methodology runs, before publishing the artifact. |

## Related

- [[django-coding-standards]] — see methodology AGENTS.md for context.
- [[django-models]] — see methodology AGENTS.md for context.
- [[django-pytest]] — see methodology AGENTS.md for context.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` keys off the observable inputs documented in Prerequisites and routes to either "run the methodology" (preconditions hold) or "skip and route elsewhere" (preconditions fail). Use it before invoking the methodology, not after.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/conftest.py`

```python
# tests/conftest.py — reusable Django + DRF + baker fixtures.
import datetime as dt

import pytest
from model_bakery import baker
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return baker.make("users.User", is_active=True)


@pytest.fixture
def staff_user(db):
    return baker.make("users.User", is_active=True, is_staff=True)


@pytest.fixture
def authed_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture(autouse=True)
def _reset_outbound_email(settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"


@pytest.fixture
def freeze_now(monkeypatch):
    """Freeze django.utils.timezone.now to a fixed instant."""
    from django.utils import timezone

    fixed = dt.datetime(2026, 1, 1, 12, 0, tzinfo=dt.timezone.utc)
    monkeypatch.setattr(timezone, "now", lambda: fixed)
    return fixed
```

### `templates/pyproject-pytest.toml`

```toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings.testing"
python_files = ["test_*.py"]
addopts = "-v --tb=short --reuse-db --cov=apps --cov-report=term-missing --cov-fail-under=80 -p randomly"
markers = [
    "slow: marks tests as slow (deselect with '-m not slow')",
    "integration: marks tests as integration tests",
]
```
