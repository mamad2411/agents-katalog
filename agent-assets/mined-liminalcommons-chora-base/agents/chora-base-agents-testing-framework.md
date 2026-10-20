---
sap_id: SAP-004
version: 1.0.0
status: active
last_updated: 2025-11-05
type: comprehensive_guide
audience: all_agents
complexity: intermediate
estimated_reading_time: 45
progressive_loading:
  phase_1: "lines 1-200"
  phase_2: "lines 201-450"
  phase_3: "full"
phase_1_token_estimate: 5000
phase_2_token_estimate: 6250
phase_3_token_estimate: 5800
tags:
  - testing
  - pytest
  - coverage
  - quality-gates
  - production
---

# Testing Framework (SAP-004) - Agent Awareness Guide

**SAP ID**: SAP-004
**Agent Compatibility**: All AI agents with file read/write and command execution
**Last Updated**: 2025-11-05

---

## 📖 Quick Reference

**New to SAP-004?** → Read **[README.md](README.md)** first (8-min read)

The README provides:
- 🚀 **Quick Start** - 8 CLI commands for running tests (test, smoke, coverage, verbose) with <60s local feedback
- 📚 **Time Savings** - 90% bug prevention via TDD, 15-20 min saved per session (avoid manual testing)
- 🎯 **4 Testing Patterns** - Async tests, parametrized tests, fixtures, mocking with pytest best practices
- 🔧 **Coverage Standards** - 85% target (research-backed sweet spot balancing thoroughness vs maintenance)
- 📊 **Success Metrics** - 95%+ bug detection, <60s test execution, ≥85% coverage, 90% CI pass rate
- 🔗 **Integration** - Works with SAP-005 (CI/CD), SAP-006 (Quality Gates), SAP-012 (TDD), SAP-003 (Bootstrap), SAP-014 (MCP)

This AGENTS.md provides: Agent-executable workflows for writing tests, running tests, debugging failures, and TDD cycles.

---

## Quick Start for Agents

This file provides **generic agent workflows** for using chora-base's pytest-based testing framework.

### First-Time Testing

1. Read [CLAUDE.md](CLAUDE.md) for Claude Code-specific patterns
2. Use this file for generic testing workflows (write tests, run tests, debug failures)
3. Follow pytest conventions: tests/ directory, test_*.py files, test_* functions

### Session Resumption

- Check pyproject.toml for pytest configuration (asyncio_mode, testpaths, coverage threshold)
- Run pytest to see current test status
- Read test failures to understand what needs fixing

---

## Common Workflows

### Workflow 1: Writing Unit Tests for New Functions

```markdown
## Context
User has added new function `validate_input(data: dict) -> bool` to src/utils/validation.py

## Steps

Step 1: Create test file
- Location: tests/utils/test_validation.py
- Pattern: tests/{module_path}/test_{module_name}.py

Step 2: Write basic test using Arrange-Act-Assert pattern
```python
# tests/utils/test_validation.py
import pytest
from src.utils.validation import validate_input

def test_validate_input_valid_data():
    """Test validate_input with valid data."""
    # Arrange
    data = {"name": "Alice", "age": 30}

    # Act
    result = validate_input(data)

    # Assert
    assert result is True

def test_validate_input_missing_name():
    """Test validate_input with missing name field."""
    # Arrange
    data = {"age": 30}

    # Act
    result = validate_input(data)

    # Assert
    assert result is False

def test_validate_input_empty_dict():
    """Test validate_input with empty dictionary."""
    data = {}
    result = validate_input(data)
    assert result is False
```

Step 3: Run tests locally
```bash
pytest tests/utils/test_validation.py
```

Step 4: Verify coverage
```bash
pytest tests/utils/test_validation.py --cov=src/utils/validation --cov-report=term-missing
```

Expected output:
```
tests/utils/test_validation.py ...                     [100%]

