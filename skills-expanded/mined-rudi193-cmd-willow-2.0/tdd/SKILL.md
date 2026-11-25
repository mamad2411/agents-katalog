---
name: tdd
description: Test-driven development for Willow 2.0 — willow_20_test schema, real DB, mock MCP
---

@markdownai v1.0

# TDD — Willow 2.0

## Rules

- Tests run against `willow_20_test` — set via `WILLOW_PG_DB=willow_20_test` in conftest.
- Never mock the database. Tests that need Postgres use the real `bridge` fixture from `tests/conftest.py`.
- Each behavior function is standalone — test it in isolation with mocked MCP calls.
- Hook handlers are tested by passing mock stdin and capturing stdout.
- Commit each green state. Never batch test + implementation into one commit.

## Cycle

1. **Write the failing test first.** Run it. Confirm it fails with the expected error — `ImportError`, `AssertionError`, not a crash.
2. **Write the minimum code to pass.** No extra logic, no preemptive abstractions.
3. **Run the test.** Green → commit → next test. Red → fix only what the test says.

## MCP Mocking Pattern

```python
from unittest.mock import patch

def test_behavior_calls_mcp(tmp_path):
    with patch("willow.fylgja.events.mymodule.call") as mock_call:
        mock_call.return_value = {"status": "ok"}
        result = my_behavior("arg")
    mock_call.assert_called_once_with(
        "tool_name", {"app_id": "hanuman", "key": "value"}
    )
```

## Hook Handler Test Pattern

```python
import json
from io import StringIO
from unittest.mock import patch

def _run(stdin_data: dict) -> str:
    import willow.fylgja.events.myhandler as m
    inp = StringIO(json.dumps(stdin_data))
    out = StringIO()
    with patch("sys.stdin", inp), patch("sys.stdout", out):
        try:
            m.main()
        except SystemExit:
            pass
    return out.getvalue()
```

## Schema Note

Migrations adding columns or tables must be applied to both `willow_20` and `willow_20_test`. The conftest `init_pg_schema` fixture handles this automatically for the test database.
