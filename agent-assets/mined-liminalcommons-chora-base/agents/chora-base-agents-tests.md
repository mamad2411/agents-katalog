# Testing Guide for {{ project_name }}

**Purpose**: Comprehensive testing instructions for AI agents and human developers.

**Parent**: See [../AGENTS.md](../AGENTS.md) for project overview and other topics.

**For Claude users**: See [CLAUDE.md](CLAUDE.md) for Claude-specific test generation patterns.

---

## Development Workflow Integration

This testing guide supports the **Test-Driven Development (TDD)** workflow.

**TDD Process** ([dev-docs/workflows/TDD_WORKFLOW.md](../dev-docs/workflows/TDD_WORKFLOW.md)):
1. **RED**: Write failing test first
2. **GREEN**: Implement minimal code to pass
3. **REFACTOR**: Improve code while keeping tests green

**Benefits:**
- 40-80% fewer defects (Microsoft Research)
- Better code design (testability enforces modularity)
- Living documentation (tests show intended behavior)
- Confident refactoring (tests catch regressions)

**Quick Decision Tree:**
- **Write unit tests first?** → **YES** (TDD reduces defects 40-80%)
- **Minimum coverage?** → **{{ test_coverage_threshold }}%** (configured in pyproject.toml)
- **Test naming?** → `test_[function]_[scenario]_[expected]`

See [../dev-docs/workflows/TDD_WORKFLOW.md](../dev-docs/workflows/TDD_WORKFLOW.md) for complete guide.

---

## Quick Reference

- **Run all tests**: `{% if include_justfile %}just test{% else %}pytest{% endif %}`
- **Run with coverage**: `{% if include_justfile %}just test-coverage{% else %}pytest --cov={{ package_name }}{% endif %}`
- **Smoke tests**: `{% if include_justfile %}just smoke{% else %}pytest tests/smoke/{% endif %}`
- **Pre-merge check**: `{% if include_justfile %}just pre-merge{% else %}./scripts/pre-merge.sh{% endif %}`

---

## Reusable Test Fixtures

This project includes reusable test fixtures in [conftest.py](conftest.py) to streamline test writing:

### Filesystem Fixtures
- `temp_workspace` - Clean temporary directory for each test
- `temp_project_structure` - Typical project layout (src/, tests/, docs/, config/)

### Module Loading
- `load_hyphenated_script` - Load Python scripts with hyphens (e.g., `my-script.py`)
  - **Use case**: Testing CLI scripts that can't be imported normally
  - **Pattern**: From chora-workspace SAP-004 reference tests

### Mock Data
- `sample_json_data` - Common JSON structure for parser/serializer tests

### Utilities
- `mock_file_operations` - Mock file I/O without filesystem access
- `captured_output` - Capture print() statements for testing

### Example Usage

See [test_example.py.template](test_example.py.template) for complete examples of:
- Testing with temporary workspaces
- Testing hyphenated scripts (importlib pattern)
- Parametrized tests
- Error handling tests
- Async tests
- Test class organization

**Quick Example**:
```python
def test_config_file(temp_workspace):
    """Test config file creation."""
    config = temp_workspace / "config.json"
    config.write_text('{"key": "value"}')
    assert config.exists()
```

---

## Testing Instructions

### Run All Tests

```bash
{% if include_justfile -%}
# Using just (recommended)
just test

{% endif -%}
# Direct pytest
pytest

# With coverage report
{% if include_justfile -%}
just test-coverage
# OR
{% endif -%}
pytest --cov={{ package_name }} --cov-report=term-missing
```

{% if include_tests -%}
### Smoke Tests (Quick Validation)

```bash
{% if include_justfile -%}
# Fast smoke tests (<30 seconds)
just smoke

{% endif -%}
# Direct pytest
pytest tests/smoke/ -v
```

### Test Categories

```bash
# Unit tests only
pytest tests/ -k "not integration and not smoke" -v

# Integration tests
pytest tests/integration/ -v

# Specific test file
pytest tests/test_example.py -v

# Specific test function
pytest tests/test_example.py::test_function -v
```

{% endif -%}
{% if include_pre_commit -%}
### Pre-Commit Hooks