---------- coverage: platform darwin, python 3.11.5 -----------
Name                           Stmts   Miss  Cover   Missing
------------------------------------------------------------
src/utils/validation.py           12      0   100%
------------------------------------------------------------
TOTAL                             12      0   100%
```

Result: New function has 100% test coverage, ready to commit
```

---

### Workflow 2: Writing Async Tests for MCP Operations

```markdown
## Context
User has added async MCP tool: async def fetch_data(resource_id: str) -> dict

## Steps

Step 1: Create async test file
- Location: tests/mcp/test_tools.py
- Use pytest-asyncio for async tests

Step 2: Write async test
```python
# tests/mcp/test_tools.py
import pytest
from src.mcp.tools import fetch_data

@pytest.mark.asyncio
async def test_fetch_data_success():
    """Test fetch_data with valid resource ID."""
    # Arrange
    resource_id = "resource-123"

    # Act
    result = await fetch_data(resource_id)

    # Assert
    assert result is not None
    assert "id" in result
    assert result["id"] == resource_id

@pytest.mark.asyncio
async def test_fetch_data_not_found():
    """Test fetch_data with non-existent resource ID."""
    # Arrange
    resource_id = "invalid-id"

    # Act & Assert
    with pytest.raises(ResourceNotFoundError):
        await fetch_data(resource_id)
```

Step 3: Run async tests
```bash
pytest tests/mcp/test_tools.py -v
```

Expected output:
```
tests/mcp/test_tools.py::test_fetch_data_success PASSED       [50%]
tests/mcp/test_tools.py::test_fetch_data_not_found PASSED     [100%]
```

**Key Pattern**: Use `@pytest.mark.asyncio` decorator for async tests
**Why**: pytest-asyncio wraps async tests in asyncio.run() automatically (asyncio_mode = "auto" in pyproject.toml)

Result: Async MCP tool has test coverage for success and error cases
```

---

### Workflow 3: Using Fixtures for Test Setup

```markdown
## Context
Multiple tests need the same test data setup (mock database, sample objects)

## Steps

Step 1: Create fixture in conftest.py or test file
```python
# tests/conftest.py (shared fixtures) or tests/utils/test_validation.py (local)
import pytest

@pytest.fixture
def sample_user_data():
    """Fixture providing sample user data for tests."""
    return {
        "name": "Alice",
        "age": 30,
        "email": "alice@example.com"
    }

@pytest.fixture
def mock_database():
    """Fixture providing mock database connection."""
    db = MockDatabase()
    db.connect()
    yield db  # Provide to test
    db.disconnect()  # Cleanup after test

@pytest.fixture
def temp_file(tmp_path):
    """Fixture providing temporary file using pytest's tmp_path."""
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("test content")
    return file_path
```

Step 2: Use fixtures in tests
```python
def test_user_validation_with_fixture(sample_user_data):
    """Test user validation using fixture data."""
    result = validate_user(sample_user_data)
    assert result is True

def test_database_query_with_fixture(mock_database):
    """Test database query using mock database."""
    mock_database.insert({"id": 1, "name": "Alice"})
    result = mock_database.query(id=1)
    assert result["name"] == "Alice"

def test_file_reading_with_fixture(temp_file):
    """Test file reading using temporary file."""
    content = temp_file.read_text()
    assert content == "test content"
```

**Key Patterns**:
- Fixture with `yield`: Setup before yield, cleanup after yield
- Fixture scope: `@pytest.fixture(scope="module")` for shared fixtures across tests
- Fixture location: conftest.py for shared, test file for local
- Built-in fixtures: `tmp_path` (temporary directory), `capsys` (capture stdout)

Result: Test data setup is reusable, tests are cleaner, cleanup is automatic
```

---

### Workflow 4: Parametrized Tests for Multiple Inputs

```markdown
## Context
Need to test same function with multiple input combinations

## Steps

Step 1: Write parametrized test
```python
import pytest

