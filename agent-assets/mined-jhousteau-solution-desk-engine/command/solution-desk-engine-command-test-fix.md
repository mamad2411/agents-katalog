---
allowed-tools: Task, Bash, Read, Write, Edit, Grep, Glob
argument-hint: "[test-path-or-pattern]"
description: "Fix failing tests by treating tests as source of truth, not code"
model: claude-sonnet-4-20250514
---

# Test Fix Workflow

## CRITICAL: Tests Are The Source of Truth

Fix failing tests by analyzing requirements and ensuring code meets test expectations.
Tests define the contract - if tests fail, the code is wrong, not the tests.

## Philosophy

1. **Tests are the specification** - They define what the code SHOULD do
2. **Never fix tests to match broken code** - Fix the code to match test expectations
3. **Remove only obsolete tests** - Tests for removed features or changed requirements
4. **Update tests only for new requirements** - When requirements legitimately change
5. **If no requirement changed and test fails** - The code is broken, fix it

## Workflow

### Phase 1: Analyze Test Failures

```bash
# Run tests to identify failures
make test || pytest [test-path-or-pattern] -v --tb=short

# Capture all failure details
pytest --tb=long --no-header -rN > /tmp/test-failures.txt
```

### Phase 2: Categorize Each Failure

Use issue-analyst agent to categorize each failing test:

1. **Obsolete Test**: Feature was removed or deprecated
   - Action: Remove the test
   - Verify: Check commit history for feature removal

2. **Requirement Changed**: New requirements conflict with old test
   - Action: Update test to match new requirements
   - Verify: Check issue tracker or recent commits for requirement changes

3. **Code Regression**: Code broke, test is correct
   - Action: Fix the code to make test pass
   - Verify: Test represents intended behavior

4. **Implementation Bug**: Code never worked correctly
   - Action: Fix the implementation
   - Verify: Test expectations are reasonable

### Phase 3: Process Each Category

#### For Obsolete Tests:
```bash
# Verify feature removal in git history
git log --grep="remove\|deprecate" --oneline | head -20

# Remove obsolete test files
git rm path/to/obsolete_test.py
```

#### For Changed Requirements:
```bash
# Document the requirement change
echo "Requirement changed: [description]" >> test-changes.log

# Update test to match new requirement
# BUT ONLY if you can prove the requirement actually changed
```

#### For Code Regressions (MOST COMMON):
Use lean-implementer agent to:
1. Read the failing test carefully
2. Understand what it expects
3. Fix the code to meet those expectations
4. Never modify the test unless it has a genuine bug

### Phase 4: Validation

Use build-validator agent:
```bash
# Run specific fixed tests
pytest path/to/fixed_test.py -v

# Run full test suite
make test

# Verify no new failures introduced
pytest --tb=short
```

### Phase 5: Quality Check

Use complexity-auditor agent:
- Ensure fixes don't add unnecessary complexity
- Verify fixes are minimal and focused
- Check that fixes don't break other tests

## Decision Tree

```
Test Failing?
├─> Is the tested feature removed/deprecated?
│   └─> YES: Remove the test
│   └─> NO: Continue
│
├─> Did requirements change?
│   └─> YES: Can you PROVE it with commits/issues?
│       └─> YES: Update test to new requirements
│       └─> NO: Fix the code
│   └─> NO: Continue
│
├─> Is test expectation reasonable?
│   └─> NO: Test has a bug (rare) - fix test
│   └─> YES: Continue
│
└─> Code is broken - FIX THE CODE, NOT THE TEST
```

## Red Flags (Never Do These)

❌ Changing test assertions to match current broken output
❌ Adding skip decorators without justification
❌ Modifying expected values to make tests pass
❌ Weakening test conditions to accommodate bugs
❌ Removing tests because "they're hard to fix"

## Green Flags (Always Do These)

✅ Read test name and docstring to understand intent
✅ Check git history for context on why test exists
✅ Verify test expectations match documented behavior
✅ Fix code to meet test's contract
✅ Keep tests as strict as originally intended
✅ Document why a test was removed (if obsolete)

## Example Scenarios

### Scenario 1: Test Expects Specific Error Message
```python
def test_validation_error_message():
    # Test expects: "Invalid email format"
    # Code returns: "Email invalid"
    # ACTION: Fix code to return expected message
```

### Scenario 2: Test Expects Certain Behavior
```python
def test_file_creation():
    # Test expects: File created with 0644 permissions
    # Code creates: File with 0600 permissions
    # ACTION: Fix code to use correct permissions
```

### Scenario 3: Test No Longer Relevant
```python
def test_deprecated_api_endpoint():
    # Test for: /api/v1/old-endpoint
    # Feature: Removed in commit abc123
    # ACTION: Remove test after verifying removal
```

## Success Criteria

- ✅ All tests pass
- ✅ No tests modified to accommodate bugs
- ✅ Code changes minimal and focused
- ✅ Obsolete tests documented and removed
- ✅ Test suite represents current requirements

## Report Format

After completion, report:
1. Tests fixed by correcting code: X
2. Tests updated for new requirements: Y
3. Tests removed as obsolete: Z
4. Total passing tests: N

Remember: **Tests define truth. If test fails, assume code is wrong until proven otherwise.**
