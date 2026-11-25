---
name: refactoring
version: 1.0.0
description: Identify code smells and apply refactoring patterns safely
uses:
  - development/testing
  - development/code-review
requires:
  tools: []
  env: []
security:
  risk_level: write
  capabilities:
    - file:read
    - file:write
  requires_approval: false
---

# Refactoring

Identify code smells and apply refactoring patterns safely — improving code structure without changing behavior. Refactoring is behavior-preserving transformation.

## Execution Model

This is an **agent-handled skill** (`handler: type: agent`). When `refactor` is invoked, you (the agent) apply the methodology below using your reasoning capabilities. There is no backing code — you follow these instructions directly. The tool schema in tool.yaml defines the external contract; this document guides how you fulfill it.

## When to Use

- Code works but is hard to read, maintain, or extend
- Duplicated code needs consolidation
- A function or class has grown too large
- Naming is unclear or misleading
- Preparing code for a new feature (make the change easy, then make the easy change)
- Technical debt reduction

## Methodology

### 1. Identify the Smell

Common code smells and their indicators:

| Smell | Indicator | Refactoring |
|-------|-----------|-------------|
| **Long function** | >30 lines, multiple responsibilities | Extract Method |
| **Large class** | >300 lines, too many fields/methods | Extract Class |
| **Duplicate code** | Same logic in multiple places | Extract Method/Class |
| **Long parameter list** | >4 parameters | Introduce Parameter Object |
| **Feature envy** | Method uses another object's data more than its own | Move Method |
| **Data clumps** | Same group of fields/params appears together | Extract Class |
| **Primitive obsession** | Using primitives instead of small objects | Replace Primitive with Object |
| **Switch statements** | Long switch/if-else chains on type | Replace with Polymorphism |
| **Speculative generality** | Abstract classes/interfaces with one implementation | Collapse Hierarchy |
| **Dead code** | Unreachable or unused code | Remove Dead Code |

### 2. Ensure Safety Net

Before refactoring:
1. **Run existing tests** — confirm they pass (this is your safety net)
2. **Identify affected code** — what files and functions will change?
3. **Check for callers** — who calls the code being refactored?
4. **Verify test coverage** — are the areas you'll change covered by tests?

If test coverage is insufficient, **write tests first** before refactoring.

### 3. Plan the Refactoring

For each refactoring step:
- What pattern are you applying? (Extract Method, Move Method, etc.)
- What is the expected result?
- How will you verify it worked?

### 4. Execute in Small Steps

**Critical rule**: Refactor in small, verifiable steps. Each step should:
1. Be a single, well-defined transformation
2. Keep the code compilable/runnable
3. Pass all existing tests
4. Be committable on its own

**Never** do a "big bang" refactoring that changes everything at once.

### 5. Verify After Each Step

After each transformation:
1. Run the test suite — all tests must pass
2. Review the change — does the code read better?
3. Check for regressions — does behavior remain the same?

### 6. Assess the Result

After completing the refactoring:
- Is the code more readable?
- Is the code more maintainable?
- Is the code easier to extend?
- Has complexity decreased (fewer branches, smaller functions)?
- Are all tests still passing?

## Output Format

```
## Refactoring: [Target]

### Smells Identified
| # | Smell | Location | Severity |
|---|-------|----------|----------|
| 1 | [smell] | [file:line] | [high/medium/low] |

### Refactoring Plan
| Step | Pattern | Before | After |
|------|---------|--------|-------|
| 1 | [pattern] | [current state] | [target state] |

### Execution
| Step | Status | Tests |
|------|--------|-------|
| 1 | [done/skipped] | [pass/fail] |

### Result
- Readability: [improved/unchanged]
- Maintainability: [improved/unchanged]
- Complexity: [reduced/unchanged]
- Tests: [all passing]
- Lines changed: [count]
```

## Quality Criteria

- Existing tests pass before, during, and after refactoring
- Each step is small and verifiable
- Behavior is preserved (refactoring, not rewriting)
- Code is measurably improved (readability, maintainability, complexity)
- No new functionality is added during refactoring
- Callers of refactored code are updated
- Changes are committable at each step

## Common Mistakes

- **Refactoring without tests**: Changing code structure without a test safety net means you can't verify behavior is preserved.
- **Big bang refactoring**: Changing everything at once makes it impossible to diagnose what broke. Small steps, verify after each.
- **Adding features during refactoring**: Refactoring and feature work are separate activities. "While I'm here, I'll also add..." leads to untraceable bugs.
- **Refactoring code you don't understand**: If you don't know what the code does, you can't verify you preserved its behavior. Understand first, then refactor.
- **Over-refactoring**: Three lines of similar code don't always need extraction. The cure (abstraction) can be worse than the disease (duplication) if the duplication is coincidental.
- **Ignoring callers**: Renaming a method or changing its signature without updating all callers. Check references before and after.
- **Not committing between steps**: Each step should be committable. If step 5 breaks something, you can revert to step 4 instead of starting over.

## Completion

Refactoring is complete when:
- Code smells are identified and prioritized
- Refactoring is executed in small, verified steps
- All existing tests pass after each step
- Behavior is preserved (no functional changes)
- Code quality is measurably improved
- Changes are committed
