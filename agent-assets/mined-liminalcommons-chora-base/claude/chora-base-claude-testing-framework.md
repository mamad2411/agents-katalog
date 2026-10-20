---
sap_id: SAP-004
version: 1.0.0
status: active
last_updated: 2025-11-20
progressive_loading:
  phase_1: "0-5k tokens (quick reference, common commands)"
  phase_2: "5-15k tokens (test patterns, workflows)"
  phase_3: "15k+ tokens (comprehensive, advanced patterns)"
---

# Testing Framework (SAP-004) - Claude-Specific Awareness

**SAP ID**: SAP-004
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-04

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

This CLAUDE.md provides: Claude Code tool patterns (Write tests, Bash pytest, Edit fixes) for TDD workflows.

---

## Quick Start for Claude

This file provides **Claude Code-specific patterns** for pytest-based testing.

### First-Time Testing

1. Read [AGENTS.md](AGENTS.md) for generic testing workflows
2. Use this file for Claude Code tool integration (Write for test files, Bash for pytest, Edit for fixes)
3. Follow 4-step process: Write test → Run pytest → Check coverage → Fix failures

### Session Resumption

- Run `pytest` with Bash tool to see current test status
- Read pyproject.toml for pytest configuration
- Use Edit tool to update tests based on failures

---

## Claude Code Testing Workflows

### Workflow 1: Writing Tests with Claude Code

```markdown
User: "Add tests for validate_input function in src/utils/validation.py"

Claude (Phase 1: Read Implementation - 0-5k tokens):
1. Read src/utils/validation.py
   # Understand function signature, logic, edge cases

Claude (Phase 2: Create Test File - 5-10k tokens):
2. Check if tests/utils/ directory exists:
   Bash: ls -la tests/utils/
   # If not exists: Bash: mkdir -p tests/utils/

3. Write test file:
   Write tests/utils/test_validation.py
   # Content: Imports, test functions, fixtures

Example test file:
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
    assert result is True, f"Expected True for valid data, got {result}"

def test_validate_input_missing_name():
    """Test validate_input with missing name field."""
    data = {"age": 30}
    result = validate_input(data)
    assert result is False, "Expected False when name is missing"

@pytest.mark.parametrize("data,expected", [
    ({"name": "Alice", "age": 30}, True),
    ({"name": "", "age": 30}, False),
    ({"name": "Alice", "age": -1}, False),
    ({}, False),
])
def test_validate_input_edge_cases(data, expected):
    """Test validate_input with various edge cases."""
    result = validate_input(data)
    assert result == expected, f"Expected {expected} for {data}"
```

Claude (Phase 3: Run Tests - 10-15k tokens):
4. Bash: pytest tests/utils/test_validation.py -v

Expected output:
```
tests/utils/test_validation.py::test_validate_input_valid_data PASSED
tests/utils/test_validation.py::test_validate_input_missing_name PASSED
tests/utils/test_validation.py::test_validate_input_edge_cases[data0-True] PASSED
tests/utils/test_validation.py::test_validate_input_edge_cases[data1-False] PASSED
tests/utils/test_validation.py::test_validate_input_edge_cases[data2-False] PASSED
tests/utils/test_validation.py::test_validate_input_edge_cases[data3-False] PASSED

6 passed in 0.12s
```

Claude (Phase 4: Check Coverage - 15-20k tokens):
5. Bash: pytest tests/utils/test_validation.py --cov=src/utils/validation --cov-report=term-missing

Expected output:
```
---------- coverage: platform darwin, python 3.11.5 -----------
Name                           Stmts   Miss  Cover   Missing
------------------------------------------------------------
src/utils/validation.py           12      0   100%
------------------------------------------------------------
TOTAL                             12      0   100%
```

Claude (response to user):
"Tests added for validate_input():
✅ 6 test cases (valid data, missing field, 4 edge cases)
✅ 100% code coverage
✅ All tests passing

Test file: tests/utils/test_validation.py"

Result: Complete test coverage for validate_input function
```

---

### Workflow 2: Writing Async Tests with Claude Code

```markdown
User: "Add async tests for fetch_data MCP tool"