```bash
{% if include_justfile -%}
# Run all pre-commit checks
just pre-commit
# OR
{% endif -%}
pre-commit run --all-files

# Install hooks (one-time setup)
pre-commit install

# Run specific hook
pre-commit run ruff --all-files
pre-commit run mypy --all-files
```

### Linting & Type Checking

```bash
{% if include_justfile -%}
# All quality checks (lint + typecheck + format)
just check

# Individual checks
just lint       # Ruff linting
just typecheck  # Mypy type checking
just format     # Ruff formatting

{% endif -%}
# Manual commands
ruff check src/{{ package_name }} tests/
mypy src/{{ package_name }}
ruff format src/{{ package_name }} tests/

# Auto-fix linting issues
ruff check --fix src/{{ package_name }} tests/
```

{% endif -%}
{% if include_tests -%}
### Coverage Requirements

- **Overall coverage:** ≥{{ test_coverage_threshold }}%
- **Critical paths:** 100% ([list critical paths])
- **[Module name]:** ≥90% ([describe module])

{% endif -%}
{% if include_justfile -%}
### Pre-Merge Verification

```bash
# Full verification before submitting PR
just pre-merge

# Equivalent to:
{% if include_pre_commit -%}
# - pre-commit run --all-files
{% endif -%}
{% if include_tests -%}
# - pytest (smoke + full test suite)
# - coverage check
{% endif -%}
```

{% endif -%}
{% if include_tests -%}

### System-Level Validation (Super-Tests)

**Philosophy:** Test workflows and system behavior, not just individual units.

Super-tests validate **end-to-end scenarios** that users actually experience, rather than granular unit tests. This approach catches integration issues, configuration problems, and emergent behavior that unit tests miss.

**When to write super-tests:**
- ✅ Before releasing a new feature (does the full workflow work?)
- ✅ After fixing a bug (does the scenario now succeed end-to-end?)
- ✅ When adding integrations (do all components work together?)
- ✅ For critical user journeys (can users accomplish their goals?)

**Example super-test patterns:**

```bash
{% if include_justfile -%}
# Run system-level validation
just super-test

# What this validates:
{% endif -%}
# 1. Full application startup and initialization
# 2. End-to-end workflow completion
# 3. Integration between all components
# 4. Configuration loading and environment setup
# 5. Error handling in realistic scenarios
```

{% if project_type == 'mcp_server' -%}
**MCP Server Super-Test Example:**
```python
# tests/super/test_full_workflow.py
def test_mcp_server_lifecycle():
    """Validate complete MCP server lifecycle: start → register tools → execute → shutdown."""
    # Start server
    server = create_server()

    # Verify all tools registered
    tools = server.list_tools()
    assert len(tools) == EXPECTED_TOOL_COUNT

    # Execute representative workflow
    result = server.call_tool("primary_tool", {"param": "value"})
    assert result.success

    # Verify side effects (files written, state updated, etc.)
    assert expected_output_exists()

    # Clean shutdown
    server.shutdown()
```

{% elif project_type == 'cli_tool' -%}
**CLI Tool Super-Test Example:**
```python
# tests/super/test_full_workflow.py
def test_cli_end_to_end_workflow(tmp_path):
    """Validate complete CLI workflow: init → process → output."""
    # Run full workflow
    result = run_cli([
        "init", "--config", str(tmp_path / "config.yml"),
        "process", "--input", "test_data.json",
        "export", "--format", "csv"
    ])

    # Verify end state
    assert result.exit_code == 0
    assert (tmp_path / "output.csv").exists()
    assert validate_output_format(tmp_path / "output.csv")
```

{% elif project_type == 'web_service' -%}
**Web Service Super-Test Example:**

```python
# tests/super/test_full_workflow.py
async def test_api_end_to_end_workflow(test_client):
    """Validate complete API workflow: auth → create → retrieve → update → delete."""
    # Authenticate
    auth_response = await test_client.post("/auth/login", json=credentials)
    token = auth_response.json()["access_token"]

    # Full CRUD workflow
    created = await test_client.post("/items", json=item_data, headers={"Authorization": f"Bearer {token}"})
    retrieved = await test_client.get(f"/items/{created.json()['id']}", headers={"Authorization": f"Bearer {token}"})
    updated = await test_client.put(f"/items/{created.json()['id']}", json=updated_data, headers={"Authorization": f"Bearer {token}"})

    # Verify end state
    assert retrieved.status_code == 200
    assert updated.json()["field"] == updated_data["field"]
```


