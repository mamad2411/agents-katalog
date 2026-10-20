# Django Testing with pytest

## Summary

**One-sentence:** Produces Django pytest tests using function style + @pytest.mark.django_db + factory_boy factories, parametrize for input variants, shallow mocks, and conftest.py that does not call ORM directly.

**One-paragraph:** Django testing under pytest: function-style tests (def test_*) with @pytest.mark.django_db, factory_boy factories in conftest.py (never raw User.objects.create_user), parametrize for input/output variants (no test_create_1 / test_create_2 sequence names), shallow mocks (no Mock(spec=...) cascading), and explicit guardrails against the LLM TDD failure mode (edit production code silently to make a failing test pass).

**Ефективно для:**

- New Django module needing unit + integration tests.
- Cleaning up unittest.TestCase classes into pytest function style.
- Replacing brittle conftest fixtures with factory_boy factories.
- Adding mutation-score gating on critical modules.

## Applies If (ALL must hold)

- Django >= 4 with pytest-django installed.
- factory_boy available (or willing to add).
- Tests run in CI and have <10 min budget.
- Mocks/fakes are used for external collaborators only.

## Skip If (ANY kills it)

- Non-Django Python projects (use practices-python-ecosystem).
- Frontend or JS tests (use testing-js-ts-frontend).
- Browser E2E (use playwright-automation).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Django app to test | module path | task brief |
| Existing fixtures / factories status | audit report | tests/ directory |
| CI runner | pytest invocation flags | ci config |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[practices-django-coding]] | code under test follows fat-model thin-view + service-layer rules |
| [[practices-python-ecosystem]] | shared pyproject + ruff + mypy + pre-commit |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 6-step procedure | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-conftest` | sonnet | factory_boy factories + pytest fixtures |
| `emit-parametrized-tests` | sonnet | one assertion concept per test; parametrize for variants |
| `scan-tdd-edit-leak` | haiku | detect production-code edits without test diff |

## Templates

| File | Purpose |
|------|---------|
| `templates/conftest.py` | factory_boy factories + pytest fixtures |
| `templates/test_order_service.py` | Parametrized pytest test with shallow mocks |
| `templates/artefact.json` | Sample artefact metadata for validator |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-testing-django-pytest.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; agent self-check |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[practices-django-coding]]
- [[practices-python-ecosystem]]
- [[testing-backend-languages]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, environment context, risk level) to a concrete conclusion, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which rule applies to the current context.
