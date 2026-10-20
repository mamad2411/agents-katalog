// Command: /test-all-functions
// Description: Generate and execute tests for EVERY function in the codebase

You are executing a comprehensive testing workflow that will:
1. Discover every function in the entire codebase
2. Generate tests for functions without tests
3. Execute all tests and identify errors
4. Create a detailed coverage report

## Workflow Steps:

### 1. Function Discovery
Scan all files and identify:
- Python functions (including async, decorated, class methods)
- JavaScript/TypeScript functions (arrow, regular, exported)
- React components and hooks
- API endpoints
- Utility functions

### 2. Test Analysis
For each function, determine:
- Current test coverage
- Complexity score
- Dependencies
- Side effects
- Error handling needs

### 3. Test Generation Strategy
Create tests that cover:
- **Happy Path**: Normal expected behavior
- **Edge Cases**: Boundary conditions, empty inputs, large inputs
- **Error Cases**: Invalid inputs, exceptions, timeouts
- **Type Safety**: Wrong types, null/undefined handling
- **Async Behavior**: Promises, callbacks, race conditions
- **State Management**: For React components
- **Integration**: How functions work together

### 4. Test Implementation
```python
# Example for Python function
def test_{function_name}_happy_path():
    """Test normal operation"""
    result = function_name(valid_input)
    assert result == expected_output

def test_{function_name}_edge_cases():
    """Test boundary conditions"""
    assert function_name([]) == default_value
    assert function_name(None) raises TypeError

def test_{function_name}_error_handling():
    """Test error scenarios"""
    with pytest.raises(ValueError):
        function_name(invalid_input)

@pytest.mark.parametrize("input,expected", [
    (case1, result1),
    (case2, result2),
])
def test_{function_name}_parameterized(input, expected):
    """Test multiple scenarios"""
    assert function_name(input) == expected
```

### 5. Execution and Validation
Run tests with:
- Coverage reporting
- Performance benchmarking
- Error categorization
- Flaky test detection

### 6. Report Generation
Create comprehensive report showing:
- Total functions found
- Test coverage percentage
- High-risk untested functions
- Performance bottlenecks
- Recommendations for improvement

## Usage Example:
```bash
# Full comprehensive testing
python src/backend/services/comprehensive_test_orchestrator.py

# Only generate tests
python src/backend/services/comprehensive_test_orchestrator.py --generate-only

# Only execute tests
python src/backend/services/comprehensive_test_orchestrator.py --execute-only

# Target specific directory
python src/backend/services/comprehensive_test_orchestrator.py --target src/backend/services
```

## Expected Output:
- `tests/generated/` - All generated test files
- `test_coverage_report.json` - Detailed coverage report
- Console output showing progress and results

## Quality Criteria:
- 100% function coverage (every function has at least one test)
- 90%+ line coverage
- All edge cases covered
- Error handling validated
- No flaky tests

Remember:
- Don't just test the happy path
- Consider all possible inputs
- Test error conditions explicitly
- Validate async behavior
- Check performance implications
