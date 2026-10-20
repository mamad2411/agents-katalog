# tests/ — Test Suite Conventions

Repo UI priority: Rotaris desktop (`apps/rotaris/`, tests in `apps/rotaris/tests/`, pytest-qt) is the **primary** UI; the Textual TUI (`test_tui_*.py` here) is **secondary**.

The canonical policy for productive intent, test levels, requirement
portfolios, and hermetic user-flow E2E coverage is
[docs/testing/test_strategy.md](../docs/testing/test_strategy.md). This file
defines executable repository conventions: locations, fixtures, and annotations.
Textual tests additionally follow
[docs/testing/textualize_testing_guide.md](../docs/testing/textualize_testing_guide.md).

## Layout

```
tests/
  conftest.py              # Central fixtures (shared across all tests)
  unit/                    # Single-module behavior tests (fast, no I/O)
  integration/             # End-to-end and multi-module tests
  capability/              # Real LLM capability tests (slow, requires endpoint)
  fixtures/
    files/                 # Sample Python fixture files
      small.py, large.py, unicode.py, crlf.py, empty.py
    configs/
      global/              # agents.yaml, models.yml (global scope fixtures)
      workspace/           # agents.yaml, models.yml (workspace scope fixtures)
```

## Core Fixtures (`tests/conftest.py`)

```python
tmp_workspace        # tmp_path with .rotaris/ subdir pre-created
fixtures_dir         # Path → tests/fixtures/
sample_small_file    # Path to fixtures/files/small.py (copied to tmp_workspace)
sample_large_file    # Path to fixtures/files/large.py
sample_unicode_file  # Path to fixtures/files/unicode.py
sample_crlf_file     # Path to fixtures/files/crlf.py
sample_empty_file    # Path to fixtures/files/empty.py
global_config_dir    # Path to fixtures/configs/global/
workspace_config_dir # Path to fixtures/configs/workspace/
```

## Test Naming

- Files: `test_<module_name>.py`
- Functions: `test_<behavior_description>()`
- No class-based test grouping required (plain functions preferred)
- New or materially changed tests start with:

```python
"""Productive use: <actor> can <productive action>.
Expected outcome: <user-observable result or enabling invariant>."""
```

## Requirement Coverage (ReqToCode)

ReqToCode rules are canonical in the [root AGENTS.md](../AGENTS.md#critical-rules--reqtocode-enforced-build-breaking).
Test-specific additions here:

Tests that cover a requirement from `docs/requirements/` carry `@verifies`:

```python
from rotaris_core.reqtocode import SWR, verifies

@verifies(SWR.SWR_103)
def test_duplicate_names_rejected(): ...
```

- Only `@verifies` references inside test roots count as coverage; a `@traces`
  in a test does not (and a `@verifies` is not an implementation trace).
- Transitional `# @req: SWR-<n>` comments still count — prefer `@verifies` for new tests.
- Machine-enforced: an unannotated `test_*` function is an **orphan-test** error
  unless it is under `tests/capability/`, marked `# reqtocode: exempt`, or listed
  in the shrink-only `docs/requirements/orphan-test-baseline.txt`.
  New tests can never be added to that baseline.
- The test must exercise real behavior of the traced code — a test that would pass
  without the implementation is a red flag.
- Meta-tests live in `tests/unit/reqtocode/`; pytest regenerates `swr.py` at session
  start, so a requirement edit fails fast in the same run. On any ReqToCode failure:
  [docs/reference/reqtocode-playbook.md](../docs/reference/reqtocode-playbook.md).

## Async Tests

```python
import pytest

@pytest.mark.asyncio            # explicit marker (also works without due to asyncio_mode=auto)
async def test_something():
    result = await some_coroutine()
    assert result == expected
```

`asyncio_mode = "auto"` in pyproject.toml — coroutine test functions are auto-detected.

## Mock Patterns

### Module-level substitution (preferred)

```python
def test_something(monkeypatch):
    monkeypatch.setattr("rotaris_core.tools.plugin_loader.register_tool", fake_register)
```

### Call assertion

```python
from unittest.mock import Mock, patch

def test_calls_register(monkeypatch):
    mock_register = Mock()
    with patch("rotaris_core.agents.registry.register_agent", mock_register):
        registry.load_all()
    mock_register.assert_called_once_with(...)
```

### LLM stub (for SummaryAgent / factory tests)

```python
from openhands.sdk.llm.message import Message

class MockLLM:
    def completion(self, messages, **kw):
        return type("R", (), {"message": Message(content='{"status":"succeeded","summary":"ok"}')})()
```

### SDK LLM (for factory / integration tests)

```python
from openhands.sdk.llm.llm import LLM
llm = LLM(model="openai/gpt-4o-mini", api_key="test")   # "test" is conventional placeholder
```

## Capability Tests (`tests/capability/`)

Real LLM end-to-end tests against a live model endpoint. **Skipped automatically** when the
configured endpoint is unreachable; auto-marked `@pytest.mark.capability` by the collection
hook in `conftest.py` (never the only E2E coverage for a requirement).

- Layout: `conftest.py` (shared fixtures), `harness.py` (`CapabilityResult` +
  `run_capability_task()`), one `test_<description>.py` per capability.
- Fixtures: `capability_workspace` (tmp_path + `.rotaris/`), `capability_config`
  (`RotarisConfig` from the user's global `~/.config/rotaris/agents.yaml` — the default
  model must be reachable).
- Adding one: create `test_<description>.py`, use those fixtures, call
  `run_capability_task(config, workspace, task=...)` from `harness.py`, assert on
  `CapabilityResult.progress` AND filesystem artifacts. No explicit marker needed.

## Test placement

| Location              | Put tests here when...                                                                      |
| --------------------- | ------------------------------------------------------------------------------------------- |
| `tests/unit/`         | Exercising focused decisions, invariants, transformations, or failure branches in isolation |
| `tests/integration/`  | Exercising real collaboration or a hermetic public-boundary user flow across modules        |
| `apps/rotaris/tests/` | Exercising the primary PySide6 product boundary with pytest-qt                              |
| `tests/capability/`   | Exercising optional live-provider confidence; never as the only E2E coverage                |

## Fixture Files

- To add a new fixture file: place it in `tests/fixtures/files/` and add a fixture in `conftest.py` following the `sample_*_file` pattern
- To add config variants: place YAML in `tests/fixtures/configs/global/` or `workspace/`

## Gotchas

- `respx` is available for mocking `httpx` requests in `FetchTool` tests
- `textual-dev` is available for Textual TUI widget testing (use `App.run_async()` or pilot)
- Hardcoded test secrets (`SecretStr("super-secret")`, `api_key="test"`) are intentional test-only values — do not replace with real credentials
- `LocalConversation` is not directly mocked in tests — patch at scheduler construction site if needed