{% endif -%}
**Benefits of super-tests:**
- 🎯 Catch integration bugs unit tests miss
- 🎯 Validate realistic user scenarios
- 🎯 Test configuration and environment setup
- 🎯 Verify error handling in context
- 🎯 Build confidence before releases

**Balance with unit tests:**
- **Unit tests:** Fast, focused, validate logic in isolation (70-80% of tests)
- **Super-tests:** Slower, comprehensive, validate workflows (20-30% of tests)

Use both. Unit tests give fast feedback during development. Super-tests give confidence before deployment.

{% endif -%}
---

## Running Tests for Specific Modules

{% if include_tests -%}
```bash
# Test specific module
pytest tests/test_{{ package_name }}_module.py -v

# Test with coverage for module
pytest tests/test_module.py --cov={{ package_name }}.module --cov-report=term-missing

# Test specific function
pytest tests/test_module.py::test_function_name -vv

# Run with debugger on failure
pytest tests/test_module.py --pdb
```

{% endif -%}
{% if include_pre_commit -%}

---

## Fixing Linting/Type Errors

```bash
# Auto-fix linting issues
ruff check --fix src/{{ package_name }}

# Format code
ruff format src/{{ package_name }}

# Check types and show errors
mypy src/{{ package_name }} --pretty --show-error-codes

# Fix specific type error
# Add type: ignore[error-code] comment to problematic line
```
{% endif %}

---

## Troubleshooting

{% if include_tests -%}
### Test Failures

```bash
# Run specific test with verbose output
pytest tests/test_example.py::test_function -vvs

# Show full error trace
pytest --tb=long

# Run with debugger
pytest --pdb

# Check test coverage
pytest --cov={{ package_name }} --cov-report=term-missing

# Clean test cache
pytest --cache-clear
rm -rf .pytest_cache __pycache__
```

{% endif -%}
{% if include_pre_commit -%}
### Type Checking Errors

```bash
# Run mypy with verbose output
mypy src/{{ package_name }} --show-error-codes --pretty

# Check specific file
mypy src/{{ package_name }}/[module].py

# Ignore specific error (if intentional)
# Add to line:
# type: ignore[error-code]

# Update mypy configuration
# Edit [tool.mypy] in pyproject.toml
```

{% endif -%}
{% if include_tests -%}
### Coverage Drop

```bash
# Show missing coverage lines
pytest --cov={{ package_name }} --cov-report=term-missing

# Generate HTML report
pytest --cov={{ package_name }} --cov-report=html
open htmlcov/index.html

# Check coverage for specific module
pytest --cov={{ package_name }}.[module] --cov-report=term-missing

# Identify untested code
coverage report --show-missing
```

{% endif -%}
{% if include_pre_commit -%}
### Pre-Commit Hook Failures

```bash
# Run specific hook
pre-commit run ruff --all-files
pre-commit run mypy --all-files

# Update hook versions
pre-commit autoupdate

# Bypass hooks (emergency only, NOT recommended)
git commit --no-verify

# Clear pre-commit cache
pre-commit clean
```

{% endif -%}

---

## Related Documentation

- **[Main AGENTS.md](../AGENTS.md)** - Project overview, architecture, common tasks
{% if include_memory -%}
- **[Memory System AGENTS.md](../.chora/memory/AGENTS.md)** - Cross-session learning, knowledge management
{% endif -%}
{% if include_docker -%}
- **[Docker AGENTS.md](../docker/AGENTS.md)** - Container operations, deployment
{% endif -%}
- **[scripts/AGENTS.md](../scripts/AGENTS.md)** - Automation scripts reference

---

**End of Testing Guide**

For questions or issues not covered here, see the main [AGENTS.md](../AGENTS.md) or open a GitHub issue.