Claude (Phase 1: Read Async Function - 0-5k tokens):
1. Read src/mcp/tools.py
   # Identify: async def fetch_data(resource_id: str) -> dict

Claude (Phase 2: Write Async Test - 5-15k tokens):
2. Write tests/mcp/test_tools.py
   # Content: pytest.mark.asyncio decorator, await syntax

Example async test:
```python
# tests/mcp/test_tools.py
import pytest
from src.mcp.tools import fetch_data
from src.mcp.errors import ResourceNotFoundError

@pytest.mark.asyncio
async def test_fetch_data_success():
    """Test fetch_data with valid resource ID."""
    # Arrange
    resource_id = "resource-123"

    # Act
    result = await fetch_data(resource_id)

    # Assert
    assert result is not None
    assert result["id"] == resource_id

@pytest.mark.asyncio
async def test_fetch_data_not_found():
    """Test fetch_data with non-existent resource ID."""
    resource_id = "invalid-id"

    with pytest.raises(ResourceNotFoundError):
        await fetch_data(resource_id)

@pytest.mark.asyncio
async def test_fetch_data_timeout():
    """Test fetch_data with timeout."""
    resource_id = "slow-resource"

    # Arrange: Mock slow response
    import asyncio
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(fetch_data(resource_id), timeout=0.1)
```

Claude (Phase 3: Run Async Tests - 15-20k tokens):
3. Bash: pytest tests/mcp/test_tools.py -v

Expected output:
```
tests/mcp/test_tools.py::test_fetch_data_success PASSED
tests/mcp/test_tools.py::test_fetch_data_not_found PASSED
tests/mcp/test_tools.py::test_fetch_data_timeout PASSED

3 passed in 0.25s
```

Claude (response to user):
"Async tests added for fetch_data():
✅ 3 test cases (success, not found, timeout)
✅ Uses @pytest.mark.asyncio decorator
✅ All async tests passing

Note: pytest-asyncio handles async/await automatically (asyncio_mode = 'auto' in pyproject.toml)"

Result: Async MCP tool tested with success and error cases
```

---

### Workflow 3: Debugging Test Failures with Claude Code

```markdown
User: "Test test_validate_input_missing_name is failing"

Claude (Phase 1: Run Failing Test - 0-5k tokens):
1. Bash: pytest tests/utils/test_validation.py::test_validate_input_missing_name -v

Output:
```
tests/utils/test_validation.py::test_validate_input_missing_name FAILED

================================= FAILURES =================================
______________ test_validate_input_missing_name ______________

    def test_validate_input_missing_name():
        data = {"age": 30}
        result = validate_input(data)
>       assert result is False
E       AssertionError: assert True is False

tests/utils/test_validation.py:15: AssertionError
```

Claude (Phase 2: Diagnose Issue - 5-10k tokens):
2. Read src/utils/validation.py
   # Line 12: def validate_input(data: dict) -> bool:
   # Line 13:     return "age" in data  # Bug: only checks age, not name

3. Identify bug: Function doesn't check for "name" field

Claude (Phase 3: Fix Implementation - 10-15k tokens):
4. Edit src/utils/validation.py
   # old_string: return "age" in data
   # new_string: return "name" in data and "age" in data

Claude (Phase 4: Verify Fix - 15-20k tokens):
5. Bash: pytest tests/utils/test_validation.py::test_validate_input_missing_name -v

Expected output:
```
tests/utils/test_validation.py::test_validate_input_missing_name PASSED
```

6. Run all tests to ensure no regressions:
   Bash: pytest tests/utils/test_validation.py -v

Claude (response to user):
"Fixed test_validate_input_missing_name failure:

Issue: validate_input() only checked for 'age' field, not 'name'
Fix: Updated validation to check both fields

src/utils/validation.py:13
- return \"age\" in data
+ return \"name\" in data and \"age\" in data

✅ test_validate_input_missing_name now passing
✅ All 6 tests passing
✅ No regressions"

Result: Bug fixed, test passing
```

---

### Workflow 4: Increasing Coverage with Claude Code

```markdown
User: "Coverage is 75%, increase it to 85%"

