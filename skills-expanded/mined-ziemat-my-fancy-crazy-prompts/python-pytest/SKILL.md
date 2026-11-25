---
name: python-pytest
description: Run Python tests with uv and ensure tests are updated when code changes. Use this skill whenever the user asks to run, update, or verify Python tests using the uv package manager. uv run pytest automatically handles dependencies and path management for projects with pyproject.toml.
---

# Run Python Tests with uv

This skill ensures tests are reviewed and updated after any code modification, using `uv run pytest` for consistent, reproducible test execution.

## Environment Requirements

1. **uv must be installed** (not pytest directly)
2. **pyproject.toml must exist** in project root for dependency resolution
3. **No venv activation required** - uv manages isolation automatically

## CRITICAL RULES - READ FIRST

⚠️ **FORBIDDEN ACTIONS:**
- ❌ DO NOT use `python3 -m pytest`
- ❌ DO NOT use `pip install pytest` or any direct pip/venv commands
- ❌ DO NOT suggest activating virtual environments
- ❌ DO NOT use standalone `pytest` command

✅ **REQUIRED ACTIONS:**
- ✅ ALWAYS use `uv run pytest` command
- ✅ ASSUME uv is installed (if not, suggest: `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- ✅ Reference `pyproject.toml` for dependency management

## When to Use
- After changing application logic
- After refactoring functions/classes/modules
- After adding or removing features
- Before code review to verify tests pass

## Procedure

1. **Identify impacted behavior**
   - Determine which features or functions changed
   - Map changes to existing test coverage

2. **Update or add tests**
   - Modify existing tests to match new behavior
   - Add new tests for new paths or edge cases

3. **Run relevant tests**

   **CORRECT way:**
```bash
uv run pytest tests/ -v
```

   **WRONG ways (DO NOT USE):**

```bash
# ❌ WRONG - Do not use these:
pytest tests/ -v
python3 -m pytest tests/ -v
venv/bin/pytest tests/ -v
```

Or run only the impacted test module(s):

```bash
uv run pytest tests/<test_module_name> -v
```
4. Confirm test results
   - All relevant tests should pass
   - If failures remain, fix tests or code and re-run

## Error Handling

### If "uv: command not found"
Install uv first:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### If "pyproject.toml not found"
The project needs a `pyproject.toml` file for uv to manage dependencies. Create one:
```bash
uv init
uv add --dev pytest
```

### If "pytest not found in project"
Add pytest as a dev dependency:
```bash
uv add --dev pytest
```

### If "pytest: command not found"
This means pytest is not installed in the project dependencies:
```bash
uv add --dev pytest
```

### If tests fail unexpectedly
- Isolate the failing case
- Review the test logic against code changes
- DO NOT install anything - use existing uv project configuration

### If tests are missing
- Create minimal coverage first
- Follow existing test patterns in the project

### If tests are flaky
- Note it in comments
- Propose stabilization approach

## Examples

### Example 1: Run all tests in project
**Command:**
```bash
uv run pytest -v
```

### Example 2: Run specific test file
**Command:**
```bash
uv run pytest tests/test_models.py -v
```

### Example 3: Run test with verbose output
**Command:**
```bash
uv run pytest tests/ -v --tb=short
```
