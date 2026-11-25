---
name: tdd-green
description: Write minimal code to make failing test pass (TDD GREEN phase, language-agnostic)
---

# TDD Green Phase (Language-Agnostic Template)

## Purpose
Write the **minimum code** necessary to make the failing test pass.

This is the **GREEN** phase of Test-Driven Development: make the test pass as quickly and simply as possible.

## Process

### 1. Review the Failing Test
- Read the test that's currently failing
- Understand exactly what behavior it expects
- Note the inputs, outputs, and assertions

### 2. Locate Implementation File
- Find or create the source file that should contain the implementation
- Follow project's file structure and naming conventions
- Import/require necessary dependencies

### 3. Write Minimal Implementation
**Critical mindset: Make it work, not make it perfect.**

- Write the simplest code that will make the test pass
- Don't worry about:
  - Edge cases not covered by current test
  - Performance optimizations
  - Beautiful abstractions
  - Future requirements
- Do focus on:
  - Making THIS test pass
  - Correct behavior for the tested case
  - Clear, readable code

### 4. Run the Tests
- Execute project's test command
- Verify the test NOW PASSES
- Check that no other tests broke

### 5. Run Quality Checks
- Format the code (auto-formatter)
- Check for linting errors
- Verify compilation (if applicable)
- Fix any warnings or errors

### 6. Commit the Implementation
- Commit message: `"Implement <feature>"`
- Both test and implementation are now committed
- The codebase is in a known good state: "feature works"

## Success Criteria

- [ ] Test that was failing now passes
- [ ] All other existing tests still pass
- [ ] Code is formatted according to project standards
- [ ] No linting errors or warnings
- [ ] Code compiles without errors
- [ ] Implementation is simple and focused
- [ ] Implementation is committed with descriptive message

## The "Fake It Till You Make It" Principle

Sometimes the simplest implementation is almost comically simple:

```
# Test expects: calculate_discount(premium_user, product) == 20
# Simplest implementation that passes:
def calculate_discount(user, product):
    return 20
```

**This is valid TDD!** If the test only checks one case, hardcoding is fine. More tests will force better implementation.

## Language-Specific Implementations

This template is implemented by:
- **Elixir**: `/implement-elixir` - Creates modules/functions, runs mix format/test
- **Python**: `/implement-python` - Creates classes/functions, runs black/pytest
- **TypeScript**: `/implement-typescript` - Creates classes/functions, runs prettier/jest
- **Ruby**: `/implement-ruby` - Creates classes/methods, runs rubocop/rspec

## Example Flow

**Test (RED):**
```
test "calculates 20% discount for premium users":
  user = create_premium_user()
  product = create_product(price: 100)
  assert calculate_discount(user, product) == 20
```

**Implementation (GREEN):**
```
def calculate_discount(user, product):
  if user.is_premium:
    return product.price * 0.20
  return 0
```

Simple, focused, makes the test pass.

## Common Mistakes

- **Over-engineering** - Don't add features not tested yet
- **Premature optimization** - Don't worry about performance yet
- **Fixing all edge cases** - Only handle cases covered by current tests
- **Skipping quality checks** - Always format and lint before committing
- **Not running all tests** - Verify nothing else broke

## What's Next

After completing GREEN phase:
1. Look at your implementation - Is it clean and simple?
   - **Yes**: Write next test (back to `/tdd-red`)
   - **No**: Run `/refactor` to clean it up while tests stay green
2. If feature is complete: Move to next feature
3. If more behavior needed: Write next test for edge case

## The Three Rules of TDD (Uncle Bob)

1. **Don't write production code** until you have a failing test
2. **Don't write more of a test** than is sufficient to fail
3. **Don't write more production code** than is sufficient to pass the test

This skill implements rule #3.