@pytest.mark.parametrize("input_data,expected", [
    ({"name": "Alice", "age": 30}, True),          # Valid data
    ({"name": "", "age": 30}, False),              # Empty name
    ({"name": "Alice", "age": -1}, False),         # Invalid age
    ({"name": "Alice"}, False),                     # Missing age
    ({}, False),                                    # Empty dict
])
def test_validate_input_parametrized(input_data, expected):
    """Test validate_input with multiple input combinations."""
    result = validate_input(input_data)
    assert result == expected, f"Expected {expected} for input {input_data}"
```

Step 2: Run parametrized test
```bash
pytest tests/utils/test_validation.py::test_validate_input_parametrized -v
```

Expected output:
```
test_validate_input_parametrized[input_data0-True] PASSED     [20%]
test_validate_input_parametrized[input_data1-False] PASSED    [40%]
test_validate_input_parametrized[input_data2-False] PASSED    [60%]
test_validate_input_parametrized[input_data3-False] PASSED    [80%]
test_validate_input_parametrized[input_data4-False] PASSED    [100%]
```

**Key Pattern**: `@pytest.mark.parametrize("param_names", [param_values])`
**Why**: One test function tests multiple cases, reduces code duplication

Result: 5 test cases with 1 test function, comprehensive coverage
```

---

### Workflow 5: Running Tests with Coverage Reports

```markdown
## Context
Need to verify test coverage meets 85% threshold

## Steps

Step 1: Run all tests with coverage
```bash
pytest --cov=src --cov-report=term-missing --cov-fail-under=85
```

Step 2: Interpret coverage output
```
---------- coverage: platform darwin, python 3.11.5 -----------
Name                           Stmts   Miss  Cover   Missing
------------------------------------------------------------
src/utils/validation.py           12      2    83%   45-46
src/utils/errors.py                8      0   100%
src/utils/responses.py            15      1    93%   78
------------------------------------------------------------
TOTAL                             35      3    91%

✅ Required test coverage of 85.0% reached. Total coverage: 91.43%
```

**Interpretation**:
- Overall coverage: 91% (✅ exceeds 85% threshold)
- validation.py: 83% (⚠️ below threshold, lines 45-46 not tested)
- Missing lines: Check "Missing" column (e.g., 45-46, 78)

Step 3: Add tests for missing lines
- Read src/utils/validation.py lines 45-46
- Write test that exercises those lines
- Re-run coverage to verify 100%

Step 4: Generate HTML coverage report (optional)
```bash
pytest --cov=src --cov-report=html
open htmlcov/index.html  # View detailed coverage with highlighted missing lines
```

**Key Pattern**: Use `--cov-report=term-missing` to see which lines need tests
**Why**: Quickly identify untested code paths

Result: Coverage increased from 83% to 100% for validation.py
```

---

### Workflow 6: Debugging Test Failures

```markdown
## Context
Test failing with unclear error message

## Steps

Step 1: Run failing test with verbose output
```bash
pytest tests/utils/test_validation.py::test_validate_input_missing_name -v
```

Expected output:
```
tests/utils/test_validation.py::test_validate_input_missing_name FAILED [100%]

================================= FAILURES =================================
______________ test_validate_input_missing_name ______________

    def test_validate_input_missing_name():
        data = {"age": 30}
        result = validate_input(data)
>       assert result is False
E       AssertionError: assert True is False

tests/utils/test_validation.py:15: AssertionError
```

**Interpretation**:
- Expected: `result is False` (validation should fail)
- Actual: `result is True` (validation passed unexpectedly)
- Issue: validate_input() not checking for missing "name" field

Step 2: Add debug output (if needed)
```python
def test_validate_input_missing_name():
    data = {"age": 30}
    result = validate_input(data)
    print(f"DEBUG: result={result}, data={data}")  # Debug output
    assert result is False
```

Run with `-s` to see print statements:
```bash
pytest tests/utils/test_validation.py::test_validate_input_missing_name -v -s
```

Step 3: Fix the bug
- Read src/utils/validation.py
- Add check for "name" field
- Re-run test to verify fix

Step 4: Remove debug output
- Clean up print statements after debugging

**Debugging Tools**:
- `pytest -v`: Verbose output (show test names, assertions)
- `pytest -s`: Show print statements
- `pytest -x`: Stop at first failure
- `pytest --lf`: Run last failed tests only
- `pytest --pdb`: Drop into debugger on failure

Result: Test passes after bug fix
```

