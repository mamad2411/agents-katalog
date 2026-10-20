# Claude Test Generation Patterns

**Purpose:** Claude-specific patterns for test generation and coverage optimization.

**Parent:** See [../CLAUDE.md](../CLAUDE.md) for project-level Claude guidance and [AGENTS.md](AGENTS.md) for generic testing guide.

---

## Claude's Testing Strengths

Claude excels at test generation because:

- **Comprehensive edge case identification** - Thinks through scenarios humans might miss
- **Pattern recognition** - Follows project test patterns consistently
- **Fixture generation** - Creates appropriate mocks and fixtures
- **Documentation** - Writes clear test docstrings
- **Coverage optimization** - Targets untested code paths

---

## Test Generation Template

### Complete Test Request Pattern

```markdown
# Test Generation Request

## Code to Test
[Paste function/class/module]

## Testing Requirements

**Coverage target:** {{ test_coverage_threshold }}%
**Framework:** pytest
**Patterns:** Follow tests/conftest.py fixtures

### Test Categories
1. ✅ Happy path (valid inputs, expected behavior)
2. ✅ Edge cases (empty, None, boundary values)
3. ✅ Error conditions (invalid inputs, exceptions)
4. ✅ Integration (if interacts with other components)

### Specific Scenarios
- [Scenario 1 to test]
- [Scenario 2 to test]
- [Scenario 3 to test]

### Mocking Strategy
Mock these external dependencies:
- [Dependency 1]: Use [specific mock/fixture]
- [Dependency 2]: Use [specific mock/fixture]

## Example Test Structure
```python
def test_function_scenario_expected(fixture):
    """Test that function handles scenario correctly.

    Verifies:
    - [Specific behavior 1]
    - [Specific behavior 2]
    """
    # Arrange
    input_data = ...
    expected = ...

    # Act
    result = function(input_data)

    # Assert
    assert result == expected
```

---

Claude, generate tests following this pattern:
1. Use pytest fixtures from conftest.py
2. Parametrize multiple scenarios where appropriate
3. Clear arrange-act-assert structure
4. Descriptive docstrings
5. Target {{ test_coverage_threshold }}% coverage
```

---

## Fixture Pattern Recognition

### Claude-Optimized Fixture Requests

**Pattern 1: Analyze Existing Fixtures**

```markdown
"Review fixtures in tests/conftest.py:

[Paste conftest.py]

Generate tests for [module] using these existing fixtures.
Follow the same patterns and naming conventions."
```

**Pattern 2: Request New Fixtures**

```markdown
"Create pytest fixture for [dependency]:

Purpose: [what it mocks/provides]
Scope: [function, class, module, session]
Pattern: Follow fixtures in tests/conftest.py

Example usage in test:
```python
def test_example(new_fixture):
    # Test using fixture
```
```

### Common Fixture Patterns

```python
# Fixture pattern Claude should follow
@pytest.fixture
def mock_external_api():
    """Mock external API for testing.

    Returns Mock object with common methods stubbed.
    """
    mock = Mock()
    mock.fetch.return_value = {"status": "success"}
    mock.post.return_value = {"id": "123"}
    return mock

@pytest.fixture
def sample_data():
    """Sample data for testing.

    Returns representative test data.
    """
    return {
        "id": "test-id",
        "name": "Test Name",
        "value": 42
    }
```

---

## Parametrized Test Pattern

### When to Use Parametrization

**Good for:**
- Testing multiple input variations
- Boundary value testing
- Testing similar scenarios with different data

### Claude Parametrization Request

```markdown
"Generate parametrized test for [function]:

Test these scenarios:
1. [Scenario 1] - input: [X], expected: [Y]
2. [Scenario 2] - input: [X], expected: [Y]
3. [Scenario 3] - input: [X], expected: [Y]

Use @pytest.mark.parametrize for clean implementation."
```

### Expected Pattern

```python
@pytest.mark.parametrize("input_val,expected", [
    ("valid_input", {"status": "success"}),
    ("edge_case", {"status": "success", "warning": "edge"}),
    ("boundary", {"status": "success", "count": 0}),
])
def test_function_scenarios(input_val, expected):
    """Test function with various inputs."""
    result = function(input_val)
    assert result == expected
```

