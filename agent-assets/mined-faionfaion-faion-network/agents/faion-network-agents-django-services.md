# Django Service Layer

## Summary

**One-sentence:** Isolate Django business logic into a services/ module of plain Python functions so views, admins, and tasks share one tested core.

**One-paragraph:** Pattern for isolating Django business logic into a `services/` layer of plain Python functions (or classes only when DI is required). Views, admins, management commands, and Celery tasks all call into the service layer; the layer in turn talks to ORM and external clients. Service functions take primitives (or pydantic models) — not request objects — and return primitives — not Response objects. This decouples business logic from HTTP and makes it directly testable.

**Ефективно для:**

- Brownfield Django codebases where fat views or fat models hurt testability.
- New projects targeting >5kloc and requiring repeatable test patterns.
- Shared business logic across views, admin, management commands, and Celery tasks.
- Onboarding agents and engineers to a consistent layering convention.

## Applies If (ALL must hold)

- Django >=4 project with non-trivial business logic.
- Business logic is reused by at least 2 of: views, admin, tasks, management commands.
- Tests run against the service layer rather than the request/response surface.
- Codebase will grow beyond what fat-view pattern can carry.

## Skip If (ANY kills it)

- Tiny CRUD app where ModelViewSet is the whole logic.
- Codebase already uses CQRS / hexagonal pattern with explicit handlers — different methodology.
- Logic is one-off scripts not reused — no payoff from extraction.
- Project is Django REST Framework with full reliance on serializer.save() business rules — refactor first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| List of business operations + their callers (view, admin, task, cmd) | table | tech-lead |
| Pydantic or dataclass policy for service inputs/outputs | ADR | tech-lead |
| Test framework + factory library (pytest + factory_boy) | config | platform |
| Existing fat-view code samples to refactor (if brownfield) | code | tech-lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[django-celery]] | Tasks call into the service layer. |
| [[logging-patterns]] | Services emit structured logs around operations. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules (services accept primitives, return primitives, no HTTP types in services, ORM only inside services, single-responsibility module per aggregate) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for service module spec + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: inventory ops → name services → extract → test → migrate callers | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `operation_inventory` | sonnet | Walk codebase, find logic in views/admin/tasks. |
| `service_extraction` | opus | Refactor needs to preserve behaviour + decouple HTTP. |
| `test_authoring` | sonnet | Mechanical pytest cases against pure service functions. |

## Templates

| File | Purpose |
|------|---------|
| `templates/service-module.py` | Service module skeleton with function signatures + docstrings |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-django-services.py` | Validate the service module spec metadata against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

- [[django-celery]]
- [[logging-patterns]]
- [[database-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps codebase size, logic reuse, and current architecture to a rule from `01-core-rules.xml`, telling the agent whether to extract services or skip when the pattern doesn't fit. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/service-module.py`

```python
# Service module skeleton for Django
# Copy and fill in: Feature, Model, app, verb, noun, params
# Conventions: lazy model imports, keyword-only args, domain exception, transaction.atomic

from __future__ import annotations
from typing import TYPE_CHECKING
from django.db import transaction

if TYPE_CHECKING:
    from apps.<app>.models import <Model>
    from apps.users.models import User


class <Feature>Error(Exception):
    """Domain errors raised by <feature> service."""


@transaction.atomic
def <verb>_<noun>(
    user: "User",
    *,
    param: str,
) -> "<Model>":
    """One-line summary.

    Business logic:
    - bullet describing each rule

    Args:
        user: User performing the action.
        param: Description.

    Returns:
        The created/updated <Model> instance.

    Raises:
        <Feature>Error: When a business rule is violated.
    """
    from apps.<app>.models import <Model>

    try:
        obj = <Model>.objects.select_for_update().get(field=param)
    except <Model>.DoesNotExist:
        raise <Feature>Error(f"<Model> {param!r} not found")

    # mutate
    obj.field = ...
    obj.save(update_fields=["field", "updated_at"])
    return obj
```
