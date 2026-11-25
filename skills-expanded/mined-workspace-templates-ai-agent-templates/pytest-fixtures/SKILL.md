---
name: pytest-fixtures
description: Designs pytest fixtures, parametrization and conftest layout so Python suites run fast, read clearly and do not share hidden state.
---

# pytest fixtures

Tests should declare what they need as arguments, and each fixture should do one job at the narrowest scope that stays fast.

## Fixtures

- Default to function scope. Raise it to `module` or `session` only for expensive, read-only resources such as a container or a compiled schema, and reset state per test inside it (transaction rollback, truncate).
- Use `yield` for teardown, not `request.addfinalizer` unless several finalizers are needed.
- Give a fixture a noun name (`db_session`, `logged_in_client`). A fixture that returns a function building objects is a factory: `make_order(status="paid")`. Prefer factories over many near-identical fixtures.
- Avoid `autouse=True` except for safety nets, such as blocking real network calls or freezing time.

## Layout

- Put fixtures used by one file in that file, by one directory in its `conftest.py`, and by the whole suite in the root `conftest.py`. Move them up only when a second user appears.
- Share through plugins or `pytest_plugins` rather than importing fixtures from test modules.

## Parametrize

- `@pytest.mark.parametrize("raw, expected", [...], ids=[...])` with readable ids. Use `pytest.param(..., marks=pytest.mark.xfail(reason=...))` for known gaps.
- Combine with fixtures through indirect parametrization only when setup depends on the case.

## Rules

- Use `monkeypatch` and `tmp_path` rather than manual patching and shared directories.
- Never hide an assertion in a fixture.
- Run `pytest --setup-show` to confirm scope and order, and a random-order plugin once to test independence.

## Report

Fixtures added or merged, scope decisions, and the run time before and after.