---

## Coverage Optimization with Claude

### Identify Untested Code

```markdown
"Current test coverage report:

[Paste pytest --cov output showing uncovered lines]

Generate tests to cover these uncovered lines:
- File: [file], Lines: [line numbers]

Focus on:
1. Error handling paths
2. Edge cases
3. Conditional branches
```

### Coverage-Driven Test Generation

```python
# Claude can target specific uncovered lines
def test_error_handling_line_45():
    """Test error path at line 45 that's uncovered."""
    with pytest.raises(ValueError, match="Invalid input"):
        function_with_error(invalid_input)
```

---

## Integration Test Patterns

### MCP Tool Integration Tests

```markdown
"Generate integration test for MCP tool:

Tool: [tool_name]
Integration point: [external API/database/other service]

Test full workflow:
1. Tool receives request
2. Calls external dependency
3. Processes response
4. Returns to caller

Mock external dependencies, test integration logic."
```

### Pattern for MCP Tools

```python
def test_mcp_tool_integration(mock_external_api, mcp_server):
    """Test MCP tool end-to-end workflow.

    Verifies:
    - Tool accepts MCP protocol request
    - Calls external API correctly
    - Handles API response
    - Returns MCP protocol response
    """
    # Arrange
    mock_external_api.fetch.return_value = {"data": "result"}

    # Act
    result = mcp_server.call_tool("tool_name", {"param": "value"})

    # Assert
    assert result["status"] == "success"
    assert result["data"] == "result"
    mock_external_api.fetch.assert_called_once_with("value")
```

---

## Async Test Patterns

### Claude Async Test Generation

```markdown
"Generate async tests for [async_function]:

Use pytest-asyncio
Test async/await patterns
Handle async context managers
Test concurrent operations if applicable"
```

### Expected Async Pattern

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    """Test async function behavior."""
    # Arrange
    input_data = ...

    # Act
    result = await async_function(input_data)

    # Assert
    assert result == expected

@pytest.mark.asyncio
async def test_async_with_context_manager():
    """Test async context manager usage."""
    async with async_context() as ctx:
        result = await ctx.method()
        assert result is not None
```

---

## Error Testing Patterns

### Exception Testing

```markdown
"Generate tests for error conditions in [function]:

Error scenarios:
1. Invalid input → ValueError
2. Missing dependency → RuntimeError
3. Network failure → ConnectionError

Use pytest.raises with match for error messages."
```

### Claude Error Test Pattern

```python
def test_function_raises_on_invalid_input():
    """Test that function raises ValueError for invalid input."""
    with pytest.raises(ValueError, match="Input must be positive"):
        function(invalid_input=-1)

def test_function_handles_missing_dependency():
    """Test graceful handling when dependency unavailable."""
    with pytest.raises(RuntimeError, match="Dependency not configured"):
        function_requiring_dependency()
```

---

## Test Documentation Patterns

### Docstring Pattern for Claude

```markdown
"Generate tests with comprehensive docstrings:

Format:
```python
def test_function_scenario():
    \"\"\"Test that function does X when Y.

    This test verifies:
    - Specific behavior 1
    - Specific behavior 2
    - Edge case handling

    Uses:
    - fixture_1: Purpose
    - fixture_2: Purpose
    \"\"\"
```
```

### Documentation Value

- **Explain "why"** - Not just what test does, but why it matters
- **List verifications** - What specific behaviors are checked
- **Note fixtures** - What fixtures are used and why
- **Edge cases** - Why this edge case is important

---

## Continuous Testing Workflow

### Test-Driven Development with Claude

```markdown
# TDD Workflow with Claude

## Step 1: Write Failing Test
"Write failing test for [feature] that should:
- Input: [X]
- Output: [Y]
- Error if: [Z]

Don't implement the function yet, just the test."

## Step 2: Implement to Pass
"Now implement [feature] to make the test pass.
Minimal implementation - just enough to go green."

