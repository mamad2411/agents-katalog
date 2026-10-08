---
name: refactor-code
description: Systematically refactor code based on analysis, applying improvements while maintaining functionality. Use when the user asks to "refactor this code", "improve code quality", "apply improvements", "fix anti-patterns", "optimize performance", or mentions "clean up code", "make it more maintainable", or "reduce complexity". Works best when an implementation_plan.md exists.
---

# Code Refactoring Skill

This skill systematically applies code improvements based on analysis, ensuring quality, maintainability, and correctness through iterative changes and comprehensive verification.

## When to Use This Skill

Trigger this skill when users ask to:
- Refactor or improve code quality
- Apply recommendations from code analysis
- Fix anti-patterns or code smells
- Optimize performance or scalability
- Reduce complexity or technical debt
- Make code more maintainable
- Clean up or modernize code

**Best Practice**: Run the `analyze-code` skill first to create `implementation_plan.md`, then use this skill to implement the recommendations.

## Refactoring Methodology

### 1. Review Implementation Plan

**Look for existing analysis:**
- Check for `implementation_plan.md` in the current directory
- If it exists, read it to understand the proposed changes
- If it doesn't exist, ask the user if they want to run `analyze-code` first
- Identify the priority order: Critical → Moderate → Minor issues

**If no plan exists:**
- Ask the user to describe specific improvements they want
- Perform quick analysis to understand current code structure
- Document the planned changes before starting

### 2. Prepare for Refactoring

**Before making changes:**
- Read all files that will be modified
- Understand current functionality and behavior
- Identify existing tests (unit tests, integration tests)
- Check for dependencies between files
- Look for configuration files that may need updates

**Create a work plan:**
- Break refactoring into small, focused steps
- Prioritize changes that maintain backward compatibility
- Plan test strategy for each change
- Identify rollback points if issues arise

### 3. Apply Changes Iteratively

**Golden Rule: One Change at a Time**

For each improvement:

1. **Make focused change**: Modify only what's needed for THIS improvement
2. **Verify immediately**: Run tests or validation after EACH change
3. **Fix if broken**: If tests fail, fix immediately before proceeding
4. **Commit mentally**: Confirm the change is stable before the next one

**Keep refactoring separate from features:**
- Do NOT add new functionality while refactoring
- Do NOT mix multiple refactoring types in one step
- Do NOT change behavior unless that's the explicit goal
- Focus: "Make the code better while keeping it doing the same thing"

**Common refactoring patterns:**

**Extract Method/Function:**
```python
# Before: Long method with multiple responsibilities
def process_user_data(data):
    # validate
    if not data.get('email'):
        raise ValueError('Email required')
    if '@' not in data['email']:
        raise ValueError('Invalid email')
    # transform
    clean_data = {
        'email': data['email'].lower().strip(),
        'name': data.get('name', '').strip()
    }
    # save
    db.save(clean_data)

# After: Separated concerns
def validate_user_data(data):
    if not data.get('email'):
        raise ValueError('Email required')
    if '@' not in data['email']:
        raise ValueError('Invalid email')

def transform_user_data(data):
    return {
        'email': data['email'].lower().strip(),
        'name': data.get('name', '').strip()
    }

def process_user_data(data):
    validate_user_data(data)
    clean_data = transform_user_data(data)
    db.save(clean_data)
```

**Replace Magic Numbers with Constants:**
```python
# Before
if user.age < 18:
    return False

# After
MINIMUM_AGE = 18
if user.age < MINIMUM_AGE:
    return False
```

**Remove Duplication:**
```python
# Before
def get_active_users():
    return db.query(User).filter(User.is_active == True).all()

def get_active_admins():
    return db.query(User).filter(User.is_active == True, User.is_admin == True).all()

# After
def get_users_by_filters(**filters):
    query = db.query(User)
    for field, value in filters.items():
        query = query.filter(getattr(User, field) == value)
    return query.all()

def get_active_users():
    return get_users_by_filters(is_active=True)

def get_active_admins():
    return get_users_by_filters(is_active=True, is_admin=True)
```