Claude (Phase 1: Check Coverage - 0-5k tokens):
1. Bash: pytest --cov=src --cov-report=term-missing --cov-fail-under=85

Output:
```
---------- coverage: platform darwin, python 3.11.5 -----------
Name                           Stmts   Miss  Cover   Missing
------------------------------------------------------------
src/utils/validation.py           12      3    75%   18-20
src/utils/errors.py                8      0   100%
------------------------------------------------------------
TOTAL                             20      3    85%

FAIL Required test coverage of 85.0% not reached. Total coverage: 75.00%
```

Claude (Phase 2: Identify Missing Coverage - 5-10k tokens):
2. Read src/utils/validation.py lines 18-20
   # Line 18: if not isinstance(data, dict):
   # Line 19:     raise TypeError("data must be dict")
   # Line 20:     return False

3. Missing coverage: TypeError exception path not tested

Claude (Phase 3: Add Missing Tests - 10-20k tokens):
4. Edit tests/utils/test_validation.py
   # Add test for TypeError

```python
def test_validate_input_invalid_type():
    """Test validate_input with non-dict input."""
    invalid_inputs = [None, "string", 123, []]

    for invalid_input in invalid_inputs:
        with pytest.raises(TypeError, match="data must be dict"):
            validate_input(invalid_input)
```

Claude (Phase 4: Verify Coverage - 20-25k tokens):
5. Bash: pytest --cov=src/utils/validation --cov-report=term-missing --cov-fail-under=85

Expected output:
```
---------- coverage: platform darwin, python 3.11.5 -----------
Name                           Stmts   Miss  Cover   Missing
------------------------------------------------------------
src/utils/validation.py           12      0   100%
------------------------------------------------------------
TOTAL                             12      0   100%
```

Claude (response to user):
"Increased coverage from 75% to 100%:

Added test: test_validate_input_invalid_type()
- Tests TypeError raised for non-dict inputs
- Covers lines 18-20 (previously untested)

Coverage now: 100% (exceeds 85% threshold)
✅ All tests passing"

Result: Coverage increased to 100%, meets threshold
```

---

### Workflow 5: Using Fixtures with Claude Code

```markdown
User: "Add fixture for sample user data, reuse across multiple tests"

Claude (Phase 1: Create Fixture - 0-10k tokens):
1. Check if tests/conftest.py exists:
   Bash: ls -la tests/conftest.py

2. If not exists, create conftest.py:
   Write tests/conftest.py
   # Content: Shared fixtures

If exists, Edit tests/conftest.py:
```python
# tests/conftest.py
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
def sample_users():
    """Fixture providing multiple sample users."""
    return [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25},
        {"name": "Charlie", "age": 35}
    ]

@pytest.fixture
def mock_database():
    """Fixture providing mock database."""
    db = MockDatabase()
    db.connect()
    yield db  # Provide to test
    db.disconnect()  # Cleanup
```

Claude (Phase 2: Update Tests to Use Fixture - 10-20k tokens):
3. Edit tests/utils/test_validation.py
   # Replace hardcoded data with fixture parameter

```python
# Before (hardcoded data)
def test_validate_user():
    user = {"name": "Alice", "age": 30}
    assert validate_user(user) is True

# After (using fixture)
def test_validate_user(sample_user_data):
    assert validate_user(sample_user_data) is True

def test_user_email_validation(sample_user_data):
    assert validate_email(sample_user_data["email"]) is True
```

Claude (Phase 3: Verify Tests - 20-25k tokens):
4. Bash: pytest tests/utils/test_validation.py -v

Claude (response to user):
"Created shared fixtures in tests/conftest.py:
✅ sample_user_data: Single user fixture
✅ sample_users: Multiple users fixture
✅ mock_database: Database fixture with cleanup

Updated 3 tests to use fixtures:
- test_validate_user()
- test_user_email_validation()
- test_database_query()

Benefits:
- Test data centralized (easier to maintain)
- Automatic cleanup (yield pattern)
- Reusable across all test files"