## Step 3: Refactor
"Refactor [feature] to improve [aspect]:
- All tests must still pass
- Improve readability/performance/etc."

## Step 4: Add Edge Cases
"Add tests for edge cases:
- [Edge case 1]
- [Edge case 2]

Then update implementation to handle them."
```

---

## Metrics Tracking for Tests

### Test Quality Metrics

```python
# Track test quality in checkpoints
"""
Test Metrics:
- Coverage: {{ test_coverage_threshold }}% (target met ✅)
- Tests added: 15
- Edge cases: 8
- Error paths: 5
- Integration tests: 2

Quality:
- All tests pass ✅
- No flaky tests ✅
- Clear docstrings ✅
- Appropriate mocks ✅
"""
```

---

## Common Test Patterns in {{ project_name }}

### Pattern 1: MCP Tool Tests

```python
def test_mcp_tool_happy_path():
    """Test MCP tool with valid input."""
    result = call_tool("tool_name", {"param": "value"})
    assert result["status"] == "success"

def test_mcp_tool_error_handling():
    """Test MCP tool handles errors gracefully."""
    result = call_tool("tool_name", {"param": "invalid"})
    assert result["status"] == "error"
    assert "message" in result
```

### Pattern 2: Utility Function Tests

```python
def test_utility_function():
    """Test utility function behavior."""
    # Use AAA pattern (Arrange-Act-Assert)
    input_data = {...}
    expected = {...}

    result = utility_function(input_data)

    assert result == expected
```

### Pattern 3: Error Formatter Tests

```python
def test_error_formatter_not_found():
    """Test ErrorFormatter.not_found generates helpful message."""
    msg = ErrorFormatter.not_found(
        entity_type="server",
        entity_id="missing",
        available=["server1", "server2"]
    )
    assert "server 'missing' not found" in msg.lower()
    assert "server1" in msg
    assert "server2" in msg
```

---

## Troubleshooting Test Generation

### Problem: Tests Too Generic

**Solution:** Provide specific scenarios

```markdown
"Tests are too generic. Generate tests for these specific scenarios:
1. [Concrete scenario 1 with exact input/output]
2. [Concrete scenario 2 with exact input/output]

Use actual data values, not placeholder variables."
```

### Problem: Mocking Not Working

**Solution:** Specify exact mocking approach

```markdown
"Mock [dependency] using this pattern:

```python
@pytest.fixture
def mock_dependency(monkeypatch):
    mock = Mock()
    mock.method.return_value = expected_value
    monkeypatch.setattr('module.path.dependency', mock)
    return mock
```

Follow this exact pattern for consistency."
```

### Problem: Low Coverage Despite Tests

**Solution:** Request coverage report analysis

```markdown
"Coverage is {{ coverage }}% but target is {{ test_coverage_threshold }}%.

Coverage report:
[Paste pytest --cov report]

Identify uncovered lines and generate targeted tests."
```

---

## Best Practices for Claude Test Generation

### ✅ Do's

1. **Provide existing test examples** - Claude learns project patterns
2. **Specify coverage target** - Claude will generate comprehensive tests
3. **List specific scenarios** - Gets concrete tests, not generic
4. **Include fixture context** - Leverages existing test infrastructure
5. **Request arrange-act-assert** - Gets clean, readable tests
6. **Ask for docstrings** - Documents test purpose

### ❌ Don'ts

1. **Don't request without context** - Needs to see project patterns
2. **Don't skip edge cases** - Claude excels at comprehensive coverage
3. **Don't ignore fixtures** - Wastes effort recreating setup
4. **Don't accept generic tests** - Push for specific, meaningful tests
5. **Don't forget async patterns** - Specify if async tests needed

---

**See Also:**
- [../CLAUDE.md](../CLAUDE.md) - Project-level Claude patterns
- [AGENTS.md](AGENTS.md) - Generic testing guide
- [../../claude/FRAMEWORK_TEMPLATES.md](../../claude/FRAMEWORK_TEMPLATES.md) - Test generation template in pattern library

---

**Version:** 3.3.0
**Last Updated:** 2025-10-26