**Improve Naming:**
```python
# Before
def calc(x, y):
    return x * y * 0.0762

# After
def calculate_area_square_feet(width_inches, height_inches):
    SQUARE_INCHES_TO_SQUARE_FEET = 0.0762
    area_square_inches = width_inches * height_inches
    return area_square_inches * SQUARE_INCHES_TO_SQUARE_FEET
```

**Reduce Nesting:**
```python
# Before
def process(data):
    if data:
        if data.is_valid():
            if data.has_permission():
                result = data.process()
                if result:
                    return result.value
    return None

# After (Guard Clauses)
def process(data):
    if not data:
        return None
    if not data.is_valid():
        return None
    if not data.has_permission():
        return None

    result = data.process()
    return result.value if result else None
```

**Replace Conditionals with Polymorphism:**
```python
# Before
def calculate_price(product):
    if product.type == 'book':
        return product.base_price * 0.9
    elif product.type == 'electronics':
        return product.base_price * 1.1
    elif product.type == 'clothing':
        return product.base_price
    return product.base_price

# After
class Product:
    def calculate_price(self):
        return self.base_price

class Book(Product):
    def calculate_price(self):
        return self.base_price * 0.9

class Electronics(Product):
    def calculate_price(self):
        return self.base_price * 1.1

class Clothing(Product):
    def calculate_price(self):
        return self.base_price
```

### 4. Update Documentation and Comments

**Update affected documentation:**
- Update docstrings if function signatures change
- Update README if public API changes
- Update inline comments if logic changes
- Remove outdated comments (code should be self-documenting when possible)

**Don't over-document:**
- Don't add comments that just repeat the code
- Don't add docstrings to private implementation details
- Don't document the obvious
- Focus comments on "why", not "what"

### 5. Comprehensive Verification

**Automated Testing (Priority 1):**

Run existing tests after each change:
```bash
# Python example
python -m pytest tests/

# JavaScript example
npm test

# Specific test file
pytest tests/test_specific.py -v
```

If tests fail:
- **STOP**: Do not proceed to next refactoring
- **ANALYZE**: Understand why the test failed
- **FIX**: Correct the refactoring or update the test
- **VERIFY**: Re-run tests until they pass

**Manual Verification (Priority 2):**

When automated tests are insufficient:
- Run the application locally
- Test affected user flows manually
- Check edge cases and boundary conditions
- Verify error handling behavior

**Performance Benchmarking (Priority 3):**

If the refactoring aimed to improve performance:
```python
# Before refactoring
import time
start = time.time()
old_function(large_input)
old_time = time.time() - start

# After refactoring
start = time.time()
new_function(large_input)
new_time = time.time() - start

print(f"Improvement: {(old_time - new_time) / old_time * 100:.1f}%")
```

**Code Quality Checks:**

Run linters and formatters:
```bash
# Python
ruff check .
ruff format .
mypy .

# JavaScript
eslint src/
prettier --write src/

# General
# Run any pre-commit hooks
```

### 6. Handle Test Failures

**If tests fail after refactoring:**

1. **Understand the failure**:
   - Read the error message carefully
   - Identify which test failed and why
   - Determine if it's a real bug or an outdated test

2. **Categorize the issue**:
   - **Real bug**: Your refactoring broke functionality → Fix the code
   - **Outdated test**: Test expectations need updating → Update the test
   - **Missing test coverage**: Refactoring exposed untested behavior → Add tests

3. **Fix appropriately**:
   ```python
   # Real bug example: Fixed implementation
   def calculate_total(items):
       # BUG: Forgot to handle empty list after refactoring
       if not items:  # FIX: Add guard clause
           return 0
       return sum(item.price for item in items)

   # Outdated test example: Update test expectations
   def test_calculate_total():
       # Before: Test expected None for empty list
       # assert calculate_total([]) is None

       # After: Updated to match new behavior
       assert calculate_total([]) == 0
   ```