---

## Testing Patterns Reference

### Test File Naming

| Pattern | Example | Purpose |
|---------|---------|---------|
| `test_*.py` | `test_validation.py` | pytest discovers files starting with "test_" |
| `tests/{module_path}/` | `tests/utils/` | Mirror src/ directory structure |
| `test_{function_name}` | `test_validate_input` | pytest discovers functions starting with "test_" |

### Test Function Patterns

```python
# Basic test (Arrange-Act-Assert)
def test_function_name():
    # Arrange
    input_data = setup_test_data()

    # Act
    result = function_to_test(input_data)

    # Assert
    assert result == expected

# Async test
@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result is not None

# Parametrized test
@pytest.mark.parametrize("input,expected", [(1, 2), (3, 4)])
def test_with_params(input, expected):
    assert function(input) == expected

# Test with fixture
def test_with_fixture(fixture_name):
    assert fixture_name is not None

# Test exception
def test_raises_error():
    with pytest.raises(ValueError):
        function_that_raises()

# Test with mocking
from unittest.mock import patch, MagicMock

def test_with_mock():
    with patch('module.function') as mock_func:
        mock_func.return_value = "mocked"
        result = call_function()
        assert result == "mocked"
```

### Coverage Thresholds

| Coverage | Status | Action |
|----------|--------|--------|
| ≥85% | ✅ Pass | Meets chora-base standard |
| 80-84% | ⚠️ Warning | Add tests for critical paths |
| <80% | ❌ Fail | Insufficient coverage, block merge |

**Rationale**: 85% threshold based on industry research (Martin Fowler, Google Testing Blog) - balances bug detection (catches 95% of bugs) with test maintenance cost.

---

## Integration with Development Workflow

### DDD → BDD → TDD Flow

```
Domain-Driven Design (DDD): Define domain model
    │
    v
[Identify bounded contexts, entities, value objects]
    │
    v
Behavior-Driven Design (BDD): Specify behavior
    │
    v
[Write user stories, acceptance criteria]
    │
    v
Test-Driven Development (TDD): Write tests first
    │
    v
[Write failing test → Implement → Test passes → Refactor]
    │
    v
[Run pytest → Coverage check → CI validation]
```

**Example**:
1. **DDD**: Domain model has `User` entity with `validate()` method
2. **BDD**: User story: "As a developer, I want user validation to reject invalid emails"
3. **TDD**: Write `test_validate_user_invalid_email()` → Implement `User.validate()` → Test passes
4. **Testing Framework**: Run `pytest --cov=src --cov-fail-under=85`

---

## Common Pitfalls for Agents

### Pitfall 1: Forgetting `@pytest.mark.asyncio` for Async Tests

**Problem**: Async test function runs synchronously, raises "coroutine was never awaited" error

**Wrong**:
```python
async def test_async_function():  # Missing decorator
    result = await async_function()
    assert result is not None
```

**Correct**:
```python
@pytest.mark.asyncio  # Required for async tests
async def test_async_function():
    result = await async_function()
    assert result is not None
```

---

### Pitfall 2: Not Mirroring src/ Directory Structure in tests/

**Problem**: tests/ directory structure doesn't match src/, hard to find tests

**Wrong**:
```
src/utils/validation.py
tests/test_all_utils.py  # All utils tests in one file
```

**Correct**:
```
src/utils/validation.py
tests/utils/test_validation.py  # Mirror src/ structure
```

---

### Pitfall 3: Hardcoding Test Data Instead of Using Fixtures

**Problem**: Test data duplicated across multiple tests, changes require updating many tests

