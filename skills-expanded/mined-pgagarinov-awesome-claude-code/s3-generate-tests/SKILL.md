---
name: s3-generate-tests
description: Generate pytest test suite for a given module
disable-model-invocation: true
argument-hint: "<module-path>"
---

# S3 — Generate Tests for `$ARGUMENTS`

Generate a comprehensive pytest test suite for the module at `$ARGUMENTS`.

## Project Test Configuration

```
!`cat pyproject.toml | grep -A 15 '\[tool.pytest'`
```

## Existing Test Files

```
!`ls tests/`
```

## Instructions

1. **Read the target module** at `$ARGUMENTS` to understand its public API
2. **Generate tests** following these patterns:

### Test Structure (AAA Pattern)
```python
class TestFunctionName:
    def test_happy_path(self):
        # Arrange
        input_data = ...
        # Act
        result = function_name(input_data)
        # Assert
        assert result == expected

    def test_edge_case(self):
        ...

    def test_error_case(self):
        with pytest.raises(ValueError):
            function_name(bad_input)
```

### Requirements
- One `class` per public function, named `TestFunctionName`
- Use `@pytest.fixture` for shared setup (especially clearing in-memory stores)
- Use `@pytest.mark.parametrize` for input variants
- Test happy path, edge cases, and error cases
- Use `autouse=True` fixtures for store cleanup
- Match the naming and style of existing tests in `tests/`

3. **Write the test file** to `tests/test_<module_name>.py`
4. **Run the tests** to verify they pass