4. **Verify the fix**:
   - Re-run the specific test
   - Run the full test suite
   - Check for related test failures

### 7. Track Progress

**Use TodoWrite tool to track refactoring steps:**

Create a todo for each change from the implementation plan:
```markdown
- [ ] Extract validation logic to separate function
- [ ] Replace magic numbers with named constants
- [ ] Add error handling for edge cases
- [ ] Update tests for new structure
- [ ] Run performance benchmarks
```

Update status after each step:
- Mark as `in_progress` when starting
- Mark as `completed` after verification passes
- Add new todos if issues are discovered

## Important Guidelines

**Safety First:**
- Never skip tests
- Make changes incrementally, not all at once
- Keep working versions (mentally note rollback points)
- If uncertain, ask the user before major structural changes

**Maintain Functionality:**
- Refactoring should NOT change behavior (unless that's the goal)
- All existing tests should pass (or be updated intentionally)
- Don't introduce new features while refactoring
- Don't remove functionality without user approval

**Focus and Scope:**
- Refactor only what was analyzed or requested
- Don't expand scope without asking
- Don't "improve" code that's not part of the task
- Don't add unnecessary abstractions

**Code Style:**
- Follow the existing code style in the project
- Use language/framework idioms
- Be consistent with naming conventions
- Match the abstraction level of surrounding code

**Performance:**
- Don't optimize prematurely
- Measure before and after if claiming performance improvement
- Consider readability vs. performance trade-offs
- Document performance-critical sections

## Refactoring Workflow

```
1. READ implementation_plan.md (or create quick plan)
   ↓
2. READ all files to be modified
   ↓
3. For each improvement (in priority order):
   ↓
   a. Make focused change using Edit tool
   ↓
   b. IMMEDIATELY verify with tests/validation
   ↓
   c. If tests FAIL → FIX before continuing
   ↓
   d. If tests PASS → Mark todo as complete, move to next
   ↓
4. Final verification:
   - Run full test suite
   - Check manual test cases
   - Run benchmarks if applicable
   - Run linters/formatters
   ↓
5. Report completion with summary
```

## Output and Reporting

**After each change:**
- Briefly describe what was changed
- Report test results (pass/fail)
- Note any issues encountered and how they were resolved

**Final summary:**
```markdown
## Refactoring Complete

### Changes Applied
1. ✅ [Change 1] - [Files modified] - Tests passing
2. ✅ [Change 2] - [Files modified] - Tests passing
3. ✅ [Change 3] - [Files modified] - Tests passing

### Verification Results
- **Automated Tests**: All passing (X/X tests)
- **Manual Testing**: [User flows tested]
- **Performance**: [Benchmark results if applicable]
- **Code Quality**: [Linter results]

### Files Modified
- `path/to/file1.py`: [Description of changes]
- `path/to/file2.py`: [Description of changes]

### Recommendations
- [Any follow-up suggestions]
- [Additional improvements identified but not implemented]
```

## Example Usage

**User:** "Refactor the authentication module based on the analysis"

**Skill Actions:**
1. Read `implementation_plan.md`
2. Create todo list from planned changes
3. For each change:
   - Apply improvement using Edit tool
   - Run `pytest tests/test_auth.py`
   - Verify tests pass
   - Mark todo complete
4. Final checks:
   - Run full test suite
   - Test login/logout flows manually
   - Run security checks
5. Report summary of changes and verification results

**User:** "Improve the performance of the data processing pipeline"

**Skill Actions:**
1. Read implementation plan or ask for specific goals
2. Apply optimizations iteratively:
   - Replace nested loops with vectorized operations
   - Run benchmark to measure improvement
   - Add streaming for large datasets
   - Run benchmark again
   - Add parallel processing
   - Final benchmark
3. Verify:
   - All data processing tests pass
   - Performance improved by X%
   - Memory usage reduced
4. Report before/after metrics