**Wrong**:
```python
def test_user_validation():
    user = {"name": "Alice", "age": 30}  # Duplicated
    assert validate_user(user) is True

def test_user_query():
    user = {"name": "Alice", "age": 30}  # Duplicated
    assert query_user(user["name"]) is not None
```

**Correct**:
```python
@pytest.fixture
def sample_user():
    return {"name": "Alice", "age": 30}

def test_user_validation(sample_user):
    assert validate_user(sample_user) is True

def test_user_query(sample_user):
    assert query_user(sample_user["name"]) is not None
```

---

### Pitfall 4: Not Running Coverage Checks Before Committing

**Problem**: Tests pass locally but coverage <85%, CI fails

**Wrong**:
```bash
pytest  # Runs tests but doesn't check coverage
git commit  # Commits without coverage verification
```

**Correct**:
```bash
pytest --cov=src --cov-fail-under=85  # Check coverage
# If coverage <85%, add more tests
git commit
```

---

### Pitfall 5: Using `assert` Without Descriptive Messages

**Problem**: Test failure message unclear, hard to debug

**Wrong**:
```python
def test_validate_input():
    assert validate_input(data)  # Unclear what failed
```

**Better**:
```python
def test_validate_input():
    result = validate_input(data)
    assert result is True, f"Expected validation to pass for data={data}, got {result}"
```

---

## Support & Resources

**SAP-004 Documentation**:
- [Capability Charter](capability-charter.md) - Problem, solution, design decisions
- [Protocol Spec](protocol-spec.md) - Technical specification (pytest config, test patterns)
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide (10 min setup)
- [Ledger](ledger.md) - Adoption tracking, version history
- [CLAUDE.md](CLAUDE.md) - Claude Code-specific testing patterns

**External Resources**:
- [pytest Documentation](https://docs.pytest.org/) - Official pytest docs
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/) - Async test support
- [pytest-cov](https://pytest-cov.readthedocs.io/) - Coverage measurement
- [Martin Fowler - Test Coverage](https://martinfowler.com/bliki/TestCoverage.html) - Coverage best practices
- [Google Testing Blog](https://testing.googleblog.com/) - Testing patterns and principles

**Related SAPs**:
- [SAP-005 (ci-cd-workflows)](../ci-cd-workflows/) - GitHub Actions test automation
- [SAP-003 (project-bootstrap)](../project-bootstrap/) - New project testing setup
- [SAP-006 (quality-gates)](../quality-gates/) - Coverage enforcement, pre-commit hooks
- [SAP-000 (sap-framework)](../sap-framework/) - Framework foundation

**Common pytest Commands**:
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/utils/test_validation.py

# Run specific test function
pytest tests/utils/test_validation.py::test_validate_input

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Run with verbose output
pytest -v

# Run with debug output (print statements)
pytest -s

# Run async tests only
pytest -m asyncio

# Run and stop at first failure
pytest -x

# Run last failed tests
pytest --lf

# Run with HTML coverage report
pytest --cov=src --cov-report=html
```

---

## Version History

- **2.0.0** (2025-11-04): Updated to Phase 2 awareness format
  - 6 common workflows: Write unit tests, async tests, fixtures, parametrized tests, coverage reports, debugging
  - Testing patterns reference (test naming, function patterns, coverage thresholds)
  - Integration with DDD → BDD → TDD workflow
  - 5 common pitfalls (async decorator, directory structure, fixtures, coverage checks, assert messages)
  - Migrated from signal patterns format to generic workflows format
- **1.1.0** (2025-10-31): Added User Signal Patterns section for bidirectional translation layer integration
- **1.0.0** (2025-10-31): Initial domain AGENTS.md for testing framework

---

**Next Steps**:
1. Read [CLAUDE.md](CLAUDE.md) for Claude Code-specific testing patterns
2. Review [protocol-spec.md](protocol-spec.md) for pytest configuration details
3. Check [adoption-blueprint.md](adoption-blueprint.md) for setup guide (10 min)
4. Write tests following patterns: tests/{module}/test_{module}.py, test_* functions, @pytest.mark.asyncio for async