Result: Tests use shared fixtures, easier to maintain
```

---

## Claude-Specific Tips

### Tip 1: Use Write for New Test Files, Edit for Updates

**Pattern**:
```bash
# New test file (file doesn't exist)
Write tests/utils/test_validation.py

# Update existing test file (add new test)
Edit tests/utils/test_validation.py
# old_string: (last test function)
# new_string: (last test function + new test function)
```

**Why**: Write creates new files, Edit modifies existing files (preserves other tests)

---

### Tip 2: Run pytest with Bash Tool, Not Python Subprocess

**Pattern**:
```bash
# Correct: Use Bash tool
Bash: pytest tests/utils/test_validation.py -v

# Wrong: Don't use python -m pytest in subprocess
# (slower, harder to capture output)
```

**Why**: Bash tool is optimized for command execution, better output capture

---

### Tip 3: Check Coverage After Writing Tests

**Pattern**:
```bash
# Always check coverage after writing tests
Bash: pytest tests/utils/test_validation.py --cov=src/utils/validation --cov-report=term-missing

# If coverage <85%, identify missing lines from "Missing" column
# Read those lines in source file
# Add tests to cover missing lines
```

**Why**: Ensures tests actually cover the code (not just pass)

---

### Tip 4: Use Parametrize for Multiple Similar Tests

**Pattern**:
```python
# Instead of multiple similar tests:
def test_validate_input_case1():
    assert validate_input({"name": "Alice", "age": 30}) is True

def test_validate_input_case2():
    assert validate_input({"name": "", "age": 30}) is False

# Use parametrize (one test, multiple cases):
@pytest.mark.parametrize("data,expected", [
    ({"name": "Alice", "age": 30}, True),
    ({"name": "", "age": 30}, False),
])
def test_validate_input(data, expected):
    assert validate_input(data) == expected
```

**Why**: Less code duplication, easier to add new cases

---

### Tip 5: Always Use @pytest.mark.asyncio for Async Tests

**Pattern**:
```python
# Async test MUST have decorator
@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result is not None
```

**Why**: Without decorator, async test runs synchronously, raises "coroutine was never awaited" error

---

## Common Pitfalls for Claude Code

### Pitfall 1: Using Write Instead of Edit for Existing Test Files

**Problem**: Write overwrites entire file, loses other tests

**Wrong**:
```bash
# File already has 5 tests
Write tests/utils/test_validation.py
# Content: Only new test (loses 5 existing tests)
```

**Correct**:
```bash
# Read file first to check if exists
Read tests/utils/test_validation.py

# If exists, use Edit to add new test
Edit tests/utils/test_validation.py
# old_string: (last test function)
# new_string: (last test function + new test)
```

---

### Pitfall 2: Not Running All Tests After Fix

**Problem**: Fix passes for one test but breaks another test

**Wrong**:
```bash
# Fix bug
Edit src/utils/validation.py

# Only run failing test
Bash: pytest tests/utils/test_validation.py::test_specific_test -v
# (might break other tests)
```

**Correct**:
```bash
# Fix bug
Edit src/utils/validation.py

# Run ALL tests to check for regressions
Bash: pytest tests/utils/test_validation.py -v
```

---

### Pitfall 3: Forgetting --cov= Target

**Problem**: Coverage report includes unrelated files

**Wrong**:
```bash
# Coverage measures everything
Bash: pytest --cov --cov-report=term-missing
# Output: Includes tests/, scripts/, etc. (not useful)
```

**Correct**:
```bash
# Coverage measures only src/
Bash: pytest --cov=src --cov-report=term-missing
# Output: Only shows src/ coverage
```

---

### Pitfall 4: Not Checking pyproject.toml Before Running Tests

**Problem**: Run pytest without knowing configuration, unexpected behavior

**Wrong**:
```bash
# Run pytest without checking config
Bash: pytest
# (might use wrong testpaths, coverage threshold, etc.)
```

**Correct**:
```bash
# Check config first (especially on first run)
Read pyproject.toml
# Look for [tool.pytest.ini_options], [tool.coverage.run]

# Then run pytest
Bash: pytest
```

---

### Pitfall 5: Writing Tests Without Reading Implementation

**Problem**: Tests don't match actual function behavior

**Wrong**:
```bash
# Write tests without reading function
Write tests/utils/test_validation.py
# (tests may not match actual validate_input() signature/behavior)
```

**Correct**:
```bash
# Read implementation first
Read src/utils/validation.py
# Understand: signature, return type, edge cases, exceptions

# Then write matching tests
Write tests/utils/test_validation.py
```

---

## Tool Usage Patterns

### Using Bash Tool for pytest

```bash
# Run all tests
Bash: pytest

# Run specific file
Bash: pytest tests/utils/test_validation.py

# Run specific test
Bash: pytest tests/utils/test_validation.py::test_validate_input

# Run with coverage
Bash: pytest --cov=src --cov-report=term-missing

# Run with verbose output
Bash: pytest -v

# Run and stop at first failure
Bash: pytest -x

# Run last failed tests only
Bash: pytest --lf

# Run with HTML coverage report
Bash: pytest --cov=src --cov-report=html
```

---

### Using Write Tool for New Test Files

```bash
# Check if test file exists first
Bash: ls tests/utils/test_validation.py
# If error (file not exists), use Write

Write tests/utils/test_validation.py
# Content: Imports, test functions, fixtures
```

---

### Using Edit Tool for Updating Tests

```bash
# Read file first to understand structure
Read tests/utils/test_validation.py

# Add new test function
Edit tests/utils/test_validation.py
# old_string: (last test function including docstring and body)
# new_string: (last test function + new test function)
```

---

### Using Read Tool for Debugging

```bash
# Read test file to see failure context
Read tests/utils/test_validation.py

# Read source file to understand implementation
Read src/utils/validation.py

# Read pyproject.toml to check configuration
Read pyproject.toml
```

---

## Support & Resources

**SAP-004 Documentation**:
- [AGENTS.md](AGENTS.md) - Generic testing workflows
- [Capability Charter](capability-charter.md) - Problem, solution, design decisions
- [Protocol Spec](protocol-spec.md) - pytest configuration, test patterns
- [Adoption Blueprint](adoption-blueprint.md) - Setup guide (10 min)
- [Ledger](ledger.md) - Adoption tracking, version history

**External Resources**:
- [pytest Documentation](https://docs.pytest.org/) - Official pytest docs
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/) - Async test support
- [pytest-cov](https://pytest-cov.readthedocs.io/) - Coverage measurement
- [Martin Fowler - Test Coverage](https://martinfowler.com/bliki/TestCoverage.html) - Coverage best practices

**Related SAPs**:
- [SAP-005 (ci-cd-workflows)](../ci-cd-workflows/) - GitHub Actions test automation
- [SAP-003 (project-bootstrap)](../project-bootstrap/) - New project testing setup
- [SAP-006 (quality-gates)](../quality-gates/) - Coverage enforcement

**Common Commands for Claude Code**:
```bash
# Write new test file
Write tests/utils/test_validation.py

# Update existing test file
Edit tests/utils/test_validation.py

# Run tests
Bash: pytest tests/utils/test_validation.py -v

# Check coverage
Bash: pytest --cov=src/utils/validation --cov-report=term-missing

# Debug test failure
Bash: pytest tests/utils/test_validation.py::test_name -v -s

# Read implementation to understand behavior
Read src/utils/validation.py

# Read test configuration
Read pyproject.toml
```

---

## Version History

- **1.0.0** (2025-11-04): Initial CLAUDE.md for SAP-004
  - 5 Claude Code workflows: Write tests, async tests, debug failures, increase coverage, fixtures
  - 5 tips: Write vs Edit, Bash for pytest, check coverage, parametrize, async decorator
  - 5 common pitfalls: Write overwrites, run all tests, --cov target, check config, read implementation
  - Tool usage patterns: Bash for pytest, Write for new files, Edit for updates, Read for debugging

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for generic testing workflows
2. Use Bash tool for pytest commands
3. Use Write tool for new test files, Edit tool for updates
4. Always check coverage after writing tests (--cov=src --cov-report=term-missing)
5. Read implementation before writing tests to understand behavior
